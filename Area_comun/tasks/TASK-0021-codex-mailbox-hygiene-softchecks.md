---
id: TASK-0021
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0014, TASK-0020]
phase: P2
spec_id: Area_comun/specs/SPEC-0021-mailbox-hygiene-softchecks.md
linked_decisions: [DECISION-0005, DECISION-0006, DECISION-0001]
execution_pipeline: [Soft-check open/ con status answered|archived => WARNING en .py, Soft-check type ACK|FYI + requires_response:false => WARNING, Mirror en .ps1, Golden cases mailbox, Verificar paridad y ejemplos existentes verdes]
acceptance_criteria: [status answered|archived en open/ => WARNING (.py y .ps1, exit 0), ACK|FYI + requires_response:false en open/ => WARNING, open+requires_response:true sin warning, legacy sin ruido, paridad .py/.ps1, root/ejemplos verdes]
test_plan: [Golden harness de mailbox (warning por caso), .py y .ps1 sobre root + ejemplos existentes]
closure_criteria: [Golden cases pasan en ambos validadores, paridad, root/ejemplos verdes, handoff documenta criterios y pruebas, claim liberado]
---

# TASK-0021 — Soft-checks de higiene de mailbox

> `implementation` → SDD obligatorio; implementar contra
> [SPEC-0021](../specs/SPEC-0021-mailbox-hygiene-softchecks.md) y DECISION-0005/0006. `ready` (spec
> emitida por Claude). Aditivo: solo **WARNING**, no rompe estado ni históricos.

## Resumen
Hace verificable la disciplina de archivado del mailbox (DECISION-0005): avisa cuando un mensaje
resuelto queda en `open/`. Surge del gap detectado en sesión (mensajes cerrados sin archivar) y
complementa TASK-0020 (`claim-before-shared-draft`). No bloquea v0.6.0; backlog inmediato.

## archivos objetivo
- `scripts/validate_collaboration_state.py`, `scripts/validate_collaboration_state.ps1`
- `examples/mailbox_hygiene_cases/`

## notas_de_ejecucion
- Implementados warnings suaves para mensajes resueltos en `open/` y `ACK|FYI` sin respuesta.
- Golden cases en `examples/mailbox_hygiene_cases/`.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0021-codex-to-claude-1.md`.

