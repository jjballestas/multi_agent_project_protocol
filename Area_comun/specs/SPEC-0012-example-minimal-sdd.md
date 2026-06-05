---
spec_id: SPEC-0012-example-minimal-sdd
task_id: TASK-0012
type: implementation
status: ready
linked_decisions: [DECISION-0004, DECISION-0002]
created_at: 2026-06-05
author: Claude
---

# SPEC-0012 — Ejemplo minimal_sdd_instance

## Contexto
Falta un ejemplo de referencia que demuestre una instancia con SDD activado. Ver
[DISENO-SDD.md](../artifacts/DISENO-SDD.md) §4, §6.

## Alcance
Crear `examples/minimal_sdd_instance/`: instancia core con `sdd.enabled:true`, una spec en `specs/`
y al menos una tarea implementable con los 6 campos SDD que valida en verde.

## No-alcance
Sin perfiles ni dominio; debe ser **neutral**. No duplicar el dogfooding del repo.

## execution_pipeline
1. Generar instancia base (scaffolding) y activar `sdd` en su `protocol.config.json`.
2. Añadir `Area_comun/specs/SPEC-0001-*.md` de ejemplo (neutral).
3. Añadir 1 tarea `implementation` con los 6 campos SDD apuntando a esa spec, en `ready`/`in_review`.
4. (Opcional) 1 tarea `discovery` con los 4 mínimos.
5. Validar con `.py` y `.ps1`; handoff.

## acceptance_criteria
- `examples/minimal_sdd_instance/` valida verde con `sdd.enabled:true` en ambos validadores.
- Contiene ≥1 spec y ≥1 tarea implementable conforme a SDD.
- Neutral de dominio; no rompe los ejemplos existentes.

## test_plan
- `python scripts/validate_collaboration_state.py --root examples/minimal_sdd_instance` → OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root examples/minimal_sdd_instance` → OK.
- Barrido de neutralidad sobre la instancia.

## closure_criteria
- Validadores verdes sobre la nueva instancia y las existentes; handoff con criterios + pruebas;
  revisión cruzada OK.
