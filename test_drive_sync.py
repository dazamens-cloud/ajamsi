#!/usr/bin/env python3
"""
Script de prueba para sincronización con Google Drive
"""

import sys
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents import DriveSyncAgent
from utils.config_loader import ConfigLoader


def main():
    print("\n" + "="*70)
    print("  PRUEBA DE SINCRONIZACIÓN CON GOOGLE DRIVE")
    print("="*70 + "\n")

    # Cargar configuración
    try:
        config_loader = ConfigLoader("config/config.json")
        config = config_loader.to_dict()
        print("✅ Configuración cargada\n")
    except Exception as e:
        logger.error(f"❌ Error cargando configuración: {e}")
        return

    # Inicializar agente
    print("🔌 Conectando con Google Drive...")
    drive_agent = DriveSyncAgent(config)

    # Obtener estado
    print("\n📊 Obteniendo estado de Google Drive...\n")
    estado = drive_agent.obtener_estado_drive()

    if estado.get('conectado'):
        print("✅ CONECTADO A GOOGLE DRIVE")
        print(f"   📁 Archivos encontrados: {estado.get('archivos_en_drive', 0)}")
        print(f"   💾 Tamaño total: {estado.get('tamaño_total_mb', 0)} MB")
        print(f"   📈 Espacio usado: {estado.get('espacio_usado_gb', 0)} GB")
        print(f"   📉 Espacio disponible: {estado.get('espacio_disponible_gb', 0)} GB")
    else:
        print("⚠️  NO CONECTADO A GOOGLE DRIVE")
        if estado.get('error'):
            print(f"   Error: {estado.get('error')}")

    # Probar sincronización
    print("\n" + "="*70)
    print("  PROBANDO SINCRONIZACIÓN")
    print("="*70 + "\n")

    resultado_sync = drive_agent.ejecutar({'archivos': 5})

    print(f"\n✅ Estado de sincronización: {resultado_sync.get('status')}")
    print(f"   Archivos procesados: {resultado_sync.get('archivos_procesados', 0)}")
    print(f"   Carpetas creadas: {resultado_sync.get('carpetas_creadas', 0)}")
    print(f"   Tamaño: {resultado_sync.get('tamaño_mb', 0)} MB")

    print("\n" + "="*70)
    print("✅ Prueba completada")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
