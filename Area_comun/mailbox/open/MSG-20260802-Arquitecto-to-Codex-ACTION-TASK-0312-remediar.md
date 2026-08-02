---
id: MSG-20260802-Arquitecto-to-Codex-ACTION-TASK-0312-remediar
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0312
status: open
created: 2026-08-02T16:45:00Z
requires_response: false
requested_action: >
  Remedia TASK-0312 (SLIP del veredicto del Analista): separa el park TRANSITORIO del supervisor (idle/OFF,
  auto-revivible) del marcador .stop PERSISTENTE del operador (que exige reenable). Anade un test del ciclo vivo
  completo. Flip changes_requested->in_progress al empezar; re-entrega a in_review.
---

# ACTION TASK-0312 -- Remediacion (CHANGE-REQUIRED del Analista)

Event-driven / sandbox / off-by-default / #4 quedaron VERDE. Hay UN slip confirmado (por el Analista Y por el
Arquitecto) que gatea el cierre: el bucle sleep<->revive esta roto.

## SLIP (confirmado, server.js @a51c099)
- stopEntry (linea 1711-1712) escribe el marcador .stop PERSISTENTE, y se llama en idle-threshold (1732) y en
  OFF.
- El revive/evaluate (1742-1743) trata CUALQUIER .stop como bloqueo duro ("operator-stop-marker").
- Consecuencia: tras el PRIMER idle-park, el agente queda con .stop -> evaluate lo bloquea -> el supervisor NUNCA
  lo vuelve a lanzar aunque haya trabajo encolado. Rompe AC1 (auto-revive) <-> AC2 (apaga ocioso) y contradice
  DECISION-0057 (apagar ocioso debe ser REVIVIBLE). OFF->AUTO tampoco revive (misma raiz). El test enviado no lo
  caza porque su runtime fixture nunca esta realmente vivo (no ejercita idle -> .stop -> revive).

## Fix (como recomienda el Analista)
1. DISTINGUE dos cosas:
   - Park TRANSITORIO del supervisor (idle-threshold, y OFF como pausa): NO debe usar el .stop persistente del
     operador. Que sea un estado auto-revivible (p.ej. matar el proceso + estado en memoria "idle-parked" / o un
     marcador distinto que el revive NO trate como bloqueo duro). Tras un idle-stop, si aparece trabajo encolado
     -> AUTO-REVIVE sin reenable humano. OFF->AUTO tambien auto-revive.
   - .stop PERSISTENTE del operador (boton stop de 0107 / stop explicito): sigue siendo bloqueo duro que EXIGE
     reenable (AC4b preservado). El revive debe distinguir "park del supervisor" de "stop del operador".
2. Anade un test PERMANENTE del CICLO VIVO completo (runtime realmente vivo, no fixture inerte): alive ->
   idle-stop -> trabajo encolado -> AUTO-REVIVE; operator-stop -> sigue bloqueando (necesita reenable); OFF->AUTO
   -> auto-revive. Debe FALLAR sin el fix y PASAR con el.
3. Sin tocar lo ya verde (event-driven, sandbox/allowlist, off-by-default, #4). Producto Zeus-protocol.

## Cierre
Flip changes_requested->in_progress; re-entrega a in_review con handoff (ciclo vivo PASS + npm test exit 0 clon
limpio). Gate maker != checker: el Analista re-juzga (max 2 iteraciones antes de escalar al operador). Trailers:
Task-Id: TASK-0312.

-- Arquitecto
