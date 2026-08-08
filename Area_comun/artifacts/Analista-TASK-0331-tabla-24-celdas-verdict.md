---
artifact: Analista-TASK-0331-tabla-24-celdas-verdict
task_id: TASK-0331
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-08
local_time: 2026-08-08 13:04 (+02:00)
anchor_commit: e9719613a3c62808263ac11739ec97756edfdd35
parent_commit: a4a400e8
protocol_head_at_review: 36931ef4
clean_clone: D:/Aegis_Scratch/mapp/rev0331r5/cc
scope: hub only (sin producto en alcance)
verdict: CHANGE-REQUIRED
---

# TASK-0331 r5 -- la tabla es honesta; el veredicto que la sostiene no esta atado

## Tu pregunta, primero y medida

**No hemos cambiado recuperacion automatica por una llamada al operador en el caso comun.** La
frontera esta bien puesta. Lo medi con procesos reales, extrayendo `Get-LeaseProcessState` del
harness entregado y ejecutandola contra procesos que arranque y mate yo:

| vector real | veredicto |
|---|---|
| hijo vivo, pid + start correctos | `live` |
| hijo matado con `taskkill /PID <p> /T /F` (la muerte dura que os pasa cada semana) | **`dead`** |
| mismo pid vivo, start-time desplazado 7 s (reuso de PID) | **`dead`** |
| `process_start_time_utc` vacio | `unknown` |
| forma de lease `reserved` (sin `pid` ni start) | `unknown` |

La linea que decide: **la muerte dura corriente clasifica `dead`, no `unknown`.** La lease `running`
lleva `pid` + `process_start_time_utc` del hijo, y el lock lleva la misma identidad escrita antes y
borrada despues. Un `taskkill /T /F`, un cuelgue matado por el watchdog o un reinicio dejan lease
legible con identidad de un proceso que ya no existe -> celda `legible|dead|*` -> `SELF_HEAL_ORPHAN_LEASE
liveness=dead action=remove`. **Automatico. Sin operador.** Ese era el modo de fallo que abrio 0331 y
no ha vuelto por la puerta de atras.

Donde SI se alcanza `unknown`, declarado por medicion y no por conjetura:

1. **Resurreccion de PID hacia un proceso cuyo `StartTime` no se puede leer.** Censo con la propia
   funcion entregada sobre los 580 procesos vivos de esta maquina: `live=421 dead=2` y
   **`unknown=157`, el 27,1 %** (AggregatorHost, csrss, dwm, fontdrvhost, servicios de sistema...).
   La asimetria "solo PID + hora prueba muerto" degrada a `unknown` -- no a `dead` -- justo cuando
   el resucitador es un proceso protegido. Es raro (exige reuso de PID *y* que caiga en ese 27 %),
   pero no es "corrupcion que no se da sola".
2. **La lease `reserved` es SIN IDENTIDAD por construccion** (`peer_mailbox_cron.ps1:1094-1101`: no
   escribe `pid` ni `process_start_time_utc`). Cada exec pasa hasta 30 s en ese estado y lo unico
   que lo rescata es el lock, que se escribe antes (`:1373`) y se borra despues. Si el lock falta en
   esa ventana -- y los runbooks de destrabe de esta instancia borran locks a mano -- el siguiente
   tick cae en marcador + `LOCKED skip` hasta rearme manual.
3. **`Write-AtomicUtf8NoBom` renombra sin fsync del temporal** (`:1526-1540`), a diferencia de la
   reserva y del marcador, que usan `Flush($true)`. Un corte de corriente inoportuno puede dejar
   lease truncada o de 0 bytes. Aqui el lock -- escrito una vez, no latido -- es la redundancia que
   sigue probando `dead`, asi que la celda resuelve sola.

**Conclusion del foco central: PASS.** El atasco ruidoso sustituye al mudo sin comprarse el caso
comun. No bloqueo por aqui.

## Lo que SI bloquea: el veredicto trivaluado esta atado por un CONTEO, no por comportamiento

Toda la tabla de 24 celdas descansa sobre una sola frase: *"solo PID mas hora de arranque prueba
`dead`; la evidencia ausente o ilegible es `unknown`, nunca `dead`"*. Esa frase vive entera dentro de
`Get-LeaseProcessState` (`:207-225`), que tiene **cinco caminos de veredicto**:

| # | camino | veredicto | observado por un test? |
|---|---|---|---|
| 1 | falta `pid` o `process_start_time_utc` | `unknown` | SI (mutado y falsado) |
| 2 | `Get-Process` devuelve `$null` | `dead` | SI |
| 3 | `Get-Process` lanza | `unknown` | **NO** |
| 4 | `start` coincide | `live` | SI |
| 5 | `start` NO coincide | `dead` | **NO** |
| 6 | `StartTime` lanza | `unknown` | **NO** |

Lo que hace el contrato con los tres no observados es esto
(`test_exec_lease_harness.py:1901-1907`):

    assert process_body.count('        return "unknown"') == 3
    mutant_body = process_body.replace(missing_identity, missing_identity_dead, 1)
    ...
    assert process_mutant["unknown"] == "dead"

Muta **la primera ocurrencia** y comprueba su comportamiento. Las otras dos quedan sujetas por
`count == 3`: un **tripwire de forma**. Y un tripwire de forma se rodea dejando la forma intacta.

### Tres mutantes de codigo muerto, los tres SUPERVIVIENTES

Todos preservan `count == 3` -- el literal `return "unknown"` sigue presente, solo que inalcanzable.
Todos corridos en clon limpio sobre `e9719613`, restaurando el fichero y verificando
`git status --porcelain` vacio al final:

| mutante | que hace en produccion | `test_exec_lease_harness.py` | `check_falsification_contracts.py` |
|---|---|---|---|
| **M1** `catch { return "dead"; return "unknown" }` en el catch de `StartTime` | un dueno **VIVO** cuyo `StartTime` no se puede leer (el 27,1 % medido) se declara `dead` y `Clear-StaleCronLockIfSafe` **BORRA su lease y su lock** | **exit 0** (28/28 PASS) | **exit 0** |
| **M2** lo mismo en el catch de `Get-Process` | idem por la otra puerta | **exit 0** | **exit 0** |
| **M3** `if ($true) { return "live" }` antes de la comparacion de hora, dejandola presente e inalcanzable | un **PID REUSADO** se lee como el dueno vivo y la lease se preserva para siempre | **exit 0** | **exit 0** |

M1 lo re-confirme en una segunda corrida aislada, con el arbol verificado limpio y sin ningun otro
proceso tocando el clon: `HARNESS_SUITE_EXIT=0`, `CONTRACTS_EXIT=0`.

Lo que esto significa, sin adornos:

- **M1 y M2 son exactamente el mutante `unknown -> dead` que el contrato declara matar.** El texto de
  la tarea dice *"Sus mutantes cambian por separado `unknown -> dead`"*. Mata uno de los tres sitios.
  Los otros dos sobreviven, y son los dos que de verdad disparan en operacion (el que mide el 27,1 %
  es el catch de `StartTime`).
- **M3 es exactamente tu foco A.** Me pediste comprobar que la comparacion de hora "discrimina de
  verdad y no es vacua". **En produccion discrimina** -- lo medi: mismo pid, hora desplazada 7 s ->
  `dead`. **En el contrato no existe**: ningun fixture de la suite tiene un PID vivo con hora
  distinta (los que llevan `process_start_time_utc` usan `pid: 999999`, que no existe, asi que caen
  por el camino 2 y la hora es decorativa). La regla que impide el reuso de PID esta implementada y
  no esta atada.
- Y el tripwire ademas es del tipo equivocado: mi primer intento (cambiar el literal en la tercera
  ocurrencia, sin dejar codigo muerto) **si** enrojecio -- pero por `AssertionError` en
  `count == 3`, es decir por un cambio de FORMA que cualquier refactor legitimo tambien rompe. Es el
  patron de DRAFT-DECISION-0105 / TASK-0341 dentro del contrato que corona esta entrega: fragil a lo
  que no importa, ciego a lo que si.

## Foco B -- celdas declaradas frente a celdas ejercidas: 24 declaradas, 18 distintas

Reconstrui los 24 fixtures de `lease_owner_lock_state_table_probe` y los hashee:

    declared cells: 24
    DISTINCT fixture inputs: 18
    byte-identical groups: 3
      ['unreadable|live|absent', 'unreadable|dead|absent', 'unreadable|unknown|absent']
      ['empty|live|absent',      'empty|dead|absent',      'empty|unknown|absent']
      ['identityless|live|absent','identityless|dead|absent','identityless|unknown|absent']

**Seis celdas son re-ejecuciones byte a byte de una hermana.** Sin lock y con lease inservible, el
eje `dueno` no es una entrada del sistema: no hay donde escribirlo. La entrega **declara** esa
convergencia en prosa ("Esas filas convergen deliberadamente en la misma accion segura"), asi que
cumple tu requisito de declararlo -- pero el numero que se reporta es 24 y el numero de
observaciones distintas es 18. Sin dientes perdidos: es contabilidad, no cobertura.

Lo que si tiene consecuencia: **ninguna de las 24 celdas ejerce la `Get-LeaseProcessState` real.**
Las 24 la sustituyen por un stub que lee un campo `probe_liveness` del propio fixture. La funcion de
verdad se observa solo en `lease_process_state_probe`, con tres casos. **Esa es la razon estructural
de que M1/M2/M3 sobrevivan**: la tabla contrata la LOGICA DE DECISION dado un veredicto, y el
veredicto se contrata en 3 de sus 6 salidas. La tabla de 24 celdas es correcta y no es el problema;
el problema esta un marco mas abajo, en quien le entrega el `live|dead|unknown`.

## Foco C -- los cuatro mutantes declarados: PASS

Los cuatro mueren, y tres de los cuatro son mutantes de **codigo muerto** como pediste:

| mutante declarado | forma | muere |
|---|---|---|
| `unknown -> dead` (default de lease ilegible) | cambio de valor | SI (`lease_exists is False`) |
| evidencia de lock ignorada | `if ($false) { $liveness = $lockLiveness }` | SI (`lease_exists is True`) |
| `unknown` como permiso | `if ($false) { return "peer_lease_unreadable" }` | SI (`before == "none"`) |
| marcador suprimido | `if ($false) {` | SI (`lock_exists is False`) |

La brecha no esta en estos cuatro. Esta en los **hermanos de la misma clase declarada** de la
seccion anterior.

## Foco D -- sin regresion en lo ya probado: PASS

Suite completa verde en clon limpio, 28/28. Los nombres de las cuatro vueltas anteriores siguen
pasando: `test_atomic_exec_admission_kills_peer_specific_lock_mutant`,
`test_orphan_lease_self_heal_matrix_requires_dead_owner_evidence`,
`test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies`,
`test_self_heal_does_not_wait_for_deadline_before_dead_pid_cleanup`,
`test_scope_aware_claim_veto_kills_both_direction_mutants`,
`test_scope_aware_lease_veto_kills_both_direction_mutants`,
`test_archived_task_work_resolution_kills_hot_only_mutant`,
`test_glob_claim_scope_fails_closed_and_kills_guard_mutant`,
`test_dirty_tree_veto_still_precedes_scope_admission`,
`test_new_instance_exports_identical_harness` (export byte-identico).

## Foco E -- el re-fijado de neutralidad: PASS, y una confesion mia

El conjunto exento es **EL MISMO**. Nueve lineas exentas (la 9 mas las ocho movidas
420/427/437/446/447/454/470/1337 -> 476/483/493/502/503/510/526/1397), y el contenido de las nueve es
**identico caracter a caracter** entre `a4a400e8` y `e9719613`:

    EXEMPTED_LINE_CONTENT_IDENTICAL = True
    OK    9->9    [ValidateSet("Auto", "Anthropic", "Codex")][string]$AgentProvider = "Auto",
    OK  420->476  $commandName = if ($AgentProvider -eq "Anthropic") { "claude" } else { "codex" }
    OK  427->483  $match = [regex]::Match($content, '"([^"]*codex\.exe)"')
    OK  437->493  $whereResults = @(& where.exe codex 2>$null)
    OK  446->502  $base = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
    OK  447->503  $candidate = Get-ChildItem -Path $base -Recurse -Filter codex.exe ...
    OK  454->510  $extensionCandidate = Get-ChildItem -Path $extensionBase -Recurse ...
    OK  470->526  # Default arguments for the reference agent (codex CLI): ...
    OK 1337->1397 # subcommand. The reference agent (codex exec) reads the prompt from stdin ...

No se colo ninguna linea distinta. Ademas verifique que los dos lectores coinciden: con el propio
lector del escaner (`Get-Content -Path -Encoding UTF8`) y con Python, el termino de identidad
aparece exactamente en `{9, 28, 476, 483, 493, 502, 503, 510, 526, 1397}` en ambos. Sin caracteres
exoticos de corte de linea (`0x0b/0x0c/0x85/U+2028` = 0), sin bytes > 127, LF puro.

Y los tres gates de neutralidad, verdes -- incluido `test_scan_domain_neutrality.py`, que ejecuta
los contratos SCOPE y PARITY y **no esta en el `verification_cmd` de 0331**, y el gemelo PowerShell:

    python scripts/test_scan_domain_neutrality.py        -> exit 0
    pwsh   scripts/scan_domain_neutrality.ps1 -Root .    -> exit 0
    python scripts/scan_domain_neutrality.py --root .    -> exit 0

**Confesion, porque el arbol caliente miente tambien en mi banco:** mi PRIMERA corrida de estos tres
gates dio rojo (`test_scan_domain_neutrality.py` exit 1 con "0 occurrences en :476", y el gemelo PS
senalando 477/484/494/504/511/527/1398, todo +1). Estuve a punto de firmarlo como regresion. Era
**contaminacion mia**: un driver de mutacion mio corria en segundo plano sobre el mismo clon y su
linea insertada desplazaba el fichero una linea. Re-corridos con `git status --porcelain` vacio
comprobado antes y despues: los tres verdes. Lo dejo escrito porque un rojo mal atribuido a esta
entrega habria costado una vuelta entera.

## Foco F -- el rojo de CI que ya mediste: confirmado, con dos correcciones

Reproducido en clon limpio: `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` ->
**exit 1**, `AssertionError: TASK-0284 pre-gate contract is incomplete` en `:342`. Condicion a
condicion, ocho de las nueve PASAN y falla solo `prelock >= 0 and lock_write > prelock`, con
`prelock=62938 lock_write=-1`.

**1. Lo que hay que arreglar es el CONTRATO, no la implementacion.** Con esas palabras, porque es lo
que mide la evidencia. La propiedad real del contrato es de ORDEN: la escritura del lock debe ocurrir
DESPUES de la sonda de residuo. **En la entrega el orden SE MANTIENE**: `$residueState =
Get-StagedResidueState` en offset 62938 (linea 1334) y `Write-AtomicUtf8NoBom -Path $LockPath` en
offset 79099 (linea 1551). Lo unico que cambio es el NOMBRE del helper (`Write-Utf8NoBom` ->
`Write-AtomicUtf8NoBom`) y la carga (de una linea de sello a un blob JSON con `owner/task_or_msg_id/
pid/process_start_time_utc`). El reemplazo es **mejor**: renombrado atomico via `File.Replace` y, sobre
todo, es la identidad PID+start del lock de la que depende la tabla trivaluada entera. El contrato
busca un literal que ya no existe y por eso `find` devuelve -1.

**2. Correccion a la atribucion: no es la remediacion 4.** `git log -S 'Write-Utf8NoBom -Path
$LockPath' -- scripts/harness/peer_mailbox_cron.ps1` da **`4c4e2665 fix(TASK-0331): preserve live
unreadable leases`, 2026-08-08 07:08:23 +0200** -- la remediacion 3. Y el padre del commit revisado,
`a4a400e8`, **ya falla** con la misma asercion, la misma linea 342 y la misma unica condicion
(`prelock=60726 lock_write=-1`). Sigue siendo de 0331 -- esta dentro de su cadena y 0331 lo posee --
pero `e9719613` no lo introdujo y revertir `e9719613` no lo limpia.

**3. El contrato no debe seguir con esa forma.** De sus nueve condiciones, ocho son subcadenas
literales del harness y la novena es un predicado de orden expresado sobre dos subcadenas literales.
La novena es la unica que carga una propiedad real, y es la que se rompio -- no porque la propiedad
se rompiera, sino porque renombraron un helper. Cuarta vez (0316, 0319, 0321, 0331). La reparacion
que sobrevive a cambio de coordenada, orden y formato es expresarla sobre la ESCRITURA RESUELTA y no
sobre el nombre: que la primera escritura de `$LockPath` en el camino de exec ocurra despues de la
sonda, y falsarla **moviendo la escritura por encima de la sonda**, no borrando una linea.

Y un agravante que no estaba en tu medicion: **`assert contract(text)` revienta ANTES de evaluar los
mutantes.** `terminal_defer_removed` y `dirty_forensics_removed` no llegan a ejecutarse. El contrato
no esta solo rojo: esta **inerte**. Lleva horas reportando rojo mientras la propiedad que defiende no
se comprueba en absoluto.

**4. Mas huecos del mismo tipo -- si, medidos.** Seis ficheros leen
`scripts/harness/peer_mailbox_cron.ps1`. El `verification_cmd` de 0331 nombra dos:

| lector del harness | en `verification_cmd`? | en CI? | exit en `e9719613` |
|---|---|---|---|
| `scripts/test_exec_lease_harness.py` | SI | SI | 0 |
| `scripts/scan_domain_neutrality.py` | SI | SI | 0 |
| `scripts/test_scan_domain_neutrality.py` | **NO** | SI | 0 |
| `scripts/scan_domain_neutrality.ps1` | **NO** | SI | 0 |
| `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | **NO** | SI (`falsification-runners`) | **1** |
| `scripts/test_anthropic_checker_harness.py` | **NO** | NO | 0 |
| `scripts/test_attested_instancing.py` | **NO** | NO | 1 (**igual en el padre**: deuda heredada ajena, `Aegis\scripts\memory\test_memory_db.py`) |

**Cuatro lectores ejecutados por CI del fichero que la tarea reescribe estan fuera de su puerta de
aceptacion.** Por eso pudo declararse verde con el runner roto: `check_falsification_contracts.py`
sale verde porque comprueba DECLARACION, y el `verification_cmd` no ejecuta al lector que si mira.

## Reproduccion

Clon limpio `git clone --local D:/Agentes/multi_agent_project_protocol cc`, `git checkout e9719613`,
arbol verificado limpio antes y despues de cada mutacion.

    python scripts/test_exec_lease_harness.py                                   -> 0   (28/28 PASS)
    python scripts/check_falsification_contracts.py --root .                    -> 0
    python scripts/check_falsification_contracts.py --root . \
           --workflow .github/workflows/validate.yml --inventory                -> 0   (57/57 missing=0)
    python scripts/validate_collaboration_state.py --root .                     -> 0
    python scripts/scan_domain_neutrality.py --root .                           -> 0
    python scripts/scan_encoding.py --root .                                    -> 0
    python scripts/test_scan_domain_neutrality.py                               -> 0   (fuera del AC)
    pwsh   scripts/scan_domain_neutrality.ps1 -Root .                           -> 0   (fuera del AC)
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py              -> 1   (fuera del AC)

Mutantes de codigo muerto (literal `return "unknown"` presente pero inalcanzable, `count == 3`
preservado), cada uno con restauracion y `git status --porcelain` vacio:

    M1 StartTime catch  -> harness 0 / contracts 0   (re-confirmado en corrida aislada)
    M2 Get-Process catch-> harness 0 / contracts 0
    M3 PID-reuse blind  -> harness 0 / contracts 0

Estado canonico del hub al revisar: `validate_collaboration_state.py` exit 0 en `36931ef4`.

## Residuales declarados

- **R1** 24 celdas declaradas / 18 fixtures distintos; 6 duplicados exactos. Las 24 usan un stub de
  liveness; cero ejercen la funcion real.
- **R2** La lease `reserved` es sin identidad por construccion; en esa ventana el lock es la unica
  identidad. No lo mido como defecto: lo declaro porque cambia donde hay que mirar si algo encalla.
- **R3** `Write-AtomicUtf8NoBom` renombra sin fsync del temporal; la reserva y el marcador si usan
  `Flush($true)`. Asimetria, no fuga medida.
- **R4** 27,1 % de los procesos vivos de esta maquina clasifican `unknown` ante resurreccion de PID.
  Numero de UNA maquina y de un contexto no elevado; no lo generalizo.
- **R5** Mi primera medicion de los gates de neutralidad estuvo contaminada por mi propio driver y
  dio un falso rojo. Corregida arriba.
- **R6** `test_attested_instancing.py` rojo en la entrega Y en el padre, y no esta cableado en CI.
  Deuda ajena, no de 0331.
- **R7** No ejecute la suite de producto: **sin producto en alcance**, por instruccion del encargo.

## Veredicto

**CHANGE-REQUIRED.**

La tabla de 24 celdas es un trabajo honesto: la frontera esta bien puesta, el atasco mudo se volvio
ruidoso sin comprarse el caso comun, los cuatro mutantes declarados mueren, el re-fijado de
neutralidad no exime nada nuevo y no hay regresion en lo ya probado. Dos cosas impiden cerrar:

**B1 (bloqueante).** El veredicto trivaluado -- la regla de oro sobre la que descansa la tabla
entera -- esta atado por un CONTEO de literales en 2 de sus 3 sitios `unknown`, y la comparacion de
hora de arranque no esta atada en absoluto. Tres mutantes de codigo muerto que preservan el conteo
sobreviven al `verification_cmd` completo, y cada uno convierte una regla declarada en su contrario:
borrar la lease de un dueno que no se puede probar muerto (M1, M2) y tomar un PID reusado por el
dueno vivo (M3). Remediacion: observar esos veredictos por COMPORTAMIENTO -- forzar el catch de
`Get-Process` y el de `StartTime`, y un caso de PID vivo con hora distinta -- y sustituir
`count == 3` por muertes por rama. El material existe: hay 157 PIDs en esta maquina cuyo `StartTime`
no se puede leer.

**B2 (bloqueante).** `falsification-runners` esta rojo **e inerte** sobre el fichero de esta tarea, y
dentro de su propia cadena (`4c4e2665`). No puede cerrarse una tarea dejando un contrato ejecutado
por CI sobre su fichero abortando antes de su paso de falsacion. La reparacion es del CONTRATO -- la
implementacion es correcta y mejor que antes -- expresada sobre la escritura resuelta y no sobre el
nombre del helper.

Si prefieres particionar B2 hacia el hilo de DECISION-0105 / TASK-0341, que es el mismo patron, me
parece defendible y lo digo explicitamente: **B1 es de 0331 y no se puede particionar**; B2 es de
0331 por propiedad pero su forma correcta es la generalizacion que ya tienes contratada.

**Bucle de arreglo:** remediacion 5 -> re-juicio mio ANTES del commit de cierre. Gates exigidos en
clon limpio y por exit code: los cuatro del `verification_cmd` **mas**
`scripts/test_scan_domain_neutrality.py`, `scripts/scan_domain_neutrality.ps1` y
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`. **Maximo 2 iteraciones**; a la tercera
escalo al operador humano.

-- Analista
