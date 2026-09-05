"""
AGENT ORCHESTRATOR - Coordinador principal del pipeline AJAMSI
Responsabilidad: Orquestar todos los agentes en el pipeline de 4 fases
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path

# Import agents
from agents.scraper_agent import ScraperAgent
from agents.idea_generator_agent import IdeaGeneratorAgent
from agents.ollama_prompt_engineer_agent import OllamaPromptEngineerAgent
from agents.caption_writer_agent import CaptionWriterAgent
from agents.video_compiler_agent import VideoCompilerAgent
from agents.image_generator_agent import ImageGeneratorAgent
from agents.tts_agent import TTSAgent
from agents.publicacion_reporter_agent import PublicacionReporterAgent
from utils.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orquestador principal que coordina todos los agentes del pipeline.

    Pipeline:
    1. ScraperAgent -> Obtener noticias reales
    2. IdeaGeneratorAgent -> Generar ideas/ángulos
    3. OllamaPromptEngineerAgent -> Generar prompts para imagen
    4. CaptionWriterAgent -> Generar captions para redes
    5. VideoCompilerAgent -> Compilar video final
    """

    def __init__(self):
        """Inicializar orquestador con todos los agentes"""
        try:
            # Cargar configuración
            config_path = Path(__file__).parent.parent / "config" / "config.json"
            if config_path.exists():
                config_loader = ConfigLoader(str(config_path))
                self.config = config_loader.to_dict()
            else:
                self.config = {
                    'ambiente': 'desarrollo',
                    'noticias_dias_atras': 7,
                    'max_noticias': 12,
                    'modelos': {
                        'ollama': 'qwen:3.5-9b-instruct',
                    }
                }

            # Inicializar agentes
            self.scraper = ScraperAgent(self.config)
            self.idea_generator = IdeaGeneratorAgent(self.config)
            self.prompt_engineer = OllamaPromptEngineerAgent(self.config)
            self.caption_writer = CaptionWriterAgent(self.config)
            self.video_compiler = VideoCompilerAgent(self.config)
            self.image_generator = ImageGeneratorAgent(self.config)
            self.tts = TTSAgent(self.config)
            self.reporter = PublicacionReporterAgent(self.config)

            logger.info("✅ AgentOrchestrator inicializado correctamente")

        except Exception as e:
            logger.error(f"❌ Error inicializando AgentOrchestrator: {e}")
            raise

    def scrappear_noticias(self, dias_atras: int = 7) -> Dict:
        """
        FASE 1: Ejecutar scraper para obtener noticias reales

        Args:
            dias_atras: Cuántos días atrás buscar noticias

        Returns:
            Dict con 'noticias' lista de noticias scrapeadas
        """
        try:
            logger.info(f"🕷️  Iniciando scraping de noticias (últimos {dias_atras} días)...")

            # Ejecutar scraper
            resultado = self.scraper.ejecutar(
                dias_atras=dias_atras,
                limite_noticias=self.config.get('max_noticias', 12)
            )

            noticias = resultado.get('noticias', [])
            logger.info(f"✅ Fase 1 completada: {len(noticias)} noticias obtenidas")

            return {
                'status': 'success',
                'noticias': noticias,
                'total': len(noticias)
            }

        except Exception as e:
            logger.error(f"❌ Error en Fase 1 (Scraping): {e}")
            return {
                'status': 'error',
                'error': str(e),
                'noticias': []
            }

    def generar_ideas(self, noticia: Dict, num_ideas: int = 2) -> Dict:
        """
        FASE 2: Generar ideas/ángulos humorísticos para una noticia

        Args:
            noticia: Dict con información de la noticia
            num_ideas: Cuántas ideas generar

        Returns:
            Dict con 'ideas' lista de ideas generadas
        """
        try:
            logger.info(f"💡 Generando ideas para noticia: {noticia.get('titulo', '')[:50]}...")

            # Generar ideas
            resultado = self.idea_generator.ejecutar(
                noticia=noticia,
                num_ideas=num_ideas
            )

            ideas = resultado.get('ideas', [])
            logger.info(f"✅ Fase 2 completada: {len(ideas)} ideas generadas")

            return {
                'status': 'success',
                'ideas': ideas,
                'total': len(ideas)
            }

        except Exception as e:
            logger.error(f"❌ Error en Fase 2 (Ideas): {e}")
            return {
                'status': 'error',
                'error': str(e),
                'ideas': []
            }

    def optimizar_prompts(self, idea: Dict, num_prompts: int = 2) -> Dict:
        """
        FASE 2B: Generar prompts de imagen con Ollama (para representar la idea)

        Args:
            idea: Dict con información de la idea
            num_prompts: Cuántos prompts generar

        Returns:
            Dict con 'prompts' lista de prompts para imagen
        """
        try:
            logger.info(f"🎨 Generando prompts para idea: {idea.get('ángulo', '')[:50]}...")

            # Generar prompts
            resultado = self.prompt_engineer.ejecutar(
                idea=idea,
                num_prompts=num_prompts
            )

            prompts = resultado.get('prompts', [])
            logger.info(f"✅ Prompts generados: {len(prompts)}")

            return {
                'status': 'success',
                'prompts': prompts,
                'total': len(prompts)
            }

        except Exception as e:
            logger.error(f"❌ Error generando prompts: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'prompts': []
            }

    def generar_captions(self, idea: Dict, num_captions: int = 3) -> Dict:
        """
        FASE 3: Generar captions para redes sociales (TikTok/Instagram)

        Args:
            idea: Dict con información de la idea
            num_captions: Cuántos captions generar

        Returns:
            Dict con 'captions' lista de captions generados
        """
        try:
            logger.info(f"✍️  Generando captions para la idea...")

            # Generar captions
            resultado = self.caption_writer.ejecutar(
                idea=idea,
                num_captions=num_captions
            )

            captions = resultado.get('captions', [])
            logger.info(f"✅ Fase 3 completada: {len(captions)} captions generados")

            return {
                'status': 'success',
                'captions': captions,
                'total': len(captions)
            }

        except Exception as e:
            logger.error(f"❌ Error en Fase 3 (Captions): {e}")
            return {
                'status': 'error',
                'error': str(e),
                'captions': []
            }

    def compilar_video(self,
                       imagen_path: str,
                       guion: str,
                       audio_path: Optional[str] = None,
                       formato: str = 'tiktok') -> Dict:
        """
        FASE 4: Compilar video final en múltiples formatos

        Args:
            imagen_path: Ruta a imagen base
            guion: Guión/descripción del video
            audio_path: Ruta a archivo de audio (opcional)
            formato: 'tiktok', 'instagram', 'youtube'

        Returns:
            Dict con ruta del video compilado
        """
        try:
            logger.info(f"🎬 Compilando video en formato {formato}...")

            # Compilar video
            resultado = self.video_compiler.ejecutar(
                imagen_path=imagen_path,
                guion=guion,
                audio_path=audio_path,
                formato=formato
            )

            logger.info(f"✅ Fase 4 completada: Video generado")

            return {
                'status': 'success',
                'video_path': resultado.get('video_path'),
                'formato': formato,
                'duracion': resultado.get('duracion')
            }

        except Exception as e:
            logger.error(f"❌ Error en Fase 4 (Video): {e}")
            return {
                'status': 'error',
                'error': str(e),
                'video_path': None
            }

    def ejecutar_pipeline_completo(self, noticias: List[Dict], progreso_cb=None) -> Dict:
        """
        Pipeline COMPLETO por cada noticia seleccionada:
        idea -> captions -> imagen -> narración TTS -> video -> documento Word

        Args:
            noticias: Lista de noticias seleccionadas
            progreso_cb: callback(porcentaje, paso, detalle) para reportar progreso

        Returns:
            Dict con 'resultados' (uno por noticia), 'doc_path' y 'errores'
        """
        def reportar(pct, paso, detalle=''):
            if progreso_cb:
                try:
                    progreso_cb(pct, paso, detalle)
                except Exception:
                    pass
            logger.info(f"[{pct}%] {paso} - {detalle}")

        resultados = []
        errores = []
        total = len(noticias)
        # 5 pasos por noticia + 1 paso final (documento)
        pasos_totales = total * 5 + 1
        paso_actual = 0

        for i, noticia in enumerate(noticias, 1):
            titulo_corto = noticia.get('titulo', '')[:45]
            item = {'noticia': noticia, 'idea': None, 'captions': [],
                    'imagen': None, 'audio': None, 'video': None}

            try:
                # 1. Idea
                paso_actual += 1
                reportar(int(paso_actual / pasos_totales * 100),
                         f"💡 Generando idea ({i}/{total})", titulo_corto)
                ideas_res = self.idea_generator.ejecutar(noticia=noticia, num_ideas=2)
                ideas = ideas_res.get('ideas', [])
                if not ideas:
                    raise Exception("No se generaron ideas")
                item['idea'] = ideas[0]

                # 2. Captions
                paso_actual += 1
                reportar(int(paso_actual / pasos_totales * 100),
                         f"✍️ Generando captions ({i}/{total})", titulo_corto)
                captions_res = self.caption_writer.ejecutar(idea=item['idea'], num_captions=3)
                item['captions'] = captions_res.get('captions', [])

                # 3. Imagen (tarjeta meme)
                paso_actual += 1
                reportar(int(paso_actual / pasos_totales * 100),
                         f"🖼️ Generando imagen ({i}/{total})", titulo_corto)
                hook = item['captions'][0].get('caption', '') if item['captions'] else ''
                imagen_res = self.image_generator.ejecutar(
                    noticia=noticia, idea=item['idea'], hook=hook)
                if imagen_res.get('status') != 'success':
                    raise Exception(f"Imagen falló: {imagen_res.get('error')}")
                item['imagen'] = imagen_res

                # 4. Narración TTS
                paso_actual += 1
                reportar(int(paso_actual / pasos_totales * 100),
                         f"🎙️ Generando narración ({i}/{total})", titulo_corto)
                guion = self.tts.construir_guion(noticia, item['idea'])
                audio_res = self.tts.ejecutar(guion)
                item['audio'] = audio_res
                audio_path = audio_res.get('audio_path')
                duracion = audio_res.get('duracion_estimada', 15) or 15

                # 5. Video
                paso_actual += 1
                reportar(int(paso_actual / pasos_totales * 100),
                         f"🎬 Compilando video ({i}/{total})", titulo_corto)
                video_res = self.video_compiler.ejecutar(
                    imagen_path=imagen_res['imagen_path'],
                    guion=guion,
                    audio_path=audio_path,
                    duracion=min(duracion, 60),
                    formato='tiktok',
                    nombre_base=f"noticia{i}"
                )
                if video_res.get('status') != 'success':
                    raise Exception(f"Video falló: {video_res.get('error')}")
                item['video'] = video_res

                resultados.append(item)

            except Exception as e:
                logger.error(f"❌ Error procesando noticia {i}: {e}")
                errores.append({'noticia': titulo_corto, 'error': str(e)})
                if item.get('video') is None:
                    resultados.append(item)  # guardar lo que se logró para el reporte

        # Documento Word final
        paso_actual += 1
        reportar(int(paso_actual / pasos_totales * 100),
                 "📄 Generando guía de publicación", "Word con captions y hashtags")
        con_video = [r for r in resultados if r.get('video')]
        doc_res = self.reporter.ejecutar(con_video) if con_video else {'doc_path': None}

        reportar(100, "✅ Pipeline completado",
                 f"{len(con_video)}/{total} videos generados")

        return {
            'status': 'success' if con_video else 'error',
            'resultados': resultados,
            'videos_generados': len(con_video),
            'doc_path': doc_res.get('doc_path'),
            'errores': errores,
        }
