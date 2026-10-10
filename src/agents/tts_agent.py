"""
TTS AGENT
Responsabilidad: Generar narración de audio 100% local con voces de Windows (pyttsx3/SAPI)
"""

import logging
from typing import Dict
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class TTSAgent:
    """
    Genera narración en audio para los videos.

    - Usa pyttsx3 (Windows SAPI) - sin internet, sin APIs
    - Busca voz en español (Helena/Sabina) automáticamente
    - Salida .wav lista para FFmpeg
    """

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        base_dir = Path(__file__).parent.parent.parent
        self.output_dir = base_dir / "audio_generado"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.disponible = self._verificar()
        self.logger.info(f"✓ TTSAgent inicializado (disponible: {self.disponible})")

    def _verificar(self) -> bool:
        try:
            import pyttsx3  # noqa: F401
            return True
        except ImportError:
            self.logger.warning("⚠️  pyttsx3 no instalado - videos sin narración")
            return False

    def _seleccionar_voz_espanola(self, engine) -> bool:
        """Seleccionar la primera voz en español disponible"""
        for voz in engine.getProperty('voices'):
            texto_id = f"{voz.id} {voz.name}".lower()
            if 'spanish' in texto_id or 'helena' in texto_id or 'sabina' in texto_id or 'es-es' in texto_id or 'es_es' in texto_id:
                engine.setProperty('voice', voz.id)
                return True
        return False

    def ejecutar(self, texto: str, velocidad: int = 165) -> Dict:
        """
        NO genera audio. Solo devuelve la descripción del guion para que
        el usuario agregue la voz manualmente (ej: CapCut, Adobe Premiere).

        Args:
            texto: Texto a narrar (se guarda solo en el documento Word)
            velocidad: Ignorado (era para pyttsx3)

        Returns:
            Dict con 'guion_narrado' (texto) y 'duracion_estimada'
        """
        try:
            self.logger.info(f"📝 Preparando guion para narración manual ({len(texto)} caracteres)...")

            # Estimar duración: ~165 palabras/min natural
            num_palabras = len(texto.split())
            duracion_estimada = max(5, round((num_palabras / 165) * 60) + 1)

            self.logger.info(f"✅ Guion listo: (~{duracion_estimada}s) - Tú añades la voz en tu editor")
            return {
                'status': 'success',
                'guion_narrado': texto,
                'duracion_estimada': duracion_estimada,
                'audio_path': None,  # No hay archivo de audio
                'nota': 'Agrega la voz manualmente en tu editor (CapCut, Adobe, etc)'
            }

        except Exception as e:
            self.logger.error(f"❌ Error preparando guion: {e}")
            return {'status': 'error', 'error': str(e), 'guion_narrado': None}

    def construir_guion(self, noticia: Dict, idea: Dict = None) -> str:
        """Construir el guion de narración a partir de la noticia"""
        titulo = noticia.get('titulo', '')
        contenido = noticia.get('contenido', '') or noticia.get('resumen', '')

        partes = [f"Atención Canarias. {titulo}."]

        if contenido:
            # Primeras 2 frases del contenido
            frases = [f.strip() for f in contenido.replace('\n', ' ').split('.') if len(f.strip()) > 20]
            if frases:
                partes.append(frases[0] + '.')
            if len(frases) > 1:
                partes.append(frases[1] + '.')

        partes.append("¿Tú qué opinas? Déjalo en los comentarios y sígueme para más noticias de las islas.")
        return ' '.join(partes)
