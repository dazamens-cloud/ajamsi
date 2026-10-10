"""
VIDEO COMPILER AGENT - Compilación REAL con FFmpeg
Responsabilidad: imagen + narración + efecto Ken Burns -> video vertical listo para TikTok
"""

import logging
import subprocess
import os
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class VideoCompilerAgent:
    """
    Compila videos REALES con FFmpeg.

    - Efecto Ken Burns (zoom lento) para que la imagen no sea estática
    - Integra narración TTS si existe
    - Verifica que el archivo final exista de verdad
    - Formatos: TikTok (1080x1920), Instagram (1080x1080), YouTube (1920x1080)
    """

    DURACION_POR_DEFECTO = 15
    FORMATOS_SOPORTADOS = {
        'tiktok': {'resolucion': '1080x1920', 'fps': 30, 'bitrate': '2500k', 'ratio': '9:16'},
        'instagram': {'resolucion': '1080x1080', 'fps': 30, 'bitrate': '2000k', 'ratio': '1:1'},
        'youtube': {'resolucion': '1920x1080', 'fps': 30, 'bitrate': '5000k', 'ratio': '16:9'},
    }

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        base_dir = Path(__file__).parent.parent.parent
        self.videos_dir = base_dir / "videos"
        self.videos_dir.mkdir(parents=True, exist_ok=True)

        self.ffmpeg_disponible = self._verificar_ffmpeg()
        self.logger.info(f"✓ VideoCompilerAgent inicializado - Videos en: {self.videos_dir}")

    def _verificar_ffmpeg(self) -> bool:
        """Verificar si FFmpeg está instalado"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                self.logger.info("✓ FFmpeg disponible")
                return True
        except Exception as e:
            self.logger.warning(f"⚠️  FFmpeg no disponible: {e}")
        return False

    def ejecutar(
        self,
        imagen_path: str,
        guion: str = '',
        audio_path: Optional[str] = None,
        duracion: int = DURACION_POR_DEFECTO,
        formato: str = 'tiktok',
        nombre_base: str = ''
    ) -> Dict:
        """
        Compilar video real con FFmpeg (Ken Burns, SIN audio).
        La voz se agrega manualmente en el editor del usuario.

        Args:
            imagen_path: Imagen base (idealmente 1080x1920)
            guion: Texto del guion (solo informativo, no se usa en audio)
            audio_path: Ignorado (usuario añade voz manualmente)
            duracion: Duración en segundos (ej: 15s para TikTok)
            formato: 'tiktok' | 'instagram' | 'youtube'
            nombre_base: Prefijo para el nombre del archivo

        Returns:
            Dict con 'video_path' verificado en disco
        """
        self.logger.info(f"🎬 Compilando video ({formato}, {duracion}s, SIN audio)...")

        try:
            imagen_path = Path(imagen_path)
            if not imagen_path.exists():
                raise FileNotFoundError(f"Imagen no encontrada: {imagen_path}")

            specs = self.FORMATOS_SOPORTADOS.get(formato)
            if not specs:
                raise ValueError(f"Formato no soportado: {formato}")

            if not self.ffmpeg_disponible:
                raise Exception("FFmpeg no está instalado - no se puede compilar video real")

            # Ignorar audio_path: usuario lo agrega en su editor (CapCut, Adobe, etc)
            video_path = self._compilar_ken_burns(imagen_path, None, duracion, formato, specs, nombre_base)

            size_mb = os.path.getsize(video_path) / (1024 * 1024)
            resultado = {
                'status': 'success',
                'video_path': str(video_path),
                'video_filename': video_path.name,
                'formato': formato,
                'resolucion': specs['resolucion'],
                'duracion_segundos': duracion,
                'tamaño_mb': round(size_mb, 2),
                'fps': specs['fps'],
                'tiene_audio': audio is not None,
                'tiene_efectos': True,
                'timestamp': datetime.now().isoformat(),
            }
            self.logger.info(f"✅ Video compilado: {video_path.name} ({size_mb:.1f}MB)")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error compilando video: {e}")
            return {'status': 'error', 'error': str(e), 'video_path': None}

    def _compilar_ken_burns(
        self,
        imagen_path: Path,
        audio_path: Optional[Path],
        duracion: int,
        formato: str,
        specs: Dict,
        nombre_base: str = ''
    ) -> Path:
        """Compilar con efecto Ken Burns (zoom lento) + narración"""
        prefijo = f"{nombre_base}_" if nombre_base else ""
        video_filename = f"{prefijo}video_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{formato}.mp4"
        video_path = self.videos_dir / video_filename

        w, h = specs['resolucion'].split('x')
        fps = specs['fps']
        total_frames = duracion * fps

        # Escalar x2 antes del zoompan para evitar jitter, luego bajar a resolución final
        filtro = (
            f"[0:v]scale={int(w)*2}:{int(h)*2}:force_original_aspect_ratio=increase,"
            f"crop={int(w)*2}:{int(h)*2},"
            f"zoompan=z='min(zoom+0.0003,1.08)':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":s={w}x{h}:fps={fps}[v]"
        )

        cmd = ['ffmpeg', '-y', '-i', str(imagen_path)]

        if audio_path:
            cmd += ['-i', str(audio_path)]
            cmd += ['-filter_complex', filtro, '-map', '[v]', '-map', '1:a',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest']
        else:
            cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo']
            cmd += ['-filter_complex', filtro, '-map', '[v]', '-map', '1:a',
                    '-c:a', 'aac', '-t', str(duracion)]

        cmd += ['-c:v', 'libx264', '-preset', 'veryfast',
                '-b:v', specs['bitrate'], '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart', str(video_path)]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                self.logger.error(f"FFmpeg Ken Burns error: {result.stderr[-500:]}")
                self.logger.warning("Intentando modo simple (sin zoom)...")
                return self._compilar_simple(imagen_path, audio_path, video_path, w, h, fps,
                                             specs['bitrate'], duracion)
        except subprocess.TimeoutExpired:
            raise Exception("FFmpeg timeout (>300s)")

        if not video_path.exists() or video_path.stat().st_size < 10000:
            raise Exception(f"Archivo de video no creado: {video_path}")

        return video_path

    def _compilar_simple(self, imagen_path: Path, audio_path: Optional[Path], video_path: Path,
                         w: str, h: str, fps: int, bitrate: str, duracion: int) -> Path:
        """Fallback: video simple sin zoom"""
        cmd = ['ffmpeg', '-y', '-loop', '1', '-i', str(imagen_path)]

        if audio_path:
            cmd += ['-i', str(audio_path), '-c:a', 'aac', '-shortest']
        else:
            cmd += ['-t', str(duracion), '-an']

        cmd += [
            '-vf', f"scale=w={w}:h={h}:force_original_aspect_ratio=decrease,"
                   f"pad=w={w}:h={h}:x='(ow-iw)/2':y='(oh-ih)/2',fps={fps}",
            '-c:v', 'libx264', '-preset', 'ultrafast',
            '-b:v', bitrate, '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', str(video_path)
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                self.logger.error(f"FFmpeg simple error: {result.stderr[-500:]}")
                raise Exception(f"FFmpeg simple falló: {result.stderr[-200:]}")
        except subprocess.TimeoutExpired:
            raise Exception("FFmpeg simple timeout")

        if not video_path.exists() or video_path.stat().st_size < 10000:
            raise Exception(f"Archivo de video no creado (simple): {video_path}")

        return video_path
