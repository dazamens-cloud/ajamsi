"""Test rápido del pipeline completo en local (sin servidor)"""
import sys
import logging
from pathlib import Path

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "src"))
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s: %(message)s')

from agent_orchestrator import AgentOrchestrator

noticia_prueba = {
    'titulo': 'La viticultura heroica canaria se hace con 105 premios mundiales',
    'contenido': 'Los vinos de Canarias han conseguido 105 premios en concursos internacionales este año. '
                 'La viticultura heroica de las islas, cultivada en terrenos volcanicos, sigue sorprendiendo al mundo.',
    'fuente': 'diario_avisos',
    'url': 'https://ejemplo.com/noticia',
}

print("\n=== TEST PIPELINE COMPLETO ===\n")
orq = AgentOrchestrator()

def progreso(pct, paso, detalle):
    print(f"  [{pct:3d}%] {paso} | {detalle}")

resultado = orq.ejecutar_pipeline_completo([noticia_prueba], progreso)

print("\n=== RESULTADO ===")
print(f"Status: {resultado['status']}")
print(f"Videos generados: {resultado['videos_generados']}")
print(f"Documento Word: {resultado['doc_path']}")
if resultado['errores']:
    print(f"Errores: {resultado['errores']}")

for r in resultado['resultados']:
    v = r.get('video') or {}
    print(f"\nVideo: {v.get('video_path')}")
    print(f"  Tamaño: {v.get('tamaño_mb')} MB, Duración: {v.get('duracion_segundos')}s, Audio: {v.get('tiene_audio')}")
