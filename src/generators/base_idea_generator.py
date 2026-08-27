"""
Base Idea Generator - Clase abstracta para generadores de ideas
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
import logging

from src.scrapers import Noticia

logger = logging.getLogger(__name__)


@dataclass
class Idea:
    """Estructura de datos para una idea de contenido"""
    titulo: str
    noticia_id: Optional[str] = None
    concepto: str = ""
    angulo_humor: str = ""
    personaje: str = "El Típico"
    estilo: str = "ilustración folclórica"
    colores: List[str] = None
    elementos_locales: List[str] = None
    prompts_sugeridos: List[str] = None
    relevancia_score: float = 0.0

    def __post_init__(self):
        """Inicializar listas vacías si no se proporcionan"""
        if self.colores is None:
            self.colores = []
        if self.elementos_locales is None:
            self.elementos_locales = []
        if self.prompts_sugeridos is None:
            self.prompts_sugeridos = []

    def __repr__(self) -> str:
        return f"<Idea: {self.titulo[:50]}... ({self.angulo_humor})>"


class BaseIdeaGenerator(ABC):
    """
    Clase base para generadores de ideas

    Define la interfaz común y proporciona utilidades compartidas
    """

    def __init__(self, config: dict):
        """
        Inicializar generador de ideas

        Args:
            config: Configuración del proyecto
        """
        self.config = config
        self.generador_config = config.get("generador_ideas", {})
        self.idioma = self.generador_config.get("idioma", "es")
        self.tono = self.generador_config.get("tono", "humor_sardónico_canario")
        self.modelo = self.generador_config.get("modelo", "claude-3-5-sonnet")
        self.temperatura = self.generador_config.get("temperatura", 0.7)
        self.max_tokens = self.generador_config.get("max_tokens", 500)

        logger.info(f"Inicializado generador de ideas: {self.__class__.__name__}")
        logger.info(f"  Idioma: {self.idioma}")
        logger.info(f"  Tono: {self.tono}")
        logger.info(f"  Modelo: {self.modelo}")

    def generar_ideas(self, noticia: Noticia, num_ideas: int = 3) -> List[Idea]:
        """
        Generar ideas de contenido desde una noticia

        Args:
            noticia: Objeto Noticia scrapeado
            num_ideas: Número de ideas a generar (default 3)

        Returns:
            Lista de objetos Idea
        """
        try:
            logger.info(f"Generando {num_ideas} ideas para: {noticia.titulo[:50]}...")

            # Validar noticia
            if not noticia or not noticia.titulo:
                logger.warning("Noticia inválida")
                return []

            # Generar ideas (implementación específica por subclass)
            ideas = self._generar_ideas_impl(noticia, num_ideas)

            if ideas:
                logger.info(f"✓ Generadas {len(ideas)} ideas")
            else:
                logger.warning("No se generaron ideas")

            return ideas

        except Exception as e:
            logger.error(f"Error generando ideas: {e}", exc_info=True)
            return []

    @abstractmethod
    def _generar_ideas_impl(self, noticia: Noticia, num_ideas: int) -> List[Idea]:
        """
        Implementación específica de generación de ideas

        Args:
            noticia: Noticia scrapeada
            num_ideas: Número de ideas a generar

        Returns:
            Lista de ideas generadas
        """
        pass

    def _crear_idea(self, titulo: str, concepto: str, angulo: str,
                   noticia: Noticia = None, **kwargs) -> Idea:
        """
        Factory para crear una idea

        Args:
            titulo: Título corto de la idea
            concepto: Concepto principal del meme
            angulo: Ángulo humorístico
            noticia: Noticia relacionada (opcional)
            **kwargs: Argumentos adicionales (colores, elementos_locales, etc.)

        Returns:
            Objeto Idea
        """
        idea = Idea(
            titulo=titulo,
            noticia_id=noticia.url if noticia else None,
            concepto=concepto,
            angulo_humor=angulo,
            personaje=kwargs.get("personaje", "El Típico"),
            estilo=kwargs.get("estilo", "ilustración folclórica"),
            colores=kwargs.get("colores", ["ocre", "marrón", "naranja"]),
            elementos_locales=kwargs.get("elementos_locales", []),
            prompts_sugeridos=kwargs.get("prompts_sugeridos", []),
        )

        return idea

    def _extraer_tema_principal(self, titulo: str, contenido: str = None) -> str:
        """
        Extraer tema principal de la noticia

        Args:
            titulo: Título de la noticia
            contenido: Contenido de la noticia (opcional)

        Returns:
            Tema principal identificado
        """
        # Temas comunes en Canarias
        temas_comunes = {
            "viento": ["viento", "aire", "ráfaga", "tormenta"],
            "turismo": ["turista", "turismo", "hotel", "playa", "viajero"],
            "política": ["gobierno", "elecciones", "cabildo", "política"],
            "economía": ["dinero", "empresa", "negocio", "trabajo"],
            "cultura": ["cultura", "arte", "música", "fiesta", "tradición"],
            "deporte": ["fútbol", "deporte", "equipo", "partido", "atleta"],
        }

        texto_bajo = (titulo + " " + (contenido or "")).lower()

        for tema, palabras_clave in temas_comunes.items():
            if any(palabra in texto_bajo for palabra in palabras_clave):
                return tema

        return "general"

    def _sugerir_elementos_locales(self, tema: str) -> List[str]:
        """
        Sugerir elementos locales según el tema

        Args:
            tema: Tema principal

        Returns:
            Lista de elementos locales sugeridos
        """
        elementos_por_tema = {
            "viento": ["molino", "vela", "bandera volando", "pelo al aire"],
            "turismo": ["sombrilla", "maleta", "cámara", "palmera"],
            "política": ["papeleta", "micrófono", "escritorio", "corbata"],
            "economía": ["dinero", "moneda", "gráfico", "briefcase"],
            "cultura": ["guitarra", "tambor", "libro", "pincel"],
            "deporte": ["balón", "camiseta", "trofeo", "cancha"],
            "general": ["El Típico", "Lanzarote", "noticia"],
        }

        return elementos_por_tema.get(tema, elementos_por_tema["general"])

    def _sugerir_colores(self, tema: str) -> List[str]:
        """
        Sugerir paleta de colores según tema

        Args:
            tema: Tema principal

        Returns:
            Lista de colores sugeridos
        """
        colores_por_tema = {
            "viento": ["azul cielo", "blanco", "gris"],
            "turismo": ["turquesa", "dorado", "blanco"],
            "política": ["azul oscuro", "rojo", "gris"],
            "economía": ["verde", "dorado", "gris"],
            "cultura": ["ocre", "naranja", "marrón"],
            "deporte": ["rojo", "amarillo", "verde"],
            "general": ["ocre", "marrón", "naranja"],
        }

        return colores_por_tema.get(tema, colores_por_tema["general"])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.idioma}, {self.tono}>"
