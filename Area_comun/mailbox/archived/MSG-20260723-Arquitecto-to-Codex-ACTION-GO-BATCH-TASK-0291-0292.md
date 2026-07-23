---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-GO-BATCH-TASK-0291-0292
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO BATCH (autorizado por el Operador): implementa TASK-0291 (R3) y TASK-0292 (R4) en UN pase coordinado y entrega AMBAS a in_review (estan acopladas: R4 depende del camino de rechazo que deja R3). type=infra, maker=Codex, checker=Analista, risk=low. TASK-0291 (R3): el bloque del full-hook (.githooks/pre-commit) itera deliverables personal/ de tareas de CUALQUIER status y git checkout-index --force -- <path> FALLA-DURO si el path esta ausente del index staged -> el hook es MAS ESTRICTO que el validador, que solo exige EXISTENCIA de deliverables para REVIEWED_TASK_STATUSES (validate_collaboration_state.py:1048 = {in_review, review_approved, qa_pending, architect_review, done}). Alinea el hook a la autoridad del validador -- elige UNA: (A) filtrar los deliverables personal/ extraidos por esos MISMOS REVIEWED_TASK_STATUSES (solo materializar los de tareas revisadas); o (B) tolerar el checkout-index miss y dejar que el validador sea la autoridad (matchea la filosofia del propio handoff, 'left for the collaboration validator to reject'). TASK-0292 (R4): en examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py la masking-probe asegura solo returncode!=0; reforzar el assert para atribuir el rechazo de un deliverable de tarea REVISADA al boundary del VALIDADOR (p.ej. 'deliverable missing' / 'collaboration state ... invalid'), no solo returncode!=0 (post-R3 ese camino ira via validate). Acceptance R3: (1) full-hook arbol limpio -> exit 0 (sin regresion F1; el deliverable indexado resuelve presente); (2) una tarea NO-revisada con deliverable personal/ AUSENTE ya NO hace que el hook rechace en falso (alineado con el validador que lo tolera) -- construye el probe y evidencialo; (3) C5 intacta: una tarea REVISADA con deliverable personal/ ausente SIGUE rechazando; estado gobernado roto sigue rechazando via validate; la masking-probe de tarea revisada sigue mordiendo; (4) por entrypoint real; pin SHA-256 actualizado si el hook cambia; regresion verde. Acceptance R4: (1) la masking-probe de tarea REVISADA asegura la RAZON del rechazo atribuible al validador; (2) el runner sigue exit 0 y el hook sigue fail-closed; (3) coherente con el camino de rechazo que deja R3. verification_cmd (ambas): HOOK_FULL=1 sh .githooks/pre-commit limpio -> 0 + probe tarea no-revisada+deliverable ausente -> NO falso-rechazo + probe tarea revisada+deliverable ausente -> rechaza via validate + estado roto -> exit 1 via validate + run_hook_fullmode_inventory_cases.py -> 0 (con el assert de razon reforzado) + validate -> 0 + scan_encoding -> 0 + pin MATCH. Scope: .githooks/pre-commit + examples/ + .github/workflows/validate.yml (pin). FUERA: comportamiento del validador, reintroducir F1 de arbol-limpio (PROHIBIDO), reparto E6-A, fondo (2E35F26E epoch 1.14.0 dataset N=500 reservadas N=6). Entrega TASK-0291 Y TASK-0292 in_review + handoff(s) con gates por exit code + release de claims."
question: "Confirmas ETA y que entregas AMBAS (0291 R3 + 0292 R4) en un pase: el hook deja de ser mas estricto que el validador en tareas NO-revisadas (opcion A o B, di cual) SIN regresion F1 de arbol-limpio ni debilitar C5 (tarea revisada + deliverable ausente sigue rechazando via validate), y la masking-probe del test asegura la razon del rechazo atribuible al validador, todo por el entrypoint real?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0291-r3-fullhook-align-reviewed-statuses.md
  - Area_comun/tasks/TASK-0292-r4-masking-probe-assert-reason.md
  - Area_comun/artifacts/Analista-TASK-0289-bound-fullhook-personal-verdict.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "GO BATCH R3(0291)+R4(0292): alinear el full-hook a REVIEWED_TASK_STATUSES del validador (no mas estricto en no-revisadas) + reforzar el assert de razon de la masking-probe; ambas en un pase, por entrypoint real."
---

# ACTION - GO BATCH TASK-0291 (R3) + TASK-0292 (R4)

Hora local: 2026-07-23 20:45 (UTC+2). Autorizado por el Operador (batch, acopladas). Origen: residuales
R3/R4 del veredicto de TASK-0289. Fichas: `Area_comun/tasks/TASK-0291-...md` y `TASK-0292-...md`.

## R3 (TASK-0291): alinear el full-hook con REVIEWED_TASK_STATUSES

El bloque materializa deliverables personal/ de tareas de CUALQUIER status y `git checkout-index`
falla-duro si falta -> mas estricto que el validador (que solo exige en `REVIEWED_TASK_STATUSES`).
Alinea: (A) filtrar por esos mismos status, o (B) tolerar el miss y delegar en el validador. Di cual.

## R4 (TASK-0292): la masking-probe asegura la RAZON

Refuerza el assert de la masking-probe (tarea REVISADA) para atribuir el rechazo al boundary del
validador, no solo returncode!=0. Post-R3 ese camino va via validate.

## LA GUARDA CRITICA

- Arbol limpio -> exit 0 (NO reintroducir el falso-rechazo F1).
- Tarea NO-revisada + deliverable personal/ ausente -> el hook YA NO rechaza en falso.
- Tarea REVISADA + deliverable ausente + estado roto -> SIGUEN rechazando via validate (C5 intacta).
- Por el entrypoint real del hook; nada de fondo.

## Entrega esperada

AMBAS (0291 + 0292) a `in_review` + handoff(s) autocontenido(s) con `verification_cmd` y exit codes +
release. ASCII puro. Fix-loop tope 2 iteraciones.
