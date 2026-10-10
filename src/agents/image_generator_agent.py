"""
IMAGE GENERATOR AGENT
Responsabilidad: Generar viñetas estilo @hummorkana (1080x1920) 100% local con PIL
Estilo: escena cartoon canaria + setup arriba / remate abajo en fuente cómic con contorno
"""

import logging
import random
import re
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class ImageGeneratorAgent:
    """
    Genera viñetas cómicas al estilo de la cuenta @hummorkana:

    - Fondo: cielo canario degradado con sol y nubes cartoon + suelo de arena
    - El Típico integrado en la escena (PNG transparente)
    - Setup del chiste ARRIBA en mayúsculas, fuente cómic con contorno
    - Remate ABAJO en el mismo estilo
    - Titular de la noticia pequeño como contexto

    100% local: solo PIL, sin APIs.
    VARIACIONES: Múltiples estilos de color y composición visual.
    """

    ANCHO = 1080
    ALTO = 1920

    # Estilos visuales diferentes para cada generación
    ESTILOS = [
        # Estilo 1: Cielo azul clásico (hummorkana original)
        {
            'nombre': 'cielo_azul',
            'cielo_arriba': (86, 170, 226),
            'cielo_abajo': (188, 228, 248),
            'arena': (238, 214, 160),
            'sol': (255, 221, 89),
            'setup_color': (255, 255, 255),
            'remate_color': (255, 221, 60),
            'posicion_personaje': 'centro',
        },
        # Estilo 2: Atardecer naranja-rojo
        {
            'nombre': 'atardecer',
            'cielo_arriba': (255, 140, 60),
            'cielo_abajo': (255, 200, 120),
            'arena': (220, 160, 80),
            'sol': (255, 80, 40),
            'setup_color': (50, 40, 30),
            'remate_color': (255, 255, 100),
            'posicion_personaje': 'derecha',
        },
        # Estilo 3: Cielo tropical morado-rosado
        {
            'nombre': 'tropical',
            'cielo_arriba': (120, 80, 180),
            'cielo_abajo': (200, 120, 200),
            'arena': (255, 200, 150),
            'sol': (255, 100, 200),
            'setup_color': (255, 255, 255),
            'remate_color': (255, 220, 100),
            'posicion_personaje': 'izquierda',
        },
        # Estilo 4: Cielo verde tropical
        {
            'nombre': 'verde_tropical',
            'cielo_arriba': (100, 200, 150),
            'cielo_abajo': (180, 230, 200),
            'arena': (180, 140, 80),
            'sol': (255, 200, 50),
            'setup_color': (20, 60, 40),
            'remate_color': (255, 220, 80),
            'posicion_personaje': 'centro',
        },
    ]

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        base_dir = Path(__file__).parent.parent.parent
        personaje_transparente = base_dir / "imagenes" / "el_tipico_canario_transparente.png"
        personaje_original = base_dir / "imagenes" / "el_tipico_canario.png"
        self.imagen_personaje = personaje_transparente if personaje_transparente.exists() \
            else personaje_original
        self.output_dir = base_dir / "imagenes_generadas"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"✓ ImageGeneratorAgent inicializado - Salida: {self.output_dir}")

    def _cargar_fuente(self, tamano: int, comic: bool = True) -> ImageFont.FreeTypeFont:
        """Cargar fuente cómic del sistema con fallbacks"""
        candidatas = ['comicbd.ttf', 'comic.ttf', 'arialbd.ttf'] if comic \
            else ['arial.ttf', 'segoeui.ttf']
        fonts_dir = Path('C:/Windows/Fonts')
        for nombre in candidatas:
            ruta = fonts_dir / nombre
            if ruta.exists():
                try:
                    return ImageFont.truetype(str(ruta), tamano)
                except Exception:
                    continue
        return ImageFont.load_default()

    @staticmethod
    def _limpiar_texto(texto: str) -> str:
        """Quitar emojis y símbolos que las fuentes del sistema no pueden dibujar"""
        limpio = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ¿?¡!.,:;()\-\'\"%€$0-9]', '', texto)
        return re.sub(r'\s+', ' ', limpio).strip()

    def _texto_envuelto(self, draw, texto: str, fuente, max_ancho: int,
                        max_lineas: int = 4) -> list:
        """Envolver texto por palabras para que quepa en max_ancho píxeles"""
        texto = self._limpiar_texto(texto)
        palabras = texto.split()
        lineas = []
        linea = ''
        for palabra in palabras:
            candidata = f"{linea} {palabra}".strip()
            if draw.textlength(candidata, font=fuente) <= max_ancho:
                linea = candidata
            else:
                if linea:
                    lineas.append(linea)
                linea = palabra
                if len(lineas) >= max_lineas:
                    break
        if linea and len(lineas) < max_lineas:
            lineas.append(linea)
        if len(' '.join(lineas)) < len(texto) and lineas:
            lineas[-1] = lineas[-1].rstrip('.,;:') + '...'
        return lineas

    def _seleccionar_estilo(self) -> Dict:
        """Seleccionar aleatoriamente uno de los estilos visuales disponibles"""
        return random.choice(self.ESTILOS)

    def _fondo_escena(self, estilo: Dict = None) -> tuple[Image.Image, Dict]:
        """Cielo degradado + sol + nubes + suelo, con estilo personalizable.
        Retorna (imagen, estilo_usado) para acceso posterior a colores."""
        if estilo is None:
            estilo = self._seleccionar_estilo()

        img = Image.new('RGB', (self.ANCHO, self.ALTO))
        draw = ImageDraw.Draw(img)

        # Cielo: degradado personalizado según estilo
        arriba = estilo['cielo_arriba']
        abajo = estilo['cielo_abajo']
        alto_cielo = int(self.ALTO * 0.82)
        for y in range(alto_cielo):
            t = y / alto_cielo
            r = int(arriba[0] + (abajo[0] - arriba[0]) * t)
            g = int(arriba[1] + (abajo[1] - arriba[1]) * t)
            b = int(arriba[2] + (abajo[2] - arriba[2]) * t)
            draw.line([(0, y), (self.ANCHO, y)], fill=(r, g, b))

        # Suelo: arena personalizada
        draw.rectangle([0, alto_cielo, self.ANCHO, self.ALTO], fill=estilo['arena'])
        linea_color = tuple(max(0, c - 30) for c in estilo['arena'])
        draw.line([(0, alto_cielo), (self.ANCHO, alto_cielo)], fill=linea_color, width=6)

        # Sol
        draw.ellipse([self.ANCHO - 300, 150, self.ANCHO - 120, 330], fill=estilo['sol'])

        # Nubes cartoon (elipses agrupadas)
        nube_color = tuple(max(200, min(255, c - 50)) for c in estilo['cielo_abajo'])
        rng = random.Random(42)
        for cx, cy, esc in [(200, 260, 1.0), (760, 420, 0.8), (380, 540, 0.65)]:
            for dx, dy, rw, rh in [(-70, 0, 90, 48), (0, -25, 100, 60), (70, 0, 90, 48)]:
                draw.ellipse(
                    [cx + dx * esc - rw * esc, cy + dy * esc - rh * esc,
                     cx + dx * esc + rw * esc, cy + dy * esc + rh * esc],
                    fill=nube_color
                )

        return img, estilo

    def _dibujar_texto_comic(self, draw, texto: str, fuente, y: int,
                             color=(255, 255, 255), contorno=(20, 20, 30),
                             max_ancho: int = None, max_lineas: int = 4,
                             interlinea: float = 1.15) -> int:
        """Dibujar texto centrado en mayúsculas con contorno grueso. Devuelve la Y final."""
        max_ancho = max_ancho or (self.ANCHO - 100)
        lineas = self._texto_envuelto(draw, texto.upper(), fuente, max_ancho, max_lineas)
        tam = fuente.size
        grosor = max(4, tam // 10)
        for linea in lineas:
            lw = draw.textlength(linea, font=fuente)
            lx = (self.ANCHO - lw) / 2
            draw.text((lx, y), linea, font=fuente, fill=color,
                      stroke_width=grosor, stroke_fill=contorno)
            y += int(tam * interlinea)
        return y

    def ejecutar(self, noticia: Dict, idea: Optional[Dict] = None,
                 hook: str = '', setup: str = '', remate: str = '') -> Dict:
        """
        Generar viñeta cómica para una noticia con ESTILO VISUAL ÚNICO.

        Args:
            noticia: Dict con 'titulo' y opcionalmente 'fuente'
            idea: Dict con 'concepto', 'setup', 'remate' (opcional)
            hook: Frase gancho alternativa
            setup: Texto de arriba (si no, se toma de la idea o se construye)
            remate: Texto de abajo (si no, se toma de la idea)

        Returns:
            Dict con 'imagen_path' y 'estilo_usado'
        """
        try:
            titulo = noticia.get('titulo', 'Noticias de Canarias')
            self.logger.info(f"🖼️  Generando viñeta para: {titulo[:50]}...")

            idea = idea or {}
            texto_setup = setup or idea.get('setup', '') or 'CHACHO, LO QUE HA PASADO'
            texto_remate = remate or idea.get('remate', '') or hook or '¿TÚ QUÉ OPINAS?'

            # Generar fondo con ESTILO ÚNICO
            img, estilo = self._fondo_escena()
            draw = ImageDraw.Draw(img)
            self.logger.info(f"  Estilo: {estilo['nombre']}")

            # --- Setup arriba con color del estilo ---
            fuente_setup = self._cargar_fuente(88)
            y_fin_setup = self._dibujar_texto_comic(
                draw, texto_setup, fuente_setup, 110,
                color=estilo['setup_color'], contorno=(25, 25, 35), max_lineas=3)

            # --- Personaje en posición variable según estilo ---
            if self.imagen_personaje.exists():
                personaje = Image.open(self.imagen_personaje).convert('RGBA')
                objetivo_alto = int(self.ALTO * 0.47)
                ratio = objetivo_alto / personaje.height
                personaje = personaje.resize(
                    (int(personaje.width * ratio), objetivo_alto), Image.LANCZOS)

                # Posición según el estilo
                posicion = estilo.get('posicion_personaje', 'centro')
                if posicion == 'izquierda':
                    px = 60
                elif posicion == 'derecha':
                    px = self.ANCHO - personaje.width - 60
                else:  # centro
                    px = (self.ANCHO - personaje.width) // 2

                py = int(self.ALTO * 0.86) - personaje.height

                # Sombra elíptica en el suelo
                sombra = Image.new('RGBA', img.size, (0, 0, 0, 0))
                sdraw = ImageDraw.Draw(sombra)
                sdraw.ellipse(
                    [px + 40, py + personaje.height - 30,
                     px + personaje.width - 40, py + personaje.height + 30],
                    fill=(90, 70, 40, 90))
                img.paste(sombra, (0, 0), sombra)
                img.paste(personaje, (px, py), personaje)

            # --- Remate abajo con color del estilo ---
            fuente_remate = self._cargar_fuente(76)
            self._dibujar_texto_comic(
                draw, texto_remate, fuente_remate, int(self.ALTO * 0.865),
                color=estilo['remate_color'], contorno=(25, 25, 35), max_lineas=2)

            # --- Contexto: titular pequeño bajo el setup ---
            fuente_ctx = self._cargar_fuente(38, comic=False)
            ctx = self._limpiar_texto(titulo)
            lineas_ctx = self._texto_envuelto(draw, ctx, fuente_ctx, self.ANCHO - 260, 2)
            y_ctx = y_fin_setup + 18
            for linea in lineas_ctx:
                lw = draw.textlength(linea, font=fuente_ctx)
                draw.text(((self.ANCHO - lw) / 2, y_ctx), linea, font=fuente_ctx,
                          fill=(40, 60, 90), stroke_width=2, stroke_fill=(235, 245, 252))
                y_ctx += 48

            # Guardar
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            imagen_path = self.output_dir / f"vineta_{timestamp}.png"
            img.save(str(imagen_path), 'PNG')

            self.logger.info(f"✅ Viñeta generada [{estilo['nombre']}]: {imagen_path.name}")
            return {
                'status': 'success',
                'imagen_path': str(imagen_path),
                'imagen_filename': imagen_path.name,
                'resolucion': f'{self.ANCHO}x{self.ALTO}',
                'estilo': estilo['nombre'],
            }

        except Exception as e:
            self.logger.error(f"❌ Error generando viñeta: {e}")
            return {'status': 'error', 'error': str(e), 'imagen_path': None}
