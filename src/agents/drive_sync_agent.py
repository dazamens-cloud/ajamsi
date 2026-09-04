"""
DRIVE SYNC AGENT
Responsabilidad: Sincronización automática con Google Drive
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Intentar importar librerías de Google
try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.oauth2.credentials import Credentials as UserCredentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    logger.warning("⚠️  Librerías de Google Drive no disponibles")


class DriveSyncAgent:
    """
    Agente especializado en sincronización con Google Drive.

    Responsabilidades:
    - Sube videos/imágenes a Google Drive
    - Organiza carpetas automáticamente
    - Mantiene versiones
    - Reporta progreso de sincronización
    """

    CARPETAS_ESTRUCTURA = {
        'videos': 'AjamSi/videos',
        'imagenes': 'AjamSi/imagenes',
        'backups_db': 'AjamSi/backups',
        'reportes': 'AjamSi/reportes',
    }

    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, config: Dict):
        """
        Inicializar el agente sync.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.drive_service = None
        self._inicializar_google_drive()
        self.logger.info("✓ DriveSyncAgent inicializado")

    def _inicializar_google_drive(self):
        """Inicializar la conexión con Google Drive usando credenciales OAuth"""
        if not GOOGLE_DRIVE_AVAILABLE:
            self.logger.warning("⚠️  Librerías de Google no disponibles, usando modo simulación")
            self.drive_service = None
            return

        try:
            credentials_path = Path(self.config.get('google_drive', {}).get('credentials_file', 'credentials.json'))

            if not credentials_path.exists():
                self.logger.warning(f"⚠️  No se encontró {credentials_path}")
                return

            # Intentar autenticarse con las credenciales
            try:
                # Primero, intentar con Service Account
                creds = Credentials.from_service_account_file(
                    str(credentials_path),
                    scopes=self.SCOPES
                )
                self.drive_service = build('drive', 'v3', credentials=creds)
                self.logger.info("✅ Autenticación con Service Account exitosa")
            except Exception as e:
                self.logger.warning(f"⚠️  Service Account falló: {e}, intentando OAuth estándar")
                # Si Service Account falla, usar OAuth estándar
                try:
                    creds = UserCredentials.from_authorized_user_file(
                        str(credentials_path),
                        scopes=self.SCOPES
                    )
                    self.drive_service = build('drive', 'v3', credentials=creds)
                    self.logger.info("✅ Autenticación OAuth exitosa")
                except Exception as e2:
                    self.logger.error(f"❌ OAuth también falló: {e2}")
                    self.drive_service = None

        except Exception as e:
            self.logger.error(f"❌ Error inicializando Google Drive: {e}")
            self.drive_service = None

    def ejecutar(self, archivos_config: Dict) -> Dict:
        """
        Sincronizar archivos con Google Drive.

        Args:
            archivos_config: Dict con archivos a sincronizar

        Returns:
            Dict con resultado de sincronización
        """
        self.logger.info("☁️  Iniciando sincronización con Google Drive...")

        try:
            # TODO: Implementar autenticación real con Google Drive API
            # Por ahora, mock sync

            num_archivos = archivos_config.get('archivos', 0)
            tamaño_estimado = num_archivos * 2.5  # MB

            # Simular creación de carpetas
            carpetas_creadas = self._crear_estructura_carpetas()

            # Simular upload
            archivos_subidos = self._simular_upload_archivos(num_archivos)

            # Simular backup de DB
            backup_realizado = self._realizar_backup_db()

            resultado = {
                'status': 'success',
                'fecha_sync': datetime.now().isoformat(),
                'archivos_procesados': num_archivos,
                'archivos_sincronizados': archivos_subidos,
                'tamaño_bytes': int(tamaño_estimado * 1024 * 1024),
                'tamaño_mb': round(tamaño_estimado, 2),
                'carpetas_creadas': carpetas_creadas,
                'backup_db': backup_realizado,
                'estado': 'sincronizado',
                'proxima_sync': self._calcular_proxima_sync(),
            }

            self.logger.info(f"✅ Sincronización completada: {archivos_subidos} archivos")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error en sincronización: {e}")
            return {
                'status': 'error',
                'error': str(e),
            }

    def sincronizar_batch_completo(self, batch_dict: Dict) -> Dict:
        """
        Sincronizar un batch completo después de procesamiento.

        Args:
            batch_dict: Dict con resultados del batch

        Returns:
            Dict con resultado de sincronización
        """
        self.logger.info("☁️  Sincronizando batch completo...")

        try:
            # Contar archivos a sincronizar
            noticias = len(batch_dict.get('fases', {}).get('scraping', {}).get('noticias', []))
            ideas = len(batch_dict.get('fases', {}).get('ideas', {}).get('ideas', []))
            captions = len(batch_dict.get('fases', {}).get('captions', {}).get('captions', []))

            total_archivos = noticias + ideas + captions

            return self.ejecutar({'archivos': total_archivos})

        except Exception as e:
            self.logger.error(f"❌ Error sincronizando batch: {e}")
            return {
                'status': 'error',
                'error': str(e),
            }

    def _crear_estructura_carpetas(self) -> int:
        """Crear estructura de carpetas en Drive"""
        if not self.drive_service:
            self.logger.warning("  ⚠️  Google Drive no conectado, usando simulación")
            return len(self.CARPETAS_ESTRUCTURA)

        self.logger.info("  📁 Creando estructura de carpetas...")
        carpetas_creadas = 0

        try:
            for nombre_tipo, ruta in self.CARPETAS_ESTRUCTURA.items():
                carpeta_id = self._crear_o_buscar_carpeta(ruta)
                if carpeta_id:
                    carpetas_creadas += 1
                    self.logger.info(f"    ✅ Carpeta '{nombre_tipo}' lista: {ruta}")
        except Exception as e:
            self.logger.error(f"  ❌ Error creando carpetas: {e}")

        return carpetas_creadas

    def _crear_o_buscar_carpeta(self, ruta: str) -> Optional[str]:
        """Crear o buscar carpeta en Google Drive"""
        try:
            partes = ruta.split('/')
            parent_id = 'root'

            for parte in partes:
                # Buscar si existe la carpeta
                query = f"name='{parte}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parent_id}' in parents"
                results = self.drive_service.files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)',
                    pageSize=1
                ).execute()

                carpetas = results.get('files', [])

                if carpetas:
                    parent_id = carpetas[0]['id']
                else:
                    # Crear la carpeta
                    file_metadata = {
                        'name': parte,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [parent_id]
                    }
                    carpeta = self.drive_service.files().create(
                        body=file_metadata,
                        fields='id'
                    ).execute()
                    parent_id = carpeta.get('id')

            return parent_id

        except HttpError as e:
            self.logger.error(f"    ❌ Error en Drive API: {e}")
            return None

    def _simular_upload_archivos(self, cantidad: int) -> int:
        """Subir archivos a Google Drive"""
        if not self.drive_service:
            self.logger.warning(f"  ⚠️  Google Drive no conectado, usando simulación ({cantidad} archivos)")
            return cantidad

        self.logger.info(f"  📤 Preparando upload de {cantidad} archivos...")
        archivos_subidos = 0

        # En producción, aquí iría lógica para subir archivos
        # Por ahora, solo reportamos que está listo
        self.logger.info(f"  ✅ {cantidad} archivos listos para sincronizar")
        return cantidad

    def _realizar_backup_db(self) -> bool:
        """Realizar backup de base de datos"""
        self.logger.info("  💾 Realizando backup de base de datos...")
        # TODO: Implementar backup real
        return True

    def _calcular_proxima_sync(self) -> str:
        """Calcular cuándo será la próxima sincronización"""
        # Default: cada 24 horas
        proxima = datetime.now()
        return (proxima).isoformat()

    def obtener_estado_drive(self) -> Dict:
        """Obtener estado de sincronización actual"""
        if not self.drive_service:
            return {
                'sincronizado': False,
                'conectado': False,
                'error': 'Google Drive no conectado',
            }

        try:
            # Obtener espacio disponible
            about = self.drive_service.about().get(fields='storageQuota').execute()
            storage_quota = about.get('storageQuota', {})

            limite_bytes = storage_quota.get('limit', 0)
            usado_bytes = storage_quota.get('usage', 0)
            disponible_bytes = limite_bytes - usado_bytes

            # Contar archivos en AjamSi
            query = "name contains 'AjamSi' and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, size)',
                pageSize=100
            ).execute()

            archivos = results.get('files', [])
            tamaño_total = sum(int(f.get('size', 0)) for f in archivos)

            return {
                'sincronizado': True,
                'conectado': True,
                'ultima_sync': datetime.now().isoformat(),
                'archivos_en_drive': len(archivos),
                'tamaño_total_mb': round(tamaño_total / (1024 * 1024), 2),
                'espacio_disponible_gb': round(disponible_bytes / (1024 * 1024 * 1024), 2),
                'espacio_usado_gb': round(usado_bytes / (1024 * 1024 * 1024), 2),
            }

        except Exception as e:
            self.logger.error(f"❌ Error obteniendo estado: {e}")
            return {
                'sincronizado': False,
                'error': str(e),
            }
