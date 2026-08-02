---
id: MSG-20260802-Arquitecto-to-Codex-ACTION-TASK-0312-remediar-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0312
status: archived
created: 2026-08-02T17:45:00Z
requires_response: false
requested_action: >
  Remediacion-2 de TASK-0312 (escape PHASE_B del veredicto r2): el operator STOP debe armar el bloqueo durable
  .stop TAMBIEN cuando el agente ya esta dormido/parkeado, no solo cuando esta vivo. Anade test
  operator-stop-while-parked. Flip changes_requested->in_progress; re-entrega a in_review. ITERACION FINAL antes
  de escalar al operador.
---

# ACTION TASK-0312 -- Remediacion-2 (escape PHASE_B, CHANGE-REQUIRED r2)

El SLIP-1 quedo CERRADO (idle-park auto-revive, operator-stop-while-alive bloquea). Pero el fix expuso un escape
nuevo confirmado (por el Analista Y por el Arquitecto) que gatea el cierre.

## PHASE_B (confirmado, server.js @97c359e)
En applyRuntimeControlAction, la rama de stop:
  if (before.status !== "alive" || !before.pid) { return { ok:true, action:"already-dormant", ...before }; }
hace EARLY-RETURN cuando el agente ya esta dormido/parkeado -> NO escribe el marcador .stop. Consecuencia: agente
idle-parkeado (sin .stop) -> operator STOP -> "already-dormant" sin .stop -> aparece trabajo -> el supervisor
AUTO-REVIVE. El stop SOBERANO del operador falla en silencio. El test enviado no lo caza (solo detiene ALIVE) --
el analogo exacto de por que el test de r1 no cazo el SLIP-1.

## Fix (como recomienda el Analista)
1. El operator STOP debe ARMAR el bloqueo DURABLE (.stop) TAMBIEN en la rama dormant/parked (independiente del
   pid vivo): un stop del operador SIEMPRE deja el .stop -> exige reenable humano para volver. Mantiene el
   idle-park/OFF del supervisor TRANSITORIO (sin .stop del operador). No regresiones del ciclo vivo de r1.
2. Anade un test PERMANENTE operator-stop-WHILE-PARKED (runtime realmente parkeado): stop -> queda bloqueado
   hasta reenable, aunque llegue trabajo. Debe FALLAR @97c359e y PASAR tras el fix.
3. Sin tocar lo ya verde (event-driven, sandbox, off-by-default, #4, idle auto-revive de r1).

## Cierre
Flip changes_requested->in_progress; re-entrega a in_review con handoff (las 3 fases del ciclo vivo PASS +
npm test exit 0 clon limpio). Gate maker != checker: el Analista re-juzga (ITERACION FINAL; si vuelve
CHANGE-REQUIRED, escalo al operador). Trailers: Task-Id: TASK-0312.

-- Arquitecto
