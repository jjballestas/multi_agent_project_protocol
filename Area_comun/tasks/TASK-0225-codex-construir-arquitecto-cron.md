---
task_id: TASK-0225
title: "Construir Arquitecto-cron headless (orquestador del GOAL-REQ-ZEUS-001); lanzamiento real lo hace el operador"
type: build
status: in_progress
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0057, DECISION-0038, DECISION-0020]
linked_goals: [GOAL-REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0225-codex-construir-arquitecto-cron.md
---

# TASK-0225 — Arquitecto-cron headless (orquestador del goal)

- **Owner build:** Codex · **Review:** Analista · **Checker:** Arquitecto
- **Habilitador del modo 24/7 headless del GOAL-REQ-ZEUS-001.**

## Contexto
Existen `personal/Codex/codex_mailbox_cron.ps1` y `personal/Analista/analista_mailbox_cron.ps1` (procesan mailbox->peer
via `codex exec`/runtime). FALTA el cron del Arquitecto, que NO solo procesa mailbox sino que **orquesta el goal**.

## Alcance
1. **Harness** `personal/Arquitecto/arquitecto_cron.ps1`, espejo estructural de los existentes: pid/log/seen/stop/lock,
   intervalo configurable, exec del runtime del Arquitecto (claude/equivalente) con un prompt por STDIN, y la
   **regla de auto-stop por orden del operador** (mismo patron de stop-order de los otros crons).
2. **Prompt de orquestacion** `personal/Arquitecto/arquitecto_cron.prompt.txt` (lo provee el Arquitecto; Codex lo cablea):
   cada ciclo -> leer mailbox/state; si una tarea WS esta in_review -> rutear review al Analista / ratificar al cerrar;
   si una WS esta done y la siguiente tiene deps despejadas -> promover UNA (GO gateado); **PAUSAR+avisar al operador
   al alcanzar N=500**; respetar rieles (push si verde; NO activar #4/F2/Engram/re-genesis sin GO; NO tocar pineados);
   narracion minima (DECISION-0038).
3. **Runbook** de arranque/stop. **El lanzamiento real del .ps1 lo ejecuta el OPERADOR** (deny-rule PowerShell del harness).

## DoD
- Harness presente y consistente con los otros crons; prompt cableado por STDIN; runbook incluido.
- Dry-run documentado (un ciclo en seco que muestre: lee estado, detecta WS, decide promover/revisar) sin escribir ledger en el dry-run.
- Gate Analista: GO. maker!=checker.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta. Producto/orquestacion en el hub; el .ps1 vive en personal/Arquitecto/.
