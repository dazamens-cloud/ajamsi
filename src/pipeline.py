"""
Pipeline Principal - Orquestador del flujo completo
"""

from typing import List, Optional, Tuple
import logging
from pathlib import Path

from src.utils.config_loader import ConfigLoader
from src.utils.db import DatabaseManager
from src.scrapers import ScraperManager, Noticia
from src.generators import ClaudeIdeaGenerator, Idea
from src.processors import FFmpegVideoCompiler, Video
from src.sync import GoogleDriveSync

logger = logging.getLogger(__name__)


class AjamSiPipeline:
    """
    Pipeline principal que coordina todo el flujo de AjamSi

    Flujo:
    1. Scrape noticias de 9 fuentes
    2. Genera ideas creativas con Claude
    3. Compila videos con FFmpeg
    4. Guarda todo en SQLite
    """

    def __init__(self, config_path: str = "config/config.json"):
        """
        Inicializar pipeline

        Args:
            config_path: Ruta a config.json
        """
        self.config = ConfigLoader.cargar(config_path)
        self.db = DatabaseManager(self.config)
        self.scraper_manager = ScraperManager(self.config)
        self.generador_ideas = ClaudeIdeaGenerator(self.config)
        self.compilador_videos = FFmpegVideoCompiler(self.config)
        self.drive_sync = GoogleDriveSync(self.config)

        logger.info("✓ Pipeline AjamSi inicializado")

    def ejecutar_completo(self, num_ideas_por_noticia: int = 3,
                         compilar_videos: bool = True) -> dict:
        """
        Ejecutar pipeline completo

        Args:
            num_ideas_por_noticia: Cuántas ideas generar por noticia
            compilar_videos: Si compilar videos (requiere imágenes)

        Returns:
            Diccionario con resumen de ejecución
        """
        logger.info("=" * 60)
        logger.info("🚀 Iniciando pipeline completo de AjamSi")
        logger.info("=" * 60)

        resumen = {
            "noticias_scrapeadas": 0,
            "ideas_generadas": 0,
            "videos_compilados": 0,
            "errores": []
        }

        try:
            # ETAPA 1: Scraping
            logger.info("\n📰 ETAPA 1: Scraping de noticias")
            noticias = self._ejecutar_scraping()
            resumen["noticias_scrapeadas"] = len(noticias)

            if not noticias:
                logger.warning("⚠ No se scrapearon noticias")
                return resumen

            # ETAPA 2: Generación de Ideas
            logger.info("\n💡 ETAPA 2: Generación de ideas")
            ideas = self._generar_ideas(noticias, num_ideas_por_noticia)
            resumen["ideas_generadas"] = len(ideas)

            # ETAPA 3: Compilación de Videos
            if compilar_videos:
                logger.info("\n🎬 ETAPA 3: Compilación de videos")
                videos = self._compilar_videos(ideas)
                resumen["videos_compilados"] = len(videos)

            # ETAPA 4: Guardar en BD
            logger.info("\n💾 ETAPA 4: Guardando en base de datos")
            self._guardar_en_bd(noticias, ideas)

            logger.info("\n" + "=" * 60)
            logger.info("✅ Pipeline completado exitosamente")
            logger.info("=" * 60)

            return resumen

        except Exception as e:
            logger.error(f"Error en pipeline: {e}", exc_info=True)
            resumen["errores"].append(str(e))
            return resumen

    def _ejecutar_scraping(self) -> List[Noticia]:
        """
        Ejecutar scraping de todas las fuentes

        Returns:
            Lista de noticias scrapeadas
        """
        try:
            logger.info("Scrapeando 9 fuentes de noticias...")
            noticias = self.scraper_manager.scrapear_todas_fuentes(
                paralelo=True,
                max_noticias=50
            )

            logger.info(f"✓ Scrapeadas {len(noticias)} noticias")
            for noticia in noticias[:3]:
                logger.debug(f"  - {noticia.fuente}: {noticia.titulo[:50]}")

            return noticias

        except Exception as e:
            logger.error(f"Error en scraping: {e}", exc_info=True)
            return []

    def _generar_ideas(self, noticias: List[Noticia],
                      num_ideas: int) -> List[Idea]:
        """
        Generar ideas desde noticias

        Args:
            noticias: Noticias scrapeadas
            num_ideas: Cuántas ideas por noticia

        Returns:
            Lista de ideas generadas
        """
        try:
            ideas = []

            for noticia in noticias:
                logger.debug(f"Generando {num_ideas} ideas para: {noticia.titulo[:40]}")

                ideas_noticia = self.generador_ideas.generar_ideas(
                    noticia=noticia,
                    num_ideas=num_ideas
                )

                ideas.extend(ideas_noticia)

            logger.info(f"✓ Generadas {len(ideas)} ideas totales")
            return ideas

        except Exception as e:
            logger.error(f"Error generando ideas: {e}", exc_info=True)
            return []

    def _compilar_videos(self, ideas: List[Idea]) -> List[Video]:
        """
        Compilar videos desde ideas (requiere imágenes)

        Args:
            ideas: Ideas a compilar

        Returns:
            Lista de videos compilados
        """
        try:
            videos = []

            for idea in ideas[:5]:  # Limitar a primeras 5 para testing
                logger.debug(f"Compilando video: {idea.titulo[:40]}")

                # En versión real, aquí iría generación de imagen + compilación
                # Por ahora, fallback mode
                video = self.compilador_videos.compilar_video(
                    idea=idea,
                    ruta_imagen="imagenes/el_tipico_canario.png"
                )

                if video:
                    videos.append(video)

            logger.info(f"✓ Compilados {len(videos)} videos")
            return videos

        except Exception as e:
            logger.error(f"Error compilando videos: {e}", exc_info=True)
            return []

    def _guardar_en_bd(self, noticias: List[Noticia],
                       ideas: List[Idea]) -> bool:
        """
        Guardar noticias e ideas en base de datos

        Args:
            noticias: Noticias a guardar
            ideas: Ideas a guardar

        Returns:
            True si exitoso
        """
        try:
            logger.info(f"Guardando {len(noticias)} noticias...")
            for noticia in noticias:
                self.db.guardar_noticia(noticia)

            logger.info(f"✓ {len(noticias)} noticias guardadas")

            logger.info(f"Guardando {len(ideas)} ideas...")
            for idea in ideas:
                self.db.guardar_idea(idea)

            logger.info(f"✓ {len(ideas)} ideas guardadas")

            return True

        except Exception as e:
            logger.error(f"Error guardando en BD: {e}", exc_info=True)
            return False

    def obtener_estadisticas(self) -> dict:
        """
        Obtener estadísticas de la base de datos

        Returns:
            Diccionario con conteos de tabla
        """
        try:
            stats = {
                "noticias": self.db.contar_noticias(),
                "ideas": self.db.contar_ideas(),
                "videos": self.db.contar_videos(),
                "imagenes": self.db.contar_imagenes(),
            }

            logger.info("📊 Estadísticas de BD:")
            for tabla, count in stats.items():
                logger.info(f"  {tabla}: {count}")

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}

    def sincronizar_a_nube(self) -> dict:
        """
        Sincronizar archivos a Google Drive

        Returns:
            Diccionario con resumen de sincronización
        """
        try:
            logger.info("\n☁️  Sincronizando a Google Drive...")

            db_path = self.config.get("base_datos", {}).get("archivo", "data/ajamsi.db")
            imagenes_path = "imagenes"
            videos_path = "videos"

            resultado = self.drive_sync.sincronizar_todo(
                ruta_bd=db_path,
                ruta_imagenes=imagenes_path,
                ruta_videos=videos_path
            )

            resumen = {
                "exitoso": resultado.exitoso,
                "archivos_sincronizados": resultado.archivos_sincronizados,
                "archivos_fallo": resultado.archivos_fallo,
                "tamaño_bytes": resultado.tamaño_bytes,
                "mensaje": resultado.mensaje,
                "detalles": resultado.detalles
            }

            if resultado.exitoso:
                logger.info(f"✓ Sincronización completada: {resultado.archivos_sincronizados} archivos")
            else:
                logger.warning(f"⚠ Sincronización con errores")

            return resumen

        except Exception as e:
            logger.error(f"Error sincronizando: {e}", exc_info=True)
            return {"exitoso": False, "mensaje": str(e)}

    def __repr__(self) -> str:
        return "<AjamSiPipeline: Scraper + Generator + Compiler + DB>"
