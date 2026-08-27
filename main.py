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
        # Cargar configuración
        print(f"{Fore.GREEN}Inicializando...{Style.RESET_ALL}")
        config = ConfigLoader(CONFIG_FILE)
        db = DatabaseManager(DATABASE_FILE)

        print(f"{Fore.GREEN}✓ Configuración cargada{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Base de datos conectada{Style.RESET_ALL}")

        # Mostrar información de proyecto
        print(f"\nProyecto: {config.get('proyecto.nombre')}")
        print(f"Isla: {config.get('proyecto.isla')}")
        print(f"Cuenta: {config.get('proyecto.cuenta_tiktok')}")

        # Mostrar estadísticas
        stats = db.obtener_stats()
        print(f"\n{Fore.CYAN}ESTADÍSTICAS:{Style.RESET_ALL}")
        print(f"  Total noticias: {stats['total_noticias']}")
        print(f"  Total ideas: {stats['total_ideas']}")
        print(f"  Total imágenes: {stats['total_imagenes']}")
        print(f"  Total videos: {stats['total_videos']}")
        print(f"  Noticias usadas: {stats['noticias_usadas']}")

        # Menú
        while True:
            print_menu()
            opcion = input(f"{Fore.YELLOW}Selecciona opción: {Style.RESET_ALL}").strip()

            if opcion == "0":
                print(f"{Fore.GREEN}¡Hasta pronto!{Style.RESET_ALL}")
                break
            elif opcion == "1":
                print(f"{Fore.CYAN}[DESARROLLO] Scraping de noticias{Style.RESET_ALL}")
            elif opcion == "2":
                print(f"{Fore.CYAN}[DESARROLLO] Generación de ideas{Style.RESET_ALL}")
            elif opcion == "3":
                print(f"{Fore.CYAN}[DESARROLLO] Generación de imágenes{Style.RESET_ALL}")
            elif opcion == "4":
                print(f"{Fore.CYAN}[DESARROLLO] Compilación de videos{Style.RESET_ALL}")
            elif opcion == "5":
                stats = db.obtener_stats()
                print(f"\n{Fore.CYAN}ESTADÍSTICAS ACTUALES:{Style.RESET_ALL}")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
            elif opcion == "6":
                print(f"{Fore.CYAN}[DESARROLLO] Configuración de preferencias{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Opción no válida{Style.RESET_ALL}")

        db.cerrar()

    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
