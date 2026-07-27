# Recovery: mata instancias del cron de la Analista (por command line) y relanza limpio.
# Espejo de codex_cron_recover.ps1. Lanzado por el Arquitecto bajo permiso de cron (operador autorizo 2026-07-28).
# Seguro: solo toca powershell cuyo command line contiene 'analista_mailbox_cron' (NO Codex, NO la sesion Claude).
$ErrorActionPreference = "Continue"
$me = $PID
$killed = @()
try {
  Get-CimInstance Win32_Process -Filter "name='powershell.exe'" |
    Where-Object { $_.CommandLine -and ($_.CommandLine -like '*analista_mailbox_cron*') -and ($_.ProcessId -ne $me) } |
    ForEach-Object {
      Write-Host ("Killing Analista cron PID " + $_.ProcessId)
      Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
      $killed += $_.ProcessId
    }
} catch { Write-Host ("CIM query failed: " + $_.Exception.Message) }
Write-Host ("Killed PIDs: " + ($killed -join ','))
Start-Sleep -Seconds 3

# Limpiar estado stale del exec anterior (lock + exec-lease + prompt) para arranque limpio
$base = Join-Path $PSScriptRoot "..\.protocol-tmp\analista_mailbox_cron"
foreach ($f in @("analista_mailbox_cron.prompt.txt","analista_mailbox_cron.lock","analista_mailbox_cron.exec-lease.json")) {
  $p = Join-Path $base $f
  try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; Write-Host ("Removed stale " + $f) }
  catch { Write-Host ($f + ": " + $_.Exception.Message) }
}

# Relanzar el cron de la Analista limpio (detached)
$cron = Join-Path $PSScriptRoot "Analista\analista_mailbox_cron.ps1"
if (Test-Path -LiteralPath $cron) {
  Start-Process powershell -ArgumentList "-NoProfile","-File",$cron,"-ExecTimeoutSeconds","600" -WindowStyle Hidden
  Write-Host ("Relaunched Analista cron (ExecTimeout=600s): " + $cron)
} else {
  Write-Host ("Cron script not found: " + $cron)
}
Write-Host "RECOVER_DONE"
