"""
CONTENT VALIDATOR AGENT
Responsabilidad: Validación de contenido antes de publicar
"""

import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentValidatorAgent:
    """
    Agente especializado en QA/Validación de contenido.

    Responsabilidades:
    - Revisa antes de publicar
    - Busca errores de ortografía
    - Verifica duración de video
    - Comprueba que imagen + caption + video casan
    - Alerta si hay problemas legales/sensibles
    """

    PALABRAS_PROHIBIDAS = ['violencia', 'delito', 'ilegal']
    DURACION_MIN = 10  # segundos
    DURACION_MAX = 60  # segundos

    def __init__(self, config: Dict):
        """
        Inicializar el agente validador.

        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("✓ ContentValidatorAgent inicializado")

    def ejecutar(self, content_dict: Dict) -> Dict:
        """
        Validar contenido antes de publicar.

        Args:
            content_dict: Dict con contenido a validar

        Returns:
            Dict con resultado de validación
        """
        self.logger.info("✔️  Validando contenido...")

        try:
            validaciones = {
                'ortografia': self._validar_ortografia(content_dict),
                'duracion': self._validar_duracion(content_dict),
                'coherencia': self._validar_coherencia(content_dict),
                'contenido_sensible': self._validar_contenido_sensible(content_dict),
                'calidad_imagen': self._validar_calidad_imagen(content_dict),
            }

            # Determinar si todo está OK
            todo_ok = all(v.get('ok', True) for v in validaciones.values())

            alertas = [v.get('alerta') for v in validaciones.values() if v.get('alerta')]
            alertas = [a for a in alertas if a]  # Remover None

            resultado = {
                'status': 'success',
                'todo_ok': todo_ok,
                'validaciones': validaciones,
                'alertas': alertas,
                'puntuacion_calidad': self._calcular_puntuacion(validaciones),
                'recomendacion': 'LISTO PARA PUBLICAR' if todo_ok else 'REVISAR ANTES DE PUBLICAR',
                'timestamp': datetime.now().isoformat(),
            }

            if todo_ok:
                self.logger.info("✅ Validación OK - Contenido listo para publicar")
            else:
                self.logger.warning(f"⚠️  Validación: {len(alertas)} alertas encontradas")

            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error validando: {e}")
            return {
                'status': 'error',
                'error': str(e),
            }

    def _validar_ortografia(self, content_dict: Dict) -> Dict:
        """Validar ortografía en captions"""
        caption = content_dict.get('caption', '')

        # TODO: Integrar con biblioteca de ortografía real
        # Por ahora, mock validation
        errores_encontrados = 0

        return {
            'ok': errores_encontrados == 0,
            'errores': errores_encontrados,
            'alerta': f"⚠️  {errores_encontrados} errores de ortografía" if errores_encontrados > 0 else None,
        }

    def _validar_duracion(self, content_dict: Dict) -> Dict:
        """Validar duración de video"""
        duracion = content_dict.get('duracion_segundos', 30)

        ok = self.DURACION_MIN <= duracion <= self.DURACION_MAX
        alerta = None

        if duracion < self.DURACION_MIN:
            alerta = f"⚠️  Video muy corto ({duracion}s, mínimo {self.DURACION_MIN}s)"
        elif duracion > self.DURACION_MAX:
            alerta = f"⚠️  Video muy largo ({duracion}s, máximo {self.DURACION_MAX}s)"

        return {
            'ok': ok,
            'duracion': duracion,
            'alerta': alerta,
        }

    def _validar_coherencia(self, content_dict: Dict) -> Dict:
        """Validar coherencia entre imagen, caption y video"""
        # TODO: Implementar validación real con IA
        # Por ahora, mock validation
        ok = True
        alerta = None

        return {
            'ok': ok,
            'alerta': alerta,
        }

    def _validar_contenido_sensible(self, content_dict: Dict) -> Dict:
        """Validar que no tenga contenido sensible/prohibido"""
        texto_completo = (
            content_dict.get('caption', '') + ' ' +
            content_dict.get('concepto', '')
        ).lower()

        palabras_encontradas = [p for p in self.PALABRAS_PROHIBIDAS if p in texto_completo]

        ok = len(palabras_encontradas) == 0
        alerta = f"⚠️  Palabras sensibles encontradas: {palabras_encontradas}" if palabras_encontradas else None

        return {
            'ok': ok,
            'palabras_sensibles': palabras_encontradas,
            'alerta': alerta,
        }

    def _validar_calidad_imagen(self, content_dict: Dict) -> Dict:
        """Validar calidad de imagen"""
        # TODO: Integrar con análisis de imagen real
        ok = True
        alerta = None

        return {
            'ok': ok,
            'alerta': alerta,
        }

    def _calcular_puntuacion(self, validaciones: Dict) -> float:
        """Calcular puntuación de calidad (0-100)"""
        puntuacion = 100.0

        for validacion in validaciones.values():
            if not validacion.get('ok', True):
                puntuacion -= 10

        return max(puntuacion, 0)
