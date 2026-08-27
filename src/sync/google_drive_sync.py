"""
Google Drive Sync - Sincronización con Google Drive
"""

from typing import Optional, List, Dict
import logging
import os
from pathlib import Path
from datetime import datetime

from .base_drive_sync import BaseDriveSync, SyncResult

logger = logging.getLogger(__name__)


class GoogleDriveSync(BaseDriveSync):
    """
    Sincronizador con Google Drive

    Usa Google Drive API para backup automático de:
    - Base de datos SQLite
    - Imágenes generadas
    - Videos compilados
    """

    def __init__(self, config: dict, credentials_path: str = "credentials.json"):
        """
        Inicializar sincronizador Google Drive

        Args:
            config: Configuración del proyecto
            credentials_path: Ruta a archivo de credenciales
        """
        super().__init__(config)

        self.credentials_path = credentials_path
        self.service = None
        self.carpeta_root_id = None

        # Intentar inicializar cliente de Google Drive
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
            from google.auth import default as auth_default

            self.google_importado = True
            self._inicializar_cliente()
            logger.info("✓ Cliente Google Drive inicializado")

        except ImportError:
            self.google_importado = False
            logger.warning("Librería google-auth-oauthlib no disponible. Modo fallback activado.")
        except Exception as e:
            self.google_importado = False
            logger.warning(f"Error inicializando Google Drive: {e}. Modo fallback activado.")

    def _inicializar_cliente(self):
        """Inicializar cliente de Google Drive API"""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            # Intentar con credenciales de service account
            if Path(self.credentials_path).exists():
                scopes = ['https://www.googleapis.com/auth/drive']
                creds = Credentials.from_service_account_file(
                    self.credentials_path,
                    scopes=scopes
                )
                self.service = build('drive', 'v3', credentials=creds)
                logger.info("✓ Autenticado con service account")

            else:
                logger.warning(f"Archivo de credenciales no encontrado: {self.credentials_path}")
                logger.info("  Instrucciones: Crear credentials.json desde Google Cloud Console")

        except Exception as e:
            logger.error(f"Error inicializando cliente: {e}")
            self.service = None

    def _sincronizar_impl(self, ruta_bd: str, ruta_imagenes: Optional[str],
                         ruta_videos: Optional[str]) -> SyncResult:
        """
        Sincronizar archivos a Google Drive

        Args:
            ruta_bd: Ruta a base de datos
            ruta_imagenes: Ruta a carpeta imágenes
            ruta_videos: Ruta a carpeta videos

        Returns:
            SyncResult con detalles
        """
        if not self.google_importado or not self.service:
            logger.warning("Google Drive no disponible, usando fallback")
            return self._sincronizar_fallback(ruta_bd, ruta_imagenes, ruta_videos)

        try:
            resultado = SyncResult(exitoso=True)
            archivos_subidos = 0

            # Crear estructura de carpetas
            self._crear_estructura_carpetas()

            # Subir base de datos
            if self._validar_archivo(ruta_bd):
                exito = self._subir_archivo(ruta_bd, self.carpeta_sync)
                if exito:
                    archivos_subidos += 1
                    tamaño = self._obtener_tamaño_archivo(ruta_bd)
                    resultado.tamaño_bytes += tamaño
                    resultado.detalles.append(f"BD: {Path(ruta_bd).name}")
                else:
                    resultado.archivos_fallo += 1

            # Subir imágenes
            if ruta_imagenes and Path(ruta_imagenes).exists():
                imagenes = self._obtener_archivos_carpeta(ruta_imagenes, ['.jpg', '.png', '.webp'])
                for imagen in imagenes:
                    exito = self._subir_archivo(imagen, self.carpeta_imagenes)
                    if exito:
                        archivos_subidos += 1
                        resultado.tamaño_bytes += self._obtener_tamaño_archivo(imagen)
                    else:
                        resultado.archivos_fallo += 1

            # Subir videos
            if ruta_videos and Path(ruta_videos).exists():
                videos = self._obtener_archivos_carpeta(ruta_videos, ['.mp4', '.webm', '.avi'])
                for video in videos:
                    exito = self._subir_archivo(video, self.carpeta_videos)
                    if exito:
                        archivos_subidos += 1
                        resultado.tamaño_bytes += self._obtener_tamaño_archivo(video)
                    else:
                        resultado.archivos_fallo += 1

            resultado.archivos_sincronizados = archivos_subidos
            resultado.exitoso = resultado.archivos_fallo == 0
            resultado.mensaje = f"Sincronizados {archivos_subidos} archivos"

            return resultado

        except Exception as e:
            logger.error(f"Error en sincronización Google Drive: {e}", exc_info=True)
            return SyncResult(exitoso=False, mensaje=str(e))

    def _crear_estructura_carpetas(self):
        """Crear estructura de carpetas en Google Drive si no existe"""
        try:
            if not self.service:
                return

            # Crear/obtener carpeta raíz
            self.carpeta_root_id = self._obtener_o_crear_carpeta(self.carpeta_sync, None)

            # Crear subcarpetas
            if self.carpeta_root_id:
                self._obtener_o_crear_carpeta(self.carpeta_imagenes, self.carpeta_root_id)
                self._obtener_o_crear_carpeta(self.carpeta_videos, self.carpeta_root_id)

            logger.debug("✓ Estructura de carpetas verificada")

        except Exception as e:
            logger.error(f"Error creando carpetas: {e}")

    def _obtener_o_crear_carpeta(self, nombre: str, parent_id: Optional[str]) -> Optional[str]:
        """
        Obtener ID de carpeta o crear si no existe

        Args:
            nombre: Nombre de la carpeta
            parent_id: ID de carpeta padre (None = raíz)

        Returns:
            ID de la carpeta o None
        """
        try:
            if not self.service:
                return None

            # Buscar carpeta existente
            query = f"name='{nombre}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            else:
                query += " and 'root' in parents"

            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()

            files = results.get('files', [])

            if files:
                return files[0]['id']

            # Crear carpeta si no existe
            file_metadata = {
                'name': nombre,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]

            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            logger.debug(f"✓ Carpeta creada: {nombre}")
            return folder.get('id')

        except Exception as e:
            logger.error(f"Error obteniendo/creando carpeta: {e}")
            return None

    def _subir_archivo(self, ruta_archivo: str, carpeta_nombre: str) -> bool:
        """
        Subir archivo a Google Drive

        Args:
            ruta_archivo: Ruta local del archivo
            carpeta_nombre: Nombre de carpeta destino

        Returns:
            True si exitoso
        """
        try:
            if not self.service or not self._validar_archivo(ruta_archivo):
                return False

            from googleapiclient.http import MediaFileUpload

            archivo_path = Path(ruta_archivo)
            archivo_nombre = archivo_path.name

            # Obtener ID de carpeta destino
            carpeta_id = None
            if carpeta_nombre == self.carpeta_sync:
                carpeta_id = self.carpeta_root_id
            else:
                # Buscar subcarpeta
                query = f"name='{carpeta_nombre}' and mimeType='application/vnd.google-apps.folder'"
                results = self.service.files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id)',
                    pageSize=1
                ).execute()
                files = results.get('files', [])
                if files:
                    carpeta_id = files[0]['id']

            if not carpeta_id:
                logger.warning(f"Carpeta no encontrada: {carpeta_nombre}")
                return False

            # Subir archivo
            file_metadata = {
                'name': archivo_nombre,
                'parents': [carpeta_id]
            }
            media = MediaFileUpload(ruta_archivo, resumable=True)

            file_obj = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            logger.debug(f"✓ Archivo subido: {archivo_nombre}")
            return True

        except Exception as e:
            logger.error(f"Error subiendo archivo: {e}")
            return False

    def _obtener_archivos_carpeta(self, ruta_carpeta: str,
                                 extensiones: List[str]) -> List[str]:
        """
        Obtener archivos de una carpeta local

        Args:
            ruta_carpeta: Ruta a carpeta
            extensiones: Lista de extensiones a incluir

        Returns:
            Lista de rutas a archivos
        """
        try:
            carpeta = Path(ruta_carpeta)
            archivos = []

            for archivo in carpeta.glob("*"):
                if archivo.is_file() and archivo.suffix.lower() in extensiones:
                    archivos.append(str(archivo))

            return archivos

        except Exception as e:
            logger.error(f"Error listando carpeta: {e}")
            return []

    def _obtener_espacio_impl(self) -> Optional[Dict]:
        """Obtener información de espacio en Google Drive"""
        try:
            if not self.service:
                return None

            about = self.service.about().get(fields='storageQuota').execute()
            quota = about.get('storageQuota', {})

            info = {
                'usado_bytes': int(quota.get('usedBytes', 0)),
                'limite_bytes': int(quota.get('limit', 0)),
                'disponible_bytes': int(quota.get('limit', 0)) - int(quota.get('usedBytes', 0))
            }

            # Convertir a GB para logs
            usado_gb = info['usado_bytes'] / (1024**3)
            limite_gb = info['limite_bytes'] / (1024**3)

            logger.info(f"📊 Espacio Google Drive: {usado_gb:.1f}GB / {limite_gb:.1f}GB usado")

            return info

        except Exception as e:
            logger.error(f"Error obteniendo espacio: {e}")
            return None

    def _sincronizar_fallback(self, ruta_bd: str, ruta_imagenes: Optional[str],
                             ruta_videos: Optional[str]) -> SyncResult:
        """
        Fallback: simular sincronización sin Google Drive

        Args:
            ruta_bd: Ruta a base de datos
            ruta_imagenes: Ruta a carpeta imágenes
            ruta_videos: Ruta a carpeta videos

        Returns:
            SyncResult simulado
        """
        logger.info("Modo fallback: simulando sincronización")

        resultado = SyncResult(exitoso=True)
        archivos = 0

        if self._validar_archivo(ruta_bd):
            archivos += 1
            resultado.tamaño_bytes += self._obtener_tamaño_archivo(ruta_bd)

        if ruta_imagenes and Path(ruta_imagenes).exists():
            imagenes = list(Path(ruta_imagenes).glob("*"))
            archivos += len([f for f in imagenes if f.is_file()])

        if ruta_videos and Path(ruta_videos).exists():
            videos = list(Path(ruta_videos).glob("*"))
            archivos += len([f for f in videos if f.is_file()])

        resultado.archivos_sincronizados = archivos
        resultado.mensaje = f"Fallback: {archivos} archivos (sin subir)"

        return resultado

    def __repr__(self) -> str:
        estado = "✓" if self.service else "✗"
        return f"<GoogleDriveSync {estado}: {self.carpeta_sync}>"
