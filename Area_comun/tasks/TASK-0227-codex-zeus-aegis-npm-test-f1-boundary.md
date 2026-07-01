---
task_id: TASK-0227
title: "Zeus-Aegis: diagnosticar y arreglar fallos pre-existentes de npm test (timeout governance-readonly + boundary F1/submit_intent)"
type: build
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0064]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
---

# TASK-0227 — Zeus-Aegis: npm test verde (boundary F1 + timeout)

- **Owner build:** Codex · **Review:** Analista · **Checker:** Arquitecto
- **Repo de producto:** `D:\Agentes\Zeus\Zeus-Aegis`. Gobernanza: hub.

## Contexto
Surge del review de WS1 (TASK-0226): `npm test` en clon limpio del producto sale 1 por dos fallos
PRE-EXISTENTES (no causados por WS1):
1. `src/server/governance-readonly.test.ts`: timeout en "lists artifacts, decisions, handoffs, and ledger events".
2. "does not expose direct ledger write surfaces in F1 routes": falla porque la UI contiene `submit_intent`.

Nota oportuna: **N=500 ya esta sellado → F2 (write-through) queda desbloqueado.** Por eso el #2 puede ser
(a) una fuga real de F2 dentro de F1 (bug de boundary), o (b) un test que quedo obsoleto al volverse licito F2.

## Alcance
1. **Diagnosticar el #2:** determinar si `submit_intent` en la UI es una superficie de escritura real en rutas
   F1 (fuga de boundary) o una referencia inerte / test obsoleto post-sello. **Reportar el hallazgo con evidencia**
   ANTES de cambiar nada estructural; si toca el boundary F1/F2, escalar a DECISION (no decidir el boundary solo).
2. **Arreglar el #1** (timeout governance-readonly): estabilizar el test (pre-warm/poll/timeout adecuado) sin enmascarar un fallo real.
3. Dejar `npm test` verde en **clon limpio** del producto (gate-by-exit-code), sin enmascarar fallos legitimos.

## DoD
- `npm test` exit 0 en clon limpio del producto.
- Reporte del diagnostico del #2 (fuga real vs obsoleto) con evidencia falsable; si requiere decision de boundary, queda planteada.
- Sin tocar el core del protocolo ni los pineados. Gate Analista: GO.

## Handoff
Autocontenida. maker!=checker. Ambiguedad -> blocked + 1 pregunta concreta.
