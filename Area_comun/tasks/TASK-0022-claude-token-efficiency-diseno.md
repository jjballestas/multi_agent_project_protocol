---
id: TASK-0022
owner: Claude
status: done
type: analysis
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: []
relates_to: [TASK-0021]
phase: P2
linked_decisions: [DECISION-0008, DECISION-0005, DECISION-0001]
objective: Diseñar el medidor de costo de contexto, el esquema de archivado de estado y el frontmatter mínimo de mailbox, con baseline medido.
expected_output: DISENO-eficiencia-de-tokens.md + specs (medidor, poda-a-historico, frontmatter mínimo) + tabla baseline; backlog de implementación para Codex.
question_to_resolve: ¿Cuál es el contrato exacto del medidor (escenarios + divisor), el formato de archivo histórico (CLAIMS_ARCHIVE/TASK_INDEX_ARCHIVE) que preserva trazabilidad sin romper el validador, y el set mínimo de frontmatter compatible hacia atrás?
closure_criterion: Specs publicadas y baseline capturado; tareas de implementación SDD-elegibles (spec_id fijado); validadores verdes.
---

# TASK-0022 — Diseño de eficiencia de tokens + baseline

> `analysis` (4 campos mínimos en frontmatter). Ejecuta DECISION-0008: produce el diseño, las specs
> y el baseline reproducible que desbloquean la implementación de Codex.

## Alcance
- **SPEC del medidor** `measure_context_cost.py`/`.ps1`: escenarios (cold-start segun AGENTS §0,
  peso muerto de estado, overhead frontmatter), divisor configurable, salida determinista, paridad.
- **SPEC de poda-a-histórico**: a dónde van `released`/`done` (`*_ARCHIVE.json`), cómo el validador
  mantiene trazabilidad, garantía de no-pérdida, migración inicial.
- **SPEC de frontmatter mínimo**: set obligatorio vs opcional-omitible, compatibilidad hacia atrás,
  ajuste de `MAILBOX_MESSAGE_TEMPLATE` y validador.
- **Baseline** capturado con la metodología (tabla antes/después vacía para llenar tras implementar).

## riesgos
- Archivar estado puede romper supuestos del validador (lee solo los archivos calientes). Mitigar:
  el validador conoce el histórico; specs lo fijan.
- Adelgazar frontmatter puede invalidar checks existentes. Mitigar: compatibilidad hacia atrás
  obligatoria; solo se omiten opcionales vacíos.

## notas_de_ejecucion
- Diseño: `Area_comun/artifacts/DISENO-eficiencia-de-tokens.md` (metodología + baseline + 3 contratos).
- **Baseline medido (2026-06-05, div 4):** cold-start 29.169 tok (CLAIMS 11.233 + TASK_INDEX 10.842 =
  75%); CLAIMS 100% `released`; TASK_INDEX 95% `done`; frontmatter mailbox 65% relleno (ratio 1,9).
- Specs: `SPEC-0023` (medidor), `SPEC-0024` (poda, mayor impacto), `SPEC-0025` (frontmatter mínimo).
- TASK-0023/0024/0025 (Codex) creadas `ready`. Orden: 0023 → 0024 → 0025. Cada una reporta delta medido.
- Validador verde tras los cambios.
