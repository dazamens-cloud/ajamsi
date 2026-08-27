"""
Base Drive Sync - Clase abstracta para sincronización en la nube
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """Resultado de una operación de sincronización"""
    exitoso: bool
    archivos_sincronizados: int = 0
    archivos_fallo: int = 0
    tamaño_bytes: int = 0
    mensaje: str = ""
    detalles: List[str] = None

    def __post_init__(self):
        if self.detalles is None:
            self.detalles = []

    def __repr__(self) -> str:
        return f"<SyncResult: {'✓' if self.exitoso else '✗'} {self.archivos_sincronizados}ok/{self.archivos_fallo}err>"


class BaseDriveSync(ABC):
    """
    Clase base para sincronización en la nube

    Define interfaz común para sincronizar archivos a servicios en nube
    """

    def __init__(self, config: dict):
        """
        Inicializar sincronizador

        Args:
            config: Configuración del proyecto
        """
        self.config = config
        self.sync_config = config.get("google_drive", {})
        self.sincronizar = self.sync_config.get("sincronizar", True)
        self.carpeta_sync = self.sync_config.get("carpeta_sync", "AjamSi_Backups")
        self.carpeta_imagenes = self.sync_config.get("carpeta_imagenes", "AjamSi_Imagenes")
        self.carpeta_videos = self.sync_config.get("carpeta_videos", "AjamSi_Videos")

        logger.info(f"Inicializado sincronizador: {self.__class__.__name__}")
        logger.info(f"  Sincronizar: {self.sincronizar}")
        logger.info(f"  Carpeta raíz: {self.carpeta_sync}")

    def sincronizar_todo(self, ruta_bd: str, ruta_imagenes: str = None,
                        ruta_videos: str = None) -> SyncResult:
        """
        Sincronizar todos los archivos a la nube

        Args:
            ruta_bd: Ruta a base de datos SQLite
            ruta_imagenes: Ruta a carpeta de imágenes (opcional)
            ruta_videos: Ruta a carpeta de videos (opcional)

        Returns:
            SyncResult con detalles de la operación
        """
        if not self.sincronizar:
            logger.info("Sincronización deshabilitada en config")
            return SyncResult(exitoso=True, mensaje="Sincronización deshabilitada")

        try:
            logger.info("Iniciando sincronización a la nube...")

            # Validar archivos
            if not Path(ruta_bd).exists():
                logger.warning(f"BD no encontrada: {ruta_bd}")
                return SyncResult(exitoso=False, mensaje=f"BD no encontrada: {ruta_bd}")

            # Implementación específica por subclass
            resultado = self._sincronizar_impl(ruta_bd, ruta_imagenes, ruta_videos)

            if resultado.exitoso:
                logger.info(f"✓ Sincronización completa: {resultado.archivos_sincronizados} archivos")
            else:
                logger.warning(f"⚠ Sincronización con errores: {resultado.archivos_fallo} fallos")

            return resultado

        except Exception as e:
            logger.error(f"Error en sincronización: {e}", exc_info=True)
            return SyncResult(exitoso=False, mensaje=str(e))

    @abstractmethod
    def _sincronizar_impl(self, ruta_bd: str, ruta_imagenes: Optional[str],
                         ruta_videos: Optional[str]) -> SyncResult:
        """
        Implementación específica de sincronización

        Args:
            ruta_bd: Ruta a base de datos
            ruta_imagenes: Ruta a carpeta imágenes
            ruta_videos: Ruta a carpeta videos

        Returns:
            SyncResult con detalles
        """
        pass

    def obtener_espacio_disponible(self) -> Optional[Dict]:
        """
        Obtener información de espacio disponible en la nube

        Returns:
            Diccionario con info de almacenamiento o None
        """
        logger.info("Obteniendo información de espacio...")
        return self._obtener_espacio_impl()

    @abstractmethod
    def _obtener_espacio_impl(self) -> Optional[Dict]:
        """
        Implementación específica para obtener espacio

        Returns:
            Diccionario con usado/disponible o None
        """
        pass

    def _validar_archivo(self, ruta: str) -> bool:
        """
        Validar que archivo existe y es accesible

        Args:
            ruta: Ruta a archivo

        Returns:
            True si válido
        """
        try:
            path = Path(ruta)
            if not path.exists():
                logger.warning(f"Archivo no encontrado: {ruta}")
                return False
            if not path.is_file():
                logger.warning(f"No es archivo: {ruta}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error validando archivo: {e}")
            return False

    def _obtener_tamaño_archivo(self, ruta: str) -> int:
        """
        Obtener tamaño de archivo en bytes

        Args:
            ruta: Ruta a archivo

        Returns:
            Tamaño en bytes o 0 si error
        """
        try:
            return Path(ruta).stat().st_size
        except Exception as e:
            logger.error(f"Error obteniendo tamaño: {e}")
            return 0

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.carpeta_sync}>"
