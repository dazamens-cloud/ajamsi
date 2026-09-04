"""
PROMPT ENGINEER AGENT
Responsabilidad: Optimizar prompts para Gemini Plus
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class PromptEngineerAgent:
    """
    Agente especializado en crear prompts optimizados para generación de imágenes.

    Responsabilidades:
    - Toma una idea creativa
    - Genera 2-3 versiones de prompt optimizadas
    - Añade contexto de estilo ("El Típico")
    - Exporta listos para Gemini
    """

    ESTILOS_VISUALES = {
        'folclórico': 'Estilo ilustración tradicional canaria, colores cálidos',
        'cartoon': 'Estilo cartoon moderno, líneas limpias',
        'vintage': 'Estilo retro/vintage, tonos sepia',
        'minimalista': 'Estilo minimalista, pocos elementos',
        'detallado': 'Muy detallado, realista con toques ilustrados',
    }

    PERSONAJE = 'El Típico Canario - hombre mayor con ropa tradicional, expresión sardónica'

    def __init__(self, config: Dict):
        """
        Inicializar el agente prompt engineer.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("✓ PromptEngineerAgent inicializado")

    def ejecutar(self, idea: Dict, num_prompts: int = 3) -> Dict:
        """
        Generar prompts optimizados para Gemini.

        Args:
            idea: Dict con concepto de idea
            num_prompts: Cuántas variaciones generar (default: 3)

        Returns:
            Dict con prompts listos para Gemini
        """
        self.logger.info(f"🎨 Optimizando prompts para: {idea.get('concepto', '')[:50]}...")

        try:
            concepto = idea.get('concepto', '')
            palabras_clave = idea.get('palabras_clave', [])

            prompts = []

            for i, estilo in enumerate(list(self.ESTILOS_VISUALES.keys())[:num_prompts]):
                prompt = self._construir_prompt(concepto, estilo, palabras_clave, i)
                prompts.append({
                    'id': f"prompt_{datetime.now().timestamp()}_{i}",
                    'numero': i + 1,
                    'estilo': estilo,
                    'descripcion_estilo': self.ESTILOS_VISUALES[estilo],
                    'prompt_text': prompt,
                    'personalizado': True,
                    'para_copiar': prompt,  # Listo para copiar-pegar
                })

            resultado = {
                'status': 'success',
                'idea_concepto': concepto,
                'prompts_generados': len(prompts),
                'prompts': prompts,
                'timestamp': datetime.now().isoformat(),
            }

            self.logger.info(f"✅ Prompts generados: {len(prompts)}")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error generando prompts: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'prompts': [],
            }

    def _construir_prompt(self, concepto: str, estilo: str, palabras_clave: List[str], numero: int) -> str:
        """Construir prompt optimizado para Gemini"""
        keywords = ', '.join(palabras_clave) if palabras_clave else 'Lanzarote'

        template = f"""
{self.PERSONAJE}

Concepto: {concepto}
Estilo visual: {self.ESTILOS_VISUALES[estilo]}
Contexto: {keywords}

Instrucciones:
- Humor sardónico típicamente canario
- Expresión de cara que transmita la emoción principal
- Paleta de colores: cálidos y vibrantes
- Técnica: Ilustración digital
- Calidad: Alta definición, listo para TikTok
- Evitar: Texto en la imagen, logos, elementos corporativos
        """.strip()

        return template
