---
task_id: TASK-0140
title: "Proyecto-front (UX): refetch fresco al navegar entre vistas (sin F5) + boton de recarga manual + refresco por intervalo opt-in (AC29, SPEC-0086 ext7)"
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
file: Area_comun/tasks/TASK-0140-codex-front-refetch-nav.md
---

# TASK-0140 - Refetch fresco al navegar (SPEC-0086 ext7, AC29; REQ-C1976857)

> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. UX READ-ONLY (sin nueva superficie de escritura).
> #1 del PLAN de los 9 requisitos PROPOSED. carry AC11/AC12/AC13/AC17.

## Alcance
1. Al activar un nav-item, la vista hace fetch fresco al server (observe) y re-renderiza con el dato actual,
   sin requerir F5: Ledger seq, conteo Backlog, Mailbox, barra de integridad reflejan el canonico ACTUAL.
2. Boton de recarga manual por seccion.
3. Refresco por intervalo configurable (opt-in; sin intervalo no hay polling).

## DoD
- AC29 verde con test de COMPORTAMIENTO permanente (navegar dispara fetch + re-render; intervalo respetado; sin
  intervalo no hay polling; fetch fallido -> estado de error, no stale-as-fresh). Carry AC11/AC12/AC13/AC17.
- Read-only: no toca submit_intent ni abre superficie de escritura.
- node --test/CI verde; npm start ejecutable; #4 epoca 1.14.0 byte-identica; validate con/sin secretos exit 0;
  drift 0; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Fuera de alcance
- Cualquier cambio de superficie de escritura (UX read-only).
- El indicador de frescura/staleness (es el #2 = REQ-547C6C54/AC30, tarea aparte que construye sobre esta).
