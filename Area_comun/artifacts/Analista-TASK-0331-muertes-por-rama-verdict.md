---
artifact: Analista-TASK-0331-muertes-por-rama-verdict
task_id: TASK-0331
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-09
local_time: 2026-08-09 00:01 (+02:00)
anchor_commit: a29e2cea
parent_commit: e9719613
protocol_head_at_review: 48242221
clean_clone: D:/Aegis_Scratch/protocol/r0331r6/cc
scope: hub only (sin producto en alcance)
verdict: CHANGE-REQUIRED
---

# TASK-0331 r6 -- las tres muertes por rama son reales; la via por la que aparecieron sigue abierta

## Tu pregunta, primero y medida

**Cuantas de las 24 celdas ejercen ahora la `Get-LeaseProcessState` REAL: cero. Las 24 siguen sobre
stub.**

No lo leo del codigo: lo mido. Colapse la funcion real entera a `return "live"` en una copia y
re-corri las 24 celdas contra esa copia. Resultado:

    cells: 24
    cells whose result CHANGES when the real Get-LeaseProcessState is collapsed to "live": 0
    changed: []

Cero de 24. Y el mismo experimento sobre `Test-LeaseProcessMatches` colapsada a `$true`:

    cells that change when Test-LeaseProcessMatches is collapsed to $true: 0

La causa es la de siempre y esta en `lease_owner_lock_state_table_probe`: despues de
`function_loader(...)` el guion de la sonda vuelve a definir **las dos** funciones
(`test_exec_lease_harness.py:720-725`), y en PowerShell la ultima definicion gana. La tabla contrata
la LOGICA DE DECISION dado un veredicto; el veredicto se lo da un stub.

Las muertes por rama que pediste no se anadieron a la tabla: se anadieron a **otra** sonda,
`lease_process_state_probe`, que si ejerce la funcion real y ahora la observa en sus **seis** salidas.
Eso tapa los tres agujeros conocidos. No cierra la via. Y la via tiene dientes: mas abajo esta el
mutante que lo demuestra.

De paso, una medida nueva sobre la tabla: las 24 celdas producen **7 salidas distintas**. En r5
reporte 18 entradas distintas; el numero de OBSERVACIONES distintas es 7. Grupos identicos:

    ['readable|dead|present', 'readable|dead|absent']
    ['readable|unknown|present', 'readable|unknown|absent', 'unreadable|live|absent',
     'unreadable|dead|absent', 'unreadable|unknown|present', 'unreadable|unknown|absent',
     'empty|live|absent', 'empty|dead|absent', 'empty|unknown|present', 'empty|unknown|absent',
     'identityless|live|absent', 'identityless|dead|absent', 'identityless|unknown|present',
     'identityless|unknown|absent']
    ['unreadable|live|present', 'empty|live|present']
    ['unreadable|dead|present', 'empty|dead|present', 'identityless|dead|present']

Lo declaro, no lo bloqueo: la convergencia esta declarada en prosa en la entrega y es contabilidad,
no cobertura perdida.

## Foco A -- M1, M2 y M3 enrojecen. Y enrojecen por COMPORTAMIENTO

Los reconstrui tal cual los medi en r5, sobre el fichero de produccion, verificando en cada caso que
el numero de literales `return "unknown"` queda **identico** al original (es decir: siguen siendo
mutantes de codigo muerto, no cambios de forma), y restaurando el arbol con
`git status --porcelain` vacio despues de cada uno.

| mutante | literal preservado | harness | contracts | asercion que lo mata |
|---|---|---|---|---|
| **M1** `catch` de `StartTime` -> `return "dead"` muerto | SI | **1** | 0 | `assert process_states == expected_process_states` (`:1868`) |
| **M2** `catch` de `Get-Process` -> `return "dead"` muerto | SI | **1** | 0 | `assert process_states == expected_process_states` (`:1868`) |
| **M3** `if ($true) { return "live" }` antes de comparar la hora | SI | **1** | 0 | `assert process_states == expected_process_states` (`:1868`) |
| **M4** identidad ausente -> `return "dead"` muerto (rama que ya no tiene mutante declarado) | SI | **1** | 0 | `assert all(row["lock_exists"] and row["lease_exists"] ...)` (`:1816`) |

Esto es exactamente lo que pediste y hay que decirlo sin rebaja:

- El tripwire `count == 3` **ha desaparecido**. En su lugar hay un oraculo de comportamiento --
  `expected_process_states` -- que fija las **seis** salidas de la funcion real: `live`, `dead`,
  `unknown`, `pid_reused -> dead`, `get_process_error -> unknown`, `start_time_error -> unknown`.
- Los tres mutantes que en r5 pasaban el `verification_cmd` entero ahora mueren, y mueren **en la
  linea 1868**, el oraculo de comportamiento, **no** en el `assert process_body.count(branch) == 1`
  de la linea 1945. El orden importa y esta bien puesto: comportamiento primero, forma despues.
- M4 es un extra mio: la entrega **quito** el mutante declarado de la primera rama
  (`missing_identity`). Comprobe que no queda descubierta: muere igual, y ademas en otra prueba
  (`test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence`), por consecuencia aguas abajo.
- La sonda tambien falla cerrada si alguien deja de pasar por el `Get-Process` sombreado: el modo
  `get_process_error` devolveria `live` en vez de `unknown` y el oraculo enrojece.

**Foco A: PASS.** Lo que decidia esta decidido.

## Foco B -- BLOQUEANTE: `Test-LeaseProcessMatches` no esta atada por nada, y su mutante reinstala el atasco mudo

Tu formulaste el riesgo con precision: *"si el arreglo anadio muertes por rama pero las celdas siguen
sobre stub, hemos tapado tres agujeros conocidos sin cerrar la via por la que aparecieron."* Fui a
buscar el siguiente agujero de esa via y lo encontre una funcion mas arriba.

`Test-LeaseProcessMatches` (`peer_mailbox_cron.ps1:228-231`) es el guardia de IDENTIDAD: decide si el
proceso que hay detras de un pid es el dueno de esa lease. Tiene dos consumidores en produccion:

- `Stop-LeaseProcessTree:233` -- `if (-not (Test-LeaseProcessMatches -Lease $Lease)) { return $false }`.
  Es lo unico que impide que el barrido de arbol mate a la **victima de un reuso de PID**.
- `Get-AdditionalWorkSignal:1053` -- `$leaseLiveness = if (Test-LeaseProcessMatches -Lease $lease)
  { "live" } else { Get-LeaseProcessState -Lease $lease }`. Decide si la lease de un peer veta la cola.

**En la suite entera esta stubeada en las siete posiciones donde se la llama**
(`test_exec_lease_harness.py:725, 768, 806, 862, 895, 931, 1711`). Donde se carga la real
(`:550`, `:575`) nadie la llama, porque alli `Stop-LeaseProcessTree` es un stub y
`Clear-StaleCronLockIfSafe` no pasa por ella. Cobertura de comportamiento: **cero**.

**M5, mutante de codigo muerto, superviviente:**

    function Test-LeaseProcessMatches {
        param($Lease)
        return $true
        return ((Get-LeaseProcessState -Lease $Lease) -ceq "live")    # linea original intacta
    }

| gate | resultado con M5 |
|---|---|
| `python scripts/test_exec_lease_harness.py` | **exit 0** (28/28 PASS) |
| `python scripts/check_falsification_contracts.py --root .` | **exit 0** |

Y el efecto en produccion, medido -- no argumentado. Sonda con la `Get-AdditionalWorkSignal` real,
la `Get-LeaseProcessState` real y la `Test-LeaseProcessMatches` real (sin ningun stub en su
posicion), contra una lease de peer en estado `running` cuyo dueno esta **probadamente muerto**
(`pid=999999`, que no existe):

    BASELINE   : {"signal": "none",              "detail": "",               "matches": false}
    M5 MUTANT  : {"signal": "active_peer_lease", "detail": "peer=Analista",  "matches": true}

Eso es, literalmente, el modo de fallo que abrio TASK-0331: **la lease de un peer muerto veta la cola
para siempre y nadie enrojece**. Con el `verification_cmd` completo en verde. Y el segundo consumidor
es peor de contar: sin ese guardia, `Stop-LeaseProcessTree` procede a matar el arbol de un pid que
puede pertenecer a **otro proceso** que reuso el numero.

No lo traigo como hallazgo colateral. Es la respuesta a tu foco B: la via sigue abierta y su siguiente
victima ya esta medida.

## Foco C -- el contrato TASK-0284: el nombre del helper ya no lo ata; la escritura resuelta, tampoco

Lo bueno primero, y es real: **el modo de fallo de r5 esta cerrado.** Renombre
`Write-AtomicUtf8NoBom` -> `Write-AtomicUtf8NoBomV2` en TODO el fichero y el runner sigue verde. El
contrato ya no cuelga del nombre del helper. Y tu mutante declarado mata.

Pero el criterio que fijaste es *"que ate la escritura resuelta del lock"*, y eso no se cumple. Cinco
variantes, cada una escrita sobre el fichero de produccion, corridas con
`python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`, arbol restaurado y verificado:

| variante | orden real lock-vs-sonda | exit | veredicto |
|---|---|---|---|
| **C0** baseline `a29e2cea` | correcto | 0 | -- |
| **C1** renombrar el helper atomico en todo el fichero | correcto | 0 | **el nombre ya no lo ata: PASS** |
| **C2** mover la llamada a inicio de linea por encima de la sonda (tu mutante declarado) | **violado** | **1** | **mata: PASS** |
| **C3** el MISMO movimiento real, escrito `$null = Write-ExecLockEvidence ...` | **violado** | **0** | **ESCAPE** |
| **C4** `Write-AtomicUtf8NoBom -Path $LockPath ...` en linea, por encima de la sonda, dejando `Write-ExecLockEvidence` intacta debajo | **violado** | **0** | **ESCAPE** |
| **C5** renombrar el parametro `$MessageName` del escritor | correcto | 0 | verde, pero por accidente (ver abajo) |

En C3 y C4 la evidencia del lock **se escribe de verdad antes de la sonda de residuo** -- la
propiedad que el contrato existe para defender -- y el contrato no lo ve.

La causa esta en `resolved_exec_lock_write` (`run_mailbox_retry_cases.py:331-345`): resuelve la
funcion escritora por un conjunto de nombres (`$LockPath` + `$MessageName` +
`process_start_time_utc`) y luego localiza sus llamadas con `(?m)^\s*<Nombre>\b`. Ata **una llamada
a inicio de linea a un nombre resuelto**, no la escritura. `$null = ` delante basta para escapar
(C3); escribir `$LockPath` por otra puerta basta para escapar (C4).

Y hay un agravante de precision que conviene saber antes de tocar nada: `function_bodies` corta por
`^function NOMBRE {`, asi que el "cuerpo" de la **ultima** funcion del fichero
(`Write-ExecLockEvidence`, `:1548`) se traga todo el resto del guion -- el bucle principal entero.
Por eso C5 sale verde: el conjunto de nombres sigue apareciendo, pero fuera de la funcion. El
resolutor es mas laxo de lo que parece, no mas robusto.

Esto es, otra vez, el patron de mi memoria: se pidio *atar la propiedad* y se entrego **otra forma,
mas estrecha**. Estrechar reduce el dano sin cambiar la clase. Quinta vez en esta familia (0316,
0319, 0321, 0331 r5, 0331 r6).

## Foco D -- el `verification_cmd` ampliado: PASS

Los tres lectores que faltaban estan dentro. Recuento de lectores de
`scripts/harness/peer_mailbox_cron.ps1` y su estado real:

| lector | en CI | en `verification_cmd` | exit en `a29e2cea` |
|---|---|---|---|
| `scripts/test_exec_lease_harness.py` | SI (`validate.yml:238`) | SI | 0 (28/28) |
| `scripts/scan_domain_neutrality.py` | SI (`:260`) | SI | 0 |
| `scripts/test_scan_domain_neutrality.py` | SI (`:263`) | **SI (nuevo)** | 0 |
| `scripts/scan_domain_neutrality.ps1` | SI (`:267`) | **SI (nuevo)** | 0 |
| `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | SI (`:284`) | **SI (nuevo)** | 0 |
| `scripts/test_anthropic_checker_harness.py` | NO | NO | 0 |
| `scripts/test_attested_instancing.py` | NO | NO | 1 (**igual en el padre**: deuda ajena heredada) |

**Los cinco lectores que CI ejecuta sobre el fichero que la tarea reescribe estan ahora dentro de su
puerta de aceptacion.** Los dos que quedan fuera no los ejecuta CI; el rojo de
`test_attested_instancing.py` es el mismo del padre (`Aegis\scripts\memory\test_memory_db.py`), ya
declarado como R6 en r5 y sin cambio.

## Foco E -- sin regresion en cinco vueltas: PASS

Suite completa en clon limpio: **28/28 PASS, exit 0**. Los nombres de las vueltas anteriores siguen
verdes, uno a uno:

    test_atomic_exec_admission_kills_peer_specific_lock_mutant
    test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence
    test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies
    test_self_heal_does_not_wait_for_deadline_before_dead_pid_cleanup
    test_scope_aware_claim_veto_kills_both_direction_mutants
    test_scope_aware_lease_veto_kills_both_direction_mutants
    test_archived_task_work_resolution_kills_hot_only_mutant
    test_glob_claim_scope_fails_closed_and_kills_guard_mutant
    test_dirty_tree_veto_still_precedes_scope_admission
    test_new_instance_exports_identical_harness
    test_active_peer_lease_reports_owner_and_claim_veto_survives
    test_preexec_defer_budget_kills_shared_counter_mutant

La correccion de `File.Replace(..., $null)` a ruta de backup unica con limpieza en `finally` es
correcta y esta ejercida por el camino real del runner: C1 la renombra entera y sigue pasando, luego
se ejecuta de verdad.

## Reproduccion

Clon limpio `git clone --no-hardlinks D:/Agentes/multi_agent_project_protocol cc`,
`git checkout a29e2cea`, arbol verificado limpio antes y despues de cada mutacion.

    python scripts/test_exec_lease_harness.py                        -> 0   (28/28 PASS)
    python scripts/check_falsification_contracts.py --root .         -> 0
    python scripts/validate_collaboration_state.py --root .          -> 0
    python scripts/scan_domain_neutrality.py --root .                -> 0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0   (15/16 corridas; ver R-FLAKE)
    python scripts/test_scan_domain_neutrality.py                    -> 0   (5 tests)
    powershell scripts/scan_domain_neutrality.ps1 -Root .            -> 0
    python scripts/scan_encoding.py --root .                         -> 0

Estado canonico del hub al revisar: `validate_collaboration_state.py` exit 0 en `48242221`;
`runtime/protocol_replay.py --check-drift` -> `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8185`.

Mutantes sobre `scripts/harness/peer_mailbox_cron.ps1`, todos con el literal original conservado:

    M1 catch StartTime      -> harness 1  (asercion :1868)   MUERE
    M2 catch Get-Process    -> harness 1  (asercion :1868)   MUERE
    M3 PID reusado ciego    -> harness 1  (asercion :1868)   MUERE
    M4 identidad ausente    -> harness 1  (asercion :1816)   MUERE
    M5 Test-LeaseProcessMatches -> $true  -> harness 0 / contracts 0   **SOBREVIVE**
    M6 tolerancia de 6 s en la comparacion de hora -> harness 0 / contracts 0   **SOBREVIVE**

Mutantes sobre el contrato TASK-0284 (runner completo): C0 0, C1 0, C2 1, C3 0, C4 0, C5 0.

## Residuales declarados

- **R1** 0 de 24 celdas ejercen la `Get-LeaseProcessState` real y 0 de 24 la
  `Test-LeaseProcessMatches` real; medido por colapso de la funcion a constante. 24 celdas -> 7
  salidas distintas.
- **R2 (R-FLAKE, nuevo)** La **primera** invocacion de `run_mailbox_retry_cases.py` en el clon frio
  fallo: `AssertionError` en `:867`, `assert "SELF_HEAL_ORPHAN_LOCK owner=TestPeer
  reason=missing_lease" in log`. Es un caso con **plazo duro de 12 s** que lanza un
  `powershell.exe -File` real. No lo he vuelto a reproducir: **1 fallo en 16 corridas** (5
  secuenciales, 4 concurrentes, 3 con la suite del harness corriendo en paralelo, mas baseline y
  drivers). Lo declaro porque este caso era **inalcanzable** antes de `a29e2cea` -- el runner abortaba
  en `:342` -- y ahora esta a la vez en CI y en el `verification_cmd`. Un runner de CI frio puede
  encontrarlo.
- **R3** M6: la sonda fija **un** desplazamiento (-7 s), asi que cualquier tolerancia inferior a 7 s
  en la comparacion de hora queda sin atar. Una propiedad se ata por su criterio, no por un punto.
- **R4** `test_attested_instancing.py` rojo en la entrega Y en el padre, fuera de CI y fuera del AC.
  Deuda ajena, sin cambio desde r5.
- **R5** `function_bodies` en el runner corta mal el cuerpo de la ultima funcion del guion (se traga
  el bucle principal). No mide un fallo hoy; explica por que C5 sale verde.
- **R6** No ejecute la suite de producto: **sin producto en alcance**, por instruccion del encargo.

## Veredicto

**CHANGE-REQUIRED.**

Lo que esta cerrado, y lo digo entero porque es la mayor parte: los tres mutantes que decidian
mueren, y mueren por comportamiento en la asercion `:1868`, no por forma; el tripwire `count == 3`
desaparecio; las seis salidas de la funcion real estan fijadas; la cuarta rama, que se quedo sin
mutante declarado, tambien muere; el contrato TASK-0284 dejo de colgar del nombre del helper y su
mutante declarado mata; los cinco lectores de CI del fichero estan dentro del `verification_cmd`; y
no hay regresion en las cinco vueltas anteriores (28/28).

Dos cosas impiden cerrar:

**B-nuevo (bloqueante).** `Test-LeaseProcessMatches` -- el guardia de identidad que decide si un pid
es el dueno de su lease -- **no esta observada por ninguna prueba**: esta stubeada en las siete
posiciones donde se la llama. Un mutante de codigo muerto que preserva la linea original
(`return $true` delante) pasa el `verification_cmd` completo y convierte una lease de peer con dueno
probadamente muerto en `active_peer_lease peer=<...>`, es decir **reinstala el atasco mudo que abrio
esta tarea**; y desarma el guardia que impide matar el arbol de una victima de reuso de PID. Esta es
tu foco B con dientes: la via por la que aparecieron M1/M2/M3 sigue abierta.

**C-nuevo (bloqueante, menor).** El contrato TASK-0284 ya no cuelga del nombre del helper, pero
tampoco ata la escritura resuelta: ata **una llamada a inicio de linea a un nombre resuelto**. Dos
movimientos reales de la escritura por encima de la sonda -- `$null = <llamada>` (C3) y escribir
`$LockPath` por otra puerta (C4) -- violan la propiedad y salen verdes.

**Como quiero que se falsee la remediacion, sin nombrar formas** (porque nombrar la forma es lo que
ha producido cinco vueltas de esta misma clase):

- **Para B-nuevo:** toda funcion que **produzca o consuma** el veredicto de vitalidad en el camino de
  admision del exec debe quedar observada al menos una vez **sin stub en su propia posicion**. El
  criterio de aceptacion que voy a aplicar es el mismo experimento que he corrido aqui: colapsar cada
  una de esas funciones a una constante en una copia y exigir que **al menos un gate del
  `verification_cmd` enrojezca**. Si colapsarla no enrojece nada, no esta atada. No pido "un test para
  `Test-LeaseProcessMatches`": pido que la propiedad sobreviva a que manana aparezca la septima
  funcion de la familia.
- **Para C-nuevo:** el contrato debe resolver **la primera escritura sobre `$LockPath` alcanzable en
  el camino de exec**, sea cual sea la forma sintactica de la llamada y pase o no por el helper
  nombrado, y debe falsarse **por cualquier reubicacion de esa escritura por encima de la sonda**.
  Mis mutantes de aceptacion seran C3 y C4 exactamente como estan escritos arriba, mas C1 y C2 para
  comprobar que no se ha comprado la robustez perdiendo lo que ya funcionaba.
- **R-FLAKE:** basta con declararlo o con quitarle la dependencia del reloj de pared; si vuelve a
  fallar en la re-corrida lo subo a bloqueante, porque un gate intermitente dentro del AC es un
  veredicto que no significa nada.

**Bucle de arreglo:** remediacion 6 -> re-juicio mio ANTES del commit de cierre. Gates exigidos en
clon limpio y por codigo de salida: los **siete** del `verification_cmd` actual, mas
`python scripts/scan_encoding.py --root .`, mas `runtime/protocol_replay.py --check-drift` limpio.
Esta es la **iteracion 2 de 2** del bucle que declare en r5; si la remediacion 6 no cierra B-nuevo,
**escalo al operador humano** en vez de pedir una tercera.

-- Analista
