# make_exe.ps1 — Compilador de SGAI-Agente.exe
# Ejecutar en una máquina Windows con PowerShell 5.1+
#
# REQUISITO: instalar ps2exe una sola vez:
#   Install-Module ps2exe -Scope CurrentUser -Force
#
# USO:
#   .\make_exe.ps1
#   .\make_exe.ps1 -ServerIP 10.50.0.100
#
param(
    [string]$ServerIP = "192.168.100.152",
    [string]$OutputDir = ".\dist"
)

$ErrorActionPreference = "Stop"

# ── 1. Verificar que ps2exe esté instalado ────────────────────────────────────
if (-not (Get-Command Invoke-ps2exe -ErrorAction SilentlyContinue)) {
    Write-Host "[INFO] Instalando ps2exe..." -ForegroundColor Cyan
    Install-Module ps2exe -Scope CurrentUser -Force
}

# ── 2. Generar agent.ps1 con la IP del servidor embebida ─────────────────────
$agentScript = Join-Path $PSScriptRoot "agent.ps1"
if (-not (Test-Path $agentScript)) {
    Write-Error "No se encontró agent.ps1 en $PSScriptRoot"
}

$tempScript = Join-Path $env:TEMP "sgai_agent_build.ps1"
(Get-Content $agentScript -Raw) -replace `
    '\[string\]\$ServerIP = "[^"]*"', `
    "[string]`$ServerIP = `"$ServerIP`"" | Set-Content $tempScript -Encoding UTF8

# ── 3. Compilar a .exe ────────────────────────────────────────────────────────
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir | Out-Null }
$exePath = Join-Path $OutputDir "SGAI-Agente.exe"

Invoke-ps2exe `
    -InputFile  $tempScript `
    -OutputFile $exePath `
    -NoConsole:$false `
    -Title      "SGAI Agente v2" `
    -Description "Agente de inventario Coopeuch" `
    -Company    "Coopeuch" `
    -Version    "2.0.0.0" `
    -requireAdmin

Remove-Item $tempScript -Force

Write-Host ""
Write-Host "✅ Compilado: $exePath" -ForegroundColor Green
Write-Host ""
Write-Host "── Próximos pasos ────────────────────────────────────────────────" -ForegroundColor Yellow
Write-Host "  1. Copia '$exePath' a backend/static/SGAI-Agente.exe en el servidor"
Write-Host "  2. El botón 'Descargar Agente' del dashboard servirá el archivo"
Write-Host "  3. Para actualizar sin rebuild: reemplaza el .exe y listo (volumen montado)"
