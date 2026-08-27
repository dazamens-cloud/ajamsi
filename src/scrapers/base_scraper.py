"""
Base Scraper - Clase abstracta para todos los scrapers de noticias
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


@dataclass
class Noticia:
    """Estructura de datos para una noticia"""
    titulo: str
    url: str
    fuente: str
    contenido: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    relevancia_score: float = 0.0

    def __repr__(self) -> str:
        fecha = self.fecha_publicacion.strftime("%Y-%m-%d") if self.fecha_publicacion else "N/A"
        return f"<Noticia: {self.titulo[:50]}... ({fecha})>"


class BaseScraper(ABC):
    """
    Clase base para scrapers de noticias

    Define la interfaz común y proporciona utilidades compartidas
    """

    def __init__(self, config: dict, timeout: int = 10):
        """
        Inicializar base scraper

        Args:
            config: Dict con configuración (nombre, url, etc.)
            timeout: Timeout para requests en segundos
        """
        self.nombre = config.get("nombre", "Unknown")
        self.url_base = config.get("url", "")
        self.prioridad = config.get("prioridad", 2)
        self.timeout = timeout
        self.user_agent = config.get("user_agent", self._get_default_user_agent())

        # Setup requests con retry logic
        self.session = self._create_session_with_retries()

        logger.info(f"Inicializado scraper: {self.nombre}")

    def _create_session_with_retries(self) -> requests.Session:
        """Crear session con retry logic para manejo de errores"""
        session = requests.Session()

        # Configurar retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # User agent
        session.headers.update({"User-Agent": self.user_agent})

        return session

    @staticmethod
    def _get_default_user_agent() -> str:
        """User agent por defecto"""
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def scrape(self, dias_atras: int = 7) -> List[Noticia]:
        """
        Scrapear noticias (método principal)

        Args:
            dias_atras: Número de días hacia atrás a buscar

        Returns:
            Lista de objetos Noticia
        """
        try:
            logger.info(f"[{self.nombre}] Iniciando scraping ({dias_atras} días)...")

            # Validar configuración
            if not self.url_base:
                raise ValueError(f"URL base no configurada para {self.nombre}")

            # Scrapear (implementación específica por subclass)
            noticias = self._scrape_impl(dias_atras)

            # Validar resultados
            if not noticias:
                logger.warning(f"[{self.nombre}] No se encontraron noticias")
                return []

            logger.info(f"[{self.nombre}] ✓ Scrapeadas {len(noticias)} noticias")
            return noticias

        except Exception as e:
            logger.error(f"[{self.nombre}] Error durante scraping: {e}", exc_info=True)
            return []

    @abstractmethod
    def _scrape_impl(self, dias_atras: int) -> List[Noticia]:
        """
        Implementación específica de scraping (por subclass)

        Args:
            dias_atras: Número de días hacia atrás

        Returns:
            Lista de noticias scrapeadas
        """
        pass

    def _fetch_url(self, url: str) -> Optional[str]:
        """
        Descargar contenido HTML de una URL con manejo de errores

        Args:
            url: URL a descargar

        Returns:
            HTML content o None si falla
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.nombre}] Error descargando {url}: {e}")
            return None

    def _is_fecha_reciente(self, fecha: Optional[datetime], dias_atras: int) -> bool:
        """
        Validar si una fecha está dentro del rango de días

        Args:
            fecha: Fecha a validar
            dias_atras: Número de días hacia atrás

        Returns:
            True si está dentro del rango
        """
        if not fecha:
            return False

        fecha_limite = datetime.now() - timedelta(days=dias_atras)
        return fecha >= fecha_limite

    def _limpiar_texto(self, texto: str) -> str:
        """
        Limpiar texto (remover espacios extras, etc.)

        Args:
            texto: Texto a limpiar

        Returns:
            Texto limpio
        """
        if not texto:
            return ""

        # Remover espacios extras
        texto = " ".join(texto.split())

        # Remover caracteres especiales problemáticos
        texto = texto.replace("\r", "").replace("\n\n\n", "\n\n")

        return texto.strip()

    def _esperar(self, segundos: float = 1.0):
        """
        Esperar entre requests (rate limiting)

        Args:
            segundos: Segundos a esperar
        """
        time.sleep(segundos)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.nombre}>"
