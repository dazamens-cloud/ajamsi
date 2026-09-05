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
        Generar archivo de audio con la narración.

        Args:
            texto: Texto a narrar
            velocidad: Palabras por minuto (150-180 natural)

        Returns:
            Dict con 'audio_path' y 'duracion_estimada'
        """
        if not self.disponible:
            return {'status': 'skip', 'audio_path': None,
                    'advertencia': 'pyttsx3 no disponible'}

        try:
            import pyttsx3
            self.logger.info(f"🎙️  Generando narración ({len(texto)} caracteres)...")

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            audio_path = self.output_dir / f"narracion_{timestamp}.wav"

            # pyttsx3 en Windows necesita un engine nuevo por llamada
            # cuando se usa save_to_file repetidamente desde threads
            engine = pyttsx3.init()
            engine.setProperty('rate', velocidad)
            engine.setProperty('volume', 1.0)
            tiene_es = self._seleccionar_voz_espanola(engine)
            if not tiene_es:
                self.logger.warning("⚠️  No hay voz en español, usando voz por defecto")

            engine.save_to_file(texto, str(audio_path))
            engine.runAndWait()
            try:
                engine.stop()
            except Exception:
                pass

            if not audio_path.exists() or audio_path.stat().st_size < 1000:
                raise Exception("El archivo de audio no se generó correctamente")

            # Estimar duración: ~velocidad palabras/min
            num_palabras = len(texto.split())
            duracion_estimada = max(5, round((num_palabras / velocidad) * 60) + 1)

            self.logger.info(f"✅ Narración generada: {audio_path.name} (~{duracion_estimada}s)")
            return {
                'status': 'success',
                'audio_path': str(audio_path),
                'audio_filename': audio_path.name,
                'duracion_estimada': duracion_estimada,
                'voz_espanola': tiene_es,
            }

        except Exception as e:
            self.logger.error(f"❌ Error generando narración: {e}")
            return {'status': 'error', 'error': str(e), 'audio_path': None}

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
