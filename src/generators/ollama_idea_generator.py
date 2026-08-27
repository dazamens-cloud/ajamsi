"""
Ollama Idea Generator - Genera ideas usando Ollama local (Qwen)
"""

from typing import List, Optional
import logging
import json
import requests

from src.scrapers import Noticia
from .base_idea_generator import BaseIdeaGenerator, Idea

logger = logging.getLogger(__name__)


class OllamaIdeaGenerator(BaseIdeaGenerator):
    """
    Generador de ideas usando Ollama (Qwen local)

    Usa Qwen corriendo en Ollama para generar ideas creativas
    sin necesidad de API key. 100% local y gratis.
    """

    def __init__(self, config: dict):
        """
        Inicializar generador

        Args:
            config: Configuración del proyecto
        """
        super().__init__(config)

        self.modelo = "qwen:latest"  # Puedes cambiar a qwen2.5, qwen2, etc.
        self.ollama_url = "http://localhost:11434"
        self.disponible = False

        # Verificar que Ollama está disponible
        self._verificar_ollama()

    def _verificar_ollama(self):
        """Verificar si Ollama está corriendo"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.disponible = True
                logger.info(f"✓ Ollama disponible en {self.ollama_url}")
                logger.info(f"  Modelo a usar: {self.modelo}")
            else:
                logger.warning("❌ Ollama no responde")
        except Exception as e:
            logger.warning(f"Ollama no disponible: {e}")
            logger.warning("  Para usar Ollama, ejecuta: ollama pull qwen && ollama serve")

    def _generar_ideas_impl(self, noticia: Noticia, num_ideas: int) -> List[Idea]:
        """
        Generar ideas usando Ollama

        Args:
            noticia: Noticia a procesar
            num_ideas: Número de ideas

        Returns:
            Lista de ideas generadas
        """
        if not self.disponible:
            logger.warning("Ollama no disponible, usando ideas genéricas")
            return self._crear_ideas_genericas(noticia, num_ideas)

        try:
            # Extraer tema
            tema = self._extraer_tema_principal(noticia.titulo, noticia.contenido)
            elementos = self._sugerir_elementos_locales(tema)
            colores = self._sugerir_colores(tema)

            # Crear prompt para Qwen
            prompt = self._crear_prompt_qwen(noticia, num_ideas, tema)

            # Llamar a Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.modelo,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": self.temperatura,
                },
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Error Ollama: {response.status_code}")
                return self._crear_ideas_genericas(noticia, num_ideas)

            # Parsear respuesta
            resultado = response.json()
            contenido = resultado.get("response", "")
            ideas = self._parsear_respuesta(contenido, noticia, elementos, colores)

            return ideas if ideas else self._crear_ideas_genericas(noticia, num_ideas)

        except Exception as e:
            logger.error(f"Error con Ollama: {e}")
            return self._crear_ideas_genericas(noticia, num_ideas)

    def _crear_prompt_qwen(self, noticia: Noticia, num_ideas: int, tema: str) -> str:
        """
        Crear prompt optimizado para Qwen

        Args:
            noticia: Noticia a procesar
            num_ideas: Número de ideas
            tema: Tema detectado

        Returns:
            Prompt formateado
        """
        return f"""Eres un generador de ideas para memes y contenido viral en TikTok.
La audiencia es de Canarias, así que añade humor local canario.

Noticia: {noticia.titulo}
Contenido: {noticia.contenido[:300]}
Tema: {tema}

Genera {num_ideas} ideas creativas para memes/videos TikTok basados en esta noticia.
Para cada idea, incluye:
1. Título
2. Concepto (una frase corta)
3. Ángulo de humor (irónico, sarcástico, etc.)
4. Elementos locales canarios a incluir
5. Paleta de colores sugerida

Formato de respuesta JSON:
[
  {{
    "titulo": "...",
    "concepto": "...",
    "angulo_humor": "...",
    "elementos_locales": ["...", "..."],
    "colores": ["#color1", "#color2"]
  }}
]

Ideas:"""

    def _parsear_respuesta(self, contenido: str, noticia: Noticia,
                          elementos: List[str], colores: List[str]) -> List[Idea]:
        """
        Parsear respuesta de Qwen

        Args:
            contenido: Respuesta de Ollama
            noticia: Noticia original
            elementos: Elementos locales sugeridos
            colores: Colores sugeridos

        Returns:
            Lista de ideas parseadas
        """
        ideas = []

        try:
            # Intentar extraer JSON de la respuesta
            json_start = contenido.find("[")
            json_end = contenido.rfind("]") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = contenido[json_start:json_end]
                ideas_data = json.loads(json_str)

                for data in ideas_data:
                    idea = Idea(
                        titulo=data.get("titulo", ""),
                        noticia_id=noticia.titulo,
                        concepto=data.get("concepto", ""),
                        angulo_humor=data.get("angulo_humor", ""),
                        personaje="El Típico Canario",
                        estilo="canario_moderno",
                        colores=data.get("colores", colores),
                        elementos_locales=data.get("elementos_locales", elementos),
                        prompts_sugeridos=[]
                    )
                    ideas.append(idea)

        except json.JSONDecodeError:
            logger.warning("No se pudo parsear JSON de Qwen, usando ideas genéricas")

        return ideas if ideas else self._crear_ideas_genericas(noticia, 3)

    def _crear_ideas_genericas(self, noticia: Noticia, num_ideas: int) -> List[Idea]:
        """Crear ideas genéricas como fallback"""
        ideas_fallback = [
            Idea(
                titulo="Reacción sorprendida",
                noticia_id=noticia.titulo,
                concepto="Cara de sorpresa ante la noticia",
                angulo_humor="sarcasmo",
                personaje="El Típico Canario",
                estilo="canario_moderno",
                colores=["#FFD700", "#FF6347"],
                elementos_locales=["Bandera de Canarias", "Playa"],
                prompts_sugeridos=[]
            ),
            Idea(
                titulo="Antes y después",
                noticia_id=noticia.titulo,
                concepto="Comparación antes/después de la noticia",
                angulo_humor="irónico",
                personaje="El Típico Canario",
                estilo="canario_moderno",
                colores=["#1E90FF", "#FF69B4"],
                elementos_locales=["Volcán", "Paisaje canario"],
                prompts_sugeridos=[]
            ),
            Idea(
                titulo="Sátira política",
                noticia_id=noticia.titulo,
                concepto="Crítica ingeniosa sobre la situación",
                angulo_humor="satírico",
                personaje="El Típico Canario",
                estilo="canario_moderno",
                colores=["#228B22", "#FFD700"],
                elementos_locales=["Carnaval de Canarias", "Música local"],
                prompts_sugeridos=[]
            ),
        ]
        return ideas_fallback[:num_ideas]
