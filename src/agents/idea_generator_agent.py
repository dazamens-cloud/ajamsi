"""
IDEA GENERATOR AGENT
Responsabilidad: Generar conceptos creativos y ángulos humorísticos
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class IdeaGeneratorAgent:
    """
    Agente especializado en generar ideas creativas para videos.

    Responsabilidades:
    - Lee una noticia
    - Genera 3-5 ángulos humorísticos
    - Respeta personaje "El Típico"
    - Usa preferencias acumuladas
    """

    ESTILOS_HUMOR = {
        'sardónico': 'Humor seco, irónico, típicamente canario',
        'absurdo': 'Humor absurdo y exagerado',
        'satírico': 'Crítica social con humor',
        'nostálgico': 'Referencia a tradiciones canarias',
        'cotidiano': 'Situaciones del día a día exageradas',
    }

    def __init__(self, config: Dict):
        """
        Inicializar el agente generador de ideas.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("✓ IdeaGeneratorAgent inicializado")

    def ejecutar(self, noticia: Dict, num_ideas: int = 3, preferencias: Optional[Dict] = None) -> Dict:
        """
        Generar ideas creativas para una noticia.

        Args:
            noticia: Dict con información de la noticia
            num_ideas: Cuántas ideas generar (default: 3)
            preferencias: Sistema de preferencias acumuladas (opcional)

        Returns:
            Dict con ideas generadas
        """
        self.logger.info(f"💡 Generando {num_ideas} ideas para: {noticia.get('titulo', '')[:50]}...")

        try:
            titulo = noticia.get('titulo', '')
            contenido = noticia.get('contenido', '')

            ideas = []

            # TODO: Integrar con Claude API para generación real
            # Por ahora, mock ideas
            for i in range(num_ideas):
                idea = {
                    'id': f"idea_{datetime.now().timestamp()}_{i}",
                    'noticia_id': noticia.get('id'),
                    'concepto': self._generar_concepto(titulo, i),
                    'angulo_humor': self._seleccionar_humor(i),
                    'descripcion': self._generar_descripcion(titulo, i),
                    'palabras_clave': self._extraer_palabras_clave(titulo),
                    'dificultad': ['fácil', 'media', 'difícil'][i % 3],
                    'relevancia': 0.75 + (i * 0.05),
                    'fecha_creacion': datetime.now().isoformat(),
                }
                ideas.append(idea)

            resultado = {
                'status': 'success',
                'noticia_titulo': titulo,
                'ideas_generadas': len(ideas),
                'ideas': ideas,
                'timestamp': datetime.now().isoformat(),
            }

            self.logger.info(f"✅ Ideas generadas: {len(ideas)}")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error generando ideas: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'ideas': [],
            }

    def _generar_concepto(self, titulo: str, numero: int) -> str:
        """Generar concepto de meme basado en título"""
        conceptos_base = [
            f"El Típico reaccionando a: {titulo[:40]}",
            f"Comparación irónica: Lanzarote vs realidad ({titulo[:30]})",
            f"Exageración absurda: {titulo[:40]}",
        ]
        return conceptos_base[numero % len(conceptos_base)]

    def _seleccionar_humor(self, numero: int) -> str:
        """Seleccionar tipo de humor"""
        humores = list(self.ESTILOS_HUMOR.keys())
        return humores[numero % len(humores)]

    def _generar_descripcion(self, titulo: str, numero: int) -> str:
        """Generar descripción de la idea"""
        return f"Idea {numero + 1}: {titulo[:50]}... con ángulo humorístico local"

    def _extraer_palabras_clave(self, titulo: str) -> List[str]:
        """Extraer palabras clave del título"""
        # TODO: Mejorar con NLP
        palabras = titulo.lower().split()
        return [p for p in palabras if len(p) > 4][:5]
