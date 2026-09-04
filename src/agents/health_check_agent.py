"""
HEALTH CHECK AGENT
Responsabilidad: Verificar que todos los requisitos están disponibles y auto-reparar si es posible
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class HealthCheckAgent:
    """Verifica disponibilidad de dependencias y requisitos del sistema con auto-repair"""

    def __init__(self):
        self.resultados = {}
        self.todo_ok = True
        self.reparaciones = []

    def verificar_todo(self, auto_repair: bool = True) -> Dict:
        """Ejecutar todas las verificaciones y reparaciones"""
        print("\n" + "="*70)
        print("🔍 VERIFICACIÓN DE SISTEMA - AJAMSI PIPELINE")
        if auto_repair:
            print("   (Con intento de auto-reparación)")
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

                # Si auto_repair está activado y falló, intenta reparar
                if not status and auto_repair:
                    print(f"   🔧 Intentando reparar {nombre}...")
                    if self._intentar_reparar(nombre):
                        status, mensaje = check_func()
                        self.resultados[nombre] = {"status": status, "mensaje": mensaje}
                        if status:
                            print(f"   ✅ {nombre} REPARADO")
                            self.reparaciones.append(nombre)
                        else:
                            print(f"   ❌ No se pudo reparar {nombre}")
                            self.todo_ok = False
                    else:
                        self.todo_ok = False
                elif not status:
                    self.todo_ok = False

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
            if self.reparaciones:
                print(f"   (Reparados: {', '.join(self.reparaciones)})")
        else:
            print("❌ FALTAN REQUISITOS - Intenta reparar o instala manualmente")
        print("="*70 + "\n")

        return {
            "todo_ok": self.todo_ok,
            "resultados": self.resultados,
            "reparaciones": self.reparaciones,
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

    def _intentar_reparar(self, nombre: str) -> bool:
        """Intenta reparar un componente fallido"""
        try:
            if nombre == "Dependencias":
                return self._reparar_dependencias()
            elif nombre == "Ollama":
                return self._reparar_ollama()
            elif nombre == "Carpetas":
                return self._reparar_carpetas()
        except Exception as e:
            print(f"   Error durante reparación: {e}")
        return False

    def _reparar_dependencias(self) -> bool:
        """Intenta instalar dependencias faltantes"""
        required = ['flask', 'flask_cors', 'feedparser', 'beautifulsoup4']
        missing = []

        for package in required:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)

        if not missing:
            return True

        try:
            print(f"   Instalando: {', '.join(missing)}")
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--quiet'] + missing,
                timeout=120,
                check=True
            )
            return True
        except Exception as e:
            print(f"   No se pudo instalar: {e}")
            return False

    def _reparar_ollama(self) -> bool:
        """Intenta iniciar Ollama si está disponible"""
        try:
            # Verificar si está instalado
            result = subprocess.run(['ollama', '--version'], capture_output=True, timeout=2)
            if result.returncode == 0:
                # Está instalado, intenta iniciar
                print(f"   Iniciando Ollama...")
                subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                import time
                time.sleep(3)  # Esperar a que arranque
                return True
        except Exception as e:
            print(f"   Ollama no encontrado: {e}")
        return False

    def _reparar_carpetas(self) -> bool:
        """Crea carpetas faltantes"""
        try:
            base_path = Path(__file__).parent.parent.parent
            folders = [
                base_path / "imagenes",
                base_path / "videos",
                base_path / "config",
            ]

            for folder in folders:
                folder.mkdir(parents=True, exist_ok=True)

            return True
        except Exception as e:
            print(f"   No se pudo crear carpetas: {e}")
            return False


if __name__ == "__main__":
    agent = HealthCheckAgent()
    resultado = agent.verificar_todo(auto_repair=True)
    sys.exit(0 if resultado["todo_ok"] else 1)
