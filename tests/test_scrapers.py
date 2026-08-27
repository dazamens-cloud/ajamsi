"""
Tests para verificar que los scrapers funcionan correctamente

Ejecutar con: python -m pytest tests/test_scrapers.py -v
O directamente: python tests/test_scrapers.py
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.config_loader import ConfigLoader
from src.scrapers import ScraperManager, Noticia


def test_config_loading():
    """Test: Cargar configuración correctamente"""
    print("\n✓ TEST: Cargando configuración...")

    config = ConfigLoader("config/config.json")

    assert config is not None, "Config no se cargó"
    assert config.get("proyecto.nombre") == "AjamSi", "Nombre del proyecto incorrecto"

    fuentes = config.get_scraper_fuentes()
    assert len(fuentes) > 0, "No hay fuentes configuradas"

    print(f"  ✓ Configuración cargada correctamente")
    print(f"  ✓ Proyecto: {config.get('proyecto.nombre')}")
    print(f"  ✓ Fuentes activas: {len(fuentes)}")

    return config


def test_scraper_manager_init(config):
    """Test: Inicializar ScraperManager"""
    print("\n✓ TEST: Inicializando ScraperManager...")

    manager = ScraperManager(config.to_dict())

    assert manager is not None, "Manager no se inicializó"
    assert len(manager.scrapers) > 0, "No hay scrapers disponibles"

    fuentes_disponibles = manager.listar_fuentes_disponibles()
    print(f"  ✓ Manager inicializado")
    print(f"  ✓ Scrapers disponibles: {fuentes_disponibles}")

    return manager


def test_scraper_structure(config):
    """Test: Verificar estructura de Noticia"""
    print("\n✓ TEST: Verificando estructura de Noticia...")

    # Crear noticia de prueba
    noticia_prueba = Noticia(
        titulo="Prueba de noticia",
        url="https://example.com/noticia",
        fuente="Test",
        contenido="Contenido de prueba",
        fecha_publicacion=datetime.now()
    )

    assert noticia_prueba.titulo == "Prueba de noticia", "Título incorrecto"
    assert noticia_prueba.url.startswith("http"), "URL inválida"
    assert noticia_prueba.fuente == "Test", "Fuente incorrecta"

    print(f"  ✓ Estructura de Noticia validada")
    print(f"  ✓ Noticia: {noticia_prueba}")


def test_scraper_config(config):
    """Test: Verificar configuración de scrapers"""
    print("\n✓ TEST: Verificando configuración de scrapers...")

    scraper_config = config.get("scrapers", {})
    fuentes = scraper_config.get("fuentes", [])

    assert len(fuentes) > 0, "No hay fuentes configuradas"

    # Validar estructura de cada fuente
    for fuente in fuentes:
        assert "nombre" in fuente, f"Falta 'nombre' en fuente"
        assert "url" in fuente, f"Falta 'url' en fuente {fuente.get('nombre')}"
        assert "prioridad" in fuente, f"Falta 'prioridad' en fuente"

    print(f"  ✓ Configuración de scrapers validada")
    print(f"  ✓ Fuentes configuradas:")
    for fuente in fuentes:
        estado = "✓ Activo" if fuente.get("activo") else "✗ Inactivo"
        print(f"    - {fuente['nombre']} ({estado})")


def test_scraper_especifico(config, nombre_scraper, clase_scraper):
    """Test: Validar un scraper específicamente"""
    print(f"\n✓ TEST: Validando {nombre_scraper}...")

    # Obtener config del scraper
    fuentes = config.get("scrapers.fuentes", [])
    scraper_config = next((f for f in fuentes if nombre_scraper in f.get("nombre", "")), None)

    if not scraper_config:
        print(f"  ⚠ {nombre_scraper} no está configurado")
        return

    # Crear scraper
    scraper = clase_scraper(scraper_config)

    assert scraper is not None, "Scraper no se inicializó"
    assert scraper.nombre == scraper_config["nombre"], "Nombre incorrecto"
    assert scraper.url_base == scraper_config["url"], "URL incorrecto"

    print(f"  ✓ Scraper inicializado: {scraper.nombre}")
    print(f"  ✓ URL base: {scraper.url_base}")
    print(f"  ✓ Prioridad: {scraper.prioridad}")
    print(f"  ✓ Estructura del scraper validada")


def test_lancelot_digital_scraper(config):
    """Test: Validar LancelotDigitalScraper"""
    from src.scrapers import LancelotDigitalScraper
    test_scraper_especifico(config, "Lancelot", LancelotDigitalScraper)


def test_cronicas_lanzarote_scraper(config):
    """Test: Validar CronicasLanzaroteScraper"""
    from src.scrapers import CronicasLanzaroteScraper
    test_scraper_especifico(config, "Crónicas", CronicasLanzaroteScraper)


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("  TESTS DE SCRAPERS - AjamSi")
    print("="*60)

    try:
        # Test 1: Cargar config
        config = test_config_loading()

        # Test 2: Estructura de Noticia
        test_scraper_structure(config)

        # Test 3: Config de scrapers
        test_scraper_config(config)

        # Test 4: Inicializar manager
        manager = test_scraper_manager_init(config)

        # Test 5: Validar scrapers específicos
        test_lancelot_digital_scraper(config)
        test_cronicas_lanzarote_scraper(config)

        # Resumen
        print("\n" + "="*60)
        print("  ✅ TODOS LOS TESTS PASARON")
        print("="*60)
        print("\nNota: No se ejecutó scraping real de URLs para evitar")
        print("      problemas de red. Los tests verifican estructura.")
        print("\nPróximo paso: Implementar test de scraping real con mock\n")

        return True

    except AssertionError as e:
        print(f"\n❌ TEST FALLIDO: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
