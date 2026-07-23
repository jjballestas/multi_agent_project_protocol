# Veredicto Analista - TASK-0291 (R3) + TASK-0292 (R4)

- Voz: Analista (checker independiente; NO maker, NO orquestador). Firma: Analista.
- Encargo: `Area_comun/mailbox/open/MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0291-0292.md`.
- Fecha/hora local del juicio: 2026-07-24 00:09 (UTC+2).
- Alcance declarado por el encargo: SOLO PROTOCOLO (hub). SIN producto (Nova-Budget/Zeus) en alcance.

## Ancla canonica

- `origin/main` = `a3d7b91` (verificado con `git rev-parse origin/main`).
- Commits de implementacion bajo juicio, ambos ANCESTROS de `a3d7b91`:
  - `23d7476` fix(TASK-0291,0292): align full hook with validator deliverable policy (R3 + R4).
  - `dd9602a` fix(TASK-0291,0292): stabilize non-reviewed hook fixture (remediacion iter1).
- El encargo citaba `b0425d6` como HEAD; en el momento del juicio `origin/main` ya avanzo a `a3d7b91`
  (commit de coordinacion del propio REVIEW). Anclo en `a3d7b91` porque contiene ambos commits de
  implementacion sin cambios posteriores sobre `.githooks/pre-commit` ni sobre el runner
  (`git diff --name-only b0425d6 a3d7b91` no toca ninguno de los dos).
- CLON LIMPIO de juicio: `/d/ccv0291` (clone --no-hardlinks + `git checkout a3d7b91`), arbol limpio.
- Sandboxes de prueba: `/d/pr0291` y `/d/pr0291old` (clones del clon limpio). NINGUNA prueba se corrio
  in-place sobre el arbol de trabajo del repo.

## Gates de protocolo (clon limpio, por exit code)

| Gate | Comando | Exit |
|------|---------|------|
| Estado colaborativo | `python scripts/validate_collaboration_state.py` | 0 |
| Encoding | `python scripts/scan_encoding.py` | 0 |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | 0 |
| Full-hook arbol limpio | `HOOK_FULL=1 sh .githooks/pre-commit` | 0 (`OK: collaboration state is valid.`) |
| Regresion (corrida 1) | `python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py` | 0 |
| Regresion (corrida 2) | idem, inmediatamente despues | 0 |
| Pin CI | `sha256sum .githooks/pre-commit` vs `.github/workflows/validate.yml` | `bd89ec302961d6db9c22a214710776986199ede11c8f7fdae2f11bc5c4b98e84` = MATCH |

Nota: el hook emite `PRUNE DUE: released_ratio 91.3 >= 90` como WARNING (no altera el exit code).
Es deuda de poda del Arquitecto, ajena a este batch; la senalo, no la toco.

## Auditoria estructural del cambio (no confianza, diff real)

- `.githooks/pre-commit`: diff contra `23d7476^` = EXACTAMENTE +3 lineas (2 de comentario + la guarda
  `git ls-files --error-unmatch -- "$path" >/dev/null 2>&1 || continue`). Nada mas cambio en el hook.
  SHA-256 previo `66e7f3814de529e8234d745cd3e639f3cfe0432aaa9858fbd4c6a275ef76f4ed`, actual
  `bd89ec302961d6db9c22a214710776986199ede11c8f7fdae2f11bc5c4b98e84` (coincide con el pin de CI).
- `git diff --stat 23d7476^ a3d7b91 -- scripts/ runtime/protocol_replay.py runtime/submit_intent.py
  protocol.config.json` -> VACIO. El validador NO fue tocado; el fondo intocable (config pineado,
  epoch) NO fue tocado.
- Autoridad efectiva del validador: `validate_collaboration_state.py:1048` exige existencia de
  deliverables solo para `REVIEWED_TASK_STATUSES` = {in_review, review_approved, qa_pending,
  architect_review, done} (linea 38). La guarda de la opcion B se dispara exactamente en la condicion
  "path ausente del index", que es la misma condicion en la que `git checkout-index` fallaba: la
  guarda no puede saltarse un path que SI se puede materializar.

## Refutacion que intente y FRACASO (la mas peligrosa)

Hipotesis de punto ciego: si la opcion B delega en el validador, y el validador solo juzga el indice
CALIENTE, entonces una tarea REVISADA ya ARCHIVADA con deliverable ausente pasaria a ser aceptada
(regresion silenciosa de C5 por el lado del archivo).

Refutada: `main()` (lineas ~1457-1480) hace `merge_by_array_field(index_hot, index_archive, "tasks",
"id", ...)` y pasa el indice FUSIONADO a `validate_tasks`. El validador cubre hot + archive. Ademas la
masking-probe del runner ataca `personal/Codex/STARTUP_PROMPT.md`, que es deliverable de `TASK-0084`
(status `done`, en `TASK_INDEX_ARCHIVE.json`): la prueba ya ejercita el camino del ARCHIVO, no solo el
caliente. Punto ciego inexistente.

## Vector por vector (pruebas propias, entrypoint REAL del hook, por exit code)

Metodo: sandbox = clon del clon limpio. Inyecto una tarea SINTETICA `TASK-9999` (fila en
`TASK_INDEX.json` + su `.md`) con `deliverables: ["personal/Codex/absent-analista-probe.md"]` (ausente
del index), apago `event_state` para no colisionar con el drift, hago `git add` explicito y corro
`HOOK_FULL=1 HOOK_SNAPSHOT_MODE=partial sh .githooks/pre-commit`. NO me fie del nombre de ningun test:
recorri la FAMILIA COMPLETA de estados, no solo el ejemplo dado.

### V1 - R3: familia NO-revisada completa (6/6) -> el hook ya NO rechaza en falso

| status | exit | `deliverable missing` | frontera validador | `could not materialize` | veredicto |
|--------|------|----------------------|--------------------|--------------------------|-----------|
| proposed | 0 | no | no | no | PASS |
| ready | 0 | no | no | no | PASS |
| claimed | 0 | no | no | no | PASS |
| in_progress | 0 | no | no | no | PASS |
| blocked | 0 | no | no | no | PASS |
| cancelled | 0 | no | no | no | PASS |

El acceptance de TASK-0291 se cumple para TODA la familia que el validador tolera, no solo para el
`ready` que usa el fixture del maker.

### V2 - C5 / R4: familia REVISADA completa (5/5) -> sigue rechazando, y por la RAZON del validador

| status | exit | `deliverable missing` | `collaboration state ... invalid` | `could not materialize` | veredicto |
|--------|------|------|------|------|-----------|
| in_review | 1 | SI | SI | no | PASS |
| review_approved | 1 | SI | SI | no | PASS |
| qa_pending | 1 | SI | SI | no | PASS |
| architect_review | 1 | SI | SI | no | PASS |
| done | 1 | SI | SI | no | PASS |

C5 INTACTA y ademas migrada al camino correcto: el rechazo ya no viene de `checkout-index` sino del
boundary del validador, que es exactamente lo que TASK-0292 exige asegurar.

### V3 - Falsabilidad: el assert de R4 y la tolerancia de R3 tienen DIENTES

Restaure el hook PRE-R3 (`23d7476^`, sha `66e7f38...`) en un sandbox y corri los MISMOS probes:

| status | hook | exit | razon observada |
|--------|------|------|-----------------|
| ready | PRE-R3 | 1 | `is not in the cache` / `could not materialize staged snapshot` |
| cancelled | PRE-R3 | 1 | idem |
| done | PRE-R3 | 1 | idem -- NO `deliverable missing`, NO frontera del validador |

Conclusion dura: (a) el falso-rechazo de tareas no-revisadas era REAL y el +3 del hook es su causa de
cierre; (b) el assert de razon de TASK-0292 NO habria pasado antes de R3 (pre-R3 el rechazo era por
`checkout-index`), luego no es un assert decorativo: distingue el mundo viejo del nuevo.

### V4 - Caza de escapes nuevos (4 vectores propios)

| id | escenario | exit | resultado |
|----|-----------|------|-----------|
| E1 | tarea REVISADA (`done`), deliverable EXISTE sin trackear en el arbol pero NO staged | 1 | rechaza con `deliverable missing` + frontera validador -- no hay enmascaramiento |
| E2 | idem con ruta `personal/./Codex/...` (intento de alias de ruta) | 1 | rechaza igual; el extractor normaliza y el validador muerde |
| E3 | estado gobernado roto staged (`TASK_INDEX.json` = `{`) | 1 | rechaza en la frontera del validador |
| E4 | tarea REVISADA con su deliverable staged como fichero NUEVO | 0 | ACEPTA -- no hay falso-rechazo por el lado positivo |

NO encontre ningun escape nuevo. La guarda de la opcion B solo puede saltar paths que el validador
juzga despues, y para tareas revisadas ese juicio es fail-closed en los 5 estados.

### V5 - Determinismo del fixture sintetico

- `run_hook_fullmode_inventory_cases.py` corrido 2 veces seguidas en el clon limpio -> exit 0 y exit 0,
  CON `TASK-0291` y `TASK-0292` ya en `in_review` (justo el estado que rompia la 1a entrega).
- `grep "TASK-0[0-9][0-9][0-9]"` sobre el runner -> unica coincidencia es el docstring
  (`"""Exercise TASK-0287 ..."""`). El fixture non-reviewed NO referencia ninguna tarea viva.
- El id sintetico se deriva por busqueda descendente `TASK-9999..TASK-9000` sobre ids EXISTENTES, y la
  tarea se crea clone-local (fila + `.md` + `git add`), por lo que es robusto a que 0291/0292 pasen a
  `done` y luego a archivo.

## Residuales declarados (NINGUNO bloqueante)

- **RES-1 (robustez del id sintetico).** `existing_task_ids` se construye SOLO con
  `TASK_INDEX.json` (caliente); ignora `TASK_INDEX_ARCHIVE.json`. Hoy no existe ningun `TASK-9xxx` en
  el archivo (lo verifique), y si algun dia lo hubiera, `merge_by_array_field` lo cazaria como
  `Duplicate task across hot/archive` -> CI ROJO, no verde falso. Sugerencia (no bloqueante): derivar
  el id sobre `hot union archive`.
- **RES-2 (precision del assert de R4).** La masking-probe exige las dos subcadenas en el output
  global, sin ligarlas al path enmascarado. Sobre una linea base verde el unico deliverable ausente es
  el inducido, asi que hoy es solido; si en el futuro coexistiera otro deliverable ausente, el assert
  podria satisfacerse sin que el enmascaramiento concreto se haya cazado. Sugerencia: asertar
  `deliverable missing: personal/Codex/STARTUP_PROMPT.md`.
- **RES-3 (preexistente al batch).** El caso positivo asegura `selected != 1 -> AssertionError`: es un
  conteo exacto acoplado al contenido vivo de los indices. Cualquier tarea futura que declare un
  deliverable `personal/` pone el CI en rojo. Ya estaba en `23d7476^` (linea 70); falla en ALTO, no en
  falso-verde. Lo dejo anotado, no lo imputo a este batch.
- **RES-4 (acoplamiento vivo residual de la masking-probe).** Sigue dependiendo de que
  `personal/Codex/STARTUP_PROMPT.md` sea deliverable de una tarea revisada (`TASK-0084`, archivada).
  Es la misma familia del defecto que el Arquitecto cazo en iter1, pero degrada en ALTO
  (`returncode == 0` -> AssertionError), no en silencio.
- **OBS (ajeno al batch).** Poda vencida (`released_ratio 91.3 >= 90`) senalada por el hook como
  WARNING. Es del Arquitecto; no la toco (DECISION-0018: la senalo).

## Recomendacion de cierre

- **TASK-0291 (R3): OK-CLOSABLE (GO).** Cierra el falso-rechazo en los 6 estados no-revisados, sin
  regresion F1 (arbol limpio exit 0), sin tocar el validador, con C5 intacta en los 5 estados
  revisados y sin escape nuevo en 4 vectores adversariales.
- **TASK-0292 (R4): OK-CLOSABLE (GO).** El assert de razon es falsable (no habria pasado pre-R3),
  el rechazo se atribuye al boundary del validador en los 5 estados revisados, y el runner es
  determinista (2/2 exit 0) con el fixture non-reviewed ya sintetico y desacoplado de tarea viva.

El cierre (flip de estado, release de claims, archivo del canal) es del Arquitecto: yo no promuevo,
no cierro y no ratifico mi propio veredicto.

---
Analista
