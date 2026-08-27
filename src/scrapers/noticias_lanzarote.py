"""
Scraper para Noticias de Lanzarote
https://www.noticiasdelanzarote.com/
"""

from datetime import datetime
from typing import List, Optional
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper, Noticia

logger = logging.getLogger(__name__)


class NoticiasLanzaroteScraper(BaseScraper):
    """
    Scraper para Noticias de Lanzarote

    Portal de noticias generalista con enfoque local.
    Estructura típica de sitio agregador de noticias.
    """

    def _scrape_impl(self, dias_atras: int) -> List[Noticia]:
        """
        Implementación específica para Noticias de Lanzarote

        Args:
            dias_atras: Número de días hacia atrás

        Returns:
            Lista de noticias
        """
        noticias = []

        try:
            # Descargar página principal
            html = self._fetch_url(self.url_base)
            if not html:
                return []

            # Parsear HTML
            soup = BeautifulSoup(html, "html.parser")

            # Buscar artículos
            articulos = self._encontrar_articulos(soup)

            if not articulos:
                logger.warning(f"[{self.nombre}] No se encontraron artículos")
                return []

            logger.info(f"[{self.nombre}] Encontrados {len(articulos)} posibles artículos")

            # Procesar cada artículo
            for articulo in articulos:
                try:
                    noticia = self._procesar_articulo(articulo)

                    if noticia and self._is_fecha_reciente(noticia.fecha_publicacion, dias_atras):
                        noticias.append(noticia)
                        logger.debug(f"[{self.nombre}] ✓ Noticia: {noticia.titulo[:50]}...")

                    self._esperar(0.5)

                except Exception as e:
                    logger.debug(f"[{self.nombre}] Error procesando artículo: {e}")
                    continue

            return noticias

        except Exception as e:
            logger.error(f"[{self.nombre}] Error en _scrape_impl: {e}", exc_info=True)
            return []

    def _encontrar_articulos(self, soup: BeautifulSoup) -> list:
        """Encontrar elementos de artículos en la página"""
        selectores = [
            "article",
            "div.article",
            "div.news-item",
            "div.noticia",
            "div.post",
            "div.entry",
            "div[class*='article']",
            "div[class*='news']",
            "div[class*='noticia']",
        ]

        for selector in selectores:
            articulos = soup.select(selector)
            if articulos and len(articulos) > 3:
                logger.debug(f"[{self.nombre}] Selector: {selector} ({len(articulos)} items)")
                return articulos

        return soup.find_all("div", limit=50) if soup else []

    def _procesar_articulo(self, articulo) -> Optional[Noticia]:
        """Procesar un elemento de artículo"""
        try:
            titulo = self._extraer_titulo(articulo)
            if not titulo:
                return None

            url = self._extraer_url(articulo)
            if not url or not self._es_url_valida(url):
                return None

            contenido = self._extraer_contenido(articulo)
            fecha = self._extraer_fecha(articulo)

            return Noticia(
                titulo=self._limpiar_texto(titulo),
                url=url,
                fuente=self.nombre,
                contenido=contenido,
                fecha_publicacion=fecha
            )

        except Exception as e:
            logger.debug(f"[{self.nombre}] Error procesando: {e}")
            return None

    def _extraer_titulo(self, articulo) -> Optional[str]:
        """Extraer título del artículo"""
        selectores = [
            "h2", "h3", "h1", "h4",
            ".title", ".headline", ".post-title",
            "[class*='title']", "[class*='heading']",
            "a.link"
        ]

        for selector in selectores:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 10:
                    return texto

        return None

    def _extraer_url(self, articulo) -> Optional[str]:
        """Extraer URL del artículo"""
        link = articulo.find("a", href=True)
        if not link:
            return None

        url = link.get("href", "").strip()
        if not url:
            return None

        # Normalizar URL
        if url.startswith("/"):
            url = "https://www.noticiasdelanzarote.com" + url
        elif not url.startswith("http"):
            url = "https://www.noticiasdelanzarote.com/" + url

        return url

    def _extraer_contenido(self, articulo) -> Optional[str]:
        """Extraer contenido/excerpt del artículo"""
        selectores = [
            ".excerpt", ".summary", ".description", ".content",
            ".post-content", ".entry-excerpt",
            "[class*='excerpt']", "[class*='summary']",
            "p"
        ]

        for selector in selectores:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 20:
                    return texto[:500]

        return None

    def _extraer_fecha(self, articulo) -> Optional[datetime]:
        """Extraer fecha de publicación"""
        # Atributos de fecha
        for attr in ["data-date", "data-published", "datetime", "data-time"]:
            fecha_str = articulo.get(attr)
            if fecha_str:
                fecha = self._parsear_fecha(fecha_str)
                if fecha:
                    return fecha

        # Elementos de fecha
        selectores = [
            ".date", ".published", ".post-date",
            ".entry-date", ".meta-date",
            "[class*='date']", "[class*='time']",
            "time"
        ]

        for selector in selectores:
            elemento = articulo.select_one(selector)
            if elemento:
                fecha_str = elemento.get_text() or elemento.get("datetime")
                if fecha_str:
                    fecha = self._parsear_fecha(fecha_str)
                    if fecha:
                        return fecha

        logger.debug(f"[{self.nombre}] Fecha no encontrada, usando hoy")
        return datetime.now()

    def _parsear_fecha(self, fecha_str: str) -> Optional[datetime]:
        """Parsear fecha en múltiples formatos"""
        if not fecha_str:
            return None

        fecha_str = fecha_str.strip()

        formatos = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d de %B de %Y",
            "%d de %b de %Y",
            "%A, %d de %B de %Y",
            "%Y-%m-%dT%H:%M:%S",
            "%d %B %Y"
        ]

        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue

        logger.debug(f"[{self.nombre}] No se pudo parsear: {fecha_str}")
        return None

    def _es_url_valida(self, url: str) -> bool:
        """Validar URL"""
        if not url or len(url) < 10:
            return False

        if not url.startswith("http"):
            return False

        extensiones_evitar = [".jpg", ".png", ".pdf", ".zip", ".gif"]
        if any(url.lower().endswith(ext) for ext in extensiones_evitar):
            return False

        return True
