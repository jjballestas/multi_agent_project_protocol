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
> tambien: "¿algo en `open/` quedo resuelto por este commit (una respuesta que acabo de escribir, un
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
- **CORRE LOS LOTES EN BACKGROUND** (`run_in_background`) o con timeout largo, **NUNCA en foreground** con el tool:
  el submit_intent re-replaya el event log creciendo (~30-60s/lote) y el tool corta a 2min -> mata el lote a mitad
  (half-apply). Lotes de ~6. Gatea `validate` VERDE despues de cada lote.
- **RECUPERACION si un lote se corto:** `validate` VERDE => submit_intent revirtio o completo atomico (sin drift);
  mira que MSG siguen en `open/` (los no-archivados) y commitea los movimientos+state de los lotes YA aplicados
  como snapshot consistente; re-corre los faltantes en BACKGROUND. Nunca commitees un state a medio aplicar.
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
checkpoint).** ·
Escribo: ASCII? response_owner? type valido para el peer? sin corte+peer? gateado exit 0? ·
Archivo (solo Arq): mensaje resuelto? claim file-scoped open+archived+#self? message_id seguro? orchestrator? ·
Peer: stale? -> senalo al owner (DECISION-0018), no toco.
