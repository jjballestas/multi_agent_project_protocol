---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0312-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0312
status: open
created: 2026-08-02T17:05:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Re-review (iteracion 2) de TASK-0312 tras la remediacion del SLIP (park vs .stop). Verifica en clon limpio del
  producto y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Foco: el ciclo vivo
  sleep<->revive cerrado y sin regresion del nucleo ya verde.
question: >
  Tras un idle-park el supervisor AUTO-REVIVE al aparecer trabajo (sin reenable humano), el operator-stop sigue
  bloqueando hasta reenable, y OFF->AUTO auto-revive; sin regresion de event-driven/sandbox/off-by-default/#4?
---

# REVIEW TASK-0312 r2 -- Remediacion del SLIP (park revivible vs .stop del operador)

Maker = Codex. Producto remediado: commit 97c359e (fix: keep supervisor parks revivable), sobre a51c099.
Ledger (hub) verde. Handoff: Area_comun/mailbox/open/MSG-20260802-Codex-to-Arquitecto-HANDOFF-TASK-0312-remediation-1.md.

## ALCANCE DE PRODUCTO (declarado)
- Repo: D:/Agentes/Zeus/Zeus-protocol (NO Nova-Budget). Commit: 97c359e.
- Gate: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0 clon limpio). Reproduce.

## Que re-verificar (foco: SLIP cerrado)
1. El SLIP (server.js): stopEntry del SUPERVISOR ya NO escribe el .stop persistente (solo mata via
   terminateRuntimeProcess); nuevo parkIfIdle (solo AUTO, sin trabajo encolado). El operator-stop
   (applyRuntimeControlAction) SIGUE escribiendo .stop (bloqueo persistente). Confirma la separacion.
2. Test PERMANENTE del ciclo VIVO (runtime realmente vivo, no fixture inerte): alive -> idle-stop -> trabajo
   encolado -> AUTO-REVIVE (sin reenable); operator-stop -> sigue bloqueando hasta reenable; OFF->AUTO ->
   auto-revive. Reproduce que FALLA contra a51c099 (pre-fix) y PASA con 97c359e.
3. SIN REGRESION del nucleo ya verde (r1): event-driven (no clock-poll), sandbox/allowlist de 0107,
   off-by-default (flag != 1 -> inerte), #4 hub byte-identico (drift 0).
4. npm test clon limpio exit 0. Sin browser -> contrato + fixtures.

## Mi capa (recompute del Arquitecto) -- ya VERDE en el fix
Lei 97c359e/src/server.js: stopEntry del supervisor ya no escribe .stop (idle-park auto-revivible); operator-stop
si escribe .stop; parkIfIdle solo AUTO + sin trabajo. SLIP resuelto. Falta tu capa independiente (npm test clon
limpio + el ciclo vivo + baseline negativo). Iteracion 2/2; emite el veredicto en Area_comun/artifacts/.

-- Arquitecto
