---
task_id: TASK-0198
title: "Zeus-Aegis F1c - vista Artifacts (read-only) + endpoint /api/governance/artifacts; cierra el panel read-only de F1 (SPEC-0107)"
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
file: Area_comun/tasks/TASK-0198-codex-zeus-aegis-f1c-artifacts.md
---

# TASK-0198 - Zeus-Aegis F1c (vista Artifacts, ultimo increment read-only de F1)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Tercer increment de F1 (SPEC-0107). **SOLO LECTURA**
> (F2 gateado post-TFM). Cierra el panel read-only de F1. Mismas reglas: lectura CANONICA (git show), sin escritura,
> PII redactada, core protocolo intacto, pin Hermes v2.3.0. Genera dataset elegible (seq>=2221).

## Alcance (F1c)

- Endpoint read-only `/api/governance/artifacts`: indice de Area_comun/artifacts/ (id, tipo derivado del nombre,
  tarea asociada, fecha) con filtro por texto. Lee el CANONICO (git ls-tree / git show), no working tree.
- Vista Artifacts en /governance: lista + filtro (decisiones/specs/tasks/handoffs/reports/veredictos). PII redactada
  en previews de texto libre.
- NO portar Intake RF-14 ni Operate (son write-path -> F2, gateado; declararlo en SEAMS.md como diferido).

## DoD (= SPEC-0107 AC, vista F1c)

- AC1 endpoint artifacts read-only desde el CANONICO (git), sin ruta de escritura (denylist intacta).
- AC2 vista Artifacts renderiza con filtro; PII redactada.
- AC3 prueba negativa: sin nueva superficie de escritura.
- AC4 node --test verde; gate F0 (npm test) sigue exit 0.
- AC5 core protocolo intacto; handoff a Arquitecto (checker).

## Nota

- Tras checker verde, F1 queda COMPLETO -> GATE 1 incluira una review adversarial del Analista (3er firmante en la
  ventana de medicion) antes de cerrar F1.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
