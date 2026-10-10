"""
PUBLICACION REPORTER AGENT
Responsabilidad: Generar documento Word con descripciones y hashtags listos para publicar
"""

import logging
from typing import List, Dict
from datetime import datetime
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

logger = logging.getLogger(__name__)


class PublicacionReporterAgent:
    """
    Genera un .docx con todo lo necesario para publicar cada video:
    - Nombre del archivo de video
    - Descripción/caption recomendado (el de mayor engagement)
    - Variantes de caption
    - Hashtags optimizados
    - Hora recomendada de publicación
    """

    HASHTAGS_BASE = ['#Canarias', '#Lanzarote', '#Tenerife', '#IslasCanarias', '#Noticias']
    HASHTAGS_HUMOR = ['#HumorCanario', '#Memes', '#ElTipicoCanario', '#ParaTi', '#fyp']

    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        base_dir = Path(__file__).parent.parent.parent
        self.output_dir = base_dir / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info("✓ PublicacionReporterAgent inicializado")

    def ejecutar(self, resultados: List[Dict]) -> Dict:
        """
        Generar documento de publicación.

        Args:
            resultados: Lista de dicts, uno por video generado, con claves:
                'noticia' (dict), 'idea' (dict), 'captions' (list),
                'video' (dict con video_filename), 'imagen' (dict)

        Returns:
            Dict con 'doc_path'
        """
        try:
            self.logger.info(f"📄 Generando documento de publicación ({len(resultados)} videos)...")
            doc = Document()

            # Portada
            titulo = doc.add_paragraph()
            titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            run = titulo.add_run("🎬 AJAMSI - Guía de Publicación")
            run.font.size = Pt(26)
            run.font.bold = True
            run.font.color.rgb = RGBColor(120, 40, 200)

            sub = doc.add_paragraph()
            sub.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            sub_run = sub.add_run(
                f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')} · "
                f"{len(resultados)} video(s) listos para publicar"
            )
            sub_run.font.size = Pt(12)
            sub_run.font.color.rgb = RGBColor(100, 100, 100)
            doc.add_paragraph()

            # Consejos generales
            doc.add_heading("📌 Consejos rápidos (algoritmo TikTok 2026)", level=1)
            consejos = [
                "Publica entre 18:00-21:00 (hora canaria) para máximo alcance",
                "Usa 3-5 hashtags nicho, NO 30 genéricos (el algoritmo lo penaliza)",
                "El caption cuenta como keywords: incluye la palabra clave de la noticia",
                "Responde a los primeros comentarios en los primeros 30 minutos",
                "Sube el mismo video a TikTok, Reels y Shorts (no reutilices el archivo con marca de agua de otra plataforma)",
            ]
            for c in consejos:
                doc.add_paragraph(c, style='List Bullet')
            doc.add_paragraph()

            # Un bloque por imagen
            for i, r in enumerate(resultados, 1):
                noticia = r.get('noticia', {})
                idea = r.get('idea', {})
                captions = r.get('captions', [])
                video = r.get('video', {})
                imagen = r.get('imagen', {})
                audio = r.get('audio', {}) or {}

                doc.add_heading(f"🖼️ CONTENIDO {i}: {noticia.get('titulo', 'Sin título')[:80]}", level=1)

                # Archivo de imagen
                p = doc.add_paragraph()
                p.add_run("Imagen: ").bold = True
                p.add_run(imagen.get('imagen_filename', 'N/A'))

                # Video si existe
                if video:
                    p = doc.add_paragraph()
                    p.add_run("Video: ").bold = True
                    p.add_run(video.get('video_filename', 'N/A'))

                p = doc.add_paragraph()
                p.add_run("Fuente noticia: ").bold = True
                p.add_run(f"{noticia.get('fuente', 'N/A')} · {noticia.get('url', '')}")

                p = doc.add_paragraph()
                p.add_run("Ángulo de humor: ").bold = True
                p.add_run(idea.get('angulo_humor', 'N/A'))

                # NARRACIÓN: Guion para que el usuario lo añada manualmente
                doc.add_heading("🎙️ NARRACIÓN (Copia este texto en tu editor)", level=2)
                guion_p = doc.add_paragraph()
                guion_text = audio.get('guion_narrado', '') or 'Sin guion'
                guion_run = guion_p.add_run(guion_text)
                guion_run.font.italic = True
                guion_run.font.size = Pt(11)
                guion_run.font.color.rgb = RGBColor(80, 80, 80)

                duracion_p = doc.add_paragraph()
                dur_run = duracion_p.add_run(
                    f"Duración estimada: ~{audio.get('duracion_estimada', 15)}s (a ritmo natural)"
                )
                dur_run.font.size = Pt(9)
                dur_run.font.italic = True
                dur_run.font.color.rgb = RGBColor(120, 120, 120)

                # Caption recomendado (mayor engagement)
                mejor = max(captions, key=lambda c: c.get('engagement_score', 0)) if captions else None
                doc.add_heading("✅ DESCRIPCIÓN RECOMENDADA (copiar y pegar)", level=2)
                if mejor:
                    caja = doc.add_paragraph()
                    caja_run = caja.add_run(mejor.get('caption', ''))
                    caja_run.font.size = Pt(13)
                    caja_run.font.bold = True

                    hashtags_p = doc.add_paragraph()
                    ht_run = hashtags_p.add_run(mejor.get('hashtags', ''))
                    ht_run.font.size = Pt(12)
                    ht_run.font.color.rgb = RGBColor(0, 102, 204)

                    score_p = doc.add_paragraph()
                    score_run = score_p.add_run(
                        f"Engagement estimado: {int(mejor.get('engagement_score', 0) * 100)}%"
                    )
                    score_run.font.italic = True
                    score_run.font.size = Pt(10)

                # Variantes
                if len(captions) > 1:
                    doc.add_heading("🔄 Variantes alternativas", level=2)
                    for c in captions:
                        if c is mejor:
                            continue
                        var = doc.add_paragraph(style='List Bullet')
                        var.add_run(f"[{c.get('tipo', '')}] ").bold = True
                        var.add_run(c.get('caption', ''))

                # Hashtags extra sugeridos
                doc.add_heading("#️⃣ Hashtags sugeridos por plataforma", level=2)
                palabras = idea.get('palabras_clave', [])[:3]
                extra = [f"#{p.capitalize()}" for p in palabras if len(p) > 3]

                tabla = doc.add_table(rows=4, cols=2)
                tabla.style = "Light Grid Accent 1"
                tabla.rows[0].cells[0].text = "Plataforma"
                tabla.rows[0].cells[1].text = "Hashtags"
                tabla.rows[1].cells[0].text = "TikTok"
                tabla.rows[1].cells[1].text = ' '.join(self.HASHTAGS_BASE[:3] + self.HASHTAGS_HUMOR[:2] + extra)
                tabla.rows[2].cells[0].text = "Instagram Reels"
                tabla.rows[2].cells[1].text = ' '.join(self.HASHTAGS_BASE + extra)
                tabla.rows[3].cells[0].text = "YouTube Shorts"
                tabla.rows[3].cells[1].text = ' '.join(self.HASHTAGS_BASE[:2] + ['#Shorts'] + extra)

                doc.add_paragraph()
                doc.add_page_break()

            # Guardar junto a los videos para que todo quede en una carpeta
            doc_path = self.output_dir / f"GUIA_PUBLICACION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            doc.save(str(doc_path))

            self.logger.info(f"✅ Documento generado: {doc_path.name}")
            return {'status': 'success', 'doc_path': str(doc_path), 'doc_filename': doc_path.name}

        except Exception as e:
            self.logger.error(f"❌ Error generando documento: {e}")
            return {'status': 'error', 'error': str(e), 'doc_path': None}
