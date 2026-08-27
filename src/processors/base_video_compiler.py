"""
Base Video Compiler - Clase abstracta para compiladores de video
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import logging

from src.generators import Idea

logger = logging.getLogger(__name__)


@dataclass
class Video:
    """Estructura de datos para un video compilado"""
    titulo: str
    idea_id: Optional[str] = None
    ruta_archivo: str = ""
    ruta_imagen: str = ""
    duracion_segundos: float = 0.0
    resolucion: str = "1080x1920"
    formato: str = "mp4"
    tamaño_bytes: int = 0
    relevancia_score: float = 0.0

    def __repr__(self) -> str:
        return f"<Video: {self.titulo[:50]}... ({self.duracion_segundos}s)>"


class BaseVideoCompiler(ABC):
    """
    Clase base para compiladores de video

    Define la interfaz común y proporciona utilidades compartidas
    """

    def __init__(self, config: dict):
        """
        Inicializar compilador de video

        Args:
            config: Configuración del proyecto
        """
        self.config = config
        self.compilador_config = config.get("compilador_videos", {})
        self.formato = self.compilador_config.get("formato", "mp4")
        self.resolucion = self.compilador_config.get("resolucion", "1080x1920")
        self.duracion_min = self.compilador_config.get("duracion_min", 15)
        self.duracion_max = self.compilador_config.get("duracion_max", 60)
        self.bitrate = self.compilador_config.get("bitrate", "5000k")
        self.fps = self.compilador_config.get("fps", 30)

        # Crear directorios si no existen
        self.output_dir = Path("videos")
        self.output_dir.mkdir(exist_ok=True, parents=True)

        logger.info(f"Inicializado compilador de video: {self.__class__.__name__}")
        logger.info(f"  Formato: {self.formato}")
        logger.info(f"  Resolución: {self.resolucion}")
        logger.info(f"  Duración: {self.duracion_min}-{self.duracion_max}s")

    def compilar_video(self, idea: Idea, ruta_imagen: str,
                      guion: Optional[str] = None) -> Optional[Video]:
        """
        Compilar un video desde una idea e imagen

        Args:
            idea: Objeto Idea con metadata
            ruta_imagen: Ruta a la imagen a usar
            guion: Guión opcional (subtítulos, narración)

        Returns:
            Objeto Video compilado o None si hay error
        """
        try:
            logger.info(f"Compilando video: {idea.titulo[:50]}...")

            # Validar entrada
            if not idea or not idea.titulo:
                logger.warning("Idea inválida")
                return None

            if not Path(ruta_imagen).exists():
                logger.warning(f"Imagen no encontrada: {ruta_imagen}")
                return None

            # Compilar (implementación específica por subclass)
            video = self._compilar_video_impl(idea, ruta_imagen, guion)

            if video:
                logger.info(f"✓ Video compilado: {video.titulo}")
            else:
                logger.warning("No se compiló el video")

            return video

        except Exception as e:
            logger.error(f"Error compilando video: {e}", exc_info=True)
            return None

    @abstractmethod
    def _compilar_video_impl(self, idea: Idea, ruta_imagen: str,
                            guion: Optional[str] = None) -> Optional[Video]:
        """
        Implementación específica de compilación de video

        Args:
            idea: Idea scrapeada
            ruta_imagen: Ruta a imagen
            guion: Guión opcional

        Returns:
            Objeto Video compilado o None
        """
        pass

    def _crear_video(self, titulo: str, idea: Idea = None,
                    ruta_imagen: str = "", ruta_archivo: str = "",
                    duracion: float = 0.0, **kwargs) -> Video:
        """
        Factory para crear un video

        Args:
            titulo: Título del video
            idea: Idea relacionada (opcional)
            ruta_imagen: Ruta a imagen
            ruta_archivo: Ruta a archivo MP4
            duracion: Duración en segundos
            **kwargs: Argumentos adicionales (resolucion, formato, etc.)

        Returns:
            Objeto Video
        """
        video = Video(
            titulo=titulo,
            idea_id=idea.titulo if idea else None,
            ruta_imagen=ruta_imagen,
            ruta_archivo=ruta_archivo,
            duracion_segundos=duracion,
            resolucion=kwargs.get("resolucion", self.resolucion),
            formato=kwargs.get("formato", self.formato),
            tamaño_bytes=kwargs.get("tamaño_bytes", 0),
        )

        return video

    def _obtener_nombre_archivo_salida(self, idea: Idea) -> str:
        """
        Generar nombre de archivo para el video

        Args:
            idea: Idea compilada

        Returns:
            Nombre de archivo (sin ruta)
        """
        # Sanitizar título para nombre de archivo
        titulo_limpio = idea.titulo.replace(" ", "_").replace("/", "_")
        titulo_limpio = "".join(c for c in titulo_limpio if c.isalnum() or c in "_-")
        titulo_limpio = titulo_limpio[:50]  # Limitar a 50 caracteres

        filename = f"{titulo_limpio}_{self.resolucion}_{self.formato}"
        return filename

    def _validar_resolucion(self, resolucion: str) -> tuple[int, int]:
        """
        Validar y parsear resolución

        Args:
            resolucion: Resolución como "1080x1920"

        Returns:
            Tupla (ancho, alto)

        Raises:
            ValueError: Si la resolución no es válida
        """
        try:
            ancho, alto = map(int, resolucion.split("x"))
            if ancho <= 0 or alto <= 0:
                raise ValueError("Dimensiones deben ser positivas")
            return (ancho, alto)
        except (ValueError, AttributeError) as e:
            logger.error(f"Resolución inválida: {resolucion}")
            raise ValueError(f"Formato de resolución debe ser 'WIDTHxHEIGHT', recibido: {resolucion}") from e

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.formato}, {self.resolucion}>"
