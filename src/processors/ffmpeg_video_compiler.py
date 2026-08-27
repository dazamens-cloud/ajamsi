"""
FFmpeg Video Compiler - Compila videos usando FFmpeg
"""

from typing import Optional, List
import logging
import subprocess
import json
from pathlib import Path

from src.generators import Idea
from .base_video_compiler import BaseVideoCompiler, Video

logger = logging.getLogger(__name__)


class FFmpegVideoCompiler(BaseVideoCompiler):
    """
    Compilador de videos usando FFmpeg

    Convierte imágenes + guiones en videos MP4 con resolución TikTok
    """

    def __init__(self, config: dict):
        """
        Inicializar compilador FFmpeg

        Args:
            config: Configuración del proyecto
        """
        super().__init__(config)

        # Verificar FFmpeg disponible
        self.ffmpeg_disponible = self._verificar_ffmpeg()
        if not self.ffmpeg_disponible:
            logger.warning("⚠ FFmpeg no está instalado. Modo fallback activado.")
        else:
            logger.info("✓ FFmpeg disponible")

    def _compilar_video_impl(self, idea: Idea, ruta_imagen: str,
                            guion: Optional[str] = None) -> Optional[Video]:
        """
        Compilar video usando FFmpeg

        Args:
            idea: Idea a compilar
            ruta_imagen: Ruta a imagen
            guion: Guión opcional (no usado en versión 1)

        Returns:
            Video compilado o None
        """
        if not self.ffmpeg_disponible:
            logger.warning("FFmpeg no disponible, usando fallback")
            return self._compilar_video_fallback(idea, ruta_imagen, guion)

        try:
            # Generar nombre de salida
            nombre_salida = self._obtener_nombre_archivo_salida(idea)
            ruta_salida = self.output_dir / f"{nombre_salida}.{self.formato}"

            # Parsear resolución
            ancho, alto = self._validar_resolucion(self.resolucion)

            # Generar comando FFmpeg
            duracion = self._calcular_duracion_optima(idea, guion)
            cmd = self._generar_comando_ffmpeg(
                ruta_imagen=str(ruta_imagen),
                ruta_salida=str(ruta_salida),
                duracion=duracion,
                ancho=ancho,
                alto=alto
            )

            logger.debug(f"Comando FFmpeg: {' '.join(cmd)}")

            # Ejecutar FFmpeg
            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos max
            )

            if resultado.returncode != 0:
                logger.error(f"Error FFmpeg: {resultado.stderr}")
                return None

            # Verificar archivo creado
            if not ruta_salida.exists():
                logger.error(f"Archivo de video no creado: {ruta_salida}")
                return None

            # Obtener información del video
            tamaño_bytes = ruta_salida.stat().st_size
            logger.debug(f"Video creado: {ruta_salida} ({tamaño_bytes} bytes)")

            # Crear objeto Video
            video = self._crear_video(
                titulo=idea.titulo,
                idea=idea,
                ruta_imagen=ruta_imagen,
                ruta_archivo=str(ruta_salida),
                duracion=duracion,
                tamaño_bytes=tamaño_bytes
            )

            return video

        except subprocess.TimeoutExpired:
            logger.error("Compilación de video excedió timeout (300s)")
            return None
        except Exception as e:
            logger.error(f"Error compilando con FFmpeg: {e}", exc_info=True)
            return None

    def _generar_comando_ffmpeg(self, ruta_imagen: str, ruta_salida: str,
                               duracion: float, ancho: int, alto: int) -> List[str]:
        """
        Generar comando FFmpeg para compilar video

        Args:
            ruta_imagen: Ruta a imagen
            ruta_salida: Ruta de salida
            duracion: Duración en segundos
            ancho: Ancho en píxeles
            alto: Alto en píxeles

        Returns:
            Lista de argumentos para subprocess
        """
        cmd = [
            "ffmpeg",
            "-y",  # Sobrescribir si existe
            "-loop", "1",  # Loop infinito de imagen
            "-i", ruta_imagen,  # Imagen de entrada
            "-c:v", "libx264",  # Codec de video
            "-t", str(duracion),  # Duración
            "-pix_fmt", "yuv420p",  # Formato píxel (compatible)
            "-vf", f"scale={ancho}:{alto}:force_original_aspect_ratio=decrease,pad={ancho}:{alto}:(ow-iw)/2:(oh-ih)/2",  # Resize + pad
            "-b:v", self.bitrate,  # Bitrate
            "-r", str(self.fps),  # FPS
            "-preset", "fast",  # Velocidad de codificación
            ruta_salida  # Archivo de salida
        ]

        return cmd

    def _calcular_duracion_optima(self, idea: Idea,
                                  guion: Optional[str] = None) -> float:
        """
        Calcular duración óptima para el video

        Args:
            idea: Idea del video
            guion: Guión (opcional)

        Returns:
            Duración en segundos
        """
        # Lógica simple: usar duración media por defecto
        # Versiones futuras pueden usar guion para calcular duración exacta
        duracion_default = (self.duracion_min + self.duracion_max) / 2
        return duracion_default

    def _compilar_video_fallback(self, idea: Idea, ruta_imagen: str,
                                guion: Optional[str] = None) -> Optional[Video]:
        """
        Fallback: crear metadata de video sin compilar (para testing)

        Args:
            idea: Idea del video
            ruta_imagen: Ruta a imagen
            guion: Guión opcional

        Returns:
            Objeto Video (sin archivo físico)
        """
        logger.info(f"Modo fallback: simulando compilación de {idea.titulo}")

        nombre_salida = self._obtener_nombre_archivo_salida(idea)
        ruta_salida_simulada = self.output_dir / f"{nombre_salida}.{self.formato}"
        duracion = (self.duracion_min + self.duracion_max) / 2

        video = self._crear_video(
            titulo=idea.titulo,
            idea=idea,
            ruta_imagen=ruta_imagen,
            ruta_archivo=str(ruta_salida_simulada),
            duracion=duracion,
            tamaño_bytes=0  # No hay archivo real
        )

        logger.info(f"Fallback video: {video.titulo} ({video.duracion_segundos}s)")
        return video

    def _verificar_ffmpeg(self) -> bool:
        """
        Verificar si FFmpeg está instalado

        Returns:
            True si FFmpeg está disponible
        """
        try:
            resultado = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                timeout=5
            )
            disponible = resultado.returncode == 0
            logger.debug(f"FFmpeg disponible: {disponible}")
            return disponible
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def obtener_informacion_video(self, ruta_video: str) -> Optional[dict]:
        """
        Obtener información de un archivo de video usando ffprobe

        Args:
            ruta_video: Ruta al archivo de video

        Returns:
            Diccionario con información (duration, width, height, etc.) o None
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                ruta_video
            ]

            resultado = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if resultado.returncode != 0:
                logger.warning(f"No se pudo obtener info: {ruta_video}")
                return None

            datos = json.loads(resultado.stdout)
            return datos

        except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
            logger.warning(f"Error obteniendo info de video: {e}")
            return None

    def __repr__(self) -> str:
        estado = "✓" if self.ffmpeg_disponible else "✗"
        return f"<FFmpegVideoCompiler {estado}: {self.formato}, {self.resolucion}>"
