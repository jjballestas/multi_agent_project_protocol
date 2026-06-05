---
spec_id: SPEC-0011-validator-sdd
task_id: TASK-0011
type: implementation
status: ready
linked_decisions: [DECISION-0004, DECISION-0001, DECISION-0003]
created_at: 2026-06-05
author: Claude
---

# SPEC-0011 — Modo SDD en los validadores (config-gated, aditivo)

## Contexto
El validador debe verificar SDD sin romper compatibilidad. Ver
[DISENO-SDD.md](../artifacts/DISENO-SDD.md) §4. Patrón aditivo + paridad igual que TASK-0007.

## Alcance
`scripts/validate_collaboration_state.py`, `scripts/validate_collaboration_state.ps1`,
`protocol.config.template.json` (bloque `sdd`), golden cases.

## No-alcance
No exigir SDD retroactivo (sería MAJOR). No tocar la lógica de claims/mailbox/profiles existente.

## execution_pipeline
1. Añadir bloque `sdd` (default `enabled:false`) a `protocol.config.template.json`.
2. Implementar `validate_sdd` en `.py` siguiendo DISENO §4.2–§4.3 (exención pre-SDD; ERROR/WARNING).
3. Replicar idéntico en `.ps1` (mismos mensajes, misma política).
4. Crear golden cases en `examples/sdd_validation_cases/` (positivos y negativos: falta cada campo, spec_id inexistente, tarea exenta, discovery sin mínimos).
5. Verificar paridad y que los ejemplos actuales siguen verdes. Handoff.

## acceptance_criteria
- Sin `sdd.enabled`: salida idéntica a la actual en root + 3 ejemplos existentes.
- Con `sdd.enabled:true` + `enforcement:new_implementable_tasks`: ERROR por campo SDD faltante o `spec_id` inexistente en tarea implementable no exenta; WARNING por mínimo faltante en discovery/etc.
- Tareas pre-SDD (sin `type`/`sdd_exempt`/anteriores a adopción) **exentas**.
- Paridad `.py`↔`.ps1` (exit codes y mensajes idénticos) en todos los golden cases.

## test_plan
- `examples/sdd_validation_cases/` con casos esperando exit 0/1; harness que compara `.py` y `.ps1`.
- `python scripts/validate_collaboration_state.py --root .` y los 3 ejemplos → OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` y ejemplos → OK.

## closure_criteria
- Todos los golden cases con exit esperado en ambos validadores; ejemplos existentes verdes;
  handoff con criterios + pruebas; revisión cruzada del arquitecto OK.
