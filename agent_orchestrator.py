"""
AGENT ORCHESTRATOR
Orquestador central que coordina todos los 10 agentes especializados de AjamSi
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar todos los agentes
from agents import (
    ScraperAgent,
    IdeaGeneratorAgent,
    OllamaPromptEngineerAgent,  # NUEVO: USA OLLAMA (sin Gemini API)
    VideoCompilerAgent,
    CaptionWriterAgent,
    BatchProcessorAgent,
    FeedbackAnalyzerAgent,
    ContentValidatorAgent,
    AnalyticsAgent,
    DriveSyncAgent,
)

from utils.config_loader import ConfigLoader


class AgentOrchestrator:
    """
    Orquestador central que coordina los 10 agentes especializados.

    Agentes disponibles:
    1. ScraperAgent - Web scraping de noticias
    2. IdeaGeneratorAgent - Generación de ideas creativas
    3. OllamaPromptEngineerAgent - Generación de prompts con OLLAMA (SIN COSTO, 100% LOCAL)
    4. VideoCompilerAgent - Compilación de videos
    5. CaptionWriterAgent - Generación de captions
    6. BatchProcessorAgent - Orquestación de bloques completos
    7. FeedbackAnalyzerAgent - Análisis de feedback
    8. ContentValidatorAgent - Validación de contenido
    9. AnalyticsAgent - Análisis de métricas
    10. DriveSyncAgent - Sincronización con Google Drive

    CAMBIO FASE 1: Reemplazó PromptEngineerAgent (Gemini API) por OllamaPromptEngineerAgent
    - Usa Ollama en lugar de Gemini
    - Sin costo
    - 100% local
    - Privacidad garantizada
    """

    def __init__(self, config_path: str = "config/config.json"):
        """
        Inicializar el orquestador con todos los agentes.

        Args:
            config_path: Ruta al archivo de configuración
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("🤖 Inicializando AgentOrchestrator...")

        # Cargar configuración
        try:
            self.config_loader = ConfigLoader(config_path)
            self.config = self.config_loader.to_dict()
        except Exception as e:
            self.logger.warning(f"⚠️  No se encontró {config_path}, usando config vacía")
            self.config = {}

        # Inicializar todos los agentes
        self.agentes = {
            'scraper': ScraperAgent(self.config),
            'idea_generator': IdeaGeneratorAgent(self.config),
            'prompt_engineer': OllamaPromptEngineerAgent(self.config),  # CAMBIO: OLLAMA en lugar de Gemini
            'video_compiler': VideoCompilerAgent(self.config),
            'caption_writer': CaptionWriterAgent(self.config),
            'feedback_analyzer': FeedbackAnalyzerAgent(self.config),
            'content_validator': ContentValidatorAgent(self.config),
            'analytics': AnalyticsAgent(self.config),
            'drive_sync': DriveSyncAgent(self.config),
        }

        # Inicializar batch processor con los agentes
        self.agentes['batch_processor'] = BatchProcessorAgent(self.config, self.agentes)

        self.logger.info("✅ AgentOrchestrator inicializado con 10 agentes")

    def ejecutar_batch_completo(self, nombre_batch: Optional[str] = None) -> Dict:
        """
        Ejecutar un batch completo del pipeline.

        Fases:
        1. Scraping de noticias
        2. Generación de ideas
        3. Optimización de prompts
        4. Generación de captions
        5. Compilación de videos
        6. Validación de contenido
        7. Análisis de feedback
        8. Sincronización con Drive

        Args:
            nombre_batch: Nombre identificador del batch (optional)

        Returns:
            Dict con resultado completo
        """
        self.logger.info("🚀 Ejecutando batch completo del pipeline")
        return self.agentes['batch_processor'].ejecutar_batch_completo(nombre_batch)

    def scrappear_noticias(self, dias_atras: int = 7) -> Dict:
        """Scrappear noticias"""
        return self.agentes['scraper'].ejecutar(dias_atras=dias_atras)

    def generar_ideas(self, noticia: Dict, num_ideas: int = 3) -> Dict:
        """Generar ideas para una noticia"""
        return self.agentes['idea_generator'].ejecutar(noticia, num_ideas=num_ideas)

    def optimizar_prompts(self, idea: Dict, num_prompts: int = 3) -> Dict:
        """Generar prompts creativos con Ollama (SIN COSTO)"""
        return self.agentes['prompt_engineer'].ejecutar(idea, num_prompts=num_prompts)

    def compilar_video(
        self,
        imagen_path: str,
        guion: str,
        audio_path: Optional[str] = None,
        formato: str = 'tiktok'
    ) -> Dict:
        """Compilar un video"""
        return self.agentes['video_compiler'].ejecutar(
            imagen_path=imagen_path,
            guion=guion,
            audio_path=audio_path,
            formato=formato
        )

    def generar_captions(self, idea: Dict, num_captions: int = 3) -> Dict:
        """Generar captions para una idea"""
        return self.agentes['caption_writer'].ejecutar(idea, num_captions=num_captions)

    def analizar_feedback(self, feedback_dict: Dict) -> Dict:
        """Analizar feedback y actualizar preferencias"""
        return self.agentes['feedback_analyzer'].ejecutar(feedback_dict)

    def validar_contenido(self, content_dict: Dict) -> Dict:
        """Validar contenido antes de publicar"""
        return self.agentes['content_validator'].ejecutar(content_dict)

    def generar_analytics(self, periodo: str = 'semanal') -> Dict:
        """Generar reporte de analytics"""
        return self.agentes['analytics'].ejecutar(periodo=periodo)

    def sincronizar_drive(self, archivos_config: Dict) -> Dict:
        """Sincronizar archivos con Google Drive"""
        return self.agentes['drive_sync'].ejecutar(archivos_config)

    def obtener_estado_agentes(self) -> Dict:
        """Obtener estado de todos los agentes"""
        return {
            'total_agentes': len(self.agentes),
            'agentes': list(self.agentes.keys()),
            'timestamp': __import__('datetime').datetime.now().isoformat(),
        }

    def listar_comandos_disponibles(self) -> Dict:
        """Listar todos los comandos disponibles"""
        return {
            'batch': {
                'comando': 'orquestador.ejecutar_batch_completo()',
                'descripcion': 'Ejecutar pipeline completo (batch)',
            },
            'scraping': {
                'comando': 'orquestador.scrappear_noticias(dias_atras=7)',
                'descripcion': 'Scrappear noticias de últimos 7 días',
            },
            'ideas': {
                'comando': 'orquestador.generar_ideas(noticia, num_ideas=3)',
                'descripcion': 'Generar 3 ideas para una noticia',
            },
            'prompts': {
                'comando': 'orquestador.optimizar_prompts(idea, num_prompts=3)',
                'descripcion': 'Optimizar prompts para Gemini',
            },
            'videos': {
                'comando': 'orquestador.compilar_video(imagen_path, guion)',
                'descripcion': 'Compilar video con FFmpeg',
            },
            'captions': {
                'comando': 'orquestador.generar_captions(idea, num_captions=3)',
                'descripcion': 'Generar captions para una idea',
            },
            'feedback': {
                'comando': 'orquestador.analizar_feedback(feedback_dict)',
                'descripcion': 'Analizar feedback y actualizar preferencias',
            },
            'validacion': {
                'comando': 'orquestador.validar_contenido(content_dict)',
                'descripcion': 'Validar contenido antes de publicar',
            },
            'analytics': {
                'comando': 'orquestador.generar_analytics(periodo="semanal")',
                'descripcion': 'Generar reporte de analytics',
            },
            'sync': {
                'comando': 'orquestador.sincronizar_drive(archivos_config)',
                'descripcion': 'Sincronizar con Google Drive',
            },
        }


def main():
    """Script de demostración del orquestador"""
    print("\n" + "="*70)
    print("  AJAMSI - AGENT ORCHESTRATOR v1.0")
    print("  Sistema de Generación Automática de Contenido TikTok")
    print("="*70 + "\n")

    # Inicializar orquestador
    orquestador = AgentOrchestrator()

    # Mostrar estado
    print(f"✅ {orquestador.obtener_estado_agentes()['total_agentes']} agentes inicializados:")
    for agente in orquestador.agentes.keys():
        print(f"   • {agente}")

    print("\n" + "="*70)
    print("COMANDOS DISPONIBLES:")
    print("="*70 + "\n")

    comandos = orquestador.listar_comandos_disponibles()
    for key, cmd in comandos.items():
        print(f"→ {key.upper()}")
        print(f"  Comando: {cmd['comando']}")
        print(f"  Descripción: {cmd['descripcion']}\n")

    print("="*70)
    print("Para ejecutar un batch completo, usa:")
    print("  >>> orquestador.ejecutar_batch_completo()")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
