---
task_id: TASK-0269
title: "[DECISION-0103][E6-C] Optimizacion del hook v2: materializar SOLO las rutas que el validador lee y medir; insumo para re-decidir el completo-local"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0269-d0103-e6-materializacion-parcial-rutas-validador.md
intake:
  type: infra
  goal: Implementar la parte C de la enmienda E6 de DECISION-0103, reducir el coste del modo COMPLETO del hook v2 (hoy 51.5-53.3s, del cual ~39s es materializar el arbol entero) materializando en el temporal SOLO las rutas que validate_collaboration_state realmente lee (Area_comun/**, runtime/state/**, scripts/, .githooks/, configs, AGENTS.md y las que el inventario determine), medir frio/caliente, y entregar la cifra como INSUMO para que el Operador re-decida si reactiva el completo-local (E6 dice que con ~15s o menos la pregunta se reabre; la decision es del Operador, no de esta unidad).
  acceptance:
    - Inventario verificable de las rutas que el validador lee (derivado del codigo, no supuesto) documentado en el handoff; la materializacion parcial las cubre TODAS (si falta una, el juicio mentiria, asi que se anade un negativo que rompa una ruta fuera del inventario inicial para probar la completitud).
    - El modo completo (bajo flag, reparto E6-A) usa la materializacion parcial y su veredicto es IDENTICO al de la materializacion total en toda la suite (positivos, negativos, borrados, rename, concurrencia) -- cero perdida de correccion.
    - Coste medido frio/caliente declarado en el handoff, junto al desglose (materializar vs validar); objetivo de referencia ~15s o menos, sin ser criterio de fallo (la cifra que salga es el entregable).
    - REPORTE final al Operador con la cifra y la recomendacion argumentada de mantener el reparto E6-A o reactivar completo-local (la unidad OFRECE, el Operador decide).
    - Limpieza robusta del temporal intacta; espejo born-operational; neutralidad, validate y encoding verdes.
  verification_cmd:
    - Suite del hook completa en verde con materializacion parcial (veredictos identicos a la total)
    - Negativo de completitud del inventario (ruta fuera del set inicial -> cazada)
    - Medicion frio/caliente en el handoff con desglose
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - .githooks/pre-commit
    - scripts/test_precommit_hook.py
    - examples/
  out_of_scope:
    - Cambiar la logica del validador o que rutas lee - FUERA (la unidad se adapta al validador, no al reves).
    - Re-decidir el reparto local/CI - FUERA (decision del Operador con la cifra).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: low
  estimate: M
---

# TASK-0269 - [E6-C] Materializacion parcial y medicion

Origen: enmienda E6 de DECISION-0103 (orden del Operador 2026-07-20, "luego GO C").
SECUENCIA: despues de TASK-0268 (comparten .githooks/pre-commit y la parte A define el
reparto sobre el que esta optimiza). Su GO lo emite el Arquitecto al cierre de 0268.
