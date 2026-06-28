# Recovery: mata instancias zombie del cron de Codex (identificadas por command line) y relanza limpio.
# Lanzado por el Arquitecto bajo permiso Bash(powershell -NoProfile -File personal/*.ps1:*) (operador autorizo).
# Seguro: solo toca powershell cuyo command line contiene 'codex_mailbox_cron' (NO el Analista, NO la sesion Claude).
$ErrorActionPreference = "Continue"
$me = $PID
$killed = @()
try {
  Get-CimInstance Win32_Process -Filter "name='powershell.exe'" |
    Where-Object { $_.CommandLine -and ($_.CommandLine -like '*codex_mailbox_cron*') -and ($_.ProcessId -ne $me) } |
    ForEach-Object {
      Write-Host ("Killing stuck Codex cron PID " + $_.ProcessId)
      Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
      $killed += $_.ProcessId
    }
} catch { Write-Host ("CIM query failed: " + $_.Exception.Message) }
Write-Host ("Killed PIDs: " + ($killed -join ','))
Start-Sleep -Seconds 3

# Limpiar el prompt.txt obsoleto (ahora deberia estar desbloqueado)
$promptFile = Join-Path $PSScriptRoot "..\.protocol-tmp\codex_mailbox_cron\codex_mailbox_cron.prompt.txt"
try {
  Remove-Item -LiteralPath $promptFile -Force -ErrorAction Stop
  Write-Host "Stale prompt.txt removed (lock cleared)."
} catch { Write-Host ("prompt.txt still locked or absent: " + $_.Exception.Message) }

# Relanzar el cron de Codex limpio (detached)
$cron = Join-Path $PSScriptRoot "Codex\codex_mailbox_cron.ps1"
if (Test-Path -LiteralPath $cron) {
  Start-Process powershell -ArgumentList "-NoProfile","-File",$cron -WindowStyle Hidden
  Write-Host ("Relaunched Codex cron: " + $cron)
} else {
  Write-Host ("Cron script not found: " + $cron)
}
Write-Host "RECOVER_DONE"
