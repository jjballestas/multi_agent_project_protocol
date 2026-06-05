---
id: TASK-0014
owner: Codex
status: proposed
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0015]
phase: P2
spec_id: Area_comun/specs/SPEC-0014-compact-comms-validator.md
execution_pipeline: [Add open+requires_response check (requested_action y question) en .py, Mirror en .ps1, WARNING conservador por context_refs, Golden cases compactos, Verificar paridad y ejemplos existentes, Handoff y liberar claim]
acceptance_criteria: [open+requires_response:true sin requested_action o question => ERROR en .py y .ps1, Mensajes legacy y requires_response:false no afectados, Golden cases con exits esperados, Paridad .py/.ps1, root y ejemplos existentes verdes]
linked_decisions: [DECISION-0005, DECISION-0001, DECISION-0004]
test_plan: [Golden harness compacto, .py y .ps1 en root + minimal_instance + dotnet_enterprise_instance + minimal_sdd_instance]
closure_criteria: [Golden cases pasan en ambos validadores, Ejemplos existentes verdes, Handoff documenta criterios y pruebas, Claim liberado]
---

# TASK-0014 — Validaciones suaves de comunicación compacta

> `implementation` → SDD obligatorio. SDD-elegible (ver `spec_id`). Implementar contra
> [SPEC-0014](../specs/SPEC-0014-compact-comms-validator.md) y DECISION-0005 §8 (aditivo, sin
> romper históricos; sin validar longitud; paridad `.py`/`.ps1`).

## SDD
Los 6 campos están en el frontmatter (canónico) y detallados en la spec.

## riesgos
- Falsos positivos en `context_refs`: heurística conservadora; ante duda, no avisar.
