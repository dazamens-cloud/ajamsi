"""
IMAGE COMPOSITOR AGENT
Responsabilidad: Componer imagen de usuario + personaje El Típico Canario en la posición correcta
"""

import logging
from typing import Dict
from datetime import datetime
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


class ImageCompositorAgent:
    """
    Toma una imagen de meme (cualquier tamaño/tema) y compone El Típico Canario
    en la posición correcta para crear una viñeta lista para TikTok.

    - Redimensiona la imagen a 1080x1920 (o mantiene aspecto si es vertical)
    - Posiciona El Típico Canario transparente
    - Devuelve PNG listo para usar
    """

    ANCHO = 1080
    ALTO = 1920

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
        self.logger.info(f"✓ ImageCompositorAgent inicializado - Salida: {self.output_dir}")

    def ejecutar(self, imagen_path: str, posicion: str = 'derecha',
                 escala: float = 0.45) -> Dict:
        """
        Componer imagen de usuario + El Típico Canario.

        Args:
            imagen_path: Ruta a imagen de meme (cualquier tamaño)
            posicion: 'izquierda', 'derecha', 'centro', 'arriba', 'abajo'
            escala: Tamaño del personaje relativo al alto (0.0-1.0, default 0.45)

        Returns:
            Dict con 'imagen_path' de la composición final
        """
        try:
            imagen_path = Path(imagen_path)
            if not imagen_path.exists():
                raise FileNotFoundError(f"Imagen no encontrada: {imagen_path}")

            self.logger.info(f"🖼️ Componiendo imagen con personaje ({posicion})...")

            # Cargar imagen de usuario
            img_usuario = Image.open(imagen_path).convert('RGB')
            w_orig, h_orig = img_usuario.size

            # Redimensionar a 1080x1920 manteniendo aspecto (letterbox si es necesario)
            img_fondo = self._redimensionar_a_formato(img_usuario)

            # Cargar personaje transparente
            personaje = Image.open(self.imagen_personaje).convert('RGBA')
            objetivo_alto = int(self.ALTO * escala)
            ratio = objetivo_alto / personaje.height
            personaje_redim = personaje.resize(
                (int(personaje.width * ratio), objetivo_alto), Image.LANCZOS
            )

            # Posicionar personaje
            px, py = self._calcular_posicion(posicion, personaje_redim)

            # Sombra suave bajo el personaje
            sombra = Image.new('RGBA', img_fondo.size, (0, 0, 0, 0))
            if posicion not in ['arriba']:
                from PIL import ImageDraw
                sdraw = ImageDraw.Draw(sombra)
                sdraw.ellipse(
                    [px + 30, py + personaje_redim.height - 40,
                     px + personaje_redim.width - 30, py + personaje_redim.height + 20],
                    fill=(90, 70, 40, 80)
                )
                img_fondo.paste(sombra, (0, 0), sombra)

            # Componer: personaje transparente sobre fondo
            img_fondo.paste(personaje_redim, (px, py), personaje_redim)

            # Guardar
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            resultado_path = self.output_dir / f"compuesto_{timestamp}.png"
            img_fondo.save(str(resultado_path), 'PNG')

            self.logger.info(f"✅ Imagen compuesta: {resultado_path.name}")
            return {
                'status': 'success',
                'imagen_path': str(resultado_path),
                'imagen_filename': resultado_path.name,
                'resolucion': f'{self.ANCHO}x{self.ALTO}',
                'posicion': posicion,
                'escala': escala,
            }

        except Exception as e:
            self.logger.error(f"❌ Error componiendo imagen: {e}")
            return {'status': 'error', 'error': str(e), 'imagen_path': None}

    def _redimensionar_a_formato(self, img: Image.Image) -> Image.Image:
        """Redimensionar imagen a 1080x1920, letterbox si es necesario"""
        w, h = img.size
        ratio_usuario = w / h
        ratio_destino = self.ANCHO / self.ALTO  # 9:16

        if ratio_usuario > ratio_destino:
            # Imagen más ancha: fijar alto, llenar ancho con fondo
            nuevo_h = self.ALTO
            nuevo_w = int(nuevo_h * ratio_usuario)
            img_redim = img.resize((nuevo_w, nuevo_h), Image.LANCZOS)
            # Letterbox horizontal
            fondo = Image.new('RGB', (self.ANCHO, self.ALTO), (20, 20, 20))
            offset = (self.ANCHO - nuevo_w) // 2
            fondo.paste(img_redim, (offset, 0))
            return fondo
        else:
            # Imagen más estrecha o igual: fijar ancho, letterbox vertical si es necesario
            nuevo_w = self.ANCHO
            nuevo_h = int(nuevo_w / ratio_usuario)
            img_redim = img.resize((nuevo_w, nuevo_h), Image.LANCZOS)
            if nuevo_h < self.ALTO:
                fondo = Image.new('RGB', (self.ANCHO, self.ALTO), (20, 20, 20))
                offset = (self.ALTO - nuevo_h) // 2
                fondo.paste(img_redim, (0, offset))
                return fondo
            else:
                # Recortar si es más alto
                offset = (nuevo_h - self.ALTO) // 2
                return img_redim.crop((0, offset, nuevo_w, offset + self.ALTO))

    def _calcular_posicion(self, posicion: str, personaje: Image.Image) -> tuple:
        """Calcular (x, y) para posicionar el personaje"""
        w, h = personaje.size

        if posicion == 'derecha':
            return (self.ANCHO - w - 40, int(self.ALTO * 0.5) - h // 2)
        elif posicion == 'izquierda':
            return (40, int(self.ALTO * 0.5) - h // 2)
        elif posicion == 'centro':
            return ((self.ANCHO - w) // 2, int(self.ALTO * 0.5) - h // 2)
        elif posicion == 'arriba':
            return ((self.ANCHO - w) // 2, 80)
        elif posicion == 'abajo':
            return ((self.ANCHO - w) // 2, self.ALTO - h - 100)
        else:
            return (self.ANCHO - w - 40, int(self.ALTO * 0.5) - h // 2)
