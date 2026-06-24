---
task_id: TASK-0170
title: "Reconciliar backlog: marcar done los 15 REQ ya entregados por TASK-0165/0166/0167 (cada uno ligado a su tarea entregadora)"
type: implementation
status: in_review
owner: Codex
phase: P2
priority: normal
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
file: Area_comun/tasks/TASK-0170-codex-reconcile-delivered-reqs.md
---

# TASK-0170 - Reconciliar 15 REQ entregados a done

> Reconciliacion de backlog: 15 REQ siguen `proposed` pero su feature YA se entrego (TASK-0165/0166/0167 DONE).
> `requirement -> done` exige `implementer` (solo Codex). maker=Codex / checker=Arquitecto. Bajo #4 enforce ON.

## Accion

Por cada REQ abajo, emitir `submit_intent` `task_status` `from: proposed` `to: done` (atomico, en una o pocas
transacciones; claim file-scoped con grano fino por REQ: `TASK_INDEX.json#<REQ>`, `PROJECT_STATE.json#active_tasks/<REQ>`,
y el seed `Area_comun/tasks/req-<id-lower>-requirement-seed.md`). El estado del seed lo sincroniza submit_intent;
si no, ajustarlo a `status: done` para casar indice/archivo. Opcional: anotar en cada seed `delivered_by: <TASK>`.

### Mapeo REQ -> tarea entregadora (verificado por el Arquitecto por titulo/contenido)

- **Entregados por TASK-0167 (front UX polish cluster):**
  - REQ-07DD94CE (busqueda Artifacts), REQ-11A2A57C (hash routing), REQ-16BDAA88 (inline Operate),
    REQ-524372E9 (KPIs contextuales), REQ-7857CDE9 (modal Intake), REQ-A4B9FE80 (chips Backlog),
    REQ-CD4CE3F1 (agrupacion Mailbox).
- **Entregados por TASK-0166 (Q1 control de runtime):**
  - REQ-9442785DD6 + REQ-DCFB1AA7 (vivo/dormido + activar/detener; DCFB1AA7 es duplicado),
    REQ-885632826E + REQ-95B96D25 (Enviar al Arquitecto; 95B96D25 es duplicado).
- **Entregados por TASK-0165 (Q2 consola de prompts / mailbox_send):**
  - REQ-269EBF78 + REQ-68896287BC (consola de prompts; 68896287BC es duplicado),
    REQ-A54DAD73 + REQ-E782911A (compositor mailbox_send; E782911A es duplicado).

(15 REQ en total. Los duplicados tambien se marcan done: su requisito quedo satisfecho por la misma entrega.)

## DoD

- Los 15 REQ pasan a `status: done` en TASK_INDEX (indice y archivo seed consistentes). validate con/sin secretos
  exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica (no toca config). Sin tocar los 2 REQ pendientes
  (REQ-4A88ECFFC4 US-4, REQ-520BBC1888 US-5) ni TASK-0118.
- Reproducido por el checker (Arquitecto): los 15 quedan done, los 2 pendientes intactos, gates verdes.

## Notas

- Es reconciliacion mecanica de estado (las features ya estan en producto y atestadas). No hay codigo de
  producto que tocar.
