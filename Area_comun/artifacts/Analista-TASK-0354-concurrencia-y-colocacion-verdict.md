# VEREDICTO TASK-0354 -- guarda de concurrencia y colocacion por host

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0354.md
    escrito             2026-08-10 09:26 local (UTC+2)  ==  2026-08-10T07:26Z
    veredicto           CHANGE-REQUIRED
    iteracion           1 de 2 antes de escalar al operador humano

## 0. Ancla canonica y por que juzgo en HEAD

La instruccion ancla en `7467857ea1eb53017284105df0a4ede359e0a8fd` y cita la implementacion
`a583e189`. Entre ese ancla y `origin/main` entraron seis commits (la cadena de TASK-0353), asi que
comprobe primero que el fichero gobernado no se mueve:

    git merge-base --is-ancestor a583e189 HEAD      -> YES
    git merge-base --is-ancestor 7467857e HEAD      -> YES
    git diff --stat 7467857e 1d78dc08 -- .github/workflows/validate.yml   -> (vacio)
    git diff --stat a583e189 1d78dc08 -- .github/workflows/validate.yml   -> (vacio)
    git log --oneline a583e189..1d78dc08 -- .github/workflows/validate.yml -> (vacio)

`.github/workflows/validate.yml` es identico en `7467857e`, `a583e189` y HEAD. Juzgo en

    HEAD canonico   1d78dc0873274b30300ec7613dfd2275b17a5cc2   (== origin/main)
    implementacion  a583e189d433d6f231aade3f8fa33acb01e81ec0
    padre           2767b2c7881a097d2ce7f34eef4b799364da3333   (a583e189^)

que es equivalente para el fichero en revision y mas estricto para las puertas de protocolo.

Superficie real del commit de implementacion (`git show --stat a583e189`): **dos ficheros**,
`.github/workflows/validate.yml` (+18) y el fichero de tarea (+1/-1, solo `status: ready` ->
`in_progress`). Este dato es la base de dos de los hallazgos de abajo.

## 1. Reproduccion -- clones limpios, exit codes reales

Cuatro clones `--shared --no-hardlinks` bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/rv0354/` (DECISION-0104), nunca en el arbol caliente:

    clone         @ 1d78dc08  (replicador del job validate, "despues")
    clone_before  @ a583e189^ (replicador del job validate, "antes")
    clone_impl    @ a583e189  (sondas puntuales sobre la implementacion)
    clone_linux   @ 1d78dc08  (puertas + sondas; `git status --short` vacio)

Puertas de protocolo en `clone_linux` (gateadas por `$?` del comando, nunca detras de un pipe):

    python scripts/validate_collaboration_state.py --root .          EXIT=0   OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                         EXIT=0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .                EXIT=0
    python runtime/protocol_replay.py --check-drift --root .          EXIT=0   PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8522
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory         EXIT=0   runners=12/12 contracts=71/71

Host de la revision para lo que exige Linux: WSL2 Ubuntu, `Python 3.12.3`, `git 2.43.0`.
Host de la revision para lo que exige Windows: Windows 11, `python 3.12`, `jsonschema 4.26.0`.
`pwsh` 7 no esta instalado en este host: por eso el replicador reporta 8 pasos UNSUPPORTED, igual
que en la entrega.

## 2. Tabla vector por vector

    AC   promesa                                              veredicto        como lo fase
    ---- ---------------------------------------------------- ---------------- --------------------------------
    AC1  corrida anterior CANCELADA por comportamiento        RESIDUAL OK      no acreditable; la entrega NO lo
                                                                              da por bueno desde el YAML
    AC2  el residual de la cancelacion, por escrito           PASS (marginal)  existe, en un solo sitio
    AC3  colocacion DERIVADA de lo que invoca                 PASS             corri los tres runners en Linux
    AC4  cero perdida de cobertura                            PASS de letra    89 -> 89 lineas, 0 perdidas
                                                              SLIPS de fondo   la igualdad oculta un arranque
                                                                              imposible (F1)
    AC5  la dependencia dura sigue dura                       PASS             FileNotFoundError reproducido
    AC6  sin regresion, saldo derivado del propio run         SLIPS            el saldo no sale de las anclas y
                                                                              el instrumento no ve el cambio

Hallazgos que gatean el cierre: **F1** (AC4/AC3, arranque imposible), **F2** (AC6, saldo no
derivado), **F3** (FOCO 2, granularidad sin decidir), **F4** (la puerta de cableado no ve el
mecanismo que esta tarea introduce).

## 3. Lo que SI esta bien, y lo verifique mas fuerte que la entrega

### AC3 -- la colocacion se sostiene por comportamiento, no por argumento

La entrega afirma la colocacion. Yo la **ejecute en el host de destino**, que es lo que nadie habia
hecho: los dos runners que se mueven nunca se han corrido en Linux.

    HOST LINUX (WSL2 Ubuntu, python 3.12.3, git 2.43.0), clon limpio @1d78dc08
      python3 examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py   EXIT=0
        "OK: authoritative delivery and in-schema friction controls are mutation-proved."
      python3 examples/runtime_turn_cases/run_post_gate_obstacle_cases.py      EXIT=0
        "OK: real run-log append rejects red-gate empty obstacles; ... mutant is killed"

    y otra vez sobre un clon `--depth 1` (la forma que usa actions/checkout@v4 por defecto,
    porque el job nuevo NO pide fetch-depth: 0):
      git clone --depth 1 --branch main  -> commits=1, HEAD=1d78dc08
      run_runtime_turn_obstacle_cases.py   EXIT=0
      run_post_gate_obstacle_cases.py      EXIT=0

Y la derivacion de host, medida en lugar de leida. Recuento exacto de terminos de host en los dos
runners que se mueven (`grep -c -F`, cada termino por separado):

    windows / powershell / pwsh / ps1 / sys.platform / os.name / linesep / autocrlf / shell=True
      -> 0 ocurrencias en los dos ficheros

    unico proceso externo:  git   (subprocess.run(("git", "init"|"config"|"add"|"commit"|"status")))

La unica linea que ramifica por plataforma en esos runners es su propio ayudante de scratch:

    def task_scratch_root() -> Path:
        base = Path(f"{ROOT.drive}/") if ROOT.drive else Path.home()

En Linux cae en `Path.home()` -> `$HOME/Aegis_Scratch/...`, escribible: no rompe la mudanza. Queda
como residual derivado: **tras el movimiento, la rama `ROOT.drive` de ese ayudante ya no la ejercita
ningun job de CI**.

### AC5 -- la dependencia dura sigue siendo dura, falsada en un host sin el interprete

No me quede en "no hay `which` ni `skip`". Corri el runner en un host sin `powershell.exe`, con la
interoperabilidad de Windows quitada del PATH a proposito:

    HOST LINUX, env PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      python3 examples/mailbox_retry_cases/run_mailbox_retry_cases.py
      EXIT=1
      FileNotFoundError: [Errno 2] No such file or directory: 'powershell.exe'

Revienta, no se salta. Es exactamente lo que el AC5 exige que siga pasando. Control en el host que
si lo tiene, para probar que el runner que se QUEDA en Windows sigue verde:

    HOST WINDOWS, clon limpio @1d78dc08
      python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   EXIT=0
      "mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)"

Nota metodologica: cuando dejo el PATH con interoperabilidad, `powershell.exe` resuelve via
`/mnt/c/...` y el runner llega mucho mas lejos (muere en `AssertionError: "ROLLBACK_DEFER
reason=head_changed"`, artefacto de mi entorno cruzado). Por eso el control con PATH desnudo es el
que vale, y por eso lo declaro.

### AC4 -- la igualdad de conjuntos, derivada por mi con parser independiente

Parseo los dos commits con PyYAML y comparo lineas de comando `run`, no nombres de paso:

    BEFORE (a583e189^)  triggers ['pull_request','push']   concurrency: None
        powershell-linux-parity  ubuntu-latest    run_steps=5
        validate                 ubuntu-latest    run_steps=77
        falsification-runners    windows-latest   run_steps=4
        por host: ubuntu 82, windows 4      lineas de comando distintas: 89

    AFTER (a583e189)    triggers ['pull_request','push']
        concurrency: {group: validate-${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: True}
        powershell-linux-parity     ubuntu-latest    run_steps=5
        validate                    ubuntu-latest    run_steps=77
        falsification-runners       windows-latest   run_steps=2
        falsification-runners-python ubuntu-latest   run_steps=3
        por host: ubuntu 85, windows 2      lineas de comando distintas: 89

    DELTA   perdidas: []    ganadas: []
    mismo comando, distinto job/host -- exactamente tres:
        python -m pip install jsonschema
            antes  [(falsification-runners, windows-latest)]
            despues[(falsification-runners, windows-latest), (falsification-runners-python, ubuntu-latest)]
        python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py     windows -> ubuntu
        python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py  windows -> ubuntu

Confirmo el 0/0 de la coordinacion. Dos matices que la cuenta de la coordinacion no muestra: mi
unidad da **89 lineas de comando** (no 83; unidad distinta, no defecto), y los **pasos `run` suben
de 86 a 87** porque el `pip install jsonschema` se duplica. El coste del job nuevo (VM + checkout +
setup-python + pip) compensa en parte el ahorro de Windows, y **nadie midio el reparto de los 2m26s
entre los tres runners**, asi que el ahorro declarado sigue sin cuantificar. No lo pide ningun AC;
lo dejo como residual.

### AC1 -- la entrega no cae en la trampa del FOCO 1

Comprobado en el texto de la entrega
(`Area_comun/mailbox/archived/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0354.md`, lineas 55-58):
"AC1 is not yet accredited. The YAML change is present, but behavioral proof requires two rapid
pushes and the first Actions run observed in `cancelled` state." No da el AC1 por bueno leyendo el
bloque del YAML. Eso es lo correcto y lo hago constar. Residual, no cumplimiento.

## 4. F1 -- el job nuevo no puede ARRANCAR el runner por el que existe

Este es el hallazgo. El job `falsification-runners-python` declara una sola dependencia:

    - name: Install falsification runner dependencies
      run: python -m pip install jsonschema

y el runner que invoca importa PyYAML en el nivel superior:

    examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py:14:   import yaml

`jsonschema` no arrastra PyYAML. Metadatos del propio paquete instalado:

    python -m pip show jsonschema
      Name: jsonschema   Version: 4.26.0
      Requires: attrs, jsonschema-specifications, referencing, rpds-py

Reproduccion, con `jsonschema` PRESENTE y `yaml` AUSENTE -- es decir, el estado exacto del
interprete que deja `actions/setup-python@v5` + esa unica linea de `pip install`:

    python D:/Aegis_Scratch/protocol/rv0354/block_yaml.py \
        examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
    control: jsonschema 4.26.0 available; yaml blocked
    ...
        import yaml
    ModuleNotFoundError: No module named 'yaml'
    EXIT=1

Segunda via, en Linux, con un venv sin PyYAML:

    /tmp/venv/bin/python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
      EXIT=1   ModuleNotFoundError: No module named 'yaml'   (linea 14)
    /tmp/venv/bin/python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py
      EXIT=0   (este solo usa stdlib + runtime.runlog: sobrevive)

Consecuencia medida, en el idioma de esta instancia: la puerta de cableado da por ejecutado lo que
no puede arrancar.

    check_falsification_contracts.py --inventory   EXIT=0
      FALSIFICATION_STATIC_WIRING runners=12/12 contracts=71/71
      contratos cuyo runner es run_runtime_turn_obstacle_cases.py:  8

**Ocho de los 71 negativos permanentes declarados estan certificados como "executed by workflow"
mientras su runner muere en el import, dentro del job que los gatea.** Muere antes de ejecutar una
sola asercion.

### Atribucion honesta (bisect, para no cargarselo al maker)

    git log --oneline -S "import yaml" -- examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
      4f141167 fix(TASK-0347): restore obstacle-aware delivery fixtures
    git show a583e189^:...run_runtime_turn_obstacle_cases.py | grep -n "^import yaml"  -> 14
    git show a583e189:...run_runtime_turn_obstacle_cases.py  | grep -n "^import yaml"  -> 14

El `import yaml` entro en TASK-0347, **antes** de esta tarea: el viejo job de Windows ya arrastraba
la misma linea de instalacion insuficiente. Asi que **F1 no es una regresion de TASK-0354**. Es un
defecto latente que esta tarea tuvo delante y copio: escribio una **declaracion de dependencias
nueva para un job nuevo** sin derivarla de los imports del runner que invoca, que es literalmente lo
que el AC3 pide hacer ("la dependencia se DERIVA del runner"), y el arreglo es una palabra dentro de
`.github/workflows/validate.yml`, la unica ruta de `scope_routes` de la tarea. Por eso lo cuento
dentro y no fuera.

### Por que nadie lo vio, y por que el verde local no vale aqui

    python scripts/replay_validate_job.py --root . --job falsification-runners-python
      STEP 01/03 PASS  Install falsification runner dependencies
      STEP 02/03 PASS  Execute runtime turn falsification runner
      STEP 03/03 PASS  Execute post-gate falsification runner
      SUMMARY declared=3 pass=3 fail=0 unsupported=0

El replicador pasa el job nuevo 3/3 en mi host **porque usa el interprete del host, que ya tiene
PyYAML, y nunca honra el `pip install` declarado del job**. Es un falso verde estructural: el
replicador no puede cazar esta clase. Con la facturacion de Actions bloqueada, ninguna corrida real
lo desmiente. Nota lateral del mismo replicador: el job de Windows sale
`SUMMARY declared=2 pass=0 fail=0 unsupported=2`, porque `runs-on: windows-*` sin `shell:` se
replica con `pwsh`, que este host no tiene.

## 5. F2 -- el saldo del AC6 no sale de las anclas, y el instrumento no ve el cambio

El `verification_cmd` de la tarea es `python scripts/replay_validate_job.py --root .`. Ese script
tiene `--job` con **default `validate`**:

    scripts/replay_validate_job.py:28:  parser.add_argument("--job", default="validate")

El job `validate` tiene sus 77 pasos `run` **byte-identicos** antes y despues (el diff del workflow
son solo el bloque `concurrency` y el job nuevo). Ninguno de los jobs que esta tarea cambia se
replica. Es un punto ciego que yo mismo deje escrito en el veredicto r2 de TASK-0353: "el numero de
paso del replicador cuenta SOLO los steps con `run:` del job `validate` (77); el runner del negativo
permanente vive en el job `falsification-runners`, que el replicador NO replica". El AC6 usa ese
instrumento como puerta de no-regresion para un cambio que vive entero fuera de su alcance.

Mis dos corridas, en clones limpios y en las anclas:

    ANTES   a583e189^   SUMMARY declared=77 pass=61 fail=8 unsupported=8
            FAIL: 03, 04, 36, 43, 50, 53, 58, 59
    DESPUES 1d78dc08    SUMMARY declared=77 pass=63 fail=6 unsupported=8
            FAIL: 36, 43, 50, 53, 58, 59

La entrega declara **60/9/8 antes y 60/9/8 despues**, con fallos 34, 36, 39, 40, 43, 50, 53, 58, 59.
Comparado con una corrida real en el padre commiteado, **cinco de las nueve entradas no cuadran**:

    declarados FAIL y en clon limpio PASS:  34 (materialize), 39 (enforce), 40 (genesis-ref)
    FAIL reales que la declaracion no tiene: 03 (Validate repository dogfood instance)
                                             04 (Run full-mode hook inventory cases)

Y la causa de 03/04 en el padre es concreta:

    STEP 03/77 FAIL exit=1  diagnostic="ERRORS: - Task TASK-0354 status mismatch:
                                        index='in_progress' file='ready'"
    STEP 04/77 FAIL exit=1  require(positive, 0, "clean governed tree in full partial-snapshot mode")

Es el rojo de coordinacion preexistente que ya senale por DECISION-0018 en el veredicto r2 de
TASK-0353, y que `a583e189` **repara de paso** al llevar el fichero de tarea de `ready` a
`in_progress`. Verificado directamente sobre la implementacion:

    clon limpio @ a583e189:  python scripts/validate_collaboration_state.py --root .   EXIT=0
    clon limpio @ a583e189:  python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
                                                                                      EXIT=0

Los dos pasos rojos del padre pasan a verde en la propia implementacion, asi que el delta
61/8/8 -> 63/6/8 es entero de la reparacion de status que `a583e189` lleva dentro, y nada del
cambio del workflow puede mover el saldo de `validate`: sus 77 pasos son byte-identicos.

O sea: la conclusion del AC6 ("no empeora") **sobrevive** -- de hecho mejora en dos pasos --, pero el
numero fue **transcrito desde un arbol de trabajo, no derivado de las anclas**. Los tres rojos
declarados y no reproducibles (34/39/40 son justamente materialize / enforce / genesis-ref, los mas
sensibles al estado sucio del arbol) apuntan a que la medicion se tomo en el arbol vivo. Es la
tercera vez seguida que el AC de saldo cae por lo mismo; el FOCO 5 lo pedia y hay que decirlo.

## 6. F3 -- FOCO 2: la granularidad es correcta hoy, y esta sin decidir

Barrido del arbol entero en el ancla buscando la declaracion de la granularidad:

    grep -rniE "cancel-in-progress|concurrency" --include=*.md --include=*.json .
      -> ni una ocurrencia que razone la eleccion (solo veredictos ajenos y el propio GO/HANDOFF)
    grep -rniE "pull_request|github\.ref" --include=*.md .
      -> ninguna mencion en la tarea, el YAML, una DECISION ni un doc de protocolo

El YAML no lleva comentario. La entrega solo reescribe la expresion ("cancels an older run of the
same workflow and ref"), que es restatement, no razonamiento. Lo derivable, y no esta escrito:

    push a una rama          github.ref = refs/heads/<rama>       grupo A
    pull_request de esa rama github.ref = refs/pull/<n>/merge     grupo B

Los dos triggers siguen activos en los dos commits (`['pull_request','push']`, medido arriba), asi
que **un PR y el push de su propia rama caen en grupos distintos y no se cancelan entre si**: el
mismo commit paga dos corridas completas en paralelo. Eso es justo lo contrario del objetivo de la
tarea. Hoy no muerde:

    gh pr list --state all -L 5   -> vacio
    ramas remotas: main, vision-nova, fix/decision-0046-replay-secret-independent

Correcto por suerte, no por diseno, que es la frase exacta del FOCO 2. Falta una linea escrita: o se
declara por que `github.ref` es la granularidad elegida y que se acepta la duplicacion push/PR, o se
pone filtro al trigger. Sin eso queda sin decidir, y el dia que se abra un PR desde `vision-nova`
duplica factura en la rama que esta tarea venia a abaratar.

## 7. F4 -- la puerta de cableado no conoce el mecanismo que esta tarea introduce

`check_falsification_contracts.py:step_gates_runner` rechaza tres formas de supresion de ejecucion:

    if "needs" in job or "needs" in step:                       return False
    if not condition_allows_execution(job.get("if")) or ...:     return False
    if not failure_reaches_job(job) or ...:                      return False

`concurrency.cancel-in-progress: true` es una **cuarta forma de supresion declarada estaticamente en
el mismo YAML** -- una corrida cancelada no ejecuta sus runners -- y la puerta no la mira ni la
declara. Su propia lista de residuales, en la salida de hoy, no la nombra:

    residuals=trigger_filters,working_directory,yaml_1_1_scalars,safe_forms_outside_whitelist,
              line_continuation_mechanism_redundancy,contract_discrimination_23_of_37,twin_TASK_0338

El dano practico esta acotado (la corrida mas nueva siempre sobrevive, y el modelo de puerta valida
el ARBOL en HEAD, que es justo lo que el AC2 declara), pero la puerta que certifica "executed by
workflow" quedo un grado mas debil sin que nadie lo declare. Con F1 encima, la frase
`runners=12/12 contracts=71/71` afirma hoy dos cosas que no son ciertas.

## 8. FOCO 3 -- el residual del AC2 esta escrito, en un solo sitio

Existe, y solo aqui:

    Area_comun/mailbox/archived/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0354.md:59
      "Cancellation means intermediate commits in a burst are not each validated. This instance
       gates the HEAD tree, so that is accepted; the cost is reduced granularity when bisecting a
       future regression."

Barrido del arbol (`bisect|granularidad|granularity` sobre *.md, *.yml, *.json, *.py): ni el
workflow, ni el fichero de tarea, ni una DECISION, ni un doc de protocolo lo recogen. Cumple la
letra del AC2 -- esta por escrito y en estado canonico -- y no se colo como comentario de
implementacion. Pero el residual del AC1 vive en el mismo unico sitio, y ese si tiene una obligacion
pendiente: **quien desbloquee la facturacion no va a encontrar en el fichero de tarea que falta
acreditar el AC1**. Residual de trazabilidad, no de conducta.

## 9. FOCO 4 -- derivada o justificada: la asercion que la entrega cita no existe

La entrega afirma: "Derived placement assertion passes for all three runners". Esa asercion **no
esta en estado canonico**: `git show --stat a583e189` son dos ficheros, el workflow y una linea de
status. No hay script, ni caso, ni contrato, ni comentario que la contenga; fue una comprobacion
local irreproducible desde el ledger.

La declaracion por runner si existe (handoff, tres vinetas, cada una nombrando el interprete o
binario invocado), y **yo la verifique por comportamiento**, que es mas de lo que el AC pedia. La
letra del AC3 se cumple. Lo que no hay es criterio escrito ni mecanismo: nada en el repo impide
manana meter un runner de Python puro en el job de Windows, ni sacar de Windows uno que invoque
`powershell.exe`. Con F1 encima, la respuesta a tu pregunta es literal: **el host de cada runner
esta derivado; su dependencia de paquetes no, y esa mitad de la derivacion es la que rompe.**

## 10. Residuales declarados

1. **Sin CI real.** Todo lo mio es local. La facturacion de Actions sigue bloqueada por decision del
   operador. El AC1 (corrida cancelada) queda pendiente de acreditar al desbloquear.
2. **El job `falsification-runners-python` nunca ha corrido en GitHub Actions.** Mitigado, no
   cerrado: probe sus dos runners en un host Linux real y en un clon `--depth 1`, exit 0 los dos. Lo
   que no puedo probar es el job (imagen ubuntu-latest, setup-python, su propio pip install) -- y F1
   dice que ese pip install es el que falla.
3. **`pwsh` 7 ausente en mi host:** 8 pasos UNSUPPORTED en el replicador, identico a la entrega.
4. **Reparto de los 2m26s entre los tres runners sin medir:** el ahorro neto (menos Windows x2, mas
   un job ubuntu con su overhead fijo) sigue sin cuantificar. Ningun AC lo pide.
5. **`task_scratch_root()`:** tras el movimiento, su rama `ROOT.drive` ya no la ejercita ningun job.
6. **Mi "despues" del replicador es HEAD (1d78dc08), no `a583e189`,** porque el job `validate` es
   byte-identico entre los dos y HEAD es la puerta mas estricta. Aisle el efecto de esta tarea
   verificando el paso 03 directamente sobre `a583e189` (EXIT=0).
7. **Mi conteo de comandos (89 lineas) no es el de la coordinacion (83).** Unidad distinta, no
   discrepancia de fondo: perdidas 0 y ganadas 0 en las dos.

## 11. Recomendacion de cierre

**CHANGE-REQUIRED.** No cerrar TASK-0354.

Lo entregado es sustancialmente bueno: la colocacion por host es correcta y ahora esta probada en el
host de destino, la dependencia dura sigue dura, no se pierde ni un comando, y el AC1 se declaro como
residual en vez de darlo por bueno desde el diff. Lo que lo bloquea es que **el job nuevo, tal y como
esta escrito, no puede arrancar el runner por el que existe** (F1), y que **el AC6 se acredito con un
numero que no sale de las anclas y con un instrumento que no ve el cambio** (F2). F3 es la linea
escrita que el FOCO 2 pedia y no esta.

### Remediacion esperada

1. **F1 -- derivar la instalacion de dependencias del job de los imports de los runners que
   invoca**, y escribir la derivacion. Se falsa ejecutando los runners del job en un interprete
   limpio que solo tenga lo que el job instala (no el del host): exit 0 con eso y solo eso. Alcanza
   tambien a la linea del job de Windows, que arrastra el mismo patron.
2. **F2 -- volver a medir el saldo en las anclas commiteadas** (`a583e189^` vs `a583e189`), en clon
   limpio, y **con un job que el cambio toque** (`--job falsification-runners` y
   `--job falsification-runners-python`), declarando que el default `--job validate` es ciego a esta
   tarea. La lista de fallos, del propio run.
3. **F3 -- declarar por escrito la granularidad** (`github.ref`) y que pasa con `pull_request`: o se
   acepta la duplicacion push/PR y se dice, o se filtra el trigger.
4. **F4 -- declarar la cancelacion como residual de la puerta de cableado** (o mirarla en
   `step_gates_runner`), para que `runners=N/N` no siga afirmando mas de lo que comprueba.
5. **AC1/AC2 -- dejar la obligacion pendiente donde se vaya a encontrar** (fichero de tarea o tarea
   de seguimiento), no solo en un mensaje archivado.

### Puertas afectadas y ciclo

Puertas a re-verificar en clon limpio, por exit code: `validate_collaboration_state.py`,
`scan_encoding.py`, `scan_domain_neutrality.py`, `protocol_replay.py --check-drift`,
`check_falsification_contracts.py --inventory`, mas la corrida de los runners del job nuevo bajo un
interprete limpio con solo lo declarado.

**Re-juicio antes del commit de cierre.** Iteracion **1 de 2**; si la clase reaparece en la segunda,
escalo al operador humano en vez de pedir una tercera.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `1d78dc0873274b30300ec7613dfd2275b17a5cc2`, implementacion `a583e189`, padre `2767b2c7`.
Alcance: solo el hub, sin producto en alcance.
