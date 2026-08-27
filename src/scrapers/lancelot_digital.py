"""
Scraper para Lancelot Digital
https://www.lancelotdigital.com/lanzarote
"""

from datetime import datetime
from typing import List, Optional
import logging
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper, Noticia

logger = logging.getLogger(__name__)


class LancelotDigitalScraper(BaseScraper):
    """
    Scraper para Lancelot Digital (especializado en Lanzarote)

    Estructura esperada del HTML:
    - Articulos en <article> o <div class="article">
    - Titulo en <h2> o <h3>
    - URL en <a href="...">
    - Fecha en atributo data-date o contenedor específico
    - Contenido/excerpt en <p> o <div class="excerpt">
    """

    def _scrape_impl(self, dias_atras: int) -> List[Noticia]:
        """
        Implementación específica para Lancelot Digital

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

            # Buscar artículos (probar múltiples selectores)
            articulos = self._encontrar_articulos(soup)

            if not articulos:
                logger.warning(f"[{self.nombre}] No se encontraron artículos en la página")
                return []

            logger.info(f"[{self.nombre}] Encontrados {len(articulos)} posibles artículos")

            # Procesar cada artículo
            for articulo in articulos:
                try:
                    noticia = self._procesar_articulo(articulo)

                    if noticia and self._is_fecha_reciente(noticia.fecha_publicacion, dias_atras):
                        noticias.append(noticia)
                        logger.debug(f"[{self.nombre}] ✓ Noticia: {noticia.titulo[:50]}...")

                    # Rate limiting
                    self._esperar(0.5)

                except Exception as e:
                    logger.debug(f"[{self.nombre}] Error procesando artículo: {e}")
                    continue

            return noticias

        except Exception as e:
            logger.error(f"[{self.nombre}] Error en _scrape_impl: {e}", exc_info=True)
            return []

    def _encontrar_articulos(self, soup: BeautifulSoup) -> list:
        """
        Encontrar elementos de artículos en la página

        Prueba múltiples selectores comunes

        Args:
            soup: BeautifulSoup object

        Returns:
            Lista de elementos HTML de artículos
        """
        # Selectores a probar (orden de probabilidad)
        selectores = [
            "article",
            "div.article",
            "div.post",
            "div.entry",
            "div.noticia",
            "div.news-item",
            "div[class*='article']",
            "div[class*='post']",
        ]

        for selector in selectores:
            articulos = soup.select(selector)
            if articulos and len(articulos) > 5:  # Al menos 5 artículos
                logger.debug(f"[{self.nombre}] Selector encontrado: {selector} ({len(articulos)} items)")
                return articulos

        # Si no encontramos con selectores, probar con tags genéricos
        articulos = soup.find_all("div", limit=50)
        return articulos if articulos else []

    def _procesar_articulo(self, articulo) -> Optional[Noticia]:
        """
        Procesar un elemento de artículo y extraer información

        Args:
            articulo: BeautifulSoup element

        Returns:
            Objeto Noticia o None si falla
        """
        try:
            # Extraer título
            titulo = self._extraer_titulo(articulo)
            if not titulo:
                return None

            # Extraer URL
            url = self._extraer_url(articulo)
            if not url:
                return None

            # Evitar URLs duplicadas o inválidas
            if not self._es_url_valida(url):
                return None

            # Extraer contenido/excerpt
            contenido = self._extraer_contenido(articulo)

            # Extraer fecha
            fecha = self._extraer_fecha(articulo)

            # Crear objeto Noticia
            noticia = Noticia(
                titulo=self._limpiar_texto(titulo),
                url=url,
                fuente=self.nombre,
                contenido=contenido,
                fecha_publicacion=fecha
            )

            return noticia

        except Exception as e:
            logger.debug(f"[{self.nombre}] Error procesando artículo: {e}")
            return None

    def _extraer_titulo(self, articulo) -> Optional[str]:
        """Extraer título del artículo"""
        # Probar múltiples selectores de título
        selectores_titulo = ["h1", "h2", "h3", "h4", ".title", ".headline", "[class*='title']"]

        for selector in selectores_titulo:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 10:  # Al menos 10 caracteres
                    return texto

        return None

    def _extraer_url(self, articulo) -> Optional[str]:
        """Extraer URL del artículo"""
        # Buscar link dentro del artículo
        link = articulo.find("a", href=True)

        if not link:
            return None

        url = link.get("href", "").strip()

        if not url:
            return None

        # Si es URL relativa, agregar dominio
        if url.startswith("/"):
            url = "https://www.lancelotdigital.com" + url
        elif not url.startswith("http"):
            url = "https://www.lancelotdigital.com/" + url

        return url

    def _extraer_contenido(self, articulo) -> Optional[str]:
        """Extraer contenido/excerpt del artículo"""
        selectores_contenido = [
            ".excerpt",
            ".summary",
            ".description",
            "[class*='excerpt']",
            "[class*='summary']",
            "p"
        ]

        for selector in selectores_contenido:
            elemento = articulo.select_one(selector)
            if elemento:
                texto = elemento.get_text()
                if texto and len(texto) > 20:
                    return texto[:500]  # Primeros 500 caracteres

        return None

    def _extraer_fecha(self, articulo) -> Optional[datetime]:
        """Extraer fecha de publicación del artículo"""
        # Probar múltiples formas de encontrar la fecha

        # 1. Buscar atributo data-date o similar
        for attr in ["data-date", "data-published", "datetime"]:
            fecha_str = articulo.get(attr)
            if fecha_str:
                fecha = self._parsear_fecha(fecha_str)
                if fecha:
                    return fecha

        # 2. Buscar elemento con clase de fecha
        selectores_fecha = [
            ".date",
            ".published",
            ".post-date",
            "[class*='date']",
            "[class*='time']",
            "time"
        ]

        for selector in selectores_fecha:
            elemento = articulo.select_one(selector)
            if elemento:
                fecha_str = elemento.get_text() or elemento.get("datetime")
                if fecha_str:
                    fecha = self._parsear_fecha(fecha_str)
                    if fecha:
                        return fecha

        # Si no encontramos fecha, asumir hoy
        logger.debug(f"[{self.nombre}] Fecha no encontrada, asumiendo hoy")
        return datetime.now()

    def _parsear_fecha(self, fecha_str: str) -> Optional[datetime]:
        """
        Parsear string de fecha a datetime

        Soporta múltiples formatos comunes
        """
        if not fecha_str:
            return None

        fecha_str = fecha_str.strip()

        # Formatos a probar
        formatos = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d de %B de %Y",
            "%d de %b de %Y",
            "%A, %d de %B de %Y",
            "%Y-%m-%dT%H:%M:%S",
        ]

        for formato in formatos:
            try:
                return datetime.strptime(fecha_str, formato)
            except ValueError:
                continue

        logger.debug(f"[{self.nombre}] No se pudo parsear fecha: {fecha_str}")
        return None

    def _es_url_valida(self, url: str) -> bool:
        """Validar que la URL sea válida"""
        if not url or len(url) < 10:
            return False

        if not url.startswith("http"):
            return False

        # Evitar URLs de imágenes, PDFs, etc.
        extensiones_evitar = [".jpg", ".png", ".pdf", ".zip"]
        if any(url.lower().endswith(ext) for ext in extensiones_evitar):
            return False

        return True
