---
artifact_id: Analista-TASK-0298-aegis-bridge-observacion-tail-verdict
task_id: TASK-0298
reviewer: Analista
role: adversarial checker (maker != checker)
iteration: 1
created_at: 2026-07-28
local_time: "2026-07-28 00:05 (UTC+2)"
anchor_protocol_commit: 92f9f061e887d70d08501964abc32eea692ec80a
anchor_product_commit: bf0d4775e8fd3d2234783bd451ac2ca3f4b9e06e
product_repo: D:/Agentes/Zeus/Zeus-protocol
verdict: CHANGE-REQUIRED
scope: producto EN ALCANCE (Zeus-protocol, node --test) + coherencia del intake en el hub
blocking_slips: 3
recommended_in_same_loop: 2
declared_residuals: 6
---

# VEREDICTO Analista - TASK-0298 (bridge control-spawn -> observacion-tail) - CHANGE-REQUIRED

**NO-GO (CHANGE-REQUIRED), iteracion 1 de 2.** El cambio de postura es real y lo verifique **por
comportamiento**, no por nombre de test: el bridge ya no spawnea nada (cero procesos hijo del
servidor mientras observa), `/send` es inerte (403, sin evento `input`, sin entrada de auditoria),
la lectura es estrictamente read-only (hashes de estado gobernado y del propio run-log identicos
antes y despues) y la fuente sale de `ARCHITECT_OBSERVE_RUNS_DIR`/config sin ningun path
hardcodeado. Eso lo doy por **verificado**.

Pero tres cosas no se sostienen bajo ataque, y la primera es la que importa mas:

1. **AC5 (redaccion PII) FALLA en el caso normal de esta unidad.** Un productor que escribe
   progresivamente -- exactamente lo que es una sesion viva del Arquitecto -- hace que **ninguna**
   regex de redaccion dispare, porque cada regex necesita el token completo dentro de un mismo chunk
   de poll. En mi corrida con un escritor progresivo el panel emitio **22 eventos, cero marcadores
   `[*-REDACTED]`**, y el correo y el NIT quedaron **en claro** tanto en el SSE como en el fichero de
   auditoria en disco. El test entregado nunca cruza esa frontera porque escribe la linea de PII
   entera en un unico `appendFile`.
2. **La unica dentadura automatica de AC4/I3 (anti-segundo-Arquitecto) falla ABIERTA.** El test
   extrae el manager con una regex anclada al texto fuente y **no comprueba que la extraccion haya
   encontrado algo**: si el ancla desaparece, `manager` es `""` y `assert.doesNotMatch("", /spawn\(/)`
   pasa. Lo demostre: inyecte un `spawn("cmd", [...])` real DENTRO de `createArchitectBridgeManager`
   y renombre la funcion ancla; el test sale **verde, exit 0**. El invariante bandera de la unidad
   queda sin guarda.
3. **AC6 dice que los tests de spawn/control se REESCRIBEN; lo que se hizo fue `test.skip` a 8**,
   y tres de esos no eran de control. Lo demostre por mutacion: con el guard de instancia unica del
   launcher **eliminado** y una referencia a `Area_comun/state/TASK_INDEX.json` **introducida** en el
   fuente del launcher, la suite completa sigue en **141 tests / 133 pass / 0 fail**, identica al
   baseline. Dos invariantes que si estaban cubiertos se quedaron sin cubrir.

El riesgo **E1** (la fuente cron solo observa el modo cron) **no lo cuento como gap**, tal como
declara el intake.

## 1. Ancla canonica y reproduccion

| Item | Valor |
|---|---|
| HEAD del hub al arrancar | `92f9f06` (== `origin/main`) |
| `python scripts/validate_collaboration_state.py` | **exit 0** -- `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py` | **exit 0** -- `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py` | **exit 0** |
| Commit de producto citado | `bf0d477` (`feat(aegis): make architect bridge observation-only`) |
| Clon limpio bajo el scratch root (DECISION-0104) | `D:/Aegis_Scratch/protocol/zp0298` @ `bf0d477`, `git status --porcelain` vacio antes y despues |
| Copias desechables para mutacion | `.../mut` (SLIP-1), `.../mut2` (SLIP-2), `.../unskip` (SLIP-2) |
| Sondas propias | `D:/Aegis_Scratch/protocol/probe/p1..p7` |

Gate del producto en el clon limpio, tal como pide el intake:

```
cd D:/Aegis_Scratch/protocol/zp0298
ZEUS_RUN_SLOW_TESTS=1 PROTOCOL_REPO_PATH=D:/Agentes/multi_agent_project_protocol \
  ZEUS_ROOT_PATH=D:/Agentes/Zeus node --test
-> TEST_EXIT=0 ; tests 141 ; pass 133 ; fail 0 ; skipped 8 ; duration_ms 48517.99
```

Reproduce el recomputo del Arquitecto (141/133/0). El clon revisado no fue mutado en ningun momento:
las mutaciones corrieron en copias aparte.

## 2. Tabla vector por vector

| # | Vector / AC | Metodo (comportamiento) | Resultado |
|---|---|---|---|
| V1 | AC6 gate del producto | `node --test` en clon limpio | **PASS** exit 0, 141/133/0/8 |
| V2 | AC1 sin hardcode | grep `protocol-tmp|arquitecto_cron` en `src/ public/ scripts/ architect-bridge.config.json` | **PASS** (0 coincidencias) |
| V3 | AC1 stream en vivo | sonda P5/P7: append al run-log -> eventos SSE `output` | **PASS** |
| V4 | AC1 rollover | sonda P4b: A, luego B mas nuevo, luego flush tardio de A | **SLIP-4** (seleccion no monotona, re-emision completa) |
| V5 | AC2 read-only (snapshot byte a byte) | sonda P5: sha256 de `TASK_INDEX.json`, `events.jsonl` y del run-log + arbol completo del repo protocolo antes/despues de attach+stream | **PASS** (los 3 hashes identicos; arbol identico: solo los 2 ficheros sembrados) |
| V6 | AC2 no-bypass | `DIRECT_WRITE_ROUTE_PATTERN` intacto en el diff + test vivo `negative no-bypass contract rejects direct ledger write surfaces` | **PASS** |
| V7 | AC3 `/send` inerte | sonda P5: 3 formas de payload | **PASS** -- 403 `observation-only: control disabled` con y sin `message`; cero evento SSE `input`; cero entrada `"kind":"input"` en auditoria; el texto del operador (`TASK-9999`) ausente del audit |
| V8 | AC3 launcher sin stdin-forward | diff + grep sobre `scripts/architect-runtime-launcher.mjs` | **PASS** (`process.stdin.on("data"` retirado; queda solo el handler `end`) |
| V9 | AC3 UI sin compose | lectura del render `renderArchitectConsoleView` | **PASS** en el markup (residual R3: el cliente de control sigue vivo) |
| V10 | AC4 sin spawn -- comportamiento | sonda P5: procesos hijo del servidor durante observacion viva y en dormant | **PASS** -- **0 hijos** en ambos casos; `spawn` ni siquiera se invoca en todo `src/server.js` |
| V11 | AC4 dormant con cron muerto | sonda P5: pid 99999999, pid file borrado, `operatorPresent:false` | **PASS** -- `dormant` + `sessionId:null` + cero eventos `output`; sin pid file -> `dormant`; sin presencia -> 403 |
| V12 | AC4 falsabilidad de la guarda | mutacion: `spawn("cmd",...)` dentro del manager + renombrar el ancla `isProcessAlive` | **SLIP-1 FAIL** -- el test sale **verde (pass 1, fail 0, exit 0)** con un spawn real dentro del manager |
| V13 | AC5 cada clase de PII AISLADA | sonda P3a: los 6 vectores por separado (no en la frase combinada) | **PASS** -- 6/6 redactados, 0 fugas literales |
| V14 | AC5 literales ausentes bajo el framing real | sondas P4a (flush a mitad de token) y **P7 (productor progresivo)** | **SLIP-3 FAIL** -- P7: **cero** marcadores `[*-REDACTED]`; `persona@example.com` y `900.123.456-7` **en claro** en SSE y en el audit |
| V15 | AC6 lista contractual de 5 endpoints | grep del contrato + test vivo | **PASS** (status/open/send/stop/stream) |
| V16 | AC6 "los tests se REESCRIBEN" | des-skip + mutacion de invariantes del launcher | **SLIP-2 FAIL** -- suite verde con el lock de instancia unica retirado y con una ruta gobernada introducida en el launcher |
| V17 | Honestidad del estado | sonda P6a: pid vivo + `observeRunsDir` inexistente | **SLIP-5** -- `status: "alive"` sin ningun evento de error: falso verde |

## 3. Bloqueos

### SLIP-1 (BLOQUEANTE) -- la guarda de AC4/I3 falla ABIERTA

`tests/staticContract.test.js`, test *"TASK-0298 architect bridge is dormant for a dead cron and
contains no spawn route"*:

```js
const manager = source.match(/function createArchitectBridgeManager\(\)[\s\S]*?\n}\n\nfunction isProcessAlive/)?.[0] || "";
assert.doesNotMatch(manager, /\bspawn\s*\(/);
```

El `|| ""` convierte cualquier fallo del ancla en una asercion vacia. Reproduccion (copia
`D:/Aegis_Scratch/protocol/mut`):

1. Inyectar dentro de `createArchitectBridgeManager`:
   `const evil = spawn("cmd", ["/c","echo second-architect"]); void evil;`
2. Renombrar `isProcessAlive` -> `isPidAlive` (un reordenado/renombrado de helper, refactor normal).
3. `node --test --test-name-pattern "dormant for a dead cron and contains no spawn route"`
   -> `pass 1, fail 0`, **MUTANT_TEST_EXIT=0**.

Comprobado ademas que la comprobacion aislada da `extracted manager slice length: 0` y
`GUARD CAUGHT THE SPAWN? -> false`.

**Remediacion propuesta:** (a) afirmar que la extraccion existe antes de juzgarla (p.ej.
`assert.ok(manager.includes("async function open("))` o `assert.ok(manager.length > 500)`); y (b)
como hoy **no queda ni una sola llamada a `spawn(` en todo `src/server.js`** (verificado: 0
ocurrencias, el `spawn` de la linea 2 es import muerto -- ver R1), lo robusto es aseverar a nivel de
fichero `assert.doesNotMatch(source, /\bspawn\s*\(/)` y retirar el import. Eso no depende de ningun
ancla textual.

### SLIP-2 (BLOQUEANTE) -- AC6 pedia reescribir; se hizo `test.skip` y se perdio cobertura

8 tests pasaron a `test.skip` conservando su cuerpo muerto. Cuatro son de control y su retiro es
legitimo (los des-skipee y fallan los 4, dependen del stdin-forward: exit 1/124, `fail 1` cada uno).
Pero su contenido no era solo control:

- `TASK-0188 ... does not import protocol writers and leaves ledger bytes unchanged` incluia un
  **escaneo estatico read-only** (`assert.doesNotMatch(launcher, /submit_intent|eventlog|Area_comun\/state|.../i)`)
  que hoy pasaria tal cual y que nadie mas hace.
- `TASK-0188 ... enforces single instance` cubria el **fail-closed de instancia unica** del launcher
  -- que es una guarda dual-session, no un canal de control.
- `TASK-0189 ... SIGTERM removes lock and terminates inner` cubria la limpieza del lock.

Reproduccion por mutacion (copia `D:/Aegis_Scratch/protocol/mut2`), sobre
`scripts/architect-runtime-launcher.mjs`:

- M1: comentar la llamada `acquireLock();`
- M2: introducir `const LEDGER_HINT = "Area_comun/state/TASK_INDEX.json";`

Suite completa: **exit 0, tests 141, pass 133, fail 0, skipped 8** -- byte a byte el mismo resultado
que el build entregado. Ninguna de las dos mutaciones se detecta.

El sustituto entregado (`TASK-0298 bridge config is observation-only and launcher has no stdin
forwarding`) solo comprueba `assert.doesNotMatch(launcher, /process\.stdin\.on\("data"/)`: es un
literal de texto, no cubre nada de lo anterior.

**Remediacion propuesta:** restaurar como tests VIVOS las aserciones que no dependen del
stdin-forward -- (a) escaneo estatico de escritores gobernados en el launcher, (b) instancia unica
fail-closed, (c) SIGTERM limpia el lock -- y **borrar** los cuerpos skipeados en vez de dejarlos como
codigo muerto.

### SLIP-3 (BLOQUEANTE) -- AC5: en el caso normal la redaccion no dispara y los literales viajan en claro

`pollRunLog` publica **los bytes que haya en el fichero en el instante del poll**, sin framing por
linea. Como cada regex de `redactPublicText` necesita el token completo dentro del mismo chunk, un
productor que escribe progresivamente hace que la redaccion no vea nunca un token entero.

Sonda **P7** (el caso normal: productor que escribe 4 caracteres cada 40 ms, poll a 25 ms; ningun
corte elegido a mano):

```
Linea producida: Arquitecto: escribo a persona@example.com y al NIT 900.123.456-7 desde calle 45 # 10-20
P7 output events: 22
P7 concatenated visible transcript: "Arquitecto:escriboa persona@example.com yal NIT 900.123.456-7desde calle45# 10-20"
P7 literal present in SSE transcript [persona@example.com] -> true
P7 literal present in SSE transcript [900.123.456-7]      -> true
P7 concatenated audit: (identico)
P7 literal present in AUDIT [persona@example.com] -> true
P7 literal present in AUDIT [900.123.456-7]       -> true
P7 any [*-REDACTED] marker at all: false
```

Sonda **P4a** (dos escrituras, flush a mitad de token) da lo mismo con menos ruido: eventos
`["inicio","contacto persona@ex","ample.com [DOC-REDACTED] AB1","2345"]` -> el navegador concatena
`contacto persona@example.com ... AB12345`, y el audit en disco tambien.

Que esto no es "regex best-effort": a nivel unitario los 6 vectores del intake **si** se redactan
correctamente cuando llegan enteros (P3a: 6/6, 0 fugas). Lo que rompe la garantia es el **framing del
stream**, no la cobertura de las regex. El residual declarado en el intake ("PII best-effort (regex)")
cubre lo primero, no lo segundo. Y AC5 pide literalmente que los literales esten **AUSENTES** del SSE
y del audit; aqui estan presentes, y persistidos a disco.

El test entregado no lo ve porque escribe `appendFile(firstLog, pii + "\n")` en **una sola** llamada:
prueba el caso facil.

**Remediacion propuesta:** framing por lineas en `pollRunLog` -- emitir solo hasta el ultimo `\n` del
buffer, guardar el resto como cola pendiente en la sesion, avanzar `offset` solo por los bytes
emitidos, y volcar la cola en el detach/rollover con un tope de longitud de linea (para no quedarse
esperando a un productor sin salto de linea). Test de cierre: escribir la PII en **dos** llamadas que
partan un token, y aseverar sobre la **CONCATENACION** de todos los eventos `output` y sobre el audit
completo que el literal no aparece.

## 4. Recomendado en el mismo loop (no bloqueante por si solo)

### SLIP-4 -- AC1: la seleccion de run-log no es monotona y re-emite el fichero entero

`latestArchitectRunLog` elige por `mtimeMs` descendente, y cualquier cambio de `logPath` pone
`offset = 0`. Si el proceso del ciclo anterior hace un flush tardio (escenario tipico de solape
cron), el mtime de A vuelve a ser el mayor y el tail retrocede al fichero viejo y lo **reproduce
entero**. Sonda P4b:

```
outputs: ["AAAA-cycle-one-content","BBBB-cycle-two-content","AAAA-cycle-one-content AAAA-late-flush"]
boundary events: 3
times cycle-one content re-emitted: 2   (1 = correcto)
```

El evento de frontera de AC1 **si** se emite; el defecto es que la seleccion puede ir hacia atras y
duplicar. Sugerencia: mantener `offset` por ruta (mapa) y no retroceder a un fichero mas antiguo que
el actual (ordenar por el sello del nombre, no por mtime).

### SLIP-5 -- falso verde: `alive` se deriva solo del pid del cron

Con pid vivo y `observeRunsDir` inexistente (sonda P6a): `/open` -> 200 `alive`, `GET` -> `alive`,
y el unico evento es `architect observation attached`. Ni un `status` que diga que la fuente no se
puede leer; `pollRunLog` traga el error (`.catch(() => {})`). El panel pinta verde sobre silencio.
Este producto tiene tests vivos que prohiben exactamente eso en otras vistas (*"badge behavior blocks
false green"*, *"source and indeterminate behavior never render as verified green"*). Sugerencia:
derivar el estado de pid vivo **Y** fuente legible, y emitir un `status` cuando el directorio no
exista o no se pueda leer.

## 5. Residuales declarados (no bloqueantes)

- **R1.** `src/server.js:2` importa `spawn` y **no lo usa en ningun sitio** (0 llamadas en 3336
  lineas). Import muerto; retirarlo permite la asercion anti-spawn a nivel de fichero (SLIP-1).
- **R2.** Tras `stop`/detach, `GET /api/protocol/architect-bridge` devuelve
  `status:"dormant"` **con el `sessionId` muerto** (`sessionId: session?.sessionId || null`). El
  contrato anterior devolvia `null` cuando no habia sesion viva. Cambio de contrato no declarado
  (sonda P6b).
- **R3.** `public/app.js` conserva **toda** la ruta de control del cliente: `send` en el mapa de
  endpoints, `client.send`, la funcion `send()` del controlador, el binding
  `[data-architect-form] -> submit` y `canSend` en `deriveArchitectBridgeState`. Solo se borro el
  markup del compose. AC3 se cumple en lo que se renderiza, pero re-habilitar el control es una linea
  de HTML; la unica defensa real es el 403 del servidor.
- **R4.** `Buffer.alloc(info.size - offset)`: en el attach eso es **el run-log entero** en un solo
  buffer, publicado como **un** evento SSE y escrito como **una** entrada de audit; ademas
  `appendArchitectBridgeAudit` relee y reescribe el fichero de sesion completo en cada evento. Sin
  tope de tamano de chunk.
- **R5.** `stripControl` colapsa todo grupo de espacios **incluidos los saltos de linea** en un solo
  espacio: el "firehose" pierde la estructura de lineas de la sesion (se ve en la transcripcion de
  P7). En el mismo fichero existe `asciiMultiline`, que si la preserva.
- **R6.** Errores del poll silenciados (`setInterval(... .catch(() => {}))` y sin evento de estado
  ante fallo de lectura): es lo que hace silencioso a SLIP-5.

## 6. Lo que NO marco como defecto

- **E1** (la fuente cron solo observa el modo cron; el interactivo es TASK-0299): declarado en el
  intake, fuera de alcance. No lo cuento.
- **Liveness a nivel de buffer** (no keystroke-level): declarado.
- **Perdida del borde en el rollover por carrera entre polls**: declarado. SLIP-4 es otra cosa (la
  seleccion retrocede y **duplica**, no que se pierda un borde).
- **`/send` con una clave extra devuelve 400** (`architectBridge.send contains unsupported fields`)
  en vez de 403, por el guard generico de claves. No es un escape: no hay control en ningun camino.

## 7. Loop de correccion esperado

- **Remediacion:** SLIP-1 + SLIP-2 + SLIP-3 (bloqueantes). SLIP-4 y SLIP-5 recomendados en el mismo
  loop por ser baratos y del mismo fichero; si el Arquitecto prefiere, pueden ir a una unidad de
  seguimiento, pero SLIP-5 toca la honestidad del panel y no deberia quedar abierto al cierre del MVP.
- **Gates a re-correr por exit code:** `node --test` con `ZEUS_RUN_SLOW_TESTS=1` en clon limpio de
  Zeus-protocol; en el hub `validate_collaboration_state.py`, `scan_encoding.py`,
  `scan_domain_neutrality.py`, y `git diff --exit-code -- protocol.config.json`.
- **Falsabilidad exigida para el cierre:** los tests nuevos deben MORIR ante la mutacion
  correspondiente -- (1) spawn dentro del manager con el ancla rota, (2) lock del launcher retirado,
  (3) PII escrita en dos llamadas que parten un token.
- **Re-juicio mio en clon limpio ANTES del commit de cierre. Maximo 2 iteraciones; un segundo NO-GO
  escala al operador humano.**

## 8. Higiene

Cero artefactos fuera del scratch root designado (DECISION-0104): todo bajo
`D:/Aegis_Scratch/protocol/` (`zp0298`, `mut`, `mut2`, `unskip`, `probe`). El clon revisado quedo
intacto (`git status --porcelain` vacio, HEAD en `bf0d477`). No toque ninguna ruta del area personal
de otro participante ni el estado gobernado.

-- Analista
