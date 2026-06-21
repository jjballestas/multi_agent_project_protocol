---
task_id: TASK-0142
title: "Proyecto-front (UX): tooltips explicativos en los badges de la barra de integridad (epoch/drift/attested/canonical/validator) (AC31, SPEC-0086 ext7)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0049]
created_at: 2026-06-21
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0142-codex-front-badge-tooltips.md
---

# TASK-0142 - Tooltips en badges de integridad (SPEC-0086 ext7, AC31; REQ-4120B017)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #3 del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Hover sobre cada badge de la barra de integridad (epoch/drift/attested/canonical/validator-exit) muestra un
   tooltip corto: valor normal, que significa al cambiar, cuando preocuparse (ej. drift=0 OK, drift>0 atencion).
2. Texto consistente con el glosario del Help. Accesible (title/aria).

## DoD
- AC31 verde con test de COMPORTAMIENTO permanente (los 5 badges exponen su tooltip con el contenido esperado).
  Carry AC11/AC12/AC13/AC17. Read-only.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Tooltips de codigos RF-N/acronimos en las vistas (es el #4 = REQ-3E31293F/AC32, tarea aparte).
- Cualquier superficie de escritura.
