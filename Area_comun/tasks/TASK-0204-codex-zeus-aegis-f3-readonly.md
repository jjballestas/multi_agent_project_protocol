---
task_id: TASK-0204
title: "Zeus-Aegis F3 (read-only): selector multi-proyecto + dashboard de metricas/coste read-only (DECISION-0064 F3.3/F3.4, DECISION-0050)"
type: integration
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0050, DECISION-0040]
file: Area_comun/tasks/TASK-0204-codex-zeus-aegis-f3-readonly.md
---

# TASK-0204 - Zeus-Aegis F3 read-only (selector multi-proyecto + dashboard)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Partes READ-ONLY de la Fase 3 (DECISION-0064). F1
> esta cerrado (GATE 1 cerrable). **SOLO LECTURA** (F2 write-through y F3 chat-por-runtime siguen fuera de este
> increment / gateados). Mismas reglas: lectura canonica (git), salud/atestacion derivada, PII por construccion,
> denylist intacta, core protocolo intacto, pin v2.3.0. Genera dataset elegible (seq>=2221).

## Alcance (F3 read-only)

- **Selector multi-proyecto (DECISION-0050, hub-centrico):** endpoint read-only `/api/governance/projects` que lista
  los proyectos gobernados (derivado de los `project` en TASK_INDEX / proyectos conocidos), y un selector en la UI
  que filtra las vistas de gobernanza por proyecto. Modelo ENTIDAD (id/kind), sin paths de disco crudos. Read-only.
- **Dashboard de metricas read-only:** endpoint `/api/governance/metrics` que deriva del ledger/estado canonico
  conteos seguros (p.ej. tareas por estado, eventos por method de firma, firmantes distintos, drift, salud). Vista
  dashboard con esas metricas. PII por construccion (sin texto libre). NADA de coste real de proveedor todavia
  (eso necesita el runtime; fuera de read-only).

## DoD

- AC1 endpoints projects/metrics read-only desde el CANONICO (git), sin ruta de escritura (denylist intacta).
- AC2 selector filtra las vistas por proyecto; modelo entidad sin path de disco crudo.
- AC3 dashboard renderiza metricas DERIVADAS del estado/ledger real (no hardcoded); salud/atestacion honesta (no
  verde si validate rojo).
- AC4 PII por construccion (sin texto libre en ids/labels); prueba negativa de no-escritura.
- AC5 node --test verde; gate F0 npm test exit 0 estable; core protocolo intacto; handoff a Arquitecto.

## Nota

- F3.1/F3.2 (chat por runtime) y F3.5 (PWA) NO entran aqui (no son read-only puros / mas riesgo). F2 (Operate)
  sigue gateado post-TFM.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
