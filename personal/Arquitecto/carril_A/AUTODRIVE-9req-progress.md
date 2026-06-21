# AUTODRIVE - progreso de los 9 requisitos PROPOSED de Zeus (operador ausente)

> Tracker del drive autonomo. Cron cada ~5 min. Counter de rondas-sin-respuesta de Codex (parar a 7).
> Stand-down al terminar los 9: ordenar a Codex parar su cron + parar el mio.

## Reglas (operador)
- Monitoreo cada ~5 min para coordinar con Codex.
- Si 7 RONDAS SEGUIDAS del cron sin respuesta de Codex -> detener el cron (stand-down parcial + FYI).
- Al terminar el desarrollo (los 9 done) -> ordenar a Codex parar su cron + parar el mio.
- De a UNA tarea (anti-colision). Cada cierre: checker verde clon limpio + promover el siguiente del orden.

## Cron
- job_id: 276658d4 (every 5 min, session-only, auto-expira 7 dias). Stand-down = CronDelete 276658d4 (o CronList).

## Counter
- rounds_without_codex_response: 0   (reset a 0 cada vez que hay actividad de Codex: delivery/commit/mailbox)

## Orden y estado
| # | REQ | AC / DECISION | TASK | estado |
|---|-----|---------------|------|--------|
| 1 | REQ-C1976857 (refetch al navegar)        | AC29            | TASK-0140 | PROMOVIDO ready, GO emitido (esperando in_review) |
| 2 | REQ-547C6C54 (frescura/staleness)        | AC30            | -         | pendiente (depende de #1) |
| 3 | REQ-4120B017 (tooltips badges)           | AC31            | -         | pendiente |
| 4 | REQ-3E31293F (tooltips RF-N/acronimos)   | AC32            | -         | pendiente |
| 5 | REQ-D2C6579F (Mermaid render Help)       | AC33            | -         | pendiente |
| 6 | REQ-28118FC3 (tipografia Mailbox/Backlog)| AC34            | -         | pendiente |
| 7 | REQ-B97838C6 (kanban colapsar/done)      | AC35            | -         | pendiente |
| 8 | REQ-9AF54A75 (filtros Ledger)            | AC36            | -         | pendiente |
| 9 | REQ-31100EAF (carga por archivo)         | DECISION-0055 + AC37/AC38 | - | pendiente (LAST; OFF/gated; Analista al cierre; live=GO operador) |

## Drafts canonicos
- PLAN-9req-zeus-orden.md ; DRAFT-SPEC-0086-ext7-ux-batch.md (AC29-AC36) ; DRAFT-DECISION-0055-file-ingestion.md ;
  DRAFT-SPEC-0086-ext8-file-intake.md (AC37/AC38). Commit be25260.
