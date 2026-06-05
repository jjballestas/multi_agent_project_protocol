---
handoff_id: HANDOFF-TASK-0008-claude-to-codex-2
task_id: TASK-0008
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: no
response_owner: Codex
requested_action: Reclamar e implementar TASK-0009 y TASK-0010 (paralelizables) contra sus SPEC; luego TASK-0011, TASK-0012 y TASK-0013. Implementar exactamente contra cada spec_id; no inventar pasos.
---

# Handoff: TASK-0008 DONE → specs entregadas, TASK-0009..0013 desbloqueadas

## 1. Minimal Context
TASK-0008 está **done**. Entregué el diseño y las specs que pediste; TASK-0009..0013 ya tienen
`spec_id` resoluble y son **SDD-elegibles**. Puedes reclamarlas y pasarlas a `ready`/`claimed`.

## 2. Entregables
- **Diseño:** [Area_comun/artifacts/DISENO-SDD.md](../artifacts/DISENO-SDD.md) — contrato de los 6
  campos SDD / 4 mínimos, cambios a plantillas, comportamiento del validador (config-gated +
  exención pre-SDD + ERROR/WARNING), esquema `sdd` y orden de implementación.
- **Specs (una por tarea):**
  - `Area_comun/specs/SPEC-0009-sdd-templates.md` → TASK-0009
  - `Area_comun/specs/SPEC-0010-specs-folder.md` → TASK-0010
  - `Area_comun/specs/SPEC-0011-validator-sdd.md` → TASK-0011
  - `Area_comun/specs/SPEC-0012-example-minimal-sdd.md` → TASK-0012
  - `Area_comun/specs/SPEC-0013-doc-sdd-onboarding.md` → TASK-0013

## 3. Decisiones de diseño que debes respetar
- **Una spec por tarea** + matriz de trazabilidad (la plantilla la creas en TASK-0010).
- `Area_comun/specs/` **ya existe** (la creé con las specs concretas). TASK-0010 añade las
  **plantillas reutilizables** (`SPEC_TEMPLATE`, `PROJECT_BRIEF_TEMPLATE`, `TEST_PLAN_TEMPLATE`,
  `TRACEABILITY_MATRIX_TEMPLATE`), **sin** tocar SPEC-0009..0013.
- **Frontmatter de la tarea = fuente canónica** de los campos SDD (DISENO §1.3).
- Validador (TASK-0011): **aditivo, config-gated, paridad `.py`↔`.ps1`**, exime tareas pre-SDD;
  los ejemplos actuales deben seguir verdes. Golden cases en `examples/sdd_validation_cases/`.
- **Core neutral**: TASK-0009/0010 tocan masters del core → sin trading/.NET/SQL/Azure.

## 4. Orden recomendado
1. TASK-0009 + TASK-0010 (paralelo) → 2. TASK-0011 → 3. TASK-0012 → 4. TASK-0013.
Cada handoff de cierre debe declarar **criterios cumplidos + pruebas ejecutadas** (nuevo formato).

## 5. Cierre de v0.4.0
Cuando TASK-0009..0013 estén `done` y verdes, yo (arquitecto) reviso contra specs y publico
**v0.4.0** (MINOR): mover Unreleased en CHANGELOG, `protocol_version`→`0.4.0`, AGENTS/PROJECT_STATE,
tag, commit + push.

## 6. Pointers
- DISENO-SDD.md, specs/SPEC-0009..0013, DECISION-0004, DECISION-0001 (versionado), DECISION-0002 (neutralidad).
- TASK_INDEX.json (cada tarea con su `spec_id`), PROJECT_STATE.json (subfase P2.SDD).
