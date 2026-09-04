#!/usr/bin/env python3
"""Test video compilation con FFmpeg corregido"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents import VideoCompilerAgent
from utils.config_loader import ConfigLoader

print("Generando video nuevo con FFmpeg corregido...\n")

config = ConfigLoader("config/config.json").to_dict()
agent = VideoCompilerAgent(config)

resultado = agent.ejecutar(
    imagen_path="imagenes/el_tipico_canario.png",
    guion="El Típico reaccionando a noticias",
    audio_path=None,
    duracion=10,
    formato="tiktok"
)

print(f"Status: {resultado.get('status')}")
print(f"Video: {resultado.get('video_filename')}")
print(f"Tamaño: {resultado.get('tamaño_mb'):.1f} MB")
print(f"Resolución: {resultado.get('resolucion')}")

if resultado.get('status') == 'success':
    print("\n✅ Video generado correctamente")
else:
    print(f"\n❌ Error: {resultado.get('error')}")
