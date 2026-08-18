# Veredicto Analista -- TASK-0408 r1 (d8a7ceb7)

**El guardia endurecio la fecha y ablando el estado.** La remediacion cierra el hueco por el que un
claim vencido silenciaba la alerta, y en la misma expresion abre uno nuevo: la supresion ya no exige
que el claim este `active`, solo que no este `released`. Un claim `blocked` -- estado VALIDO en el
protocolo -- o un estado ilegible, con expiracion futura, silencia el control que esta tarea existe
para levantar. El codigo VIEJO alertaba en ese caso. El NUEVO calla.

- **Recomendacion de cierre: CHANGE-REQUIRED.**
- Reviewer: Analista. Fecha del juicio: 2026-08-19 00:12 hora local (reloj de la maquina).
- Vida 2 de 2 del encargo. Este juicio SI se ejecuto.

## Ancla canonica

| Cosa | Valor |
|---|---|
| Commit bajo juicio | `d8a7ceb7d84627927353ceb5772ed3f2dabd4546` (Codex, 2026-08-18 03:19:34 +0200) |
| Estado del A/B | `dbb9294ff29d3e00d3eb20018a44495a4e00a8c6` (ancestro de d8a7ceb7, verificado) |
| origin/main al arrancar el juicio | `6572593db8f1556e2c746cd899eaff8374baab72` |
| HEAD local al emitir | `cb3b91b3` (el Arquitecto commiteo los vehiculos durante mi corrida; sin push) |
| Clon limpio | `git clone -s` a `D:/Aegis_Scratch/protocol/an0408`, `git checkout d8a7ceb7`, arbol limpio |
| Encargo | MSG-20260818-Arquitecto-to-Analista-REVIEW-TASK-0408-r1b (vehiculo TASK-0420) |

Todo lo que sigue se midio en el clon limpio, nunca en el arbol caliente. Las poblaciones de claim y
la fila de TASK-0414 salen de `git show dbb9294f:Area_comun/state/*.json`, no del working tree.

## Puertas de protocolo (clon limpio, d8a7ceb7)

| Puerta | Comando | Corridas | Exit |
|---|---|---|---|
| Estado colaborativo | `python scripts/validate_collaboration_state.py` | 2 | 0, 0 -- `OK: collaboration state is valid.` |
| Drift runtime | `protocol_state_drift` de `runtime/protocol_replay.py` sobre la raiz del clon | 2 | 0, 0 -- `has_drift=False up_to_seq=9893 entries=0` |
| Encoding | `python scripts/scan_encoding.py` | 2 | 0, 0 -- `OK: encoding scan is clean.` |
| Neutralidad Python | `python scripts/scan_domain_neutrality.py` | 2 | 0, 0 |
| Neutralidad PowerShell | `pwsh -File scripts/scan_domain_neutrality.ps1` | 2 | 0, 0 -- **103 s medidos**, no excedio 5 min en mi entorno |
| Propiedad enfocada | `test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant` | 2 | PASS, PASS |

La neutralidad PowerShell la cito como VERDE: el maker no pudo, yo si, dos corridas y 103 s
cronometrados en la segunda. La discrepancia es de entorno, no del entregable.

El validador in-place sobre el arbol caliente tambien dijo `OK: collaboration state is valid.`
(warnings de higiene de mailbox, ninguno bloqueante), asi que el arbol no estaba a medio entregar.

## Corte 1 -- el A/B sobre el estado canonico de dbb9294f: PASA

Estado real, no sintetico: TASK-0414 `in_progress` owner Codex, con sus DOS claims `active` y
vencidos (`2026-08-17T11:55:04Z` y `2026-08-17T12:01:00Z`). Se extrae `Test-StalledTaskObligations`
por AST de CADA version del fichero de produccion y se corre sobre el MISMO estado.

    CANONICAL A/B on dbb9294f state, TASK-0414, peer=Codex
      run1: OLD alerts=0 | NEW alerts=1 keys=[stalled_task|TASK-0414|]
      run2: OLD alerts=0 | NEW alerts=1 keys=[stalled_task|TASK-0414|]

La direccion se midio en las DOS versiones sobre el mismo estado, dos corridas cada una. El codigo
viejo da CERO y el nuevo da UNA. **PASA.** El defecto original esta cerrado.

## Corte 2 -- la conjuncion: SLIPS

La produccion no exige `status == active`. Exige `status != released`. La mitad de la fecha se
endurecio; la mitad del estado se ablando. Matriz completa, dos corridas por celda, ambas versiones
sobre la misma fila de tarea:

| Poblacion del claim | OLD | NEW | Esperado por el criterio |
|---|---|---|---|
| sin claims | 1 | 1 | ALERTA |
| `active` + futuro | 0 | 0 | suprime |
| `active` + pasado | 0 | **1** | ALERTA (arreglo) |
| `active` sin campo `expires_at` | 0 | **1** | ALERTA (arreglo) |
| `active` + `"not-a-date"` | 0 | **1** | ALERTA (arreglo) |
| `active` + cadena vacia | 0 | **1** | ALERTA (arreglo) |
| `active` + `null` JSON | 0 | **1** | ALERTA (arreglo) |
| `active` + `12345` numerico | 0 | **1** | ALERTA (arreglo) |
| `active` + `"2026-08-18"` (solo fecha) | 0 | **1** | ALERTA (medianoche local ya pasada) |
| `released` + futuro | 1 | 1 | ALERTA |
| `blocked` + pasado | 1 | 1 | ALERTA |
| **`blocked` + futuro** | **1** | **0** | **ALERTA -- REGRESION** |
| **estado basura `"zzz"` + futuro** | **1** | **0** | **ALERTA -- REGRESION** |
| `"ACTIVE"` + futuro | 0 | 0 | suprime (caja) |
| `"RELEASED"` + futuro | 1 | 1 | ALERTA (caja) |

Ausente e ilegible ALERTAN: eso se confirma en seis poblaciones distintas, no solo en el ejemplo
dado. Pero las dos filas en negrita son escapes NUEVOS que el codigo pre-arreglo no tenia.

### HALLAZGO A (bloqueante) -- el estado no-`released` suprime

`scripts/harness/peer_mailbox_cron.ps1:1320`

    if ([string]$_.task_id -ne [string]$task.id -or [string]$_.status -eq "released") { return $false }

El predicado admite como supresor CUALQUIER estado que no sea `released`. `blocked` es un estado de
claim de primera clase: `scripts/validate_collaboration_state.py:37` declara
`VALID_CLAIM_STATUSES = {"active", "released", "blocked"}` y en el `CLAIMS.json` canonico de hoy hay
DOS claims `blocked` vivos. **La ventana no es hipotetica: esta fechada en el propio registro.**

    "claim_id": "CLAIM-20260703-Codex-TASK-0230-route-correction",
    "status":     "blocked",
    "started_at": "2026-07-03T08:59:15Z",
    "updated_at": "2026-07-03T08:59:15Z",
    "expires_at": "2026-07-04T00:00:00Z"

`started_at == updated_at`: la fila se escribio `blocked` y no se toco mas, con la expiracion
**quince horas en el FUTURO**. Con el codigo de d8a7ceb7 esa fila habria suprimido la alerta de
TASK-0230 durante esas quince horas; con el codigo viejo, no. Y su hermana
`-route-release-helper` es identica. Dos filas reales, validador en verde, en el estado canonico.

La asimetria es lo que lo convierte en defecto y no en gusto: **la misma expresion falla-cerrado
(alerta) ante una fecha basura y falla-abierto (calla) ante un estado basura.** Un claim con
`status` malformado, de una version futura del esquema o de una escritura a medias, apaga durante
toda su vigencia justo el control que TASK-0408 existe para encender.

Reproduccion (mutando PRODUCCION, no el runner; misma sonda, mismas poblaciones):

    variant                                                   none  current  expired  blocked+fut  released+fut
    HEALTHY (d8a7ceb7)                                           1        0        1            0             1
    M4 criterion-compliant (-ne released -> -ne active)          1        0        1            1             1

La correccion cabe en una palabra: `-ne "released"` pasa a `-ne "active"`, y el resto de la fila no
se mueve. Yo no la aplico: soy checker.

**Justicia con el maker, que no lo escondio:** su nota de evidencia en el propio fichero de tarea
declara "a claim suppresses `stalled_task` only when it is **not released**, has a readable
`expires_at`...". Es decir, declaro `not released`, no `active`; el criterio que el Arquitecto me
mando refutar dice `active`. La divergencia esta a la vista, no enterrada. Lo que la convierte en
defecto y no en diferencia de redaccion es la frase siguiente de esa misma nota: "this is the
conservative direction for a watchdog". Ese principio se aplico a la fecha y se invirtio en el
estado, dentro de la misma expresion. Y el arbitro final no es ninguna de las dos redacciones sino
el comportamiento: sobre `blocked` + futuro el codigo viejo alertaba y el nuevo calla.

### HALLAZGO C (cobertura, sostiene el A) -- la sonda es ciega a esta mitad

`obligation_alert_probe` construye sus tres poblaciones SIEMPRE con `"status": "active"`
(`scripts/test_exec_lease_harness.py:1548`). Nunca varia el estado, asi que no puede ver la mitad
del predicado que fallo. Lo acredito con dos mutantes de PRODUCCION que la propiedad enfocada
declara verdes:

| Mutante de produccion | Efecto medido | Veredicto de la sonda |
|---|---|---|
| M3: borrar la clausula de estado entera | `released` + futuro pasa de ALERTA a silencio | **PASS x2 -- SOBREVIVE** |
| M4: exigir `active` (la correccion) | `blocked` + futuro pasa de silencio a ALERTA | **PASS x2 -- SOBREVIVE** |

La sonda no distingue "sin control de estado" de "control correcto" de "control laxo": las tres
formas le dan verde. La garantia del corte 2 **no esta atada por ningun test**. Tras los mutantes
restaure el fichero, la propiedad volvio a PASS x2 y el arbol del clon quedo limpio.

## Corte 3 -- la sonda contra las tres poblaciones y los dos mutantes declarados: PASA (con el hueco del C)

Las tres poblaciones existen y discriminan lo que el maker dice:

| Poblacion | `old_stalled_count` sano | mutante solo-status (predicado de expiracion a `$true`) |
|---|---|---|
| sin claims | 1 | 1 |
| vigente | 0 | 0 |
| vencido | **1** | **0 -- mutante muerto** |

El mutante de solo-conteo tambien muere, medido sobre la funcion de produccion extraida por AST:

    exit=-1 outcome=transient attempt=1 -> exhausted=True      (sano)
    exit=-1 outcome=transient attempt=1 -> exhausted=False     (mutante: sin la clausula -1)

Los dos mutantes que el maker declara mueren de verdad. Lo que no existe es un mutante para la
mitad del estado, que es donde esta el escape (HALLAZGO A / C).

## Corte 4 -- el presupuesto de reintentos de otros caminos: SI cambia, y estaba FUERA DE ALCANCE

### HALLAZGO B (bloqueante) -- la entrega toca lo que el intake prohibe tocar

El bloque `out_of_scope` de TASK-0408 dice, literal:

> "NO se toca el presupuesto de reintentos ni las causas por las que un mensaje se difiere (0405,
> 0406, 0407, 0337, 0387): esta tarea entra por lo que pasa DESPUES de que muera, no por evitar que
> muera."

`Test-ExecRetryExhausted` es exactamente el presupuesto de reintentos: cambia el numero de intentos
de 3 a 1 para toda una clase de salidas. Familia completa medida sobre la funcion de produccion:

    exit=-1   outcome=transient    attempt=1 -> exhausted=True     <- 3 intentos pasan a 1
    exit=-1   outcome=transient    attempt=2 -> exhausted=True
    exit=-1   outcome=unconfirmed  attempt=1 -> exhausted=False
    exit=-1   outcome=definitive   attempt=1 -> exhausted=False
    exit=0    outcome=transient    attempt=1 -> exhausted=False
    exit=1    outcome=transient    attempt=1 -> exhausted=False
    exit=1    outcome=transient    attempt=3 -> exhausted=True
    exit=255  outcome=transient    attempt=1 -> exhausted=False
    exit=-2   outcome=transient    attempt=1 -> exhausted=False

Cual es esa clase, medido y no razonado: `-1` es el codigo que deja `Process.Kill()` en esta
plataforma. Lo comprobe arrancando un proceso y matandolo: `Process.Kill() -> ExitCode = -1`. Es
decir, **todo exec que mata el arnes** -- TREE_KILL por deadline (linea 1644), TREE_KILL
post-entrega (linea 1679) y el `$process.Kill()` de la linea 801 -- entra en la clase.

Y `Get-ExecOutcomeClass` clasifica esas muertes como `transient` salvo que el ULTIMO renglon de
stdout sea una linea `OUTCOME:` valida, cosa que un proceso matado rara vez alcanza a escribir:

    exit=-1 stdout termina en OUTCOME-transient -> outcome=transient  terminal_at_attempt1=True
    exit=-1 stdout termina en OUTCOME-confirmed -> outcome=confirmed  terminal_at_attempt1=False
    exit=-1 stdout truncado por el kill         -> outcome=transient  terminal_at_attempt1=True
    exit=-1 stdout vacio                        -> outcome=transient  terminal_at_attempt1=True
    exit=-1 stdout vacio + OwnEvidence          -> outcome=transient  terminal_at_attempt1=True   <-- el peor

La ultima fila es la que me preocupa: un exec que **si escribio en el ledger** (`OwnEvidence` true)
pero murio por el techo antes de imprimir su linea `OUTCOME:` ahora se declara agotado en la primera
observacion y pierde los dos intentos que antes tenia para aterrizar lo que quedo a medias. La regla
de codigo de salida precede a la de `OwnEvidence` en `Get-ExecOutcomeClass`, asi que la evidencia
propia no lo rescata.

Caminos NO afectados, verificados: la rama `catch`/`EXEC_FAIL` (linea 1726) conserva
`$attempt -ge $MaxTransientRetries` con su presupuesto de 3, y el contador de `defers`
(`active_external_claim`, el que mato tres encargos mios el 18-ago) no lo toca este commit.

Que quede claro lo que NO estoy diciendo: hacer terminal la muerte por techo puede ser lo correcto
para que el tablero deje de mentir. Lo que digo es que es **un cambio de presupuesto de reintentos
que el propio intake de la tarea declara fuera de alcance**, y que su colateral -- el exec con
evidencia propia que pierde dos vidas -- no esta declarado ni medido en la entrega. Eso se resuelve
con una DECISION o con una ampliacion explicita del alcance, no dentro de una remediacion.

## La suite completa NO esta verde, y NO se lo imputo a esta entrega

Corri `python scripts/test_exec_lease_harness.py` entera en el clon limpio de `d8a7ceb7`:
**`SUMMARY total=32 passed=28 failed=4`, exit 1.** La propiedad enfocada que gatea esta tarea esta
entre las 28 verdes. Discrimine caso por caso antes de acusar a nadie:

| Test caido | Discriminante que corri | Causa |
|---|---|---|
| `test_atomic_exec_admission_kills_peer_specific_lock_mutant` | reejecutado aislado | **PASS x2 -- flaky bajo carga**, no la entrega |
| `test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies` | leido el error | **`PermissionError [WinError 32]`** sobre `D:/Aegis_Scratch/multi_agent_project_protocol/task0319-tests` -- colision de entorno |
| `test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants` | corrido en clon limpio del PADRE `d8a7ceb7^` (`ebc3eab1`) | **FAIL x2 tambien en el padre -- PREEXISTENTE**, no la entrega |
| el cuarto | nombre no capturado en mi primera corrida | no clasificado; lo declaro como limitacion medida |

**Anomalia de entorno que si merece aviso (DECISION-0018), y no es de esta entrega:**
`scripts/test_exec_lease_harness.py:329` fija una ruta de scratch ABSOLUTA y COMPARTIDA:

    base = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0319-tests")

No depende del clon ni del proceso. Esa noche habia OCHO corridas concurrentes de
`validate_collaboration_state.py` de otros execs en la maquina; dos corridas simultaneas de esta
suite se pisan el mismo directorio y una muere con `WinError 32`. Consecuencia metodologica:
**"verde dos veces" en esta suite no es reproducible mientras un peer pueda estar corriendola a la
vez**, que es la condicion normal de este repo. La propiedad enfocada aguanta porque no toca esa
ruta, pero la suite entera no es un gate fiable hasta que la base sea unica por proceso.

Que quede explicito: el `failed=4` NO cuenta contra `d8a7ceb7`. Lo reporto porque un numero
publicado se re-deriva o no se publica, y porque el tercero -- preexistente y determinista, con un
`AssertionError` de mensaje VACIO -- lleva caido al menos desde el commit padre sin que nadie lo
diga.

## Residuos declarados (no bloqueantes)

1. `Test-ExecRetryExhausted` lee `$MaxTransientRetries` del ambito ambiente, no de un parametro. En
   produccion existe (parametro del script, linea 19) y no hay defecto vivo. Pero medido sin esa
   variable en ambito, la funcion devuelve `True` para TODA la familia, incluido `exit=0`: si algun
   dia se mueve a un modulo o a un job scope, agota todo en el primer intento y falla en silencio.
   La sonda tiene que inyectar `$MaxTransientRetries = 3` a mano, que es la senal de humo.
2. `[DateTimeOffset]::TryParse` usa la cultura del proceso. Un `expires_at` sin zona ni hora
   (`"2026-08-18"`, forma que existe hoy en `CLAIMS.json`) se lee como medianoche LOCAL: el claim se
   considera vencido durante todo su propio dia. Es conservador (alerta de mas) y por eso no bloquea.
3. La comparacion de estado es insensible a la caja en las dos versiones (`"ACTIVE"` suprime,
   `"RELEASED"` no suprime). Consistente entre viejo y nuevo, sin cambio de comportamiento.
4. El validador emite `unverifiable=9222` en el limite de verificacion de auth de eventos. Preexiste
   a esta entrega y no lo imputo.

## Veredicto

**CHANGE-REQUIRED.** El corte 1 pasa limpio y el corte 3 pasa. Bloquean el A (la remediacion abre un
escape nuevo en la direccion contraria a su proposito, con la mitad de la conjuncion sin exigir) y el
B (toca el presupuesto de reintentos que el intake declara fuera de alcance, con un colateral no
declarado). El C explica por que el A pudo pasar los gates: no hay test que lo mire.

## Bucle de arreglo esperado

- **Remediacion r2 (maker):** (1) exigir `status -eq "active"` en el predicado de supresion;
  (2) anadir a `obligation_alert_probe` una poblacion con `status` distinto de `active`/`released`
  y expiracion futura, y el mutante que la mate; (3) resolver el B por una de dos vias, a eleccion
  del Arquitecto: sacar `Test-ExecRetryExhausted` de esta entrega y llevarlo a tarea propia, o
  ampliar el alcance de 0408 por DECISION y declarar y medir el colateral del exec con `OwnEvidence`.
- **Puertas afectadas:** `test_exec_lease_harness.py` (propiedad enfocada),
  `validate_collaboration_state.py`, `scan_encoding.py`, neutralidad Python y PowerShell. Todas con
  DOS corridas.
- **Re-juicio:** independiente y ANTES del commit de cierre, con el A/B de dbb9294f repetido mas la
  nueva poblacion de estado.
- **Tope:** maximo 2 iteraciones (r2, r3). Si a la tercera sigue abierto, escala al operador humano.

## Reproducibilidad

Todo gate citado se corrio DOS veces. Cada numero de este veredicto se re-deriva de la corrida que
lo gatea en el clon limpio de `d8a7ceb7`; ninguno viene del arbol caliente. Sonda propia, no el
runner del maker, salvo donde digo explicitamente que corri la propiedad enfocada del maker.

-- Analista
