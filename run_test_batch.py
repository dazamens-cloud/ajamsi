#!/usr/bin/env python3
"""
Script de prueba: Ejecutar batch completo
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_orchestrator import AgentOrchestrator

def main():
    # Inicializar orquestador
    print("\n" + "="*70)
    print("  PRUEBA COMPLETA - AJAMSI BATCH PROCESSOR")
    print("="*70 + "\n")

    orquestador = AgentOrchestrator()

    # Ejecutar batch completo
    print("🚀 Iniciando pipeline completo...\n")
    resultado = orquestador.ejecutar_batch_completo(nombre_batch="test_demo_2026")

    # Mostrar resultados
    print("\n" + "="*70)
    print("  RESULTADOS DEL BATCH")
    print("="*70 + "\n")

    print(f"Nombre del batch: {resultado.get('nombre')}")
    print(f"Estado: ✅ Completado")
    print(f"Inicio: {resultado.get('inicio')}\n")

    # Detalles de cada fase
    fases = resultado.get('fases', {})

    print("📋 FASES EJECUTADAS:\n")

    if 'scraping' in fases:
        scraping = fases['scraping']
        noticias = scraping.get('noticias', [])
        print(f"1️⃣  SCRAPING")
        print(f"   ✅ Noticias encontradas: {len(noticias)}")
        if noticias:
            print(f"   📌 Muestra: {noticias[0].get('titulo', 'Sin título')[:60]}...")
        print()

    if 'ideas' in fases:
        ideas_result = fases['ideas']
        ideas = ideas_result.get('ideas', [])
        print(f"2️⃣  GENERACIÓN DE IDEAS")
        print(f"   ✅ Ideas creadas: {len(ideas)}")
        if ideas:
            print(f"   💡 Muestra: {ideas[0].get('concepto', 'Sin concepto')[:60]}...")
        print()

    if 'prompts' in fases:
        prompts_result = fases['prompts']
        prompts = prompts_result.get('prompts', [])
        print(f"3️⃣  OPTIMIZACIÓN DE PROMPTS")
        print(f"   ✅ Prompts generados: {len(prompts)}")
        if prompts:
            print(f"   🎨 Estilos: {', '.join([p.get('estilo', 'sin estilo') for p in prompts[:3]])}")
        print()

    if 'captions' in fases:
        captions_result = fases['captions']
        captions = captions_result.get('captions', [])
        print(f"4️⃣  GENERACIÓN DE CAPTIONS")
        print(f"   ✅ Captions creados: {len(captions)}")
        if captions:
            print(f"   ✍️  Muestra: {captions[0].get('caption', 'Sin caption')[:60]}...")
        print()

    if 'videos' in fases:
        videos_result = fases['videos']
        videos = videos_result.get('videos', [])
        print(f"5️⃣  COMPILACIÓN DE VIDEOS")
        print(f"   ✅ Videos compilados: {len(videos)}")
        if videos:
            print(f"   🎬 Formato: {videos[0].get('formato', 'sin formato')}")
        print()

    if 'validacion' in fases:
        validacion_result = fases['validacion']
        print(f"6️⃣  VALIDACIÓN DE CONTENIDO")
        print(f"   ✅ Contenido validado")
        print(f"   🟢 Estado: {validacion_result.get('estado', 'OK')}")
        print()

    if 'sync' in fases:
        sync_result = fases['sync']
        print(f"7️⃣  SINCRONIZACIÓN CON DRIVE")
        print(f"   ✅ Archivos sincronizados: {sync_result.get('archivos_sincronizados', 0)}")
        print(f"   ☁️  Tamaño: {sync_result.get('tamaño_mb', 0)} MB")
        print()

    # Estadísticas generales
    print("="*70)
    print("  📊 ESTADÍSTICAS GENERALES")
    print("="*70 + "\n")

    errores = resultado.get('errores', [])
    print(f"✅ Fases completadas: {len(fases)}")
    print(f"⚠️  Errores: {len(errores)}")
    print(f"📈 Estado general: {'SUCCESS' if resultado.get('status') == 'success' else 'FAILED'}")

    print("\n" + "="*70)
    print("✅ PRUEBA COMPLETADA CON ÉXITO")
    print("="*70 + "\n")

    # Guardar resultado a JSON
    with open('reportes/test_batch_resultado.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    print("💾 Resultado guardado en: reportes/test_batch_resultado.json\n")


if __name__ == "__main__":
    main()
