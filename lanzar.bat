@echo off
REM Lanzador de AjamSi v1.0
REM Ejecuta el pipeline completo

cd /d "%~dp0"

echo.
echo ========================================
echo   🎬 AJAMSI v1.0
echo   Sistema de TikTok Canario
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo.
    echo Por favor instala Python desde python.org
    pause
    exit /b 1
)

echo ✓ Python detectado
echo.

REM Ejecutar pipeline
echo 🚀 Iniciando pipeline...
echo.

python main.py

echo.
echo ========================================
echo   ✅ Pipeline completado
echo ========================================
pause
