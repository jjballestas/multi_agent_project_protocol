---
message_id: MSG-20260705-Arquitecto-to-Operador-RESPUESTA-reset-env-hallazgos
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: false
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.14/s.15
one_line_summary: "Cron Codex relanzado (nuevo pid), TASK-0253 desbloqueada (in_progress), Codex corriendo F-NOVA-01. Enmiendas + hallazgos de seguridad registrados."
requested_action: ""
question: ""
---

# RESPUESTA - reset sandbox + env listas + hallazgos (2026-07-05 ~10:13Z / 12:13 local)

## (a) Cron de Codex relanzado
Pid viejo 140068 matado (autorizacion tuya explicita), nuevo pid 99072 vivo y confirmado en `tasklist`.
Hereda las 2 env vars de tu entorno de usuario (yo no lei ni escribi el valor en ningun momento).

## (b) TASK-0253 desbloqueada
`blocked -> in_progress` (commit `6f4132d`, pusheado). ACTION ruteada a Codex para correr F-NOVA-01 (los
8 criterios GWT de la SPEC + THROW re-verificados contra el proc desplegado, sesion con
ANSI_NULLS/QUOTED_IDENTIFIER ON + SESSION_CONTEXT tenant_id, reset por task_id entre corridas). El Asesor
ya confirma que Codex esta corriendo la verificacion en vivo.

## (c) F-NOVA-01 + cierre de P4.1
Aun en curso (Codex ejecutando). En cuanto entregue, verifico contra el checker adversarial (ya confirme
items 2/3/4 del NO-GO anterior como reales, no cosmeticos) y si F-NOVA-01 pasa, ratifico + capturo la fila
CLOSE de medicion (tokens del err.log) y ruteo el done-flip a Codex. Aviso apenas cierre.

## Enmiendas fechadas registradas (sin reabrir el sello)
- **s.14:** Reset no-admin (`Budget.Reset_Sandbox_Mutator_Baseline`) -- grant 107 -> 108.
- **s.15:** hallazgos del log de cambios con dueno: #8/auth (dueno Analista, GAP vs DD-01 -- verifique
  Program.cs, CERO auth wiring en los 8 endpoints, no solo los nuevos) + #7/transiciones-autorizacion
  (converge con #8, dueno pattern-setter P4.1) + #5/ReadOnlySqlOptions (dueno Codex, ya en su ACTION de
  F-NOVA-01) + rubric punto 7 clarificado (no cubria auth de endpoint, ahora explicito para futuros
  checkers). Resto (6 de 9) = deuda/higiene/roadmap sin dueno urgente, como triage el Asesor.

## Ruteado
- ACTION a Analista: confirma/registra el hallazgo #8 (auth) formal.
- ACTION a Codex: F-NOVA-01 + rename ReadOnlySqlOptions (mismo ciclo).

Higiene de mailbox pendiente (open/ crecio con esta cadena) -- la corro en la proxima ventana idle.
