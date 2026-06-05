---
id: TASK-0024
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0023]
relates_to: [TASK-0025]
phase: P2
spec_id: Area_comun/specs/SPEC-0024-poda-estado-historico.md
linked_decisions: [DECISION-0008, DECISION-0001, DECISION-0007]
execution_pipeline: [Crear CLAIMS_ARCHIVE/TASK_INDEX_ARCHIVE (+template), Migrar released/done a archivo (ventana conservadora), Validador lee caliente union archivo, AGENTS §0 cold-start a calientes + historico bajo demanda, Medir before/after con measure_context_cost]
acceptance_criteria: [Cold-start medido baja ~70% con before/after real, Trazabilidad intacta (nada borrado y consultable), Validador verde con cobertura equivalente (lee caliente union archivo), Caliente solo active/no-done + ventana, paridad .py/.ps1]
test_plan: [measure_context_cost antes/despues, validador en root + ejemplos, inconsistencia indice-archivo detectada]
closure_criteria: [Poda sin perdida, validador verde con cobertura equivalente, delta medido en handoff, AGENTS §0 actualizado, claim liberado]
---

# TASK-0024 — Poda de estado a histórico (mayor impacto)

> `implementation` → SDD; implementar contra [SPEC-0024](../specs/SPEC-0024-poda-estado-historico.md)
> y DECISION-0008 §2. **Mayor ahorro del lote** (~−74% cold-start). Sin pérdida: archivar ≠ borrar.
> Depende de TASK-0023 (medir el delta). Reclamar antes de mover estado (DECISION-0007).
