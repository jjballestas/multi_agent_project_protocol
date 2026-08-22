# Veredicto Analista -- TASK-0408 r2 (6eb491f5)

**La conjuncion cierra por los dos lados y el presupuesto vuelve a tres.** Los tres puntos de mi
CHANGE-REQUIRED de r1 estan entregados y los verifique por comportamiento, no por lectura: la
supresion exige ahora `status -eq "active"`, la sonda ve por fin la mitad que fallaba y sus dos
mutantes mueren por asercion de COMPORTAMIENTO (no por la guarda de conteo de cadena), y la familia
completa de `Test-ExecRetryExhausted` volvio a ser identica a la de antes de la tarea. Encontre un
mutante nuevo que sobrevive, pero no toca ninguno de los tres puntos ni lo introdujo esta entrega:
lo declaro como residuo con su reproduccion.

- **Recomendacion de cierre: OK-CLOSABLE.**
- Reviewer: Analista. Fecha del juicio: 2026-08-22, 07:05 hora local (reloj de la maquina).
- Encargo: `MSG-20260822-Arquitecto-to-Analista-REVIEW-TASK-0408-r2` (vehiculo TASK-0420).

## Ancla canonica

| Cosa | Valor |
|---|---|
| Commit bajo juicio | `6eb491f525c0a16ad2091f73755dc6a2fb4a452d` (Codex, 2026-08-22 01:55:46 +0200) |
| Ancla de r1 (version anterior) | `d8a7ceb7d84627927353ceb5772ed3f2dabd4546` |
| Ancla del A/B pre-0408 | `dbb9294ff29d3e00d3eb20018a44495a4e00a8c6` |
| `origin/main` al arrancar el juicio | `98f45c006e8f6e604ebd124ddb4841dacca0a6a9` |
| Clon limpio del juicio | `git clone -s` a `D:/Aegis_Scratch/protocol/an0408r2`, `git checkout 6eb491f5`, arbol limpio |
| Clon limpio de mutacion | `D:/Aegis_Scratch/protocol/an0408r2m`, mismo commit, restaurado y verificado limpio tras cada mutante |

**El ancla sigue vigente**, comprobado y no supuesto: `git diff --stat 6eb491f5 origin/main --
scripts/harness/peer_mailbox_cron.ps1 scripts/test_exec_lease_harness.py` sale VACIO. Los cinco
commits posteriores no tocan ninguno de los dos ficheros bajo juicio.

Todo numero de este veredicto se midio en clon limpio. Las tres versiones de produccion se
materializaron con `git show <commit>:scripts/harness/peer_mailbox_cron.ps1`, nunca desde el arbol
caliente. Sonda propia con extraccion por AST (`[Parser]::ParseFile` + `FunctionDefinitionAst` +
`Invoke-Expression`), no el runner del maker, salvo donde digo explicitamente que corri la propiedad
enfocada del maker.

## Puertas (clon limpio, 6eb491f5) -- comando, salida y NUMERO DE CORRIDAS

| Puerta | Comando | Corridas | Exit / salida |
|---|---|---|---|
| Estado colaborativo | `python scripts/validate_collaboration_state.py --root .` | 2 | 0, 0 -- `OK: collaboration state is valid.` |
| Drift runtime | `protocol_state_drift(Path("."))` de `runtime/protocol_replay.py` | 2 | `has_drift=False up_to_seq=10103 entries=0` en las dos |
| Encoding | `python scripts/scan_encoding.py --root .` | 2 | 0, 0 -- `OK: encoding scan is clean.` |
| Neutralidad Python | `python scripts/scan_domain_neutrality.py --root .` | 2 | 0, 0 |
| Neutralidad PowerShell | `pwsh -File scripts/scan_domain_neutrality.ps1` | 2 | 0, 0 -- 141 s y 147 s cronometrados |
| Propiedad enfocada | `test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant` | 2 | 0, 0 (codigo de salida REAL, sin tuberia intermedia) |

Dos precisiones sobre esta tabla, porque un cardinal publicado se re-deriva o no se publica:

1. **La neutralidad PowerShell tardo 141 s y 147 s.** La segunda corrida seguia en marcha mientras
   redactaba y cerro en verde antes de emitir; cito las dos con su cronometro. El maker declaro no
   haber podido correr esta puerta: la discrepancia es de entorno, no del entregable, igual que en r1.
2. **La suite ancha `test_exec_lease_harness.py` esta EXCLUIDA por declaracion, no omitida por
   comodidad.** En r1 medi que su conjunto de fallos varia entre corridas sobre el MISMO commit
   (`failed=4` en una, `failed=3` en la siguiente, con caidos distintos), porque
   `test_exec_lease_harness.py:329` fija una ruta de scratch absoluta y compartida. No la corri aqui
   y **no reclamo ningun resultado suyo**. El maker declaro lo mismo en su handoff; coincidimos.

El validador emite el warning `unverifiable=9432` en el limite de verificacion de auth de eventos.
Preexiste a esta entrega, ya lo declare en r1 y no lo imputo.

## Punto 1 -- la supresion exige `active`, no "distinto de released": PASA

Produccion en `scripts/harness/peer_mailbox_cron.ps1:1321`:

    if ([string]$_.task_id -ne [string]$task.id -or [string]$_.status -ne "active") { return $false }

El liston es mi propia matriz de r1. La amplie de 15 a **18 poblaciones** (anadi estado AUSENTE,
fecha-sola futura y claim de OTRA tarea) y la corri sobre las TRES versiones de produccion, dos
corridas cada una. Alertas por celda:

| Poblacion del claim | OLD `dbb9294f` | r1 `d8a7ceb7` | **r2 `6eb491f5`** | Esperado |
|---|---|---|---|---|
| sin claims | 1 | 1 | 1 | ALERTA |
| `active` + futuro | 0 | 0 | 0 | suprime |
| `active` + pasado | 0 | 1 | 1 | ALERTA (el arreglo de r1) |
| `active` sin campo `expires_at` | 0 | 1 | 1 | ALERTA |
| `active` + `"not-a-date"` | 0 | 1 | 1 | ALERTA |
| `active` + cadena vacia | 0 | 1 | 1 | ALERTA |
| `active` + `null` JSON | 0 | 1 | 1 | ALERTA |
| `active` + `12345` numerico | 0 | 1 | 1 | ALERTA |
| `active` + `"2026-08-18"` (fecha sola, pasada) | 0 | 1 | 1 | ALERTA |
| `active` + `"2999-01-01"` (fecha sola, futura) | 0 | 0 | 0 | suprime |
| `released` + futuro | 1 | 1 | 1 | ALERTA |
| `blocked` + pasado | 1 | 1 | 1 | ALERTA |
| **`blocked` + futuro** | 1 | **0** | **1** | **ALERTA -- regresion de r1 CERRADA** |
| **estado basura `"zzz"` + futuro** | 1 | **0** | **1** | **ALERTA -- regresion de r1 CERRADA** |
| **campo `status` AUSENTE + futuro** | 1 | **0** | **1** | **ALERTA -- poblacion nueva, tambien cerrada** |
| `"ACTIVE"` + futuro | 0 | 0 | 0 | suprime (caja) |
| `"RELEASED"` + futuro | 1 | 1 | 1 | ALERTA (caja) |
| claim de OTRA tarea, `active` + futuro | 1 | 1 | 1 | ALERTA |

Las dos filas que enrojecian en r1 alertan. La tercera -- `status` ausente, que r1 no probo -- cae
del mismo lado sin que nadie tuviera que pedirlo.

### La propiedad que hace fuerte al punto 1: DOMINANCIA, medida y no razonada

En las 18 poblaciones **no existe una sola celda donde OLD alerte y r2 calle**. El conjunto de
alertas de r2 contiene al de OLD y le anade seis. Es decir: r2 no puede ser mas silencioso que el
codigo pre-0408 en ninguna poblacion que sepa construir. Esa es exactamente la garantia que r1 no
tenia, y es la forma correcta de comprobar que un arreglo que endurece una mitad no ablando la otra.

### La ventana fechada de r1, sobre las FILAS REALES del registro

No la reconstrui sintetica. Tome las dos filas reales que sigo teniendo hoy en
`Area_comun/state/CLAIMS.json` de `6eb491f5` -- `CLAIM-20260703-Codex-TASK-0230-route-correction` y
su hermana `-route-release-helper`, ambas `status: blocked` -- y las puse en la mitad FUTURA de su
propia ventana (`expires_at` al futuro), con TASK-0230 `in_progress` owner Codex:

    run1/OLD_dbb9294f   alerts=1 keys=[stalled_task|TASK-0230]
    run1/R1_d8a7ceb7    alerts=0 keys=[]
    run1/NEW_6eb491f5   alerts=1 keys=[stalled_task|TASK-0230]
    run2/OLD_dbb9294f   alerts=1 keys=[stalled_task|TASK-0230]
    run2/R1_d8a7ceb7    alerts=0 keys=[]
    run2/NEW_6eb491f5   alerts=1 keys=[stalled_task|TASK-0230]

Las quince horas de silencio que documente en r1 dejan de existir en r2. Dos corridas.

### Y el defecto ORIGINAL sigue cerrado (corte 1 de r1, repetido)

A/B sobre el estado canonico real de `dbb9294f` (TASK-0414 `in_progress` owner Codex, con sus DOS
claims `active` y VENCIDOS), 73 ficheros de tarea materializados y envejecidos, misma raiz para las
tres versiones:

    run1: OLD_dbb9294f alerts=0 | R1_d8a7ceb7 alerts=1 [stalled_task|TASK-0414] | NEW_6eb491f5 alerts=1 [stalled_task|TASK-0414]
    run2: OLD_dbb9294f alerts=0 | R1_d8a7ceb7 alerts=1 [stalled_task|TASK-0414] | NEW_6eb491f5 alerts=1 [stalled_task|TASK-0414]

r2 conserva lo que r1 gano. Dos corridas. **Punto 1: PASA.**

## Punto 2 -- la sonda ve la mitad que fallaba y los dos mutantes MUEREN: PASA

`obligation_alert_probe` (`scripts/test_exec_lease_harness.py:1547-1548`) construye ahora la
poblacion `non_active`: `status: "blocked"` con `expires_at: "2999-01-01T00:00:00Z"`. Es decir,
estado distinto de `active` y distinto de `released`, con expiracion FUTURA -- la poblacion exacta
que el encargo pedia. La propiedad la asierta junto a las otras dos:

    assert (current["old_stalled_count"], expired["old_stalled_count"], non_active["old_stalled_count"]) == (0, 1, 1)

Corri la propiedad enfocada del maker contra SEIS versiones de produccion en el clon de mutacion,
restaurando el fichero y verificando `git status --short` vacio despues de cada una:

| Mutante de PRODUCCION | Efecto medido con mi sonda | Puerta del maker | Muere por |
|---|---|---|---|
| **Mu1: borrar la clausula de estado entera** (`-ne "active"` -> `$false`) | `blocked`+fut pasa de ALERTA a silencio | **exit 1 -- MUERE** | linea 2134, tupla de poblaciones |
| **Mu2: el defecto de r1** (`-ne "active"` -> `-eq "released"`) | `blocked`+fut pasa de ALERTA a silencio | **exit 1 -- MUERE** | linea 2134, tupla de poblaciones |
| Mu3: laxo (`-notin @("active","blocked")`) | `blocked`+fut pasa a silencio | exit 1 -- MUERE | linea 2134 |
| Mu5: borrar la clausula de expiracion (`return $true`) | `active`+pasado pasa a silencio | exit 1 -- MUERE | linea 2134 |
| Mu6: re-anadir la clausula `exit=-1` | `exit=-1` agota en el intento 1 | exit 1 -- MUERE | linea 2127, `minus_one_exhausted is False` |
| Mu4: borrar la clausula `task_id` | claim de OTRA tarea suprime | **exit 0 -- SOBREVIVE** | ver residuo 1 |

**Los dos mutantes que el encargo exige matar mueren.** Y mueren por la razon correcta, que es lo
que fui a comprobar en vez de conformarme con el exit 1: leyendo el `traceback`, los dos caen en la
**linea 2134**, que es la asercion de COMPORTAMIENTO sobre las tres poblaciones -- no en la guarda
`assert source.count(status_predicate) == 1` de la linea 2149, que habria sido una muerte
tautologica por desaparicion de la cadena. La distincion importa: una puerta que mata sus mutantes
por conteo de texto esta verde por construccion. Esta los mata por conducta.

El 2x2 tambien cierra en la direccion positiva: con produccion SANA la sonda da `non_active = 1` y
los mutantes dan `0`. Direccion medida en ambas versiones, no supuesta.

**Punto 2: PASA.**

## Punto 3 -- el presupuesto de la clase `exit=-1` vuelve a TRES: PASA

Produccion en `scripts/harness/peer_mailbox_cron.ps1:1301-1304`:

    function Test-ExecRetryExhausted {
        param([int]$ExitCode, [string]$Outcome, [int]$Attempt)
        return ($Attempt -ge $MaxTransientRetries)
    }

No lo tomo de la palabra del maker ni de la del Arquitecto. Familia completa medida sobre la funcion
de produccion extraida por AST, con `$MaxTransientRetries = 3`, r1 contra r2:

| Caso | r1 `d8a7ceb7` | **r2 `6eb491f5`** |
|---|---|---|
| `exit=-1 outcome=transient attempt=1` | **True** (agotado en el primer intento) | **False** |
| `exit=-1 outcome=transient attempt=2` | **True** | **False** |
| `exit=-1 outcome=transient attempt=3` | True | True |
| `exit=-1 outcome=unconfirmed attempt=1` | False | False |
| `exit=-1 outcome=definitive attempt=1` | False | False |
| `exit=0 outcome=transient attempt=1` | False | False |
| `exit=1 outcome=transient attempt=1` | False | False |
| `exit=1 outcome=transient attempt=3` | True | True |
| `exit=255 outcome=transient attempt=1` | False | False |
| `exit=-2 outcome=transient attempt=1` | False | False |

La clase `exit=-1` -- que en r1 medi que es la que deja `Process.Kill()` en esta plataforma, o sea
TODO exec que mata el arnes por techo o post-entrega -- recupera sus tres intentos. El colateral que
me preocupaba (el exec que SI escribio en el ledger y murio antes de imprimir su `OUTCOME`) deja de
existir: ya no pierde dos vidas.

### La comprobacion que faltaba: contra QUE linea de base se "restaura"

`Test-ExecRetryExhausted` **no existia en `dbb9294f`**: la introdujo esta misma tarea. Asi que
"volver a tres" no se puede verificar comparando la funcion contra si misma. Fui a la expresion que
la funcion sustituyo, `dbb9294f:1699`:

    $exhausted = $attempt -ge $MaxTransientRetries

Y a su nuevo punto de llamada, `6eb491f5:1709`:

    $exhausted = Test-ExecRetryExhausted -ExitCode $process.ExitCode -Outcome $outcome -Attempt $attempt

El cuerpo de r2 es literalmente esa misma expresion. La refactorizacion es **preservadora de
comportamiento en las diez celdas de la familia**, incluidos los parametros `$ExitCode` y `$Outcome`
que la funcion ahora recibe y **no usa**. El `out_of_scope` de TASK-0408 -- "NO se toca el
presupuesto de reintentos" -- vuelve a estar honrado. **HALLAZGO B de r1: CERRADO.**

Ademas el punto queda **atado por una puerta**, no solo declarado: el mutante Mu6, que re-anade la
clausula `exit=-1`, muere en la linea 2127. Un futuro que reintroduzca el atajo se estrella contra
la propiedad enfocada.

**Punto 3: PASA.**

## Tabla vector-por-vector

| Vector del encargo | Veredicto | Evidencia |
|---|---|---|
| (1) supresion exige `status -eq "active"` | **PASA** | matriz 18x3x2; dominancia sin excepcion; filas reales de TASK-0230 x2 |
| (1b) las dos filas que enrojecian: `blocked`+fut y basura+fut | **PASA** | 1 / 1 en r2 frente a 0 / 0 en r1, dos corridas |
| (1c) el defecto original de r1 sigue cerrado | **PASA** | A/B real de `dbb9294f`, TASK-0414: OLD 0, r2 1, dos corridas |
| (2) `obligation_alert_probe` incluye la poblacion no-`active` con expiracion futura | **PASA** | `non_active` = `blocked` + `2999-01-01`, asertada `== 1` |
| (2b) muere el mutante "borrar la clausula de estado entera" | **PASA** | Mu1 exit 1, linea 2134 (comportamiento) |
| (2c) muere el mutante "exigir active" invertido (el defecto de r1) | **PASA** | Mu2 exit 1, linea 2134 (comportamiento) |
| (3) presupuesto de `exit=-1` de vuelta a TRES | **PASA** | familia de 10 casos; identidad con `dbb9294f:1699`; Mu6 muere |
| -- | **SLIP declarado** | Mu4 (clausula `task_id`) sobrevive: residuo 1 |
| -- | **SLIP declarado** | Mu7 (presupuesto inflado) sobrevive: residuo 5 |

## Residuos declarados (ninguno bloqueante)

**1. NUEVO -- la sonda es ciega a la mitad `task_id` de la conjuncion.** Mutante Mu4: borrar
`[string]$_.task_id -ne [string]$task.id -or ` del predicado. La propiedad enfocada le da **exit 0:
SOBREVIVE**. Medido con mi sonda, poblacion "claim de OTRA tarea, `active` + futuro", dos corridas:

    NEW_6eb491f5            othertask-active+fut  alerts=1
    Mu4_drop_taskid_clause  othertask-active+fut  alerts=0

Con Mu4, un unico claim activo sobre cualquier tarea apagaria la alerta de TODAS. No lo imputo a
esta entrega: la clausula esta intacta desde `dbb9294f` y ni r1 ni r2 la tocan, y no forma parte de
los tres puntos que se me mandaron refutar. Lo declaro porque es la misma forma de defecto que el
HALLAZGO C de r1 -- una mitad de la conjuncion sin ningun test que la mire -- y porque el arreglo es
barato: una poblacion mas en `obligation_alert_probe` con `task_id` distinto de `TASK-test`.

**2. NUEVO -- el presupuesto no esta anclado por arriba.** Mutante Mu7:
`($Attempt -ge $MaxTransientRetries)` -> `($Attempt -ge ($MaxTransientRetries + 5))`. Exit 0:
**SOBREVIVE**. La propiedad asierta que `exit=-1` y `exit=1` NO estan agotados en el intento 1, pero
no asierta que ALGO se agote en el intento 3. Un mutante que infle el presupuesto pasa la puerta.
Direccion contraria al defecto de r1 (agota de mas), asi que no bloquea; una asercion mas lo cierra.

**3. CARRY de r1, sin cambios -- ambito ambiente.** `Test-ExecRetryExhausted` lee
`$MaxTransientRetries` del ambito ambiente, no de un parametro. Medido con la variable FUERA de
ambito:

    NO-SCOPE exit=0  outcome=transient attempt=1 -> exhausted=True
    NO-SCOPE exit=1  outcome=transient attempt=1 -> exhausted=True
    NO-SCOPE exit=-1 outcome=transient attempt=1 -> exhausted=True

Todo se agota en el primer intento, en silencio. Hoy no hay defecto vivo (el parametro del script,
linea 19, esta en ambito), pero r2 convierte esta funcion en **el unico sitio donde se calcula el
presupuesto** del camino de la linea 1709: si algun dia se mueve a un modulo o a un `job` scope,
falla-abierto sin ruido. La sonda del maker tiene que inyectar `$MaxTransientRetries = 3` a mano, que
es la senal de humo.

**4. CARRY de r1, sin cambios -- cultura del proceso.** `[DateTimeOffset]::TryParse` usa la cultura
del proceso: un `expires_at` sin hora se lee como medianoche LOCAL. Medido: `active + "2999-01-01"`
suprime; `active + "2026-08-18"` alerta. Conservador (alerta de mas), por eso no bloquea.

**5. CARRY de r1, sin cambios -- la comparacion de estado es insensible a la CAJA.** `"ACTIVE"` +
futuro suprime en las tres versiones. Consistente entre viejo y nuevo, sin cambio de comportamiento.
Lo re-declaro con una advertencia que en r1 no hice: **si alguna vez se escribe un gemelo Python de
este predicado, un `set` de Python y un `-eq` de PowerShell daran veredictos OPUESTOS sobre
`"ACTIVE"`.** Es la trampa de paridad por caja; conviene fijar la normalizacion antes de que exista
el gemelo.

**6. CARRY de r1, sin cambios -- `test_exec_lease_harness.py:329`** fija una ruta de scratch absoluta
y compartida, no derivada del clon ni del proceso. Es la causa medida de que la suite ancha no sea
hoy un gate discriminante. No es de esta entrega y sigue mereciendo tarea propia.

**7. `unverifiable=9432`** en el limite de verificacion de auth de eventos del validador. Preexiste.

## Veredicto

**OK-CLOSABLE.** Los tres puntos de mi CHANGE-REQUIRED estan cerrados y verificados por
comportamiento en clon limpio: la conjuncion exige `active` y no hay poblacion donde r2 calle y el
codigo pre-0408 alertara; la sonda ve por fin la mitad que fallaba y sus dos mutantes mueren por
asercion de conducta, no por conteo de cadena; y el presupuesto de reintentos es de nuevo
identico al de `dbb9294f`, con un mutante que impide reintroducir el atajo. No queda ningun bloqueo.

Los dos mutantes supervivientes que encontre (residuos 1 y 2) son huecos de cobertura sobre codigo
que esta entrega no toco y en direcciones que no reabren el defecto de la tarea. Los declaro para que
no queden invisibles, no para retener el cierre.

Como no emito CHANGE-REQUIRED, no abro bucle de arreglo: el maker no tiene remediacion pendiente por
mi parte y el cierre es decision del Arquitecto.

## Reproducibilidad

Cada puerta lleva su numero de corridas en la tabla de arriba, y la unica que dio UNA corrida esta
declarada como tal en vez de citada como verde doble. La suite ancha esta excluida por declaracion
con su medicion de r1, no omitida. Toda la instrumentacion (sondas por AST, matriz de poblaciones,
bateria de siete mutantes, estados reales materializados desde `git show`) vive en
`D:/Aegis_Scratch/protocol/an0408r2_probe/` y los dos clones en
`D:/Aegis_Scratch/protocol/an0408r2` y `.../an0408r2m`, dejados limpios.

-- Analista
