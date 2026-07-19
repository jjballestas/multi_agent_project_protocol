---
task_id: TASK-0265
title: "[DECISION-0103][gate] Revision adversarial del conjunto TASK-0257..0264 por el checker formal de proveedor diverso (DECISION-0101)"
type: doc
status: ready
owner: Analista
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Arquitecto
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0101, DECISION-0099]
linked_decisions: [DECISION-0103, DECISION-0101]
file: Area_comun/tasks/TASK-0265-d0103-gate-revision-adversarial-conjunto.md
intake:
  type: doc
  goal: Gate final de la tanda DECISION-0103, revision adversarial del CONJUNTO de unidades TASK-0257..TASK-0264 por el checker formal de proveedor diverso (DECISION-0101, maker OpenAI/Codex, checker Anthropic/Claude), verificando cada acceptance contra el codigo real en CLON LIMPIO de HEAD e intentando romper activamente los mecanismos nuevos (hook, gate de turno 0, cruce de friccion, no-re-oferta).
  acceptance:
    - Veredicto por unidad (GO / NO-GO con hallazgos accionables file:line + repro) emitido por mailbox, verificado en clon limpio de HEAD, no en working tree caliente.
    - Pruebas adversariales minimas ejecutadas y evidenciadas, (a) commit con estado rojo que el hook DEBE rechazar; (b) turno runtime con friccion y obstacles vacio rechazado; (c) mensaje REPORTE con friction_count mayor que 0 y obstacles vacio rechazado; (d) historico de mailbox sigue verde (grandfathering); (e) propuesta rechazada en el registro de ofertas NO se re-ofrece.
    - Residuales honestos declarados (lo que no se pudo probar y por que).
    - El veredicto NO ratifica nada por si mismo, la ratificacion y los flips de cierre siguen el flujo normal (Arquitecto ratifica, Codex ejecuta los done-flips).
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - Runners de las suites de las unidades 2-7 en verde en el clon limpio
    - Evidencia de las 5 pruebas adversariales en el reporte del veredicto
  scope_routes:
    - Area_comun/mailbox/open/
  out_of_scope:
    - Corregir codigo (checker-only, DECISION-0099; los hallazgos vuelven al maker como remediacion).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: low
  estimate: M
---

# TASK-0265 - [DECISION-0103][gate] Revision adversarial del conjunto

Origen: DECISION-0103 unidad 9 de la tabla (gate). Va ULTIMA, cuando 0257..0264 esten
in_review. El Analista es checker-only (no maker); sus mensajes de mailbox seran
file-scoped. OK del plan recibido 2026-07-19. Nota (enmienda E2): TASK-0257 tiene
ademas un gate propio inmediato al aterrizar; este gate final barre el conjunto
igualmente, incluida 0257 en su version final.
