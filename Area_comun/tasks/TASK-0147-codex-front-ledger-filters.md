---
task_id: TASK-0147
title: "Proyecto-front (UX): filtros del Ledger #4 por actor y tipo de evento + paginacion/carga progresiva (AC36, SPEC-0086 ext7)"
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
file: Area_comun/tasks/TASK-0147-codex-front-ledger-filters.md
---

# TASK-0147 - Filtros + paginacion del Ledger #4 (SPEC-0086 ext7, AC36; REQ-9AF54A75)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #8 (ultimo UX) del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Cabecera del Ledger: filtro por actor (Arquitecto/Codex/Operador) y por tipo de evento (intent.applied, etc.).
2. Al seleccionar, la lista se reduce a los coincidentes.
3. Paginacion/carga progresiva para no renderizar 900+ eventos a la vez.

## DoD
- AC36 verde con test de COMPORTAMIENTO permanente (filtrar por actor/tipo reduce la lista; la paginacion limita
  el render; sin filtro pagina por defecto). El texto libre sigue REDACTADO (no afloja PII). Carry
  AC11/AC12/AC13/AC17. Read-only sobre el ledger atestado.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Carga de requerimiento por archivo (es el #9 = REQ-31100EAF, DECISION-0055).
- Cualquier superficie de escritura / aflojar la redaccion de PII.
