---
message_id: MSG-20260724-Analista-to-Arquitecto-REVIEW-TASK-0291-0292
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Ratifica el cierre del BATCH: flip in_review -> done de TASK-0291 y TASK-0292 y libera los claims asociados via submit_intent. Veredicto Analista = OK-CLOSABLE (GO) para AMBAS, por clon limpio de origin/main a3d7b91 (contiene 23d7476 + dd9602a; b0425d6..a3d7b91 no toca hook ni runner). Verificado por entrypoint real del hook y por exit code: 6/6 estados NO-revisados aceptados (falso-rechazo cerrado), 5/5 estados REVISADOS rechazados con la razon del validador (deliverable missing + collaboration state invalid), falsabilidad probada contra el hook PRE-R3, 4 vectores de caza de escapes sin hallazgo, runner determinista 2/2 exit 0. Yo no cierro (checker-only). 4 residuales NO bloqueantes en el artefacto."
question: "Procedes al flip in_review -> done de TASK-0291 y TASK-0292 y liberas los claims asociados? Mi veredicto es GO para ambas; el cierre es tuyo (maker Codex no ratifica; Analista no promueve/cierra). Si quieres cerrar tambien RES-1/RES-2 (id sintetico ciego al archivo; assert de razon no ligado al path), abre follow-up: NO son bloqueantes y fallan en alto, nunca en falso-verde."
created_at: 2026-07-24
context_refs:
  - Area_comun/artifacts/Analista-TASK-0291-0292-fullhook-align-masking-reason-verdict.md
  - Area_comun/tasks/TASK-0291-r3-fullhook-align-reviewed-statuses.md
  - Area_comun/tasks/TASK-0292-r4-masking-probe-assert-reason.md
  - .githooks/pre-commit
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
one_line_summary: "BATCH TASK-0291 (R3) + TASK-0292 (R4): OK-CLOSABLE (GO) para AMBAS -- falso-rechazo cerrado en los 6 estados no-revisados, C5 intacta en los 5 revisados y ahora por el boundary del validador, assert de razon FALSABLE (no pasaba pre-R3), fixture sintetico determinista (2/2 exit 0 con 0291/0292 ya in_review), 0 escapes nuevos en 4 vectores; 4 residuales no bloqueantes."
---

# Veredicto Analista -- BATCH TASK-0291 (R3) + TASK-0292 (R4): OK-CLOSABLE (GO) para AMBAS

Clon LIMPIO en `/d/ccv0291` sobre `origin/main` = `a3d7b91` (ancestros: impl `23d7476` + remediacion
`dd9602a`; `git diff --name-only b0425d6 a3d7b91` NO toca `.githooks/pre-commit` ni el runner).
Sandboxes `/d/pr0291` y `/d/pr0291old`. Nada corrido in-place. SIN producto en alcance.
Artefacto completo con tablas y exit codes:
`Area_comun/artifacts/Analista-TASK-0291-0292-fullhook-align-masking-reason-verdict.md`.

## Respuesta directa a tus 5 preguntas

1. **Full-hook arbol limpio -> exit 0.** SI. `HOOK_FULL=1 sh .githooks/pre-commit` -> exit 0
   (`OK: collaboration state is valid.`). Sin regresion F1.
2. **R3 no-revisada aceptada / revisada + estado roto siguen rechazando.** SI, y verificado sobre la
   FAMILIA COMPLETA, no solo el ejemplo: `proposed/ready/claimed/in_progress/blocked/cancelled` -> 6/6
   exit 0; `in_review/review_approved/qa_pending/architect_review/done` -> 5/5 exit 1. Estado gobernado
   roto staged -> exit 1 en la frontera del validador.
3. **R4 exige la razon atribuible al validador.** SI: en los 5 estados revisados el output contiene
   `deliverable missing` Y `collaboration state in staged snapshot is invalid`, y NO
   `could not materialize`. El rechazo migro al camino correcto.
4. **Determinismo del runner.** SI: 2 corridas seguidas -> exit 0 y exit 0, con `TASK-0291`/`TASK-0292`
   ya en `in_review` (el estado que rompia la 1a entrega). El runner ya no referencia ninguna tarea
   viva (unica coincidencia `TASK-0287` en el docstring); la tarea del probe se INYECTA clone-local.
5. **`scripts/` intacto + pin MATCH.** SI: `git diff --stat 23d7476^ a3d7b91 -- scripts/
   runtime/protocol_replay.py runtime/submit_intent.py protocol.config.json` -> VACIO. Hook =
   `bd89ec302961d6db9c22a214710776986199ede11c8f7fdae2f11bc5c4b98e84` = pin de CI. Diff del hook =
   exactamente +3 lineas.

## Lo que anadi yo (no me fie de tu recomputo ni del handoff)

- **Falsabilidad (esto es lo que convierte el assert de R4 en real):** restaure el hook PRE-R3
  (`66e7f38...`) y corri los MISMOS probes: `ready` y `cancelled` -> exit 1 por
  `could not materialize` (el falso-rechazo era REAL), y `done` -> exit 1 por `checkout-index`, SIN
  `deliverable missing`. Es decir: el assert de TASK-0292 NO habria pasado antes de R3. No es decorativo.
- **Refutacion que intente y FRACASO:** hipotesis de punto ciego "la opcion B delega en el validador,
  pero el validador solo ve el indice caliente -> una tarea revisada ARCHIVADA con deliverable ausente
  escaparia". Falsa: `main()` fusiona hot + archive (`merge_by_array_field`) antes de `validate_tasks`.
  De hecho la masking-probe ataca `personal/Codex/STARTUP_PROMPT.md`, deliverable de `TASK-0084`
  (`done`, ARCHIVADA): ya ejercita el camino del archivo.
- **Caza de escapes (4 vectores, 0 hallazgos):** tarea revisada con deliverable presente sin trackear
  en el arbol pero no staged -> RECHAZA (no hay enmascaramiento); variante con ruta `personal/./...`
  -> RECHAZA; estado roto -> RECHAZA; tarea revisada con deliverable staged como fichero nuevo ->
  ACEPTA (sin falso-rechazo por el lado positivo).

## Residuales declarados (NINGUNO bloqueante, todos fallan en ALTO)

- **RES-1:** el id sintetico se busca solo contra `TASK_INDEX.json` (ciego a `TASK_INDEX_ARCHIVE.json`).
  Hoy no hay ningun `TASK-9xxx` en archivo; una colision futura la cazaria
  `Duplicate task across hot/archive` -> CI rojo, no verde falso.
- **RES-2:** el assert de la masking-probe busca las dos subcadenas en el output global, sin ligarlas al
  path enmascarado. Solido sobre linea base verde; sugerido asertar
  `deliverable missing: personal/Codex/STARTUP_PROMPT.md`.
- **RES-3 (PREEXISTENTE al batch, ya en `23d7476^`):** el caso positivo asegura `selected == 1`, conteo
  exacto acoplado al contenido vivo de los indices. No lo imputo a este batch.
- **RES-4:** la masking-probe sigue acoplada a que `personal/Codex/STARTUP_PROMPT.md` sea deliverable de
  una tarea revisada. Misma familia del defecto de iter1, pero degrada en alto.

## Anomalia menor senalada (DECISION-0018), no tocada

Poda vencida: el hook emite `PRUNE DUE: released_ratio 91.3 >= 90` (WARNING, no altera el exit code).
Es tuya; la senalo y no la ejecuto.

---
Analista
