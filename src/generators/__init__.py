"""
Módulo de generadores para AjamSi

Genera ideas creativas de memes desde noticias scrapeadas
"""

from .base_idea_generator import BaseIdeaGenerator, Idea
from .claude_idea_generator import ClaudeIdeaGenerator

__all__ = [
    'BaseIdeaGenerator',
    'Idea',
    'ClaudeIdeaGenerator'
]
