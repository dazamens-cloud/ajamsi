@echo off
chcp 65001 > nul
cls

echo.
echo ================================================================
echo  AJAMSI - PWA LOCAL
echo  Iniciando servidor...
echo ================================================================
echo.

echo. [*] Verificando dependencias...
python -m pip install -q -r requirements_pwa.txt

echo. [*] Abriendo interfaz web en 3 segundos...
timeout /t 3 /nobreak

start http://localhost:5000

echo.
echo [OK] Iniciando servidor en http://localhost:5000
echo.

python app_backend.py
