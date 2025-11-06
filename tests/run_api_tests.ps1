# Script para ejecutar el servidor y los tests automáticamente
Write-Host "🚀 Iniciando Backend y Tests del API" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si el entorno virtual está activado
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Activando entorno virtual..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Verificar si el servidor ya está corriendo
Write-Host "🔍 Verificando si el servidor está corriendo..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Servidor ya está activo" -ForegroundColor Green
    $serverRunning = $true
} catch {
    Write-Host "ℹ️  Servidor no activo, iniciando..." -ForegroundColor Blue
    $serverRunning = $false
}

if (-not $serverRunning) {
    # Iniciar servidor en background
    Write-Host "🔧 Iniciando servidor en background..." -ForegroundColor Yellow
    $serverJob = Start-Job -ScriptBlock {
        Set-Location $using:PWD
        & ".\venv\Scripts\python.exe" run_server.py
    }
    
    # Esperar a que el servidor esté listo
    Write-Host "⏳ Esperando a que el servidor esté listo..." -ForegroundColor Yellow
    $maxWait = 30
    $waited = 0
    $ready = $false
    
    while ($waited -lt $maxWait -and -not $ready) {
        Start-Sleep -Seconds 1
        $waited++
        
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 1 -ErrorAction Stop
            $ready = $true
        } catch {
            Write-Host "." -NoNewline
        }
    }
    
    Write-Host ""
    
    if ($ready) {
        Write-Host "✅ Servidor listo!" -ForegroundColor Green
    } else {
        Write-Host "❌ Timeout esperando al servidor" -ForegroundColor Red
        Stop-Job -Job $serverJob
        Remove-Job -Job $serverJob
        exit 1
    }
}

Write-Host ""
Write-Host "🧪 Ejecutando tests del API..." -ForegroundColor Cyan
Write-Host ""

# Ejecutar tests desde el directorio raíz
$rootDir = Split-Path -Parent $PSScriptRoot
Set-Location $rootDir
& ".\venv\Scripts\python.exe" "tests\test_api.py"

# Si iniciamos el servidor, preguntar si detenerlo
if (-not $serverRunning) {
    Write-Host ""
    Write-Host "🛑 ¿Quieres detener el servidor? (S/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    
    if ($response -eq "S" -or $response -eq "s") {
        Write-Host "⏹️  Deteniendo servidor..." -ForegroundColor Yellow
        Stop-Job -Job $serverJob
        Remove-Job -Job $serverJob
        Write-Host "✅ Servidor detenido" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Servidor sigue corriendo en background (Job ID: $($serverJob.Id))" -ForegroundColor Blue
        Write-Host "   Para detenerlo más tarde: Stop-Job -Id $($serverJob.Id)" -ForegroundColor Blue
    }
}

Write-Host ""
Write-Host "✅ Proceso completado" -ForegroundColor Green
