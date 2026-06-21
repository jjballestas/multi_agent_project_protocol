---
task_id: TASK-0143
title: "Proyecto-front (UX): tooltips en codigos RF-N y acronimos tecnicos (SDD/T0/HMAC/PII...) en todas las vistas, fuente unica = glosario del Help (AC32, SPEC-0086 ext7)"
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
file: Area_comun/tasks/TASK-0143-codex-front-rfn-tooltips.md
---

# TASK-0143 - Tooltips en codigos RF-N y acronimos (SPEC-0086 ext7, AC32; REQ-3E31293F)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #4 del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Hover sobre un codigo RF-N (RF-5, RF-14...) o acronimo (SDD/T0/HMAC/PII...) en cualquier vista -> nombre
   completo; codigos interactivos (cursor pointer).
2. Diccionario = UNA fuente unica, compartida con el glosario del Help (no duplicar).

## DoD
- AC32 verde con test de COMPORTAMIENTO permanente (hover sobre RF-5/SDD/HMAC rinde el texto esperado; el set
  cubre los codigos que el front muestra). Carry AC11/AC12/AC13/AC17. Read-only.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Render de diagramas Mermaid en Help (es el #5 = REQ-D2C6579F/AC33).
- Cualquier superficie de escritura.
