---
task_id: TASK-0228
title: "[REQ-ZEUS-001][WS5] Alta del Analista en NOVA + decision mapeo rol->agente + wrapper new_instance(4 firmantes)"
type: build
status: proposed
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001]
linked_decisions: [DECISION-0072, DECISION-0073, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0228-reqzeus-ws5-alta-analista-nova.md
---

# TASK-0228 - [REQ-ZEUS-001][WS5] Alta del Analista en NOVA + 4 firmantes

- **Owner build:** Codex - **Review:** Analista - **Gobierna/mapeo:** Arquitecto
- **Repo instancia:** NOVA (`D:/Agentes/Zeus/NOVA`). Gobernanza: hub. **PRIMERO del backlog** (condiciona owner:Analista).

## Alcance
1. Extender `new_instance.py` (o wrapper) para sembrar **4 agentes** (Arquitecto, Codex, Analista, human_owner) y
   crear `personal/<id>/` de cada uno.
2. **Alta del Analista (checker)** en NOVA: registrar en `agent_roles`/`PROJECT_STATE.agents` + legend de `TASK_INDEX.json`.
3. **Decision de mapeo rol->agente** (cita NOVA-ARQ-001); `quality_policy`: `allow_self_review:false`, `allow_self_qa:false` (maker!=checker).

## DoD
- Instancia NOVA valida exit 0 con 4 agentes; una TASK `owner:Analista` es valida (validador no la rechaza).
- Decision de mapeo rol->agente existe; maker!=checker comprobable por roster.
- Tier coordination por defecto (DECISION-0072/0073). Sin tocar el core del protocolo ni los pineados. Gate Analista: GO.

## Handoff
Autocontenida. maker!=checker. Ambiguedad -> blocked + 1 pregunta concreta.
