@echo off
REM Lanzador Automático de AjamSi v1.0
REM Busca Python automáticamente y ejecuta el pipeline

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ========================================
echo   🎬 AJAMSI v1.0 - Lanzador Automático
echo   Sistema de TikTok Canario
echo ========================================
echo.

REM Rutas donde buscar Python (en orden de preferencia)
set PYTHON_PATHS=^
    C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe^
    C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe^
    C:\Python312\python.exe^
    C:\Python311\python.exe^
    C:\Python310\python.exe^
    python.exe

REM Buscar Python en las rutas
set PYTHON_FOUND=0
for %%P in (%PYTHON_PATHS%) do (
    if !PYTHON_FOUND! equ 0 (
        if "%%P"=="python.exe" (
            where python >nul 2>&1
            if !errorlevel! equ 0 (
                for /f "delims=" %%A in ('where python') do set PYTHON_PATH=%%A
                set PYTHON_FOUND=1
            )
        ) else if exist "%%P" (
            set PYTHON_PATH=%%P
            set PYTHON_FOUND=1
        )
    )
)

if !PYTHON_FOUND! equ 0 (
    echo ❌ Error: Python no encontrado
    echo.
    echo Acciones:
    echo   1. Instala Python desde https://www.python.org
    echo   2. Asegúrate de marcar "Add Python to PATH"
    echo   3. Reinicia este script
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado: !PYTHON_PATH!
echo.
echo 🚀 Iniciando pipeline AjamSi...
echo.

"!PYTHON_PATH!" main.py

echo.
echo ========================================
echo   ✅ Pipeline completado
echo ========================================
echo.
pause
