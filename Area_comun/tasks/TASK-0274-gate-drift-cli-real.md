---
task_id: TASK-0274
title: "[HIGIENE-GATE] El gate de drift declarado es VACUO: dar entrypoint CLI real a protocol_replay.py y corregir toda la documentacion que lo cita como prueba"
type: infra
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0022]
linked_decisions: [DECISION-0022]
file: Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
intake:
  type: infra
  goal: "El comando que los tres participantes venimos citando como gate de drift, python runtime/protocol_replay.py --check-drift, NO PRUEBA NADA, protocol_replay.py no tiene entrypoint CLI (sin bloque __main__, sin argparse), asi que importa el modulo y sale 0 con CUALQUIER argumento. Verificado por el checker en el re-juicio de TASK-0272 (F-0272R1-05) y RECOMPUTADO de forma independiente por el Arquitecto, --bogus-flag devuelve exit 0. El chequeo real vive en la funcion protocol_state_drift(), que si discrimina (hoy has_drift=False, up_to_seq 5317). El dano es de FALSA GARANTIA, aparece en handoffs, en veredictos de review y en cuerpos de commit como evidencia de que el ledger no tiene deriva, cuando el exit 0 era incondicional. Esta unidad convierte el gate en real y limpia las citas."
  acceptance:
    - "python runtime/protocol_replay.py --check-drift devuelve exit 0 SOLO si protocol_state_drift() reporta has_drift False, y exit distinto de 0 si reporta deriva."
    - "Un flag desconocido (por ejemplo --bogus-flag) devuelve exit distinto de 0 en vez de 0, para que un error de tipeo no vuelva a fabricar un verde."
    - "Salida legible con el veredicto y el up_to_seq alcanzado, para que el que lo corre pueda citarlo con numero."
    - "Prueba negativa permanente que fabrica deriva en un sandbox y exige exit distinto de 0, mas la positiva sobre el ledger limpio."
    - "Barrido de la documentacion viva que cita el comando (README del runtime, plantillas de handoff, skills y runbooks de instancia) para que ninguna lo presente como gate sin el CLI real."
    - "Espejo en el export born-operational, la instancia nacida hereda el gate real, no el vacuo."
  verification_cmd:
    - "python runtime/protocol_replay.py --check-drift ; echo $? (exit 0 sobre el ledger limpio)"
    - "python runtime/protocol_replay.py --bogus-flag ; echo $? (exit distinto de 0)"
    - "Runner de la prueba negativa de deriva en verde"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - runtime/protocol_replay.py
    - examples/
    - scripts/
    - Area_comun/protocol/
  out_of_scope:
    - "Cambiar la semantica de la deteccion de deriva (que se considera drift) - FUERA, solo se le pone una puerta real a lo que ya calcula."
    - "Tocar el ledger, el snapshot o reescribir eventos - PROHIBIDO."
    - "protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: low
  estimate: S
---

# TASK-0274 - El gate de drift no era un gate

Origen: hallazgo F-0272R1-05 del re-juicio de TASK-0272, con un retracto parcial honesto
del propio checker (su veredicto anterior citaba el mismo comando vacuo). El Arquitecto
lo recomputo por su cuenta antes de registrar la unidad: `--bogus-flag` sale 0.

Lo grave no es el bug, es la clase, un gate que no puede fallar aparece en la evidencia
de todos los cierres recientes. Mientras esta unidad no cierre, quien necesite afirmar
que no hay deriva debe correr la funcion `protocol_state_drift()` y citar el `up_to_seq`,
no el comando.

Pertenece a la tanda 0103 por herencia de la clausula C3, la evidencia que se reporta en
una entrega tiene que ser verificable de verdad.
