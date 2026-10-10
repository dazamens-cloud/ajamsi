"""
SCRAPER AGENT - FASE 2: SCRAPING REAL
Responsabilidad: Web scraping de noticias de Lanzarote/Canarias
Usa RSS feeds + BeautifulSoup para scraping real
"""

import logging
import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class ScraperAgent:
    """
    Agente especializado en raspar noticias de fuentes locales.

    Responsabilidades:
    - Raspa noticias REALES de fuentes RSS
    - Scraping con BeautifulSoup como fallback
    - Filtra por relevancia y fecha
    - Detecta duplicados
    - Valida contenido
    """

    # RSS Feeds de Canarias (más confiables que web scraping)
    RSS_FEEDS = {
        'canarias7': 'https://www.canarias7.es/feeds/rss',
        'diario_avisos': 'https://diariodeavisos.elespanol.com/feed',
        'eldiario_canarias': 'https://www.eldiario.es/canariasahora/feed',
    }

    # URLs base para scraping directo
    FUENTES_LANZAROTE = {
        'lancelot_digital': 'https://www.lancelotdigital.com/lanzarote',
        'cronicas_lanzarote': 'https://www.cronicasdelanzarote.es/',
        'noticias_lanzarote': 'https://www.noticiasdelanzarote.com/',
        'diario_lanzarote': 'https://www.diariodelanzarote.com/',
        'periodico_lanzarote': 'https://www.elperiodicodelanzarote.com/',
    }

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

    def __init__(self, config: Dict):
        """Inicializar el agente scraper"""
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.timeout = config.get('scrapers', {}).get('timeout', 10)
        self.logger.info("✓ ScraperAgent inicializado (FASE 2: REAL)")

    def ejecutar(self, dias_atras: int = 7, limite_noticias: int = 20) -> Dict:
        """Ejecutar scraping REAL de noticias"""
        self.logger.info(f"🕷️  FASE 2: Scraping REAL ({dias_atras} días atrás)...")

        try:
            noticias = []

            # 1. Scraping desde RSS feeds (primario - más confiable)
            self.logger.info("  📡 Intentando RSS feeds...")
            noticias_rss = self._scrape_rss_feeds()
            noticias.extend(noticias_rss)
            self.logger.info(f"    ✓ {len(noticias_rss)} noticias de RSS")

            # 2. Scraping directo con BeautifulSoup (secundario)
            self.logger.info("  🔍 Intentando scraping directo...")
            noticias_directas = self._scrape_sitios_directos()
            noticias.extend(noticias_directas)
            self.logger.info(f"    ✓ {len(noticias_directas)} noticias de scraping")

            # Procesamiento
            noticias = self._filtrar_por_fecha(noticias, dias_atras)
            noticias = self._remover_duplicados(noticias)
            noticias = noticias[:limite_noticias]

            for noticia in noticias:
                noticia['relevancia_score'] = self._calcular_relevancia(noticia)

            noticias.sort(key=lambda x: x['relevancia_score'], reverse=True)

            resultado = {
                'status': 'success',
                'noticias_encontradas': len(noticias),
                'noticias': noticias,
                'timestamp': datetime.now().isoformat(),
            }

            self.logger.info(f"✅ Scraping completado: {len(noticias)} noticias validadas")
            return resultado

        except Exception as e:
            self.logger.error(f"❌ Error en scraping: {e}")
            return {'status': 'error', 'error': str(e), 'noticias': []}

    def _scrape_rss_feeds(self) -> List[Dict]:
        """Scraping desde RSS feeds (más confiable)"""
        noticias = []

        for nombre, url in self.RSS_FEEDS.items():
            try:
                self.logger.debug(f"    Leyendo RSS: {nombre}")
                feed = feedparser.parse(url)

                for entry in feed.entries[:10]:  # Primeras 10 entradas
                    noticia = {
                        'titulo': entry.get('title', 'Sin título'),
                        'contenido': entry.get('summary', '')[:500],
                        'url': entry.get('link', ''),
                        'fecha': self._parsear_fecha_rss(entry.get('published')),
                        'fuente': nombre,
                        'tipo': 'rss',
                    }

                    if noticia['titulo'] and noticia['url']:
                        noticias.append(noticia)

            except Exception as e:
                self.logger.warning(f"  ⚠️  Error RSS {nombre}: {e}")

        return noticias

    def _scrape_sitios_directos(self) -> List[Dict]:
        """Scraping directo con BeautifulSoup (fallback)"""
        noticias = []

        for nombre, url in list(self.FUENTES_LANZAROTE.items())[:3]:  # Top 3
            try:
                self.logger.debug(f"    Scraping: {nombre}")
                response = requests.get(url, headers={'User-Agent': self.USER_AGENT}, timeout=self.timeout)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Buscar artículos (selectores comunes)
                articles = soup.find_all(['article', 'div'], class_=lambda x: x and 'article' in x.lower())[:5]

                for article in articles:
                    titulo_elem = article.find(['h1', 'h2', 'h3', 'a'])
                    contenido_elem = article.find(['p', 'summary'])

                    if titulo_elem:
                        noticia = {
                            'titulo': titulo_elem.get_text(strip=True)[:200],
                            'contenido': contenido_elem.get_text(strip=True)[:500] if contenido_elem else '',
                            'url': url,
                            'fecha': datetime.now().isoformat(),
                            'fuente': nombre,
                            'tipo': 'scraping',
                        }

                        if noticia['titulo']:
                            noticias.append(noticia)

            except Exception as e:
                self.logger.warning(f"  ⚠️  Error scraping {nombre}: {e}")

        return noticias

    def _filtrar_por_fecha(self, noticias: List[Dict], dias_atras: int) -> List[Dict]:
        """Filtrar noticias por rango de fecha"""
        fecha_limite = datetime.now() - timedelta(days=dias_atras)
        resultado = []
        for n in noticias:
            try:
                fecha = self._parsear_fecha(n.get('fecha'))
                if fecha and fecha > fecha_limite:
                    resultado.append(n)
            except:
                resultado.append(n)
        return resultado

    def _remover_duplicados(self, noticias: List[Dict]) -> List[Dict]:
        """Detectar y remover noticias duplicadas"""
        vistos = set()
        resultado = []
        for noticia in noticias:
            titulo_hash = hash(noticia.get('titulo', '').lower())
            if titulo_hash not in vistos:
                vistos.add(titulo_hash)
                resultado.append(noticia)
        return resultado

    def _calcular_relevancia(self, noticia: Dict) -> float:
        """Calcular score de relevancia (0-100) - favoreciendo contenido ligero/divertido"""
        score = 50.0
        titulo = noticia.get('titulo', '').lower()
        contenido = noticia.get('contenido', '').lower()

        # Penalidades DURAS por temas serios/oscuros (filtro meme-friendly)
        palabras_negativas = {
            'asesinato': -60, 'muerto': -50, 'muerte': -50, 'crimen': -55,
            'violencia': -50, 'delito': -45, 'droga': -40, 'narcotráfico': -50,
            'accidente fatal': -40, 'homicidio': -60, 'víctima mortal': -50,
            'enfrentamiento': -35, 'disparos': -40, 'ataque': -30,
            'política': -25, 'congreso': -20, 'parlamento': -20,
            'desastre': -30, 'tragedia': -40, 'catástrofe': -45,
        }

        for palabra_negativa, penalidad in palabras_negativas.items():
            if palabra_negativa in titulo or palabra_negativa in contenido[:200]:
                score += penalidad  # Sumar penalidad (negativa)

        # BONUS por temas ligeros/divertidos (favorecidos para memes)
        palabras_positivas = {
            'turismo': 20, 'playa': 15, 'viaje': 15, 'evento': 18,
            'fiesta': 20, 'festival': 22, 'carnaval': 25, 'cultura': 18,
            'deporte': 12, 'fútbol': 10, 'equipo': 8,
            'arte': 15, 'museo': 12, 'exposición': 15,
            'tendencia': 15, 'viral': 18, 'meme': 25,
            'humor': 20, 'cómico': 20, 'jocoso': 20,
            'anécdota': 15, 'curiosidad': 15, 'inusual': 18,
            'gastronomía': 12, 'comida': 10, 'restaurante': 10,
            'naturaleza': 12, 'animal': 12, 'fauna': 10,
            'lanzarote': 20, 'canaria': 15, 'archipiélago': 10,
            'canarias': 15, 'isleta': 10,
        }

        for palabra_positiva, bonus in palabras_positivas.items():
            if palabra_positiva in titulo:
                score += bonus * 1.5  # 1.5x bonus en título
            elif palabra_positiva in contenido[:200]:
                score += bonus

        # Penalidad para contenido muy corto
        if len(noticia.get('contenido', '')) < 50:
            score -= 20

        return max(-100, min(score, 100.0))

    def _parsear_fecha(self, fecha_str: Optional[str]) -> datetime:
        """Parsear string de fecha (maneja timezone-aware y naive)"""
        if not fecha_str:
            return datetime.now()
        try:
            dt = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
            if dt.tzinfo:
                return dt.replace(tzinfo=None)
            return dt
        except:
            return datetime.now()

    def _parsear_fecha_rss(self, fecha_str: Optional[str]) -> str:
        """Parsear fecha RSS a ISO format (naive)"""
        if not fecha_str:
            return datetime.now().isoformat()
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(fecha_str)
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            return dt.isoformat()
        except:
            return datetime.now().isoformat()
