"""
FEEDBACK ANALYZER AGENT
Responsabilidad: Analizar feedback y actualizar preferences.json
"""

import logging
from typing import Dict, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class FeedbackAnalyzerAgent:
    """
    Agente especializado en análisis de feedback y aprendizaje.

    Responsabilidades:
    - Recibe feedback del usuario (✅/🔶/❌)
    - Actualiza preferences.json
    - Identifica patrones
    - Sugiere mejoras futuras
    """

    TIPOS_FEEDBACK = {
        '✅': 'positivo',
        '🔶': 'neutral',
        '❌': 'negativo',
    }

    def __init__(self, config: Dict):
        """
        Inicializar el agente feedback analyzer.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("✓ FeedbackAnalyzerAgent inicializado")

    def ejecutar(self, feedback_dict: Dict) -> Dict:
        """
        Analizar feedback y actualizar preferencias.

        Args:
            feedback_dict: Dict con feedback del usuario
                Ej: {'videos': {1: '✅', 4: '✅', 7: '❌', ...}}

        Returns:
            Dict con análisis y recomendaciones
        """
        self.logger.info("📊 Analizando feedback...")

        try:
            analisis = {
                'fecha': datetime.now().isoformat(),
                'feedback_procesado': feedback_dict,
                'estadisticas': self._calcular_estadisticas(feedback_dict),
                'patrones_identificados': self._identificar_patrones(feedback_dict),
                'recomendaciones': self._generar_recomendaciones(feedback_dict),
                'actualizaciones_preferences': self._generar_actualizaciones(feedback_dict),
            }

            # TODO: Guardar en preferences.json
            self._actualizar_preferences_file(analisis)

            resultado = {
                'status': 'success',
                'analisis': analisis,
                'videos_positivos': len([f for f in feedback_dict.values() if f == '✅']),
                'videos_negativos': len([f for f in feedback_dict.values() if f == '❌']),
                'tasa_exito': self._calcular_tasa_exito(feedback_dict),
            }

            self.logger.info(f"✅ Análisis completado")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error analizando feedback: {e}")
            return {
                'status': 'error',
                'error': str(e),
            }

    def _calcular_estadisticas(self, feedback_dict: Dict) -> Dict:
        """Calcular estadísticas del feedback"""
        total = len(feedback_dict)
        positivos = len([f for f in feedback_dict.values() if f == '✅'])
        neutrales = len([f for f in feedback_dict.values() if f == '🔶'])
        negativos = len([f for f in feedback_dict.values() if f == '❌'])

        return {
            'total_videos': total,
            'positivos': positivos,
            'neutrales': neutrales,
            'negativos': negativos,
            'porcentaje_exito': (positivos / total * 100) if total > 0 else 0,
        }

    def _identificar_patrones(self, feedback_dict: Dict) -> List[str]:
        """Identificar patrones en el feedback"""
        patrones = []

        stats = self._calcular_estadisticas(feedback_dict)

        if stats['porcentaje_exito'] > 70:
            patrones.append("Alta tasa de éxito (>70%) - sistema funcionando bien")
        elif stats['porcentaje_exito'] < 30:
            patrones.append("Baja tasa de éxito (<30%) - requiere ajustes")

        if stats['positivos'] > stats['negativos']:
            patrones.append("Tendencia positiva en último batch")

        return patrones

    def _generar_recomendaciones(self, feedback_dict: Dict) -> List[str]:
        """Generar recomendaciones basadas en feedback"""
        recomendaciones = []

        stats = self._calcular_estadisticas(feedback_dict)

        if stats['porcentaje_exito'] < 50:
            recomendaciones.append("Aumentar variedad en ángulos humorísticos")
            recomendaciones.append("Revisar relevancia de temas seleccionados")

        recomendaciones.append("Continuar con el estilo de videos positivos")

        return recomendaciones

    def _generar_actualizaciones(self, feedback_dict: Dict) -> Dict:
        """Generar actualizaciones para preferences.json"""
        stats = self._calcular_estadisticas(feedback_dict)

        return {
            'ultima_tasa_exito': stats['porcentaje_exito'],
            'videos_totales_procesados': stats['total_videos'],
            'tendencia': 'positiva' if stats['positivos'] > stats['negativos'] else 'negativa',
            'fecha_ultimo_feedback': datetime.now().isoformat(),
        }

    def _actualizar_preferences_file(self, analisis: Dict):
        """Guardar análisis en preferences.json"""
        # TODO: Implementar actualización real de preferences.json
        self.logger.info("💾 Actualizando preferences.json (mock)")
