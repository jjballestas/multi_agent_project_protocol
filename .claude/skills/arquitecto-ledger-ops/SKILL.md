---
name: arquitecto-ledger-ops
description: >-
  Preflight checklist y recetas exactas para operaciones gobernadas del Arquitecto en
  multi_agent_project_protocol (este repo, escritor-unico VIVO). USAR ANTES de: cualquier
  runtime/submit_intent.py (task_upsert / task_status / claim / decision / mailbox_archive),
  antes de soltar un mensaje GO/REVIEW en Area_comun/mailbox/open/, antes de pedir review a un
  peer (Codex/Analista), y antes de commitear estado/ledger. Evita los fallos recurrentes:
  claim plano que pierde scope, mensajes no-ASCII, requires_response sin response_owner,
  pedir review sin commitear (HEAD rojo en clean clone), drift por apply a medias, y el
  footgun de stop-order que apaga los crons. Trigger words: submit_intent, GO, REVIEW, claim,
  task_upsert, task_status, mailbox, cerrar tarea, ledger, dataset, registrar tarea.
---

# Arquitecto — operaciones gobernadas del ledger (preflight)

Fuente de verdad: `AGENTS.md` (s.7), `personal/Arquitecto/STARTUP_PROMPT.md`, DECISION-0020/0022/0038/0040.
Este skill es el **checklist activo** de esas reglas. Si algo entra en conflicto, mandan esos docs.

## 0. Cold-start primero (no te saltes esto)
Antes de la primera escritura: lee `personal/Arquitecto/STARTUP_PROMPT.md` + `MEMORY.md`, mira
`git log --oneline -8` + `git status`, y `CLAIMS.json`. Escritor unico VIVO: **editar
`Area_comun/state/*.json` a mano = drift HARD-FAIL**. TODA transicion via `submit_intent --actor-id Arquitecto`.

## 1. Mensajes de mailbox (GO / REVIEW / cualquier MSG-*.md)
ANTES de escribir el archivo en `Area_comun/mailbox/open/`:
- **ASCII puro.** Nada de acentos, `—`, `→`, `≥`, `∧`, comillas tipograficas. Usa `->`, `>=`, `AND`, `-`.
- **`requires_response: true` EXIGE `response_owner: <destinatario>`** (y, para el validador clasico,
  `requested_action` y/o `question`). Sin `response_owner` -> `validate_collaboration_state.py` exit 1.
- **type que el cron del peer reconoce:** Codex acepta `GO/REQUEST/ACTION/HANDOFF/REVIEW/QUESTION/DECISION`;
  **Analista acepta `REVIEW/REQUEST/ACTION/QUESTION/DECISION` (NO "GO")**. O pon `requested_action` no vacio.
- **FOOTGUN stop-order (RESUELTO 2026-07-02 con el harness de TASK-0236):** el detector de corte ahora es
  IGUALDAD EXACTA: el cron solo se detiene si `requested_action.Trim()` (o `one_line_summary`) es EXACTAMENTE
  `STOP_JOB`. Ya puedes MENCIONAR "STOP_JOB"/stop/parada/para/kill libremente en el cuerpo/campos -> **ya NO hay
  footgun** con el harness desplegado. (Historico: el `-cmatch`/contains viejo auto-detenia el cron si una linea
  tenia una palabra-stop `(detener|deten|parar|para|stop)` junto a `(cron|monitor|<Peer>)`; asi "para Codex" o
  mencionar STOP_JOB tumbaban el cron. Si algun cron corre un harness pre-0236, vuelve a aplicar la regla vieja.)
- **GATEA TU PROPIO MENSAJE** antes de seguir: `python scripts/validate_collaboration_state.py` exit 0
  Y `python scripts/scan_encoding.py` exit 0. `scan_encoding` cubre `open/` Y `archived/`.

## 2. submit_intent — recetas que funcionan a la primera
- **Claim acquire: SIEMPRE anidado** bajo la clave `claim`, nunca plano (plano se materializa perdiendo
  `scope`, bug en `runtime/protocol_replay.py:821`):
  `{"type":"claim","op":"acquire","claim":{"claim_id":...,"owner":"Arquitecto","task_id":...,"status":"active","scope":[...],"started_at":ts,"updated_at":ts,"expires_at":...}}`
- **El `scope` del claim DEBE incluir su propia fila `CLAIMS.json#<claim_id>`** o no podras liberarlo
  (release exige scope sobre `CLAIMS.json#<claim_id>`).
- **Scope con FRAGMENTO, no archivo entero:** para `task_upsert`/`task_status` el scope necesita
  `Area_comun/state/TASK_INDEX.json#TASK-XXXX` y `Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-XXXX`
  (mas el `.md` de la tarea). `task_status` reescribe el `.md` -> incluye `Area_comun/tasks/TASK-XXXX-*.md`.
- **El `.md` de la tarea necesita frontmatter YAML con `status:`** y campo `file:` o el apply falla
  ("task file has no status field"). Crea el `.md` ANTES del claim (artifacts-before-claim, DECISION-0020 #1).
- **Secuenciar en submits separados** (acquire -> upsert -> release) es mas robusto que un solo `--intents`
  cuando hay dependencia claim->write; si usas `--intents`, valida el ordenamiento.
- **`--actor-id Arquitecto`, `--timestamp` UTC real, `--commit $(git rev-parse HEAD)`** en cada llamada.

### 2b. Lecciones 2026-07-03 (fallos reales, no repetir)
- **TODO `task_status` exige claim ACTIVO del actor** que cubra `TASK_INDEX.json#<id>` +
  `PROJECT_STATE.json#active_tasks/<id>` + el `.md` de la tarea -- tambien las RATIFICACIONES
  (in_review->review_approved). Sin claim: "ERROR: no active claim for actor covers this intent".
  Patron: tx atomica claim-acquire -> task_status(s) -> claim-release.
- **`in_progress->in_review` exige capability `implementer`** para type docs/build (solo
  analysis/triage/extraction son owner-closeable, DECISION-0032/0060). Tareas docs propias del
  Arquitecto: el flip a in_review lo ejecuta CODEX via ACTION (igual que los done-flips).
- **El archivo `--intents` es un OBJETO** `{"idempotency_key": "...", "intents": [...]}`, NO un
  array plano ("ERROR: transaction JSON must be an object").
- **Intent `decision`** = `{"type":"decision","decision_id":"DECISION-XXXX"}` con el `.md` de la
  decision YA creado (artifacts-before-claim) y claim que incluya `Area_comun/state/PROJECT_STATE.json`
  (ruta FULL, no fragmento) + el `.md` de la decision.
- **Clean clone en Windows:** `git clone -c core.longpaths=true` o el checkout muere por MAX_PATH
  ("Filename too long") y validate da 128 sin ser un fallo real del ledger.
- **`task_upsert` modifica PROJECT_STATE ADEMAS de TASK_INDEX** (2026-07-03, drift real): al commitear un
  registro de tarea, stagea SIEMPRE `Area_comun/state/PROJECT_STATE.json` + `.slim.json` junto con
  `TASK_INDEX.json` + `.slim.json` + events + snapshot. Omitir PROJECT_STATE deja el working tree con drift:
  validate LIVE verde (el tree tiene los cambios) pero HEAD en CLON LIMPIO rojo -> el Analista pre-gatea en
  clon limpio y ABORTA la review (silent-refusal legitimo). Verifica `git status Area_comun/state/` LIMPIO
  antes de pedir review. Fix si ya paso: commitea PROJECT_STATE + des-seen la review del Analista.
- **NO uses subject `fix(`/`revert(`/`hotfix(` en commits gobernados** salvo que incluyas `Fixes-Task:` (el
  gate de trailers lo exige; me mordio 2x). Usa `chore(`/`state(`/`coord(`/`tasks(` para correcciones que no
  son remediacion de una tarea concreta. Ver s.2c.

### 2c. Gate de trailers ACTIVO (desde 2026-07-03, COMMIT_TRAILERS.json) -- muerde al Arquitecto
Con el gate activo, TODO commit que toque rutas gobernadas (Area_comun/**, runtime/state/**) DEBE:
- Llevar `Task-Id: TASK-XXXX` (o `Task-Id: none` + `Ops-Reason: <motivo>` para coordinacion sin tarea)
  en la SECCION FINAL de trailers. **`Task-Id:` y `Co-Authored-By:` van en el MISMO parrafo final,
  sin blank line entre ellos** -- un salto de linea deja el Task-Id fuera del bloque de trailers que el
  parser lee (F-0240-01) -> "touches governed routes without exact Task-Id trailer".
- Si el subject empieza con `fix(`/`revert(`/`hotfix(` (FIX_SUBJECT_PATTERN), EXIGE ADEMAS
  `Fixes-Task: TASK-XXXX` -> si no, "is fix/revert/hotfix without exact Fixes-Task trailer". Para evitarlo
  en commits que no corrigen una tarea, usa subject `chore(`/`coord(`/`tasks(` en vez de `fix(`.
- **GATEA EL PUSH en validate POST-commit** (no solo pre-commit): un commit con trailer malo se crea igual;
  corre `validate` DESPUES del commit y antes del push. Si sale rojo, el commit ya existe -> corrige en un
  commit nuevo (o, si es teething del gate recien activado, avanza `start_commit` de COMMIT_TRAILERS.json
  al commit ofensor -- rev-list start..HEAD lo excluye -- documentando el motivo; NO reescribas historia
  pusheada).
- El gate se activa creando `Area_comun/protocol/COMMIT_TRAILERS.json` {enabled:true, start_commit:<sha>}
  (fuera del config pineado). Solo tras relanzar los harnesses de peers con prompts que emiten trailers
  (F-2 anti-DoS) y verificar 1 commit de peer con trailer.

### 2d. Intake DoR, claim de higiene, y validacion de override (2026-07-12, fallos reales)
- **`task_upsert` de REGISTRO admite intake PARCIAL; promover `proposed->ready` EXIGE el intake DoR COMPLETO**
  (8 campos: `type`, `goal`, `acceptance`, `verification_cmd`, `scope_routes`, `out_of_scope`, `risk`, `estimate`
  -- validador `scripts/validate_collaboration_state.py:460`, `submit_intent.py:255`). Si registras una tarea con
  intake parcial y luego la promueves, falla "task ... intake field invalid or empty: <campo>". Completa el intake
  en el `.md` ANTES de promover (el gate lee el `.md`, no el index).
- **El claim de `mailbox_archive`/higiene EXIGE `task_id`** (no es task-less): usa un id de ops como
  `OPS-MAILBOX-HYGIENE-<fecha>` (convencion vista en los archives previos). Sin `task_id` -> "claim acquire
  requires task_id".
- **Validar un OVERRIDE (`event-state.runtime.json`): chequea la GUARDA DE CLAVES PERMITIDAS**, no solo la
  resolucion de rutas. `event_state` del override solo admite `actor_auth_enforce` / `actor_auth_config` /
  `event_auth` (`runtime/eventlog.py:263`); CUALQUIER otra clave (p.ej. `anchor_enabled`) = "unsupported
  event_state keys" -> validate RECHAZA. El "anchor canonico-solo" es OPERACIONAL (solo el clon canonico corre el
  anchor), NO una clave del override. Un override "estructuralmente ok" con una clave extra FALLA validate --
  corre `validate` en un clon fresco antes de declararlo valido.

## 3. Recuperacion de drift (apply a medias)
Si un apply falla a mitad (p.ej. error en el `.md`) la slim puede quedar desincronizada:
`python -c "from pathlib import Path; from runtime.protocol_replay import materialize_from_event_log_if_enabled; materialize_from_event_log_if_enabled(Path('.'))"`
re-materializa el estado desde los eventos (NO toca genesis). Verifica drift 0 antes de reintentar.
- **REGENERAR EL SNAPSHOT tambien (2026-07-07, verificado 2x): re-materializar reconstruye los JSON de estado
  (CLAIMS/TASK_INDEX/PROJECT_STATE) pero NO actualiza `runtime/state/snapshot.json` -> `up_to_seq` queda
  desfasado del head del log y `validate` sale rojo con "snapshot mismatch: up_to_seq differs". Tras
  re-materializar, SIEMPRE regenera el snapshot:**
  `python -c "import sys; sys.path.insert(0,'.'); from pathlib import Path; from runtime.eventlog import rebuild_snapshot, write_snapshot; snap=rebuild_snapshot(Path('.')); write_snapshot(Path('.'), snap)"`
  y recien ahi valida (val=0). Aplica igual en el timeout de submit_intent a mitad de tx (s.6).
- **`scan_encoding` rojo TRANSITORIO por `runtime/memory/index.db`:** si corre un build de memdb (indexador
  SQLite) y deja `index.db` (gitignored) a mitad del scan, el scan lo intenta abrir como texto y da rojo/
  FileNotFoundError. No es un fallo real: `rm -f runtime/memory/index.db` y re-scan.

## 4. Pedir review / cerrar (maker != checker)
- **COMMITEA el saneamiento ANTES de pedir review.** El peer valida con **clean clone de HEAD**; si tus
  correcciones estan solo en el working tree, HEAD sale rojo y el peer bloquea (con razon).
- Stage EXPLICITO por path (nunca `git add -A`: barre `personal/`). Snapshot consistente, gates verdes por
  **exit code** (no por grep: `grep ERROR` da exit 0 al matchear y NO frena).
- Verifica el arbol commiteado: `git ls-tree HEAD <ruta>`, `git show HEAD:<msg>` tiene `response_owner`, etc.
- Cierre en dos partes: Codex `in_progress->in_review`; Arquitecto ratifica `in_review->review_approved` (checker).
  **El flip final `review_approved->done` exige capability `implementer` -> lo hace CODEX, NO el Arquitecto**
  (submit_intent con actor Arquitecto sobre un `task_status ...->done` es rechazado: "lacks capability implementer").
  Por eso el Arquitecto rutea un ACTION done-flip a Codex tras ratificar; no intenta cerrarlo el mismo.
- **CUALQUIER `->done` exige implementer = Codex, sea cual sea el owner/type de la tarea (leccion 2026-07-02):** al
  cerrar tareas type `review` propias del Analista (p.ej. cierre de reviews huerfanas), NI el Analista (type review
  no esta en el set owner-closeable de submit_intent.py: solo `analysis/triage/extraction` cierran por owner) NI el
  Arquitecto (sin implementer) pueden flip `ready->done` -> ambos reciben rechazo. Cadena correcta: el Analista
  CONFIRMA el cierre (mailbox), el Arquitecto lo ratifica, y **Codex ejecuta el `->done`** (unico con implementer).
  El Arquitecto SI puede `->cancelled` (probado), pero NO `->done`. Si necesitas cerrar reviews a done, rutea ACTION
  done-flip a Codex citando la confirmacion del Analista.
- **Tras CADA commit: actualiza memoria (DECISION-0026) + push si verde.**

## 5. Re-disparar un cron sobre un mensaje ya "seen"
El cron marca cada MSG con firma `nombre|longitud|mtime`. Para que reprocese: cambia la longitud del MSG, o
borra su entrada en `.protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.seen.json` (limpio, sin tocar git).

### 5b. El Analista ABORTA+marca-seen si el canonico esta ROJO (leccion 2026-07-02)
El harness del Analista **pre-gatea en validate VERDE** antes de ejecutar una review: si el canonico esta rojo
(p.ej. un peer a medio entregar -> `TASK-XXXX status mismatch index vs file` + `Handoff-release violation: owner
sigue con claim activo`), **ABORTA la review Y marca el MSG como seen** -> NO reintenta solo, y el trabajo queda
silenciosamente sin hacer (visto con el relay del pivote mientras Codex entregaba 0229). REGLAS: (1) **rutea reviews
al Analista SOLO con el ledger VERDE** (`validate_collaboration_state.py` exit 0), no durante una entrega de peer a
medias; (2) si aborto por rojo, cuando el canonico vuelva verde **des-seen** su entrada en el `seen.json` para que
reintente; (3) su reporte de aborto ("que Arquitecto/Codex deje el canonico verde y libere/cierre TASK-XXXX") es la
senal -> destraba el ledger (espera el commit del peer o cierra tu la transicion) y luego des-seen.

## 6. `submit_intent` timeoutea a mitad de transaccion (2026-07-06, real, 3 episodios en una sesion)
Bajo contencion/carga (peers escribiendo el mismo `events.jsonl` casi simultaneamente), `submit_intent.py`
puede timeoutear (30-100s) DESPUES de haber escrito uno o mas eventos `intent.applied` al log pero ANTES de
completar TODOS los intents de la transaccion o sus EFECTOS DE ARCHIVO. Dos sintomas distintos:
- **Falta un intent de la transaccion (tipicamente el `claim release` final):** `tail events.jsonl` muestra
  los primeros N-1 intents aplicados pero no el ultimo. Fix: reenvia SOLO el intent faltante como
  `--intent` standalone (no la transaccion completa -- reenviarla entera fallaria porque los primeros
  intents ya se aplicaron, p.ej. "claim already active").
- **El evento SI aplico pero el EFECTO DE ARCHIVO no ocurrio:** especifico de `mailbox_archive`. La logica
  que mueve fisicamente el `.md` de `open/` a `archived/` (`apply_mailbox_side_effects` en
  `submit_intent.py`) corre SOLO en el momento del submit original -- `materialize_from_event_log_if_
  enabled()` (la funcion de re-materializacion) SOLO reconstruye los JSON de estado (CLAIMS/TASK_INDEX/
  PROJECT_STATE), NO re-ejecuta efectos de archivo. Si el proceso muere despues de escribir el evento
  `mailbox_archive` pero antes de mover el archivo, el ledger dice "archivado" y el disco dice "sigue en
  open/" -- drift silencioso. Fix: mueve el archivo A MANO replicando la logica exacta (actualizar
  `status: open` -> `status: archived` en el frontmatter del `.md`, luego mover el archivo de
  `Area_comun/mailbox/open/` a `Area_comun/mailbox/archived/`) -- NUNCA reenvies el intent (fallaria con
  "message not found in open" porque el evento ya dice archivado).
- **Diagnostico generico:** tras cualquier timeout de `submit_intent`, SIEMPRE (1) `tail -N events.jsonl`
  comparando los `intent_count` esperados de la transaccion contra los que realmente aparecen; (2)
  re-materializar state (s.3 de este skill); (3) verificar el estado FISICO real (mailbox, claims activos)
  contra lo que el log dice; (4) reenviar SOLO lo que falta.
- **Causa raiz del timeout AUN no diagnosticada con certeza** (el lock `.ledger.lock` se probo LIBRE con un
  probe manual `msvcrt.locking(LK_NBLCK)` durante uno de los hangs -- no es el lock file el que bloquea).
  Candidato mas probable: I/O lento bajo escritura concurrente del arbol compartido. Mitigacion que
  funciono: reintentar con timeout MUY generoso (90-100s) en vez de asumir deadlock indefinido.

## 7. Cuando el CLASIFICADOR DE PERMISOS del harness bloquea una accion (2026-07-06, nuevo)
El auto-mode classifier del harness puede bloquear una accion tuya que consideras legitima por precedente
ya establecido (p.ej. avanzar `start_commit` de `COMMIT_TRAILERS.json` por un commit de un peer/asesor sin
trailer -- mecanismo documentado y usado repetidamente en este mismo skill/archivo) o por ser claramente
necesaria para la tarea (p.ej. verificar llaves/firmantes de OTRA instancia como parte de un corte de
gobernanza pedido explicitamente por el operador). **La respuesta correcta es SIEMPRE parar y pedir
autorizacion explicita** (via `AskUserQuestion` en sesion interactiva, o via mailbox si es asincrono) --
**NUNCA buscar un comando alternativo que logre lo mismo sin el permiso** (el classifier puede no tener el
contexto completo del precedente/historia; tu trabajo es darle ese contexto al operador para que decida,
no rodear el bloqueo). Si el operador confirma, procede con la MISMA accion que fue bloqueada (no una
alternativa "creativa"); si no confirma, deja la accion pendiente y sigue con el resto de la cola.

## Checklist de una linea (pega mentalmente antes de actuar)
ASCII? · response_owner? · type valido para el peer? · sin "para"+peer? · claim anidado + scope#self + fragmentos? ·
.md con status/file? · validate+encoding exit 0? · committeado antes de pedir review? · gateado por exit-code? ·
si el classifier bloquea, pido permiso -- no rodeo?
