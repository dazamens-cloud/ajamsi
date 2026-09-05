@echo off
REM Lanzador de AJAMSI Studio - PWA interactiva
REM Arranca el servidor y abre el navegador

cd /d "%~dp0"

echo.
echo ========================================
echo   AJAMSI Studio
echo   Noticias Canarias a Videos TikTok
echo ========================================
echo.

set PYTHON_PATH=C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo ERROR: Python no encontrado en %PYTHON_PATH%
    echo Actualiza la ruta en lanzar.bat
    pause
    exit /b 1
)

echo Python OK: %PYTHON_PATH%
echo.
echo Abriendo interfaz en http://localhost:5000 ...
start "" "http://localhost:5000"

"%PYTHON_PATH%" app_backend.py

pause
