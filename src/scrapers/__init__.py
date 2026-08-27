"""
Módulo de scraping para AjamSi

Scrapers para extraer noticias de múltiples fuentes
"""

from .base_scraper import BaseScraper, Noticia
from .lancelot_digital import LancelotDigitalScraper
from .cronicas_lanzarote import CronicasLanzaroteScraper
from .noticias_lanzarote import NoticiasLanzaroteScraper
from .diario_lanzarote import DiarioLanzaroteScraper
from .periodico_lanzarote import PeriodoLanzaroteScraper
from .scraper_manager import ScraperManager

__all__ = [
    'BaseScraper',
    'Noticia',
    'LancelotDigitalScraper',
    'CronicasLanzaroteScraper',
    'NoticiasLanzaroteScraper',
    'DiarioLanzaroteScraper',
    'PeriodoLanzaroteScraper',
    'ScraperManager'
]
