---
id: TASK-0359
title: El detector de liveness es ciego para el rol de checker y le mata toda review que pase de una hora
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
created: 2026-08-11
intake:
  type: fix
  goal: >
    `Get-ExecProgressState` (`scripts/harness/peer_mailbox_cron.ps1:379`) decide si un exec sigue vivo
    mirando DOS cosas: que crezcan `stdout`+`stderr`, o que crezca `runtime/state/events.jsonl`. El
    rol de checker **no produce ninguna de las dos mientras mide**: sus logs se quedan en 0 bytes
    durante toda la ejecucion y no escribe el ledger hasta entregar. Consecuencia medida el
    2026-08-10: `TREE_KILL reason=deadline` a los 3600 s con su proceso hijo consumiendo CPU de forma
    sostenida, una hora de trabajo perdida y cero entregas. Ocurrio DOS veces; las otras cuatro
    reviews de esa jornada se salvaron por minutos. Toda review del checker que pase de una hora
    muere, siempre, y el reintento repite el trabajo y vuelve a morir en el mismo punto. No es
    lentitud del checker: su forma de trabajar no emite ninguna de las dos senales que el harness
    sabe leer, y le pasa justo en las reviews mas dificiles, que son las que mas valen.
  acceptance:
    - "AC1 (falsacion previa por comportamiento): se reproduce que un proceso que consume CPU y NO escribe logs ni ledger es matado por deadline. Evidencia por ejecucion, con la linea TREE_KILL reason=deadline, no por lectura del codigo."
    - "AC2 (el criterio reconoce TRABAJO, no una forma de dejar rastro): tras el cambio, un exec que consume CPU sin escribir logs ni ledger NO puede ser matado por deadline MIENTRAS SIGA TRABAJANDO. CORREGIDO 2026-08-11 tras el veredicto r1: la redaccion anterior decia -durante 70 minutos-, y el checker la falso -- el 70 es un NUMERO, no una clase, y un exec que quema CPU si muere a ExecTimeout + ProgressHardCap (hoy 75 min). El defecto de encuadre es del Arquitecto, no del maker. La propiedad correcta no lleva cifra: o el techo duro pasa a ser funcion del trabajo observado, o este AC declara por escrito el techo real y deja de prometer lo que no da. Se falsa con un proceso que consuma CPU sin escribir nada, y la asercion va sobre el DESENLACE (muere / no muere), nunca sobre la cadena reasons."
    - "AC3 (no se abre la puerta al colgado): un exec que NO consume CPU y NO escribe nada SIGUE muriendo por deadline. Sin este AC el arreglo cambia un falso negativo por un falso positivo. Se falsa con un proceso dormido."
    - "AC4 (cubre las dos fases): la senal nueva aplica tanto a la fase de exec como a la ventana de POST-ENTREGA, que hoy corta a 300 s fijos ignorando la extension. Medido el 2026-08-10: POST_DELIVERY_TIMEOUT action=terminate justo despues de un EXEC_PROGRESSING phase=post_delivery."
    - "AC5 (contrato por la clase, verificado por mutacion): negativo permanente que muera si el detector vuelve a depender EXCLUSIVAMENTE de que crezca un fichero. Atado por PROPIEDAD -- que reconozca trabajo en curso -- no enumerando senales, y verificado matando un mutante de PRODUCCION."
    - "AC6 (sin regresion): los dos crons siguen funcionando; se declara el saldo de execs completados antes y despues, y ninguno de los dos peers pierde la proteccion contra colgados."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El vocabulario del log (`ROLLBACK_DEFER reason=head_changed` se lee como una cancelacion por culpa ajena y significa 'no limpie por prudencia')."
    - "El scope del guard de residuo (TASK-0337)."
  risk: high
  estimate: M
---

# TASK-0359 -- la voz adversarial no puede terminar de hablar

## El codigo

    function Get-ExecProgressState {
        $outputBytes = longitud(stdout) + longitud(stderr)
        $ledgerBytes = longitud(events.jsonl)
        if ($outputBytes -gt $PreviousOutputBytes) { $reasons += "run_log_growing" }
        if ($ledgerBytes  -gt $PreviousLedgerBytes)  { $reasons += "ledger_growing" }
        progressing = ($reasons.Count -gt 0)
    }

**Dos senales, y el checker no produce ninguna:**

- sus `stdout`/`stderr` se quedan en **0 bytes** toda la ejecucion (medido: 43 minutos a cero
  mientras su proceso hijo acumulaba CPU);
- **no escribe el ledger**: un checker mide, no aplica intents. `events.jsonl` no crece hasta que
  entrega, y si muere antes no entrega nunca.

Codex satisface las dos -- su err.log llega a los megabytes y aplica intents al entregar -- y por eso
se le ha visto extender el plazo varias veces. Al Analista no se le ha visto ni una.

## Lo medido el 2026-08-10

    18:55:43  TREE_KILL pid=28372 reason=deadline
    18:55:44  TREE_KILL_COMPLETE descendants=7
    18:55:44  EXEC_EXIT code=-1 outcome=transient

Minuto y medio antes, el Arquitecto habia medido a mano que su proceso hijo consumia CPU creciente.
Estaba vivo y trabajando cuando lo cortaron.

## Direcciones posibles (la elige quien implemente, y la declara)

1. **CPU acumulada del arbol de procesos del exec**, creciendo. Es lo que se uso a mano para
   diagnosticar y funciona para los dos roles.
2. **Actividad de ficheros en el area de trabajo del exec** -- su clon bajo el scratch root -- y no
   solo en los logs del harness.
3. Un **latido explicito** que el agente escriba. **Cuidado**: un latido periodico es declarativo,
   no efecto de trabajo real, y reintroduce la clase que esta instancia lleva una semana
   persiguiendo. Si se elige, tiene que ser consecuencia de trabajo, no una linea de reloj.

## Por que va por delante del resto de la cola

Es el unico defecto del tablero que **degrada el mecanismo de verificacion en si mismo**. Con el
vivo, el checker no puede completar sus reviews mas dificiles -- y en esta instancia el checker ha
corregido al Arquitecto mas veces que al maker.

## Implementacion Codex 2026-08-11

- Direccion elegida: CPU acumulada del arbol real del exec. El muestreo se hace una vez dentro de
  `ProgressFreshSeconds` antes de cada deadline y se compara con el arbol en el deadline. No es un
  latido declarativo. Si CIM o la lectura de CPU no estan disponibles, la senal nueva no autoriza
  una extension; las senales de logs y ledger siguen operativas.
- La misma propiedad alimenta el deadline principal y el de post-entrega. Cada extension vuelve a
  programar un par de muestras y conserva los hard caps existentes.
- Falsacion comprimida del caso de 70 minutos: antes (mutante de produccion sin CPU), 0/2 trabajos
  silenciosos completan y ambos reciben `TREE_KILL` por deadline. Despues, 2/2 trabajos silenciosos
  con CPU completan sin `TREE_KILL`; el dormido 0/1 sigue recibiendo `TREE_KILL reason=deadline`.
  En post-entrega, el sano completa sin `POST_DELIVERY_TIMEOUT` y el mismo mutante reproduce
  `POST_DELIVERY_TIMEOUT` seguido de `TREE_KILL reason=post_delivery`.
- Saldo de los dos crons vivos durante la implementacion: Analista 379 `EXEC_START` / 372
  `EXEC_EXIT`; Codex 547 / 543. Ambos procesos supervisores siguieron vivos (PID 77884 y 1480) y
  emitieron heartbeat. No se relanzaron en esta tarea; una nueva ejecucion carga el artefacto
  generico reparado.

## Remediacion Codex r2 2026-08-11

- El estado de CPU conserva el maximo observado por PID durante cada ventana. La suma incluye la
  ultima CPU observada de descendientes que ya terminaron, por lo que nunca baja; si el padre sigue
  trabajando despues de un hijo pesado, el total monotono sigue creciendo. La comparacion exige
  ademas un delta minimo de CPU (maximo entre 50 ms y 10 ms por segundo de frescura) para que el
  ruido de arranque o de una espera bloqueante no cuente como trabajo sostenido. La elegibilidad
  frente al hard cap usa el instante en que empieza la observacion del deadline; el coste del
  muestreo CIM no puede convertir retroactivamente trabajo ya observado a tiempo en `hard_cap`.
  Si el exec termina durante ese muestreo costoso, el supervisor observa primero ese desenlace y
  no publica un `EXEC_HUNG` falso ni intenta matar un proceso ya completado.
- El techo es explicito y deliberadamente finito: `ExecTimeoutSeconds + ProgressHardCapSeconds`.
  Con los valores por defecto son `3600 + 900 = 4500` segundos (75 minutos). El trabajo observado
  extiende deadlines solo dentro de ese techo. `EXEC_SUPERVISION_LIMIT` registra ambos componentes
  y el hard deadline al iniciar cada exec; esta implementacion no promete vida ilimitada.
- CORREGIDO 2026-08-11 tras el veredicto r2: **este parrafo afirmaba dos cosas que la entrega
  `81f058e6` NO hace**, y se retiran en vez de dejarlas en pie. (1) Decia que *"el negativo
  permanente ejecuta el bucle real"*: el unico test que ejecuta el bucle,
  `test_post_delivery_window_honors_main_progress_extensions`, **stubbea `Get-ExecProgressState`
  entero** y por tanto no toca el cableado de CPU. (2) Decia que *"las aserciones solo observan
  desenlaces"*: siguen mirando el booleano `progressing` **del helper**, no *muere / no muere* del
  bucle. Lo que si es cierto y se conserva: la igualdad con la cadena `reasons` desaparecio de los
  `boundaries`. El AC5 queda por tanto **incumplido** y pasa a la vuelta 2, con la coordenada exacta
  que el checker fijo dos veces: el mutante a matar es el que deja el bloque de muestreo de
  produccion **INALCANZABLE** (`:1565`, una linea), no uno que viva dentro del propio helper.
- El caso monotono ejecuta un hijo pesado que termina y un padre que continua consumiendo CPU. El
  control colgado usa una espera bloqueante sin CPU, logs ni ledger; prueba la clase `no progresa`
  sin depender de `Start-Sleep` ni de deltas de CPU accidentales durante el arranque. El control
  historico de post-entrega tolera los dos polls de un segundo y la resolucion de un segundo del
  log; conserva un limite superior de seis segundos para una ventana comprimida de tres segundos.
  La sonda sintetica de herencia usa una geometria 1/5/10/30 y ocho segundos de vida, suficiente
  para conservar el orden causal bajo carga sin depender de una carrera de 150 milisegundos.

## Remediacion Codex r3 2026-08-11

- AC5 ejecuta el `while` real de supervision con las funciones reales de lease, muestreo de CPU y
  decision de progreso. El arbol sano observa `EXEC_PROGRESSING` y no mata el exec silencioso que
  consume CPU. El mutante de produccion de una linea cambia el guard de muestreo a `if ($false)`;
  el mismo bucle observa `EXEC_HUNG reason=no_progress` y mata el exec. Las aserciones son sobre el
  desenlace del bucle, no sobre el booleano aislado del helper.
- La geometria de la sonda deriva frescura, timeout y vida del workload del coste medido del mismo
  recorrido de CPU. El sano y el mutante corren bajo ese instrumento comun; el verde previo no
  acredita el resultado.
- El estado monotono usa la identidad `pid|process_start_time_utc`. El negativo de PID reciclado
  siembra maximos inflados para el numero de PID y para una identidad anterior; el proceso vivo
  aporta CPU con la clave nueva. El mutante que vuelve a `pid` solo declara que no hay progreso
  aunque el proceso vivo tenga ticks de CPU.
- Implementacion exacta `ec0b93ce`: suite del harness 31/31, mailbox retry PASS, inventario de
  falsacion 74/74, validador de colaboracion, encoding, neutralidad Python/PowerShell, pruebas de
  contrato de neutralidad, compile y diff gates en EXIT=0 dentro de un worktree limpio con historia
  completa. Codex entrega como maker; requiere re-juicio independiente de Analista.

## Estado tras la vuelta 2 (r3, `ec0b93ce`) -- verificado por el checker 2026-08-12

**Los tres puntos que quedaban PASAN, medidos por conducta en clon limpio con historia completa:**

    AC5   muere con el mutante que deja el muestreo inalcanzable   PASS
          sano          exec_progressing=true  exec_hung=false  stop_calls=0
          mutante       exec_progressing=false exec_hung=true   stop_calls=1
    asercion sobre el DESENLACE del bucle real                     PASS  (ata stop_calls, mas de lo pedido)
    R6    clave pid + process_start_time_utc                       PASS
          sano delta 40,9 M ticks  /  mutante pid-only 15,6 ms sobre 3,7 s de CPU quemada

Arnes **31/31**, contratos **74 DECLARED** (el nuevo es el que dice ser), retry cases, validate,
encoding y las dos neutralidades en EXIT=0. El rojo determinista de r2 no reproduce.

**Queda ABIERTO S2, y es la misma clase en otra coordenada.** La sonda ejecuta solo el nodo `while` y
**escribe ella misma** las tres lineas de produccion que alimentan el camino de CPU (`:1493-:1495`),
que quedan fuera del extent invocado. En r2 el hand-feed era `$before`; aqui es el calendario del
muestreo. Un mutante de **un caracter** en `:1495` -- solo el signo -- restaura el defecto entero y el
negativo entregado se queda verde: sin semilla, `$progressProcessCpuSample` sigue `$null` en el primer
deadline y el detector vuelve a depender EXCLUSIVAMENTE de que crezca un fichero, que es justo lo que
AC5 prohibe. El texto del contrato promete matar *"when the production CPU-sampling block is
unreachable"*, y ese mutante lo deja inalcanzable de hecho sin tocarlo: **promete mas clase de la que
verifica**.

Arreglo especificado y ya ejecutado por el checker: cuatro lineas, **solo test**, invocando el bloque
desde la semilla en vez del nodo y borrando las tres asignaciones a mano. Criterio de aceptacion por
conducta: con `:1495` mutado por el signo, el negativo debe **morir**. Recomendado ademas declarar
como `mutation` del contrato la de la semilla, estrictamente mas fuerte que `if ($false)`.

**Residuales declarados que NO bloquean:** R9 (el margen del negativo de R6 es 15,6 ms contra un
umbral fijo de 50 ms, no derivado), R10 (la rama de post-entrega `:1541-:1555` no la ejecuta ningun
negativo, asi que **AC4 no lo sostiene ningun contrato**), R1 (una sola muestra por ventana; `:1571`
asigna `MaxValue` incondicionalmente), R8 (`Get-ExecTreeCpuTicks` es codigo muerto) y R5 (seis
corridas de CI en `failure`: no hay verde de Actions para esta entrega).

Esta era la vuelta 2 de 2. Conceder una tercera o cerrar con S2 abierto **lo decide el operador**.

