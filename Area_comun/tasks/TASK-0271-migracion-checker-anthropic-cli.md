---
task_id: TASK-0271
title: "[DECISION-0101] Migracion del harness del checker formal al CLI de Anthropic (Claude): implementa la decision firmada; elimina los flags del clasificador sobre trabajo adversarial legitimo"
type: infra
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Arquitecto
project: multi_agent_project_protocol
relates_to: [DECISION-0101, DECISION-0099]
linked_decisions: [DECISION-0101]
file: Area_comun/tasks/TASK-0271-migracion-checker-anthropic-cli.md
intake:
  type: infra
  goal: Implementar DECISION-0101 (firmada 2026-07-17, sin tarea de implementacion hasta hoy), el harness del Analista (analista_mailbox_cron.ps1 y su invoker de exec) migra su runtime de exec del CLI de OpenAI al CLI de Anthropic (claude), conservando INTACTO el contrato del protocolo (lectura de mailbox, envelope de veredicto, artefactos, trailers, STOP_JOB por igualdad exacta post-0236, seen.json, locks/leases). Motivo operativo re-confirmado el 2026-07-20: el clasificador de OpenAI mato 2 veces el exec de la review de TASK-0267 a mitad de escritura de pruebas adversariales (mismo patron que motivo la decision, 5+ flags historicos). GO del Operador en orden directa 2026-07-20.
  acceptance:
    - El harness migrado invoca el CLI de Anthropic para el exec del turno con el MISMO contrato de entrada/salida (mailbox in -> review -> veredicto MSG + artefacto + commit con trailers); diversidad de proveedor preservada y documentada (maker OpenAI != checker Anthropic, corazon de 0101).
    - Semanticas del harness intactas y verificadas, STOP_JOB solo por igualdad exacta (0236), firma seen por nombre|longitud|mtime, max_no_arquitecto_rounds, lock/lease por exec.
    - ROLLBACK ensayado, el .ps1 anterior queda preservado y el procedimiento de vuelta atras (parar cron nuevo, relanzar viejo) documentado en el handoff; el cutover en vivo es un paso OPERADO (relanzamiento gateado por autorizacion de sesion), no automatico.
    - Verificacion end-to-end con un turno REAL controlado, un mensaje REVIEW de prueba en sandbox (o el primer encargo real post-cutover con supervision) produce veredicto completo sin flags del clasificador; evidencia en el handoff.
    - Latencia/coste por exec anotados como dato comparativo (sin umbral de fallo).
    - Sin secretos en el repo (API keys por entorno local, jamas commiteadas); ASCII; neutralidad.
  verification_cmd:
    - Turno de review de prueba end-to-end con veredicto producido (evidencia en handoff)
    - Prueba del detector STOP_JOB (igualdad exacta) en el harness migrado
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - personal/Analista/
    - Area_comun/protocol/
  out_of_scope:
    - Cambiar el protocolo de review o el formato de veredictos - FUERA.
    - El cutover en vivo del cron (operacion del Arquitecto con autorizacion de sesion, tras el veredicto de esta unidad) - FUERA del build.
    - Harness de Codex (el maker se queda en su proveedor; la diversidad es el punto) - FUERA.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: medium
  estimate: M
---

# TASK-0271 - [DECISION-0101] Migracion del checker a Anthropic CLI

Origen: DECISION-0101 firmada sin tarea de implementacion (hueco detectado el
2026-07-20 al ser flageado el exec del checker 2x durante la review de 0267); GO del
Operador en orden directa. REVIEWER = Arquitecto (el Analista no puede auto-revisar el
swap de su propio runtime; la verificacion es ratificacion del Arquitecto + evidencia
del turno end-to-end + primer encargo real supervisado). SECUENCIA: build puede
arrancar tras el veredicto de 0267 (no cambiar el juez a mitad de un juicio); si el
retry de 0267 vuelve a ser flageado, esta unidad se ADELANTA como desbloqueador y la
review pendiente se cubre con checker informal Anthropic declarado (checker_formal=0,
patron ya probado 2x en este proyecto).
