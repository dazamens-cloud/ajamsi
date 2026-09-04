#Requires -Version 5.0
<#
.SYNOPSIS
    AJAMSI Server Monitor - Sistema de monitoreo y reinicio automático del servidor Flask

.DESCRIPTION
    Monitorea continuamente la disponibilidad del servidor Flask. Si detecta que ha caído,
    lo reinicia automáticamente. Incluye logging completo, manejo de errores robusto,
    y notificaciones de estado.

.PARAMETER CheckInterval
    Intervalo en segundos entre chequeos de salud. Default: 10 segundos

.PARAMETER MaxRetries
    Número de intentos fallidos antes de reiniciar. Default: 2

.PARAMETER LogPath
    Ruta del archivo de log. Default: servidor.log en el directorio del proyecto
#>

param(
    [int]$CheckInterval = 10,
    [int]$MaxRetries = 2,
    [string]$LogPath = "D:\proyectos godot\tik tok\ajamsi\servidor.log"
)

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

$ProjectPath = "D:\proyectos godot\tik tok\ajamsi"
$PythonExe = "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe"
$AppFile = "app_backend.py"
$ApiHealthUrl = "http://localhost:5000/api/state"
$ApiInitUrl = "http://localhost:5000/api/init"
$Port = 5000

# ============================================================================
# FUNCIONES DE LOGGING
# ============================================================================

function Write-Log {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,

        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR")]
        [string]$Level = "INFO"
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"

    # Escribir a consola con colores
    switch ($Level) {
        "SUCCESS" { Write-Host $logEntry -ForegroundColor Green }
        "WARNING" { Write-Host $logEntry -ForegroundColor Yellow }
        "ERROR" { Write-Host $logEntry -ForegroundColor Red }
        default { Write-Host $logEntry -ForegroundColor Cyan }
    }

    # Escribir a archivo
    try {
        Add-Content -Path $LogPath -Value $logEntry -ErrorAction SilentlyContinue
    }
    catch {
        # Si falla el log a archivo, no interrumpir
    }
}

# ============================================================================
# FUNCIONES DE GESTIÓN DEL SERVIDOR
# ============================================================================

function Test-PortAvailable {
    param([int]$Port)

    try {
        $tcpConnection = Test-NetConnection -ComputerName "127.0.0.1" -Port $Port -WarningAction SilentlyContinue
        return $tcpConnection.TcpTestSucceeded
    }
    catch {
        return $false
    }
}

function Stop-AllPythonServers {
    Write-Log "Terminando procesos Python anteriores..." "INFO"

    try {
        $processes = Get-Process python -ErrorAction SilentlyContinue
        if ($processes) {
            $processes | Stop-Process -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 2
            Write-Log "Procesos Python terminados" "SUCCESS"
        }
        else {
            Write-Log "No hay procesos Python ejecutándose" "INFO"
        }
    }
    catch {
        Write-Log "Error terminando procesos: $_" "WARNING"
    }
}

function Start-FlaskServer {
    Write-Log "Iniciando servidor Flask..." "INFO"

    try {
        $job = Start-Job -ScriptBlock {
            Set-Location "D:\proyectos godot\tik tok\ajamsi"
            & "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe" app_backend.py 2>&1
        }

        Write-Log "Proceso Flask iniciado (JobID: $($job.Id))" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Error iniciando servidor: $_" "ERROR"
        return $false
    }
}

function Test-ServerHealth {
    try {
        $response = Invoke-WebRequest -Uri $ApiHealthUrl `
            -UseBasicParsing `
            -ErrorAction Stop `
            -TimeoutSec 5

        if ($response.StatusCode -eq 200) {
            return $true
        }
    }
    catch {
        # El servidor no responde
    }

    return $false
}

# ============================================================================
# RUTINA PRINCIPAL DE MONITOREO
# ============================================================================

function Start-Monitoring {
    Write-Log "======================================" "INFO"
    Write-Log "AJAMSI Server Monitor - Iniciando" "INFO"
    Write-Log "Intervalo chequeo: $CheckInterval segundos" "INFO"
    Write-Log "Max reintentos: $MaxRetries" "INFO"
    Write-Log "Ruta log: $LogPath" "INFO"
    Write-Log "======================================" "INFO"

    # Cleanup inicial
    Stop-AllPythonServers

    # Iniciar servidor
    if (-not (Start-FlaskServer)) {
        Write-Log "Falló iniciar servidor en primer intento" "ERROR"
        Start-Sleep 5
        Start-FlaskServer
    }

    Start-Sleep 5

    # Variables de control
    $consecutiveFailures = 0
    $restartCount = 0
    $startTime = Get-Date

    Write-Log "Monitoreo iniciado correctamente" "SUCCESS"
    Write-Log "======================================" "INFO"

    # LOOP PRINCIPAL DE MONITOREO
    while ($true) {
        Start-Sleep $CheckInterval

        # Chequear salud del servidor
        $isHealthy = Test-ServerHealth
        $uptime = (Get-Date) - $startTime
        $uptimeStr = "{0:hh\:mm\:ss}" -f $uptime

        if ($isHealthy) {
            # Servidor está bien
            Write-Host "[✓] OK | Uptime: $uptimeStr | Restarts: $restartCount" -ForegroundColor Green
            $consecutiveFailures = 0
        }
        else {
            # Servidor no responde
            $consecutiveFailures++
            Write-Host "[✗] FALLO #$consecutiveFailures | Uptime: $uptimeStr" -ForegroundColor Red

            if ($consecutiveFailures -ge $MaxRetries) {
                Write-Log "Servidor caído ($consecutiveFailures fallos). Reiniciando..." "WARNING"

                # Detener y reiniciar
                Stop-AllPythonServers
                Start-FlaskServer
                Start-Sleep 5

                $consecutiveFailures = 0
                $restartCount++
                $startTime = Get-Date

                Write-Log "Servidor reiniciado. Total reinicios: $restartCount" "SUCCESS"
            }
        }
    }
}

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

try {
    Start-Monitoring
}
catch {
    Write-Log "Error fatal en el monitor: $_" "ERROR"
    exit 1
}
