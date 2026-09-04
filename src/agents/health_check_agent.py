"""
HEALTH CHECK AGENT
Responsabilidad: Verificar que todos los requisitos están disponibles antes de ejecutar el pipeline
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class HealthCheckAgent:
    """Verifica disponibilidad de dependencias y requisitos del sistema"""

    def __init__(self):
        self.resultados = {}
        self.todo_ok = True

    def verificar_todo(self) -> Dict:
        """Ejecutar todas las verificaciones"""
        print("\n" + "="*70)
        print("🔍 VERIFICACIÓN DE SISTEMA - AJAMSI PIPELINE")
        print("="*70)

        checks = [
            ("Python", self._check_python),
            ("FFmpeg", self._check_ffmpeg),
            ("Ollama", self._check_ollama),
            ("Carpetas", self._check_carpetas),
            ("Dependencias", self._check_dependencias),
        ]

        for nombre, check_func in checks:
            try:
                status, mensaje = check_func()
                self.resultados[nombre] = {
                    "status": status,
                    "mensaje": mensaje,
                }
                emoji = "✅" if status else "❌"
                print(f"{emoji} {nombre}: {mensaje}")
            except Exception as e:
                self.resultados[nombre] = {
                    "status": False,
                    "mensaje": str(e),
                }
                print(f"❌ {nombre}: ERROR - {e}")
                self.todo_ok = False

        print("\n" + "="*70)
        if self.todo_ok:
            print("✅ SISTEMA LISTO - Puedes comenzar el pipeline")
            print("="*70 + "\n")
        else:
            print("❌ FALTAN REQUISITOS - Instala lo necesario antes de continuar")
            print("="*70 + "\n")

        return {
            "todo_ok": self.todo_ok,
            "resultados": self.resultados,
        }

    def _check_python(self) -> Tuple[bool, str]:
        """Verificar versión de Python"""
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if sys.version_info >= (3, 9):
            return True, f"Python {version} ✓"
        return False, f"Python {version} (necesita 3.9+)"

    def _check_ffmpeg(self) -> Tuple[bool, str]:
        """Verificar FFmpeg"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                timeout=5,
                text=True
            )
            if result.returncode == 0:
                # Extraer versión
                version_line = result.stdout.split('\n')[0]
                return True, f"FFmpeg disponible - {version_line[:40]}"
        except FileNotFoundError:
            return False, "FFmpeg no instalado (descárgalo desde ffmpeg.org)"
        except subprocess.TimeoutExpired:
            return False, "FFmpeg timeout"
        except Exception as e:
            return False, f"Error: {e}"

    def _check_ollama(self) -> Tuple[bool, str]:
        """Verificar Ollama"""
        try:
            result = subprocess.run(
                ['curl', '-s', 'http://localhost:11434/api/tags'],
                capture_output=True,
                timeout=3,
                text=True
            )
            if result.returncode == 0:
                return True, "Ollama corriendo en localhost:11434"
            else:
                return False, "Ollama no responde - ejecuta: ollama serve"
        except FileNotFoundError:
            return False, "curl no encontrado"
        except Exception as e:
            return False, f"Ollama no disponible: {e}"

    def _check_carpetas(self) -> Tuple[bool, str]:
        """Verificar carpetas necesarias"""
        base_path = Path(__file__).parent.parent.parent
        folders = [
            base_path / "imagenes",
            base_path / "videos",
            base_path / "config",
        ]

        missing = []
        for folder in folders:
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
                missing.append(folder.name)

        if missing:
            return True, f"Carpetas creadas: {', '.join(missing)}"
        return True, "Todas las carpetas existen"

    def _check_dependencias(self) -> Tuple[bool, str]:
        """Verificar dependencias de Python"""
        required = ['flask', 'flask_cors', 'feedparser', 'beautifulsoup4']
        missing = []

        for package in required:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)

        if missing:
            return False, f"Instalar: pip install {' '.join(missing)}"
        return True, "Todos los paquetes instalados"


if __name__ == "__main__":
    agent = HealthCheckAgent()
    resultado = agent.verificar_todo()
    sys.exit(0 if resultado["todo_ok"] else 1)
