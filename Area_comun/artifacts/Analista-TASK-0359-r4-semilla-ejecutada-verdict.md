# Veredicto Analista -- TASK-0359 r4 (la sonda ejecuta la semilla de produccion)

- Revisor: Analista (voz adversarial independiente)
- Fecha: 2026-08-12, 12:15-12:50 hora local (UTC+2)
- Ancla protocolo: `cac45c2f` (HEAD de `origin/main` al abrir la review)
- Implementacion juzgada: `e08d9e54` -- `test(TASK-0359): execute production sampling seed`
- Alcance declarado por el Arquitecto: SOLO hub, sin producto (no se gatea `npm test`)
- Clon limpio con historia completa: `git clone -s` -> `D:/Aegis_Scratch/mapp/t0359r4`,
  `git checkout e08d9e54`, working tree limpio
- Vuelta: 3 de las concedidas (r4 de review)
- Recomendacion de cierre: **OK-CLOSABLE**, con un residual NUEVO declarado (R11) que **no convierto
  en cuarta vuelta**

---

## 0. Resumen en una linea

El liston que fije en r3 **se cumple y lo he medido yo**: con `:1495` mutado por el **signo** -- un
caracter -- el negativo entregado **MUERE**, y muere por la **asercion de conducta**, no por un conteo
de texto; el arbol sano sigue vivo. La respuesta a tu pregunta es **si, todavia queda**: la sonda
sigue escribiendo a mano `:1475` y `:1485`, y un mutante de **un caracter** en `:1485` falsifica la
primera clausula del propio texto del contrato con el negativo **verde**. Es un coordenada mas
afuera, no es el defecto que esta tarea existe para arreglar, y por tu presupuesto **no pido vuelta
cuatro**: te lo entrego como tarea sucesora y la decision es tuya y del operador.

---

## 1. Reproduccion (gates, por exit code, en clon limpio sobre `e08d9e54`)

    cd D:/Aegis_Scratch/mapp/t0359r4 && git checkout e08d9e54    # working tree limpio

    python scripts/validate_collaboration_state.py --root .           EXIT=0   OK: collaboration state is valid.
    python scripts/scan_encoding.py                                   EXIT=0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py                          EXIT=0
    powershell -File scripts/scan_domain_neutrality.ps1               EXIT=0
    python scripts/check_falsification_contracts.py                   EXIT=0   74 DECLARED
    python scripts/test_exec_lease_harness.py                         EXIT=0   SUMMARY total=31 passed=31 failed=0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    EXIT=0

El inventario sigue en **74** contratos: esta vuelta no anade contrato, extiende los `boundaries` del
que ya existia (`NEG-HARNESS-WORK-DERIVED-EXEC-LIVENESS`, de 4 a 8) y cambia su `mutation`. Coherente
con "solo test y texto gobernado".

Diff del ancla: `scripts/test_exec_lease_harness.py` (+38/-4), el cuerpo de la tarea, y el rastro de
ledger (`CLAIMS.json`, `CLAIMS.slim.json`, `events.jsonl`, `snapshot.json`). **Produccion intacta**:
`scripts/harness/peer_mailbox_cron.ps1` no aparece en el commit. Verificado.

Estado canonico sano en el ancla y en HEAD. En `cac45c2f` la unica claim activa es
`CLAIM-20260812-Arquitecto-OPS-selfhosted-probe`, con scope sobre su propia fila y
`.github/workflows/selfhosted-probe.yml`: **ninguna claim ajena sobre `Area_comun/artifacts/` ni
sobre `Area_comun/mailbox/open/`**, que son las rutas donde escribo. La claim de Codex
`CLAIM-20260812-Codex-TASK-0359-remediation4` ya esta liberada.

---

## 2. Instrumento propio

Mi sonda **no es la del maker**, y esta vuelta la diferencia es el punto de corte: extrae el bloque de
produccion desde **`:1485`** (`$execHardDeadlineUtc = $deadlineUtc.AddSeconds(...)`) hasta el final del
nodo `while`, es decir **una coordenada mas arriba que la sonda entregada**, que empieza en `:1493`.
Asi `:1485-:1492` -- el techo duro, la linea de log del limite, el recomputo de `$eventsPath` y las
dos lineas base de bytes -- se **ejecutan desde el artefacto** en vez de escribirse a mano.

El ancla es un **prefijo** (`$execHardDeadlineUtc = $deadlineUtc.AddSeconds(`), no la linea entera,
para que un arbol con `:1485` mutado tambien se localice. Como produccion recalcula
`$eventsPath = Join-Path $Root "runtime\state\events.jsonl"`, mi sonda crea ese fichero vacio en la
raiz temporal para no introducir una diferencia que no estoy midiendo.

Ficheros: `D:/Aegis_Scratch/mapp/t0359r4_probe/my_instrument.py` (mi sonda),
`run_delivered_negative.py` (corre el negativo ENTREGADO con `HARNESS_PATH` apuntando a un arbol
mutado y **dice en que asercion muere**), y los cinco mutantes `M1..M5-*.ps1`.

---

## 3. El liston de r3, medido

**Criterio que fije yo:** con `:1495` mutado a `AddSeconds($progressSampleSeconds)` (un caracter), el
negativo debe **morir**; el arbol sano debe seguir vivo.

Negativo ENTREGADO corriendo contra cinco arboles de produccion, uno por uno:

| Arbol | Mutacion (produccion) | Negativo entregado | Muere en |
|-------|----------------------|--------------------|----------|
| sano | -- | **PASS** (31/31 en suite) | -- |
| M1 | `:1495` `AddSeconds(-$x)` -> `AddSeconds($x)` (**1 caracter**) | **FAIL = MUERE** | `assert healthy_outcome["exec_progressing"] is True` |
| M2 | `:1495` -> `[DateTime]::MaxValue` | **FAIL = MUERE** | `assert healthy_outcome["exec_progressing"] is True` |
| M3 | `:1567` guarda -> `if ($false) {` | **FAIL = MUERE** | `assert healthy_outcome["exec_progressing"] is True` |
| M4 | `:1485` `AddSeconds($x)` -> `AddSeconds(-$x)` (**1 caracter**) | **PASS = NO SE ENTERA** | -- (ver 4) |
| M5 | `:1520` (2.a ocurrencia de la semilla) -> `[DateTime]::MaxValue` | FAIL, pero en `assert source.count(live_sampling_seed) == 2` | conteo de **TEXTO**, no conducta |

Lo importante de la columna "muere en": M1, M2 y M3 mueren en la **primera asercion de conducta** del
test, que se evalua **antes** que cualquier asercion de forma. No es una muerte por conteo de cadenas;
es que el arbol mutado deja de mantener vivo al exec. La falsacion que firme en r3 **no reproduce**.

Mi instrumento independiente sobre los mismos arboles, dos controles del sano intercalados:

    sano       exec_progressing=True   exec_hung=False  stop_calls=0  instrument_cost_ms=316
               LOG: EXEC_PROGRESSING reason=process_tree_cpu_growing
    M4         exec_progressing=False  exec_hung=True   stop_calls=1  instrument_cost_ms=309
               LOG: EXEC_HUNG reason=hard_cap action=terminate
    sano       exec_progressing=True   exec_hung=False  stop_calls=0  instrument_cost_ms=225   (control)
               LOG: EXEC_PROGRESSING reason=process_tree_cpu_growing
    M1         exec_progressing=False  exec_hung=True   stop_calls=1  instrument_cost_ms=299
               LOG: EXEC_HUNG reason=no_progress action=terminate
    M5         exec_progressing=True   exec_hung=False  stop_calls=0  instrument_cost_ms=307

El sano no puede pasar por otra senal: `stdout`, `stderr` y los dos `events.jsonl` los crea la sonda
vacios y nadie los escribe; el unico `reason` posible es `process_tree_cpu_growing`, y ahi esta.

**Tabla vector por vector de lo que pediste:**

| # | Vector | Veredicto | Evidencia |
|---|--------|-----------|-----------|
| 1 | Con `:1495` mutado por el signo, el negativo MUERE | **PASS** | M1, muerte en la asercion de conducta |
| 2 | El arbol sano sigue vivo | **PASS** | suite 31/31 + dos controles de mi instrumento |
| 3 | La sonda ejecuta la semilla en vez de escribirla | **PASS** | `Invoke-Expression $srcText.Substring($seedIdx, ...)` desde `:1493`; las tres asignaciones a mano borradas |
| 4 | El `mutation` declarado del contrato es el de la semilla | **PASS** | `sign_changed_source = source.replace(live_sampling_seed, sign_changed_seed, 1)` |
| 5 | La seccion de la vuelta esta escrita en el cuerpo de la tarea | **PASS** | seccion "Remediacion Codex vuelta 3 2026-08-12"; la frase "AC5 incumplido" que quedaba vive dentro de la seccion historica de r2, superada por la seccion de estado tras r3 |
| -- | **Tu pregunta: queda alguna linea de produccion que la sonda siga escribiendo?** | **SI, quedan cuatro** | ver 4 |

---

## 4. Respuesta a tu pregunta, con el mutante encima de la mesa (R11)

Si. La sonda entregada arranca en `:1493`, y sigue escribiendo de su puno cuatro cosas que produccion
calcula, **todas en el camino de decision**:

| Produccion | Linea | Para que sirve en la decision |
|------------|-------|-------------------------------|
| `:1475` | `$deadlineUtc = [DateTime]::UtcNow.AddSeconds($ExecTimeoutSeconds)` | fija el primer deadline **y** es la base de la semilla de `:1495` |
| `:1485` | `$execHardDeadlineUtc = $deadlineUtc.AddSeconds($ProgressHardCapSeconds)` | es la mitad derecha de la guarda de `:1511` |
| `:1488-:1491` | `$progressOutputBytes = 0L` + el `foreach` que suma stdout/stderr | linea base de `run_log_growing` |
| `:1492` | `$progressLedgerBytes = ...` | linea base de `ledger_growing` |

`:1475` no es extraible: la sigue `Start-Process $invocation.FilePath` con media docena de variables de
produccion que la sonda no puede montar. Eso es una frontera legitima y no lo cuento como defecto.

**`:1485` si es extraible, y es explotable.** Mutante M4, **un caracter** (`AddSeconds($x)` ->
`AddSeconds(-$x)`):

    MI instrumento (ejecuta :1485 desde el artefacto):
      exec_progressing=false  exec_hung=true  stop_calls=1
      LOG: EXEC_HUNG pid=36276 reason=hard_cap action=terminate

    NEGATIVO ENTREGADO con HARNESS_PATH sobre ese mismo arbol:
      RESULT=PASS  (el negativo no se entera)

Con `$execHardDeadlineUtc` por detras de `$deadlineUtc`, la guarda de `:1511`
(`$progress.progressing -and $progressObservedAtUtc -lt $execHardDeadlineUtc`) es falsa desde el primer
segundo: el exec que **si** esta quemando CPU se declara `hard_cap` y se mata en su primer deadline. El
texto del contrato dice, literalmente, *"must keep a silent CPU-working exec alive at its first
deadline"*. M4 falsifica esa clausula, con un caracter, y el negativo se queda verde. Y no lo cubre
nadie mas: `:1485` esta **copiado a mano en dos sondas** distintas del arnes (`:1150` y `:1361` del
test) y **ejecutado desde el artefacto en ninguna**.

### 4.1 Por que aun asi firmo OK-CLOSABLE, y no repito el bloqueo de r3

Lo digo explicito porque la simetria con r3 invita a bloquear otra vez, y creo que seria un error:

1. **No es el defecto que esta tarea existe para arreglar.** Lo que bloquee en r3 restauraba
   *exactamente* AC5: el detector volvia a depender EXCLUSIVAMENTE de que creciera un fichero, y el
   checker se quedaba ciego. M4 no reintroduce esa ceguera; introduce el fallo contrario (matar a uno
   que trabaja) por aritmetica del techo duro. Es otra clausula, otra linea y otro modo de fallo.
2. **AC5 y R6 estan cerrados por conducta y medidos por mi**, con el mutante mas fuerte que sabia
   pedir.
3. **Tu presupuesto esta agotado y me dijiste que no concediera la cuarta.** No la concedo. R11 es
   material de **tarea sucesora**, exactamente igual que R1, R8, R9 y R10, que ya se estan arrastrando
   declarados.

Si tu criterio es que el texto del contrato no puede prometer una clausula que no verifica **antes** de
cerrar nada, esa es una escalada tuya al operador, no un veto mio. Yo he puesto el coste encima de la
mesa para que la decision sea barata: mover el ancla de la sonda de `:1493` a `:1485` y borrar tres
lineas de preambulo es del mismo tamano que el parche de esta vuelta, y ya lo he ejecutado yo.

---

## 5. Residuales declarados

- **R11 (NUEVO) -- `:1485` se escribe a mano y es explotable con un caracter.** Medido arriba. Mismo
  patron que S1 (r2, `$before`) y S2 (r3, el calendario), tercera coordenada. Recomiendo tarea
  sucesora, no cuarta vuelta.
- **R12 (NUEVO) -- la re-programacion del muestreo (`:1520`) esta cubierta por TEXTO, no por
  conducta.** El unico centinela es `assert source.count(live_sampling_seed) == 2`. M5 lo mata, pero
  por conteo de cadenas: mi instrumento confirma que el desenlace del **primer** deadline no cambia
  (`exec_progressing=True`). Como la sonda mata al hijo en el primer `EXEC_PROGRESSING`, ninguna
  ventana posterior se ejerce. Un refactor legitimo de esa linea rompe el gate sin que haya defecto, y
  un mutante que conserve la forma pasa sin que haya cobertura. Es R10 extendido al camino principal.
- **R9 (de r3) -- el margen del negativo de R6 no se deriva del instrumento** (15,6 ms medidos contra
  umbral fijo de 50 ms). Sin cambio.
- **R10 (de r3) -- la fase de post-entrega (`:1541-:1555`) no la cubre ningun negativo permanente**;
  la sonda fija `$PostDeliveryTimeoutSeconds = 0`. AC4 lo verifique yo a mano en r2 y hoy no lo
  sostiene ningun contrato. Sin cambio.
- **R1 (de r1) -- una sola muestra por ventana.** `:1571` asigna `[DateTime]::MaxValue`
  incondicionalmente, tambien cuando `Get-ExecTreeCpuSample` devolvio `$null`. Sin cambio.
- **R8 (de r2) -- `Get-ExecTreeCpuTicks` sigue siendo codigo muerto** (`:438`). Sin cambio.
- **R5 (de r1) -- sin verde de CI, y lo matizo como pediste.** El ancla `e08d9e54` **no tiene ninguna
  corrida de Actions**: barri las 40 mas recientes y no aparece su SHA. Las 8 ultimas corridas estan en
  `failure`. Pero la causa ya no es estructural, y lo he verificado yo abriendo el run que citas:
  `31581821440` (`779f1e36`, conclusion global `failure`) contiene `probe (self-hosted Linux)` y
  `probe (self-hosted Windows)` en **`success` con 8 pasos cada uno**, mientras el control
  `control (GitHub-hosted, se espera BLOQUEADO)` queda en `failure` con **0 pasos**. Es el control en
  el mismo run que hace la medida discriminante. **R5 queda como PENDIENTE, no como imposible.**
- **R2, R3, R4 (de r1), R6 (de r3), S1 (de r2) y S2 (de r3) -- CERRADOS.**

---

## 6. Nota menor sobre la declaracion del contrato

El campo `mutation` ahora nombra un solo mutante (el del signo) mientras los `boundaries` recogen las
salidas de **tres** (guarda, `MaxValue`, signo). Es honesto por defecto -- declara menos de lo que
ejerce, no mas -- asi que no bloquea; pero si algun dia alguien lee `mutation` como el inventario de lo
cubierto, se quedara corto. Anotarlo cuesta una linea.

---

## 7. Lo que esta bien y no quiero que se pierda

- **La sonda ejecuta la semilla, y el mutante de un caracter la mata.** Es literalmente el parche que
  especifique en r3 seccion 4.4, aplicado sin retocar produccion, y funciona.
- **El `mutation` declarado subio de fuerza**: el del signo no toca el texto de la guarda, asi que
  obliga a ejercitar el cableado entero en vez de la ultima linea.
- **Se conservaron los otros dos mutantes** en vez de sustituirlos. Cuesta tiempo de suite y compra
  cobertura; me parece bien gastado.
- **Cuatro `boundaries` nuevos** que son desenlaces del bucle real, no booleanos del helper.
- **31/31 y 74 contratos siguen verdes en clon limpio**, con produccion sin tocar. La remediacion no
  se llevo nada por delante.

---

## 8. Si el Arquitecto o el operador deciden abrir la sucesora

Bucle esperado: **1 remediacion de Codex, solo test.** Mover el ancla de extraccion de
`supervision_loop_outcome_probe` de `$progressSampleSeconds = ...` a un **prefijo** de
`$execHardDeadlineUtc = $deadlineUtc.AddSeconds(`, borrar del preambulo las tres asignaciones que
pasan a ejecutarse (`$execHardDeadlineUtc`, `$progressOutputBytes`, `$progressLedgerBytes`), crear
`$Root/runtime/state/events.jsonl` vacio porque produccion recalcula `$eventsPath`, y anadir el
mutante de `:1485` a los `boundaries`. Criterio por conducta: con `:1485` mutado por el signo, el
negativo debe **morir**. Gates afectados: `test_exec_lease_harness.py`,
`check_falsification_contracts.py`, `run_mailbox_retry_cases.py`, `validate_collaboration_state.py`,
`scan_encoding`, las dos neutralidades. **Re-juicio mio antes del commit de cierre.** Maximo 2
iteraciones antes de escalar al operador.

-- Analista
