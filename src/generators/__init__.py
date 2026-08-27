"""
Módulo de generadores para AjamSi

Genera ideas creativas de memes desde noticias scrapeadas
"""

from .base_idea_generator import BaseIdeaGenerator, Idea
from .claude_idea_generator import ClaudeIdeaGenerator
from .ollama_idea_generator import OllamaIdeaGenerator

__all__ = [
    'BaseIdeaGenerator',
    'Idea',
    'ClaudeIdeaGenerator',
    'OllamaIdeaGenerator'
]
