---
name: mailbox-hygiene
description: >-
  Como todos los agentes (Arquitecto/Codex/Analista) mantienen limpio el canal Area_comun/mailbox Y el
  estado protocolar: escribir mensajes bien formados, NO dejar mensajes resueltos en open/, archivar los
  consumidos de forma gobernada, Y correr la PODA (protocol_prune / prune_state.py) cuando este vencida.
  USAR al: ENTREGAR UN REPORTE/HANDOFF AL OPERADOR (regla dura 2026-07-04, reforzada 2026-07-05: cada
  reporte = checkpoint de higiene, ACOPLADO al mismo gate de commit, no un paso aparte que se olvida bajo
  carga), escribir un GO/REVIEW/FYI/HANDOFF, cerrar una tarea, responder un mensaje, o cuando open/ acumula
  mensajes ya respondidos/entregados/superados. Reglas duras: ASCII puro; requires_response exige
  response_owner; claim de mailbox SOLO file-scoped a MSG-*.md (nunca dir-level); archivar (mailbox_archive)
  exige capability orchestrator (solo el Arquitecto); los peers senalan mensajes stale via DECISION-0018, no
  los tocan; la poda (`prune_state.py --check`) se corre en el MISMO checkpoint, no aparte. Complementa
  arquitecto-ledger-ops y arquitecto-cron-lifecycle. Trigger words: mailbox, higienizar, higiene, archivar,
  mailbox_archive, MSG, open, archived, mensaje resuelto, consumido, stale, huerfano, response_owner, ASCII,
  canal limpio, GO consumido, poda, prune, protocol_prune, prune_state.
---

# Mailbox hygiene -- canal limpio para todos los agentes

> Objetivo: en `Area_comun/mailbox/open/` SOLO viven mensajes **vivos y accionables**. Todo lo respondido,
> consumido o superado se **archiva** (open -> archived). Un `open/` lleno de mensajes muertos confunde el
> cold-start, re-dispara crons y esconde lo accionable. Minimal narration (DECISION-0038): no narres el proceso.

## 0. Quien puede que
- **Todos los agentes:** escriben mensajes bien formados y **gatean** su propio mensaje antes de soltarlo.
- **Solo el Arquitecto (capability `orchestrator`):** ejecuta `mailbox_archive` (mover open->archived).
  Codex/Analista **no pueden archivar** (submit_intent lo rechaza: "lacks required capability: orchestrator").
- **Los peers (Codex/Analista):** si ven un mensaje stale/huerfano lo **senalan** al owner (DECISION-0018);
  no lo arreglan bajo claim ajeno ni lo dejan sin senalar.

## 0-quater. Poda coordinada en el checkpoint (clausula NORMATIVA -- DECISION-0120)

> Revision: 2026-08-18 (DECISION-0120, firmada por el operador humano en persona).
> Antes de esta fecha esta seccion NO EXISTIA en la copia viva: el 16-ago se borro la clausula
> ratificada de TASK-0273 **sin decision previa**, que CLAUDE.md regla 2 exige. La 0120 regulariza
> ese incumplimiento y reformula el paso 2 en vez de derogarlo.

La norma vive en `Area_comun/protocol/TASK_PROTOCOL.md`, seccion *Coordinated Pruning Checkpoint*.
**Esta skill no la sustituye: la operacionaliza.** Lo vinculante:

- solo el Arquitecto corre `--apply`, dentro del checkpoint de higiene;
- **precondiciones (paso 1, intactas y correctas):** arbol gobernado limpio y CERO claims de peer,
  comprobados como pasos de solo-lectura SEPARADOS antes del apply;
- **paso 2, reformulado por la 0120:** si falla una precondicion **no se espera la ventana: se
  abre.** El coordinador deja de rutear; un peon solo arranca exec si hay mensaje, asi que el
  checkpoint ocioso llega solo cuando la cola drena. La barrera explicita a peers sigue siendo
  excepcional;
- la secuencia completa es la de la seccion 0-bis: **higiene -> dejar de rutear -> podar -> volver
  a rutear**;
- el checkpoint **no relaja claim-as-lock** ni permite podar a traves de scopes de peer vivos.

**Las cuatro superficies (problema n-ario de la 0120 s.4):** esta copia viva, el master exportable,
`TASK_PROTOCOL.md` y la copia desplegada en cada instancia deben decir lo mismo. La 0120 alinea
**esta y la normativa**; el master espera al generador y la desplegada espera a **TASK-0417**,
porque hoy el informe de upgrade no compara la ruta consumida.

## 0-bis. SECUENCIA OBLIGATORIA: higienizar -> dejar de rutear -> podar -> volver a rutear

> Directiva del operador, 2026-08-16, con la medicion que la respalda.

    1. HIGIENIZAR el mailbox   (mailbox_archive de los consumidos)  <- el 73% del gate
    2. DEJAR DE RUTEAR         (la ventana de poda se abre SOLA)
    3. PODAR                   (cero claims y cero locks)
    4. VOLVER A RUTEAR

**El paso 1 es el que mas mueve la aguja.** Medido:

    open/ 61 mensajes  ->  cold_start_tokens 74130
    open/  5 mensajes  ->  cold_start_tokens 20277   (umbral 20000)

**53.853 tokens, el 73 %, eran mailbox.** Y la confirmacion inversa, el mismo dia: rutear tres
reviews subio el gate de 20277 a **22201**. **Rutear engorda el mismo gate que la higiene
adelgaza**, asi que el orden no es preferencia: es lo unico que converge.

**CORRECCION de una afirmacion que estuvo medio dia en commits y en una nota de version:**
`cold_start_tokens` **NO** es irreducible. Lo declare asi tras medirlo justo despues de una poda
que no tocaba el mailbox, y generalice mal. `prune_state.py:286` **si** poda mailbox
(`mailbox_keep_recent: 8`) pero **recoge de `answered/`, no de `open/`**: la clasificacion de
"consumido" es del ORQUESTADOR. **Correr la poda NO es hacer higiene de mailbox.**

## 0-ter. La ventana de poda: la abro yo, no se pide (2026-08-16)

**La poda no coexiste con ningun trabajo de peon:** su claim pide
`Area_comun/state/CLAIMS.json` **ENTERO**, asi que choca con CUALQUIER claim activo, sea de la
tarea que sea (`claim acquire overlaps active claim ...`). Igual para toda op que reclame el
ledger completo.

**La ventana NO se pide a los peones: se abre sola.** Un peon solo arranca exec **si hay mensaje
que procesar**. Con la cola vacia se queda quieto por si mismo -- sin gastarle un exec, sin que
se auto-retire, sin relanzar nada.

> **PODAR ANTES DE RUTEAR. Cada mensaje que se suelta cierra la ventana que hace falta.**

**No la caces a ojo: dura SEGUNDOS** (el hueco entre que un peon cierra su exec y tomaria el
siguiente mensaje). Encadenala a un comando en background con las TRES condiciones a la vez:

```bash
n=0
until { [ ! -f .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.lock ] \
     && [ ! -f .protocol-tmp/analista_mailbox_cron/analista_mailbox_cron.lock ] \
     && [ "$(python -c "
import json
c=json.load(open('Area_comun/state/CLAIMS.json'))
cl=c.get('claims',c) if isinstance(c,dict) else c
print(len([x for x in cl if x.get('status')=='active']))
")" = "0" ]; } || [ $n -ge 90 ]; do sleep 20; n=$((n+1)); done
python scripts/prune_state.py --root . --apply
```

Evidencia del 2026-08-16: fallo a las 12:29 (claim de Codex en 0378-r4) y a las 13:43 -- esta
segunda **la cerre yo al rutear un GO**, orden invertido. Entro a las 13:56:52, intento 22 del
encadenado, 32 claims archivados, exit 0.

**Por que NO pedirlo por mailbox:** no se puede expresar "espera" en un canal donde todo mensaje
consume una ejecucion. El mensaje de pausa gasta un exec, y cada ronda vacia cuenta contra
`MaxNoCoordinatorRounds 15` -> el peon **se auto-retira en ~75 min**. `STOP_JOB` es todo-o-nada y
volver exige relanzar (accion con permiso), y el marcador de parada no respeta el limite de lote
(TASK-0407). La barrera correcta, si se hace algun dia, es una marca de estado consultada en
`Acquire-ExecReservation` (`deferred: quiesce_active`), no un mensaje.

**Lo que la poda NO cierra:** `cold_start_tokens` mide el coste de lectura en frio, que dirigen
las tareas **ABIERTAS**, mientras la poda solo archiva las **TERMINALES**. El gate seguira rojo
por mucho que se pode; lo que si despeja es `released_ratio` y `done_ratio`.

## 1. Escribir un mensaje bien formado (antes de dejarlo en open/)
- **ASCII puro.** Nada de acentos ni simbolos tipograficos. Usa `->`, `>=`, `AND`, `-`.
  `scan_encoding.py` cubre `open/` Y `archived/`.
- **`requires_response: true` EXIGE `response_owner: <destinatario>`** + `requested_action` y/o `question`.
  Sin ellos, `validate_collaboration_state.py` sale exit 1.
- **`type` que el cron del peer reconoce:** Codex acepta `GO/REQUEST/ACTION/HANDOFF/REVIEW/QUESTION/DECISION`;
  **Analista acepta `REVIEW/REQUEST/ACTION/QUESTION/DECISION` (NO "GO")**. O pon `requested_action` no vacio.
- **FOOTGUN stop-order:** no combines un verbo de corte `(detener|deten|parar|para|stop|standdown|stand-down)`
  con `(cron|monitor|monitoreo|<peer>)` en una misma linea: el cron del peer se auto-detiene. Evita "para".
- **GATEA tu propio mensaje:** `python scripts/validate_collaboration_state.py` exit 0 **Y**
  `python scripts/scan_encoding.py` exit 0, antes de seguir.

## 2. Claims sobre mailbox (DECISION-0020)
- **SOLO file-scoped a archivos MSG-*.md concretos. NUNCA dir-level** (`Area_comun/mailbox/open` a secas
  bloquea el canal entero y al peer). `submit_intent` lo rechaza: "mailbox claim must be file-scoped".
- No listes en el `scope` un MSG que aun no existe (artifacts-before-claim, #1).

## 3. Cuando archivar (triggers de higiene)

> **REGLA DURA DEL OPERADOR (2026-07-04): CADA REPORTE = CHECKPOINT DE HIGIENE.** Cada vez que entregas
> un reporte/handoff al operador (o cierras un turno con salida visible), ANTES o JUNTO con ese reporte
> haces una PASADA de higiene: clasifica `open/` (consumidos vs vivos) y archiva los consumidos. NO es
> opcional ni depende del umbral cada-5/watchdog>=10 (esos son la red de respaldo que se cae bajo carga;
> el reporte es el trigger DETERMINISTA que no se te vuela). El reporte solo se entrega DESPUES de dejar
> `open/` con solo lo accionable, o -- si la ventana NO es segura (peer en exec/lock, ver s.4b) -- el
> reporte DECLARA EXPLICITAMENTE los N consumidos que quedan pendientes de archivar y por que
> (drift-abort). Nunca entregues un reporte dejando consumidos en `open/` SIN decirlo. Un `open/` sucio
> tras un reporte es un reporte falso del panel del operador.

> **FALLO REAL 2026-07-05 (por que la regla de arriba se cae bajo carga, y como se corrige):** en una
> cascada rapida de 7-8 ciclos bloqueo->grant-DBA->retry (F-NOVA-01 de TASK-0253), el Arquitecto emitio
> reporte tras reporte sin correr NUNCA la higiene -- el operador tuvo que llamar la atencion 2 veces
> ("por que debo picarte", "no estan los watchdog vivos"). Causa raiz: la regla vive como TEXTO en este
> skill, sin ningun enforcer mecanico que la dispare antes de escribir el reporte; bajo presion (cada
> mensaje del peer exige una accion inmediata), la atencion se va al contenido tecnico del bloqueo y la
> higiene se trata como "tarea aparte, la hago despues" -- que nunca llega. Memoria previa
> ([[feedback-higiene-mailbox-cada-5]]) YA registraba este mismo patron de fallo; volvio a pasar, prueba
> de que "recordarlo" no basta bajo carga.
> **FIX ESTRUCTURAL (no depende de la memoria, se acopla al mismo paso mecanico que ya vas a ejecutar):**
> la clasificacion de higiene (open/ consumido vs vivo) va DENTRO del MISMO checklist de "gate antes de
> commit" que usas para CUALQUIER escritura de mailbox (ver s.4b y `arquitecto-ledger-ops`), no como un
> paso posterior separado. Concretamente: cada vez que vas a `git commit` algo que toca
> `Area_comun/mailbox/` o `Area_comun/state/`, la MISMA pasada que corre `validate`+`scan_encoding` responde
> tambien: "algo en `open/` quedo resuelto por este commit (una respuesta que acabo de escribir, un
> veredicto que acabo de procesar)? -> archivalo en el MISMO submit_intent/commit, no en uno aparte".
> Si la ventana no es segura (peer con lock), la higiene queda pendiente pero DECLARADA en el proximo
> reporte -- nunca implicita. La poda (`prune_state.py --check`) se revisa en el MISMO punto (s.3b).

### 3b. Poda del estado (protocol_prune / prune_state.py) -- mismo checkpoint que la higiene de mailbox
`scripts/prune_state.py` archiva entradas terminales del estado "caliente" (tareas `done`, claims
`released`) cuando cruzan un UMBRAL configurado en `protocol.config.json` (`done_ratio_hard`,
`released_ratio_hard`; tambien hay un umbral de `cold_start_tokens`). **No es mantenimiento de cada commit,
es de UMBRAL** -- pero revisar si esta vencida es tan barato como correr `--check`, asi que se hace en el
MISMO checkpoint que la higiene de mailbox (mismo reporte, misma pasada), no en un ciclo aparte que se
puede saltar:
```
python scripts/prune_state.py --check
```
Exit 0 = no hace falta podar todavia. Exit 1 con `PRUNE DUE: ...` = corre:
```
python scripts/prune_state.py --root . --actor-id Arquitecto --timestamp <ISO> --commit $(git rev-parse HEAD) --apply
```
Mismas reglas de ventana-idle y lock-contention que el resto de `submit_intent` (s.4b): si un peer tiene
lock activo, el archivo del ledger puede estar tomado (`OSError: Resource deadlock avoided`) -- reintenta
cuando el peer quede idle, no fuerces. Gatea `validate`+`scan_encoding` despues de aplicar, igual que
cualquier otra transaccion gobernada, y commitea/pushea el resultado.

Archiva un MSG de `open/` cuando quede **resuelto**:
- **Respondido:** su respuesta ya existe (el `response_owner` contesto).
- **GO/ACTION consumido:** la tarea que ordenaba ya se entrego (existe su commit `deliver`).
- **REVIEW resuelto:** el veredicto (GO/NO-GO) ya se emitio y se actuo (incluye el MSG de solicitud Y el
  MSG de veredicto de la ronda cerrada).
- **FYI/HANDOFF informativo:** ya leido, sin accion pendiente.
- **Superado:** una ronda/mensaje mas nuevo lo reemplaza (p.ej. remediation-2 supera la entrega original).
Manten en `open/` solo lo **accionable o en espera de respuesta**. Escribe la asercion (el "archivado") solo
**despues** de que el ledger lo respalde (DECISION-0020 #6).

## 4. Como archivar (SOLO Arquitecto; via submit_intent)
`mailbox_archive` es una transaccion gobernada (escritor unico). Receta:
1. **Claim file-scoped** que cubra las DOS rutas del MSG + su propia fila para liberarse:
   - `Area_comun/mailbox/open/<MSG>.md`, `Area_comun/mailbox/archived/<MSG>.md`, y `CLAIMS.json#<claim_id>`.
2. `submit_intent` con la intent:
   `{"type":"mailbox_archive","message_id":"<MSG-... id seguro, sin / \\ ..>"}`
   (mas los campos de accountability que exige el payload).
   `--actor-id Arquitecto --timestamp <ISO> --commit $(git rev-parse HEAD)`.
3. Efecto: el archivo se mueve `open -> archived` (transicion registrada en el ledger).
4. **Lote:** varios MSG resueltos en un solo `submit_intent --intents {"intents":[...]}` (uno por MSG).
   El intent lleva accountability: `{"type":"mailbox_archive","message_id":"<id sin .md>","author":"<from del MSG>","relayed_by":"Arquitecto","endorsement":"none"}`.
Ver la receta base y los gotchas en `arquitecto-ledger-ops`.

### 4b. EJECUTAR la higiene sin romper nada (lecciones 2026-07-02, aprendidas a golpes)
- **VENTANA IDLE de verdad, verificada en paso SEPARADO:** ANTES de disparar un lote, comprueba en un comando
  aparte: 0 claims de peers, `git status` sin state a medias de peer, y NINGUN peer con lock (exec). **Si algo no
  esta limpio, ABORTA -- no dispares.** (Error real: correr el check y el submit_intent en el mismo comando y
  archivar mientras Codex entregaba -> working tree interleaved.) Si YA quedo interleaved con una entrega de peer:
  el submit_intent es atomico (validate se mantiene VERDE); deja que el peer commitee (su commit hornea tus
  archive-events en los state files compartidos) y luego TU commiteas los movimientos `open->archived` que el peer
  no stageo (si no, HEAD queda inconsistente para clon limpio: snapshot dice archivado pero los .md siguen en open/).
- **LOTES PEQUENOS (<=3), timeout generoso, y VERIFICA EL ESTADO FISICO tras cualquier timeout (leccion
  2026-07-07, reforzada -- mailbox_archive es TIMEOUT-PRONE aun con los peers idle):** el submit_intent re-replaya
  el event log creciendo y bajo I/O variable timeoutea aun sin contencion de peer. Un lote de 6 timeoteo DOS veces
  en una sesion; **lotes de <=3 completaron limpios.** Corre con timeout 100-150s (o `run_in_background`), NUNCA
  foreground corto. El timeout NO significa fallo: los eventos suelen aplicar (revisa `tail events.jsonl` = los
  `intent.applied` esperados) pero el EFECTO DE ARCHIVO (mover el .md) y/o el snapshot pueden quedar a medias.
- **RECUPERACION del half-apply -- en instancia ENFORCE (materialize on) el fix es re-materializar, NO git checkout:**
  1) mira que MSG siguen en `open/` (los no movidos); si el evento `mailbox_archive` aplico pero el .md sigue en
  `open/`, **muevelo A MANO** (frontmatter `status: open`->`archived` + `mv open/ -> archived/`) -- reenviar el
  intent falla ("message not found in open" porque el evento ya dice archivado). 2) Si `snapshot.up_to_seq` quedo
  detras del head del log (`validate` rojo "snapshot mismatch"), **re-materializa Y regenera el snapshot**:
  `materialize_from_event_log_if_enabled(Path('.'))` y luego `rebuild_snapshot(Path('.'))`+`write_snapshot(...)`
  (re-materializar reconstruye los JSON pero NO actualiza snapshot.json). 3) Si el `claim release` final no aplico
  (claim sigue activo), reenvia SOLO ese intent standalone. 4) `validate`+`scan_encoding` exit 0, y commitea los
  moves+state como snapshot consistente. (En instancia SIN materialize, en cambio, usa git checkout con la guarda
  de peer-lock de abajo -- son caminos distintos segun el modo de la instancia.)
- **NUNCA `git checkout runtime/state/*` / `Area_comun/state/*` mientras un peer esta en EXEC (leccion 2026-07-03,
  colision real):** si un lote de higiene half-aplico (submit_intent cortado a 2min: events appendidos, snapshot
  detras, moves incompletos) y quieres revertir, VERIFICA PRIMERO que ningun peer tenga lock. Si Codex/Analista
  esta escribiendo (submit_intent del flip de otra tarea), tu `git checkout events.jsonl` REVIERTE los eventos del
  peer -> corrompe el event log y deja TASK_INDEX inconsistente con events (validate rojo). Me paso: colisiono con
  el flip de 0234 de Codex. FIX seguro: si el half-apply es TUYO y esta SIN COMMITEAR y ningun peer escribe,
  `git checkout` de los state files restaura HEAD limpio; si un peer esta en exec, ESPERA a que termine y commitee
  (su commit es la fuente de verdad), luego re-haces tu higiene desde el HEAD sincronizado. El re-materialize
  (`materialize_from_event_log_if_enabled`) es NO-OP si la instancia viva no tiene materialize enabled -> no
  cuentes con el para recuperar; usa git checkout (con la guarda de peer-lock) o espera al peer.
- **NO higienices JUSTO DESPUES de rutear un REVIEW a un peer (leccion 2026-07-03):** la higiene deja el working
  tree con drift (events/CLAIMS modificados, snapshot detras) hasta que commiteas; si el peer EXEC su review en esa
  ventana, ABORTA (su gate detecta el drift, silent-refusal; err.log "snapshot mismatch / drift detected"). La
  higiene va COMMITEADA Y PUSHEADA (HEAD limpio) ANTES o BIEN SEPARADA de rutear reviews. Preferir higiene
  INTERACTIVA con commit inmediato en ventana idle sin peer-exec inminente (p.ej. POST-cierre de tarea).
- **Commit:** stage explicito de `Area_comun/mailbox` + `Area_comun/state` + `runtime/state` (los movimientos y el
  ledger juntos = snapshot consistente), gate `validate`+`scan_encoding` exit 0, push.

## 5. Peers: detectar y senalar (DECISION-0018), no tocar
Si Codex/Analista ven un mensaje stale (respondido pero sigue en open/), un estado que contradice el mailbox,
o un claim huerfano sobre un MSG: **notifican al Arquitecto** con un MSG accionable y lo registran. **No**
dir-claiman el mailbox, **no** archivan (no tienen orchestrator), **no** arreglan en silencio bajo claim ajeno.

## 6. Post-archivo (cierre limpio)
- `scan_encoding.py` (cubre open+archived) + `validate_collaboration_state.py` exit 0; **drift 0**.
- Commit con **stage explicito por path** (nunca `git add -A`); push si verde.
- Actualiza memoria (DECISION-0026). Los mensajes de FYI de cierre van **despues** del archivado, no antes.

## Checklist de una linea
**Antes de CADA reporte (mismo gate que el commit, no un paso aparte): pasada de higiene (clasifico open/ +
archivo consumidos, o declaro los pendientes) + `prune_state.py --check` (si PRUNE DUE, aplico en el mismo
checkpoint).** -
Escribo: ASCII? response_owner? type valido para el peer? sin corte+peer? gateado exit 0? -
Archivo (solo Arq): mensaje resuelto? claim file-scoped open+archived+#self? message_id seguro? orchestrator? -
Peer: stale? -> senalo al owner (DECISION-0018), no toco.

## Dos reglas duras que costaron encargos vivos (2026-08-18/19)

**NO archives un `MSG-...-to-<Peer>` que no este en el `seen.json` de su destinatario.** Una pasada
de higiene archivo un ACTION **vivo y sin consumir**: el peon nunca lo vio y ademas se le borro la
entrada del `retry.json`. La tarea quedo `in_progress` **sin mensaje, sin reintento y sin claim** --
un encargo huerfano que NINGUN vigia ve, porque los tres desenlaces que vigilan (entrega, cuelgue,
`RETRY_EXHAUSTED`) exigen que el encargo haya llegado a ejecutarse. "Consumido" no es una propiedad
del mensaje ni de su edad: es una propiedad del DESTINATARIO. Antes de meter un encargo en un lote,
exige UNA de dos pruebas: su clave esta en `.protocol-tmp/<peer>_mailbox_cron/*.seen.json`, o existe
su artefacto de entrega (commit del maker, handoff, veredicto). Sin ninguna, **no se archiva aunque
lleve horas**. Si ya se archivo, el destrabe no es des-archivar: es **reemitir con ID NUEVO**.

**ARCHIVAR NO DESENCOLA.** Un `mailbox_archive` gobernado saca el mensaje de `open/` pero deja su
entrada viva en el `retry.json` del peer, que seguira reintentandolo. Toda muerte o consumo de un
encargo son **TRES pasos juntos, nunca un subconjunto**: (1) archivar de forma gobernada, (2) borrar
su entrada del `retry.json` (con respaldo `.bak-<hora>` antes), (3) si murio, reemitir con **ID
NUEVO** escribiendo dentro la causa y la cuenta de vidas. Ojo con `outcome=defer_terminal`: **agota
la entrada entera**, no consume un intento, aunque imprima un `attempts=N` que parece margen.
