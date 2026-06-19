---
id: TASK-0126
title: Proyecto-front MVP etapa 2 - Observar (RF-1..RF-4 read-only sobre el canonico) (DECISION-0049 / SPEC-0086)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0029, DECISION-0047]
created_at: 2026-06-20
---

# TASK-0126 - Proyecto-front MVP etapa 2 (Observar)

## Objective

Etapa 2 del MVP single-operator (SPEC-0086), sobre el scaffold de etapa 1 (TASK-0124, done). En
`D:\Agentes\Zeus\Zeus-protocol`, **vistas READ-ONLY sobre el canonico** del protocolo: RF-1 dashboard
(TASK_INDEX backlog, CLAIMS, PROJECT_STATE, version/epoca, drift verde/rojo), RF-2 mailbox (open/answered/
archived, requires_response), RF-3 artefactos navegables (decisiones/specs/tasks/handoffs/reports por id +
*_refs), RF-4 ledger #4 / procedencia (timeline atestado: seq, actor, firma verificada, prev_hash, anclaje;
badge atestado; drift). Usa el diseno UI de Claude Design en `D:\Agentes\Zeus\Zeus-protocol\design\interface\`
(design-system/tokens + componentes dashboard/kanban/timeline/claims-table/badges/canonical-indicator).
maker=Codex, checker=Arquitecto.

## Alcance (SPEC-0086 etapa 2, RF-1..RF-4)

- SOLO LECTURA del canonico (git show / objetos git, NO el working tree volatil). NINGUNA escritura
  (operar = etapa 3, via submit_intent). Reflejar epoca/version/drift deterministas.
- RF-4 atestacion: la verificacion de firmas/cadena/anclaje del front coincide con
  validate_chain/validate_agent_signatures/verify_anchor del runtime; drift verde/rojo == protocol_state_drift.
- Codigo SOLO en Zeus-protocol; CI del producto verde; sin dependencias innecesarias; canal ASCII.

## DoD

SPEC-0086 AC1 (read-only canonico), AC3 (atestacion correcta), AC5 (integridad fuente), AC6 (neutralidad/
acoplamiento), AC7 (CI verde), AC9 (determinismo), AC10 (gates protocolo) aplicables a etapa 2; maker=Codex/
checker=Arquitecto; sin escritura directa; sin tocar #4/config. Reporta a in_review con claim file-scoped +
submit_intent.

## Verification

- CI del producto verde (node --test); las vistas leen el canonico read-only (sin escritura directa al
  ledger; prueba estatica); atestacion coincide con el runtime.
- `validate_collaboration_state.py --root .` (con y sin secretos) + scans del protocolo exit 0; drift 0.
