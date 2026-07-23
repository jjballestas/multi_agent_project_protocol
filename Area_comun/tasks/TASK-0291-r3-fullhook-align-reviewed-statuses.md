---
task_id: TASK-0291
title: "[DECISION-0103][R3/follow-up] Full-hook: alinear la materializacion de deliverables personal/ con la autoridad del validador (no ser mas estricto en tareas no-revisadas)"
type: infra
status: in_review
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0289, TASK-0287]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0291-r3-fullhook-align-reviewed-statuses.md
intake:
  type: infra
  goal: "Residual R3 del veredicto del checker en TASK-0289. El bloque del full-hook (.githooks/pre-commit) itera deliverables personal/ de tareas de CUALQUIER status y git checkout-index --force -- <path> FALLA-DURO si el path esta ausente del index staged -> rechazo. Pero el validador solo exige EXISTENCIA de deliverables para REVIEWED_TASK_STATUSES (validate_collaboration_state.py:1048). Divergencia: en tareas NO-revisadas (cancelled/proposed/ready/claimed/in_progress/blocked) el hook es mas estricto que el validador -> falso-rechazo sabor-F1 (latente hoy). Alinear el hook a la autoridad del validador: (opcion A) filtrar los deliverables personal/ extraidos por los mismos REVIEWED_TASK_STATUSES; o (opcion B) tolerar el checkout-index miss y dejar que el validador sea la autoridad. El maker elige e implementa una."
  acceptance:
    - "El full-hook sobre arbol limpio sigue exit 0 (sin regresion F1); el deliverable indexado (personal/Codex/STARTUP_PROMPT.md) resuelve presente."
    - "Una tarea NO-revisada que lista un deliverable personal/ AUSENTE ya NO hace que el hook rechace en falso (queda alineado con el validador, que lo tolera). Construir el probe y evidenciarlo."
    - "C5 intacta: una tarea REVISADA con un deliverable personal/ ausente SIGUE rechazando; un estado gobernado roto sigue rechazando via validate; la masking-probe sobre un deliverable de tarea revisada sigue mordiendo."
    - "Se prueba por el ENTRYPOINT REAL del hook; pin SHA-256 actualizado si el hook cambia; paridad CI; regresion (run_hook_fullmode_inventory_cases.py) verde."
  verification_cmd:
    - "HOOK_FULL=1 sh .githooks/pre-commit arbol limpio -> exit 0 (evidencia)"
    - "probe tarea NO-revisada + deliverable personal/ ausente -> hook NO rechaza en falso (evidencia; alineado con validador)"
    - "probe tarea REVISADA + deliverable personal/ ausente -> hook rechaza (C5, evidencia)"
    - "estado roto staged + HOOK_FULL=1 -> exit 1 via validate (evidencia)"
    - "python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py -> 0 ; validate -> 0 ; scan_encoding -> 0"
  scope_routes:
    - .githooks/pre-commit
    - examples/
    - .github/workflows/validate.yml
  out_of_scope:
    - "Cambiar el comportamiento del validador -- FUERA."
    - "Reintroducir el falso-rechazo F1 de arbol limpio -- PROHIBIDO."
    - "El reparto E6-A (default partial) -- FUERA."
    - "Fondo intocable (2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6) -- FUERA."
  risk: low
  estimate: S
---

# TASK-0291 - [DECISION-0103][R3] Full-hook alineado con REVIEWED_TASK_STATUSES

Origen: residual R3 del veredicto de TASK-0289 (divergencia hook>validador confirmada por probe del
checker). El hook rechaza deliverables personal/ ausentes de tareas NO-revisadas que el validador
tolera. Alinear (filtrar por reviewed statuses, o tolerar y delegar en el validador). No bloqueante.
