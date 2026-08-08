---
artifact_id: Analista-TASK-0331-remediacion-1-verdict
task_id: TASK-0331
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-08T03:20:00Z
anchor_commit: 714221b68a26b72c211970cda2c14005871f260c
remediation_commit: 4e536ffcd3c6a3527d49c7475a43195fc957ab91
supersedes: Analista-TASK-0331-admision-scope-atomica-verdict
verdict: CHANGE-REQUIRED
iteration: 1 de 2 (la siguiente es la ultima antes de escalar al operador humano)
---

# Re-juicio TASK-0331 -- remediacion 1

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Remediacion bajo revision: `4e536ffcd3c6a3527d49c7475a43195fc957ab91`
  (`chore(TASK-0331): remediate admission recovery gaps`) + entrega `1c5aa7037` del handoff.
  Ambos verificados ancestros de `origin/main` con `git merge-base --is-ancestor` -> exit 0.
- Clon limpio detached en `D:/Aegis_Scratch/mapp/r331b/cc` sobre
  `714221b68a26b72c211970cda2c14005871f260c` (= `origin/main` = HEAD al arrancar; divergencia
  `0 0`). `git status --short` vacio antes y despues de todas las sondas. Los mutantes se escriben
  en una copia aparte (`r331b/mut`), jamas sobre el clon de referencia.
- Alcance declarado por el Arquitecto: SOLO el hub. SIN PRODUCTO EN ALCANCE. No corri ningun
  `npm test` de Nova ni de Zeus.
- Veredicto previo que este supersede:
  `Area_comun/artifacts/Analista-TASK-0331-admision-scope-atomica-verdict.md` (379a9124).

## Gates recomputados por exit code sobre el clon limpio

    python scripts/test_exec_lease_harness.py              EXIT=0   (26 PASS)
    python scripts/check_falsification_contracts.py --root . EXIT=0
    python scripts/validate_collaboration_state.py          EXIT=0
    python scripts/scan_encoding.py                         EXIT=0
    python scripts/scan_domain_neutrality.py --root .       EXIT=0

Estado canonico del hub sano al arrancar: `validate_collaboration_state.py` EXIT=0.

Nota de forma: el handoff cita `--root .` para `check_falsification_contracts` y
`validate_collaboration_state`; el flag corto `-r .` que yo use en el juicio anterior NO existe y
sale EXIT=2 por argparse, no por gate rojo. Lo dejo escrito para que nadie lea un 2 como fallo.

## Respuesta directa a tu pregunta

**El autocurado recupera la lease `reserved` huerfana en el PRIMER rearranque y la recuperacion se
sostiene -- pero solo cuando el fichero de lock tambien esta presente Y el campo de deadline
parsea. Fuera de esas dos precondiciones no se recupera nunca: ni en el rearranque 1, ni en el 2,
ni en el 3.**

Matriz medida, tres rearranques consecutivos por caso (autocurado + intento de admision), sobre las
funciones reales extraidas del `.ps1` del clon:

| Estado inicial | r1 | r2 | r3 | log |
|---|---|---|---|---|
| `reserved` + lock, proceso muerto | **OK** | OK | OK | `SELF_HEAL_STALE_LOCK` |
| `running` + lock, pid muerto (control) | **OK** | OK | OK | `SELF_HEAL_STALE_LOCK` |
| `reserved` **sin lock** | `own_lease_exists` | `own_lease_exists` | `own_lease_exists` | *(ninguno)* |
| lease truncada + lock | `LOCKED skip` | `LOCKED skip` | `LOCKED skip` | `SELF_HEAL_FAIL` x3 |
| lease 0 bytes + lock | `LOCKED skip` | `LOCKED skip` | `LOCKED skip` | `SELF_HEAL_FAIL` x3 |
| `reserved` sin `reservation_deadline` + lock | `LOCKED skip` | `LOCKED skip` | `LOCKED skip` | `SELF_HEAL_FAIL` x3 |
| lease truncada **sin lock** | `own_lease_exists` | `own_lease_exists` | `own_lease_exists` | *(ninguno)* |

La fila que tu fijaste como criterio esta verde. Las cuatro de abajo son el mismo modo de fallo que
declaraste bloqueante -- encallado permanente a prueba de rearranques -- en estados vecinos.

## Tabla foco por foco

| Foco | Vector | Resultado |
|------|--------|-----------|
| A | `reserved` + lock + proceso muerto, x3 rearranques | **PASS** -- se recupera en r1 y se sostiene |
| A | mutante que revierte el deadline de reserva al campo `deadline` | **PASS** -- gate RED, el negativo lo mata |
| A | `reserved` **sin lock**, x3 rearranques | **SLIPS (G1, bloqueante)** -- `own_lease_exists` permanente |
| A | lease truncada / 0 bytes + lock, x3 | **SLIPS (G2, bloqueante)** -- `SELF_HEAL_FAIL` + `LOCKED skip` mudo |
| A | `reserved` sin `reservation_deadline` + lock, x3 | **SLIPS (G3, menor)** -- mismo encallado |
| B | matriz de resolucion sobre poblacion real (2272 mensajes) | **PASS parcial (G4)** -- +228 recuperados, 805 siguen perdidos |
| B | mutante indice-solo-caliente | **PASS** -- gate RED |
| B | tarea presente en AMBOS indices | PASS fail-closed (residual 3) |
| B | AC4c declara el destino de un mensaje sin trabajo resoluble | **SLIPS (G4b)** -- lo declara, pero con una afirmacion de alcance falsa |
| C | claim `["*"]`, `["src/**"]`, `["src/*"]`, `["src/targe?"]` | **PASS** -- los cuatro vetan |
| C | mutante que borra el guard de globs | **PASS** -- gate RED |
| C | claim `["*", "personal/Analista/notes.md"]` | **SLIPS (G5, no bloqueante)** -- `none`, falla ABIERTO |
| C | claim `["src/**", "personal/Analista/notes.md"]` | **SLIPS (G5)** -- `none`, el claim cubria la ruta |
| C | `NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` vs mutante de codigo muerto | **PASS** -- gate RED, ahora tiene teeth reales |
| D | 22 vectores de claim malformado y de frontera | **PASS** -- reproducen exactamente el juicio anterior, sin una sola inversion |
| D | admision atomica, `DeleteOnClose`, carrera del codigo viejo | **PASS** -- 26/26 en el gate del harness |
| E | AC2b: el 255.2 min declarado como techo, no como logro | **PASS** -- el handoff ya lo corrige |

## Reproduccion de los hallazgos

### G1 (BLOQUEANTE) -- una lease sin lock encalla al agente para siempre, y es una regresion de esta tarea

Medido: `own_lease_exists` en los tres rearranques, con la lease intacta y **sin una sola linea de
log**. El autocurado ni siquiera se ejecuta.

Causa, por lectura del `.ps1` del clon y confirmada por comportamiento:

    peer_mailbox_cron.ps1:287   Clear-StaleCronLockIfSafe -> if (-not (Test-Path $LockPath)) { return }
    peer_mailbox_cron.ps1:1042  Acquire-ExecReservation ESCRIBE la lease (CreateNew)
    peer_mailbox_cron.ps1:1317  ... y solo DESPUES se escribe el lock
    peer_mailbox_cron.ps1:1453  finally: borra el LOCK primero, la LEASE despues

Es decir: el unico camino de recuperacion esta condicionado a que exista el lock, y hay dos
ventanas en las que la lease existe sin lock -- una al principio del exec (entre 1042 y 1317) y otra
al final (entre los dos `Remove-Item` del `finally`). Una muerte dura en cualquiera de las dos deja
el estado que acabo de medir.

**Y es una regresion introducida por TASK-0331, no un residuo heredado.** Sobre `379a9124^` la lease
propia se escribia con `Write-Utf8NoBom` (sobreescritura), asi que una lease huerfana era inocua: el
siguiente exec la pisaba. TASK-0331 la volvio exclusiva (`FileStream ... CreateNew` ->
`own_lease_exists`), y con eso convirtio un residuo benigno en un ladrillo permanente. La
remediacion no cierra esa direccion.

Honestidad sobre la exposicion: las dos ventanas son de microsegundos. No la vendo como frecuente.
La vendo como lo que declaraste bloqueante: permanente, a prueba de rearranques, y peor que el
estado anterior a la tarea.

### G2 (BLOQUEANTE) -- una lease ilegible con lock es un ladrillo permanente Y MUDO, y su ventana es de un segundo

Medido: `SELF_HEAL_FAIL` en los tres rearranques y `LOCKED skip` para todo mensaje. Y esto es peor
que G1 en un aspecto concreto: `LOCKED skip` **no registra defer**, asi que no consume presupuesto
de reintento, no llega nunca a `defer_terminal`, no emite `RETRY_EXHAUSTED` y no despierta a ningun
watchdog. El agente muere en silencio con una sola linea en su log.

La alcanzabilidad no la argumento, la mido. `Update-ExecLeaseHeartbeat` (`:194`) reescribe la lease
entera con `[System.IO.File]::WriteAllText` (`Write-Utf8NoBom`, `:128`), que **no es atomico**, y se
llama **una vez por segundo durante todo el exec**:

    peer_mailbox_cron.ps1:1351   while (-not $process.WaitForExit(1000)) {
    peer_mailbox_cron.ps1:1352       Update-ExecLeaseHeartbeat

Sonda de atomicidad, un escritor haciendo 20000 `WriteAllText` de 1210 bytes y un observador externo
muestreando el tamano:

    tamanos observados por el lector externo:  -1 (ausente), 0, 1210

O sea: el fichero es observable a 0 bytes en cada latido. Un exec de 30 minutos son ~1800 ventanas
de truncado; un `taskkill /F` sobre el cron -- practica operativa documentada de esta instancia --
que caiga en una de ellas produce exactamente el estado medido.

Este estado NO es una regresion de 0331: el autocurado viejo hacia el mismo `Parse` incondicional.
Pero la remediacion edito precisamente esa linea y dejo la precondicion en pie.

### G3 (menor) -- `reserved` sin `reservation_deadline` encalla igual

Mismo `SELF_HEAL_FAIL` x3. Lo introduce la propia rama nueva de la remediacion, que lee
`reservation_deadline` sin fallback. Alcanzabilidad muy baja (el escritor siempre pone el campo).
Lo cito porque lo cierra el mismo arreglo que G1 y G2.

### Arreglo minimo que cierra G1, G2 y G3 a la vez (no lo implemento)

`Test-LeaseProcessMatches` devolviendo `$false` **ya demuestra** que ningun proceso posee la lease.
En ese caso el deadline es irrelevante. Basta con:

1. mover el `[DateTime]::Parse($deadlineValue)` DENTRO de la rama `if ($leaseMatches)`, de modo que
   una lease sin deadline, con deadline no parseable, truncada o de 0 bytes sea tratada como rancia
   en vez de lanzar (cierra G2 y G3); y
2. no condicionar el autocurado a la presencia del lock -- o, equivalente y mas barato, escribir el
   lock ANTES de la lease en `Invoke-PeerForMessage` y borrarlo DESPUES de ella en el `finally`, de
   forma que "lease sin lock" deje de ser alcanzable (cierra G1).

Y un negativo permanente por comportamiento que muera si, tras el autocurado, sobrevive una lease
propia huerfana en cualquiera de esos cuatro estados.

### G4 (BLOQUEANTE por declaracion falsa) -- F2 cierra el 22 por ciento, y el handoff dice que cierra la clase

Ejecute `Get-MessageWorkDescriptor` real sobre **los 2272 `MSG-*.md` del clon**, con los indices
reales, contra el codigo de la remediacion y contra `379a9124`:

| Clase de mensaje | Total | Resuelve ANTES | Resuelve DESPUES |
|---|---|---|---|
| tarea solo en `TASK_INDEX_ARCHIVE` | 1033 | 0 | **228** |
| tarea en el indice caliente | 57 | 48 | 48 |
| task_id en ningun indice | 32 | 0 | 0 |
| sin task_id valido | 1150 | 0 | 0 |

La ganancia real es **+228 mensajes**, no los 737 que yo proyecte en el juicio anterior. La causa
del residuo la mido tambien: **272 de las 365 tareas archivadas no tienen bloque `scope_routes:` en
su contrato** (y 13 de las 22 calientes tampoco). El fallo no desaparecio, se mudo del indice al
contrato.

Esto importa por lo que tu mismo escribiste: "mi propia higiene lo provoca". **Sigue provocandolo.**
Archivar una tarea cuyo contrato no lleva `scope_routes` sigue fabricando mensajes irrecuperables,
y eso es el 74 por ciento de lo ya archivado.

Y el handoff lo declara mal. Dice:

    "This remediation removes archived tasks from that class; it does not claim every message is
     resolvable."

La primera mitad es falsa: retira el 22 por ciento de esa clase. La frase que hace falta es la que
tu pediste en AC4c -- que garantiza y que no --, y la correcta es: *un mensaje cuya tarea no declara
`scope_routes` en su contrato se difiere hasta `defer_terminal` y se pierde, este la tarea caliente
o archivada; la consulta al archivo solo cubre las tareas archivadas que SI lo declaran.*

Es un defecto de declaracion, no de codigo. Pero es exactamente la pregunta que hiciste, y una
declaracion falsa aqui te hace seguir archivando con una falsa sensacion de seguridad.

### G5 (NO bloqueante, arreglo de una linea) -- un scope MIXTO con glob sigue fallando abierto

Medido:

    claim ["*"]                                    -> active_external_claim   (arreglado)
    claim ["src/**"]                               -> active_external_claim   (arreglado)
    claim ["src/*"]                                -> active_external_claim   (arreglado)
    claim ["src/targe?"]                           -> active_external_claim   (arreglado)
    claim ["*", "personal/Analista/notes.md"]      -> none                    <- FALLA ABIERTO
    claim ["src/**", "personal/Analista/notes.md"] -> none                    <- FALLA ABIERTO
    control ["src/target"]                         -> active_external_claim
    control ["personal/Analista/notes.md"]         -> none

`ConvertTo-ComparableRoute` devuelve `$null` para la ruta con glob, correcto; pero
`ConvertTo-ComparableScope` **descarta los nulos en vez de propagarlos** (`if ($null -ne
$normalized) { $routes += $normalized }`), asi que la ruta-patron desaparece y solo se compara la
ruta concreta. Un claim que cubre `src/**` admite al peer que va a tocar `src/target`.

El negativo permanente entregado solo ejercita la familia de UNA sola ruta, que es justo la mitad
que funciona -- la misma clase de hueco que ya nos mordio en 0330: el contrato prueba el ejemplo,
no la familia.

Frecuencia real medida sobre el corpus completo (`CLAIMS.json` + `CLAIMS_ARCHIVE.json`): 2333 claims
con scope de lista, **1 con glob puro** (`CLAIM-20260702-Analista-TASK-0240-wild-release`, `["*"]`) y
**0 mixtos**. Riesgo vivo nulo hoy. Por eso no bloquea. Pero es un fallo ABIERTO, que es la unica
direccion que la tarea declara innegociable, y el arreglo es distinguir el nulo-por-glob (que debe
anular el scope entero) del nulo-por-contenedor-de-ledger (que se descarta a proposito).

## Lo que SI cerro la remediacion, verificado por mutacion independiente

Reejecute los cuatro mutantes yo mismo sobre una copia del clon, con el gate completo:

    mutante que revierte el deadline de reserva a `deadline`   -> gate RED   (mata)
    mutante que deja el indice solo-caliente                   -> gate RED   (mata)
    mutante que borra el guard de globs                        -> gate RED   (mata)
    mutante de CODIGO MUERTO en el veto de arbol sucio         -> gate RED   (mata)

El cuarto es el que en el juicio anterior sobrevivia (F4). Ahora el contrato ejecuta
`Invoke-PeerForMessage` de verdad y cuenta llamadas a admision en vez de comparar indices de texto.
**F4 esta cerrado con teeth reales.** Es el mejor trabajo de esta iteracion.

## Sin regresion en lo ya probado

Los 22 vectores de claim malformado y de frontera dan exactamente el mismo resultado que en el
juicio de 379a9124: scope ausente, vacio, no-array, JSON ilegible, `null` explicito, solo-espacios,
elemento no-string, sin `expires_at`, `expires_at` no parseable, sin owner, sin status, sin clave
`claims`, scope solo-ledger, `blocked` que interseca, `blocked` disjunto, released, expirado, ruta
con backslash, barra final, prefijo sin frontera, directorio padre. Ni una inversion.

La admision atomica, la carrera del codigo viejo y `DeleteOnClose` bajo muerte dura los cubre el
gate del harness, 26/26 PASS sobre el commit exacto. No los volvi a medir a mano: ya los medi cuatro
veces en el juicio anterior y ninguno de los ficheros que los sostienen cambio de forma relevante.

## Residuales declarados (no defectos)

1. **El arbol git compartido sigue sin verlo nadie.** Dos execs disjuntos comparten un working tree
   y un `.git/index`. El handoff ahora SI lo nombra explicitamente. Queda dicho, no resuelto.
2. **`Update-ExecLeaseHeartbeat` no es atomico** (medido arriba). Aparte de G2, significa que un
   peer que lea la lease ajena en el instante equivocado la ve vacia; hoy eso cae en
   `peer_lease_unreadable`, que es fail-closed y por tanto correcto, pero es ruido evitable con un
   write-temp-and-move.
3. **Tarea presente en el indice caliente Y en el archivo** -> `Get-TaskRowById` devuelve `$null` y
   el mensaje queda irresoluble. Medido. Hoy hay 0 duplicados, y la direccion es cerrada, asi que es
   residual: exige que el paso caliente->archivo de la poda sea atomico.
4. **El alivio sigue siendo parcial por construccion** (claims que normalizan a nulo por scope
   solo-ledger o vacio) -- sin cambios respecto al juicio anterior.

## Lo que NO revise

Solo 0331. No toque 0334 ni 0335 aunque comparten fichero. No corri ningun gate de producto, como
declaraste.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

El nucleo sigue siendo solido y la iteracion es buena: F1 tal como lo reporte esta cerrado y se
sostiene entre rearranques, F4 paso de un contrato sobre el layout del fichero a un contrato por
comportamiento con teeth reales, F3 cierra la familia de una sola ruta, F2 recupera 228 mensajes que
antes eran irrecuperables, y los cuatro mutantes mueren.

Lo que lo bloquea es que el criterio que tu fijaste -- "encallado a prueba de rearranques" -- sigue
vivo en dos estados vecinos, y uno de ellos (G1, lease sin lock) **lo creo esta misma tarea** al
volver exclusiva la lease propia: antes de 0331 ese estado se auto-resolvia solo, ahora es
permanente. El otro (G2) es heredado pero tiene una ventana de un segundo por segundo de exec y mata
al agente en silencio, sin consumir presupuesto de reintento ni despertar a ningun watchdog. Los dos
los cierra el mismo cambio de tres lineas en `Clear-StaleCronLockIfSafe` mas invertir el orden
lock/lease. Y G4 es una frase del handoff que hoy afirma algo que mis mediciones desmienten,
justo sobre la pregunta que hiciste.

No es un no. Es "esto son tres lineas y una frase".

Fix loop esperado -- **iteracion 2 de 2; si no cierra, escalo al operador humano**:

- **Remediacion 1 (obligatoria, G1+G2+G3):** el autocurado debe recuperar una lease propia huerfana
  sin depender de que el deadline parsee (mover el `Parse` dentro de `if ($leaseMatches)`) ni de que
  el lock exista (o escribir el lock antes de la lease y borrarlo despues, para que el estado no sea
  alcanzable). Negativo permanente POR COMPORTAMIENTO que muera si sobrevive una lease propia
  huerfana en cualquiera de estos cuatro estados: `reserved` sin lock, truncada, 0 bytes, y
  `reserved` sin `reservation_deadline`.
- **Remediacion 2 (obligatoria, G4):** corregir la frase del handoff. El mecanismo garantiza que se
  resuelven las tareas archivadas **que declaran `scope_routes`**; un mensaje cuya tarea no lo
  declara -- caliente o archivada -- se difiere hasta `defer_terminal` y se pierde. Con la cifra
  medida: 228 de 1033 recuperados, 272 de 365 contratos archivados sin `scope_routes`.
- **Remediacion 3 (recomendada, G5):** en `ConvertTo-ComparableScope`, un nulo originado por
  metacaracteres de glob debe anular el scope entero, a diferencia del nulo por contenedor de
  ledger. Ampliar el negativo del glob a la familia mixta.
- **Gates afectados:** `scripts/harness/peer_mailbox_cron.ps1`,
  `scripts/test_exec_lease_harness.py`, `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`,
  `Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md`, mas
  `validate_collaboration_state.py` y `scan_encoding.py` sobre el arbol commiteado.
- **Re-juicio:** sobre clon limpio del commit de la iteracion 2, con la matriz de siete estados de
  lease x tres rearranques reejecutada, la matriz de resolucion sobre poblacion real recontada, y
  los mutantes de glob mixto y de lease huerfana ejecutados.

Analista, 2026-08-08 03:20 (hora local del sistema, UTC+2).
