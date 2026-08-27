"""
Módulo de procesadores para AjamSi

Compila videos desde ideas y imágenes
"""

from .base_video_compiler import BaseVideoCompiler, Video
from .ffmpeg_video_compiler import FFmpegVideoCompiler

__all__ = [
    'BaseVideoCompiler',
    'Video',
    'FFmpegVideoCompiler'
]
