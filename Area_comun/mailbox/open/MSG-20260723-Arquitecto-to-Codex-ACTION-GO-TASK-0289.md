---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-GO-TASK-0289
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0289 (R2/follow-up de DECISION-0103, residual del veredicto de TASK-0287, type=infra, maker=Codex, checker=Analista, risk=low, estimate=S). El fix de TASK-0287 anadio el arbol COMPLETO 'personal' al snapshot_inventory del modo full parcial (.githooks/pre-commit) para resolver deliverables de tarea bajo personal/** (TASK-0084 -> personal/Codex/STARTUP_PROMPT.md). Eso materializa CIENTOS de archivos y sube la latencia del full-hook local (HOOK_FULL=1). ACOTAR el coste: materializar SOLO las rutas de personal/** que son deliverables de tarea (resueltas desde los indices de tarea TASK_INDEX + TASK_INDEX_ARCHIVE), no el arbol personal/ entero -- o de otro modo reducir el coste de materializacion -- SIN reintroducir el falso-rechazo F1 (TASK-0287) y SIN debilitar C5. El modo default (partial-cost E6-A) NO cambia; el full-hook es opt-in local y el CI clon-limpio es la frontera dura. Acceptance: (1) el full-hook sobre arbol limpio sigue exit 0 (sin regresion F1), los deliverables antes omitidos (HUMAN_GUIDE.md, personal/Codex/STARTUP_PROMPT.md) siguen resolviendo presentes; (2) el full-hook sigue rechazando un estado gobernado genuinamente roto via validate (C5 intacta) Y las masking-probes siguen mordiendo (borrado staged de un deliverable inventariado -> exit 1); (3) la materializacion de personal/** se REDUCE de forma medible (solo las rutas-deliverable necesarias, o un conjunto acotado documentado); si un enfoque dirigido resulta inviable, documenta el motivo y deja el include amplio con el coste reconocido; (4) se prueba por el ENTRYPOINT REAL del hook (no atajos); pin SHA-256 del hook actualizado si el hook cambia; paridad CI mantenida. verification_cmd: HOOK_FULL=1 sh .githooks/pre-commit arbol limpio -> exit 0 (evidencia) + negativo (estado roto staged + HOOK_FULL=1 -> exit 1 via validate) + masking-probe (git rm --cached de un deliverable inventariado + HOOK_FULL=1 -> exit 1) + python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py -> 0 + validate + scan_encoding -> 0. Scope: .githooks/pre-commit + examples/ + .github/workflows/validate.yml (solo pin). FUERA: comportamiento del validador, reparto E6-A (default no cambia), REINTRODUCIR F1 (PROHIBIDO), fondo (protocol.config.json pineado 2E35F26E epoch 1.14.0, dataset N=500, reservadas N=6). Entrega TASK-0289 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas ETA para TASK-0289 y que el enfoque acotado (materializar solo las rutas-deliverable de personal/**, o el fallback documentado) mantiene el full-hook exit 0 en arbol limpio (sin regresion F1) Y sigue rechazando el estado roto + masking-probe (C5 intacta), probado por el entrypoint real del hook?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0289-r2-bound-fullhook-personal-materialization.md
  - Area_comun/artifacts/Analista-TASK-0287-hook-fullmode-inventory-verdict.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "GO TASK-0289 (R2): acotar la materializacion de personal/** del full-hook (latencia) a las rutas-deliverable, sin reintroducir F1 ni debilitar C5; evidencia por entrypoint real."
---

# ACTION - GO TASK-0289 (R2: acotar materializacion de personal/** en el full-hook)

Hora local: 2026-07-23 17:55 (UTC+2). Origen: residual R2 del veredicto del checker en TASK-0287.
Follow-up de mantenimiento autorizado por el Operador (GO explicito). Segunda unidad tras R1
(TASK-0288, ya cerrada). Ficha completa en
`Area_comun/tasks/TASK-0289-r2-bound-fullhook-personal-materialization.md`.

## El coste

El fix de 0287 inventario el arbol `personal` COMPLETO en el snapshot parcial del full-hook para que
`validate` resuelva los deliverables bajo personal/** (TASK-0084 -> `personal/Codex/STARTUP_PROMPT.md`).
Materializa cientos de archivos -> latencia del full-hook local (opt-in).

## LA GUARDA CRITICA (no reintroducir F1, no debilitar C5)

Acota la materializacion a las rutas-deliverable necesarias (resueltas de TASK_INDEX + archive), o
documenta por que el include amplio se mantiene. PROHIBIDO reintroducir el falso-rechazo F1: el
arbol limpio DEBE seguir en exit 0 con los deliverables (HUMAN_GUIDE.md, personal/Codex/STARTUP_PROMPT.md)
resolviendo presentes. C5 intacta: estado roto + masking-probe siguen mordiendo. Evidencia por el
entrypoint real del hook.

## Entrega esperada

TASK-0289 a `in_review` + handoff autocontenido con `verification_cmd` y exit codes (limpio->0;
negativo->1; masking-probe->1; regresion->0; validate/scan_encoding->0) + release del claim. ASCII
puro. Fix-loop tope 2 iteraciones.
