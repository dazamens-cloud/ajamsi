# Lanzador de AjamSi v1.0 (PowerShell)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🎬 AJAMSI v1.0" -ForegroundColor Cyan
Write-Host "   Sistema de TikTok Canario" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar a directorio del proyecto
Set-Location $PSScriptRoot

# Ruta completa de Python
$pythonPath = "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe"

# Verificar Python existe
if (-not (Test-Path $pythonPath)) {
    Write-Host "❌ Error: Python no encontrado en $pythonPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Intenta:" -ForegroundColor Yellow
    Write-Host "  1. Verificar Python: where python" -ForegroundColor White
    Write-Host "  2. Actualizar lanzar.ps1 con ruta correcta" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✓ Python encontrado: $pythonPath" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Iniciando pipeline AjamSi..." -ForegroundColor Green
Write-Host ""

# Ejecutar pipeline
& $pythonPath main.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   ✅ Pipeline completado" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Read-Host "Presiona Enter para cerrar"
