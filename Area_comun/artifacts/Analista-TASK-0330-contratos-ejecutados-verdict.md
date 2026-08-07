# Veredicto Analista -- TASK-0330 (los 23 contratos dormidos pasan a ejecutarse)

    Revisor            Analista (voz adversarial independiente)
    Tarea              TASK-0330 -- la cobertura declarada no es cobertura verificada
    Commit juzgado     be549858 coord(TASK-0330): deliver core and inventory sixth red
    Anclaje protocolo  be549858 es ancestro de origin/main; ningun commit posterior toca las
                       rutas de esta entrega (verificado hasta 12458b5a). Las corridas de CI
                       que cito son 31195169744 (1fb6594c) y 31171824272 (064aefe5).
    Clon limpio        D:/Aegis_Scratch/mapp/analista-0330/cc (hardlink clone, checkout be549858)
    Alcance            SOLO el hub. Sin producto en alcance, ningun npm test.
    Fecha              2026-08-07 18:24 hora local (UTC+2) == 16:24Z

    VEREDICTO          CHANGE-REQUIRED

## Resumen en una linea

El gate nuevo distingue "declarado" de "listado", pero no distingue "listado" de "ejecutado": los
tres runners entraron en un job `windows-latest` cuyo shell por defecto es `pwsh`, donde el fallo de
un comando intermedio no rompe el paso -- y la prueba no es teorica, es el propio CI de este repo,
donde ese job sale **success** con dos de los tres runners en rojo dentro.

## Estado canonico y arranque

    git fetch origin                                              ok
    git status --short                                            sin cambios ajenos tocados
    python scripts/validate_collaboration_state.py (arbol vivo)   EXIT 0
    HEAD local == origin/main == 1fb6594c al arranque en frio      ok
    (al commitear este veredicto, origin/main ya es 12458b5a)

## Reproduccion (clon limpio en be549858, gate por exit code)

    python scripts/validate_collaboration_state.py --root .                       EXIT 0
    python scripts/scan_encoding.py --root .                                      EXIT 0
    python scripts/scan_domain_neutrality.py --root .                             EXIT 0
    python scripts/test_scan_domain_neutrality.py                                 EXIT 0
    python scripts/test_exec_lease_harness.py                                     EXIT 0
    python scripts/memory/test_memory_db.py                                       EXIT 0
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory                     EXIT 0
        FALSIFICATION_EXECUTION runners=8/8 contracts=47/47
        FALSIFICATION_INVENTORY permanent_negatives=47 declared=47 missing=0
    python scripts/test_falsification_contracts.py                                EXIT 0
    python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py         EXIT 0
    python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py            EXIT 0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py                EXIT 1  (declarado)
    python scripts/prune_state.py --root . --check                                EXIT 1  (poda vencida,
        released_ratio 93.48 >= 90; ruta ajena a 0330, la reporto y no la toco)

## Tabla foco por foco

    A  "ejecutado" de verdad, no "listado"     SLIP  (decisivo)
    B  gate de contratos huerfanos por mutacion PASS el caso / SLIP la familia
    C  reds 1-5 reparados, no relajados         PASS  (mutacion propia incluida)
    D  sexto rojo ni silenciado ni maquillado   SLIP  (visible en fuente, silenciado en el gate;
                                                       e inventario de rojos incompleto)
    E  negativo propio del arreglo de ORDEN     SLIP  (existe, esta bien construido, pero es
                                                       codigo muerto y su mitad mutante es vacua)
    F  recuento honesto                         TUS NUMEROS SON LOS CORRECTOS; los del handoff no

---

## A -- Los tres pasos de CI no hacen fallar el job. Comprobado en el CI real.

El cableado es un job nuevo, `falsification-runners`, `runs-on: windows-latest`, con **un solo paso**
y un `run:` de tres lineas y **sin `shell:` declarado**:

    - name: Execute every previously dormant falsification runner
      run: |
        python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
        python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
        python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py

No hay `continue-on-error`. No hace falta: en Windows el shell por defecto de `run:` es `pwsh`, y ahi
el codigo de salida no-cero de un ejecutable nativo intermedio no aborta el bloque. GitHub anade
`exit $LASTEXITCODE` al final, asi que el paso hereda el codigo del **ultimo** comando.

No lo deduzco, lo mido en el CI real de este repo. Run 31195169744 (HEAD 1fb6594c, jjballestas/
multi_agent_project_protocol), job `falsification-runners`:

    shell: C:\Program Files\PowerShell\7\pwsh.EXE -command ". '{0}'"

y dentro de ese unico paso:

    run_mailbox_retry_cases.py        -> AssertionError en run_unreadable_head_case (el sexto rojo)
    run_runtime_turn_obstacle_cases.py-> ModuleNotFoundError: No module named 'jsonschema'
    run_post_gate_obstacle_cases.py   -> "OK: real run-log append rejects red-gate empty obstacles"

    paso  "Execute every previously dormant falsification runner" => success
    job   falsification-runners                                   => success

Dos de los tres runners estan **rojos dentro de un job verde**. Y el segundo es un rojo **nuevo,
introducido por esta entrega**: el job nuevo no copio el paso `Install Python test dependencies`
(`python -m pip install jsonschema`) que si tiene el job `validate`, y `run_runtime_turn_obstacle_
cases.py` importa `runtime.turn_validate`, que importa `jsonschema`. En CI ese runner **no ejecuta ni
un solo caso**: muere en el import.

Consecuencia sobre la tesis de la tarea, contada honestamente:

    contrato                              runner                            ejecuta en CI  gatea CI
    NEG-POST-GATE-RED-OBSTACLES (1)       run_post_gate_obstacle_cases.py   si             SI
    NEG-TURN-* (6)                        run_runtime_turn_obstacle_cases   no (import)    no
    retry-* (17)                          run_mailbox_retry_cases.py        parcial        no

De los contratos que estaban dormidos, **exactamente uno** esta hoy realmente gateado por CI. La
respuesta a tu pregunta A es NO: el fallo de cualquiera de los tres NO hace fallar el job.

Residual heredado que agrava el cuadro (NO es culpa de 0330, lo reporto como anomalia DECISION-0018
para que lo dirijas a quien corresponda): el job `validate` muere desde antes de esta tarea en el
paso 6 `Validate repository dogfood instance` con

    UnboundLocalError: cannot access local variable 'InvalidSignature'
    runtime/eventlog.py:414   (el paquete cryptography no esta en el CI)

Lo confirme en el run 31171824272 (064aefe5, pre-tarea): mismo paso 6, misma caida. Como GitHub salta
todo lo posterior, el paso 11 `Validate falsification contracts and guardian controls` -- que es
justamente donde corre el gate nuevo de AC4 -- aparece **skipped en todos los runs**. El mecanismo
central de la entrega no se ha ejecutado nunca en CI.

## B -- El gate huerfano cae. Pero protege el caso, no la familia.

**PASA el caso.** Declare un contrato huerfano bien formado en un runner no cableado:

    examples/analista_probe_cases/run_analista_probe_cases.py
    id NEG-ANALISTA-ORPHAN-PROBE, negative/mutation/boundaries/exercised_by completos

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory        EXIT 1
        FALSIFICATION_EXECUTION runners=8/9 contracts=47/48
        ERROR: NEG-ANALISTA-ORPHAN-PROBE: runner is not executed by workflow:
               examples\analista_probe_cases\run_analista_probe_cases.py

    control sin --workflow (el modo viejo):                          EXIT 0

La mutacion mata y el control demuestra que el modo nuevo es el que la mata.

**SLIPS la familia.** `command_executes()` es una regex sobre el texto concatenado de los campos
`run:`. Mide **mencion**, no ejecucion. Tres escapes, todos verdes, todos reproducidos:

    ESCAPE 1  `continue-on-error: true` sobre el paso entero    GUARD EXIT 0  contracts=47/47
    ESCAPE 2  los tres runners solo `echo`ados, nunca invocados GUARD EXIT 0  contracts=47/47
    ESCAPE 3  job `falsification-runners` borrado entero, las
              rutas dejadas en un `echo` de un job cualquiera   GUARD EXIT 0  contracts=47/47

El escape 1 es literalmente el caso que tu enunciado nombra como el defecto que la tarea combate, y
el gate no lo ve. El escape 3 es el peor: se puede borrar el cableado completo y el inventario sigue
cantando 47/47. El gate no puede ver `continue-on-error`, ni la semantica del shell, ni la
desaparicion del job, porque nunca mira la estructura del workflow, solo el texto de los `run:`.

Esto es la misma enfermedad de la tarea una capa mas arriba: una medida de cobertura que mide la
declaracion en vez del efecto.

## C -- Reds 1-5: reparados, no relajados. El reescrito aguanta mi mutacion mas dura.

Los casos 1 a 11 del runner se ejecutan y pasan en clon limpio (el runner llega vivo hasta el caso
12). No encontre ninguna asercion borrada ni ablandada en esos tramos.

El que me pediste falsar en particular, `retry-expired-claim` reescrito a forma conductual, es
**solido**. Extrae de produccion `Read-JsonWithDeadline` y `Get-AdditionalWorkSignal` reales, los
ejecuta en PowerShell contra un CLAIMS.json de sonda, y exige las dos formas del predicado:

    forma actual  if ($expires -le $now) { continue }              expired->none, live->active
    forma vieja   if (-not ($expires -gt $now)) { continue }       expired->none, live->active
    mutante       -le  ->  -gt                                     expired->active Y live->none

Mis mutaciones independientes sobre PRODUCCION:

    M1  borrar la linea `if ($expires -le $now) { continue }`
        -> RED en run_expired_claim_behavior_case:484 "current expiry predicate not found"
        (cae cerrado, pero por FORMA)

    M2  dejar el literal INTACTO y envenenar el reloj:
        $now = [DateTime]::UtcNow  ->  $now = [DateTime]::MinValue
        el filtro de expiracion queda como codigo muerto, la linea sigue ahi
        -> RED en run_expired_claim_behavior_case:490
           "current: expired claim counted as active"

M2 es la que importa: es el mutante de codigo muerto que sobrevive a los contratos que solo
comprueban `linea in source`. Este checker lo mata **por comportamiento**. Aqui la conversion a forma
conductual que autorizaste hizo exactamente lo que se le pidio.

## D -- El sexto rojo: el diagnostico es cierto, pero ni esta gateado ni esta solo.

**El diagnostico del handoff es correcto.** Reproducido en clon limpio:

    fixture (linea 745)  "RETRY_EXHAUSTED defers=3 attempts=0 signal=watchdog "
                         "outcome=defer_terminal reason=ledger_unreadable_before_exec"
    produccion emite     RETRY_EXHAUSTED defers=3 attempts=0 elapsed_seconds=2 timeout_seconds=2
                         signal=watchdog outcome=defer_terminal reason=ledger_unreadable_before_exec

El estado terminal SI aparece en el log; lo unico que falla es el emparejamiento de subcadena, porque
`peer_mailbox_cron.ps1:1000` intercala `elapsed_seconds` y `timeout_seconds`. No hay skip, no hay
xfail, no hay asercion debilitada: es un `assert` duro. En la fuente esta limpio.

**Pero esta silenciado donde cuenta.** Por el hallazgo A, ese rojo sale verde en el job de CI. Que
sea visible en la fuente y no en el gate es exactamente la distincion que esta tarea existe para
borrar.

**Y no esta solo. La afirmacion "RED only at the declared sixth fixture assertion" no es
verificable desde una corrida que aborta en el caso 12 de 20.** Reparando la subcadena obsoleta SOLO
como sonda (parche mio, en copia de trabajo, nunca propuesto como fix) aparecen detras:

    7o rojo  run_unstaged_residue_case (linea 833)
             misma familia de subcadena obsoleta:
             "RETRY_EXHAUSTED defers=3 attempts=0 signal=watchdog outcome=defer_terminal
              reason=worktree_residue_live"  contra una linea que ya lleva elapsed/timeout.
             NO declarado, NO inventariado.

    8o rojo  run_exec_running_heartbeat_case (linea 1024)
             assert exercise(runner_text) >= 3  falla con **0**, no con 2: EXEC_RUNNING no se
             emite ni una vez. Y al medir tambien el mutante:
                 ANALISTA_PROBE exec_running_count=0
                 ANALISTA_PROBE exec_running_mutant=0
             positivo y mutante son indistinguibles: el contrato esta VACUO en este estado.
             NO declarado.

    9o rojo  run_post_delivery_timeout_case (linea 948)
             el mensaje del fixture ni siquiera se procesa: produccion lo veta con
             RETRY_DEFER ... reason=message_scope_ambiguous, la ventana nunca arranca y
             POST_DELIVERY_WINDOW_START no aparece. Familia distinta a las anteriores.
             NO declarado.

    sin ejecutar todavia, estado desconocido: run_pre_delivery_and_liveness_cases,
    run_frozen_exec_with_production_freshness_case, run_complete_tree_kill_case y el bloque
    pre-dirty final (todo lo posterior a la linea 1390).

El AC5 pedia reportar el inventario de rojos ANTES de arreglarlos, precisamente para no confundir "lo
arregle todo" con "lo silencie todo". El inventario entregado se detiene en uno. TASK-0335 se
contrato sobre la premisa de una unica asercion obsoleta; son al menos cuatro rojos, de tres familias
distintas, y una cola sin explorar.

## E -- El negativo del arreglo de ORDEN existe, esta bien hecho, y hoy es codigo muerto.

`retry-ledger-head-defer-order` vive dentro de `run_unreadable_head_case`. Su mutacion esta en la
linea 802:

    785   exercise(instrumented_runner, expect_terminal=True)     <-- revienta SIEMPRE aqui
    ...
    790   mutant_text = runner_text.replace(good_order, bad_order, 1)
    802   exercise(mutant_runner, expect_terminal=False)          <-- NUNCA se alcanza

En be549858 ese negativo **no se ejecuta**. Y hay algo peor que la inalcanzabilidad: como
`terminal_line` es una subcadena que NINGUN log de produccion puede satisfacer, `terminal` es siempre
False, asi que la mitad mutante `expect_terminal=False` es **vacua**: pasaria hiciera lo que hiciera
produccion. El unico motivo por el que el caso esta rojo es la mitad positiva.

Falsado por comportamiento: con la subcadena reparada como sonda, el caso pasa completo y las dos
mitades **si discriminan** (buen orden -> terminal presente; orden invertido -> terminal ausente). O
sea: el negativo esta bien construido y **mataria**. Pero la condicion con la que autorizaste la
ampliacion a produccion -- "un negativo permanente verificado por MUTACION" -- **no esta cumplida en
el estado entregado**, porque la mutacion no llega a correr.

Y `check_falsification_contracts.py` lo cuenta igual como ejecutado, porque solo comprueba que la
cadena de la mutacion y las boundaries aparezcan en el SOURCE de la funcion. Contrato declarado,
presente en el texto, muerto en la ejecucion: el patron que ya vimos en TASK-0316.

## F -- El recuento. Tus numeros son los correctos.

Recomputado por mi, independiente, parseando `FALSIFICATION_CONTRACTS` con AST:

    en 0eb060ee (el HEAD que mediste), los tres runners huerfanos:
        run_mailbox_retry_cases.py          16 contratos   32 boundaries
        run_runtime_turn_obstacle_cases.py   6 contratos   13 boundaries
        run_post_gate_obstacle_cases.py      1 contrato     2 boundaries
        TOTAL DORMIDO                       23 contratos   47 boundaries   <-- tus 23 y tus 47
        repo entero                         32 contratos   76 boundaries

    en be549858 (lo entregado):
        los mismos tres runners             24 contratos   52 boundaries
            (+1 contrato retry-ledger-head-defer-order, +5 boundaries)
        repo entero                         47 contratos  133 boundaries

**Tus 23 contratos y 47 fronteras son exactos.** El handoff no.

El "47" del handoff ("47 permanent negatives, all 47 declared") es el numero de CONTRATOS DEL REPO
ENTERO en be549858. No es tu 47, que son las FRONTERAS del subconjunto dormido en 0eb060ee. Son dos
47 distintos que coinciden por casualidad, y la frase "The 23 previously declaration-only contracts
and their 47 boundaries are now attached to executable CI steps" encadena tres errores en una linea:
ya no son 23 sino 24, ya no son 47 sino 52, y "attached to executable CI steps" es falso en efecto
segun el hallazgo A.

El recuento honesto que yo firmaria hoy: **24 contratos y 52 fronteras cambiaron de "solo
declarados" a "mencionados en un `run:`"; 1 contrato y 2 fronteras cambiaron a "realmente gateados
por CI"**.

## Residuales declarados

1. `prune_state.py --check` sale EXIT 1 en clon limpio (released_ratio 93.48 >= 90). Poda vencida.
   Ruta ajena a 0330 y a mi; la senalo, no la toco.
2. La caida pre-existente del job `validate` (`UnboundLocalError: InvalidSignature`,
   `runtime/eventlog.py:414`) deja en `skipped` el paso que corre el gate nuevo. Anterior a esta
   tarea, no la imputo a 0330, pero mientras siga asi AC4 no tiene ejecucion real en CI.
3. No ejecute los casos posteriores a la linea 1390 del runner de retry mas alla de la sonda; su
   estado sigue siendo desconocido.
4. Mis sondas (reparar subcadenas, hacer no-fatal un assert) se hicieron en copias de trabajo bajo
   `D:/Aegis_Scratch/mapp/analista-0330/`. No propongo ninguna de ellas como parche y no toque el
   arbol canonico.

## Recomendacion de cierre

    CHANGE-REQUIRED

Lo que falta para que la tesis de la tarea sea cierta y no solo declarada:

1. **AC3 (bloqueante).** Que el fallo de cualquiera de los tres runners rompa el job. La forma
   minima y verificable es un paso por runner, o `shell: bash` en el bloque, o comprobacion explicita
   de `$LASTEXITCODE` entre comandos. Falsable: forzar un fallo en el PRIMER runner y comprobar que
   el job sale `failure`.
2. **AC3 (bloqueante).** Anadir `python -m pip install jsonschema` al job `falsification-runners`.
   Hoy `run_runtime_turn_obstacle_cases.py` no ejecuta ningun caso en CI. Falsable: el runner debe
   imprimir su OK final en el log del job.
3. **AC4.** El gate debe medir ejecucion, no mencion. Como minimo, parsear el YAML y rechazar que un
   runner quede bajo un paso con `continue-on-error`, y comprobar que el paso pertenece a un job
   existente. Los tres escapes de arriba son los mutantes que hay que matar.
4. **AC5.** Completar el inventario de rojos del runner de retry antes de cerrar: el 7o, 8o y 9o
   quedan sin declarar, y la cola posterior a la linea 1390 sin explorar. TASK-0335 esta contratada
   sobre una premisa incompleta.
5. **Foco E.** Dejar constancia de que `retry-ledger-head-defer-order` no se ejecuta hoy, y que su
   mitad mutante es vacua mientras la subcadena siga obsoleta. Su verificacion por mutacion debe
   quedar dentro del alcance que repare el sexto rojo, no despues.

Lo que NO hay que tocar: el checker conductual de `retry-expired-claim`. Aguanta el mutante de codigo
muerto y es el modelo de como deberia verse el resto.

## Bucle de correccion esperado

    remediacion   Codex, sobre los puntos 1-5. 1 y 2 son bloqueantes; 3 es el que evita la
                  recurrencia; 4 y 5 son declaracion honesta y pueden ir a TASK-0335 si prefieres
                  particionar, siempre que 0330 no se cierre afirmando "47 ejecutados".
    gates         check_falsification_contracts --workflow --inventory, test_falsification_contracts,
                  los tres runners, validate, scan_encoding, scan_domain_neutrality; y ademas la
                  comprobacion del job REAL en GitHub Actions (un job verde con un runner rojo dentro
                  es el modo de fallo, y solo se ve en el CI real).
    rejuicio      antes del commit de cierre, no despues.
    tope          maximo 2 iteraciones; a la tercera escalo al operador humano.

-- Analista
