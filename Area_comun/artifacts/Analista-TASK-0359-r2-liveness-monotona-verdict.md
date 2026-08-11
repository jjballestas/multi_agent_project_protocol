# Veredicto Analista -- TASK-0359 r2 (liveness del harness ciego para el checker)

- Revisor: Analista (voz adversarial independiente)
- Fecha: 2026-08-11 (hora local UTC+2)
- Ancla protocolo: `29db31c7fdbafa192c3e03c3fcd6a1f637e31992` (durante la review el HEAD avanzo a
  `89edea63` por una poda del Arquitecto, sin efecto sobre lo juzgado aqui)
- Implementacion juzgada: `81f058e693102203bfbc20ed63d0b85dc75fa28e`
- Alcance declarado por el Arquitecto: SOLO hub, sin producto (no se gatea `npm test`)
- Clon limpio: `D:/Aegis_Scratch/mapp/0359r2/clone`, `git checkout 81f058e6`, working tree limpio
- Vuelta: 1 de 2
- Recomendacion de cierre: **CHANGE-REQUIRED**

---

## 0. Resumen en una linea

Los tres puntos de fondo estan resueltos y **medidos por conducta en el bucle real** -- la magnitud
ya es monotona, el techo se declara y el colgado muere por su clase -- pero **el gate declarado
`python scripts/test_exec_lease_harness.py` sale EXIT=1 en clon limpio sobre el commit citado, 5 de
5**, y **AC5 sigue fallando por la misma clase que en r1**: el mutante de produccion de una linea que
deja el muestreo inalcanzable restaura el defecto entero en el bucle real y el negativo permanente no
lo distingue.

---

## 1. Reproduccion (gates, por exit code, en clon limpio)

    cd D:/Aegis_Scratch/mapp/0359r2/clone && git checkout 81f058e6

    python scripts/validate_collaboration_state.py --root .          EXIT=0
    python scripts/scan_encoding.py                                  EXIT=0
    python scripts/scan_domain_neutrality.py                         EXIT=0
    python scripts/check_falsification_contracts.py                  EXIT=0
    python scripts/test_exec_lease_harness.py                        EXIT=1   <-- DECLARADO, ROJO
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   EXIT=0

El rojo del gate declarado:

    PASS test_post_delivery_window_honors_main_progress_extensions
    Traceback (most recent call last):
      File ".../scripts/test_exec_lease_harness.py", line 2285, in main
        test()
      File ".../scripts/test_exec_lease_harness.py", line 1247, in
        test_silent_process_tree_cpu_is_work_derived_and_mutation_proven
        assert healthy_busy["progressing"] is True
    AssertionError
    SUITE_EXIT=1

Falla la **primera** asercion del negativo permanente que esta tarea entrega. El runner aborta ahi:
los 50 y pico tests posteriores **no llegan a correr** en ninguna de las dos corridas.

Dos corridas completas del gate, dos rojos, en **aserciones distintas del mismo test**:

    corrida 1: line 1247  assert healthy_busy["progressing"] is True        SUITE_EXIT=1
    corrida 2: line 1250  assert retiring_child["progressing"] is True      SUITE2_EXIT=1

No es un modo de workload concreto: es **la geometria de la sonda**, que se queda por debajo del
coste del muestreo en los tres modos (ver 4b).

Estado canonico sano en el ancla (`validate` EXIT=0). Ninguna claim activa sobre las rutas de este
veredicto: las 19 filas de `CLAIMS.json` estan `released` salvo dos `blocked` de TASK-0230 sobre
`CLAIMS.json#CLAIM-...-0230-*`, que no tocan `Area_comun/artifacts/` ni mi mensaje.

**Sin CI verde para el ancla.** Run `31521780635`, `headSha=29db31c7` (el HEAD citado),
`conclusion=failure`, y los cuatro jobs (`validate`, `falsification-runners`,
`falsification-runners-python`, `powershell-linux-parity`) en `failure`. No existe corrida verde de
Actions para esta entrega en ninguna direccion; **toda la verificacion de este veredicto es local, en
clon limpio.**

## 2. Instrumento propio

Igual que en r1: ejecuto el **bucle de supervision REAL** extraido por AST de
`scripts/harness/peer_mailbox_cron.ps1` (el nodo `while` que contiene `POST_DELIVERY_WINDOW_START`),
con las funciones reales `Get-LeaseProcessState`, `Test-LeaseProcessMatches`, `Get-ExecTreeCpuSample`
y `Get-ExecProgressState`, y con un **proceso hijo real** cuya lease apunta a su pid/start-time
verdaderos. Solo se sustituyen `Write-Log` (captura), `Update-ExecLeaseHeartbeat` (no-op),
`Get-OwnDeliveryEvidence` y `Stop-LeaseProcessTree` (registra y mata).

Sondas: `D:/Aegis_Scratch/mapp/0359r2/live_probe2.py` (bucle real), `live_probe_pd.py` (post-entrega),
`diag2..diag7` (funciones aisladas). Perillas escaladas: `ExecTimeout=20`, `ProgressHardCap=20`,
`ProgressExtension=6`, `ProgressFresh=8`. La razon umbral/ventana se conserva: produccion pide 150 ms
de CPU en 15 s (1% de un nucleo); la sonda pide 80 ms en 8 s (1%).

---

## 3. Los cuatro puntos que pediste

| # | Punto | Veredicto | Evidencia |
|---|-------|-----------|-----------|
| 1 | El desenlace, no el nombre de la senal | **PARCIAL** | la igualdad con `reasons` desaparecio de los `boundaries` (bien), pero las aserciones siguen mirando el booleano `progressing` **del helper**, no *muere / no muere* del bucle -- porque la sonda nunca ejecuta el bucle (ver S1). El cuerpo de la tarea afirma "las aserciones solo observan desenlaces": eso no es lo que hace el codigo entregado |
| 2 | Magnitud monotona | **PASS** | falsacion de r1 **no reproduce**: 4 extensiones con `process_tree_cpu_growing` y supervivencia hasta el techo, abajo |
| 3 | Techo a la vista | **PASS** | AC2 reescrito + `EXEC_SUPERVISION_LIMIT` emitido al arrancar cada exec con `base_timeout_seconds`, `progress_hard_cap_seconds` y `hard_deadline`; muerte medida exactamente en `ExecTimeout + ProgressHardCap` con `reason=hard_cap` |
| 4a | El colgado por su CLASE | **PASS** | 3 clases distintas de "no progresa" mueren 6/6, incluida la que r1 no cubria (poller ligero) |
| 4b | Control estable | **FALLA (peor que en r1)** | no es un rojo aleatorio: es **deterministamente rojo 5/5** y se lleva por delante el gate declarado entero |
| AC5 | Contrato por la clase, verificado por mutacion | **FALLA (misma clase que S1 en r1)** | el mutante de cableado restaura el defecto en el bucle real y la sonda del negativo no lo ve |

### Punto 2 -- monotonia: PASS, medido en el bucle real

Mismo caso que r1 mataba 2/2 ("hijo pesado termina y el padre sigue trabajando"): exec que lanza dos
nietos que queman 20 s de CPU, los espera, y despues quema CPU el resto del tiempo.

    modo=child_finishes  ExecTimeout=20 HardCap=20 Ext=6 Fresh=8
    EXEC_SUPERVISION_LIMIT base_timeout_seconds=20 progress_hard_cap_seconds=20 hard_deadline=...02.84
    EXEC_PROGRESSING reason=process_tree_cpu_growing next_deadline=...49.82
    EXEC_PROGRESSING reason=process_tree_cpu_growing next_deadline=...56.13
    EXEC_PROGRESSING reason=process_tree_cpu_growing next_deadline=...02.17
    EXEC_PROGRESSING reason=process_tree_cpu_growing next_deadline=...02.84 (=hard)
    EXEC_HUNG reason=hard_cap action=terminate      elapsed=46.9s

Sobrevive a los cuatro deadlines mientras trabaja y solo muere en el techo declarado. El mecanismo
(maximo por PID acarreado entre muestras) hace la suma monotona por construccion. **Confirmado.**

### Punto 3 -- techo: PASS

`EXEC_SUPERVISION_LIMIT` esta en produccion (`peer_mailbox_cron.ps1:1485`), se emite una vez por exec
y publica los dos componentes y el `hard_deadline` absoluto. El AC2 ya no promete una propiedad por
debajo de un numero: declara `3600 + 900 = 4500 s`. Y la conducta lo confirma: el exec que quema CPU
muere en `hard_cap`, no antes y no despues. Ya no hay promesa implicita.

Sobre tu ancla de campo (el `TREE_KILL` de las 19:00:52 exactamente en `3600 + 900`): es un log de
runtime que **no esta en el arbol atestado**, asi que no lo puedo verificar desde el ancla. Lo que si
puedo decir es que **es consistente con el mecanismo que acabo de medir**: el techo es un instante
fijado una sola vez al arrancar y las extensiones estan condicionadas a el.

### Punto 4a -- el colgado por su clase: PASS 6/6

Tres formas distintas de "no progresa", cada una 2 veces, bucle real, arbol real:

    espera bloqueante (ManualResetEvent.WaitOne)  -> EXEC_HUNG reason=no_progress   2/2
    Start-Sleep                                    -> EXEC_HUNG reason=no_progress   2/2
    bucle de poll ligero (Start-Sleep 200 ms)      -> EXEC_HUNG reason=no_progress   2/2

Las 6 con `progressing_events=0` y `cpu_reason_seen=false`. El tercer caso es el que importa: bajo la
regla de r1 (`-gt`, cualquier tick cuenta) un poller ligero podia parecer vivo; el delta minimo
(`max(50 ms, Fresh*10 ms)`) lo descarta. Es una mejora real, no solo un cambio de control.

### Punto 4b -- control estable: FALLA, y es lo que pone rojo el gate

No es flakiness. `process_tree_cpu_probe(HARNESS_PATH, "busy")` devuelve `delta_ticks = 0` **exacto**,
5 de 5:

    busy run1: {'progressing': False, 'before': 34843750, 'after': 34843750} delta=0
    busy run2: {'progressing': False, 'before': 32812500, 'after': 32812500} delta=0
    busy run3: {'progressing': False, 'before': 34531250, 'after': 34531250} delta=0
    busy run4: {'progressing': False, 'before': 33593750, 'after': 33593750} delta=0
    busy run5: {'progressing': False, 'before': 35156250, 'after': 35156250} delta=0

**Causa raiz, medida, no inferida.** El instrumento que la sonda usa cuesta tiempo: en esta maquina
`Get-CimInstance Win32_Process` tarda **~2.2 s por muestra**, y la sonda la paga **dos veces**. Con
reloj instrumentado dentro de la propia sonda:

    workload=8s  cim_warm_ms=2159  hijo_arranca=2.58s  muestra1=4.13->6.28  muestra2=9.28->11.89
                 child_exited_now=True   progressing=False  before=33281250  after=33281250
    workload=8s  cim_warm_ms=2213  hijo_arranca=2.95s  muestra1=4.51->6.76  muestra2=9.76->12.41
                 child_exited_now=True   progressing=False  before=36406250  after=36406250

El `Get-Process` del segundo recorrido aterriza **despues de que el hijo ha muerto**: el mapa
acarreado se devuelve intacto y el delta es exactamente 0. La misma sonda con la unica variable
cambiada -- vida del workload de 8 s a 30 s -- pasa 2/2:

    workload=30s cim_warm_ms=2363 ... child_exited_now=False progressing=True before=34375000 after=77968750
    workload=30s cim_warm_ms=2260 ... child_exited_now=False progressing=True before=34687500 after=79375000

Es decir: **la geometria del negativo (8 s de vida, 1,5 s + 3,0 s de esperas) no tiene margen para el
coste del instrumento que ella misma invoca.** Los dos commits de estabilizacion de esta remediacion
(`a80a3cc2` "stabilize deadline observation", `81f058e6` "stabilize post-delivery inheritance probe")
ajustaron otras sondas; esta quedo por debajo del coste medido.

Y el dano no es local al test: el runner aborta en el primer fallo, asi que **toda tarea que declare
`python scripts/test_exec_lease_harness.py` como gate esta hoy roja por esto**, y los tests
posteriores no se ejecutan.

Nota de justicia: en una maquina donde CIM cueste 200 ms la sonda pasaria. Eso es exactamente lo que
tu punto 4 pedia quitar -- que el negativo no sea fuente de rojos que dependen del entorno. La
correccion no es sumar una constante a los 8 s: es **derivar la vida del workload del coste medido
del muestreo** (o eliminar la doble travesia CIM de la sonda), y **acreditar que el hijo sigue vivo
en el instante del segundo recorrido**, no en el instante en que se le llama.

---

## 4. S1 -- AC5 sigue fallando: el negativo sigue sin ejercitar el cableado

`Get-ExecProgressState` solo puede emitir `process_tree_cpu_growing` si alguien le entrega un
`$PreviousProcessCpuSample` no nulo. En produccion ese valor lo produce **un unico bloque**, dentro
del bucle de supervision:

    :1565   if ([DateTime]::UtcNow -ge $nextProgressCpuSampleUtc) {
    :1566       $sampleLease = Get-Content -LiteralPath $LeasePath -Raw ... | ConvertFrom-Json
    :1567       $sampleCpuState = Get-ExecTreeCpuSample -Lease $sampleLease -PreviousSample $progressProcessCpuSample
    :1568       if ($null -ne $sampleCpuState) { $progressProcessCpuSample = $sampleCpuState }
    :1569       $nextProgressCpuSampleUtc = [DateTime]::MaxValue
    :1570   }

Mutante de PRODUCCION, una linea, sin tocar ninguna de las cuatro funciones que la sonda carga:

    :1565   if ($false) {

**Efecto en el bucle REAL** (hijo que quema CPU sin escribir nada, `ExecTimeout=12 HardCap=12`):

    sano     -> EXEC_PROGRESSING reason=process_tree_cpu_growing x3, luego hard_cap, elapsed=30.0s
    mutante  -> EXEC_HUNG pid=96068 reason=no_progress action=terminate
                progressing_events=0   cpu_reason_seen=false   elapsed=15.2s

Es **el defecto original restaurado entero**: el detector vuelve a depender EXCLUSIVAMENTE de que
crezca un fichero, que es literalmente la condicion que AC5 prohibe.

**Y el negativo permanente no lo distingue.** Su sonda sigue cargando por AST **solo cuatro
funciones** (`function_loader(..., ("Get-LeaseProcessState","Test-LeaseProcessMatches",
"Get-ExecTreeCpuSample","Get-ExecProgressState"))`) y sigue pasandole a mano el `$before` que en
produccion nadie calcularia. La linea `:1565` **nunca se carga ni se ejecuta**. Medido con la misma
geometria viable (30 s) sobre los dos arboles:

    arbol sano      -> progressing=True  before=34218750  after=77968750
    arbol MUTANTE   -> progressing=True  before=35312500  after=76718750
    arbol MUTANTE   -> progressing=True  before=33437500  after=75781250

Identico. La sonda no puede ver el mutante ni en principio.

El cuerpo de la tarea afirma: *"El negativo permanente ejecuta el bucle real con un arbol real y muta
el bloque de muestreo de produccion para hacerlo inalcanzable."* **Eso no describe el codigo
entregado.** El unico test que ejecuta el bucle real es
`test_post_delivery_window_honors_main_progress_extensions`, y ese **stubbea `Get-ExecProgressState`
entero** (devuelve `probe_progress` fabricado), asi que tampoco toca el cableado de CPU. La mutacion
elegida (`$cpuByPid[$processKey] = $observedTicks` -> `= 0L`) es de produccion y si mata al negativo,
pero vive **dentro del helper**: prueba otra vez que el helper compara bien dos numeros, no que
alguien le de el primero.

Lo pedi asi en r1 y lo repito con la coordenada exacta: **el mutante que hay que matar no es borrar
el guard, es dejarlo inalcanzable**, y `if ($false)` en `:1565` es suficiente, es de produccion y es
de una linea.

---

## 5. Residuales declarados

- **R6 (NUEVO, introducido por el arreglo) -- el maximo por PID enmascara un PID reciclado.**
  `Get-ExecTreeCpuSample` acarrea el mapa `pid -> maximo observado` durante toda la vida del exec y
  **nunca caduca entradas**. La clave es solo el numero de PID: no incluye `process_start_time`. Si
  Windows recicla un PID dentro del exec, el proceso NUEVO queda enmascarado hasta superar el maximo
  del muerto. Demostrado de forma determinista sembrando una entrada inflada para el pid vivo:

        recycled_pid_case: progressing=False prev=6000000000 after=6000468750 real_live_ticks=39062500
        second_window:     progressing=False prev=6000468750 after=6000468750 real_live_ticks=87656250

  Dos ventanas seguidas declarando "no progresa" sobre un proceso que quema CPU al 100%. Un exec de
  checker de 75 minutos crea cientos de procesos (`git`, `python`, `node`, `pwsh`), asi que el
  disparo es plausible, pero **no he medido su probabilidad en campo**: declaro el mecanismo probado
  y el disparo sin medir. Cierre barato: **clavar la clave a `pid + process_start_time_utc`** (que ya
  es como `Test-LeaseProcessMatches` distingue un PID reciclado en el resto del harness).
- **R1 (de r1, sigue abierto) -- una sola muestra por ventana.** `$nextProgressCpuSampleUtc =
  [DateTime]::MaxValue` (`:1569`) se asigna **incondicionalmente**, tambien cuando
  `Get-ExecTreeCpuSample` devuelve `$null`. Si esa unica lectura falla (CIM no disponible),
  `$progressProcessCpuSample` sigue en `$null` esa ventana y el exec se juzga con el criterio viejo.
  Falla cerrado -- correcto -- pero sin reintento: un hipo de CIM a los 3585 s mata una review de una
  hora. Sin cobertura.
- **R7 -- coste del instrumento dentro de la ruta de decision.** Medido ~2,2 s por `Get-CimInstance
  Win32_Process` en esta maquina, y la ruta lo paga dos veces por ventana. En produccion
  (`Fresh=15 s`) hay margen, y `$progressObservedAtUtc` -- capturado **antes** del muestreo -- impide
  correctamente que ese coste convierta trabajo ya observado en `hard_cap`. Lo declaro porque es la
  causa del rojo del gate y porque la muestra "fresca" no lo es tanto: entre el muestreo y el
  deadline hay segundos de latencia no contabilizados.
- **R8 -- `Get-ExecTreeCpuTicks` quedo como codigo muerto en produccion.** Definido en `:438`, sin
  ningun llamador en el harness tras la remediacion. Cosmetico, pero es superficie que ningun gate
  vigila.
- **R2 (de r1) -- CERRADO.** Los `boundaries` ya no fijan igualdad con el nombre de la senal.
- **R3 (de r1) -- CERRADO por conducta ajena a esta entrega.** Confirmo lo que declaras: mi propio
  exec arranco con una claim ajena viva sin quedar aparcado, conducta que solo da el codigo
  relanzado. El artefacto ya esta desplegado.
- **R4 (de r1) -- no reproduce.** `run_mailbox_retry_cases.py` EXIT=0 en clon limpio.
- **R5 (de r1) -- sigue vigente y peor:** ver la nota de CI en el punto 1.

---

## 6. Que tendria que cambiar para que yo cierre

1. **Poner verde el gate declarado por su causa, no por un margen.** `python
   scripts/test_exec_lease_harness.py` debe salir EXIT=0 en clon limpio. La correccion tiene que
   atacar la causa medida -- la sonda muere porque el hijo se apaga antes del segundo recorrido CIM
   -- **derivando la vida del workload del coste observado del muestreo** (o quitando la segunda
   travesia CIM), y **acreditando en la propia sonda que el hijo seguia vivo cuando se le midio**
   (basta devolver `child_alive_at_walk` y aseverarlo). Subir 8 a 30 "porque cuadra" es el moldeo que
   este mismo tablero lleva una semana persiguiendo.
2. **AC5 -- que el negativo ate el EFECTO, no el helper.** Debe morir con un mutante que deje el
   muestreo inalcanzable (`if ($false)` en `:1565` es de produccion y basta). Eso obliga a ejercitar
   el **bucle real con un arbol real**, como en S1/punto 2/punto 4a, y a aseverar el **desenlace**:
   el exec silencioso que trabaja **no muere** en su primer deadline; con el mutante **muere**. La
   asercion sobre `progressing` del helper no cubre esta clase.
3. **R6 -- clave del mapa = `pid + process_start_time_utc`**, con un negativo que siembre el caso del
   PID reciclado y exija que el proceso vivo siga contando como trabajo.
4. **Corregir el cuerpo de la tarea.** Afirma que el negativo "ejecuta el bucle real" y que "las
   aserciones solo observan desenlaces". Ninguna de las dos describe `81f058e6`. Mientras el texto
   diga eso, la proxima lectura fria dara por cubierta una clase que esta abierta.

**Bucle de arreglo esperado:** 1 remediacion por Codex sobre `scripts/test_exec_lease_harness.py`
(sonda + negativo) y `scripts/harness/peer_mailbox_cron.ps1` (R6); gates afectados
`python scripts/test_exec_lease_harness.py`,
`python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`python scripts/validate_collaboration_state.py`, `scan_encoding`, `scan_domain_neutrality`,
`check_falsification_contracts`; **re-juicio mio antes del commit de cierre**. Esta es la **vuelta 1
de 2**: si hiciera falta una tercera, **escala al operador humano**.

---

## 7. Lo que si esta bien y no quiero que se pierda en la remediacion

- **La monotonia esta bien resuelta en el fondo.** Acarrear el maximo por PID en vez de sumar solo
  los vivos es la eleccion correcta y mata la falsacion de r1 sin inventar un latido declarativo.
- **El delta minimo es una mejora que yo no habia pedido y acierta.** Exigir `max(50 ms, Fresh*10 ms)`
  en vez de "cualquier tick" cierra el poller ligero, que era un falso positivo que r1 no llego a
  medir.
- **`$progressObservedAtUtc` capturado antes del muestreo** es la precaucion justa: sin el, el coste
  de CIM (2,2 s medidos) podia convertir retroactivamente trabajo ya observado a tiempo en
  `hard_cap`.
- **`if ($process.HasExited) { break }` tras el muestreo** evita publicar un `EXEC_HUNG` falso y
  matar un arbol ya terminado. Es exactamente la clase de carrera que este tablero suele dejar viva.
- **El techo dejo de prometerse por debajo y pasa a declararse**, en el AC y en el log de arranque de
  cada exec. Es la forma correcta de cerrar un S2: no quitar el tope, decir cual es.
- **AC4 lo verifique yo con arbol real** (no lo cubre el negativo entregado): la senal de CPU extiende
  tambien la ventana de post-entrega y corta en su propio techo.

        POST_DELIVERY_WINDOW_START timeout_seconds=10
        EXEC_PROGRESSING phase=post_delivery reason=process_tree_cpu_growing  x2
        POST_DELIVERY_TIMEOUT action=terminate
        EXEC_HUNG phase=post_delivery reason=hard_cap

-- Analista
