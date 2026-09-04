#!/usr/bin/env python3
"""
TEST OLLAMA PHASE 1
Script para verificar que Ollama está configurado correctamente
y que OllamaPromptEngineerAgent funciona.
"""

import sys
import json
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents import OllamaPromptEngineerAgent
from utils.config_loader import ConfigLoader

print("\n" + "="*70)
print("  TEST OLLAMA - PHASE 1")
print("  Verificar OllamaPromptEngineerAgent")
print("="*70 + "\n")

# 1. Cargar configuración
print("1️⃣  Cargando configuración...")
try:
    config_loader = ConfigLoader("config/config.json")
    config = config_loader.to_dict()
    print("   ✅ Config cargada correctamente\n")
except Exception as e:
    print(f"   ❌ Error cargando config: {e}\n")
    sys.exit(1)

# 2. Inicializar OllamaPromptEngineerAgent
print("2️⃣  Inicializando OllamaPromptEngineerAgent...")
try:
    agent = OllamaPromptEngineerAgent(config)
    print("   ✅ Agent inicializado\n")
except Exception as e:
    print(f"   ❌ Error inicializando agent: {e}\n")
    sys.exit(1)

# 3. Verificar estado de Ollama
print("3️⃣  Verificando disponibilidad de Ollama...")
estado = agent.obtener_estado()
print(f"   Ollama URL: {estado['ollama_url']}")
print(f"   Modelo: {estado['modelo']}")
print(f"   Disponible: {estado['ollama_disponible']}")

if estado['ollama_disponible']:
    print("   ✅ Ollama está disponible\n")
else:
    print("   ⚠️  Ollama NO está disponible")
    print("   Pero el agent puede usar prompts fallback\n")

# 4. Crear idea de prueba
print("4️⃣  Creando idea de prueba...")
idea_prueba = {
    'concepto': 'Un canario sorprendido viendo las noticias',
    'palabras_clave': ['Lanzarote', 'sorpresa', 'noticia'],
    'angulo_humor': 'sarcasmo',
}
print(f"   Concepto: {idea_prueba['concepto']}\n")

# 5. Generar prompts
print("5️⃣  Generando prompts con OllamaPromptEngineerAgent...")
try:
    resultado = agent.ejecutar(idea_prueba, num_prompts=2)

    print(f"\n   Status: {resultado['status']}")
    print(f"   Generador: {resultado.get('generador', 'desconocido')}")
    print(f"   Prompts generados: {resultado['prompts_generados']}\n")

    # Mostrar prompts generados
    for prompt in resultado['prompts']:
        print(f"   📝 PROMPT #{prompt['numero']} - Estilo: {prompt['estilo']}")
        print(f"      " + "-"*60)
        print(f"      {prompt['prompt_text'][:200]}...")
        print()

    print("   ✅ Prompts generados exitosamente\n")

except Exception as e:
    print(f"   ❌ Error generando prompts: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 6. Resumen
print("="*70)
print("✅ TEST PHASE 1 COMPLETADO")
print("="*70)
print("\n📊 Resumen:")
print(f"   • Agent inicializado: ✅")
print(f"   • Ollama disponible: {'✅' if estado['ollama_disponible'] else '⚠️  (Usando fallback)'}")
print(f"   • Generación de prompts: ✅")
print(f"   • Prompts generados: {resultado['prompts_generados']}")

if estado['ollama_disponible']:
    print("\n🎉 Sistema listo para producción con Ollama")
else:
    print("\n⚠️  Sistema funcionando con fallback (instala Ollama para máximo rendimiento)")

print("\n" + "="*70)
print("PRÓXIMO PASO: Ejecutar FASE 2 (Scraper Real)")
print("="*70 + "\n")
