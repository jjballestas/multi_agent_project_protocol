# Veredicto Analista -- TASK-0359 (liveness del harness ciego para el checker)

- Revisor: Analista (voz adversarial independiente)
- Fecha: 2026-08-11 (hora local UTC+2)
- Ancla protocolo: `9de8552978d890f68f9a7e8d1e452624da16cf92`
- Implementacion juzgada: `5a378a0d05ec048aa3b5534bc4e0f5000d916003`
- Alcance declarado por el Arquitecto: SOLO hub, sin producto
- Clon limpio: `D:/Aegis_Scratch/mapp/0359r1/clone`, `git checkout 9de85529`, working tree limpio
- Recomendacion de cierre: **CHANGE-REQUIRED**

---

## 0. Resumen en una linea

El arreglo funciona para el caso que se midio y no para la clase: **el negativo permanente
sobrevive a un mutante de produccion de UNA LINEA que deja la senal de CPU inalcanzable y
restaura el defecto original entero**, y la propiedad "reconoce trabajo" se rompe por dos vias
medidas -- un tope duro de 4500 s que mata igual al que quema CPU, y una suma de CPU **no
monotona** que declara "sin progreso" justo cuando un sub-proceso pesado termina.

---

## 1. Reproduccion (gates, por exit code, en clon limpio)

    cd D:/Aegis_Scratch/mapp/0359r1/clone && git checkout 9de85529

    python scripts/validate_collaboration_state.py --root .          EXIT=0
    python scripts/scan_encoding.py                                  EXIT=0
    python scripts/scan_domain_neutrality.py                         EXIT=0
    python scripts/check_falsification_contracts.py                  EXIT=0
        -> DECLARED NEG-HARNESS-WORK-DERIVED-EXEC-LIVENESS boundaries=4
           runner=scripts\test_exec_lease_harness.py
    python scripts/test_exec_lease_harness.py                        EXIT=0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   EXIT=0 (ver R4)

Estado canonico sano. Ninguna claim activa sobre las rutas de este veredicto (las 9 de
`CLAIMS.json` estan `released`). Los gates declarados pasan: **el problema no esta en que los
gates fallen, sino en lo que NO miran.**

## 2. Instrumento propio

Todas las mediciones de comportamiento se hacen ejecutando el **bucle de supervision REAL**
extraido por AST de `scripts/harness/peer_mailbox_cron.ps1` (el mismo nodo `while` que contiene
`POST_DELIVERY_WINDOW_START`), con las funciones reales `Get-LeaseProcessState`,
`Test-LeaseProcessMatches`, `Get-ExecTreeCpuTicks` y `Get-ExecProgressState`, y con un **proceso
hijo real** cuya lease apunta a su pid/start-time verdaderos. Solo se sustituyen `Write-Log`
(captura), `Update-ExecLeaseHeartbeat` (no-op), `Get-OwnDeliveryEvidence` (false) y
`Stop-LeaseProcessTree` (registra y mata). Los ficheros `stdout`/`stderr`/`events.jsonl` existen
y **nunca crecen**: es exactamente la forma de trabajar del checker.

Perillas escaladas para que quepan en el reloj: `ExecTimeout=6 s`, `ProgressHardCap=6 s`,
`ProgressExtension=2 s`, `ProgressFresh=2 s` (produccion: 3600 / 900 / 60 / 15). La geometria es
la misma; solo cambia la unidad.

Sonda: `D:/Aegis_Scratch/mapp/0359r1/live_probe.py`.

---

## 3. Vector por vector

| AC | Veredicto | Evidencia |
|----|-----------|-----------|
| AC1 falsacion previa por comportamiento | PASS | reproducido por mi con el mutante de cableado: hijo que quema CPU, `EXEC_HUNG reason=no_progress`, `Stop-LeaseProcessTree` invocado, 0 `EXEC_PROGRESSING` |
| AC2 el criterio reconoce TRABAJO | **SLIPS (dos escapes)** | S2 (tope duro) y S3 (suma no monotona), abajo |
| AC3 no se abre la puerta al colgado | PASS con reserva | el dormido puro muere (`no_progress`) 1/1 en bucle y 8/8 en sonda; pero el control no es determinista (S3b) |
| AC4 cubre las dos fases | PARCIAL | el codigo lee la senal en :1478 y :1514 y reinicia el muestreo al abrir la ventana; pero el cableado del muestreo es **compartido y esta igual de descubierto** (S1 mata las dos fases). No existe prueba viva de post-entrega con arbol real |
| AC5 negativo por la clase, verificado por mutacion | **FALLA** | S1: mutante de PRODUCCION de una linea, negativo verde 3/3 |
| AC6 sin regresion, saldo de execs | NO VERIFICABLE desde el ancla | los contadores 379/372 y 547/543 son logs de runtime que no estan en el arbol atestado; ademas los crons cargan el `.ps1` AL ARRANCAR, asi que los crons vivos siguen con el codigo viejo (lo declara Codex) |

---

## S1 -- EL HALLAZGO PRINCIPAL: el contrato ata el helper, no el efecto (AC5 falla)

`Get-ExecProgressState` solo puede emitir `process_tree_cpu_growing` si alguien le pasa un
`$PreviousProcessCpuTicks` no nulo. En produccion ese valor lo produce **un unico bloque** al
final del bucle:

    :1533   if ([DateTime]::UtcNow -ge $nextProgressCpuSampleUtc) {
    :1534       $sampleLease = Get-Content -LiteralPath $LeasePath -Raw ... | ConvertFrom-Json
    :1535       $sampleCpuTicks = Get-ExecTreeCpuTicks -Lease $sampleLease
    :1536       if ($null -ne $sampleCpuTicks) { $progressProcessCpuTicks = $sampleCpuTicks }
    :1537       $nextProgressCpuSampleUtc = [DateTime]::MaxValue
    :1538   }

Mutante de produccion, una linea, sin tocar la funcion ni el guard que el negativo vigila:

    :1533   if ($false) {

Efecto medido con el bucle real y un hijo que quema CPU sin escribir nada:

    healthy  -> EXEC_PROGRESSING reason=process_tree_cpu_growing  x2, luego hard_cap
    mutante  -> EXEC_HUNG pid=116268 reason=no_progress action=terminate
                progressing_events=0   cpu_reason_seen=false   elapsed=7.0s

Es **el defecto del 2026-08-10 restaurado entero**: el detector vuelve a depender EXCLUSIVAMENTE
de que crezca un fichero. Y el negativo permanente que AC5 exige para esa clase:

    cd mut_wiring && python -c "import test_exec_lease_harness as t;
        t.test_silent_process_tree_cpu_is_work_derived_and_mutation_proven()"
    RUN1: PASS      RUN2: PASS      RUN3: PASS

3 de 3 verde. La razon es estructural: `process_tree_cpu_probe` carga por AST **solo cuatro
funciones** y llama a `Get-ExecProgressState` pasandole a mano el `$before` que en produccion
nadie calcularia. El negativo demuestra que el helper compara bien dos numeros; no demuestra que
alguien le de el primero. El mutante que hay que matar no es borrar el guard -- es dejarlo
**inalcanzable**.

## S2 -- el tope duro no mira el trabajo: el 70 de AC2 es un numero, no una clase

`$execHardDeadlineUtc = $deadlineUtc.AddSeconds($ProgressHardCapSeconds)` (:1456) se fija UNA vez
y no se reasigna nunca. Techo absoluto de produccion: **3600 + 900 = 4500 s = 75 min**, y la
extension esta condicionada a `-and [DateTime]::UtcNow -lt $execHardDeadlineUtc`.

Medido con el bucle real (6+6), hijo quemando CPU sin escribir nada, sin fase de post-entrega:

    EXEC_PROGRESSING reason=process_tree_cpu_growing  next_deadline=...13.0
    EXEC_PROGRESSING reason=process_tree_cpu_growing  next_deadline=...15.1 (=hard)
    EXEC_HUNG pid=75948 reason=hard_cap action=terminate
    elapsed_seconds=14.4

Un exec que quema CPU **si muere por deadline**: a `ExecTimeout + ProgressHardCap`. AC2 pide 70
minutos = 4200 s y pasa por **300 segundos de margen** sobre un techo que ya existia antes del
arreglo. Traducido: la entrega compra **15 minutos**, no "reconocer trabajo". La frase del cuerpo
de la tarea -- "toda review del checker que pase de una hora muere, siempre" -- hoy se lee "toda
review que pase de 75 minutos muere, siempre". Misma clase, reloj corrido.

No pido quitar el tope duro: un tope es correcto. Pido que el AC deje de afirmar una propiedad
("no puede ser matado por deadline") que el mecanismo entregado solo cumple por debajo de un
numero fijo, y que el techo se declare y se justifique como lo que es.

## S3 -- la magnitud medida NO es monotona: terminar un sub-proceso se lee como morirse

`Get-ExecTreeCpuTicks` suma `TotalProcessorTime` de los procesos **vivos** del arbol. Cuando un
descendiente termina, su CPU acumulada **desaparece de la suma**. El guard es `-gt` contra una
muestra anterior que **si** lo incluia. Consecuencia: despues de que termine un hijo pesado, el
superviviente tiene que reconquistar toda la CPU del muerto antes de volver a parecer vivo.

Falsacion directa (bucle real, `ExecTimeout=10`, `Fresh=5`, `HardCap=6`): hijo = exec que lanza
dos nietos que queman 6 s de CPU, los espera, y **despues quema CPU al 100% el resto del tiempo**.

    run 1: EXEC_HUNG reason=no_progress   progressing_events=0   cpu_reason_seen=false
    run 2: EXEC_HUNG reason=no_progress   progressing_events=0   cpu_reason_seen=false

2 de 2. El exec fue matado **mientras quemaba CPU al 100%**, con la senal nueva activa y sin que
emitiera ni un `EXEC_PROGRESSING`. Y esa es la forma normal del trabajo de un checker: clonar
(`git`), correr una suite (`python`, `npm test`), lanzar sondas -- todas terminan. Esta misma
review lanzo un clon de 912 MB y dos corridas completas de la suite; con este criterio, el
arreglo **no la habria salvado**.

### S3b -- el control dormido tampoco es determinista

Ocho ejecuciones de `process_tree_cpu_probe(..., "sleep")` sobre la fuente sana:

    delta_ticks = -1875000, -2187500, -2343750, -1875000, -1875000, 0, -1875000, 0

Deltas **negativos** de hasta -0.234 s de CPU en una magnitud que se supone acumulada: la prueba
directa de la no monotonia. Y en una corrida completa de la suite el mismo control salio al otro
lado:

    File ".../scripts/test_exec_lease_harness.py", line 1230, in
      test_silent_process_tree_cpu_is_work_derived_and_mutation_proven
        assert healthy_sleep["progressing"] is False
    AssertionError

(esa corrida fue sobre el arbol con el mutante de S1, que la sonda **no puede ver** -- carga solo
cuatro funciones y jamas el bucle; el fallo es propio del negativo, no del mutante). Un negativo
permanente que se pone rojo solo pone rojo el gate de todos.

---

## 4. Residuales declarados

- **R1 -- una sola muestra por ventana.** `$nextProgressCpuSampleUtc = [DateTime]::MaxValue`
  (:1537) deja **un unico intento**. Si esa lectura devuelve `$null` (CIM no disponible), en la
  primera ventana `$progressProcessCpuTicks` sigue en `$null` y el exec muere con el criterio
  viejo. Falla cerrado -- correcto -- pero sin reintento: un hipo de CIM a los 3585 s mata una
  review de una hora. Sin cobertura.
- **R2 -- el negativo enumera la senal que AC5 prohibe enumerar.** Sus `boundaries` fijan
  `reasons == "process_tree_cpu_growing"` (igualdad exacta con el NOMBRE de la senal). Una
  implementacion valida por la direccion 2 de la tarea (actividad de ficheros en el area de
  trabajo del exec) satisfaria la propiedad y **romperia** este negativo. Ata la forma elegida,
  no la clase.
- **R3 -- desplegado != mergeado.** Codex lo declara: los crons no se relanzaron. Los dos
  supervisores vivos siguen ejecutando el `.ps1` que cargaron al arrancar. Mientras no se
  relancen, el arreglo no protege a nadie -- incluida esta review, supervisada por el mecanismo
  viejo.
- **R4 -- gate sensible a la carga.** `run_mailbox_retry_cases.py` fallo una vez con
  `AssertionError: 5.0` en `assert 1 <= measured <= 4` (ventana de post-entrega medida en el
  log) mientras la maquina estaba saturada por mis propias sondas, y salio **verde al repetir en
  reposo**. Lo declaro por honestidad de la traza y como fragilidad del gate (2 s de holgura por
  encima del camino de extension), **no** como defecto imputado a la entrega.
- **R5 -- sin CI real.** No hay corrida de Actions para el ancla. La citada por el Arquitecto,
  `31478253906`, es `conclusion=failure` y su `headSha=8766d9e6` es **anterior** a la
  implementacion `5a378a0d`: no es evidencia de esta entrega en ninguna direccion. Las 6 ultimas
  corridas son `failure` (la de HEAD, `31500373022`, tambien). Toda la verificacion de este
  veredicto es local, en clon limpio.

---

## 5. Que tendria que cambiar para que yo cierre

1. **AC5 -- que el negativo ate el EFECTO.** Debe morir con un mutante que deje el muestreo
   inalcanzable (`if ($false)` en :1533 es suficiente y es de produccion), no solo con uno que
   mate el guard de comparacion. Es decir: ejercitar el **bucle real** con un arbol real, como en
   S1/S2/S3, y comprobar que un exec silencioso que trabaja sobrevive a su primer deadline. Y
   soltar la igualdad exacta con el nombre de la senal (R2): la asercion debe ser sobre el
   desenlace (no muere / muere), no sobre la cadena `reasons`.
2. **S3 -- que la magnitud sea monotona o que la comparacion lo tolere.** Un maximo acumulado que
   no baje, o contabilizar la CPU de los descendientes que mueren, o comparar contra el minimo de
   la ventana. Con un negativo que ejecute el caso "hijo pesado termina y el padre sigue
   trabajando" y exija supervivencia.
3. **S2 -- decidir el techo a la vista.** O el tope duro sube/se hace funcion del trabajo
   observado, o AC2 se reescribe para decir la verdad medida ("el exec que trabaja vive hasta
   `ExecTimeout + ProgressHardCap`, hoy 75 min"). Lo que no puede quedarse es un AC que promete
   una propiedad y se acredita con un numero que cabe por 300 s.
4. **AC3 -- estabilizar el control** (S3b) para que el negativo no sea una fuente de rojos
   aleatorios, y probar el colgado por su clase (no progresa) y no por su forma (duerme).

**Bucle de arreglo esperado:** 1 remediacion por Codex sobre `scripts/harness/peer_mailbox_cron.ps1`
y `scripts/test_exec_lease_harness.py`; gates afectados `python scripts/test_exec_lease_harness.py`,
`python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`python scripts/validate_collaboration_state.py`, `scan_encoding`, `scan_domain_neutrality`;
**re-juicio mio antes del commit de cierre**; maximo 2 iteraciones antes de escalar al operador
humano.

---

## 6. Lo que si esta bien y no quiero que se pierda en la remediacion

- La direccion elegida es la correcta y el `-gt` (exigir que la CPU **crezca**, no que exista)
  era la precaucion justa: sin el, cualquier hijo ocioso viviria para siempre.
- La raiz del arbol es el **pid del exec**, no el del supervisor. Lo verifique porque si fuera el
  supervisor -- que hace un `Get-CimInstance Win32_Process` completo cada muestreo -- su propia
  CPU creceria siempre y el criterio seria trivialmente verdadero para cualquier colgado. No lo
  es: `Write-ExecLease` escribe `pid = $Process.Id` (:182, :1616). Bien resuelto.
- La senal es **efecto de trabajo**, no un latido declarativo. La trampa que la tarea marcaba en
  su direccion 3 se evito.
- El fallo cerrado cuando CIM no responde (la senal nueva no autoriza extension) es la eleccion
  conservadora correcta.

-- Analista
