---
task_id: TASK-0292
title: "[DECISION-0103][R4/follow-up] Regresion full-hook: la masking-probe debe asegurar la RAZON del rechazo (boundary del validador), no solo returncode!=0"
type: infra
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0289, TASK-0291]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0292-r4-masking-probe-assert-reason.md
intake:
  type: infra
  goal: "Residual R4 del veredicto del checker en TASK-0289. En examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py la masking-probe asegura solo returncode!=0, no la RAZON. Post-0289 esa prueba pasa via checkout-index ('could not materialize'), NO via el 'deliverable missing' / boundary del validador. C5 no se debilita (los deliverables de tareas revisadas estan doblemente cubiertos), pero la prueba ya NO demuestra que muerde el camino del VALIDADOR. Reforzar el assert para atribuir el rechazo al boundary del validador (como ya hace el caso de estado-roto). NOTA: depende de TASK-0291 (R3) -- si R3 tolera el checkout-index miss, la masking-probe de tarea revisada pasara a rechazar via validate y este assert sera el correcto; coordinar orden."
  acceptance:
    - "La masking-probe de un deliverable de tarea REVISADA asegura la RAZON del rechazo atribuible al validador (p.ej. 'deliverable missing' / 'collaboration state ... invalid'), no solo returncode!=0."
    - "El caso sigue verde (exit 0 del runner) y el hook sigue rechazando (fail-closed); ningun cambio de comportamiento del hook por este test."
    - "Coordinar con TASK-0291 (R3): el assert refleja el camino de rechazo resultante tras R3."
  verification_cmd:
    - "python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py -> exit 0 (con el assert de razon reforzado)"
    - "python scripts/validate_collaboration_state.py -> 0 ; python scripts/scan_encoding.py -> 0"
  scope_routes:
    - examples/
  out_of_scope:
    - "Cambiar el comportamiento del hook o del validador -- FUERA (solo el assert del test)."
    - "Fondo intocable -- FUERA."
  risk: low
  estimate: S
---

# TASK-0292 - [DECISION-0103][R4] masking-probe asegura la razon del rechazo

Origen: residual R4 del veredicto de TASK-0289. La masking-probe solo asegura returncode!=0; post-0289
pasa via checkout-index, no via el validador. Reforzar el assert de razon. Depende de R3 (TASK-0291)
para el camino de rechazo final. Menor, no bloqueante.
