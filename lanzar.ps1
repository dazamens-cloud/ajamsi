# Lanzador de AjamSi v1.0 (PowerShell)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎬 AJAMSI v1.0" -ForegroundColor Cyan
Write-Host "   Sistema de TikTok Canario" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar a directorio del proyecto
Set-Location $PSScriptRoot

# Verificar Python
try {
    python --version 2>$null | Out-Null
    Write-Host "✓ Python detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Python desde python.org" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "🚀 Iniciando pipeline..." -ForegroundColor Green
Write-Host ""

# Ejecutar pipeline
python main.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ Pipeline completado" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Read-Host "Presiona Enter para cerrar"
