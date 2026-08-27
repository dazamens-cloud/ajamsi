"""
Cargador de configuración para AjamSi
"""

import json
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """Cargador y gestor de configuración"""

    def __init__(self, config_file: str | Path):
        """
        Inicializar cargador de configuración

        Args:
            config_file: Ruta al archivo config.json
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde archivo JSON"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {self.config_file}")

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✓ Configuración cargada desde {self.config_file}")
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Error al parsear JSON en {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtener valor de configuración usando notación con puntos

        Args:
            key: Clave con notación de puntos (ej: 'scrapers.fuentes')
            default: Valor por defecto si no existe

        Returns:
            Valor de configuración
        """
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def get_scraper_fuentes(self) -> list:
        """Obtener lista de fuentes de scraping activas"""
        fuentes = self.get('scrapers.fuentes', [])
        return [f for f in fuentes if f.get('activo', True)]

    def get_generador_config(self) -> Dict:
        """Obtener configuración del generador de ideas"""
        return self.get('generador_ideas', {})

    def get_gemini_config(self) -> Dict:
        """Obtener configuración de Gemini"""
        return self.get('generador_imagenes', {})

    def get_video_config(self) -> Dict:
        """Obtener configuración de compilación de videos"""
        return self.get('compilador_videos', {})

    def get_drive_config(self) -> Dict:
        """Obtener configuración de Google Drive"""
        return self.get('google_drive', {})

    def get_db_path(self) -> Path:
        """Obtener ruta de la base de datos"""
        db_file = self.get('base_datos.archivo', 'data/ajamsi.db')
        return Path(db_file)

    def get_preferences_file(self) -> Path:
        """Obtener ruta del archivo de preferencias"""
        pref_file = self.get('aprendizaje.archivo_preferencias', 'data/preferences.json')
        return Path(pref_file)

    def to_dict(self) -> Dict:
        """Obtener configuración completa como diccionario"""
        return self.config
