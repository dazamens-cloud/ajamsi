"""
Script de prueba para procesar una noticia de Rosalía
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

# Crear noticia de prueba sobre Rosalía
noticia_rosalia = Noticia(
    titulo="Rosalía anuncia nuevo álbum y regresa a Canarias para concierto",
    url="https://example.com/rosalia-concierto",
    fuente="Canarias7",
    contenido="""La cantante Rosalía ha confirmado que lanzará nuevo álbum el próximo trimestre.
    Además, anunció que realizará una gira especial por Canarias con conciertos exclusivos en Las Palmas y Santa Cruz de Tenerife.
    Los fans canarios están emocionados por su regreso a las islas después de 3 años.""",
    fecha_publicacion=datetime.now().strftime("%Y-%m-%d"),
    relevancia_score=0.95
)

print("=" * 60)
print("🎤 PROCESANDO NOTICIA DE ROSALÍA CON AJAMSI")
print("=" * 60)
print(f"\n📰 Noticia: {noticia_rosalia.titulo}")
print(f"📍 Fuente: {noticia_rosalia.fuente}")
print(f"📝 Contenido: {noticia_rosalia.contenido[:100]}...\n")

# Inicializar generador de ideas
print("🤖 Generando ideas con Qwen/Ollama...")
generador = OllamaIdeaGenerator(config)

# Generar 3 ideas
ideas = generador.generar_ideas(noticia_rosalia, num_ideas=3)

print(f"\n✅ Se generaron {len(ideas)} ideas:\n")

for i, idea in enumerate(ideas, 1):
    print(f"💡 IDEA {i}: {idea.titulo}")
    print(f"   Concepto: {idea.concepto}")
    print(f"   Ángulo: {idea.angulo_humor}")
    print(f"   Elementos locales: {', '.join(idea.elementos_locales)}")
    print(f"   Colores: {', '.join(idea.colores)}")
    print()

print("=" * 60)
print("✅ Procesamiento completado")
print("=" * 60)
