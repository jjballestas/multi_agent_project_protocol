---
task_id: TASK-0289
title: "[DECISION-0103][R2/follow-up] Acotar la materializacion de personal/** en el snapshot parcial del full-hook (latencia) sin reintroducir el falso-rechazo F1 ni debilitar C5"
type: infra
status: done
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-23
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, TASK-0287]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0289-r2-bound-fullhook-personal-materialization.md
intake:
  type: infra
  goal: "Residual R2 del veredicto del checker en TASK-0287. El fix de 0287 anadio el arbol COMPLETO 'personal' al snapshot_inventory del modo full parcial para que el validador resuelva los deliverables de tarea bajo personal/** (TASK-0084 -> personal/Codex/STARTUP_PROMPT.md). Eso materializa CIENTOS de archivos y sube la latencia del full-hook local (HOOK_FULL=1). Acotar el coste: materializar SOLO las rutas de personal/** que son deliverables de tarea (resueltas desde los indices de tarea), no el arbol personal/ entero -- o de otro modo reducir el coste de materializacion -- SIN reintroducir el falso-rechazo F1 y SIN debilitar C5. El modo default (partial-cost E6-A) NO cambia; el full-hook es opt-in local y el CI clon-limpio es la frontera dura."
  acceptance:
    - "El full-hook sobre un arbol limpio sigue en exit 0 (sin regresion F1); los deliverables antes omitidos (HUMAN_GUIDE.md, personal/Codex/STARTUP_PROMPT.md) siguen resolviendo como presentes."
    - "El full-hook sigue rechazando un estado gobernado genuinamente roto via validate (C5 intacta) Y las masking-probes siguen mordiendo (borrado staged de un deliverable inventariado -> exit 1)."
    - "La materializacion de personal/** se REDUCE de forma medible (solo las rutas-deliverable necesarias, o un conjunto acotado documentado); si un enfoque dirigido resulta inviable, documentar el motivo y dejar el include amplio con el coste reconocido explicitamente."
    - "Se prueba por el ENTRYPOINT REAL del hook (no atajos); pin SHA-256 del hook actualizado si el hook cambia; paridad CI mantenida."
  verification_cmd:
    - "HOOK_FULL=1 sh .githooks/pre-commit sobre arbol limpio -> exit 0 (evidencia)"
    - "negativo (estado gobernado roto staged + HOOK_FULL=1) -> exit 1 via validate (evidencia)"
    - "masking-probe (git rm --cached de un deliverable inventariado + HOOK_FULL=1) -> exit 1 (evidencia)"
    - "python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py -> exit 0"
    - "python scripts/validate_collaboration_state.py -> 0 ; python scripts/scan_encoding.py -> 0"
  scope_routes:
    - .githooks/pre-commit
    - examples/
    - .github/workflows/validate.yml
  out_of_scope:
    - "Cambiar el comportamiento del validador (validate_collaboration_state) -- FUERA."
    - "El reparto E6-A (modo partial por defecto) -- FUERA; el default no cambia."
    - "Reintroducir el falso-rechazo F1 (TASK-0287) -- PROHIBIDO."
    - "Fondo intocable: protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E), dataset N=500, reservadas N=6 -- FUERA."
  risk: low
  estimate: S
---

# TASK-0289 - [DECISION-0103][R2] Acotar materializacion de personal/** en el full-hook

Origen: residual R2 declarado por el checker (Analista) en el veredicto de TASK-0287. El fix de 0287
inventario el arbol `personal` completo para resolver deliverables bajo personal/**, subiendo la
latencia del full-hook local (opt-in). Acotar a las rutas-deliverable necesarias sin reintroducir el
falso-rechazo F1 ni debilitar C5. Follow-up no bloqueante; el CI clon-limpio es la frontera dura.
