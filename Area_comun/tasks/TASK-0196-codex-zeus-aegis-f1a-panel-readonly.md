---
task_id: TASK-0196
title: "Zeus-Aegis F1a - panel SOLO-LECTURA: contrato /api/governance/* (health/state/backlog/mailbox) + vistas Estado(salud)/Backlog/Mailbox (SPEC-0107, DECISION-0064)"
type: integration
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0050, DECISION-0022, DECISION-0040]
file: Area_comun/tasks/TASK-0196-codex-zeus-aegis-f1a-panel-readonly.md
---

# TASK-0196 - Zeus-Aegis F1a (panel read-only, primer increment)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Primer increment de la Fase 1 (DECISION-0064 /
> SPEC-0107). **SOLO LECTURA** -- la UI lee slim views, NO escribe estado (el writer-path F2 sigue gateado
> post-TFM). NO toca el core del protocolo, #4, ni el baseline congelado. Construir esto genera dataset elegible
> (gobernanza via submit_intent, seq >= 2221).

## Alcance (F1a)

- **Contrato read-only** `/api/governance/{health,state,backlog,mailbox}` como rutas que hacen shell/IPC a Python y
  leen el CANONICO (slim views / git show del HEAD canonico), NO el working tree crudo.
- **Vista Estado + header de salud:** PROJECT_STATE slim + indicador validador/drift **DERIVADO de la verificacion
  real** (tri-estado; fail-safe a no-verde; NUNCA verde hardcodeado).
- **Vista Backlog/Tareas:** TASK_INDEX slim con filtros (texto/estado/owner).
- **Vista Mailbox:** Area_comun/mailbox/open/.
- PII redactada (DECISION-0040). Pin Hermes v2.3.0.

## DoD (= SPEC-0107 AC1-AC6)

- AC1 endpoints health/state/backlog/mailbox sirven slim views read-only (sin ruta de escritura al ledger).
- AC2 salud DERIVADA de validate/drift reales (tri-estado, fail-safe no-verde, no hardcoded).
- AC3 Estado/Backlog(filtros)/Mailbox renderizan desde el canonico; PII redactada.
- AC4 prueba NEGATIVA: test que confirma que NO existe superficie de escritura directa al ledger desde la UI.
- AC5 node --test verde; el gate F0 (npm test) sigue exit 0; **waiver F0 revisado en docs/SEAMS.md** (los fallos
  upstream que F1a NO usa quedan waivados con justificacion; los que toque, verdes).
- AC6 core protocolo intacto; handoff autocontenido a Arquitecto (checker).

## Notas

- F1b (Decisiones/Ledger/Handoffs) y F1c (migrar componentes de zeus-protocol) son increments POSTERIORES.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- **POLITICA:** tras cerrar este caso (checker verde), el Arquitecto actualiza Zeus-Aegis/pipeline.html (control).
