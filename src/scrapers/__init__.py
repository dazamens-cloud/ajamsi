"""
Módulo de scraping para AjamSi

Scrapers para extraer noticias de múltiples fuentes
"""

from .base_scraper import BaseScraper, Noticia
from .lancelot_digital import LancelotDigitalScraper
from .scraper_manager import ScraperManager

__all__ = [
    'BaseScraper',
    'Noticia',
    'LancelotDigitalScraper',
    'ScraperManager'
]
