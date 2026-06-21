---
task_id: TASK-0146
title: "Proyecto-front (UX): kanban del Backlog - colapsar columnas vacias (count=0) y mostrar contenido de done (AC35, SPEC-0086 ext7)"
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
file: Area_comun/tasks/TASK-0146-codex-front-kanban-collapse.md
---

# TASK-0146 - Kanban: colapsar vacias + mostrar done (SPEC-0086 ext7, AC35; REQ-B97838C6)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #7 del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Columnas con count=0 -> modo compacto (solo cabecera, sin hueco).
2. Columna done MUESTRA su contenido (lista o resumen paginado, no solo el numero).
3. Ancho del kanban se adapta al contenido real.

## DoD
- AC35 verde con test de COMPORTAMIENTO permanente (columna en 0 -> compacto; done con N -> renderiza/pagina; no
  queda done con count pero sin lista). Carry AC11/AC12/AC13/AC17. Read-only.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Filtros del Ledger (es el #8 = REQ-9AF54A75/AC36).
- Cualquier superficie de escritura.
