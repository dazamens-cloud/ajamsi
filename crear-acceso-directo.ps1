# Script para crear acceso directo en el Escritorio

$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ProjectPath = Get-Location
$LanzadorPath = Join-Path $ProjectPath "lanzar.bat"
$AccesoDirectoPath = Join-Path $DesktopPath "AjamSi - Lanzar.lnk"

Write-Host ""
Write-Host "Creando acceso directo en el escritorio..." -ForegroundColor Cyan
Write-Host ""

# Crear objeto COM para crear el shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($AccesoDirectoPath)
$Shortcut.TargetPath = $LanzadorPath
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.Description = "Lanzador de AjamSi - Sistema de TikTok Canario"
$Shortcut.IconLocation = "C:\Windows\System32\cmd.exe,0"
$Shortcut.Save()

Write-Host "✓ Acceso directo creado en: $AccesoDirectoPath" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes hacer doble clic en 'AjamSi - Lanzar' desde el escritorio" -ForegroundColor Yellow
Write-Host ""
Write-Host "O ejecuta: & '$LanzadorPath'" -ForegroundColor Cyan
