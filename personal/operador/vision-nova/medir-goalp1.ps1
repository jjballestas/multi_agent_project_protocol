# medir-goalp1.ps1 - wrapper de conveniencia para medir el piloto GOAL-P1 (PowerShell)
# El asesor DISENA; TU (Operador) lo corres. La atestacion del sha256 la hace el Arquitecto.
#
# Uso (desde cualquier carpeta):
#   .\personal\operador\vision-nova\medir-goalp1.ps1 abrir
#   .\personal\operador\vision-nova\medir-goalp1.ps1 actualizar -ReworksN 1
#   .\personal\operador\vision-nova\medir-goalp1.ps1 cerrar -TokensDev 12000 -TokensTotal 12000 -FechaFin 2026-07-08
#   .\personal\operador\vision-nova\medir-goalp1.ps1 verificar
#
# NOTA: confirma la ruta del corpus ($Corpus) con el Arquitecto (es su corpus + el atesta).
#       Si 'python' no resuelve, cambia $Py a 'py'.

param(
  [Parameter(Mandatory=$true, Position=0)]
  [ValidateSet('abrir','actualizar','cerrar','verificar')]
  [string]$Accion,
  [int]$TokensDev = 0,
  [int]$TokensTotal = 0,
  [int]$ReworksN = 0,
  [string]$FechaFin = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = "D:\Agentes\multi_agent_project_protocol"
$Corpus   = "personal/Arquitecto/TFM-medicion/corpus/medicion"
$Ledger   = "$Corpus/medicion_ledger.py"
$Py       = "python"   # cambia a 'py' si 'python' no resuelve
$Hoy      = Get-Date -Format 'yyyy-MM-dd'
$Fecha    = if ($FechaFin) { $FechaFin } else { $Hoy }

Set-Location $RepoRoot

switch ($Accion) {
  'abrir' {
    Write-Host "Abriendo fila GOAL-P1 (baseline, fundacion, estimate L)..." -ForegroundColor Cyan
    & $Py "$Ledger" nueva-fila --corpus "$Corpus" --set tarea_id=GOAL-P1 --set brazo=baseline --set par_id=NA --set estimate_previo_SML=L --set criticidad=fundacion --set "fecha_commit_estimate=$Hoy"
  }
  'actualizar' {
    Write-Host "Actualizando fila GOAL-P1 (orchestration_mode=mono, reworks_n=$ReworksN)..." -ForegroundColor Cyan
    & $Py "$Ledger" actualizar --corpus "$Corpus" --clave GOAL-P1 --set orchestration_mode=mono --set "reworks_n=$ReworksN"
  }
  'cerrar' {
    Write-Host "Cerrando fila GOAL-P1 (done, tokens_dev=$TokensDev, total=$TokensTotal, fecha_fin=$Fecha)..." -ForegroundColor Cyan
    & $Py "$Ledger" cerrar-fila --corpus "$Corpus" --clave GOAL-P1 --set estado_final=done --set "fecha_fin=$Fecha" --set "tokens_dev=$TokensDev" --set "tokens_total_atribuibles=$TokensTotal" --atestar
  }
  'verificar' {
    Write-Host "Verificando + sha256 (pasa el sha256 al Arquitecto para atestar)..." -ForegroundColor Cyan
    & $Py "$Ledger" verificar --corpus "$Corpus"
    & $Py "$Ledger" sha256 --corpus "$Corpus"
  }
}
