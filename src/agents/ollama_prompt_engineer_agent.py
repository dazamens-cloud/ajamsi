"""
OLLAMA PROMPT ENGINEER AGENT
Responsabilidad: Generar prompts creativos usando Ollama (SIN COSTO)
Reemplaza PromptEngineerAgent que usaba Gemini API
"""

import logging
import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class OllamaPromptEngineerAgent:
    """
    Agente especializado en crear prompts optimizados usando Ollama.

    Responsabilidades:
    - Toma una idea creativa
    - USA OLLAMA para generar prompts creativos dinámicamente
    - Genera 2-3 variaciones únicas
    - Añade contexto de estilo ("El Típico Canario")
    - Exporta listos para imagen generativa

    Ventajas vs Gemini:
    ✅ SIN COSTO
    ✅ 100% Local
    ✅ Sin límites API
    ✅ Privacidad garantizada
    """

    # Estilos visuales disponibles
    ESTILOS_VISUALES = {
        'folclórico': 'Estilo ilustración tradicional canaria, colores cálidos',
        'cartoon': 'Estilo cartoon moderno, líneas limpias y dinámicas',
        'vintage': 'Estilo retro/vintage, tonos sepia y nostálgicos',
        'minimalista': 'Estilo minimalista, pocos elementos pero impactantes',
        'detallado': 'Muy detallado, realista con toques ilustrados',
        'digital_art': 'Arte digital moderno, colores vibrantes',
        'abstracto': 'Abstracto con formas geométricas y colores contrastantes',
    }

    PERSONAJE = 'El Típico Canario - hombre mayor con ropa tradicional, expresión sardónica y humor local'

    def __init__(self, config: Dict):
        """
        Inicializar el agente prompt engineer con Ollama.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

        # Configuración de Ollama
        self.ollama_url = config.get('ollama_url', 'http://localhost:11434')
        self.modelo = config.get('ollama_modelo', 'mistral:latest')  # o 'llama2', 'neural-chat', etc.
        self.temperatura = config.get('ollama_temperatura', 0.7)
        self.disponible = False

        # Verificar disponibilidad
        self._verificar_ollama()
        self.logger.info("✓ OllamaPromptEngineerAgent inicializado")

    def _verificar_ollama(self) -> bool:
        """
        Verificar si Ollama está corriendo en el puerto configurado.

        Returns:
            True si Ollama está disponible, False si no
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                self.disponible = True
                modelos = response.json().get('models', [])
                self.logger.info(f"✓ Ollama disponible en {self.ollama_url}")
                self.logger.info(f"  Modelos disponibles: {len(modelos)}")
                self.logger.info(f"  Usando modelo: {self.modelo}")
                return True
            else:
                self.logger.warning(f"❌ Ollama responde pero status {response.status_code}")
                self._mostrar_instrucciones_ollama()
                return False
        except Exception as e:
            self.logger.warning(f"❌ Ollama no disponible: {e}")
            self._mostrar_instrucciones_ollama()
            return False

    def _mostrar_instrucciones_ollama(self):
        """Mostrar instrucciones para instalar/ejecutar Ollama"""
        print("""
        ⚠️  OLLAMA NO ESTÁ DISPONIBLE

        Para usar OllamaPromptEngineerAgent:

        1. Descarga Ollama desde: https://ollama.ai
        2. Instala en tu sistema
        3. Abre terminal y ejecuta:
           ollama pull mistral
           ollama serve

        4. Ollama se ejecutará en http://localhost:11434

        Modelos recomendados:
        - mistral      (Rápido, buen balance)
        - neural-chat  (Optimizado para chat)
        - llama2       (Más completo)
        - qwen:latest  (Muy bueno en creatividad)
        """)

    def ejecutar(self, idea: Dict, num_prompts: int = 3) -> Dict:
        """
        Generar prompts creativos usando Ollama.

        Args:
            idea: Dict con concepto de idea
            num_prompts: Cuántas variaciones generar (default: 3)

        Returns:
            Dict con prompts listos para imagen generativa
        """
        self.logger.info(f"🎨 [OLLAMA] Generando prompts para: {idea.get('concepto', '')[:50]}...")

        try:
            concepto = idea.get('concepto', '')
            palabras_clave = idea.get('palabras_clave', [])
            angulo_humor = idea.get('angulo_humor', 'humor')

            if not self.disponible:
                self.logger.warning("⚠️  Ollama no disponible, usando prompts estáticos")
                return self._generar_prompts_fallback(idea, num_prompts)

            prompts = []
            estilos_a_usar = list(self.ESTILOS_VISUALES.keys())[:num_prompts]

            for i, estilo in enumerate(estilos_a_usar):
                # Generar prompt dinámico con Ollama
                prompt_generado = self._generar_prompt_dinamico(
                    concepto,
                    estilo,
                    palabras_clave,
                    angulo_humor
                )

                prompts.append({
                    'id': f"ollama_prompt_{datetime.now().timestamp()}_{i}",
                    'numero': i + 1,
                    'estilo': estilo,
                    'descripcion_estilo': self.ESTILOS_VISUALES[estilo],
                    'prompt_text': prompt_generado,
                    'generador': 'ollama',  # Marca que fue generado por Ollama
                    'para_copiar': prompt_generado,
                })

            resultado = {
                'status': 'success',
                'idea_concepto': concepto,
                'prompts_generados': len(prompts),
                'prompts': prompts,
                'generador': 'ollama',
                'timestamp': datetime.now().isoformat(),
            }

            self.logger.info(f"✅ {len(prompts)} prompts generados por Ollama")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error generando prompts: {e}")
            return self._generar_prompts_fallback(idea, num_prompts)

    def _generar_prompt_dinamico(self, concepto: str, estilo: str,
                                 palabras_clave: List[str], angulo_humor: str) -> str:
        """
        Generar prompt dinámico usando Ollama.

        Args:
            concepto: Concepto de la idea
            estilo: Estilo visual a usar
            palabras_clave: Palabras clave de contexto
            angulo_humor: Ángulo de humor principal

        Returns:
            Prompt generado por Ollama
        """
        keywords = ', '.join(palabras_clave) if palabras_clave else 'Lanzarote, Canarias'

        # Crear prompt para Ollama
        prompt_ollama = f"""Eres un experto en descripción de imágenes para generadores como Stable Diffusion, DALL-E, etc.

Genera una descripción detallada y creativa para una imagen basada en:
- Concepto: {concepto}
- Estilo visual: {self.ESTILOS_VISUALES.get(estilo, 'moderno')}
- Contexto: {keywords}
- Personaje: {self.PERSONAJE}
- Ángulo de humor: {angulo_humor}

La descripción debe:
1. Ser detallada y visual (250-300 palabras)
2. Incluir detalles de composición y colores
3. Ser específica para generadores de imágenes
4. Mantener el humor canario sardónico
5. Ser lista para copiar-pegar directamente

Genera SOLO el prompt, sin introducciones ni explicaciones adicionales."""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.modelo,
                    "prompt": prompt_ollama,
                    "stream": False,
                    "temperature": self.temperatura,
                },
                timeout=30
            )

            if response.status_code == 200:
                resultado = response.json()
                prompt_generado = resultado.get('response', '').strip()
                if prompt_generado:
                    return prompt_generado
            else:
                self.logger.warning(f"Error Ollama: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error llamando Ollama: {e}")

        # Fallback a template si falla Ollama
        return self._construir_prompt_template(concepto, estilo, palabras_clave, angulo_humor)

    def _construir_prompt_template(self, concepto: str, estilo: str,
                                   palabras_clave: List[str], angulo_humor: str) -> str:
        """
        Construir prompt usando template como fallback.

        Args:
            concepto: Concepto de la idea
            estilo: Estilo visual
            palabras_clave: Palabras clave
            angulo_humor: Ángulo de humor

        Returns:
            Prompt formateado
        """
        keywords = ', '.join(palabras_clave) if palabras_clave else 'Lanzarote'

        template = f"""{self.PERSONAJE}

Concepto: {concepto}
Estilo visual: {self.ESTILOS_VISUALES[estilo]}
Contexto: {keywords}
Ángulo de humor: {angulo_humor}

Instrucciones de composición:
- Expresión facial que transmita {angulo_humor}
- Paleta de colores: cálidos y vibrantes
- Técnica: Ilustración digital de alta calidad
- Resolución: Optimizada para TikTok (9:16)
- Elementos: Incluir referencias locales canarias
- Evitar: Texto, logos, elementos corporativos
- Estado de ánimo: Auténtico, relatable, divertido

Detalles técnicos:
- Lighting: Natural, cálido
- Fondo: Sugerente pero no distractivo
- Profundidad: 3D moderno
- Calidad: 8k, ultra detallado"""

        return template

    def _generar_prompts_fallback(self, idea: Dict, num_prompts: int) -> Dict:
        """
        Generar prompts usando templates como fallback cuando Ollama no está disponible.

        Args:
            idea: Dict con concepto de idea
            num_prompts: Número de prompts a generar

        Returns:
            Dict con prompts fallback
        """
        self.logger.warning("⚠️  Usando prompts fallback (Ollama no disponible)")

        concepto = idea.get('concepto', '')
        palabras_clave = idea.get('palabras_clave', [])
        angulo_humor = idea.get('angulo_humor', 'humor')

        prompts = []
        estilos_a_usar = list(self.ESTILOS_VISUALES.keys())[:num_prompts]

        for i, estilo in enumerate(estilos_a_usar):
            prompt_text = self._construir_prompt_template(
                concepto,
                estilo,
                palabras_clave,
                angulo_humor
            )

            prompts.append({
                'id': f"fallback_prompt_{datetime.now().timestamp()}_{i}",
                'numero': i + 1,
                'estilo': estilo,
                'descripcion_estilo': self.ESTILOS_VISUALES[estilo],
                'prompt_text': prompt_text,
                'generador': 'fallback_template',
                'para_copiar': prompt_text,
            })

        return {
            'status': 'success',
            'idea_concepto': concepto,
            'prompts_generados': len(prompts),
            'prompts': prompts,
            'generador': 'fallback_template',
            'advertencia': 'Usando templates - Ollama no disponible',
            'timestamp': datetime.now().isoformat(),
        }

    def obtener_estado(self) -> Dict:
        """Obtener estado del agente"""
        return {
            'nombre': 'OllamaPromptEngineerAgent',
            'ollama_disponible': self.disponible,
            'ollama_url': self.ollama_url,
            'modelo': self.modelo,
            'estilos_disponibles': len(self.ESTILOS_VISUALES),
            'temperatura': self.temperatura,
        }
