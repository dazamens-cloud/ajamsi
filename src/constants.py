"""
Constantes del proyecto AjamSi
"""

import os
from pathlib import Path

# Rutas base
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
SRC_DIR = PROJECT_ROOT / "src"
LOGS_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Archivos
CONFIG_FILE = CONFIG_DIR / "config.json"
PREFERENCES_FILE = DATA_DIR / "preferences.json"
DATABASE_FILE = DATA_DIR / "ajamsi.db"

# Directorios de datos
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
IMAGES_DIR = DATA_DIR / "images"
VIDEOS_DIR = DATA_DIR / "videos"

# Crear directorios si no existen
for dir_path in [DATA_DIR, CONFIG_DIR, LOGS_DIR, OUTPUT_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, IMAGES_DIR, VIDEOS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Constantes de aplicación
APP_NAME = "AjamSi"
APP_VERSION = "0.1.0"
ISLA = "Lanzarote"
CUENTA_TIKTOK = "@hummorkana"

# Constantes de scraping
TIMEOUT_SCRAPER = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
DIAS_ATRAS = 7

# Constantes de generación
IDIOMA_GENERACION = "es"
TONO_HUMOR = "sardónico_canario"

# Constantes de video
RESOLUCION_VIDEO = "1080x1920"
FPS_VIDEO = 30
DURACION_MIN_VIDEO = 15
DURACION_MAX_VIDEO = 60

# Códigos de feedback
FEEDBACK_BUENO = "✅"
FEEDBACK_AJUSTAR = "🔶"
FEEDBACK_MALO = "❌"

# Estados del workflow
ESTADO_PENDIENTE = "pendiente"
ESTADO_EN_PROGRESO = "en_progreso"
ESTADO_COMPLETADO = "completado"
ESTADO_ERROR = "error"
