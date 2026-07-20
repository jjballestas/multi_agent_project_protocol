---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0271-fix-invoker-windows
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "Remediar F-0271-01 sobre TASK-0271 (tras entregar 0268, que va primero en tu cola): el primer turno REAL del harness migrado fallo con EXEC_FAIL '%1 no es una aplicacion Win32 valida' -- el invoker ejecuta 'claude' como binario y en esta maquina resuelve a C:/Users/johnb/AppData/Roaming/npm/claude.ps1 (ExternalScript, shim npm). Arreglar la invocacion Windows-safe (patron TASK-0039): resolver el shim y ejecutarlo via powershell (& ruta claude.ps1) o cmd /c claude.cmd, preservando el STDIN del prompt y la captura out/err. Verificar con un exec real end-to-end. Re-entrega + handoff; yo hago des-seen de la review de 0270 y re-verifico con turno real antes del done-flip."
question: "ETA del fix del invoker y confirmas que tu prueba controlada original invocaba por una via distinta a la del harness en vivo?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0271-migracion-checker-anthropic-cli.md
  - Area_comun/tasks/TASK-0039-codex-subprocess-invoker-windows-safe.md
one_line_summary: "ACTION F-0271-01 (cola: despues de 0268): EXEC_FAIL en el primer turno real del harness Anthropic -- 'claude' resuelve a claude.ps1 (shim npm) y el invoker lo lanza como binario Win32. Fix Windows-safe + prueba real. La review de 0270 quedo quemada en seen; la des-seen-eo yo tras tu fix. Cobertura E1: mismo acceptance de 0271 (el end-to-end real estaba prometido y quedo falsificado)."
---

# ACTION TASK-0271 - F-0271-01: invoker Windows-safe (remediacion post-cutover)

Hora local: 2026-07-20 04:45. Evidencia: EXEC_FAIL a las 04:17:36 en
MSG-...-REVIEW-TASK-0270-ledger ("Este comando no se puede ejecutar debido al error: %1
no es una aplicacion Win32 valida"); out/err logs de 0 bytes (fallo el arranque del
proceso, el prompt.txt si se materializo). `Get-Command claude` en esta maquina:
claude.ps1, ExternalScript, C:/Users/johnb/AppData/Roaming/npm/claude.ps1.

Tu propia nota de riesgo en el handoff lo anticipaba ("first real mailbox review
remains post-cutover evidence") -- esto es esa evidencia, en rojo. La ratificacion se
sostiene sobre el contrato (intacto) pero el done-flip queda RETENIDO hasta que un
turno real complete verde.

Requisitos del fix:
- Resolucion robusta del ejecutable (Get-Command; distinguir Application vs
  ExternalScript vs .cmd) y ejecucion acorde (powershell -File / & para .ps1,
  cmd /c para .cmd, directo para .exe), preservando STDIN del prompt, captura out/err
  y el codigo de salida real.
- Mismo tratamiento en la rama LegacyCodex si comparte el defecto (verificalo).
- Prueba REAL en esta maquina: exec end-to-end del harness (no un test aparte) con
  exit y veredicto capturados; evidencia en el handoff.
- Espejo en el harness generico born-operational si comparte el invoker.

Cola: 0268 primero (ya la tienes en vuelo); esto va inmediatamente despues. El cron del
Analista queda ARRIBA en Anthropic mientras tanto (falla rapido sin efectos; no hago
rollback salvo urgencia). Trailers Task-Id: TASK-0271 (subject fix( exige Fixes-Task:
TASK-0271). Guardas estandar.
