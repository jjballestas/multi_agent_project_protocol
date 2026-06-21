---
message_id: MSG-20260621-Arquitecto-to-Operador-RESP-GO-SPECS-PLAN
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "Plan/orden de los 9 requisitos PROPOSED autorado y drafts canonicos (commit be25260). Orden: bloque A frescura (C1976857->547C6C54), B tooltips (4120B017->3E31293F->D2C6579F), C layout (28118FC3->B97838C6->9AF54A75), D ingestion LAST (REQ-31100EAF=DECISION-0055, OFF/gated, Analista al cierre). 8 UX = ext SPEC-0086 sin DECISION; ingestion = DECISION propia. Arranque: TASK-0140 (#1) promovido + GO a Codex. Drive autonomo (ausente): monitoreo por cron cada ~5 min, de a una tarea; paro el cron si 7 rondas seguidas sin respuesta de Codex; al terminar los 9 ordeno a Codex parar su cron y paro el mio."
context_refs:
  - personal/Arquitecto/carril_A/PLAN-9req-zeus-orden.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext7-ux-batch.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0055-file-ingestion.md
  - personal/Arquitecto/carril_A/AUTODRIVE-9req-progress.md
deadline_or_blocking_level: normal
---

# RESP - plan/orden de los 9 + arranque del drive autonomo

Autorizado y en marcha. Respondo tu pregunta (el orden) y confirmo el modo de trabajo mientras estas ausente.

## Clasificacion
- **8 UX aditivos** (read-only, sin nueva superficie de escritura) -> EXTENSIONES de SPEC-0086 (AC29-AC36),
  SIN DECISION; carry AC11/AC12/AC13/AC17.
- **1 ingestion** REQ-31100EAF -> **DECISION-0055 propia** + ext8 (AC37/AC38), OFF-by-default, reversible por
  flag, **PASADA DEL ANALISTA** (ingestion/egress) al cierre, **uso vivo = GO posterior tuyo** (no lo enciendo).

## Orden de ejecucion (de menor a mayor riesgo)
- **A. Frescura:** 1) REQ-C1976857 refetch al navegar (AC29) -> 2) REQ-547C6C54 frescura/staleness (AC30).
- **B. Tooltips:** 3) REQ-4120B017 badges (AC31) -> 4) REQ-3E31293F RF-N/acronimos (AC32) -> 5) REQ-D2C6579F
  Mermaid en Help (AC33, sin agregar dependencia de servidor).
- **C. Layout:** 6) REQ-28118FC3 tipografia (AC34) -> 7) REQ-B97838C6 kanban (AC35) -> 8) REQ-9AF54A75 filtros
  Ledger (AC36).
- **D. Ingestion (LAST):** 9) REQ-31100EAF (DECISION-0055 + AC37/AC38).

## Arranque
TASK-0140 (#1, AC29) **promovido ready/Codex + GO emitido**. Codex implementa; yo checker; cierro y promuevo
el siguiente, de a una (anti-colision).

## Modo mientras estas ausente (acuso tus reglas)
- **Monitoreo por cron cada ~5 min** para coordinar con Codex.
- **Si 7 rondas seguidas del cron sin respuesta de Codex** -> detengo el cron (dejo FYI con el estado).
- **Al terminar los 9 (todos done)** -> ordeno a Codex parar su cron y **paro el mio**.
- Cada cierre: checker verde desde clon limpio, gates (validate con/sin secretos exit 0, drift 0, #4 byte-
  identica, npm test), commit como Arquitecto + Co-Author Codex. REQ-31100EAF NO se enciende vivo sin tu GO.

Tracker del progreso: personal/Arquitecto/carril_A/AUTODRIVE-9req-progress.md. Canal ASCII.
