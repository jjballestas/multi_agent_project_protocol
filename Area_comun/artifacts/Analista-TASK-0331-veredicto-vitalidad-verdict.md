---
artifact_id: Analista-TASK-0331-veredicto-vitalidad-verdict
task_id: TASK-0331
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-09
local_time: 2026-08-09 14:35 (+02:00)
anchor_commit: bc2efc8add3cf090e816e113345cd2d5ab98bd17
parent_commit: 3d3daf5f
protocol_head_at_review: 5e6cd41c
clean_clone: D:/Aegis_Scratch/protocol/r0331r7/cc
supersedes: Analista-TASK-0331-muertes-por-rama-verdict
scope: hub only (sin producto en alcance)
iteration: r7
verdict: CHANGE-REQUIRED
---

# TASK-0331 r7 -- tu criterio se cumple; la clase sigue abierta en dos coordenadas nuevas

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Tus dos preguntas, medidas y separadas

Las hiciste juntas y tienen respuestas distintas. Las separo porque de eso depende el veredicto.

**1. "Colapsar a una constante cualquiera de las dos funciones del veredicto de vitalidad enrojece
al menos un gate?" -- SI, las dos, en todas las direcciones. PASS sin matices.**

**2. "Sigue habiendo un camino donde el veredicto de vitalidad no lo observa nadie?" -- SI. Dos.
Los dos fallan ABIERTO y los dos pasan los SIETE gates del `verification_cmd`.** Uno mata un
proceso vivo ajeno; el otro convierte un veto incondicional en paso libre.

## Foco A -- tu criterio, literal, sobre produccion

Mutantes de **codigo muerto** sobre `scripts/harness/peer_mailbox_cron.ps1` en el clon limpio:
`return <constante>` insertado justo despues de la linea `param(...)`, cuerpo original intacto
debajo. Arbol restaurado y `git status --porcelain` vacio despues de cada uno.

| # | mutante de produccion | harness | contracts | muere en |
|---|---|---|---|---|
| P1 | `Get-LeaseProcessState -> "live"` | **1** | 0 | `test_orphan_lease_self_heal_matrix...` `:1893` |
| P2 | `Get-LeaseProcessState -> "dead"` | **1** | 0 | idem `:1893` |
| P3 | `Get-LeaseProcessState -> "unknown"` | **1** | 0 | idem `:1897` |
| P4 | `Test-LeaseProcessMatches -> $true` | **1** | 0 | `test_admission_liveness_path...` `:2070` `assert healthy == expected` |
| P5 | `Test-LeaseProcessMatches -> $false` | **1** | 0 | idem `:2070` |

Cinco de cinco mueren. **P4 y P5 son el M5 de r6**: en r6 ese mutante pasaba el `verification_cmd`
entero y convertia la lease de un peer probadamente muerto en `active_peer_lease`. Ya no. Y muere
en la asercion de comportamiento (`healthy == expected`), no en una comprobacion de forma.

La sonda nueva es honesta en el mecanismo: `admission_liveness_path_probe` carga las funciones por
AST y **no las redefine detras** -- que era la causa exacta de las 24 celdas sobre stub -- y observa
`Get-AdditionalWorkSignal` real con `Get-LeaseProcessState` y `Test-LeaseProcessMatches` reales.
`healthy` se calcula sobre `HARNESS_PATH`, es decir sobre produccion: por eso muta produccion y
enrojece, no solo sus propias copias.

**Cuantas posiciones la ejercen ahora.** Una, la nueva. Las siete posiciones stubeadas de
`test_exec_lease_harness.py` (`:802, :845, :883, :939, :972, :1008, :1788`) siguen exactamente donde
estaban. Y el recuento de r6 se me quedo corto: hay **dos posiciones stubeadas mas, en el otro
fichero de la puerta de aceptacion**, `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
(`:596` `return $false`, `:1434` `return $true`, ambas via `provided=("Test-LeaseProcessMatches",)`).
Son **nueve stubs frente a una observacion real**. No lo traigo como reproche de recuento: la de
`:1434` es la causa mecanica del primer bloqueante.

## Foco B -- el PID reusado ya discrimina de verdad

Con el stub era decorativo. Ahora la sonda usa el proceso PowerShell real y le desplaza la hora de
arranque 7 s: la funcion real devuelve `dead`, la identidad no coincide y la senal de admision es
`none`. Fijado en dos sitios independientes -- `expected_process_states` de r6 y
`reused_state`/`reused_matches`/`reused_signal` de la sonda nueva. **PASS.**

Con una salvedad medida, la misma R3 de r6 y sigue viva:

    G2  tolerancia de 6 s en la comparacion de hora     harness 0  contracts 0  retry 0   SOBREVIVE

Las dos sondas fijan **un** desplazamiento (-7 s). Cualquier tolerancia por debajo de 7 s queda sin
atar. Una propiedad se ata por su criterio, no por un punto.

## Foco C -- sin regresion en seis vueltas: PASS, y por construccion

`scripts/harness/peer_mailbox_cron.ps1` es **byte a byte identico** entre el ancla de r6 y la de r7:

    a29e2cea:scripts/harness/peer_mailbox_cron.ps1  ->  dedb572d247824796ef5050179e69338bfca4219
    bc2efc8a:scripts/harness/peer_mailbox_cron.ps1  ->  dedb572d247824796ef5050179e69338bfca4219

La remediacion 6 es **test-only** sobre el fichero que la tarea reescribe. La produccion no puede
haber regresado: es la misma que medi en r6, donde la carrera, la admision atomica con
`DeleteOnClose`, los 17 vectores malformados sin una sola inversion y la convergencia a tres
rearranques quedaron verificados. Confirmado ademas empiricamente: **29/29 PASS** (28 en r6, +1
nueva) y los siete gates en exit 0. Los nombres de todas las vueltas siguen verdes uno a uno.

## Foco D -- TASK-0284 no se toca aqui, pero la particion no aterriza en ningun sitio

Confirmado lo que preguntas: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` **no** lo
toca este commit; el diff son seis ficheros y solo uno de codigo
(`scripts/test_exec_lease_harness.py`, 117 lineas, cero borradas).

Pero la particion, tal y como esta escrita hoy en el ledger, deja mi bloqueante C-nuevo **sin dueno**:

    TASK-0331 (nota de remediacion 6):  "El frente de escritura alcanzable sobre $LockPath queda
                                         fuera de esta remediacion y se particiono hacia TASK-0341"
    TASK-0341 (intake.out_of_scope):    "El contrato de subcadenas de run_mailbox_retry_cases.py,
                                         que va por la via de TASK-0331."

Cada tarea se lo pasa a la otra por escrito. TASK-0341 se creo el 2026-08-08 (`6954f7db`, commit
unico, sin ediciones posteriores), o sea **antes** de mi hallazgo de r6, y su `out_of_scope` nunca
se actualizo para recogerlo. Ninguna otra tarea del indice lo nombra.

Y sigue vivo. Re-medido en el ancla de r7, contra el runner **actual** (que cambio desde r6:
`8d2e8018 -> 29d76fa3`, por otras tareas):

    C3  la MISMA llamada escrita como `$null = Write-ExecLockEvidence ...`   retry = 0   ESCAPA

La evidencia del lock se escribe de verdad por encima de la sonda de residuo y el contrato no lo ve.
Lo senalo por DECISION-0018: no es de esta tarea arreglarlo, pero cerrar 0331 con la particion como
esta redactada deja caer un escape medido.

## BLOQUEANTE 1 -- el guardia de identidad de `Stop-LeaseProcessTree` no lo observa nadie, y su ausencia MATA

`Stop-LeaseProcessTree:233-235` es el segundo consumidor del veredicto de vitalidad y lo unico que
impide que el barrido de arbol mate a la **victima de un reuso de PID**. Lo dije por su nombre en
r6. Sigue sin observarse.

**Mutante G1** (dead-code, conserva el `return $false` original):

    if ($false) {
        return $false
    }

| gate | G1 |
|---|---|
| `test_exec_lease_harness.py` | **0** (29/29) |
| `check_falsification_contracts.py --root .` | **0** |
| `run_mailbox_retry_cases.py` | **0** |
| `validate_collaboration_state.py` / `scan_domain_neutrality.py` / `test_scan_domain_neutrality.py` / `scan_domain_neutrality.ps1` | **0 / 0 / 0 / 0** |
| `scan_encoding.py --root .` | **0** |

Los **siete** gates del `verification_cmd` en verde. Y el efecto en produccion, medido -- arranco yo
un hijo `Start-Sleep 45`, escribo una lease que reclama su pid con la hora de arranque desplazada
7 s (es decir: ese pid ya **no** es el dueno de la lease) y llamo a la funcion real:

    BASELINE : returned=False  victim_alive=True   logs=[]
    G1       : returned=True   victim_alive=False  logs=['TREE_KILL pid=92268 reason=orphan_expired
                                                          message=MSG-victim',
                                                         'TREE_KILL_COMPLETE pid=92268 descendants=1']

**El mutante mata un proceso vivo que no es suyo y lo reporta como `TREE_KILL_COMPLETE`.** Direccion
del fallo: ABIERTA y destructiva. Es la inversion exacta de la regla que gobierna esta tarea -- "el
arreglo no debe convertir la direccion cerrada en abierta".

**Por que es invisible, mecanicamente.** La unica prueba que ejerce el cuerpo de
`Stop-LeaseProcessTree` es `run_complete_tree_kill_case` (`run_mailbox_retry_cases.py:1381`), y lo
extrae asi:

    extract_powershell_function_closure(runner_text, ("Stop-LeaseProcessTree",),
                                        provided=("Write-Log", "Test-LeaseProcessMatches"))

`provided=` significa "no lo cargues, yo te lo doy": y lo que le da (`:1434`) es
`function Test-LeaseProcessMatches { param($Lease) return $true }`. **El unico test que ejerce al
consumidor sustituye el guardia por un `$true` fijo.** Por construccion no puede observarlo. F1 y F2
(colapsar la funcion entera a `$true`/`$false`) SI mueren en ese runner -- pero mueren porque el
runner comprueba si el arbol muere de verdad, no si el guardia existe. La funcion esta observada; el
guardia, no.

## BLOQUEANTE 2 -- el veredicto tiene tres valores y la identidad solo observa dos

`Get-LeaseProcessState` devuelve `live`, `dead` o `unknown` -- las seis salidas que la propia r6 fijo
en `expected_process_states`. La sonda nueva observa `Test-LeaseProcessMatches` sobre `live` y sobre
`dead`. **Sobre `unknown`, nadie.**

**Mutante G3** (una palabra; el guardia deja de exigir identidad y solo excluye la muerte confirmada):

    -    return ((Get-LeaseProcessState -Lease $Lease) -ceq "live")
    +    return ((Get-LeaseProcessState -Lease $Lease) -cne "dead")

Pasa `healthy == expected` intacto, porque en los tres vectores de la sonda (`live`, `dead`,
`dead`-por-reuso) da exactamente el mismo resultado que el original. Y pasa los siete gates:

    harness 0   contracts 0   retry 0   validate 0   neutrality x3 = 0   encoding 0

Efecto en produccion, medido con `Get-AdditionalWorkSignal` real contra una lease de peer con
`state=running`, `process_start_time_utc=""` (estado **indeterminable**) y `work_scope` **disjunto**
del trabajo del mensaje:

    BASELINE : {"state":"unknown", "matches":false, "signal":"peer_lease_unreadable"}
    G3       : {"state":"unknown", "matches":true,  "signal":"none", "detail":"peer=Analista"}

El baseline **veta incondicionalmente** ante la duda -- `peer_lease_unreadable` sale antes de mirar
el scope. El mutante llama "viva" a una lease cuyo dueno no se puede identificar, se salta el guard
`if ($leaseLiveness -ceq "unknown") { return "peer_lease_unreadable" }`, cae al filtro de scope, no
interseca y devuelve **`none`: sin veto**.

Eso es convertir la duda en permiso. Es la clausula que TASK-0331 declara INNEGOCIABLE en AC3 y
extiende a las leases en AC2b ("si no se puede determinar... SIGUE VETANDO, mismo criterio
fail-closed del AC3"), y es la unica garantia de anti-colision que DECISION-0020 pide. Un mutante de
una palabra la invierte y los siete gates lo certifican verde.

Y el mismo mutante, en el otro consumidor, autoriza a `Stop-LeaseProcessTree` a matar el arbol de un
pid cuya identidad no se pudo establecer.

## El experimento de la septima funcion (E1) -- no concluyente, y lo digo

En r6 pedi que la propiedad sobreviviera a que manana aparezca una funcion mas de la familia. Lo
intente: extraje la comparacion de hora a un helper nuevo `Test-LeaseStartTimeMatches` llamado desde
`Get-LeaseProcessState`, primero fiel (E1a) y luego colapsado a `$true` (E1b).

    E1a  helper nuevo, fiel        harness=1   (esperaba verde)
    E1b  el mismo, colapsado       harness=1

Los dos rojos, y **por la misma causa, que no es la que buscaba**: `function_loader` carga funciones
por nombre, el helper nuevo no esta enrolado en ninguna llamada, la sonda lo invoca y PowerShell
falla -- muere en `test_live_unreadable_lease_is_preserved...:1922` (`logs == []`), no en una
asercion del veredicto. **Mi experimento no mide lo que queria medir**, asi que no lo cuento ni a
favor ni en contra. Lo unico que deja establecido es que el cargador falla CERRADO ante una funcion
no enrolada, que es la direccion buena. La pregunta de fondo sigue sin respuesta y no la convierto
en bloqueante.

## La familia completa que SI cierra

Colapse a constante, sobre produccion, cada funcion que produce o consume el veredicto de vitalidad
en el camino del exec. Las seis mueren:

| mutante de produccion | harness | contracts | retry | veredicto |
|---|---|---|---|---|
| `Get-LeaseProcessState` -> live / dead / unknown | 1 | 0 | -- | MUERE |
| `Test-LeaseProcessMatches` -> `$true` / `$false` | 1 | 0 | -- | MUERE |
| `Stop-LeaseProcessTree` -> `$true` | 0 | 0 | **1** | MUERE |
| `Stop-LeaseProcessTree` -> `$false` | 0 | 0 | **1** | MUERE |
| `Get-ProcessStartTimeUtc` -> `""` | 0 | 0 | **1** | MUERE |
| `Get-AdditionalWorkSignal` -> `"none"` | **1** | 0 | 1 | MUERE |
| `Get-AdditionalWorkSignal` -> `"active_peer_lease"` | **1** | 0 | 1 | MUERE |
| `Clear-StaleCronLockIfSafe` -> `return` | **1** | 0 | 1 | MUERE |

Ninguna funcion de la familia sobrevive al colapso. Lo que sobrevive no es una funcion sin observar:
son **dos consumos** sin observar dentro de funciones observadas (G1) y **un valor del veredicto**
sin observar (G3). El criterio que fije en r6 -- colapsar la funcion -- resulta ser necesario pero
no suficiente, y eso es tanto un limite de mi criterio como del arreglo. Lo digo asi de claro para
que la remediacion no persiga otra vez la forma que yo nombre.

## Reproduccion

Clon limpio `git clone --no-hardlinks D:/Agentes/multi_agent_project_protocol cc`,
`git checkout bc2efc8a`, arbol verificado limpio antes y despues de cada mutacion.

    python scripts/test_exec_lease_harness.py                        -> 0   (29/29 PASS)
    python scripts/check_falsification_contracts.py --root .         -> 0
    python scripts/validate_collaboration_state.py --root .          -> 0
    python scripts/scan_domain_neutrality.py --root .                -> 0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0
    python scripts/test_scan_domain_neutrality.py                    -> 0
    powershell scripts/scan_domain_neutrality.ps1 -Root .            -> 0
    python scripts/scan_encoding.py --root .                         -> 0

Inventario de contratos, forma de CI (`--workflow ... --inventory`) -> exit 0:

    FALSIFICATION_INVENTORY permanent_negatives=69 declared=69 missing=0
    DECLARED NEG-HARNESS-ADMISSION-LIVENESS-PRODUCTION-PATH boundaries=4
             runner=scripts/test_exec_lease_harness.py

y ese runner lo ejecuta CI (`validate.yml:273`). Los cinco lectores de CI del fichero siguen dentro
del `verification_cmd`.

Estado canonico del hub al revisar: `validate_collaboration_state.py` exit 0 sobre `5e6cd41c`;
`runtime/protocol_replay.py --check-drift` -> `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8375`.

Sonda de efecto en produccion (los dos supervivientes): las dos corridas de arriba, con
`Get-AdditionalWorkSignal` / `Stop-LeaseProcessTree` reales y sin ningun stub en la posicion del
guardia bajo prueba.

## Residuales declarados

- **R1** Nueve posiciones stubean `Test-LeaseProcessMatches` (siete en `test_exec_lease_harness.py`,
  dos en `run_mailbox_retry_cases.py` via `provided=`) frente a una que la ejerce. Las 24 celdas de
  la tabla normativa siguen sobre stub: el fichero de la sonda es **puramente aditivo** respecto a
  r6 (cero lineas borradas), asi que mi medida de r6 -- 0 de 24 celdas cambian al colapsar -- sigue
  vigente sin recomprobarla. La entrega lo declara en prosa; no lo bloqueo.
- **R2 (G2)** Tolerancia por debajo de 7 s en la comparacion de hora, sin atar. Era R3 en r6.
- **R3** El frente de escritura sobre `$LockPath` (C3) sigue escapando y **ninguna tarea lo reclama**
  hoy por escrito. Ver Foco D.
- **R4** No re-corri `test_attested_instancing.py`: rojo en la entrega y en el padre desde r5, fuera
  de CI y fuera del AC. Deuda ajena, sin cambio.
- **R5** El R-FLAKE de r6 (`run_mailbox_retry_cases.py`, caso con plazo duro de 12 s) **no reaparecio**
  en esta vuelta: 11 corridas del runner (1 baseline + 10 sobre mutantes), veredicto determinista en
  todas. Lo bajo de "vigilado" a "no reproducido", sin retirarlo.
- **R6** Sin producto en alcance, por instruccion del encargo.

## Veredicto

**CHANGE-REQUIRED.**

Lo cerrado, entero, porque es lo mayor: **el M5 de r6 esta muerto**; las dos funciones del veredicto
enrojecen al colapsarlas, en todas las direcciones, por comportamiento y sobre produccion; la sonda
no se redefine detras del cargador, que era la causa raiz de las 24 celdas; el PID reusado
discrimina de verdad; el contrato nuevo esta declarado, inventariado y su runner lo ejecuta CI; la
produccion es byte-identica a la de r6 y no hay regresion (29/29, siete gates verdes); y la entrega
declara sus propios limites sin adornarlos, incluida la particion.

Lo que impide cerrar son dos consumos del mismo veredicto que **ningun gate observa** y que fallan
ABIERTO:

**G1.** El guardia de identidad de `Stop-LeaseProcessTree` -- cegarlo mata un proceso vivo ajeno
(`victim_alive=True -> False`) y lo reporta como exito, con los siete gates en verde. El unico test
que ejerce esa funcion sustituye el guardia por `return $true`.

**G3.** `Test-LeaseProcessMatches` solo esta observada sobre `live` y `dead`. Sobre `unknown` --
tercer valor del mismo veredicto -- una palabra (`-ceq "live"` -> `-cne "dead"`) convierte un veto
incondicional en `none`: la duda deja de vetar. Siete gates en verde.

**Como quiero que se falsee la remediacion, sin nombrar la forma** (nombrar la forma es lo que ha
producido siete vueltas de esta clase):

- **Todo consumo del veredicto de vitalidad debe quedar observado sin sustituir el productor en su
  propia posicion.** El criterio de aceptacion que aplicare: para cada punto del codigo de produccion
  que decida algo a partir de ese veredicto, neutralizar ESE punto -- no la funcion entera -- debe
  enrojecer al menos un gate. Mis mutantes de aceptacion seran G1 y G3 exactamente como estan escritos
  arriba. Si la remediacion los mata pero aparece un tercer consumo sin observar, el patron no se ha
  cerrado.
- **El veredicto tiene tres valores y los tres deciden.** Cualquier observacion que solo cubra dos de
  ellos deja la mitad de la ambiguedad sin atar; `unknown` es precisamente el valor donde vive la
  regla fail-closed.
- **G2** basta con declararlo o con atar la comparacion por su criterio en vez de por un punto.

**Bucle de arreglo.** Ya agote el presupuesto que declare en r5 y confirme en r6 (2 iteraciones), y
la remediacion 6 SI cerro el bloqueante por el que lo declare. Por eso no lo doy por incumplido:
**recomiendo elevar la decision al operador humano** antes de abrir una octava vuelta, con dos
direcciones sobre la mesa:

- **(a) Particionar.** Cerrar TASK-0331 por sus AC -- que se cumplen -- y abrir una tarea nueva,
  con dueno explicito, para "todo consumo del veredicto observado + `unknown` con dientes", llevandose
  ademas el C3 huerfano del Foco D. Es mi recomendacion: la tarea original (el guard serializaba a los
  dos agentes) esta resuelta hace vueltas, y lo que queda es una clase distinta.
- **(b) Octava vuelta** sobre 0331 con G1/G3 como criterio de aceptacion.

Si se elige (a), pido que la particion se escriba en el ledger de las **dos** tareas en el mismo paso:
lo del Foco D demuestra que una particion declarada solo en un mensaje se evapora.

Gates exigidos para el re-juicio, en clon limpio y por codigo de salida: los siete del
`verification_cmd`, mas `scan_encoding.py --root .`, mas `protocol_replay.py --check-drift` limpio.

-- Analista
