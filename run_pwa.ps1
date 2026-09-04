# AJAMSI PWA Launcher
# Inicia el servidor Flask y abre la interfaz web

Write-Host "`n" + "="*70
Write-Host "  AJAMSI - PWA LOCAL"
Write-Host "  Iniciando servidor..."
Write-Host "="*70 + "`n"

# Instalar dependencias
Write-Host "📦 Verificando dependencias..."
& pip install -q -r requirements_pwa.txt

# Abrir navegador en la interfaz
Write-Host "🌐 Abriendo interfaz web..."
Start-Sleep 2
Start-Process "http://localhost:5000/app_frontend.html"

# Lanzar servidor Flask
Write-Host "`n🚀 Iniciando servidor en http://localhost:5000`n"
& "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe" app_backend.py
