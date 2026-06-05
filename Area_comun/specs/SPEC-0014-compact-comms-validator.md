---
spec_id: SPEC-0014-compact-comms-validator
task_id: TASK-0014
type: implementation
status: ready
linked_decisions: [DECISION-0005, DECISION-0001, DECISION-0004]
created_at: 2026-06-05
author: Claude
---

# SPEC-0014 — Validaciones suaves de comunicación compacta

## Contexto
DECISION-0005 §8 define chequeos suaves para el mailbox compacto, compatibles con históricos.

## Alcance
`scripts/validate_collaboration_state.py` y `.ps1` (paridad). Golden cases nuevos.

## No-alcance
No validar longitud. No invalidar mensajes históricos. No tocar la lógica SDD/perfiles existente.

## execution_pipeline
1. En ambos validadores, para mensajes en `mailbox/open/` con `requires_response: true`:
   ERROR si falta `requested_action` o `question`.
2. WARNING si el mensaje referencia trabajo existente y no declara `context_refs`
   (heurística conservadora: solo cuando hay marcadores claros; ante duda, no avisar).
3. Mensajes sin los campos nuevos (formato legacy) NO se invalidan.
4. Golden cases en `examples/compact_comms_validation_cases/` (o reutilizar patrón existente):
   compacto válido; falta `question`; legacy exento.
5. Paridad `.py`↔`.ps1`; ejemplos e instancias actuales siguen verdes. Handoff.

## acceptance_criteria
- open + requires_response:true sin `requested_action` o `question` ⇒ ERROR (ambos validadores).
- Mensajes legacy y `requires_response:false` no se ven afectados.
- Golden cases con exits esperados; paridad `.py`↔`.ps1`.
- root + ejemplos existentes siguen verdes.

## test_plan
- Golden harness compacto (exit codes + salida normalizada .py vs .ps1).
- `.py` y `.ps1` sobre root + minimal_instance + dotnet_enterprise_instance + minimal_sdd_instance.

## closure_criteria
- Golden cases pasan en ambos validadores; ejemplos verdes; handoff con criterios+pruebas;
  revisión cruzada del arquitecto OK.
