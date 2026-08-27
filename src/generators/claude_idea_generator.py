"""
Claude Idea Generator - Genera ideas usando Claude API
"""

from typing import List, Optional
import logging
import json

from src.scrapers import Noticia
from .base_idea_generator import BaseIdeaGenerator, Idea

logger = logging.getLogger(__name__)


class ClaudeIdeaGenerator(BaseIdeaGenerator):
    """
    Generador de ideas usando Claude API

    Usa Claude 3.5 Sonnet para generar ideas creativas de memes canarios
    desde noticias scrapeadas.
    """

    def __init__(self, config: dict, api_key: Optional[str] = None):
        """
        Inicializar generador

        Args:
            config: Configuración del proyecto
            api_key: API key de Claude (si no está en env vars)
        """
        super().__init__(config)

        self.api_key = api_key
        self.client = None

        # Importar cliente de Claude
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key) if api_key else Anthropic()
            logger.info("✓ Cliente Claude inicializado")
        except ImportError:
            logger.warning("Librería anthropic no disponible. Modo fallback activado.")
        except Exception as e:
            logger.error(f"Error inicializando cliente Claude: {e}")

    def _generar_ideas_impl(self, noticia: Noticia, num_ideas: int) -> List[Idea]:
        """
        Generar ideas usando Claude

        Args:
            noticia: Noticia a procesar
            num_ideas: Número de ideas

        Returns:
            Lista de ideas generadas
        """
        if not self.client:
            logger.warning("Cliente Claude no disponible, usando fallback")
            return self._generar_ideas_fallback(noticia, num_ideas)

        try:
            # Extraer tema
            tema = self._extraer_tema_principal(noticia.titulo, noticia.contenido)
            elementos = self._sugerir_elementos_locales(tema)
            colores = self._sugerir_colores(tema)

            # Crear prompt
            prompt = self._crear_prompt_generacion(noticia, num_ideas, tema)

            # Llamar a Claude
            response = self.client.messages.create(
                model=self.modelo,
                max_tokens=self.max_tokens,
                temperature=self.temperatura,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parsear respuesta
            contenido = response.content[0].text
            ideas = self._parsear_respuesta(contenido, noticia, elementos, colores)

            return ideas

        except Exception as e:
            logger.error(f"Error con Claude API: {e}")
            logger.info("Usando generador fallback")
            return self._generar_ideas_fallback(noticia, num_ideas)

    def _crear_prompt_generacion(self, noticia: Noticia, num_ideas: int, tema: str) -> str:
        """
        Crear prompt para Claude

        Args:
            noticia: Noticia a procesar
            num_ideas: Número de ideas
            tema: Tema identificado

        Returns:
            Prompt para Claude
        """
        prompt = f"""
Eres un experto en crear memes canarios divertidos y virales.
Tu tarea es generar {num_ideas} ideas de memes basados en la siguiente noticia.

CONTEXTO:
- Personaje: El Típico (personaje folclórico canario)
- Estilo: Ilustración folclórica con humor sardónico
- Isla: Lanzarote
- Idioma: Español (con acento canario)
- Tono: Humor local, satírico pero amable

NOTICIA:
Título: {noticia.titulo}
Contenido: {noticia.contenido or "No disponible"}

TEMA IDENTIFICADO: {tema}

POR FAVOR, GENERA {num_ideas} IDEAS DE MEMES:

Para cada idea, proporciona:
1. TÍTULO: Nombre corto de la idea (máx 10 palabras)
2. CONCEPTO: Descripción breve del meme (máx 30 palabras)
3. ÁNGULO HUMORÍSTICO: Qué es lo gracioso (máx 20 palabras)
4. ELEMENTOS LOCALES: Elementos canarios a incluir (lista)
5. PROMPT PARA IMAGEN: Descripción detallada para generar la imagen

Asegúrate de que cada idea:
- Sea respetuosa pero satírica
- Use humor canario (referencias locales, acento, cultura)
- Sea fácil de visualizar
- Sea potencialmente viral en TikTok

FORMATO DE RESPUESTA (JSON):
```json
{{
  "ideas": [
    {{
      "titulo": "...",
      "concepto": "...",
      "angulo": "...",
      "elementos": ["...", "..."],
      "prompt_imagen": "..."
    }}
  ]
}}
```
"""
        return prompt.strip()

    def _parsear_respuesta(self, contenido: str, noticia: Noticia,
                          elementos: List[str], colores: List[str]) -> List[Idea]:
        """
        Parsear respuesta de Claude

        Args:
            contenido: Texto de respuesta de Claude
            noticia: Noticia original
            elementos: Elementos locales sugeridos
            colores: Colores sugeridos

        Returns:
            Lista de ideas parseadas
        """
        ideas = []

        try:
            # Extraer JSON
            inicio = contenido.find("{")
            fin = contenido.rfind("}") + 1

            if inicio == -1 or fin <= inicio:
                logger.warning("No se encontró JSON en respuesta")
                return []

            json_str = contenido[inicio:fin]
            datos = json.loads(json_str)

            # Procesar ideas
            for item in datos.get("ideas", []):
                idea = self._crear_idea(
                    titulo=item.get("titulo", "Sin título"),
                    concepto=item.get("concepto", ""),
                    angulo=item.get("angulo", ""),
                    noticia=noticia,
                    personaje="El Típico",
                    estilo="ilustración folclórica",
                    colores=colores,
                    elementos_locales=item.get("elementos", elementos),
                    prompts_sugeridos=[item.get("prompt_imagen", "")]
                )

                ideas.append(idea)
                logger.debug(f"✓ Idea creada: {idea.titulo}")

            return ideas

        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error procesando respuesta: {e}")
            return []

    def _generar_ideas_fallback(self, noticia: Noticia, num_ideas: int) -> List[Idea]:
        """
        Generador fallback cuando Claude no está disponible

        Args:
            noticia: Noticia a procesar
            num_ideas: Número de ideas

        Returns:
            Ideas genéricas fallback
        """
        logger.info(f"Generando {num_ideas} ideas fallback")

        tema = self._extraer_tema_principal(noticia.titulo, noticia.contenido)
        elementos = self._sugerir_elementos_locales(tema)
        colores = self._sugerir_colores(tema)

        ideas_fallback = [
            self._crear_idea(
                titulo=f"El Típico y la noticia",
                concepto=f"El Típico reaccionando a: {noticia.titulo[:40]}",
                angulo="Reacción sorprendida",
                noticia=noticia,
                elementos_locales=elementos,
                colores=colores,
                prompts_sugeridos=[
                    f"El Típico canario asombrado por la noticia de {tema}, "
                    f"ilustración folclórica, elementos locales: {', '.join(elementos[:2])}"
                ]
            ),
            self._crear_idea(
                titulo=f"Cuando te enteras de...",
                concepto=f"Meme de reacción sobre {noticia.titulo[:40]}",
                angulo="Humor por contraste",
                noticia=noticia,
                elementos_locales=elementos,
                colores=colores,
                prompts_sugeridos=[
                    f"Dos versiones del Típico: antes y después de enterarse de {tema}"
                ]
            ),
            self._crear_idea(
                titulo=f"{tema.capitalize()} en Lanzarote",
                concepto=f"Crítica satírica de {noticia.titulo[:40]}",
                angulo="Sátira local",
                noticia=noticia,
                elementos_locales=elementos,
                colores=colores,
                prompts_sugeridos=[
                    f"Caricatura del Típico comentando sobre {tema} con toque canario"
                ]
            )
        ]

        return ideas_fallback[:num_ideas]

    def __repr__(self) -> str:
        return f"<ClaudeIdeaGenerator: {self.modelo}>"
