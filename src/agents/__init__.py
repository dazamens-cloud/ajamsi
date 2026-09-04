"""
Módulo de Agentes Especializados para AjamSi
Cada agente es responsable de una tarea específica en el pipeline
"""

from .scraper_agent import ScraperAgent
from .idea_generator_agent import IdeaGeneratorAgent
from .prompt_engineer_agent import PromptEngineerAgent
from .ollama_prompt_engineer_agent import OllamaPromptEngineerAgent
from .video_compiler_agent import VideoCompilerAgent
from .caption_writer_agent import CaptionWriterAgent
from .batch_processor_agent import BatchProcessorAgent
from .feedback_analyzer_agent import FeedbackAnalyzerAgent
from .content_validator_agent import ContentValidatorAgent
from .analytics_agent import AnalyticsAgent
from .drive_sync_agent import DriveSyncAgent

__all__ = [
    'ScraperAgent',
    'IdeaGeneratorAgent',
    'PromptEngineerAgent',
    'OllamaPromptEngineerAgent',  # NUEVO: Usa Ollama en lugar de Gemini
    'VideoCompilerAgent',
    'CaptionWriterAgent',
    'BatchProcessorAgent',
    'FeedbackAnalyzerAgent',
    'ContentValidatorAgent',
    'AnalyticsAgent',
    'DriveSyncAgent',
]
