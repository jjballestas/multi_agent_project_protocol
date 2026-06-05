---
id: TASK-0012
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0010, TASK-0011]
relates_to: [TASK-0009]
phase: P2
spec_id: Area_comun/specs/SPEC-0012-example-minimal-sdd.md
execution_pipeline: [Generate base example instance, Enable sdd in protocol config, Add neutral example spec, Add conforming implementable task, Validate Python and PowerShell, Create handoff and release claim]
acceptance_criteria: [minimal_sdd_instance validates green with SDD enabled, Instance contains at least one spec, Instance contains at least one implementable task with six SDD fields, Example remains domain-neutral, Existing examples remain green]
linked_decisions: [DECISION-0004, DECISION-0002]
test_plan: [Run Python validator on minimal_sdd_instance, Run PowerShell validator on minimal_sdd_instance, Run validators on existing examples, Run neutrality scan on minimal_sdd_instance]
closure_criteria: [New example validates green, Existing examples remain valid, Handoff documents evidence, Claim released]
review: Aceptada por Claude contra SPEC-0012. Verificacion independiente - examples/minimal_sdd_instance con sdd.enabled:true valida verde en .py y .ps1 (tarea TASK-0002 conforme + SPEC-0002); neutral; ejemplos previos siguen verdes.
---

# TASK-0012 — Crear example minimal_sdd_instance

> Tipo `implementation` → **SDD obligatorio**. TASK-0008 ya entregó la spec: **SDD-elegible**
> (su ejecución depende además de TASK-0010/0011).

## objetivo
Crear `examples/minimal_sdd_instance/` que demuestre una instancia con `sdd.enabled: true`, una
spec en `specs/`, y una tarea implementable con los 6 campos SDD que valida en verde.

## SDD (resuelto — ver spec_id)
Los 6 campos están definidos en [SPEC-0012-example-minimal-sdd.md](../specs/SPEC-0012-example-minimal-sdd.md).
Implementar contra esa spec (instancia neutral con `sdd.enabled`, ≥1 spec y ≥1 tarea implementable conforme).

## riesgos
- No romper los ejemplos existentes; no introducir dominio en el ejemplo SDD (debe ser neutral).

## notas_de_ejecucion
- Creado `examples/minimal_sdd_instance/` con `sdd.enabled:true`.
- Anexada spec neutral `Area_comun/specs/SPEC-0002-sdd-example.md` dentro del ejemplo.
- Anexada tarea `TASK-0002` con los seis campos SDD.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0012-codex-to-claude-1.md`.
