---
task_id: TASK-0175
title: "Reconciliar backlog: marcar done los 9 REQ ya entregados por TASK-0171 (US-4) y TASK-0172 (cluster RC)"
type: implementation
status: in_review
owner: Codex
phase: P2
priority: normal
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
file: Area_comun/tasks/TASK-0175-codex-reconcile-rc-us4-reqs.md
---

# TASK-0175 - Reconciliar 9 REQ entregados a done

> El backlog se ve lleno: 9 REQ siguen proposed pero su feature ya se entrego. requirement->done exige
> implementer (solo Codex). maker=Codex / checker=Arquitecto. Bajo #4 enforce ON. Igual patron que TASK-0170.

## Accion
Por cada REQ abajo, `submit_intent` `task_status` `from: proposed` `to: done` (atomico; claim file-scoped por REQ:
TASK_INDEX.json#<REQ>, PROJECT_STATE.json#active_tasks/<REQ>, y el seed req-<id>-requirement-seed.md). El estado del
seed lo sincroniza submit_intent.

### Mapeo REQ -> tarea entregadora (verificado por el Arquitecto)
- **Entregados por TASK-0172 (cluster RC, rediseno Intake):** REQ-EE0CA804 (RC-01), REQ-3F85B44C (RC-02),
  REQ-E0606D12 (RC-03), REQ-FA303A81 (RC-03 dup), REQ-1C7B4275 (RC-04), REQ-B6146E35 (RC-04 dup), REQ-E6B404D5
  (RC-05), REQ-01193FD6 (RC-06).
- **Entregado por TASK-0171 (US-4 worker de producto + modelo):** REQ-4A88ECFFC4.

(9 REQ en total. NO tocar REQ-520BBC1888 (US-5, gated) ni REQ-C1EDD835 (nuevo, sin entregar) ni REQ-D642E4D8
(in_progress, del operador) ni TASK-0118.)

## DoD
- Los 9 REQ pasan a done (indice + seed consistentes). validate con/sin secretos exit 0; drift 0; neutralidad+
  encoding 0; #4 byte-identica. US-5/C1EDD835/D642E4D8/0118 intactos. Reproducido por el checker (Arquitecto).
