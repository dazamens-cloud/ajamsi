"""
CAPTION WRITER AGENT
Responsabilidad: Generar captions y hashtags optimizados para TikTok
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class CaptionWriterAgent:
    """
    Agente especializado en crear captions y hashtags para TikTok.

    Responsabilidades:
    - Lee imagen + idea
    - Genera captions cortos (máx 280 caracteres)
    - Incluye hashtags trending locales
    - Múltiples versiones (hook, humor, call-to-action)
    """

    MAX_CARACTERES = 280
    HASHTAGS_TRENDING = ['#Lanzarote', '#Canarias', '#Humor', '#Meme', '#Local']

    HOOKS = [
        'Espera el final 👀',
        'No te lo vas a creer 😂',
        'Acertaste? 🤔',
        'Esto es Lanzarote 🏝️',
        'Si eres canario...',
    ]

    def __init__(self, config: Dict):
        """
        Inicializar el agente caption writer.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("✓ CaptionWriterAgent inicializado")

    def ejecutar(self, idea: Dict, num_captions: int = 3) -> Dict:
        """
        Generar captions optimizados para TikTok.

        Args:
            idea: Dict con concepto de idea
            num_captions: Cuántas variaciones generar

        Returns:
            Dict con captions listos para publicar
        """
        self.logger.info(f"✍️  Generando {num_captions} captions...")

        try:
            concepto = idea.get('concepto', '')
            palabras_clave = idea.get('palabras_clave', [])

            captions = []

            tipos = ['hook', 'humor', 'call_to_action'][:num_captions]

            for i, tipo in enumerate(tipos):
                caption = self._generar_caption(concepto, tipo, palabras_clave)
                hashtags = self._generar_hashtags(concepto, palabras_clave)

                caption_completo = f"{caption}\n\n{hashtags}"

                captions.append({
                    'id': f"caption_{datetime.now().timestamp()}_{i}",
                    'numero': i + 1,
                    'tipo': tipo,
                    'caption': caption,
                    'hashtags': hashtags,
                    'caption_completo': caption_completo,
                    'caracteres': len(caption),
                    'dentro_limite': len(caption) <= self.MAX_CARACTERES,
                    'engagement_score': 0.75 + (i * 0.05),
                })

            resultado = {
                'status': 'success',
                'idea_concepto': concepto,
                'captions_generados': len(captions),
                'captions': captions,
                'timestamp': datetime.now().isoformat(),
            }

            self.logger.info(f"✅ Captions generados: {len(captions)}")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error generando captions: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'captions': [],
            }

    def _generar_caption(self, concepto: str, tipo: str, palabras_clave: List[str]) -> str:
        """Generar caption basado en tipo"""
        if tipo == 'hook':
            hook = self.HOOKS[hash(concepto) % len(self.HOOKS)]
            return f"{hook} {concepto[:60]}"

        elif tipo == 'humor':
            return f"Que les parece? 😂 {concepto[:50]}..."

        elif tipo == 'call_to_action':
            return f"Sigue para más 👇 {concepto[:45]}..."

        else:
            return concepto[:self.MAX_CARACTERES]

    def _generar_hashtags(self, concepto: str, palabras_clave: List[str]) -> str:
        """Generar hashtags relacionados"""
        hashtags = self.HASHTAGS_TRENDING.copy()

        # Añadir hashtags de palabras clave
        for palabra in palabras_clave[:2]:
            if len(palabra) > 3:
                hashtags.append(f"#{palabra.lower()}")

        # Limitar a 8-10 hashtags
        hashtags = hashtags[:10]

        return ' '.join(hashtags)
