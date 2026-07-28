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
foreach ($f in @("analista_mailbox_cron.prompt.txt","analista_mailbox_cron.lock","analista_mailbox_cron.exec-lease.json","analista_mailbox_cron.retry.json","analista_mailbox_cron.residue-first-seen.json","analista_mailbox_cron.stop")) {
  $p = Join-Path $base $f
  try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; Write-Host ("Removed stale " + $f) }
  catch { Write-Host ($f + ": " + $_.Exception.Message) }
}

# Relanzar el cron de la Analista limpio (detached)
$cron = Join-Path $PSScriptRoot "Analista\analista_mailbox_cron.ps1"
if (Test-Path -LiteralPath $cron) {
  # ExecTimeout=3600 a proposito (NO 600): las reviews adversariales de la Analista tardan 12-37 min
  # (clone limpio + validate ~2min x2 + scan gates + analisis + verdict + commit). El 600 que se bajo
  # para MATAR RAPIDO los hangs de npm-test de CODEX mataba TODAS las reviews en el deadline (evidencia:
  # 4/4 execs killed reason=deadline a exactamente 600s, 0/0-byte por --output-format text = muerte muda).
  # Los timeouts son PER-AGENTE: Codex se queda en 600 (execs de implementacion rapidos + ventana
  # post-entrega); la Analista necesita 3600. Las reviews salen solas al terminar (~15-20 min tipico);
  # el 3600 es solo tope de seguridad. Diagnostico: 2026-07-28 (ver project-state-snapshot).
  Start-Process powershell -ArgumentList "-NoProfile","-File",$cron,"-ExecTimeoutSeconds","3600","-AgentModel","claude-opus-4-8" -WindowStyle Hidden
  Write-Host ("Relaunched Analista cron (ExecTimeout=3600s, AgentModel=claude-opus-4-8): " + $cron)
} else {
  Write-Host ("Cron script not found: " + $cron)
}
Write-Host "RECOVER_DONE"
