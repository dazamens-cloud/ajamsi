# AJAMSI - Monitor de Servidor Automático
# Reinicia el servidor Flask si falla
# Ejecución: powershell -File monitor_servidor.ps1

$projectPath = "D:\proyectos godot\tik tok\ajamsi"
$pythonExe = "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe"
$appFile = "app_backend.py"
$apiUrl = "http://localhost:5000/api/state"
$checkInterval = 10  # Segundos entre chequeos
$logFile = "$projectPath\servidor.log"

function Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $message"
    Write-Host $logEntry -ForegroundColor Cyan
    Add-Content -Path $logFile -Value $logEntry
}

function StartServer {
    Log "🚀 Iniciando servidor..."
    try {
        $job = Start-Job -ScriptBlock {
            cd $using:projectPath
            & $using:pythonExe $using:appFile
        }
        Log "✓ Servidor iniciado (Job ID: $($job.Id))"
        return $true
    }
    catch {
        Log "❌ Error iniciando servidor: $_"
        return $false
    }
}

function CheckServer {
    try {
        $response = curl $apiUrl -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            return $true
        }
    }
    catch {
        return $false
    }
}

function StopAllServers {
    Get-Process python.exe -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep 2
}

# INICIAR MONITOREO
Log "╔══════════════════════════════════════════════╗"
Log "║ AJAMSI - Monitor de Servidor Automático     ║"
Log "║ Intervalo de chequeo: $checkInterval segundos       ║"
Log "╚══════════════════════════════════════════════╝"

# Matar servidores anteriores
StopAllServers
Log "⏹️  Procesos anteriores terminados"

# Iniciar servidor
StartServer
Start-Sleep 3

# Loop de monitoreo
$consecutive_fails = 0
while ($true) {
    Start-Sleep $checkInterval

    if (CheckServer) {
        Write-Host "✓ Servidor OK" -ForegroundColor Green -NoNewline
        Write-Host " @ $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Gray
        $consecutive_fails = 0
    }
    else {
        $consecutive_fails++
        Write-Host "❌ Servidor NO responde (intento $consecutive_fails)" -ForegroundColor Red

        if ($consecutive_fails -ge 2) {
            Log "⚠️  Servidor caído, reiniciando..."
            StopAllServers
            StartServer
            Start-Sleep 3
            $consecutive_fails = 0
        }
    }
}
