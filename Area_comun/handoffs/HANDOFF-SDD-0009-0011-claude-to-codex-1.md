---
handoff_id: HANDOFF-SDD-0009-0011-claude-to-codex-1
task_id: TASK-0011
spec_id: none
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: no
response_owner: Codex
acceptance_criteria_verified: yes
tests_run:
  - examples/sdd_validation_cases/run_sdd_cases.ps1 (OK)
  - python validator per SDD case (exits 0/1/0/0 esperados)
  - .py y .ps1 validators en root + 3 ejemplos (OK)
  - neutrality scan core/templates (limpio)
spec_deviations:
  - TASK-0010 anadio REQUIREMENTS/ACCEPTANCE_CRITERIA templates (aditivo, neutral) - aceptado
decisions_referenced:
  - DECISION-0004
---

# Handoff: TASK-0009/0010/0011 aceptadas (DONE)

## 1. Resultado
**OK / DONE** las tres, revisadas contra SPEC-0009/0010/0011. Verificación independiente: golden
cases SDD con paridad `.py`↔`.ps1`; SDD off ⇒ validadores verdes en root + 3 ejemplos; core/templates
neutral. Detalle en el `review` de cada tarea (TASK_INDEX + task files).

## 2. Pendiente para cerrar SDD (tú)
- **TASK-0012** (`examples/minimal_sdd_instance`) — SPEC-0012. SDD-elegible.
- **TASK-0013** (doc onboarding SDD en README_INSTANCIACION) — SPEC-0013.

## 3. Requested Action
Reclama e implementa **TASK-0012** y **TASK-0013** contra sus specs. Al dejarlas `in_review` + handoff,
yo reviso y **publico v0.4.0** (agrupando el commit de TASK-0008). No hagas commit/push del release.

## 4. Pointers
- specs/SPEC-0012, specs/SPEC-0013; DISENO-SDD §6 (orden); DECISION-0004.
