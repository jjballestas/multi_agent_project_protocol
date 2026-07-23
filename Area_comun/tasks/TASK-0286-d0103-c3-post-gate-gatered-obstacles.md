---
task_id: TASK-0286
title: "[DECISION-0103][C3/E7] Enforcement post-gate de gate-red -> obstacles no vacio, sobre el run-log (capa apply), donde gate_green existe"
type: feature
status: in_progress
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-22
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0259]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0286-d0103-c3-post-gate-gatered-obstacles.md
intake:
  type: feature
  goal: Implementar la mitad OBJETIVA del sensor de friccion de DECISION-0103 C3 (carril runtime) que TASK-0259 NO puede hostear. Probado en el re-juicio de 0259 iter1 (artifact Analista-TASK-0259-remediation-iter1-verdict) y sellado en la enmienda E7, gate_green (el resultado objetivo del gate) se produce POST-gate (validate_turn corre pre-gate en orchestrator.py:947; apply_gate_and_commit en :1018; gate_green se escribe al run-log en :1026), por lo que es INOBSERVABLE a turn-validate-time. Esta unidad enforcea "gate rojo (gate_green:false) + obstacles vacio = FAIL" en la capa CORRECTA, la entrada del run-log despues de que el gate corre, cerrando el vector que 0259 declara honestamente fuera de su alcance (un agente que reporta outcome=ok con gate objetivamente rojo y obstacles vacio).
  acceptance:
    - El check post-gate lee gate_green (o equivalente objetivo del run-log/resultado de apply) y, si el gate fue rojo Y el bloque obstacles del turno esta vacio/ausente, FALLA con mensaje accionable (que sensor disparo y que falta).
    - Gate verde -> no exige obstacles (no fuerza prosa). Anti-teatro preservado, espejo de 0259.
    - El check se ejerce por el entrypoint REAL que recibe el gate_green (la ruta de apply / lectura del run-log), NUNCA alimentando un campo fuera-de-schema a una funcion unit (la trampa unit-vs-behavior que hundio 0259 iter1).
    - El limite se documenta donde declara C4/E7, gate-red objetivo vive aqui (post-gate); las senales auto-declarables (transiciones autoritativas, revert) viven en 0259 (turn_validate).
    - Suite cubre, por el entrypoint real, gate-rojo x (con/sin obstacles) + gate-verde, todos con el resultado esperado.
    - Negativos permanentes (0283) con mutacion, gate-rojo + obstacles vacio enrojece; revertir el arreglo enrojece el contrato.
    - Suites del runtime verdes; validate + scan_encoding en verde; probado en scratch/examples, NUNCA se ejecuta el orchestrator en el hub.
  verification_cmd:
    - python examples/runtime_turn_cases/run_runtime_turn_cases.py
    - Suite nueva o extendida del check post-gate (examples/, patron run_*.py) en verde
    - python scripts/check_falsification_contracts.py --inventory
    - python scripts/test_falsification_contracts.py
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - runtime/apply.py
    - runtime/runlog.py
    - runtime/
    - examples/runtime_turn_cases/
  out_of_scope:
    - turn_validate.py y las senales auto-declarables (transiciones, revert) - ESO es TASK-0259.
    - Cambiar el turn_schema (TASK-0258).
    - Ejecutar el orchestrator en el hub - FUERA (validacion solo en scratch/examples).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: medium
  estimate: M
---

# TASK-0286 - [DECISION-0103][C3/E7] gate-red objetivo post-gate -> obstacles

Origen: enmienda E7 a DECISION-0103 (split de capa del sensor de friccion C3 runtime, firma del
Operador 2026-07-22). Unidad hermana de TASK-0259: 0259 enforcea la friccion AUTO-DECLARABLE
(transiciones autoritativas + revert) en `turn_validate` (pre-gate); esta unidad enforcea la
friccion OBJETIVA (gate_green:false) en la capa apply/run-log (post-gate), la unica donde
gate_green existe. Juntas cubren C3 runtime entero, cada mitad en su capa correcta. Depende del
cierre de 0259 (para no solapar el mismo suite) y del OK del plan.
