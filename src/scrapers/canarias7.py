"""
Scraper para Canarias7
https://www.canarias7.es/
"""

from datetime import datetime
from typing import List, Optional
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper, Noticia

logger = logging.getLogger(__name__)


class Canarias7Scraper(BaseScraper):
    """
    Scraper para Canarias7

    Principal periódico digital de Canarias.
    Cobertura general de noticias de Canarias.
    """

    def _scrape_impl(self, dias_atras: int) -> List[Noticia]:
        """Implementación específica para Canarias7"""
        noticias = []

        try:
            html = self._fetch_url(self.url_base)
            if not html:
                return []

            soup = BeautifulSoup(html, "html.parser")
            articulos = self._encontrar_articulos(soup)

            if not articulos:
                logger.warning(f"[{self.nombre}] No se encontraron artículos")
                return []

            logger.info(f"[{self.nombre}] Encontrados {len(articulos)}")

            for articulo in articulos:
                try:
                    noticia = self._procesar_articulo(articulo)
                    if noticia and self._is_fecha_reciente(noticia.fecha_publicacion, dias_atras):
                        noticias.append(noticia)
                        logger.debug(f"[{self.nombre}] ✓ {noticia.titulo[:50]}...")
                    self._esperar(0.5)
                except Exception as e:
                    logger.debug(f"[{self.nombre}] Error: {e}")
                    continue

            return noticias

        except Exception as e:
            logger.error(f"[{self.nombre}] Error: {e}", exc_info=True)
            return []

    def _encontrar_articulos(self, soup: BeautifulSoup) -> list:
        """Encontrar artículos"""
        selectores = [
            "article", "div.article", "div.post", "div.noticia",
            "div.news", "div.entry", "div[class*='article']",
            "div[class*='post']", "div[class*='news']",
        ]

        for selector in selectores:
            articulos = soup.select(selector)
            if articulos and len(articulos) > 3:
                logger.debug(f"[{self.nombre}] {selector}")
                return articulos

        return soup.find_all("div", limit=50) if soup else []

    def _procesar_articulo(self, articulo) -> Optional[Noticia]:
        """Procesar artículo"""
        try:
            titulo = self._extraer_titulo(articulo)
            if not titulo:
                return None

            url = self._extraer_url(articulo)
            if not url or not self._es_url_valida(url):
                return None

            return Noticia(
                titulo=self._limpiar_texto(titulo),
                url=url,
                fuente=self.nombre,
                contenido=self._extraer_contenido(articulo),
                fecha_publicacion=self._extraer_fecha(articulo)
            )

        except Exception as e:
            logger.debug(f"[{self.nombre}] Error: {e}")
            return None

    def _extraer_titulo(self, articulo) -> Optional[str]:
        """Extraer título"""
        for selector in ["h2", "h3", "h1", ".title", "[class*='title']", "a"]:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 10:
                    return texto
        return None

    def _extraer_url(self, articulo) -> Optional[str]:
        """Extraer URL"""
        link = articulo.find("a", href=True)
        if not link:
            return None

        url = link.get("href", "").strip()
        if not url:
            return None

        if url.startswith("/"):
            url = "https://www.canarias7.es" + url
        elif not url.startswith("http"):
            url = "https://www.canarias7.es/" + url

        return url

    def _extraer_contenido(self, articulo) -> Optional[str]:
        """Extraer contenido"""
        for selector in [".excerpt", ".summary", ".description", "p"]:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 20:
                    return texto[:500]
        return None

    def _extraer_fecha(self, articulo) -> Optional[datetime]:
        """Extraer fecha"""
        for attr in ["data-date", "data-published", "datetime"]:
            fecha_str = articulo.get(attr)
            if fecha_str:
                fecha = self._parsear_fecha(fecha_str)
                if fecha:
                    return fecha

        for selector in [".date", ".published", "time"]:
            elemento = articulo.select_one(selector)
            if elemento:
                fecha_str = elemento.get_text() or elemento.get("datetime")
                if fecha_str:
                    fecha = self._parsear_fecha(fecha_str)
                    if fecha:
                        return fecha

        return datetime.now()

    def _parsear_fecha(self, fecha_str: str) -> Optional[datetime]:
        """Parsear fecha"""
        if not fecha_str:
            return None

        fecha_str = fecha_str.strip()
        formatos = [
            "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y",
            "%d de %B de %Y", "%Y-%m-%dT%H:%M:%S",
        ]

        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue

        return None

    def _es_url_valida(self, url: str) -> bool:
        """Validar URL"""
        if not url or len(url) < 10 or not url.startswith("http"):
            return False
        extensiones_evitar = [".jpg", ".png", ".pdf", ".zip"]
        return not any(url.lower().endswith(ext) for ext in extensiones_evitar)
