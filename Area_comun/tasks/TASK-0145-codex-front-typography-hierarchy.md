---
task_id: TASK-0145
title: "Proyecto-front (UX): jerarquia tipografica en Mailbox y Backlog (asunto/titulo prominente; ID tecnico secundario) (AC34, SPEC-0086 ext7)"
type: product
status: in_review
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0049]
created_at: 2026-06-21
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0145-codex-front-typography-hierarchy.md
---

# TASK-0145 - Jerarquia tipografica Mailbox/Backlog (SPEC-0086 ext7, AC34; REQ-28118FC3)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #6 del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Mailbox: asunto prominente (mayor tamano/peso); `MSG-...` secundario (mas pequeno, menor contraste).
2. Backlog: titulo de la tarea primero; `REQ-/TASK-id` en formato secundario debajo.
3. Tokens del design-system.

## DoD
- AC34 verde con test de CONFORMIDAD permanente (el id tecnico no tiene el mismo peso visual que el asunto/titulo;
  clases/tokens correctos). Carry AC11/AC12/AC13/AC17. Read-only.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Colapsar columnas del kanban / mostrar done (es el #7 = REQ-B97838C6/AC35).
- Cualquier superficie de escritura.
