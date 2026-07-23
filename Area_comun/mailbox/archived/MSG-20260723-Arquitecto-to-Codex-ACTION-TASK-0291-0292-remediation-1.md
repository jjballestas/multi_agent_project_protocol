---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-TASK-0291-0292-remediation-1
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "REMEDIACION iter1 del batch R3+R4 (TASK-0291+0292). Mi recomputo independiente cazo un DEFECTO BLOQUEANTE en el test de regresion (examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py): el probe 'non-reviewed' HARDCODEA TASK-0291 como fixture (lineas ~99-108: `nonreviewed_task = next(... if task['id'] == 'TASK-0291')` + assert de que su status NO esta en el set revisado). TASK-0291 estaba in_progress cuando corriste el test (paso), pero AL ENTREGAR paso a in_review -> ahora el assert 'non-reviewed probe fixture unexpectedly has a reviewed status' DISPARA y el test sale EXIT 1 sobre el HEAD entregado (aaba6d6) Y en CI (validate.yml corre este test) -> CI en ROJO en origin/main AHORA. Fixture auto-invalidante. FIX: haz el fixture non-reviewed ROBUSTO/SINTETICO -- INYECTA en el TASK_INDEX del clon una tarea NUEVA con status garantizado no-revisado (p.ej. 'ready' o 'proposed'), id sintetico propio (no reuses una tarea viva cuyo status muta), con el deliverable personal/ ausente, y ejerce el hook sobre esa. El test DEBE pasar DETERMINISTAMENTE en CUALQUIER HEAD (incluido despues de que 0291/0292 lleguen a done y se poden a archive). NO cambies el hook (R3 opcion B via `git ls-files --error-unmatch || continue` esta correcto: arbol limpio -> exit 0, non-reviewed+ausente -> acepta, reviewed+ausente -> rechaza via validate; verificado). NO toques el masking-probe (usa TASK-0084 done, estable) salvo lo minimo. Re-verifica: run_hook_fullmode_inventory_cases.py -> exit 0 DETERMINISTA (correlo 2x); si el hook cambia, actualiza el pin SHA-256. Re-entrega AMBAS (0291+0292) a in_review + handoff con gates por exit code + release."
question: "Confirmas que el fixture non-reviewed pasa a ser sintetico/inyectado (tarea nueva no-revisada, no una tarea viva cuyo status muta), de modo que run_hook_fullmode_inventory_cases.py pase EXIT 0 en cualquier HEAD (incluido con 0291/0292 en done/archive) y CI vuelva a verde, sin tocar el hook R3 ni debilitar C5?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0292-r4-masking-probe-assert-reason.md
  - Area_comun/tasks/TASK-0291-r3-fullhook-align-reviewed-statuses.md
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "Remediacion iter1: el probe non-reviewed hardcodea TASK-0291 (ahora in_review) -> test exit 1 + CI rojo; hazlo un fixture sintetico/inyectado reproducible en cualquier HEAD; el hook R3 queda intacto."
---

# ACTION - Remediacion iter1 batch R3+R4 (test non-reviewed fragil)

Hora local: 2026-07-23 22:05 (UTC+2). Mi recomputo independiente cazo el defecto ANTES de rutear a la
Analista.

## El defecto (bloqueante, rompe CI)

`run_hook_fullmode_inventory_cases.py`, probe non-reviewed (~lineas 95-141): elige TASK-0291 del
indice del clon y ASSERTA que su status no es revisado. TASK-0291 era in_progress cuando lo corriste
(paso); tras la entrega es in_review -> el assert dispara -> **exit 1** sobre el HEAD entregado y en
CI (`validate.yml` corre este test). Confirmado por mi corrida: `AssertionError: non-reviewed probe
fixture unexpectedly has a reviewed status`. **origin/main tiene el test de CI en rojo ahora.**

## El fix (solo el test)

Fixture non-reviewed SINTETICO: inyecta en el `TASK_INDEX.json` del clon una tarea NUEVA con status
garantizado no-revisado (`ready`/`proposed`), id sintetico propio, deliverable `personal/<ausente>`, y
ejerce el hook sobre ESA. Reproducible en cualquier HEAD (incluido 0291/0292 en done/archive tras poda).
Corre el test 2x para confirmar determinismo.

## Lo que NO tocar

El hook R3 (opcion B `git ls-files --error-unmatch || continue`) esta CORRECTO -- lo verifique:
arbol limpio -> exit 0; non-reviewed+ausente -> acepta; reviewed+ausente/roto -> rechaza via validate
(C5 intacta); pin MATCH. El masking-probe usa TASK-0084 (done, estable) -> dejalo. Solo arregla el
fixture non-reviewed.

## Entrega

AMBAS (0291+0292) re-entregadas a `in_review` + handoff con `verification_cmd` y exit codes (test 2x
-> 0) + release. ASCII puro. Es la iteracion 1 (tope 2).
