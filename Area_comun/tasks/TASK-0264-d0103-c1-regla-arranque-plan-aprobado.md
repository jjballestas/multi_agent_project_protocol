---
task_id: TASK-0264
title: "[DECISION-0103][C1] Regla de arranque documentada: ningun conjunto de unidades gobernadas se ejecuta sin plan aprobado por el humano"
type: doc
status: review_approved
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0096]
linked_decisions: [DECISION-0103, DECISION-0096]
file: Area_comun/tasks/TASK-0264-d0103-c1-regla-arranque-plan-aprobado.md
intake:
  type: doc
  goal: Documentar en el protocolo la regla de arranque de DECISION-0103 C1, ningun conjunto de unidades gobernadas se ejecuta sin que el humano haya visto y aprobado la lista (tabla id/goal/acceptance/verification_cmd/required_capability/risk/estimate), con aprobacion registrada (event log / mailbox firmado) y re-aprobacion ante cambio material; quien presenta el plan (Asesor u orquestador) no arranca ejecucion antes del OK registrado.
  acceptance:
    - Regla anadida en Area_comun/protocol/TASK_PROTOCOL.md (o el doc equivalente del ciclo de vida) citando DECISION-0103 C1, con la tabla de campos del plan y el requisito de registro de la aprobacion.
    - Espejo en el export born-operational (DECISION-0096) si el doc exportado contiene esa seccion, para que instancias nuevas nazcan con la regla.
    - FYI por mailbox a los participantes afectados (Asesor) indicando que la regla esta publicada; cada participante actualiza su propio prompt de arranque en su area privada.
    - ASCII puro y neutralidad de dominio en todo lo publicado.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - Area_comun/protocol/TASK_PROTOCOL.md
    - AGENTS.template.md
    - Area_comun/mailbox/open/
  out_of_scope:
    - Editar personal/asesor/ o cualquier area privada ajena - FUERA (cada participante actualiza la suya).
    - El gate mecanico de turno 0 (TASK-0260; esta unidad es la regla escrita, no el enforcement).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
  risk: low
  estimate: S
---

# TASK-0264 - [DECISION-0103][C1] Regla de arranque: plan aprobado primero

Origen: DECISION-0103 clausula 1 (lado doc), unidad 8 de la tabla. Depende del OK del
plan. El mensaje de mailbox que esta unidad emita sera file-scoped (MSG concreto), nunca
claim dir-level sobre el canal.
