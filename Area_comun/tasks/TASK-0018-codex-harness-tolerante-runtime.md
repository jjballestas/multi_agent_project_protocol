---
id: TASK-0018
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0016]
relates_to: [TASK-0017]
phase: P2
spec_id: Area_comun/specs/SPEC-0018-harness-tolerante-runtime.md
linked_decisions: [DECISION-0006, DECISION-0001]
execution_pipeline: [Detección con fallback python (python/py -3/python3) y powershell (pwsh/powershell), Marcar SKIPPED(WARNING) la mitad sin runtime, Verificar paridad solo si ambos presentes, Resumen final de ejecutado/saltado, Aplicar a run_sdd_cases.ps1 y run_compact_comms_cases.ps1]
acceptance_criteria: [Falta un runtime => su mitad SKIPPED(WARNING) y el harness no falla, Falta logica (exit inesperado del runtime presente) => falla, Ningún runtime => falla con mensaje claro, Con ambos runtimes los exits esperados actuales no cambian, Resumen final sin truncado silencioso]
test_plan: [Simular ausencia de python y de powershell, ejecutar ambos harness con ambos runtimes (paridad intacta), casos golden existentes verdes]
closure_criteria: [Harness no fallan por entorno, comportamiento de paridad intacto con ambos runtimes, handoff documenta la política de skip, claim liberado]
---

# TASK-0018 — Harness tolerantes a runtime (skip con aviso)

> `implementation` → SDD obligatorio; implementar contra
> [SPEC-0018](../specs/SPEC-0018-harness-tolerante-runtime.md) y DECISION-0006 §1. `ready` (spec
> emitida por TASK-0016). Aditivo: los harness se vuelven *más* tolerantes, no cambian exits
> esperados cuando ambos runtimes están.

## Resumen
Elimina la fragilidad de "exige ambos runtimes": detección con fallback y `SKIPPED (WARNING)` para
el runtime ausente; falla solo por lógica o por falta total de runtime. Ver DECISION-0006 §1.

## archivos objetivo
- `examples/sdd_validation_cases/run_sdd_cases.ps1`
- `examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`


