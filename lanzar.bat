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

REM Usar ruta completa de Python
set PYTHON_PATH=C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe

REM Verificar Python existe
if not exist "%PYTHON_PATH%" (
    echo ❌ Error: Python no encontrado en %PYTHON_PATH%
    echo.
    echo Intenta:
    echo   1. Verificar Python instalado: where python
    echo   2. Actualizar lanzar.bat con ruta correcta
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado: %PYTHON_PATH%
echo.

REM Ejecutar pipeline
echo 🚀 Iniciando pipeline AjamSi...
echo.

"%PYTHON_PATH%" main.py

echo.
echo ========================================
echo   ✅ Pipeline completado
echo ========================================
pause
