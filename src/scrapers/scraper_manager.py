"""
ScraperManager - Orquestador de todos los scrapers
"""

from typing import List, Dict
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base_scraper import Noticia
from .lancelot_digital import LancelotDigitalScraper
from .cronicas_lanzarote import CronicasLanzaroteScraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """
    Gestor centralizado de scrapers

    Coordina múltiples scrapers y agrega resultados
    """

    def __init__(self, config: dict):
        """
        Inicializar manager

        Args:
            config: Configuración del proyecto (config.json)
        """
        self.config = config
        self.scraper_config = config.get("scrapers", {})
        self.timeout = self.scraper_config.get("timeout", 10)
        self.user_agent = self.scraper_config.get("user_agent")

        # Mapeo de scrapers (nombre_fuente -> clase_scraper)
        self.scrapers_disponibles = {
            "Lancelot Digital": LancelotDigitalScraper,
            "Crónicas de Lanzarote": CronicasLanzaroteScraper,
            # Aquí irán más scrapers conforme los creemos
        }

        # Instancias de scrapers
        self.scrapers = self._inicializar_scrapers()

        logger.info(f"ScraperManager inicializado con {len(self.scrapers)} scraper(s)")

    def _inicializar_scrapers(self) -> Dict[str, object]:
        """
        Inicializar instancias de scrapers según configuración

        Returns:
            Dict de scrapers por nombre
        """
        scrapers = {}
        fuentes = self.scraper_config.get("fuentes", [])

        for fuente in fuentes:
            nombre = fuente.get("nombre")
            activo = fuente.get("activo", True)

            if not nombre or not activo:
                continue

            # Buscar clase del scraper
            clase_scraper = self.scrapers_disponibles.get(nombre)

            if not clase_scraper:
                logger.warning(f"No hay scraper disponible para: {nombre}")
                continue

            try:
                # Crear instancia con config
                scraper = clase_scraper(fuente, timeout=self.timeout)
                scrapers[nombre] = scraper
                logger.info(f"✓ Scraper inicializado: {nombre}")

            except Exception as e:
                logger.error(f"Error inicializando scraper {nombre}: {e}")
                continue

        return scrapers

    def scrapear_todas_fuentes(self, dias_atras: int = 7, paralelo: bool = True) -> List[Noticia]:
        """
        Scrapear todas las fuentes activas

        Args:
            dias_atras: Número de días hacia atrás
            paralelo: Si ejecutar en paralelo (más rápido pero más recursos)

        Returns:
            Lista agregada de todas las noticias
        """
        if not self.scrapers:
            logger.error("No hay scrapers disponibles")
            return []

        if paralelo:
            return self._scrapear_paralelo(dias_atras)
        else:
            return self._scrapear_secuencial(dias_atras)

    def _scrapear_secuencial(self, dias_atras: int) -> List[Noticia]:
        """
        Scrapear fuentes de forma secuencial

        Args:
            dias_atras: Número de días hacia atrás

        Returns:
            Lista agregada de noticias
        """
        logger.info(f"Iniciando scraping secuencial de {len(self.scrapers)} fuente(s)")

        todas_noticias = []

        for nombre, scraper in self.scrapers.items():
            try:
                noticias = scraper.scrape(dias_atras)
                todas_noticias.extend(noticias)
                logger.info(f"[{nombre}] ✓ {len(noticias)} noticias agregadas")

            except Exception as e:
                logger.error(f"[{nombre}] Error durante scraping: {e}")
                continue

        # Ordenar por fecha (más recientes primero)
        todas_noticias.sort(key=lambda n: n.fecha_publicacion or datetime.now(), reverse=True)

        logger.info(f"✓ Scraping completado: {len(todas_noticias)} noticias totales")
        return todas_noticias

    def _scrapear_paralelo(self, dias_atras: int) -> List[Noticia]:
        """
        Scrapear fuentes en paralelo

        Args:
            dias_atras: Número de días hacia atrás

        Returns:
            Lista agregada de noticias
        """
        logger.info(f"Iniciando scraping paralelo de {len(self.scrapers)} fuente(s)")

        todas_noticias = []

        # Usar ThreadPoolExecutor para paralelismo
        max_workers = min(len(self.scrapers), 5)  # Máximo 5 threads

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._scraper_wrapper, nombre, scraper, dias_atras): nombre
                for nombre, scraper in self.scrapers.items()
            }

            # Procesar resultados conforme completen
            for future in as_completed(futures):
                nombre = futures[future]
                try:
                    noticias = future.result()
                    todas_noticias.extend(noticias)
                    logger.info(f"[{nombre}] ✓ {len(noticias)} noticias agregadas")

                except Exception as e:
                    logger.error(f"[{nombre}] Error en thread: {e}")
                    continue

        # Ordenar por fecha
        todas_noticias.sort(key=lambda n: n.fecha_publicacion or datetime.now(), reverse=True)

        logger.info(f"✓ Scraping paralelo completado: {len(todas_noticias)} noticias totales")
        return todas_noticias

    @staticmethod
    def _scraper_wrapper(nombre: str, scraper: object, dias_atras: int) -> List[Noticia]:
        """
        Wrapper para ejecutar scraper en thread

        Args:
            nombre: Nombre del scraper
            scraper: Instancia del scraper
            dias_atras: Número de días

        Returns:
            Noticias del scraper
        """
        return scraper.scrape(dias_atras)

    def scrapear_fuente_especifica(self, nombre_fuente: str, dias_atras: int = 7) -> List[Noticia]:
        """
        Scrapear una fuente específica

        Args:
            nombre_fuente: Nombre de la fuente
            dias_atras: Número de días hacia atrás

        Returns:
            Noticias de esa fuente
        """
        if nombre_fuente not in self.scrapers:
            logger.error(f"Fuente no disponible: {nombre_fuente}")
            return []

        scraper = self.scrapers[nombre_fuente]

        try:
            noticias = scraper.scrape(dias_atras)
            logger.info(f"[{nombre_fuente}] Scrapeadas {len(noticias)} noticias")
            return noticias

        except Exception as e:
            logger.error(f"[{nombre_fuente}] Error: {e}")
            return []

    def listar_fuentes_disponibles(self) -> List[str]:
        """
        Listar fuentes de scraping disponibles

        Returns:
            Lista de nombres de fuentes
        """
        return list(self.scrapers.keys())

    def obtener_estadisticas(self) -> dict:
        """
        Obtener estadísticas de scrapers

        Returns:
            Dict con información de cada scraper
        """
        stats = {
            "total_scrapers": len(self.scrapers),
            "fuentes": list(self.scrapers.keys())
        }

        return stats
