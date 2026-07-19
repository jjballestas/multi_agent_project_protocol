---
task_id: TASK-0260
title: "[DECISION-0103][C1] Vista de plan del conjunto (--plan-all / render de TASK_INDEX) + gate de aprobacion de turno 0 en el orchestrator"
type: feature
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0009]
linked_decisions: [DECISION-0103, DECISION-0009]
file: Area_comun/tasks/TASK-0260-d0103-c1-vista-plan-gate-aprobacion-turno0.md
intake:
  type: feature
  goal: Implementar la clausula 1 de DECISION-0103 en el runtime, (a) vista de plan del CONJUNTO (orchestrator --plan-all o render equivalente de TASK_INDEX + intake de los .md) que imprime por unidad id, goal, acceptance, verification_cmd, required_capability, risk y estimate; (b) gate de aprobacion de turno 0, el orchestrator rehusa ejecutar el turno 1 de un conjunto sin registro de aprobacion humana que referencie el plan aprobado (event log / mailbox firmado), y una modificacion material del plan (unidad nueva, acceptance o risk cambiado) invalida la aprobacion y exige re-aprobar.
  acceptance:
    - El comando de vista imprime la tabla completa del conjunto leyendo TASK_INDEX + los .md (proyeccion de los ficheros atestados, DECISION-0009; la vista jamas inventa ni corrige datos).
    - Gate de turno 0, sin registro de aprobacion verificable (p.ej. hash del render del plan aprobado referenciado en el event log o en mailbox firmado), el orchestrator rehusa arrancar con mensaje claro; con aprobacion registrada, arranca.
    - Cambio material respecto al plan aprobado (unidad nueva, acceptance o risk distinto) invalida la aprobacion previa; el mecanismo de comparacion (hash o diff de campos) queda documentado y probado.
    - Aprobar el conjunto es distinto de supervised_autonomy.human_checkpoint_every_k y NO lo enciende ni lo requiere.
    - Suites del runtime verdes; el gate se prueba en instancia scratch / examples, NUNCA se ejecuta el orchestrator en el hub en esta tanda.
  verification_cmd:
    - python examples/runtime_turn_cases/run_runtime_turn_cases.py
    - Suite nueva o extendida del gate de plan (runner en examples/, mismo patron run_*.py) en verde
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
  scope_routes:
    - runtime/orchestrator.py
    - runtime/
    - examples/
  out_of_scope:
    - Ejecutar el orchestrator en el hub - FUERA (validacion solo en scratch/examples; orden del Operador 2026-07-19).
    - Ampliar la definicion de cambio material mas alla de C1 (p.ej. carve-out de unidades de remediacion) - FUERA; esa precision es la nota de diseno N1 elevada al Operador y, si procede, enmienda de la 0103.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: medium
  estimate: M
---

# TASK-0260 - [DECISION-0103][C1] Vista de plan + gate turno 0

Origen: DECISION-0103 clausula 1, unidad 4 de la tabla. Depende del OK del plan (que,
por la paradoja de arranque, esta primera vez es manual via mailbox).
