"""
Desarrollo completo de IDEA 1: Reacción Sorprendida
Noticia: Rosalía regalo 1.000 euros a fan
"""

import sys
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config_loader import ConfigLoader
from generators import Idea

# Cargar configuración
config = ConfigLoader("config/config.json")

# Crear la idea desarrollada
idea_reaccion = Idea(
    titulo="Reacción Sorprendida",
    noticia_id="rosalia-1000-euros-fan",
    concepto="Cara de sorpresa ante la noticia de los 1.000 euros",
    angulo_humor="sarcasmo",
    personaje="El Típico Canario",
    estilo="canario_moderno",
    colores=["#FFD700", "#FF6347", "#FFFFFF"],  # Dorado, Rojo coral, Blanco
    elementos_locales=["Bandera de Canarias", "Playa de Lanzarote", "Mar turquesa"],
    prompts_sugeridos=[
        "Expresión de shock cuando Rosalía regala 1.000 euros",
        "Transición rápida de tristeza a alegría",
        "Efecto de dinero cayendo del cielo"
    ]
)

print("\n" + "="*90)
print("🎬 STORYBOARD - IDEA 1: REACCIÓN SORPRENDIDA")
print("="*90)

print(f"""
📝 INFORMACIÓN GENERAL:
   Título: {idea_reaccion.titulo}
   Ángulo: {idea_reaccion.angulo_humor.upper()}
   Personaje: {idea_reaccion.personaje}
   Estilo: {idea_reaccion.estilo}
   Duración: 15 segundos

📌 CONCEPTO:
   {idea_reaccion.concepto}

🎨 IDENTIDAD VISUAL:
   Colores principales: {', '.join(idea_reaccion.colores)}
   - Dorado (#FFD700): Dinero, éxito, celebración
   - Rojo coral (#FF6347): Energía, emoción
   - Blanco (#FFFFFF): Limpieza, claridad

🏝️ ELEMENTOS CANARIOS:
   {chr(10).join(f'   - {el}' for el in idea_reaccion.elementos_locales)}

{"="*90}
📱 GUIÓN TÉCNICO - 15 SEGUNDOS
{"="*90}

ESCENA 1 (0-5 segundos) - BEFORE: LA TRISTEZA
─────────────────────────────────────────────
   Plano: Close-up del "Típico Canario"
   Acción: Vendiendo merchandising de Rosalía en la playa
   Expresión: Triste, desesperado
   Fondo: Playa de Lanzarote, bandera de Canarias
   Sonido: Música melancólica en fondo
   Texto en pantalla: "Vendiendo merch para cumplir mi sueño 😭"
   Música: Sonido triste/nostálgico

ESCENA 2 (5-8 segundos) - EL TWIST: LA NOTICIA
───────────────────────────────────────────────
   Plano: Transición rápida
   Acción: Recibe la noticia (teléfono/redes sociales)
   Expresión: SORPRESA MÁXIMA (ojos abiertos, boca abierta)
   Efecto: Zoom de cámara rápido
   Sonido: Sonido de sorpresa (ding, wow)
   Texto en pantalla: "Rosalía me regala 1.000€ 😱💰"
   Música: Cambio a música alegre/épica

ESCENA 3 (8-15 segundos) - AFTER: LA ALEGRÍA
─────────────────────────────────────────────
   Plano: Wide shot - El personaje saltando de alegría
   Acción: Celebración con dinero cayendo (efecto)
   Expresión: Felicidad absoluta
   Fondo: Playa turquesa, bandera canaria ondeando
   Efectos: Confeti, dinero cayendo, luz dorada
   Sonido: Música celebratoria
   Texto en pantalla: "Cuando Rosalía es una REINA 👑💛"
   Transición: Fade out con logo de @hummorkana

{"="*90}
🎵 SUGERENCIAS DE AUDIO
{"="*90}

Opción 1 (VIRAL): "Que Siga La Música" - Rosalía remix
Opción 2 (HUMOR): Sonido de sorpresa + efecto dinero
Opción 3 (EMOCIONAL): Música inspiradora canaria

{"="*90}
📸 DETALLES DE PRODUCCIÓN
{"="*90}

VESTUARIO:
   - "El Típico Canario" con traje tradicional canario
   - Detalles: Pañuelo, sombrilla, chanclas típicas
   - Maquillaje: Expresión exagerada (comedia)

LOCACIÓN:
   - Playa de Lanzarote (preferiblemente con volcanes)
   - Hora: Atardecer (luz dorada natural)
   - Accesorio: Bandera de Canarias

EFECTOS VISUALES:
   - Transición rápida entre scenes (CORTE SECO)
   - Efectos de dinero cayendo (stock footage)
   - Confeti/efectos de celebración
   - Zoom rápido en la cara de sorpresa

DURACIÓN VIDEOS:
   - Vertical: 9:16 (TikTok)
   - Resolución: 1080x1920 (Full HD)
   - FPS: 30fps
   - Codec: H.264

{"="*90}
📊 ANÁLISIS DE VIRALIDAD
{"="*90}

ELEMENTOS VIRALES:
   ✅ Sorpresa emocional (pico de emoción)
   ✅ Personaje reconocible (Típico Canario)
   ✅ Actualidad (Rosalía + 1000€)
   ✅ Humor sarcástico (relatable)
   ✅ Elementos canarios (comunidad local)
   ✅ Música viral (Rosalía)
   ✅ Duración corta (15 seg = perfecto TikTok)

TARGETS:
   - Edad: 13-35 años (TikTok main audience)
   - Localización: Canarias (pero viral en España)
   - Intereses: Música, celebrity, humor local
   - Plataformas: TikTok, Instagram Reels, YouTube Shorts

HASHTAGS SUGERIDOS:
   #Rosalía #Canarias #SorpresaSorprendida #TípicosCanarios
   #ViralTikTok #LaRosaLía #LanzaroteComoTúLaAmas

{"="*90}
✅ CHECKLIST DE PRODUCCIÓN
{"="*90}

ANTES DE GRABAR:
   ☐ Scout de locación en playa
   ☐ Permisos necesarios
   ☐ Equipamiento: Cámara, micrófono, luz
   ☐ Vestuario y maquillaje listos
   ☐ Efectos visuales descargados
   ☐ Música/sonido listo
   ☐ Storyboard impreso

DURANTE LA GRABACIÓN:
   ☐ Múltiples takes (al menos 5)
   ☐ Diferentes ángulos (close-up, wide, medio)
   ☐ B-roll de playa/volcán
   ☐ Capturar expresiones auténticas
   ☐ Grabar sin audio (agregamos después)

DESPUÉS DE GRABAR:
   ☐ Editar en Adobe Premiere/DaVinci
   ☐ Agregar transiciones
   ☐ Aplicar color grading (colores vibrantes)
   ☐ Agregar efectos de dinero/confeti
   ☐ Sincronizar con música
   ☐ Agregar captions/textos
   ☐ Exportar en 1080x1920 @30fps

POST-PUBLICACIÓN:
   ☐ Publicar en TikTok (3-8 PM hora canaria)
   ☐ Publicar en Instagram Reels
   ☐ Publicar en YouTube Shorts
   ☐ Responder comentarios
   ☐ Analizar métricas (views, likes, shares)
   ☐ Ajustar según engagement

{"="*90}
🎬 READY FOR PRODUCTION
{"="*90}
""")

# Crear archivo de configuración para el video
config_video = {
    "titulo": idea_reaccion.titulo,
    "duracion_segundos": 15,
    "resolucion": "1080x1920",
    "fps": 30,
    "colores": idea_reaccion.colores,
    "elementos": idea_reaccion.elementos_locales,
    "personaje": idea_reaccion.personaje,
    "estilo": idea_reaccion.estilo
}

print(f"\n📁 Configuración exportada a: config_idea_1_rosalia.json")

import json
with open("config_idea_1_rosalia.json", "w", encoding="utf-8") as f:
    json.dump(config_video, f, indent=2, ensure_ascii=False)

print("✅ Storyboard completado y listo para producción")
print("🎬 Próximo paso: Grabar en Lanzarote")
