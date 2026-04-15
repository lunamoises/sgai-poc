# SGAI Agent v2 — Ejecutar en equipos Windows
# Requiere: PowerShell 5.1+
param(
    [string]$ServerIP = "192.168.100.152",
    [string]$ApiKey   = "sgai-secret-key-2026"
)

$url = "http://$ServerIP/v1/register"

try {
    $cpu    = (Get-CimInstance Win32_Processor | Select-Object -First 1).Name
    $ram    = "{0} GB" -f [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
    $disk   = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
    $libre  = "{0} GB" -f [math]::Round($disk.FreeSpace / 1GB, 1)
    $ip     = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notmatch '^127'} | Select-Object -First 1).IPAddress

    $body = @{
        hostname    = $env:COMPUTERNAME
        ip_interna  = $ip
        modelo_cpu  = $cpu
        ram_total   = $ram
        disco_libre = $libre
    } | ConvertTo-Json

    $resp = Invoke-RestMethod -Uri $url -Method POST -Body $body `
            -ContentType "application/json" `
            -Headers @{"X-API-KEY" = $ApiKey}

    Write-Host "[OK] Registrado: $($env:COMPUTERNAME) -> id=$($resp.id)"
} catch {
    Write-Host "[ERROR] $_"
}
