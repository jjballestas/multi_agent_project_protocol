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

# Limpiar el prompt.txt obsoleto (ahora deberia estar desbloqueado) + el estado de reintentos-agotados
# (retry.json) y residue-first-seen.json, que PERSISTEN en disco y hacen que las tareas pendientes queden
# como no-procesables tras un restart. NO se toca seen.json (mensajes legitimamente consumidos).
$rt = Join-Path $PSScriptRoot "..\.protocol-tmp\codex_mailbox_cron"
foreach ($f in @("codex_mailbox_cron.prompt.txt","codex_mailbox_cron.retry.json","codex_mailbox_cron.residue-first-seen.json")) {
  $p = Join-Path $rt $f
  try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; Write-Host ("Removed stale " + $f) }
  catch { Write-Host ($f + ": " + $_.Exception.Message) }
}

# Relanzar el cron de Codex limpio (detached)
$cron = Join-Path $PSScriptRoot "Codex\codex_mailbox_cron.ps1"
if (Test-Path -LiteralPath $cron) {
  # ExecTimeout=1800 / PostDelivery=600 (operador aprobo 2026-07-28, reversa del 600/300 previo).
  # Evidencia: el 600/300 mataba hasta el CIERRE de un done-flip trivial (el post-delivery de 300s corto a
  # Codex durante memory-persist+commit) y hacia imposible la remediacion de 0298 (clone Zeus + fix + node
  # --test). La proteccion anti-hang real ya la da TASK-0300 (tree-kill de arbol completo + bound post-entrega),
  # asi que el 600 crudo ya no hace falta como defensa. Codex es per-agente. Ver leccion analista-review-timeout.
  Start-Process powershell -ArgumentList "-NoProfile","-File",$cron,"-ExecTimeoutSeconds","1800","-PostDeliveryTimeoutSeconds","600" -WindowStyle Hidden
  Write-Host ("Relaunched Codex cron (ExecTimeout=1800s, PostDeliveryTimeout=600s): " + $cron)
} else {
  Write-Host ("Cron script not found: " + $cron)
}
Write-Host "RECOVER_DONE"
