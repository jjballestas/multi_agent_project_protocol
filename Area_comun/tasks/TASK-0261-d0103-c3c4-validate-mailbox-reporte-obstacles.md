---
task_id: TASK-0261
title: "[DECISION-0103][C3/C4] validate_mailbox exige obstacles + contador de friccion en mensajes type REPORTE (carril sesion), con grandfathering del historico"
type: feature
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0261-d0103-c3c4-validate-mailbox-reporte-obstacles.md
intake:
  type: feature
  goal: Implementar el carril sesion de DECISION-0103 C3/C4 en validate_mailbox (scripts/validate_collaboration_state.py), los mensajes type REPORTE de entrega de unidad gobernada exigen el bloque obstacles bien formado (mismos 4 campos + enum que el turn_schema de TASK-0258) mas un contador minimo de friccion (friction_count, reintentos / rechazos de gate / correcciones del checker), con el cruce friction_count mayor que 0 Y obstacles vacio = FAIL, que es el espejo sesion de la regla runtime.
  acceptance:
    - Mensaje type REPORTE de entrega sin bloque obstacles bien formado o sin friction_count -> validate exit distinto de 0 con mensaje accionable.
    - friction_count mayor que 0 con obstacles vacio -> FAIL; friction_count 0 con obstacles vacio -> PASA (lista vacia legitima).
    - GRANDFATHERING obligatorio, la regla aplica solo a mensajes con date igual o posterior a la fecha de adopcion (o marker de version de schema en el frontmatter); el historico de open/, answered/ y archived/ NO se pone rojo (validate barre las 3 carpetas).
    - El limite presencia-vs-veracidad del carril sesion queda documentado donde declara C4 (el validador fuerza presencia y forma; la veracidad del contador es del agente y se declara como expuesta).
    - Suite de casos mailbox cubre los 4 cuadrantes (friccion x obstacles) + el caso grandfathered, todos con el resultado esperado.
    - validate exit 0 sobre el arbol actual del hub con el historico intacto.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - Runner de la suite de casos mailbox correspondiente (examples/, patron run_*.py) en verde
    - python scripts/scan_encoding.py
  scope_routes:
    - scripts/validate_collaboration_state.py
    - examples/
    - Area_comun/protocol/
  out_of_scope:
    - La plantilla del mensaje (TASK-0262, coordinar el MISMO bloque; esta unidad valida, no redacta plantillas).
    - Sensores automaticos de friccion en sesion - FUERA (C4 declara que no existen; el contador es declarativo).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: medium
  estimate: M
---

# TASK-0261 - [DECISION-0103][C3/C4] validate_mailbox: obstacles + friccion en REPORTE

Origen: DECISION-0103 clausulas 3 y 4, unidad 5 de la tabla. El riesgo es que una regla
nueva sobre un canal vivo pinte rojo el historico; el grandfathering por fecha/marker es
la mitigacion y es parte del acceptance, no opcional. Depende del OK del plan y de la
convencion de bloque fijada con TASK-0258/0262.
