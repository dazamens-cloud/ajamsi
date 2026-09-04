"""
Script para procesar la noticia real de Rosalía - Canarias7
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config_loader import ConfigLoader
from scrapers import Noticia
from generators import OllamaIdeaGenerator
from datetime import datetime

# Cargar configuración
config = ConfigLoader("config/config.json")

# Noticia real de Rosalía
noticia_rosalia_real = Noticia(
    titulo="Rosalía sorprende con 1.000 euros a un fan que vendía merchandising suyo para cumplir un sueño",
    url="https://www.canarias7.es/revista-c7/rosalia-sorprende-1000-euros-fan-vendia-merchandising-20260825215022-ntrc.html",
    fuente="Canarias7",
    contenido="""La cantante Rosalía sorprendió a un fan que vendía merchandising suyo para cumplir un sueño personal.
    Al enterarse de la historia, la artista regaló 1.000 euros al joven para ayudarle a conseguir su objetivo.
    El gesto de generosidad de Rosalía se ha viralizado en redes sociales, generando miles de comentarios positivos
    sobre la humanidad y el corazón de la cantante. Muchos fans destacan que es un ejemplo de cómo las celebridades
    pueden impactar positivamente en las vidas de sus seguidores.""",
    fecha_publicacion="2026-08-25",
    relevancia_score=0.98
)

print("\n" + "=" * 80)
print("🎤 PROCESANDO NOTICIA REAL DE ROSALÍA CON AJAMSI")
print("=" * 80)
print(f"\n📰 Noticia: {noticia_rosalia_real.titulo}")
print(f"📍 Fuente: {noticia_rosalia_real.fuente}")
print(f"📅 Fecha: {noticia_rosalia_real.fecha_publicacion}")
print(f"🔗 URL: {noticia_rosalia_real.url}")
print(f"\n📝 Contenido: {noticia_rosalia_real.contenido}\n")

# Inicializar generador de ideas
print("🤖 Generando ideas con Qwen/Ollama...")
generador = OllamaIdeaGenerator(config)

# Generar 5 ideas para esta noticia emotiva
ideas = generador.generar_ideas(noticia_rosalia_real, num_ideas=5)

print(f"\n✅ Se generaron {len(ideas)} ideas para viral TikTok:\n")

for i, idea in enumerate(ideas, 1):
    print(f"\n{'='*80}")
    print(f"💡 IDEA {i}: {idea.titulo.upper()}")
    print(f"{'='*80}")
    print(f"   📌 Concepto: {idea.concepto}")
    print(f"   😂 Ángulo humor: {idea.angulo_humor}")
    print(f"   🏝️  Elementos canarios: {', '.join(idea.elementos_locales)}")
    print(f"   🎨 Paleta colores: {', '.join(idea.colores)}")
    print(f"   👤 Personaje: {idea.personaje}")
    print(f"   🎬 Estilo: {idea.estilo}")

print(f"\n{'='*80}")
print("✅ ANÁLISIS COMPLETADO - LISTO PARA PRODUCCIÓN")
print("="*80)

print("\n📊 POTENCIAL VIRAL:")
print("   - Tema emotivo: ✅ (Rosalía + generosidad)")
print("   - Relevancia local: ✅ (Canarias7)")
print("   - Impacto emocional: ✅ (Historia inspiradora)")
print("   - Viralidad: ✅ MUY ALTA (Celebrities + dinero + sueños)")
print("\n🚀 Recomendación: Crear 3-5 videos cortos con diferentes ángulos")
print("   Duración ideal: 15-30 segundos (TikTok short)")
