# Veredicto Analista -- TASK-0359 r3 (el desenlace del bucle real y la semilla del muestreo)

- Revisor: Analista (voz adversarial independiente)
- Fecha: 2026-08-12, 00:20-00:35 hora local (UTC+2)
- Ancla protocolo: `c3246b2d` (HEAD de `origin/main` al abrir la review; durante la review el remoto
  avanzo a `0370f105` por trabajo ajeno, sin efecto sobre lo juzgado aqui)
- Implementacion juzgada: `ec0b93ce6` -- `fix(TASK-0359): bind liveness to real loop outcome`
- Alcance declarado por el Arquitecto: SOLO hub, sin producto (no se gatea `npm test`)
- Clon limpio con historia completa: `git clone -s` -> `D:/Aegis_Scratch/mapp/t0359r3`,
  `git checkout ec0b93ce`, working tree limpio
- Vuelta: 2 de 2
- Recomendacion de cierre: **CHANGE-REQUIRED**

---

## 0. Resumen en una linea

Los **tres puntos que pediste PASAN por conducta** -- el mutante correcto muere, la asercion es
*muere / no muere* del bucle real, y la clave del mapa distingue un PID reciclado -- pero el negativo
sigue **sembrando a mano lo que produce produccion**: el bucle se ejecuta desde `while`, y las tres
lineas que lo alimentan (`:1493-:1495`) las escribe la propia sonda, de modo que **un mutante de
produccion de UN CARACTER en `:1495` restaura el defecto entero y el negativo se queda verde**.

Respuesta directa a tu pregunta: **si, el negativo distingue el arbol sano del mutante de la guarda.**
Lo que no distingue es el arbol sano del mutante de la **semilla**, y ese devuelve lo mismo en los dos
casos, igual que en r2 pero en otra coordenada.

---

## 1. Reproduccion (gates, por exit code, en clon limpio sobre `ec0b93ce`)

    cd D:/Aegis_Scratch/mapp/t0359r3 && git checkout ec0b93ce

    python scripts/validate_collaboration_state.py --root .           EXIT=0
    python scripts/scan_encoding.py                                   EXIT=0
    python scripts/scan_domain_neutrality.py                          EXIT=0
    powershell -File scripts/scan_domain_neutrality.ps1               EXIT=0
    python scripts/check_falsification_contracts.py                   EXIT=0   (74 DECLARED)
    python scripts/test_exec_lease_harness.py                         EXIT=0   (31/31)
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    EXIT=0

    SUMMARY total=31 passed=31 failed=0

El rojo de r2 (`test_exec_lease_harness.py` EXIT=1, 5 de 5) **no reproduce**: la geometria de la sonda
ahora se deriva del coste medido del instrumento (`instrument_cost_ms` medido 823-1034 ms en esta
maquina) en vez de una constante. El runner ademas ya no aborta en el primer fallo: acumula y publica
`SUMMARY`, asi que un negativo roto deja de esconder a los 30 siguientes. Las dos cosas son mejoras
reales que no pedi.

El inventario paso de 73 a 74 por `NEG-HARNESS-PROCESS-IDENTITY-CPU-SAMPLE`, que es el que dice ser
(runner `scripts/test_exec_lease_harness.py`, 4 boundaries, ejercido por
`test_process_tree_cpu_sample_distinguishes_recycled_pid`).

Estado canonico sano en el ancla. Ninguna claim activa sobre `Area_comun/artifacts/` ni sobre
`Area_comun/mailbox/open/`: las dos filas no liberadas de `CLAIMS.json` son las dos `blocked` de
TASK-0230, con scope sobre `CLAIMS.json#CLAIM-...-0230-*`.

**Sin CI verde.** `gh run list -L 6`: seis corridas consecutivas de `Validate protocol state` en
`failure`, incluidas `cb29c7af` y las tres posteriores. Toda la verificacion de este veredicto es
local, en clon limpio. R5 sigue abierto y no lo tocan estas entregas.

---

## 2. Instrumento propio

Mi sonda no es la del maker. Ejecuta el **bloque de produccion completo**: desde la linea
`$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)` (`:1493`) hasta el final del nodo
`while`, tomado por offsets del AST sobre el texto original:

    $seedIdx = $srcText.IndexOf('$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)')
    $productionBlock = $srcText.Substring($seedIdx, $whileNode.Extent.EndOffset - $seedIdx)
    Invoke-Expression $productionBlock

Con las cuatro funciones reales cargadas por AST, un hijo real que quema CPU en silencio, y solo
`Write-Log` / `Update-ExecLeaseHeartbeat` / `Get-OwnDeliveryEvidence` / `Stop-LeaseProcessTree`
sustituidos. Perillas derivadas del coste medido del instrumento, igual que hace ahora el maker.

Sonda: `D:/Aegis_Scratch/mapp/t0359r3_probe/real_loop_probe.py`.
Control del negativo entregado sobre arboles mutados:
`D:/Aegis_Scratch/mapp/t0359r3_probe/run_delivered_negative_on_mutant.py`.

---

## 3. Los tres puntos de esta vuelta

| # | Punto | Veredicto | Evidencia |
|---|-------|-----------|-----------|
| 1 | AC5 -- el mutante correcto (`if ($false)` en la guarda de muestreo) | **PASS** | sano y mutante dan desenlaces OPUESTOS, ver 3.1 |
| 2 | Asercion sobre el desenlace, no sobre `progressing` del helper | **PASS** | los cuatro `boundaries` son `exec_progressing` / `exec_hung` del stream de log del bucle real, mas `stop_calls`; el booleano del helper desaparecio |
| 3 | R6 -- PID reciclado (`pid + process_start_time_utc`) | **PASS** | clave clavada en produccion `:415-416`; negativo permanente mata el mutante pid-only, ver 3.3 |
| -- | **S2 (NUEVO, bloqueante)** -- la semilla del muestreo sigue puesta a mano | **FALLA** | dos mutantes de produccion de una linea en `:1495` restauran el defecto entero con el negativo VERDE, ver 4 |

### 3.1 Punto 1 -- el mutante de la guarda muere. Medido.

Coordenada en este arbol: la guarda esta en **`:1567`** (en `81f058e6` era `:1565`; el arreglo de R6
anadio una linea). Sonda **entregada**, mismo instrumento, dos arboles:

    DELIVERED probe / arbol sano
      exec_progressing=true  exec_hung=false  stop_calls=0   instrument_cost_ms=967
      LOG: EXEC_PROGRESSING reason=process_tree_cpu_growing next_deadline=...45.46 ...

    DELIVERED probe / mutante :1567  if ($false) {
      exec_progressing=false exec_hung=true   stop_calls=1   instrument_cost_ms=1020
      LOG: EXEC_HUNG pid=55908 reason=no_progress action=terminate ...

No es el mismo valor en los dos casos. La falsacion que firme en r1 y r2 **no reproduce**. Y lo
confirmo con mi instrumento independiente (que ademas ejecuta la semilla de produccion):

    MY instrument / mutante :1567 ->  EXEC_HUNG reason=no_progress, stop_calls=1

El sano no puede pasar por otra senal: `stdout`, `stderr` y `events.jsonl` los crea la sonda vacios y
nadie los escribe; el unico `reason` posible es `process_tree_cpu_growing`, y ahi esta en el log.

### 3.2 Punto 2 -- la asercion mira el desenlace

Los `boundaries` del contrato pasaron de cuatro igualdades sobre `progressing` del helper a:

    assert healthy_outcome["exec_progressing"] is True
    assert healthy_outcome["exec_hung"] is False
    assert mutant_outcome["exec_progressing"] is False
    assert mutant_outcome["exec_hung"] is True

mas `stop_calls == 0` / `== 1`, que ata la **llamada real a la ruta de kill**. Eso es *muere / no
muere*. Es lo que pedi y esta hecho.

Matiz que declaro para que no se lea de mas: el `exec_hung is False` del caso sano vale porque el
`Write-Log` de la sonda mata al hijo en cuanto ve el primer `EXEC_PROGRESSING`. La propiedad
acreditada es exactamente **"sobrevive a su PRIMER deadline"**, que es lo que dice el texto del
contrato. No acredita el segundo deadline ni el techo; eso ya lo firme yo en r2 por conducta.

### 3.3 Punto 3 -- R6 cerrado. Medido.

Produccion `:415-416`:

    $processStartTimeUtc = $treeProcess.StartTime.ToUniversalTime().ToString("o")
    $processKey = "{0}|{1}" -f $processId, $processStartTimeUtc

Sonda entregada sobre los dos arboles (siembra `inflated=6e9` bajo el PID numerico y bajo una
identidad vieja del mismo PID):

    healthy          progressing=true   before=12000000000  after=12040781250  live_ticks=40937500
    mutante pid-only progressing=false  before=12000000000  after=12000156250  live_ticks=37187500

Discrimina, y discrimina por la razon correcta: con la clave de identidad el proceso vivo entra como
entrada nueva y suma sus 4,09 s de CPU; con la clave pid-only queda enmascarado bajo el maximo
inflado y el delta cae a 15,6 ms sobre un proceso que estaba quemando 3,7 s de CPU. **R6 cerrado.**

---

## 4. S2 -- el negativo sigue sembrando lo que produccion calcula (BLOQUEANTE)

La sonda entregada ejecuta **solo el nodo `while`**:

    Invoke-Expression $whileNode.Extent.Text

y escribe ella misma, justo antes, las tres lineas de produccion que alimentan el camino de CPU:

    :1493   $progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)
    :1494   $progressProcessCpuSample = $null
    :1495   $nextProgressCpuSampleUtc = $deadlineUtc.AddSeconds(-$progressSampleSeconds)

Las tres estan **fuera** del extent que la sonda invoca. Es la misma clase de r2 en otra coordenada:
alli el hand-feed era `$before`; aqui es el calendario del muestreo.

### 4.1 Mutante A -- `:1495` -> `[DateTime]::MaxValue` (una linea, produccion)

    MY instrument (ejecuta la semilla de produccion):
      exec_progressing=false  exec_hung=true  stop_calls=1
      LOG: EXEC_HUNG pid=6644 reason=no_progress action=terminate

    NEGATIVO ENTREGADO con HARNESS_PATH apuntando a ese mismo arbol:
      RESULT=PASS  (el negativo NO se entera)

El defecto queda restaurado **entero y permanente**: sin la semilla, la guarda de `:1567` nunca se
cumple, `$progressProcessCpuSample` sigue `$null` al llegar al primer deadline,
`Get-ExecProgressState` recibe `$PreviousProcessCpuSample = $null` y el detector vuelve a depender
EXCLUSIVAMENTE de que crezca un fichero. Es literalmente la condicion que AC5 prohibe.

### 4.2 Mutante A2 -- el mismo, cambiando UN CARACTER (el signo)

    :1495   $nextProgressCpuSampleUtc = $deadlineUtc.AddSeconds($progressSampleSeconds)

Mismo arbol, los dos instrumentos, a la vez:

    MY instrument      exec_progressing=false  exec_hung=true   stop_calls=1
                       LOG: EXEC_HUNG pid=8028 reason=no_progress action=terminate

    DELIVERED probe    exec_progressing=true   exec_hung=false  stop_calls=0
                       LOG: EXEC_PROGRESSING reason=process_tree_cpu_growing ...

**Identico al arbol sano.** Es exactamente la frase que escribi en r2 -- "devuelve lo mismo en los dos
casos" -- reproducida sobre `ec0b93ce`, con un mutante de un caracter que ni siquiera toca la guarda.

### 4.3 Por que esto bloquea y no es solo un residual

El texto del contrato dice: *"...and kill it when the production CPU-sampling block is unreachable."*
El mutante A2 deja el bloque **inalcanzable de hecho** (el calendario nunca vence) sin tocar su texto,
y el negativo no lo mata. El contrato promete una clase mas ancha de la que verifica: cualquier
lectura fria futura dara por cubierto el cableado del muestreo cuando lo cubierto es solo su ultima
linea de guarda. Eso es el falso-seguro que este negativo existe para impedir.

### 4.4 El arreglo, ya ejecutado por mi (4 lineas, SOLO TEST, sin tocar produccion)

En `supervision_loop_outcome_probe`, sustituir la invocacion del nodo por el bloque que empieza en la
semilla, y **borrar** las tres asignaciones que la sonda hace a mano:

    $srcText = [System.IO.File]::ReadAllText($sourcePath)
    $seedIdx = $srcText.IndexOf('$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)')
    if ($seedIdx -lt 0) { throw "missing production seed" }
    Invoke-Expression $srcText.Substring($seedIdx, $whileNode.Extent.EndOffset - $seedIdx)

Con eso mi instrumento mata A, A2 y el de la guarda. Recomiendo ademas que el `mutation` declarado del
contrato sea el **signo de `:1495`** (A2) en vez de -- o ademas de -- `if ($false)`: es estrictamente
mas fuerte, porque deja el texto de la guarda intacto y obliga a ejercitar el cableado entero.

---

## 5. Residuales declarados

- **R9 (NUEVO) -- el margen del negativo de R6 no se deriva del instrumento.** El mutante pid-only
  produjo 15,6 ms de ruido contra un umbral de 50 ms (`FreshSeconds=1`): factor 3,2. Es un margen
  fijo en una maquina concreta, la misma clase que R7. No bloquea; declararlo o derivarlo.
- **R10 (NUEVO) -- la fase de post-entrega no la cubre ningun negativo permanente.** La sonda fija
  `$PostDeliveryTimeoutSeconds = 0`, asi que la rama `:1541-:1555` -- que resetea
  `$progressProcessCpuSample = $null` y REPROGRAMA el muestreo -- nunca se ejecuta. AC4 lo verifique
  yo a mano en r2; hoy no lo sostiene ningun contrato.
- **Cuerpo de la tarea sin seccion r3.** `TASK-0359-*.md` termina en la remediacion r2 y sigue
  diciendo *"El AC5 queda por tanto incumplido y pasa a la vuelta 2"*, describiendo `81f058e6`. Falla
  del lado seguro (subestima), asi que no bloquea, pero hay que escribir la seccion r3 antes de
  cerrar, y que diga solo lo que `ec0b93ce` hace.
- **R1 (de r1, sigue abierto) -- una sola muestra por ventana.** `:1571` asigna
  `$nextProgressCpuSampleUtc = [DateTime]::MaxValue` **incondicionalmente**, tambien cuando
  `Get-ExecTreeCpuSample` devolvio `$null`. Un hipo de CIM en la unica lectura de la ventana juzga ese
  deadline con el criterio viejo. Falla cerrado, sin reintento, sin cobertura.
- **R7 (de r2) -- coste del instrumento en la ruta de decision.** Medido 823-1034 ms por muestra hoy
  (2,2 s en r2). La sonda ya lo mide y deriva su geometria de el: es la correccion que pedi. En
  produccion (`Fresh=15 s`) hay margen.
- **R8 (de r2) -- `Get-ExecTreeCpuTicks` sigue siendo codigo muerto** (`:438`), sin llamadores.
- **R5 (de r1) -- sigue vigente y peor:** seis corridas seguidas de CI en `failure`, ninguna verde
  para esta entrega ni para las anteriores.
- **R2, R3, R4 (de r1) -- CERRADOS**, sin cambio respecto a r2.
- **R6 -- CERRADO** en esta vuelta.

---

## 6. Que tendria que cambiar para que yo cierre

1. **Que el negativo ejecute la semilla de produccion**, no la escriba. El parche exacto esta en 4.4,
   son cuatro lineas y no toca produccion. Criterio de aceptacion por conducta: con `:1495` mutado a
   `AddSeconds($progressSampleSeconds)` (un caracter), el negativo debe **morir**.
2. **Que el `mutation` declarado del contrato sea el de la semilla** (o incluya los dos), para que el
   texto del contrato deje de prometer mas clase de la que verifica.
3. **Escribir la seccion r3 del cuerpo de la tarea** describiendo `ec0b93ce` y retirando la frase que
   declara AC5 incumplido.

**Bucle de arreglo esperado:** 1 remediacion de Codex, **solo test** (`scripts/test_exec_lease_harness.py`)
mas el texto del contrato en `Area_comun/protocol/FALSIFICATION_CONTRACTS.json` si la cadena de
mutacion esta registrada alli, y el cuerpo de `Area_comun/tasks/TASK-0359-*.md`. Sin cambio de
produccion. Gates afectados: `python scripts/test_exec_lease_harness.py`,
`python scripts/check_falsification_contracts.py`,
`python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`python scripts/validate_collaboration_state.py --root .`, `scan_encoding`, y las dos neutralidades.
**Re-juicio mio antes del commit de cierre.**

**Presupuesto:** esta era la **vuelta 2 de 2**. Con esto se agota el limite de dos iteraciones que
fijaste, asi que **la decision de conceder una tercera vuelta o cerrar con el residual abierto es del
operador humano**, no mia. Lo que si digo, para que esa decision sea barata: el arreglo esta
completamente especificado, es de cuatro lineas de test, ya lo ejecute yo y mata los tres mutantes.

---

## 7. Lo que esta bien y no quiero que se pierda

- **El bucle real, ejecutado de verdad.** `Invoke-Expression $whileNode.Extent.Text` con las cuatro
  funciones reales, un hijo real y stubs solo en los bordes es la forma correcta. El problema es
  donde empieza el extent, no el metodo.
- **La geometria derivada del instrumento.** Medir `instrument_cost_ms` y derivar de el la vida del
  workload, `ProgressFresh` y `ExecTimeout` es exactamente lo que pedi en r2 y cierra el rojo
  determinista sin sumar constantes al azar.
- **El runner acumula fallos y publica `SUMMARY`.** Antes, un negativo roto abortaba la suite y
  escondia a los 30 siguientes; ese defecto de instrumento se llevo por delante el gate entero en r2.
  Esto lo arregla para todo el tablero, no solo para esta tarea.
- **`stop_calls` como asercion.** Atar la llamada real a la ruta de kill, y no solo la linea de log,
  es mejor de lo que pedi.
- **R6 clavado a `pid|process_start_time_utc`**, coherente con como el resto del arnes ya distinguia
  un PID reciclado.

-- Analista
