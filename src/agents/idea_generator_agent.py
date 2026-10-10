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

            for i in range(num_ideas):
                setup, remate = self._generar_chiste_canario(titulo, contenido, i)
                idea = {
                    'id': f"idea_{datetime.now().timestamp()}_{i}",
                    'noticia_id': noticia.get('id'),
                    'concepto': self._generar_concepto(titulo, i),
                    'setup': setup,
                    'remate': remate,
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

    # Expresiones y referencias canarias para los chistes (estilo @hummorkana)
    SETUPS_CANARIOS = [
        "CHACHO, {tema}",
        "ÑOS, {tema}",
        "AGÜITA CON {tema}",
        "XIOS, {tema}",
        "MI NIÑO, {tema}",
    ]

    REMATES_CANARIOS = [
        "MÁS CONTENTO QUE CHICHARRERO EN LOS CARNAVALES",
        "ESO SÍ QUE ES UN PUNTAZO, MI NIÑO",
        "NI EL GOFIO LEVANTA TANTO EL ÁNIMO",
        "MÁS ORGULLOSO QUE ABUELA CON SUS PAPAS ARRUGADAS",
        "ESTO SE CELEBRA CON UN BARRAQUITO",
        "MÁS FELIZ QUE TURISTA EN EL TEIDE",
        "HASTA LA CABRA LO ESTÁ CELEBRANDO",
        "MÁS RÁPIDO QUE GUAGUA CUESTA ABAJO",
    ]

    REMATES_QUEJA = [
        "MÁS APRETADO QUE SARDINA EN LATA... Y SIN MOJO",
        "ME DERRITO MÁS RÁPIDO QUE QUESO EN SANCOCHO",
        "NI CON TRES BARRAQUITOS ME LEVANTO YO DE ESTA",
        "MÁS PERDIDO QUE TURISTA SIN GUAGUA",
        "ESTO NO LO ARREGLA NI EL GOFIO",
        "MÁS LENTO QUE LA COLA DEL FEROBUS",
        "AGÜITA, Y LUEGO DICEN QUE EXAGERAMOS",
    ]

    PALABRAS_NEGATIVAS = ['crisis', 'violencia', 'problema', 'denuncia', 'critica',
                          'dimisión', 'irresponsable', 'exigen', 'avisa', 'no es posible',
                          'falta', 'retraso', 'queja', 'polémica']

    def _generar_chiste_canario(self, titulo: str, contenido: str, numero: int) -> tuple:
        """Generar setup + remate estilo humor canario según el tono de la noticia"""
        # Tema condensado del titular (primeras palabras significativas)
        palabras = [p for p in titulo.split() if len(p) > 3][:6]
        tema = ' '.join(palabras) if palabras else titulo[:40]

        setup_plantilla = self.SETUPS_CANARIOS[(hash(titulo) + numero) % len(self.SETUPS_CANARIOS)]
        setup = setup_plantilla.format(tema=tema.upper())

        # Tono: celebración o queja según el titular
        es_negativa = any(p in titulo.lower() for p in self.PALABRAS_NEGATIVAS)
        remates = self.REMATES_QUEJA if es_negativa else self.REMATES_CANARIOS
        remate = remates[(hash(titulo) + numero) % len(remates)]

        return setup, remate

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
