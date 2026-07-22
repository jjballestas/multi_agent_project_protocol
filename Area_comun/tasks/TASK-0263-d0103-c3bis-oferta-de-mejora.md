---
task_id: TASK-0263
title: "[DECISION-0103][C3-bis] Mecanismo de oferta de mejora: recurrence_risk high o root_cause repetido -> propuesta redactada al humano + registro durable de aceptar/rechazar/parquear"
type: feature
status: in_review
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0263-d0103-c3bis-oferta-de-mejora.md
intake:
  type: feature
  goal: Implementar la clausula 3-bis de DECISION-0103 en ambos carriles, deteccion de obstaculos candidatos a mejora (recurrence_risk high, o el mismo root_cause en dos o mas entregas, sobre run-logs y mensajes REPORTE) que genera una OFERTA al humano con la propuesta de skill/regla YA REDACTADA (borrador del cambio concreto, no un consejo generico), y un registro durable de la respuesta humana (aceptar / rechazar / parquear) que evita re-ofrecer la misma propuesta en bucle. Ofrece, NO crea, ningun agente modifica protocolo ni skill por su cuenta.
  acceptance:
    - Deteccion implementada sobre los obstacles de ambos carriles con criterio documentado y determinista de mismo root_cause (match exacto o clave normalizada; sin heuristica opaca).
    - La oferta generada incluye el borrador del cambio concreto (texto de la skill/regla propuesta) y cita los obstaculos que la motivan.
    - Registro durable de ofertas y respuestas en ruta gobernada (definir en el diseno de la unidad, p.ej. JSON en Area_comun/), consultado antes de ofrecer, una propuesta rechazada o parqueada NO se re-ofrece salvo evidencia nueva declarada.
    - Cero rutas de auto-aplicacion, el output es una oferta en el reporte/mailbox; el cambio real va por el flujo normal (DECISION + tarea) solo si el humano acepta.
    - Suite de casos, recurrence_risk high genera oferta; root_cause repetido x2 genera oferta; rechazada no se re-ofrece; aceptada queda marcada; sin candidatos no ofrece nada.
  verification_cmd:
    - Runner de la suite nueva del mecanismo (examples/, patron run_*.py) en verde
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - scripts/
    - runtime/
    - examples/
    - Area_comun/protocol/
  out_of_scope:
    - Crear o modificar skills/reglas automaticamente - PROHIBIDO por la propia clausula (ofrece, no crea).
    - Los bloques obstacles en si (TASK-0258/0259/0261, dependencias previas).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA.
  risk: medium
  estimate: L
---

# TASK-0263 - [DECISION-0103][C3-bis] Oferta de mejora

Origen: DECISION-0103 clausula 3-bis, unidad 7 de la tabla. Es la unidad mas grande de
la tanda (estimate L), depende de que el bloque obstacles exista en ambos carriles
(TASK-0258/0259/0261) y del OK del plan. El maker presenta el diseno del registro
durable (ruta y forma) en su primer handoff antes de construir, para que el checker
pueda objetar la forma temprano.
