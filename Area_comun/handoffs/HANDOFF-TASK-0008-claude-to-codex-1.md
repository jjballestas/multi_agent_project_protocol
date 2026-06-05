---
handoff_id: HANDOFF-TASK-0008-claude-to-codex-1
task_id: TASK-0008
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: yes
response_owner: Codex
requested_action: Confirmar el plan y la titularidad de TASK-0009..0013. NO iniciar TASK-0009/0010/0011/0012 hasta que TASK-0008 (Claude) entregue las specs (spec_id) - son implementation y DECISION-0004 prohibe ready/claimed/in_progress sin los 6 campos SDD.
---

# Handoff: SDD formalizado (DECISION-0004) → backlog TASK-0008..0013

## 1. Minimal Context
El operador humano pidió incorporar **SDD como gate previo a implementación + pipeline + criterios
de cierre**. Quedó formalizado en
[DECISION-0004](../decisions/DECISION-0004-sdd-pipeline-y-cierre.md) (aceptada). Esto crea la
subfase **P2.SDD**, que se publicará como **v0.4.0** (MINOR, aditivo, config-gated, sin migración
retroactiva).

## 2. La regla, en breve
- Ninguna tarea **implementable** (`implementation`/`refactor`/`integration`/`migration`/`security`/`release`)
  pasa a `ready`/`claimed`/`in_progress` sin: `spec_id`, `execution_pipeline`, `acceptance_criteria`,
  `linked_decisions`, `test_plan`, `closure_criteria`.
- Tareas `discovery`/`analysis`/`review`/`documentation`/`triage`: bastan `objective`,
  `expected_output`, `question_to_resolve`, `closure_criterion`.
- Ante requerimiento ambiguo o dudas: **preguntar antes de implementar**; si no hay claridad, crear
  tarea `discovery`/`analysis`, no `implementation`. No inventar pasos.
- Revisión cruzada valida contra `spec_id` + `closure_criteria`. El handoff declara criterios
  cumplidos + pruebas ejecutadas.

## 3. Backlog creado (en TASK_INDEX.json)
| Tarea | Owner | Tipo | Estado | Depende |
|-------|-------|------|--------|---------|
| TASK-0008 Diseñar SDD (produce las specs) | **Claude** | analysis | **ready** | — |
| TASK-0009 Templates (TASK_PROTOCOL/TASK_TEMPLATE/HANDOFF/HUMAN_REPORT) | Codex | implementation | proposed | 0008 |
| TASK-0010 `specs/` + 4 plantillas SDD | Codex | implementation | proposed | 0008 |
| TASK-0011 Validadores modo SDD (.py/.ps1) + bloque `sdd` en config | Codex | implementation | proposed | 0008,0010 |
| TASK-0012 `examples/minimal_sdd_instance` | Codex | implementation | proposed | 0010,0011 |
| TASK-0013 Doc onboarding SDD (README_INSTANCIACION) | Codex | documentation | proposed | 0009,0010 |

## 4. Por qué 0009..0012 están `proposed` (no `ready`)
Son `implementation` y aún **no tienen `spec_id`** (sus 6 campos SDD están "pendiente" en el cuerpo
de cada tarea). Es la propia regla de DECISION-0004 en acción: **TASK-0008 (Claude) las desbloquea**
entregando las specs. No las reclames antes.

## 5. Requested Action (Codex)
1. **Confirma** el plan y que asumes TASK-0009..0013 (ajustamos titularidad si prefieres otra).
2. **Espera** a TASK-0008: te entregaré el diseño (`Area_comun/artifacts/DISENO-SDD.md`) y los
   `spec_id` por tarea. Entonces podrás completar los 6 campos y pasar cada una a `ready`.
3. Al implementar TASK-0011: **aditivo y con paridad `.py`↔`.ps1`** (como TASK-0007); sin
   `sdd.enabled` el validador se comporta igual que hoy; exime tareas históricas/pre-SDD.
4. Mantén el **core neutral** (TASK-0009/0010 tocan masters del core): sin trading/.NET/SQL/Azure.

## 6. Risks and Assumptions
- Riesgo: romper compatibilidad si el validador exige SDD a todo → sería MAJOR (prohibido aquí).
  Solo `enforcement: "new_implementable_tasks"`.
- Asumo Python+PowerShell con golden cases para TASK-0011 (positivos y negativos).
- No migración retroactiva: TASK-0001..0007 son pre-SDD.

## 7. Open Questions / BLOCKED
- ¿Aceptas la titularidad propuesta (0009..0013 a Codex, 0013 documentation)? Si no, propónlo aquí.
- Pregunta abierta no bloqueante (a resolver en TASK-0008): ¿una spec global del rollout o una por
  tarea? Recomendación: una por tarea, enlazadas a una matriz de trazabilidad.

## 8. Pointers
- `Area_comun/decisions/DECISION-0004-sdd-pipeline-y-cierre.md`
- `Area_comun/tasks/TASK-0008-*..TASK-0013-*`
- `Area_comun/state/TASK_INDEX.json` (leyenda `type` + `sdd_note`), `PROJECT_STATE.json` (subfase P2.SDD)
- DECISION-0001 (versionado MINOR/MAJOR), DECISION-0002 (core neutral)
