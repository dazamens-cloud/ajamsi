$pythonPath = "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe"
$projectPath = "D:\proyectos godot\tik tok\ajamsi"
$apiUrl = "http://localhost:5000/api/state"

function CheckAndRestart {
    while ($true) {
        Start-Sleep 5
        try {
            $response = Invoke-WebRequest -Uri $apiUrl -UseBasicParsing -ErrorAction Stop
            Write-Host "[OK] Servidor activo" -ForegroundColor Green
        }
        catch {
            Write-Host "[ERROR] Servidor caldo, reiniciando..." -ForegroundColor Red
            Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
            Start-Sleep 2
            Start-Job -ScriptBlock {
                cd "D:\proyectos godot\tik tok\ajamsi"
                & "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe" app_backend.py
            }
            Start-Sleep 5
        }
    }
}

# Detener procesos anteriores
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2

# Iniciar servidor
Start-Job -ScriptBlock {
    cd "D:\proyectos godot\tik tok\ajamsi"
    & "C:\Users\andre\AppData\Local\Programs\Python\Python312\python.exe" app_backend.py
}

Start-Sleep 3

# Ejecutar monitoreo
CheckAndRestart
