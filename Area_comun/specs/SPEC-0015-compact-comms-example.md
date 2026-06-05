---
spec_id: SPEC-0015-compact-comms-example
task_id: TASK-0015
type: implementation
status: ready
linked_decisions: [DECISION-0005, DECISION-0002]
created_at: 2026-06-05
author: Claude
---

# SPEC-0015 — Ejemplo compact_communication_case

## Contexto
Falta un ejemplo de referencia que muestre comunicación compacta conforme a DECISION-0005.

## Alcance
`examples/compact_communication_case/`: un par de mensajes de mailbox compactos (p.ej. REVIEW→OK,
o BLOCKED con una sola `question`) usando `MAILBOX_MESSAGE_TEMPLATE.md`, más un handoff compacto.

## No-alcance
Sin dominio (neutral). No modificar instancias existentes.

## execution_pipeline
1. Crear instancia mínima (o subset) con mailbox que contenga 1-2 mensajes compactos válidos
   (códigos estándar, `context_refs`, una `question`).
2. Incluir un handoff compacto de ejemplo.
3. Validar con `.py` y `.ps1`; barrido de neutralidad. Handoff.

## acceptance_criteria
- El ejemplo valida verde en ambos validadores (incl. chequeos suaves de TASK-0014 si ya están).
- Los mensajes usan el formato compacto y códigos estándar; neutral de dominio.
- No rompe ejemplos existentes.

## test_plan
- `.py` y `.ps1` sobre `examples/compact_communication_case`.
- Barrido de neutralidad sobre el ejemplo.

## closure_criteria
- Ejemplo verde en ambos validadores; neutral; handoff con criterios+pruebas; revisión cruzada OK.
