@echo off
REM Lanzador de AJAMSI - Dashboard + Pipeline de Contenido
REM Arranca el servidor Flask y abre el dashboard

cd /d "%~dp0"

echo.
echo ========================================
echo    AJAMSI - Content Pipeline
echo    Noticias Canarias ^> Videos TikTok
echo ========================================
echo.

set PYTHON_PATH=C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo ERROR: Python no encontrado
    echo Actualiza PYTHON_PATH en lanzar.bat
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo [OK] Iniciando servidor Flask en puerto 5000...
echo.
echo URLS:
echo   Dashboard:  http://localhost:5000
echo   Studio:     http://localhost:5000/studio
echo.
timeout /t 2

start "" "http://localhost:5000"

"%PYTHON_PATH%" app_backend.py

pause
