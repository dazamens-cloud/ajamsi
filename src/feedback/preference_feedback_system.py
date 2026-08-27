"""
Preference Feedback System - Sistema de feedback con preferences.json
"""

from typing import Dict, List, Optional
import json
import logging
from pathlib import Path
from datetime import datetime

from .base_feedback_system import BaseFeedbackSystem, TipoFeedback, RegistroFeedback, Preferencia

logger = logging.getLogger(__name__)


class PreferenceFeedbackSystem(BaseFeedbackSystem):
    """
    Sistema de feedback que guarda preferencias en JSON

    Aprende de feedback del usuario y guarda patrones exitosos en preferences.json
    """

    def __init__(self, config: dict):
        """
        Inicializar sistema de feedback con preferencias

        Args:
            config: Configuración del proyecto
        """
        super().__init__(config)

        self.archivo_prefs = Path(self.archivo_preferencias)
        self.archivo_prefs.parent.mkdir(parents=True, exist_ok=True)

        # Cargar o crear preferencias
        self.preferencias = self._cargar_preferencias()

        logger.info("✓ Sistema de feedback inicializado")

    def _registrar_impl(self, feedback: RegistroFeedback) -> bool:
        """
        Registrar feedback en archivo JSON

        Args:
            feedback: Registro de feedback

        Returns:
            True si exitoso
        """
        try:
            # Cargar histórico actual
            historial = self._cargar_historial()

            # Convertir feedback a diccionario
            registro = {
                "tipo": feedback.tipo.value,
                "idea_id": feedback.idea_id,
                "video_id": feedback.video_id,
                "tema": feedback.tema,
                "angulo_humor": feedback.angulo_humor,
                "elementos_locales": feedback.elementos_locales,
                "comentario": feedback.comentario,
                "fecha": datetime.now().isoformat()
            }

            historial.append(registro)

            # Guardar en archivo
            self._guardar_historial(historial)
            logger.debug(f"✓ Feedback registrado: {feedback.tipo.value}")

            return True

        except Exception as e:
            logger.error(f"Error registrando feedback: {e}")
            return False

    def _actualizar_preferencia(self, categoria: str, clave: str, score: float):
        """
        Actualizar preferencia específica

        Args:
            categoria: Categoría (temas, angulos, elementos)
            clave: Clave de preferencia
            score: Score (0-1)
        """
        try:
            if categoria not in self.preferencias:
                self.preferencias[categoria] = {}

            if clave not in self.preferencias[categoria]:
                self.preferencias[categoria][clave] = {
                    "frecuencia": 0,
                    "score_total": 0.0,
                    "score_promedio": 0.0
                }

            pref = self.preferencias[categoria][clave]
            pref["frecuencia"] += 1
            pref["score_total"] += score
            pref["score_promedio"] = pref["score_total"] / pref["frecuencia"]

            # Guardar inmediatamente
            self._guardar_preferencias()

            logger.debug(f"Actualizada: {categoria}.{clave} = {pref['score_promedio']:.2f}")

        except Exception as e:
            logger.error(f"Error actualizando preferencia: {e}")

    def _obtener_preferencias_impl(self) -> Dict[str, List[Preferencia]]:
        """
        Obtener preferencias desde archivo

        Returns:
            Diccionario de preferencias
        """
        try:
            resultado = {}

            for categoria, items in self.preferencias.items():
                resultado[categoria] = []

                for clave, stats in items.items():
                    pref = Preferencia(
                        clave=clave,
                        valor=clave,
                        frecuencia=stats.get("frecuencia", 1),
                        score_promedio=stats.get("score_promedio", 0.0),
                        fecha_actualizado=""
                    )
                    resultado[categoria].append(pref)

                # Ordenar por score descendente
                resultado[categoria].sort(key=lambda p: p.score_promedio, reverse=True)

            return resultado

        except Exception as e:
            logger.error(f"Error obteniendo preferencias: {e}")
            return {}

    def _obtener_estadisticas_impl(self) -> Dict:
        """
        Obtener estadísticas de feedback

        Returns:
            Diccionario con estadísticas
        """
        try:
            historial = self._cargar_historial()

            stats = {
                "total_feedbacks": len(historial),
                "excelentes": sum(1 for f in historial if f["tipo"] == "✅"),
                "aceptables": sum(1 for f in historial if f["tipo"] == "🔶"),
                "malos": sum(1 for f in historial if f["tipo"] == "❌"),
                "temas_registrados": len(self.preferencias.get("temas", {})),
                "angulos_registrados": len(self.preferencias.get("angulos", {})),
                "elementos_registrados": len(self.preferencias.get("elementos", {}))
            }

            # Calcular porcentajes
            if stats["total_feedbacks"] > 0:
                stats["porcentaje_excelentes"] = (stats["excelentes"] / stats["total_feedbacks"]) * 100
                stats["porcentaje_aceptables"] = (stats["aceptables"] / stats["total_feedbacks"]) * 100
                stats["porcentaje_malos"] = (stats["malos"] / stats["total_feedbacks"]) * 100

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}

    def _cargar_preferencias(self) -> Dict:
        """
        Cargar preferencias desde archivo

        Returns:
            Diccionario de preferencias
        """
        try:
            if self.archivo_prefs.exists():
                with open(self.archivo_prefs, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    logger.debug(f"✓ Preferencias cargadas")
                    return datos

            else:
                logger.debug("Creando preferencias iniciales")
                return {
                    "temas": {},
                    "angulos": {},
                    "elementos": {},
                    "version": "1.0"
                }

        except Exception as e:
            logger.error(f"Error cargando preferencias: {e}")
            return {
                "temas": {},
                "angulos": {},
                "elementos": {},
                "version": "1.0"
            }

    def _guardar_preferencias(self):
        """Guardar preferencias en archivo"""
        try:
            with open(self.archivo_prefs, 'w', encoding='utf-8') as f:
                json.dump(self.preferencias, f, indent=2, ensure_ascii=False)
                logger.debug("✓ Preferencias guardadas")

        except Exception as e:
            logger.error(f"Error guardando preferencias: {e}")

    def _cargar_historial(self) -> List[Dict]:
        """
        Cargar historial de feedback

        Returns:
            Lista de registros
        """
        try:
            archivo_historial = Path(self.archivo_preferencias).parent / "feedback_historial.json"

            if archivo_historial.exists():
                with open(archivo_historial, 'r', encoding='utf-8') as f:
                    return json.load(f)

            return []

        except Exception as e:
            logger.error(f"Error cargando historial: {e}")
            return []

    def _guardar_historial(self, historial: List[Dict]):
        """
        Guardar historial de feedback

        Args:
            historial: Lista de registros
        """
        try:
            archivo_historial = Path(self.archivo_preferencias).parent / "feedback_historial.json"

            with open(archivo_historial, 'w', encoding='utf-8') as f:
                json.dump(historial, f, indent=2, ensure_ascii=False)
                logger.debug("✓ Historial guardado")

        except Exception as e:
            logger.error(f"Error guardando historial: {e}")

    def obtener_top_temas(self, limite: int = 5) -> List[Preferencia]:
        """
        Obtener temas con mejor score

        Args:
            limite: Número máximo de temas

        Returns:
            Lista de temas ordenados por score
        """
        prefs = self.obtener_preferencias()
        temas = prefs.get("temas", [])
        return temas[:limite]

    def obtener_top_angulos(self, limite: int = 5) -> List[Preferencia]:
        """
        Obtener ángulos con mejor score

        Args:
            limite: Número máximo de ángulos

        Returns:
            Lista de ángulos ordenados por score
        """
        prefs = self.obtener_preferencias()
        angulos = prefs.get("angulos", [])
        return angulos[:limite]

    def obtener_top_elementos(self, limite: int = 5) -> List[Preferencia]:
        """
        Obtener elementos con mejor score

        Args:
            limite: Número máximo de elementos

        Returns:
            Lista de elementos ordenados por score
        """
        prefs = self.obtener_preferencias()
        elementos = prefs.get("elementos", [])
        return elementos[:limite]

    def generar_reporte_feedback(self) -> str:
        """
        Generar reporte de feedback

        Returns:
            Texto con reporte
        """
        try:
            stats = self.obtener_estadisticas_feedback()
            prefs = self.obtener_preferencias()

            reporte = f"""
📊 REPORTE DE FEEDBACK Y PREFERENCIAS
{'='*50}

ESTADÍSTICAS GENERALES:
  Total feedbacks: {stats.get('total_feedbacks', 0)}
  ✅ Excelentes: {stats.get('excelentes', 0)} ({stats.get('porcentaje_excelentes', 0):.1f}%)
  🔶 Aceptables: {stats.get('aceptables', 0)} ({stats.get('porcentaje_aceptables', 0):.1f}%)
  ❌ Malos: {stats.get('malos', 0)} ({stats.get('porcentaje_malos', 0):.1f}%)

TOP TEMAS (mejor score):
"""
            for tema in self.obtener_top_temas(5):
                reporte += f"  • {tema.valor}: {tema.score_promedio:.2f} (×{tema.frecuencia})\n"

            reporte += "\nTOP ÁNGULOS (mejor score):\n"
            for angulo in self.obtener_top_angulos(5):
                reporte += f"  • {angulo.valor}: {angulo.score_promedio:.2f} (×{angulo.frecuencia})\n"

            reporte += "\nTOP ELEMENTOS (mejor score):\n"
            for elemento in self.obtener_top_elementos(5):
                reporte += f"  • {elemento.valor}: {elemento.score_promedio:.2f} (×{elemento.frecuencia})\n"

            return reporte

        except Exception as e:
            logger.error(f"Error generando reporte: {e}")
            return ""

    def __repr__(self) -> str:
        return f"<PreferenceFeedbackSystem: {self.archivo_preferencias}>"
