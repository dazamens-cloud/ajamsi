"""
IMAGE GENERATOR AGENT
Responsabilidad: Generar imágenes de video (tarjetas meme 1080x1920) 100% local con PIL
"""

import logging
import re
import textwrap
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

logger = logging.getLogger(__name__)


class ImageGeneratorAgent:
    """
    Genera tarjetas visuales estilo meme para los videos.

    - Fondo degradado oscuro
    - Badge "NOTICIA" arriba
    - Titular de la noticia en texto grande envuelto
    - Personaje "El Típico Canario" centrado
    - Hook/frase abajo en amarillo
    - Marca de agua

    100% local: solo PIL, sin APIs.
    """

    ANCHO = 1080
    ALTO = 1920

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        base_dir = Path(__file__).parent.parent.parent
        self.imagen_personaje = base_dir / "imagenes" / "el_tipico_canario.png"
        self.output_dir = base_dir / "imagenes_generadas"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"✓ ImageGeneratorAgent inicializado - Salida: {self.output_dir}")

    def _cargar_fuente(self, tamano: int, negrita: bool = True) -> ImageFont.FreeTypeFont:
        """Cargar fuente del sistema con fallbacks"""
        candidatas = ['impact.ttf', 'arialbd.ttf', 'arial.ttf', 'segoeuib.ttf'] if negrita \
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

    def _fondo_degradado(self) -> Image.Image:
        """Crear fondo degradado vertical azul oscuro -> negro"""
        img = Image.new('RGB', (self.ANCHO, self.ALTO))
        arriba = (26, 26, 64)   # azul noche
        abajo = (10, 10, 18)    # casi negro
        for y in range(self.ALTO):
            t = y / self.ALTO
            r = int(arriba[0] + (abajo[0] - arriba[0]) * t)
            g = int(arriba[1] + (abajo[1] - arriba[1]) * t)
            b = int(arriba[2] + (abajo[2] - arriba[2]) * t)
            for_line = Image.new('RGB', (self.ANCHO, 1), (r, g, b))
            img.paste(for_line, (0, y))
        return img

    @staticmethod
    def _limpiar_texto(texto: str) -> str:
        """Quitar emojis y símbolos que las fuentes del sistema no pueden dibujar"""
        limpio = re.sub(r'[^\w\sáéíóúüñÁÉÍÓÚÜÑ¿?¡!.,:;()\-\'\"%€$0-9]', '', texto)
        return re.sub(r'\s+', ' ', limpio).strip()

    def _texto_envuelto(self, draw: ImageDraw.ImageDraw, texto: str, fuente, max_ancho: int,
                        max_lineas: int = 5) -> list:
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
        # Si sobró texto, marcar la última línea con puntos suspensivos
        if len(' '.join(lineas)) < len(texto) and lineas:
            lineas[-1] = lineas[-1].rstrip('.,;:') + '...'
        return lineas

    def ejecutar(self, noticia: Dict, idea: Optional[Dict] = None, hook: str = '') -> Dict:
        """
        Generar tarjeta de imagen para una noticia.

        Args:
            noticia: Dict con 'titulo' y opcionalmente 'fuente'
            idea: Dict con 'concepto' (opcional)
            hook: Frase gancho para la parte inferior

        Returns:
            Dict con 'imagen_path'
        """
        try:
            titulo = noticia.get('titulo', 'Noticias de Canarias')
            self.logger.info(f"🖼️  Generando imagen para: {titulo[:50]}...")

            img = self._fondo_degradado()
            draw = ImageDraw.Draw(img)

            # --- Badge "NOTICIA" ---
            fuente_badge = self._cargar_fuente(52)
            badge_texto_plano = "ULTIMA HORA · CANARIAS"
            bw = draw.textlength(badge_texto_plano, font=fuente_badge)
            bx = (self.ANCHO - bw) / 2
            draw.rounded_rectangle(
                [bx - 40, 90, bx + bw + 40, 190],
                radius=20, fill=(200, 30, 30)
            )
            draw.text((bx, 110), badge_texto_plano, font=fuente_badge, fill=(255, 255, 255))

            # --- Titular ---
            fuente_titular = self._cargar_fuente(72)
            lineas = self._texto_envuelto(draw, titulo, fuente_titular, self.ANCHO - 120)
            y = 260
            for linea in lineas:
                lw = draw.textlength(linea, font=fuente_titular)
                lx = (self.ANCHO - lw) / 2
                # sombra
                draw.text((lx + 4, y + 4), linea, font=fuente_titular, fill=(0, 0, 0))
                draw.text((lx, y), linea, font=fuente_titular, fill=(255, 255, 255))
                y += 90

            # --- Personaje ---
            if self.imagen_personaje.exists():
                personaje = Image.open(self.imagen_personaje).convert('RGBA')
                # Escalar a ~55% del alto del lienzo
                objetivo_alto = int(self.ALTO * 0.52)
                ratio = objetivo_alto / personaje.height
                nuevo_tam = (int(personaje.width * ratio), objetivo_alto)
                personaje = personaje.resize(nuevo_tam, Image.LANCZOS)

                # Marco estilo "foto" alrededor del personaje
                px = (self.ANCHO - personaje.width) // 2
                py = y + 40
                borde = 12
                draw.rounded_rectangle(
                    [px - borde, py - borde,
                     px + personaje.width + borde, py + personaje.height + borde],
                    radius=24, fill=(255, 255, 255), outline=(255, 214, 10), width=6
                )
                img.paste(personaje, (px, py), personaje)
                y_hook = py + personaje.height + 60
            else:
                y_hook = y + 200

            # --- Hook inferior ---
            texto_hook = hook or (idea.get('concepto', '') if idea else '') or '¿Qué opinas?'
            fuente_hook = self._cargar_fuente(64)
            lineas_hook = self._texto_envuelto(draw, texto_hook, fuente_hook, self.ANCHO - 140,
                                               max_lineas=2)
            for linea in lineas_hook:
                lw = draw.textlength(linea, font=fuente_hook)
                lx = (self.ANCHO - lw) / 2
                draw.text((lx + 3, y_hook + 3), linea, font=fuente_hook, fill=(0, 0, 0))
                draw.text((lx, y_hook), linea, font=fuente_hook, fill=(255, 214, 10))
                y_hook += 80

            # --- Marca de agua ---
            fuente_marca = self._cargar_fuente(40, negrita=False)
            marca = "@ElTipicoCanario"
            mw = draw.textlength(marca, font=fuente_marca)
            draw.text(((self.ANCHO - mw) / 2, self.ALTO - 90), marca,
                      font=fuente_marca, fill=(160, 160, 180))

            # Guardar
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            imagen_path = self.output_dir / f"tarjeta_{timestamp}.png"
            img.save(str(imagen_path), 'PNG')

            self.logger.info(f"✅ Imagen generada: {imagen_path.name}")
            return {
                'status': 'success',
                'imagen_path': str(imagen_path),
                'imagen_filename': imagen_path.name,
                'resolucion': f'{self.ANCHO}x{self.ALTO}',
            }

        except Exception as e:
            self.logger.error(f"❌ Error generando imagen: {e}")
            return {'status': 'error', 'error': str(e), 'imagen_path': None}
