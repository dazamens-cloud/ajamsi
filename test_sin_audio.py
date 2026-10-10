#!/usr/bin/env python3
"""
Test rápido: Verifica que el pipeline genera videos sin audio
"""

import sys
from pathlib import Path

# Windows: evitar crashes de cp1252 al imprimir emojis en consola
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_orchestrator import AgentOrchestrator


def test_pipeline_sin_audio():
    """Ejecutar pipeline completo en una noticia de prueba (sin audio)"""
    print("\n" + "="*60)
    print("TEST: Pipeline sin narración TTS (video + descripción en Word)")
    print("="*60)

    orch = AgentOrchestrator()

    # Noticia de prueba
    test_noticia = {
        'id': 'test_001',
        'titulo': 'Nuevo parque eólico en Fuerteventura genera 2000 empleos',
        'contenido': 'Las autoridades anunciaron un proyecto para instalar parques eólicos '
                    'que beneficiará a toda la isla con energía renovable.',
        'resumen': 'Gran inversión en energía limpia para Canarias',
        'fuente': 'RTVCanarias',
        'url': 'https://ejemplo.com/noticia-001',
    }

    noticias = [test_noticia]

    def progreso_callback(porcentaje, paso, detalle):
        print(f"[{porcentaje:3d}%] {paso:35s} {detalle}")

    print("\n▶️  Iniciando pipeline (SOLO IMÁGENES)...\n")

    try:
        resultado = orch.ejecutar_pipeline_completo(noticias, progreso_cb=progreso_callback, generar_video=False)

        print("\n" + "="*60)
        print("RESULTADOS")
        print("="*60)
        print(f"Estado: {resultado.get('status')}")
        print(f"Imágenes generadas: {resultado.get('imagenes_generadas', 0)}/1")
        print(f"Videos generados: {resultado.get('videos_generados', 0)}/1")
        print(f"Documento: {Path(resultado.get('doc_path')).name if resultado.get('doc_path') else 'N/A'}")

        if resultado.get('errores'):
            print(f"\n⚠️  Errores ({len(resultado['errores'])}):")
            for err in resultado['errores']:
                print(f"  - {err.get('noticia')}: {err.get('error')}")

        # Verificar archivos en /videos/
        videos_dir = Path(__file__).parent / "videos"
        if videos_dir.exists():
            videos = list(videos_dir.glob("*.mp4"))
            docs = list(videos_dir.glob("*.docx"))
            imagenes = list(videos_dir.glob("vineta_*.png"))
            print(f"\n📁 Archivos en /videos/:")
            print(f"  - {len(imagenes)} PNG (imágenes)")
            print(f"  - {len(videos)} MP4 (videos)")
            print(f"  - {len(docs)} DOCX (guías)")
            if docs:
                print(f"\n📄 Documento generado:")
                for doc in sorted(docs)[-1:]:
                    print(f"   {doc.name}")
            if imagenes:
                print(f"\n🖼️ Última imagen:")
                for img in sorted(imagenes)[-1:]:
                    size_kb = img.stat().st_size / 1024
                    print(f"   {img.name} ({size_kb:.0f} KB)")
            if videos:
                print(f"\n🎬 Último video:")
                for vid in sorted(videos)[-1:]:
                    size_mb = vid.stat().st_size / (1024 * 1024)
                    print(f"   {vid.name} ({size_mb:.1f} MB)")

        print("\n✅ Pipeline completado sin errores fatales")
        return resultado.get('status') == 'success'

    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    exito = test_pipeline_sin_audio()
    sys.exit(0 if exito else 1)
