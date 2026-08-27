"""
Base Feedback System - Clase abstracta para sistemas de feedback
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TipoFeedback(Enum):
    """Tipos de feedback posibles"""
    EXCELENTE = "✅"  # Muy bueno, repetir patrón
    ACEPTABLE = "🔶"  # Funciona pero mejorable
    MALO = "❌"       # No funcionó, evitar


@dataclass
class Preferencia:
    """Preferencia aprendida del feedback"""
    clave: str
    valor: str
    frecuencia: int = 1
    score_promedio: float = 0.0
    fecha_actualizado: str = ""

    def __repr__(self) -> str:
        return f"<Preferencia: {self.clave}={self.valor} (score: {self.score_promedio:.2f})>"


@dataclass
class RegistroFeedback:
    """Registro de un feedback dado por usuario"""
    tipo: TipoFeedback
    idea_id: Optional[str] = None
    video_id: Optional[str] = None
    tema: Optional[str] = None
    angulo_humor: Optional[str] = None
    elementos_locales: List[str] = field(default_factory=list)
    comentario: Optional[str] = None
    fecha: str = ""

    def __repr__(self) -> str:
        return f"<Feedback: {self.tipo.value} - {self.tema}>"


class BaseFeedbackSystem(ABC):
    """
    Clase base para sistemas de feedback

    Registra feedback del usuario y aprende patrones para mejorar generación
    """

    def __init__(self, config: dict):
        """
        Inicializar sistema de feedback

        Args:
            config: Configuración del proyecto
        """
        self.config = config
        self.feedback_config = config.get("aprendizaje", {})
        self.actualizar_cada_feedback = self.feedback_config.get("actualizar_cada_feedback", True)
        self.archivo_preferencias = self.feedback_config.get("archivo_preferencias", "data/preferences.json")

        logger.info(f"Inicializado sistema de feedback: {self.__class__.__name__}")
        logger.info(f"  Actualizar: {self.actualizar_cada_feedback}")
        logger.info(f"  Preferencias: {self.archivo_preferencias}")

    def registrar_feedback(self, tipo: TipoFeedback, idea_id: Optional[str] = None,
                          video_id: Optional[str] = None, tema: Optional[str] = None,
                          angulo: Optional[str] = None, elementos: Optional[List[str]] = None,
                          comentario: Optional[str] = None) -> bool:
        """
        Registrar feedback del usuario

        Args:
            tipo: TipoFeedback (EXCELENTE, ACEPTABLE, MALO)
            idea_id: ID de idea (opcional)
            video_id: ID de video (opcional)
            tema: Tema de noticia (opcional)
            angulo: Ángulo humorístico (opcional)
            elementos: Elementos locales usados (opcional)
            comentario: Comentario adicional (opcional)

        Returns:
            True si se registró exitosamente
        """
        try:
            logger.info(f"Registrando feedback: {tipo.value}")

            feedback = RegistroFeedback(
                tipo=tipo,
                idea_id=idea_id,
                video_id=video_id,
                tema=tema,
                angulo_humor=angulo,
                elementos_locales=elementos or [],
                comentario=comentario
            )

            # Guardar en BD/archivo (implementación específica)
            exito = self._registrar_impl(feedback)

            if exito and self.actualizar_cada_feedback:
                # Actualizar preferencias inmediatamente
                self._actualizar_preferencias(feedback)

            return exito

        except Exception as e:
            logger.error(f"Error registrando feedback: {e}", exc_info=True)
            return False

    @abstractmethod
    def _registrar_impl(self, feedback: RegistroFeedback) -> bool:
        """
        Implementación específica de registro de feedback

        Args:
            feedback: Registro de feedback

        Returns:
            True si exitoso
        """
        pass

    def obtener_preferencias(self) -> Dict[str, List[Preferencia]]:
        """
        Obtener preferencias aprendidas

        Returns:
            Diccionario de preferencias por categoría
        """
        try:
            logger.debug("Obteniendo preferencias...")
            return self._obtener_preferencias_impl()

        except Exception as e:
            logger.error(f"Error obteniendo preferencias: {e}")
            return {}

    @abstractmethod
    def _obtener_preferencias_impl(self) -> Dict[str, List[Preferencia]]:
        """
        Implementación específica de obtención de preferencias

        Returns:
            Diccionario de preferencias
        """
        pass

    def _actualizar_preferencias(self, feedback: RegistroFeedback):
        """
        Actualizar preferencias basado en feedback

        Args:
            feedback: Registro de feedback
        """
        try:
            logger.debug(f"Actualizando preferencias desde feedback...")

            # Calcular score del feedback
            score = self._calcular_score_feedback(feedback.tipo)

            # Actualizar temas
            if feedback.tema:
                self._actualizar_preferencia("temas", feedback.tema, score)

            # Actualizar ángulos
            if feedback.angulo_humor:
                self._actualizar_preferencia("angulos", feedback.angulo_humor, score)

            # Actualizar elementos
            for elemento in feedback.elementos_locales:
                self._actualizar_preferencia("elementos", elemento, score)

            logger.info(f"✓ Preferencias actualizadas")

        except Exception as e:
            logger.error(f"Error actualizando preferencias: {e}")

    @abstractmethod
    def _actualizar_preferencia(self, categoria: str, clave: str, score: float):
        """
        Actualizar una preferencia específica

        Args:
            categoria: Categoría (temas, angulos, elementos)
            clave: Clave de preferencia
            score: Score del feedback
        """
        pass

    def _calcular_score_feedback(self, tipo: TipoFeedback) -> float:
        """
        Calcular score numérico para feedback

        Args:
            tipo: TipoFeedback

        Returns:
            Score (0-1)
        """
        if tipo == TipoFeedback.EXCELENTE:
            return 1.0
        elif tipo == TipoFeedback.ACEPTABLE:
            return 0.5
        else:  # MALO
            return 0.0

    def obtener_tema_recomendado(self) -> Optional[str]:
        """
        Obtener tema recomendado basado en preferencias

        Returns:
            Tema con mejor score o None
        """
        try:
            prefs = self.obtener_preferencias()
            temas = prefs.get("temas", [])

            if not temas:
                return None

            # Retornar tema con mejor score
            mejor_tema = max(temas, key=lambda t: t.score_promedio)
            logger.debug(f"Tema recomendado: {mejor_tema.valor} (score: {mejor_tema.score_promedio:.2f})")
            return mejor_tema.valor

        except Exception as e:
            logger.error(f"Error obteniendo tema recomendado: {e}")
            return None

    def obtener_angulo_recomendado(self) -> Optional[str]:
        """
        Obtener ángulo humorístico recomendado

        Returns:
            Ángulo con mejor score o None
        """
        try:
            prefs = self.obtener_preferencias()
            angulos = prefs.get("angulos", [])

            if not angulos:
                return None

            mejor_angulo = max(angulos, key=lambda a: a.score_promedio)
            logger.debug(f"Ángulo recomendado: {mejor_angulo.valor} (score: {mejor_angulo.score_promedio:.2f})")
            return mejor_angulo.valor

        except Exception as e:
            logger.error(f"Error obteniendo ángulo recomendado: {e}")
            return None

    def obtener_estadisticas_feedback(self) -> Dict:
        """
        Obtener estadísticas de feedback

        Returns:
            Diccionario con estadísticas
        """
        try:
            stats = self._obtener_estadisticas_impl()

            logger.info("📊 Estadísticas de Feedback:")
            for clave, valor in stats.items():
                logger.info(f"  {clave}: {valor}")

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}

    @abstractmethod
    def _obtener_estadisticas_impl(self) -> Dict:
        """
        Implementación específica de estadísticas

        Returns:
            Diccionario con estadísticas
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.archivo_preferencias}>"
