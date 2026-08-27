"""
Módulo de feedback para AjamSi

Registra feedback del usuario y aprende patrones para mejorar
"""

from .base_feedback_system import BaseFeedbackSystem, TipoFeedback, RegistroFeedback, Preferencia
from .preference_feedback_system import PreferenceFeedbackSystem

__all__ = [
    'BaseFeedbackSystem',
    'TipoFeedback',
    'RegistroFeedback',
    'Preferencia',
    'PreferenceFeedbackSystem'
]
