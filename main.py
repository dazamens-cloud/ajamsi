"""
Script principal de AjamSi
Sistema automático de generación de contenido TikTok desde noticias de Canarias
"""

import sys
from pathlib import Path
from colorama import Fore, Style, init

# Inicializar colorama para Windows
init()

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config_loader import ConfigLoader
from utils.db import DatabaseManager
from src.constants import (
    APP_NAME, APP_VERSION, CONFIG_FILE, DATABASE_FILE,
    PROJECT_ROOT
)


def print_header():
    """Imprimir encabezado de la aplicación"""
    print(f"{Fore.CYAN}")
    print("=" * 60)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print(f"  Sistema de Generación Automática de Contenido TikTok")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")


def print_menu():
    """Mostrar menú principal"""
    print(f"\n{Fore.YELLOW}MENÚ PRINCIPAL{Style.RESET_ALL}")
    print("-" * 40)
    print("1. Scrapear noticias")
    print("2. Generar ideas")
    print("3. Generar imágenes")
    print("4. Compilar videos")
    print("5. Ver estadísticas")
    print("6. Configurar preferencias")
    print("0. Salir")
    print("-" * 40)


def main():
    """Función principal"""
    print_header()

    try:
        # Importar Pipeline
        from pipeline import AjamSiPipeline

        # Cargar configuración
        print(f"{Fore.GREEN}Inicializando AjamSi Pipeline...{Style.RESET_ALL}")
        pipeline = AjamSiPipeline(CONFIG_FILE)

        print(f"{Fore.GREEN}✓ Pipeline inicializado{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Base de datos conectada{Style.RESET_ALL}")

        # Mostrar información de proyecto
        print(f"\n{Fore.CYAN}Proyecto:{Style.RESET_ALL} AjamSi v{APP_VERSION}")
        print(f"{Fore.CYAN}Isla:{Style.RESET_ALL} Lanzarote")
        print(f"{Fore.CYAN}Cuenta:{Style.RESET_ALL} @hummorkana")

        # Mostrar estadísticas iniciales
        stats = pipeline.obtener_estadisticas()
        print(f"\n{Fore.CYAN}ESTADÍSTICAS ACTUALES:{Style.RESET_ALL}")
        print(f"  Noticias: {stats.get('noticias', 0)}")
        print(f"  Ideas: {stats.get('ideas', 0)}")
        print(f"  Imágenes: {stats.get('imagenes', 0)}")
        print(f"  Videos: {stats.get('videos', 0)}")

        # Ejecutar pipeline completo
        print(f"\n{Fore.YELLOW}Ejecutando pipeline completo...{Style.RESET_ALL}\n")

        resultado = pipeline.ejecutar_completo(
            num_ideas_por_noticia=3,
            compilar_videos=True
        )

        # Mostrar resumen
        print(f"\n{Fore.CYAN}RESUMEN DE EJECUCIÓN:{Style.RESET_ALL}")
        print(f"  ✅ Noticias scrapeadas: {resultado.get('noticias_scrapeadas', 0)}")
        print(f"  ✅ Ideas generadas: {resultado.get('ideas_generadas', 0)}")
        print(f"  ✅ Videos compilados: {resultado.get('videos_compilados', 0)}")

        if resultado.get('errores'):
            print(f"  ⚠️  Errores: {len(resultado.get('errores', []))}")

        # Sincronizar a Google Drive
        print(f"\n{Fore.YELLOW}Sincronizando con Google Drive...{Style.RESET_ALL}")
        sync_result = pipeline.sincronizar_a_nube()

        print(f"{Fore.CYAN}Sincronización:{Style.RESET_ALL}")
        print(f"  Archivos: {sync_result.get('archivos_sincronizados', 0)}")
        print(f"  Tamaño: {sync_result.get('tamaño_bytes', 0) / (1024**2):.1f} MB")

        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"✅ ¡PIPELINE COMPLETADO EXITOSAMENTE!")
        print(f"{'='*60}{Style.RESET_ALL}\n")

    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
