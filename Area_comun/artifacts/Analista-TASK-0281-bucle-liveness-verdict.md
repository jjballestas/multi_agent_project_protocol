# Veredicto adversarial -- TASK-0281 (commit 8ea4874)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-21 05:37 (reloj del sistema, sin convertir)
- Encargo: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0281-y-orden-de-cierre
- **Veredicto: NO-GO / CHANGE-REQUIRED**

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado | `8ea4874243b3603c16b0c0fde78629857b53f8c8` ("fix(TASK-0281): harden mailbox loop liveness") |
| Es ancestro de main | si (`git branch --contains` -> main, origin/main) |
| Commits posteriores que tocan el codigo juzgado | ninguno (`33e3af7` solo anade handoff + estado + memoria; `4e27033` solo memoria) |
| HEAD del protocolo al emitir | `323ac9f` |
| Clon limpio | `D:/ccv0281` (`git clone --no-local` + `git checkout 8ea4874`); todos los gates corridos ALLI |
| Alcance | solo este hub. **Sin producto en alcance.** |

Aviso de ventana (DECISION-0018, informativo): al emitir, Codex tiene entrega en vuelo de
`F-0280R4-02` (claim activa `CLAIM-20260721-Codex-TASK-0280-F02-memory` sobre
`CLAIMS.json#...` y `personal/Codex/Memory.md`; arbol con esas rutas modificadas sin
commitear). No toque ninguna de esas rutas. Comito solo mis dos archivos por pathspec
explicito.

## 2. Reproduccion (todo por exit code, en el clon limpio sobre 8ea4874)

```
python scripts/validate_collaboration_state.py            -> exit 0  ("OK: collaboration state is valid.")
python scripts/scan_encoding.py                           -> exit 0  ("OK: encoding scan is clean.")
python scripts/scan_domain_neutrality.py                  -> exit 0
protocol_state_drift(.)['has_drift']                      -> False   (up_to_seq 5518, hot==replay)
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
                                                          -> exit 0  ("mailbox retry cases: PASS")
```

**Los cinco gates estan VERDES sobre `8ea4874`.** Nada de lo que sigue los contradice: son
caminos que la suite no cubre. Los cuatro negativos permanentes que anade el maker prueban lo
que dicen probar; el problema es la familia que dejan fuera.

## 3. Banco de falsacion propio (vector por vector)

Metodo: extraccion verbatim de `Get-OwnEvidence` y `Get-StagedResidueState` del `.ps1` de
`8ea4874` y ejecucion con payloads propios (probes A y D), mas tres corridas de comportamiento
del runner COMPLETO en sandbox git real (probes B, C, E). No confie en nombres de test ni en
el texto del handoff.

| # | Vector atacado | Metodo | Resultado |
|---|---|---|---|
| V1 | punto 1: lock huerfano sin lease se auto-sana | suite enviada + lectura | **PASS** (`SELF_HEAL_ORPHAN_LOCK`, lock borrado, cola viva) |
| V2 | punto 1: tramo lock->exec cubierto por el mismo `finally` | lectura del diff | **PASS** (todo el tramo entro al `try`; el `catch` guarda `$ledgerHeadBefore -and $headBefore`) |
| V3 | punto 2: `ledger_unreadable_before_exec` con tope y senal | suite enviada | **PASS** (`RETRY_EXHAUSTED attempts=5 signal=watchdog`) |
| V4 | punto 3: log DESORDENADO (evento propio historico con seq alto) | suite enviada + lectura | **PASS** (la ventana ya no depende del orden) |
| V5 | punto 3, control negativo: sin actividad, ledger intacto | probe A c1 | **PASS** (`own=False`) |
| V6 | punto 3, control positivo: evento propio NUEVO anadido | probe A c2 | **PASS** (`own=True`) |
| V7 | **punto 3: log REESCRITO que crece (re-genesis / migracion / restauracion)** | probe A c3 + probe B (runner completo) | **SLIP -> F-0281-01** |
| V8 | **punto 3: log COMPACTADO que encoge, con trabajo propio real** | probe A c5 | **SLIP -> F-0281-02** |
| V9 | punto 3: compactacion + apendices ajenos que rebasan la base | probe A c4 | PASS por aritmetica de bytes, no por construccion (ver F-0281-01) |
| V10 | punto 4: residuo fresco no stageado difiere con senal | suite enviada + probe C fase 1 | **PASS** (`worktree_residue_live` + `RETRY_EXHAUSTED`) |
| V11 | punto 4, arbol limpio | probe D2 | **PASS** (`none`) |
| V12 | **punto 4: ruta que git ENTRECOMILLA (espacio o byte no-ASCII)** | probe D2 + probe E (runner completo) | **SLIP -> F-0281-03** |
| V13 | **punto 4: agotamiento sin recuperacion tras limpiarse el arbol** | probe C fase 2 (runner completo) | **SLIP -> F-0281-04** |
| V14 | regresion: frontera de outcome (token > exit > evidencia > texto) | diff + suite | **PASS** en la forma; ver nota en F-0281-01 |
| V15 | regresion: lo cerrado en 0280 sigue cerrado | suite enviada exit 0 | **PASS** (torn-tail, pre-dirty, preservacion firmada, ledger ambiguo, lease) |

## 4. Los cuatro deslices, falsificables

### F-0281-01 (BLOQUEANTE) -- la ventana por bytes SI deja pasar un evento anterior a ella

Es la respuesta directa a tu pregunta, y es **si**. `Get-OwnEvidence` asume que
`events.jsonl` es estrictamente append-only. Si el log se **reescribe y queda mas largo**
que la base, el offset previo apunta a otro sitio y la ventana `[base, fin)` cubre
**historia**, no trabajo nuevo.

Probe A (funcion extraida verbatim, base = 562 bytes):

```
c1_no_activity                 len=562   own=False   PASS
c2_real_new_own_event          len=665   own=True    PASS
c3_rewrite_grows_same_history  len=856   own=TRUE    SLIP   <-- misma historia, cero trabajo nuevo
```

Probe B (runner COMPLETO, sandbox git real): agente falso que **no hace nada**, no emite
token de outcome, sale 0, y solo reescribe el ledger con la MISMA historia re-serializada
mas larga:

```
EXEC_START pid=27056 message=MSG-probe.md
EXEC_EXIT code=0 outcome=confirmed message=MSG-probe.md
seen.json = {"MSG-probe.md": "MSG-probe.md|153|639202014413192176"}
invocaciones del agente = 1   |   mensaje sigue en open/ sin responder
```

**El mensaje queda consumido para siempre (`seen`) con cero trabajo hecho.** Esto viola
palabra por palabra el acceptance del propio punto 3: *"se toma del tamano en bytes ... de
modo que una cola desordenada **o reescrita** no pueda hacer pasar un evento historico como
propio de la ventana"*. La reescritura esta explicitamente en el criterio, y no esta cerrada.

No es hipotetico: `runtime/eventlog.py:1131` (`EventLog.compact_through`) **reescribe
`events.jsonl` en sitio** re-serializando los eventos restantes. El supuesto append-only lo
rompe este mismo repositorio.

**De que lado falla:** de los dos. Si la reescritura acaba **mas larga** que la base,
acepta de mas (F-0281-01: confirma trabajo que no existio). Si acaba **mas corta**, acepta
de menos (F-0281-02).

Sobre F-0280R4-01: tienes razon en que un `torn_tail` no puede desplazar la ventana hacia
atras, porque la longitud incluye el fragmento desgarrado. Ese camino concreto **si** muere
por construccion. Pero la FAMILIA ("evidencia historica pasa por propia") no muere: reentra
por la puerta de la reescritura. Y por eso mismo confirmo tu diagnostico de metodo: anadir
un guard de `torn_tail` habria sido enumeracion. Lo que hace falta no es otra rama sino un
ancla que no dependa de la posicion en bytes.

### F-0281-02 (no bloqueante por si solo, agravante de F-0281-04) -- la compactacion oculta trabajo real

Probe A c5: el peer hace trabajo real y firma un evento nuevo, pero una compactacion durante
la ventana deja el fichero mas corto que la base -> `currentLength -le $LedgerBytesBefore` ->
`own=False`. El trabajo real no se acredita, el outcome cae a `unconfirmed`, se dispara el
rollback y se consume presupuesto de reintento. Con F-0281-04 debajo, eso termina en
descarte permanente de un mensaje que **si** se trabajo.

### F-0281-03 (BLOQUEANTE) -- el punto 4 reintroduce el punto 2: defer silencioso e infinito

`Get-StagedResidueState` ahora parsea `git status --porcelain=v1`, pero git **entrecomilla**
las rutas con espacio o bytes no-ASCII (`core.quotepath` por defecto). `$row.Substring(3)`
devuelve `"peer draft notes.md"` **con las comillas**, y `Test-Path -LiteralPath` lanza
`Caracteres no validos en la ruta de acceso`. Con `$ErrorActionPreference = "Stop"`, la
excepcion **escapa** de `Invoke-PeerForMessage` (la llamada esta en la linea 696, FUERA del
`try` que abre en la 735) y cae en el `catch` del bucle principal.

Probe D2 (funcion extraida):

```
ascii_control     ?? fresh-residue.txt                    -> "live"   PASS
nonascii_quoted   ?? "residuo-a\303\261adido.txt"         -> throw    SLIP
space_quoted      ?? "fresh residue.txt"                  -> throw    SLIP
clean_tree        (vacio)                                 -> "none"   PASS
```

Probe E (runner COMPLETO, 12 s, un unico fichero sucio no rastreado con espacio en el nombre):

```
LOOP_ERROR rondas         : 12
muestra                   : LOOP_ERROR Caracteres no validos en la ruta de acceso.
registros RETRY_*         : NINGUNO
retry.json                : no existe
agente invocado           : False
mensaje sin procesar      : True
```

Doce rondas, cero reintentos contabilizados, cero `RETRY_EXHAUSTED`, cero senal de watchdog,
el agente nunca arranca y el mensaje nunca se procesa. **Eso es exactamente el defecto (2)
que esta tarea existe para matar** -- *"Ningun defer puede ser silencioso e infinito"* --
reintroducido por la puerta que abre el arreglo del defecto (4). El pre-gate viejo miraba
solo el indice; el nuevo mira todo el arbol y todos los no-rastreados, asi que la superficie
de disparo crece enormemente.

Exposicion real, no hipotetica: este repositorio **ya versiona** una ruta con espacio,
`examples/full_runtime_instance/personal/operador humano/.gitkeep`. Verificado en el clon
limpio: crear cualquier fichero en esa area de participante produce
`?? "examples/full_runtime_instance/personal/operador humano/nota.md"` y atasca el runner.
Y `personal/<id>/` es precisamente donde DECISION-0016 manda que cada participante escriba.

### F-0281-04 (BLOQUEANTE) -- el punto 4 cambia un problema por otro: descarte permanente

Es tu ataque numero 2, y se confirma, aunque no en la forma que temias. El defer **si**
agota y **si** senaliza (el maker cumple la letra del acceptance). Lo que no hace es
**recuperar**. Probe C, runner completo:

- Fase 1 -- un peer esta a mitad de entrega (un fichero rastreado modificado, fresco). Tres
  rondas: `RETRY_DEFER attempt=1`, `attempt=2`, `RETRY_EXHAUSTED attempts=3 signal=watchdog
  reason=worktree_residue_live`. El agente **nunca** se invoca.
- Fase 2 -- el peer termina y commitea. **El arbol queda perfectamente limpio.** Once rondas
  mas: `Heartbeat processable_messages=0`, once veces. El agente sigue sin invocarse. El
  mensaje `requires_response: true` sigue en `open/` sin responder, para siempre.

```
retry.json = {"MSG-urgent.md": {"attempts":3,"exhausted":true,"outcome":"deferred",
              "reason":"worktree_residue_live", ...}}
agente invocado tras limpiarse el arbol : False
rondas declarando la cola VACIA          : 11
```

El filtro de `Get-ProcessablePeerMessages` excluye para siempre todo mensaje con
`exhausted=true` y firma igual; solo un cambio de nombre/tamano/mtime del fichero resetea el
presupuesto. La cola no queda "parada para siempre": queda **declarandose vacia** mientras
pierde un mensaje vivo. Un observador (o un watchdog que mire la cola en vez del log) ve un
bucle sano.

La asimetria es el defecto: un veto **ambiental** (el peer estaba ocupado 3 rondas) consume
el mismo presupuesto que un intento **real**. Post-exec el descarte es defendible -- el
agente corrio tres veces y fallo. Pre-exec el agente no corrio **ni una sola vez**. Bajo
DECISION-0020, dos agentes escribiendo en ventanas solapadas es la condicion normal de
operacion, no la excepcion.

## 5. Residuos declarados (NO bloqueantes, para el registro)

- **R1** -- `Clear-StaleCronLockIfSafe` se ejecuta en la linea 823, ANTES del guard de
  instancia unica de la 824. Un arranque concurrente puede borrar el lock de una instancia
  viva durante la ventana entre escribir el lock (736) y escribir el lease (755), que incluye
  un arranque de python y dos `git diff`. No lo reproduje; el guard de pid lo hace poco
  alcanzable.
- **R2** -- `Get-OwnEvidence` acredita a este exec cualquier evento firmado del peer que
  aparezca en la ventana, incluido el que escriba un humano o una segunda instancia del mismo
  peer durante el exec. Es preexistente (la base por `seq` tenia lo mismo) y no lo cuento
  contra 0281.
- **R3** -- `Get-WorktreeDiskProof` (linea 478) parsea el mismo `--porcelain -z`. Con `-z` git
  NO entrecomilla, asi que ahi no aplica F-0281-03; lo dejo anotado para que el arreglo no
  uniformice en la direccion equivocada.
- **R4** -- `ROLLBACK_DEFER reason=rollback_probe_failed` aparecio en probe B sobre un ledger
  reescrito. No lo investigue a fondo; queda como sintoma adyacente.

## 6. Recomendacion de cierre

**CHANGE-REQUIRED.** No es cerrable. Dos de los cuatro puntos que el maker reclama cerrados
no lo estan:

- el punto 3 incumple su acceptance **verbatim** (la palabra "reescrita" esta en el criterio);
- el punto 4 reintroduce el punto 2 (F-0281-03) y crea perdida silenciosa de mensajes
  (F-0281-04).

Los puntos 1 y 2 estan cerrados y bien probados; el trabajo no es descartable, es incompleto.

Lo que un arreglo tiene que **sobrevivir** (no propongo implementacion; soy checker):

1. Que el banco de negativos incluya **reescritura del log**, en las dos direcciones (mas
   largo y mas corto que la base), con control positivo, y que un evento propio historico NO
   confirme. Un ancla que dependa de la posicion en bytes no puede pasar esa prueba: hace
   falta que la evidencia se ate al exec (correlacion propia del exec), no al offset.
2. Que el pre-gate de residuo sobreviva a rutas entrecomilladas por git -- espacio y byte
   no-ASCII -- **sin lanzar**, y que ningun camino del pre-gate pueda producir `LOOP_ERROR`
   en vez de un defer contabilizado.
3. Que un veto ambiental que impide invocar al agente sea distinguible de un intento real
   fallido, y que el mensaje vuelva a ser elegible cuando la condicion ambiental desaparece.
   Mientras un mensaje agotado siga fuera de la cola, `Heartbeat processable_messages=0` es
   un reporte falso.

**Bucle de arreglo esperado:** remediacion por el maker (Codex) acotada a estos tres puntos;
gates afectados = suite `run_mailbox_retry_cases.py` (con negativos nuevos para reescritura,
ruta entrecomillada y recuperacion post-agotamiento) + `validate_collaboration_state.py` +
`scan_encoding.py` + `scan_domain_neutrality.py` + drift 0; re-juicio mio sobre el commit de
remediacion ANTES del commit de cierre. **Maximo 2 iteraciones**; a la tercera escalo al
operador humano.

Sobre el orden de cierre que fijaste: no me pronuncio sobre si 0280 cierra antes o despues,
es tu decision. Solo dejo el dato: **0280 no puede apoyarse hoy en "la base por offset en
bytes" como estructura que mata F-0280R4-01 por construccion.** Mata ese camino concreto, si;
no mata la familia. Si cierras 0280 sobre esa base, el argumento de cierre queda atado a que
F-0281-01 se repare primero.

-- Analista
