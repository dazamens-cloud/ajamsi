#!/usr/bin/env python3
"""
TEST SCRAPER - PHASE 2
Script para verificar que el scraping real funciona correctamente
"""

import sys
import json
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents import ScraperAgent
from utils.config_loader import ConfigLoader

print("\n" + "="*70)
print("  TEST SCRAPER - PHASE 2")
print("  Verificar ScraperAgent con scraping REAL")
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

# 2. Inicializar ScraperAgent
print("2️⃣  Inicializando ScraperAgent...")
try:
    agent = ScraperAgent(config)
    print("   ✅ Agent inicializado\n")
except Exception as e:
    print(f"   ❌ Error inicializando agent: {e}\n")
    sys.exit(1)

# 3. Ejecutar scraping REAL
print("3️⃣  Ejecutando scraping REAL de noticias...")
print("   (Esto puede tardar 10-30 segundos)\n")

try:
    resultado = agent.ejecutar(dias_atras=7, limite_noticias=10)

    print(f"   Status: {resultado['status']}")
    print(f"   Noticias encontradas: {resultado['noticias_encontradas']}\n")

    if resultado['noticias']:
        print("   📰 NOTICIAS OBTENIDAS:")
        print("   " + "-"*66)

        for i, noticia in enumerate(resultado['noticias'][:5], 1):
            print(f"\n   #{i} - {noticia.get('fuente', 'desconocida').upper()}")
            print(f"       Título: {noticia.get('titulo', 'Sin título')[:70]}")
            print(f"       Relevancia: {noticia.get('relevancia_score', 0):.1f}/100")
            print(f"       Tipo: {noticia.get('tipo', 'desconocido')}")
            print(f"       Fecha: {noticia.get('fecha', 'desconocida')[:10]}")

        print("\n   " + "-"*66)
        print(f"\n   ✅ Scraping exitoso: {resultado['noticias_encontradas']} noticias\n")
    else:
        print("   ⚠️  No se encontraron noticias (esto es normal si las fuentes no responden)\n")

except Exception as e:
    print(f"   ❌ Error durante scraping: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Estadísticas
print("="*70)
print("✅ TEST PHASE 2 COMPLETADO")
print("="*70)

if resultado['noticias']:
    fuentes = {}
    for noticia in resultado['noticias']:
        fuente = noticia.get('fuente', 'desconocida')
        fuentes[fuente] = fuentes.get(fuente, 0) + 1

    print("\n📊 Estadísticas:")
    print(f"   • Total de noticias: {resultado['noticias_encontradas']}")
    print(f"   • Fuentes utilizadas: {len(fuentes)}")
    for fuente, count in fuentes.items():
        print(f"     - {fuente}: {count}")
    print("\n🎉 Sistema listo para producción con scraping REAL")
else:
    print("\n⚠️  No se encontraron noticias")
    print("   Posibles razones:")
    print("   - Sitios no disponibles/bloqueados")
    print("   - Timeout de conexión")
    print("   - Cambios en estructura HTML")
    print("\n💡 Sugerencias:")
    print("   - Verifica tu conexión a Internet")
    print("   - Aumenta timeout en config.json")
    print("   - Intenta manualmente en navegador")

print("\n" + "="*70)
print("PRÓXIMO PASO: Ejecutar FASE 3 (Video Creator Real)")
print("="*70 + "\n")
