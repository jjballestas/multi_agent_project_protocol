# AUTODRIVE - progreso de los 9 requisitos PROPOSED de Zeus (operador ausente)

> Tracker del drive autonomo. Cron cada ~5 min. Counter de rondas-sin-respuesta de Codex (parar a 7).
> Stand-down al terminar los 9: ordenar a Codex parar su cron + parar el mio.

## Reglas (operador)
- Monitoreo cada ~5 min para coordinar con Codex.
- Si 7 RONDAS SEGUIDAS del cron sin respuesta de Codex -> detener el cron (stand-down parcial + FYI).
- Al terminar el desarrollo (los 9 done) -> ordenar a Codex parar su cron + parar el mio.
- De a UNA tarea (anti-colision). Cada cierre: checker verde clon limpio + promover el siguiente del orden.

## Cron
- job_id: b5085d65 (every 5 min, session-only, auto-expira 7 dias; el previo 276658d4 se detuvo a las 7 rondas y se relanzo). Stand-down = CronDelete b5085d65 (o CronList).

## Counter
- rounds_without_codex_response: 0   (reset a 0 cada vez que hay actividad de Codex: delivery/commit/mailbox)

## Orden y estado
| # | REQ | AC / DECISION | TASK | estado |
|---|-----|---------------|------|--------|
| 1 | REQ-C1976857 (refetch al navegar)        | AC29            | TASK-0140 | DONE (checker verde; Zeus 60fdb97; npm 31/31) |
| 2 | REQ-547C6C54 (frescura/staleness)        | AC30            | TASK-0141 | DONE (checker verde; Zeus 88b4604; npm 33/33) |
| 3 | REQ-4120B017 (tooltips badges)           | AC31            | TASK-0142 | DONE (checker verde; Zeus cb4c0b1; npm 34/34) |
| 4 | REQ-3E31293F (tooltips RF-N/acronimos)   | AC32            | TASK-0143 | DONE (checker verde; Zeus 8e41461; npm 35/35) |
| 5 | REQ-D2C6579F (Mermaid render Help)       | AC33            | TASK-0144 | DONE (checker verde; Zeus 4ee322b; npm 36/36) |
| 6 | REQ-28118FC3 (tipografia Mailbox/Backlog)| AC34            | TASK-0145 | DONE (checker verde; Zeus 5f53224; npm 37/37) |
| 7 | REQ-B97838C6 (kanban colapsar/done)      | AC35            | TASK-0146 | DONE (checker verde; Zeus 90ea26b; npm 38/38) |
| 8 | REQ-9AF54A75 (filtros Ledger)            | AC36            | TASK-0147 | PROMOVIDO ready, GO emitido (esperando in_review) |
| 9 | REQ-31100EAF (carga por archivo)         | DECISION-0055 + AC37/AC38 | - | pendiente (LAST; OFF/gated; Analista al cierre). PRE-AUTH del operador REGISTRADA: al cerrar con Analista OK dejar ingestion RUNTIME-READY (versionado OFF, env) SIN otro GO; si Analista pide cambios, NO aplica |

## Drafts canonicos
- PLAN-9req-zeus-orden.md ; DRAFT-SPEC-0086-ext7-ux-batch.md (AC29-AC36) ; DRAFT-DECISION-0055-file-ingestion.md ;
  DRAFT-SPEC-0086-ext8-file-intake.md (AC37/AC38). Commit be25260.
