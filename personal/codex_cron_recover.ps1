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
  # ExecTimeout=1800 (operador aprobo) / PostDelivery=1800 (subido de 600 -- el 600 era numero del Arquitecto).
  # FLAW DEL HARNESS (cazado 2026-07-28 con TASK-0299): la ventana post-entrega arranca ante CUALQUIER escritura
  # al ledger, y un GO de una tarea `ready` hace que Codex flipee ready->in_progress AL INICIO -> el post-delivery
  # de 600s arrancaba a los 3 min y mataba a Codex a mitad de IMPLEMENTACION (deadline a los 10 min). Con
  # PostDelivery=1800=ExecTimeout, la ventana post-entrega ya no mata antes del ExecTimeout (que es el bound real;
  # el tree-kill de TASK-0300 sigue limpiando zombies). Fix PROPIO pendiente: el post-delivery debe gatillar en la
  # transicion a in_review (la ENTREGA), no en cualquier escritura. Ver leccion + follow-up de TASK-0300/0302.
  Start-Process powershell -ArgumentList "-NoProfile","-File",$cron,"-ExecTimeoutSeconds","1800","-PostDeliveryTimeoutSeconds","1800" -WindowStyle Hidden
  Write-Host ("Relaunched Codex cron (ExecTimeout=1800s, PostDeliveryTimeout=1800s): " + $cron)
} else {
  Write-Host ("Cron script not found: " + $cron)
}
Write-Host "RECOVER_DONE"
