"""
Generar Reporte Word Profesional - IDEA 1: Reacción Sorprendida
Noticia: Rosalía regala 1.000 euros a fan
"""

import sys
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Crear documento
doc = Document()

# Estilo: Agregar tabla de estilos
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# ════════════════════════════════════════════════════════════
# PORTADA
# ════════════════════════════════════════════════════════════

titulo = doc.add_paragraph()
titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
titulo_run = titulo.add_run("🎬 STORYBOARD & GUIÓN TÉCNICO")
titulo_run.font.size = Pt(28)
titulo_run.font.bold = True
titulo_run.font.color.rgb = RGBColor(255, 215, 0)  # Dorado

subtitulo = doc.add_paragraph()
subtitulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
subtitulo_run = subtitulo.add_run("IDEA 1: REACCIÓN SORPRENDIDA")
subtitulo_run.font.size = Pt(20)
subtitulo_run.font.bold = True
subtitulo_run.font.color.rgb = RGBColor(255, 107, 107)  # Rojo coral

noticia_titulo = doc.add_paragraph()
noticia_titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
noticia_titulo_run = noticia_titulo.add_run("Rosalía sorprende con 1.000 euros a un fan")
noticia_titulo_run.font.size = Pt(14)
noticia_titulo_run.font.italic = True

doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
info_run = info.add_run("Fuente: Canarias7 | Canal: @hummorkana\n")
info_run.font.size = Pt(11)
info_run2 = info.add_run(f"Generado: {datetime.now().strftime('%d de %B de %Y a las %H:%M')}\n")
info_run2.font.size = Pt(10)
info_run2.font.italic = True
info_run3 = info.add_run("Generado con AjamSi - Sistema de Generación Automática de Contenido TikTok")
info_run3.font.size = Pt(9)
info_run3.font.color.rgb = RGBColor(128, 128, 128)

# Salto de página
doc.add_page_break()

# ════════════════════════════════════════════════════════════
# INFORMACIÓN GENERAL
# ════════════════════════════════════════════════════════════

doc.add_heading('📝 INFORMACIÓN GENERAL', level=1)

tabla_info = doc.add_table(rows=7, cols=2)
tabla_info.style = 'Light Grid Accent 1'

datos = [
    ("Título", "Reacción Sorprendida"),
    ("Ángulo Humorístico", "Sarcasmo"),
    ("Personaje Principal", "El Típico Canario"),
    ("Duración", "15 segundos"),
    ("Resolución", "1080x1920 (9:16 TikTok)"),
    ("FPS", "30 fps"),
    ("Formato", "Video Vertical")
]

for i, (clave, valor) in enumerate(datos):
    tabla_info.rows[i].cells[0].text = clave
    tabla_info.rows[i].cells[1].text = valor
    tabla_info.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

# ════════════════════════════════════════════════════════════
# CONCEPTO CREATIVO
# ════════════════════════════════════════════════════════════

doc.add_heading('💡 CONCEPTO CREATIVO', level=1)

concepto_p = doc.add_paragraph()
concepto_p.add_run("Concepto Base: ").bold = True
concepto_p.add_run("Cara de sorpresa ante la noticia de los 1.000 euros que Rosalía regaló a un fan.")

doc.add_paragraph("Un video que juega con la emoción del fan que vendía merchandising de Rosalía cuando "
                  "de repente recibe la noticia de que la cantante le ha regalado 1.000 euros. "
                  "El contraste entre la tristeza inicial y la alegría final es el corazón del video.")

# ════════════════════════════════════════════════════════════
# IDENTIDAD VISUAL
# ════════════════════════════════════════════════════════════

doc.add_heading('🎨 IDENTIDAD VISUAL', level=1)

doc.add_heading('Paleta de Colores', level=2)

tabla_colores = doc.add_table(rows=4, cols=2)
tabla_colores.style = 'Light Grid Accent 1'

colores = [
    ("Color Primario", "DORADO (#FFD700) - Dinero, éxito, celebración"),
    ("Color Secundario", "ROJO CORAL (#FF6347) - Energía, emoción"),
    ("Color Terciario", "BLANCO (#FFFFFF) - Limpieza, claridad"),
]

for i, (tipo, desc) in enumerate(colores):
    tabla_colores.rows[i].cells[0].text = tipo
    tabla_colores.rows[i].cells[1].text = desc
    tabla_colores.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True

doc.add_heading('Elementos Canarios', level=2)

for elemento in ["🏝️ Playa de Lanzarote", "🌊 Mar turquesa", "🚩 Bandera de Canarias"]:
    doc.add_paragraph(elemento, style='List Bullet')

# ════════════════════════════════════════════════════════════
# GUIÓN TÉCNICO - 15 SEGUNDOS
# ════════════════════════════════════════════════════════════

doc.add_page_break()
doc.add_heading('📱 GUIÓN TÉCNICO - 15 SEGUNDOS', level=1)

# ESCENA 1
doc.add_heading('ESCENA 1 (0-5 segundos) - BEFORE: LA TRISTEZA', level=2)

escena1_data = [
    ("Plano", "Close-up del 'Típico Canario'"),
    ("Acción", "Vendiendo merchandising de Rosalía en la playa"),
    ("Expresión", "Triste, desesperado"),
    ("Fondo", "Playa de Lanzarote + Bandera de Canarias"),
    ("Sonido", "Música melancólica en fondo"),
    ("Texto en Pantalla", "\"Vendiendo merch para cumplir mi sueño 😭\""),
    ("Duración", "5 segundos"),
]

t1 = doc.add_table(rows=len(escena1_data), cols=2)
t1.style = 'Light Grid Accent 1'
for i, (clave, valor) in enumerate(escena1_data):
    t1.rows[i].cells[0].text = clave
    t1.rows[i].cells[1].text = valor

# ESCENA 2
doc.add_heading('ESCENA 2 (5-8 segundos) - EL TWIST: ¡LA SORPRESA!', level=2)

escena2_data = [
    ("Plano", "Transición rápida"),
    ("Acción", "Recibe la noticia en el teléfono/redes sociales"),
    ("Expresión", "SORPRESA MÁXIMA (ojos abiertos, boca abierta)"),
    ("Efecto Visual", "Zoom de cámara rápido"),
    ("Sonido", "Efecto de sorpresa (ding, wow)"),
    ("Texto en Pantalla", "\"¡Rosalía me regala 1.000€! 😱💰\""),
    ("Música", "Cambio a música alegre/épica"),
    ("Duración", "3 segundos"),
]

t2 = doc.add_table(rows=len(escena2_data), cols=2)
t2.style = 'Light Grid Accent 1'
for i, (clave, valor) in enumerate(escena2_data):
    t2.rows[i].cells[0].text = clave
    t2.rows[i].cells[1].text = valor

# ESCENA 3
doc.add_heading('ESCENA 3 (8-15 segundos) - AFTER: ¡LA CELEBRACIÓN!', level=2)

escena3_data = [
    ("Plano", "Wide shot - El personaje saltando de alegría"),
    ("Acción", "Celebración con dinero cayendo (efecto visual)"),
    ("Expresión", "Felicidad absoluta"),
    ("Fondo", "Playa turquesa + Bandera canaria ondeando"),
    ("Efectos", "Confeti, dinero cayendo, luz dorada"),
    ("Sonido", "Música celebratoria"),
    ("Texto en Pantalla", "\"¡Cuando Rosalía es una REINA! 👑💛\""),
    ("Transición", "Fade out con logo @hummorkana"),
    ("Duración", "7 segundos"),
]

t3 = doc.add_table(rows=len(escena3_data), cols=2)
t3.style = 'Light Grid Accent 1'
for i, (clave, valor) in enumerate(escena3_data):
    t3.rows[i].cells[0].text = clave
    t3.rows[i].cells[1].text = valor

# ════════════════════════════════════════════════════════════
# OPCIONES DE MÚSICA
# ════════════════════════════════════════════════════════════

doc.add_page_break()
doc.add_heading('🎵 OPCIONES DE AUDIO', level=1)

doc.add_heading('Opción 1: "Que Siga La Música" - Rosalía (RECOMENDADO)', level=2)
doc.add_paragraph("Uso de música viral de Rosalía. Aprovecha el trending y la identificación "
                  "con la artista. Máximo impacto viral.")

doc.add_heading('Opción 2: Sonido de Sorpresa + Efecto Dinero', level=2)
doc.add_paragraph("Sonidos humorísticos sin música vocal. Genera más comedia y énfasis en la reacción.")

doc.add_heading('Opción 3: Música Inspiradora Canaria', level=2)
doc.add_paragraph("Sonido folclórico canario. Refuerza identidad local pero menor alcance viral.")

# ════════════════════════════════════════════════════════════
# DETALLES DE PRODUCCIÓN
# ════════════════════════════════════════════════════════════

doc.add_page_break()
doc.add_heading('📸 DETALLES DE PRODUCCIÓN', level=1)

doc.add_heading('Locación', level=2)
doc.add_paragraph("Playa de Lanzarote (preferiblemente con volcanes de fondo)")
doc.add_paragraph("Hora de grabación: Atardecer (5-7 PM) - Luz dorada natural")
doc.add_paragraph("Clima: Despejado, mar tranquilo")

doc.add_heading('Vestuario', level=2)
doc.add_paragraph("'El Típico Canario' con traje tradicional canario")
doc.add_paragraph("Detalles: Pañuelo, sombrilla, chanclas típicas")
doc.add_paragraph("Maquillaje: Expresión exagerada para comedia")

doc.add_heading('Equipamiento', level=2)
equip = ["📹 Cámara (4K mínimo)", "🎤 Micrófono externo", "💡 Iluminación (reflectores)",
         "🎬 Estabilizador/Trípode", "💻 Computadora para edición"]
for item in equip:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('Efectos Visuales', level=2)
efectos = ["Transición rápida entre escenas (CORTE SECO)",
          "Efectos de dinero cayendo (stock footage)",
          "Confeti/explosión de confeti",
          "Zoom rápido en la cara de sorpresa",
          "Color grading vibrante (colores saturados)"]
for efecto in efectos:
    doc.add_paragraph(efecto, style='List Bullet')

# ════════════════════════════════════════════════════════════
# ANÁLISIS VIRAL
# ════════════════════════════════════════════════════════════

doc.add_page_break()
doc.add_heading('📊 ANÁLISIS DE VIRALIDAD', level=1)

doc.add_heading('Elementos Virales', level=2)

elementos_virales = [
    ("✅", "Sorpresa emocional - Pico de emoción garantizado"),
    ("✅", "Personaje reconocible - 'Típico Canario' ya conocido"),
    ("✅", "Actualidad - Noticia trending (Rosalía + dinero)"),
    ("✅", "Humor sarcástico - Relatable para audiencia canaria"),
    ("✅", "Elementos canarios - Comunidad local se identifica"),
    ("✅", "Música viral - Canción trending"),
    ("✅", "Duración perfecta - 15 segundos = TikTok ideal"),
]

t_viral = doc.add_table(rows=len(elementos_virales), cols=2)
t_viral.style = 'Light Grid Accent 1'
for i, (marca, desc) in enumerate(elementos_virales):
    t_viral.rows[i].cells[0].text = marca
    t_viral.rows[i].cells[1].text = desc

doc.add_heading('Target Audience', level=2)

target = [
    ("Edad", "13-35 años (TikTok main audience)"),
    ("Localización", "Canarias (trending nacional/España)"),
    ("Intereses", "Música, celebrities, humor local"),
    ("Plataformas", "TikTok, Instagram Reels, YouTube Shorts"),
    ("Dispositivo", "Móvil (vertical)"),
]

t_target = doc.add_table(rows=len(target), cols=2)
t_target.style = 'Light Grid Accent 1'
for i, (tipo, desc) in enumerate(target):
    t_target.rows[i].cells[0].text = tipo
    t_target.rows[i].cells[1].text = desc

# ════════════════════════════════════════════════════════════
# HASHTAGS Y DISTRIBUCIÓN
# ════════════════════════════════════════════════════════════

doc.add_heading('#️⃣ HASHTAGS SUGERIDOS', level=1)

hashtags = "#Rosalía #Canarias #SorpresaSorprendida #TípicosCanarios #ViralTikTok #LaRosaLía #LanzaroteComoTúLaAmas #@hummorkana"
ht_p = doc.add_paragraph(hashtags)
ht_p.runs[0].font.italic = True
ht_p.runs[0].font.color.rgb = RGBColor(0, 100, 200)

doc.add_heading('📱 DISTRIBUCIÓN MULTICANAL', level=1)

canales = [
    ("TikTok", "Publicar 3-8 PM hora canaria (peak hours)"),
    ("Instagram Reels", "Publicar simultáneamente"),
    ("YouTube Shorts", "Publicar en canal"),
    ("Twitter", "Compartir enlace + context"),
    ("Email Community", "Newsletter con BTS (behind the scenes)"),
]

for canal, accion in canales:
    p = doc.add_paragraph(f"{canal}: {accion}", style='List Bullet')

# ════════════════════════════════════════════════════════════
# CHECKLIST
# ════════════════════════════════════════════════════════════

doc.add_page_break()
doc.add_heading('✅ CHECKLIST DE PRODUCCIÓN', level=1)

doc.add_heading('ANTES DE GRABAR', level=2)
before = ["☐ Scout de locación en playa", "☐ Obtener permisos necesarios",
         "☐ Verificar equipamiento", "☐ Vestuario y maquillaje preparados",
         "☐ Descargar efectos visuales", "☐ Música/sonido listo",
         "☐ Storyboard impreso para referencia"]
for item in before:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('DURANTE LA GRABACIÓN', level=2)
during = ["☐ Grabar mínimo 5 takes de cada escena", "☐ Múltiples ángulos (close-up, wide, medio)",
         "☐ B-roll de playa/volcanes", "☐ Capturar expresiones auténticas",
         "☐ Grabar sin audio (agregar después)", "☐ Verificar iluminación"]
for item in during:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('DESPUÉS DE GRABAR', level=2)
after = ["☐ Transferir archivos a computadora", "☐ Organizar by escena/ángulo",
        "☐ Crear proyecto en Adobe Premiere/DaVinci", "☐ Editar secuencia principal",
        "☐ Agregar transiciones y efectos", "☐ Aplicar color grading",
        "☐ Agregar efectos de dinero/confeti", "☐ Sincronizar con música",
        "☐ Agregar captions y textos", "☐ Exportar 1080x1920 @30fps"]
for item in after:
    doc.add_paragraph(item, style='List Bullet')

doc.add_heading('POST-PUBLICACIÓN', level=2)
post = ["☐ Publicar en TikTok (3-8 PM)", "☐ Publicar en Instagram Reels",
       "☐ Publicar en YouTube Shorts", "☐ Responder comentarios activamente",
       "☐ Analizar métricas (views, likes, shares)", "☐ Crear videos compilados de reacciones",
       "☐ Ajustar estrategia según engagement"]
for item in post:
    doc.add_paragraph(item, style='List Bullet')

# ════════════════════════════════════════════════════════════
# CONCLUSIÓN
# ════════════════════════════════════════════════════════════

doc.add_page_break()

conclusion = doc.add_paragraph()
conclusion.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
conclusion_run = conclusion.add_run("🎬 LISTO PARA PRODUCCIÓN 🎬")
conclusion_run.font.size = Pt(16)
conclusion_run.font.bold = True
conclusion_run.font.color.rgb = RGBColor(255, 107, 107)

final = doc.add_paragraph()
final.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
final_text = final.add_run(
    "Este storyboard ha sido generado automáticamente por AjamSi,\n"
    "sistema de generación automática de contenido TikTok.\n\n"
    "Basado en análisis de: Noticia Rosalía (Canarias7)\n"
    "Tema: Rosalía sorprende con 1.000 euros a fan\n\n"
    f"Generado: {datetime.now().strftime('%d de %B de %Y')}\n"
    "Canal: @hummorkana"
)
final_text.font.size = Pt(10)
final_text.font.italic = True
final_text.font.color.rgb = RGBColor(128, 128, 128)

# Guardar documento
output_path = f"reportes/IDEA_1_Rosalia_Reaccion_Sorprendida_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
Path("reportes").mkdir(exist_ok=True)
doc.save(output_path)

print(f"\n✅ Reporte profesional generado:")
print(f"📄 {output_path}")
print(f"\n📊 Documento incluye:")
print(f"   ✓ Storyboard completo (3 escenas)")
print(f"   ✓ Guión técnico detallado")
print(f"   ✓ Especificaciones de producción")
print(f"   ✓ Análisis de viralidad")
print(f"   ✓ Checklist de producción")
print(f"   ✓ Hashtags y distribución")
print(f"\n🎬 Listo para compartir con el equipo de producción")
