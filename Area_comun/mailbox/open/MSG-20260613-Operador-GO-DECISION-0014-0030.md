---
message_id: MSG-20260613-Operador-GO-DECISION-0014-0030
type: GO
task_id: DECISION-0014,DECISION-0030
from: operador humano
to: Claude,Codex
status: open
requires_response: false
response_owner: none
one_line_summary: GO aprobado para DECISION-0014 (poda sistematica) e integración en CI + DECISION-0030 (slim-views cold-start). Ambas aditivas, off-by-default, medidas. Backlog: SPEC + TASK encolar tras convergencia. Proxima: Claude -> SPEC + Codex -> implementacion.
requested_action: Claude redacta SPEC-0076+ para slim-views (campos, drift-check extension, coldstart_globs). Codex implementa tras SPEC (materializacion, rotacion log, medicion antes/despues). Ambas off-by-default, con flag de activacion opt-in.
context_refs:
  - Area_comun/decisions/DECISION-0014-poda-sistematica.md
  - Area_comun/decisions/DECISION-0030-slim-views-y-cold-start.md
---

# GO — DECISION-0014 (poda en CI) + DECISION-0030 (slim-views) APROBADAS

**Aprobación operador: AMBAS DECISIONES AUTORIZADAS PARA IMPLEMENTACION.**

## DECISION-0014 — Mantenimiento sistemático (poda por umbral medido)

**Status:** ACCEPTED (2026-06-06) → **GO para implementación en CI y automatización**

- Integrar `prune_state.py --check` en post-commit hook o CI pre-merge
- Hard-fail si released_ratio >= threshold sin aprobacion manual
- Automatizar el --apply post-turno (post-release task, pre-push)
- Medir antes/despues (DECISION-0008)

## DECISION-0030 — Slim-views y politica de cold-start just-in-time

**Status:** PROPOSED (2026-06-13) → **ACCEPTED** (2026-06-13) → **GO para diseño e implementacion**

**Problema:** cold-start carga ~19.5k tokens de archivos full completos; context rot persiste. 
**Palanca:** slim-views derivadas (proyecciones de campos selectos) + politica just-in-time.

### Slim-views a materializar:

1. **TASK_INDEX.slim.json:** solo `{id, status, owner, phase, priority, title, blocked_by_questions?}` para tareas vivas
2. **PROJECT_STATE.slim.json:** narrativa recortada a ventanas `recent_*`; `active_tasks` reducido
3. **CLAIMS.slim.json:** solo claims `active` con `{claim_id, task_id, owner, scope}`

### Politica just-in-time:

- `coldstart_globs` apunta a `*.slim.json` + AGENTS.md + README + TASK_PROTOCOL (DEJA fuera full + event log)
- Evento log nunca al cold-start (snapshot.json es base)
- Detalle se recupera on-demand del TASK-XXXX.md / DECISION-XXXX.md / handoff concreto

### Integridad:

- Slim-views = **derivadas, regenerables, sin pérdida**; el full + archive siguen siendo autoritativos
- Drift checker extendido: slim no diverge del snapshot o aborta con rollback
- Gate de medición: cold-start < 10k tokens con slim (vs ~19.5k actual)

### Aditivo + Off-by-default:

- Flags de activacion opt-in por instancia
- SemVer: MINOR
- Neutral de dominio (proyecciones genéricas, no business logic)

## Backlog (secuencia)

1. **SPEC (Claude):** contrato exacto de cada slim-view, extension drift-checker, ajuste coldstart_globs, golden cases
2. **TASK (Codex, tras SPEC):** materializacion en submit_intent, rotacion events.jsonl, medicion before/after

## Siguiente paso

1. Claude redacta SPEC (estimado 2-3 horas de diseño)
2. Codex implementa (tras SPEC closed, estimado 4-6 horas)
3. Medir delta antes/despues; solo entonces activar en esta instancia (si delta confirma < 10k)

---

*GO emitido por operador. Ambas decisiones autorizadas. SPEC + TASK encolarán tras convergencia.*
