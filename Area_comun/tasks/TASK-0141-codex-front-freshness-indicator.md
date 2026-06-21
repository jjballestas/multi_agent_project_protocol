---
task_id: TASK-0141
title: "Proyecto-front (UX): indicador de frescura ('actualizado hace Ns') + spinner de carga + estado STALE (AC30, SPEC-0086 ext7)"
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
file: Area_comun/tasks/TASK-0141-codex-front-freshness-indicator.md
---

# TASK-0141 - Indicador de frescura + staleness (SPEC-0086 ext7, AC30; REQ-547C6C54)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #2 del PLAN. Construye sobre TASK-0140 (AC29).
> carry AC11/AC12/AC13/AC17.

## Alcance
1. Barra de integridad / pie de seccion muestra "actualizado hace Ns" derivado del timestamp REAL del ultimo
   fetch exitoso.
2. Durante una carga, spinner/indicador sutil.
3. Si el dato es STALE (> N s sin refrescar), el indicador cambia de estado visual.

## DoD
- AC30 verde con test de COMPORTAMIENTO permanente (tras fetch -> muestra antiguedad; pasado el umbral -> STALE;
  durante carga -> spinner; nunca pinta fresco un dato viejo). Carry AC11/AC12/AC13/AC17.
- Read-only: no toca submit_intent ni abre superficie de escritura.
- node --test/CI verde; #4 epoca 1.14.0 byte-identica; validate con/sin secretos exit 0; drift 0;
  neutralidad/encoding limpio. Reproducido por el checker desde clon limpio; maker!=checker. Commit como
  Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Cualquier superficie de escritura (UX read-only). El refetch al navegar ya es TASK-0140 (AC29).
