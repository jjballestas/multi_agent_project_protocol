---
task_id: TASK-0244
title: "[VISION-NOVA][F1.7] RELEASE v1.18.0 (CHANGELOG + tag; SIN bumpear epoch pineado)"
type: docs
status: review_approved
owner: Arquitecto
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0083]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0244-visionnova-f1g-release-1180.md
intake:
  type: doc
  goal: Release v1.18.0 (CHANGELOG + tag SemVer sobre commit verde en clon limpio) SIN bumpear el epoch pineado; templates sincronizados con las reglas F1.
  acceptance:
    - CHANGELOG.md actualizado a v1.18.0 con las entradas F1 (intake gate, exception.recorded, trailers, taxonomia, envelope+fixloop, DECISION-0084).
    - Tag v1.18.0 creado sobre commit con los 3 gates verdes en clon limpio.
    - Templates (.template.*) sincronizados con intake / exception / trailers / envelope.
    - protocol.config.json byte-identico (epoch 1.14.0 PINNED, DECISION-0047).
    - FYI al operador con el tag y el estado de activacion de trailers.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - CHANGELOG.md
    - AGENTS.template.md
    - Area_comun/protocol/
  out_of_scope:
    - NO bumpear protocol_version/epoch ni tocar protocol.config.json (re-genesis coordinada unica via DECISION-0047).
    - La activacion del trailer_start_seq es un paso explicito SEPARADO (COMMIT_TRAILERS.json tras relanzar crons con prompts 0242), no parte del tag.
    - No relanza crons (gate de permisos del operador).
  risk: medium
  estimate: M
---

# TASK-0244 - [VISION-NOVA][F1.7] RELEASE v1.18.0

Owner: Arquitecto. Cierra F1. Este tag lo consume F2.1 (TASK-0230, new_instance nova-budget).

## CONDICION (hallazgo F-4 del Arquitecto, ya en backlog v2)
v1.18.0 es la LINEA DE RELEASE (CHANGELOG + tag SemVer), NO el epoch. El epoch
`protocol.config.json` permanece PINNED en 1.14.0 (genesis #4); F1-G NO lo bumpea ni toca el
config pineado (DECISION-0047, versionado en dos ejes).

## DoD (testable)
1. CHANGELOG actualizado a v1.18.0.
2. Tag v1.18.0 sobre commit con los 3 gates verdes en clon limpio.
3. Templates sincronizados con las reglas nuevas (intake / exception / trailers / envelope).
4. protocol.config.json byte-identico (epoch 1.14.0). FYI al operador.
