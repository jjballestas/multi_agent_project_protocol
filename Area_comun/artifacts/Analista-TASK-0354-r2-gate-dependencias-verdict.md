# VEREDICTO TASK-0354 r2 -- el gate de dependencias del workflow

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0354-r2.md
    escrito             2026-08-10 12:05 local (UTC+2)  ==  2026-08-10T10:05Z
    veredicto           CHANGE-REQUIRED -- con ESCALADA al operador humano
    iteracion           2 de 2 consumida; no pido una tercera vuelta, la decision sube

## 0. Ancla canonica

    ancla de la instruccion   269e5d1340f64ff320fd724f5fadfd0a9afaecda
    implementacion            a47bed116aea540dc5a324d23b4ad6d1c7c1c675
    padre de la 1a entrega    2767b2c7881a097d2ce7f34eef4b799364da3333  (= a583e189^)

`.github/workflows/validate.yml` es byte-identico entre `a47bed11`, el ancla `269e5d13` y
`origin/main` (`d29fd21f`):

    git diff --stat a47bed11 d29fd21f -- .github/workflows/validate.yml   -> (vacio)
    git diff --stat 269e5d13 d29fd21f -- .github/workflows/validate.yml   -> (vacio)

Juzgo en el ancla. Alcance: **solo el hub, sin producto en alcance**.

## 1. Reproduccion -- clones limpios y entornos fieles

Tres clones `--shared --no-hardlinks` bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/rv0354r2/` (DECISION-0104), nunca en el arbol caliente:

    c1  @ 269e5d13   (medicion; `git status --short` vacio)
    c2  @ 269e5d13   (mutantes; restaurado y verificado limpio tras cada uno)
    c3  @ 2767b2c7   (anclaje "antes")

Y **tres interpretes**, uno por cada declaracion de job, porque este gate lee los paquetes
instalados del interprete en el que corre y por tanto un host gordo miente en las dos direcciones:

    venv_bare      (solo stdlib)                       == job falsification-runners
    venv_jy        jsonschema pyyaml                   == job falsification-runners-python
    venv_validate  cryptography jsonschema pyyaml      == job validate

Puertas de protocolo en `c1`, gateadas por `$?` del comando, nunca detras de un pipe:

    python scripts/validate_collaboration_state.py --root .           EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                          EXIT=0  OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .                 EXIT=0
    python runtime/protocol_replay.py --check-drift --root .          EXIT=0  drift CLEAN
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory          EXIT=0  runners=12/12 contracts=71/71

El gate bajo revision lo extraje del YAML **con un parser independiente** (PyYAML sobre el
documento, no copy-paste) a `gate.py`, quitando solo el envoltorio `python - <<'PY'` / `PY`.
3068 bytes. Todo mutante de abajo corre ese mismo cuerpo.

## 2. Tabla vector por vector

    vector                                                        veredicto      como lo fase
    ------------------------------------------------------------- -------------- ---------------------------
    F1 instancia -- el job nuevo arranca su runner                PASS           venv con SOLO lo declarado
    F1 clase -- "ningun runner se queda sin sus dependencias"     SLIPS (G1,G2)  dos escapes reproducidos
    F2 -- saldo AC6 derivado de las anclas y de un job tocado     PASS           re-derivado por mi en c1/c3
    F3 -- granularidad github.ref declarada por escrito           PASS           en el fichero de tarea
    F4 -- cancelacion declarada como residual de la puerta        PASS marginal  declarado en texto, no en el
                                                                                 `residuals=` de la propia puerta
    AC1 -- corrida realmente cancelada                            RESIDUAL OK    la entrega NO lo da por bueno
    AC2 -- residual de commits intermedios, por escrito           PASS           ahora en el fichero de tarea
    AC3 -- colocacion derivada por runner                         PASS           sin movimientos nuevos
    AC4 -- cero perdida de cobertura                              PASS           0 invocaciones de runner perdidas
    AC5 -- la dependencia dura sigue dura                         PASS           sin skip/which/try nuevos
    AC6 -- sin regresion, saldo del propio run                    PASS           4 corridas del replicador

Escapes que gatean el cierre: **G1** (vive HOY en el workflow), **G2** (clase, latente).
Observaciones declaradas: **G3**, **G4**, **G5**, **G6**, **G7**.

## 3. Lo que esta bien, y lo verifique mas fuerte que la entrega

### El gate mata el defecto original, y el diagnostico nombra las cuatro cosas

    U0  c1 intacto,        venv_validate     WORKFLOW_RUNNER_DEPENDENCIES PASS runners=72   EXIT=0
    M1  quito pyyaml del job falsification-runners-python
                                             WORKFLOW_RUNNER_DEPENDENCIES FAIL              EXIT=1
        falsification-runners-python: examples\runtime_turn_cases\run_runtime_turn_obstacle_cases.py
        imports yaml; requires one of ['pyyaml'], declared ['jsonschema']

### La instancia esta cerrada por COMPORTAMIENTO, no por lectura del YAML

No me quede en que el YAML diga `pyyaml`. Corri los runners de cada job en un interprete que tiene
**exactamente lo que ese job instala y nada mas**:

    venv_jy (jsonschema pyyaml)  == job falsification-runners-python
      python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py   EXIT=0
        "OK: authoritative delivery and in-schema friction controls are mutation-proved."
      python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py      EXIT=0
        "OK: real run-log append rejects red-gate empty obstacles; ... mutant is killed"

### La linea que la remediacion BORRO del job de Windows: justificada, y lo probe

`a47bed11` elimina `python -m pip install jsonschema` del job `falsification-runners`. Borrar una
instalacion es la mutacion que mas facilmente introduce el defecto que esta tarea venia a cerrar,
asi que la ejecute en el entorno exacto que deja ese job hoy -- `setup-python` y **ningun** paquete:

    HOST WINDOWS, c1 limpio, venv_bare (solo stdlib) en PATH
      python examples/mailbox_retry_cases/run_mailbox_retry_cases.py          EXIT=0
      "mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)"

Y segui la cadena de procesos hijo que ese runner dispara, porque el gate no la ve: el runner lanza
`powershell.exe` sobre `scripts/harness/peer_mailbox_cron.ps1`, que a su vez invoca
`& python scripts/ledger_head.py` y `& python -c "...runtime.protocol_replay..."`. Los dos objetivos
son stdlib puro (`ledger_head.py`: argparse/hashlib/json/pathlib/typing; `protocol_replay.py` no
tiene import externo de nivel superior y su `cryptography` es perezoso). El borrado es correcto.

### El recorrido de imports es `ast.walk`, y eso es una fortaleza

La instruccion preguntaba que direccion es la real. Medida:

    C1  import DENTRO de una funcion de un runner descubierto   -> gate FAIL   EXIT=1
    C2  importlib.import_module('attrs') en el mismo runner     -> gate PASS   EXIT=0

`ast.walk` si atrapa el import anidado. Solo el import dinamico se le escapa (G5, menor).

### El mapeo modulo -> distribucion esta bien hecho

`importlib.metadata.packages_distributions()` mas la normalizacion PEP 503 resuelven `yaml ->
pyyaml` sin la heuristica casera. En el entorno FIEL del job `validate` el mapa tiene **15 modulos**
y la lista de nombres locales **396** (169 stems de `.py` + 228 nombres de directorio, de los cuales
10 vienen de `.git`). Solape real: **`__pycache__`** y nada mas. La observacion de diseno del
encargo se confirma: la exclusion es mas ancha de lo necesario, pero hoy no enmascara nada.

## 4. G1 -- el gate ya no ve un runner que el workflow invoca HOY

Este es el hallazgo. El descubrimiento del gate ancla al principio de linea:

    r"(?m)^\s*python(?:3)?\s+([^\s]+\.py)(?:\s|$)"

Y el propio workflow, **dos pasos por encima del gate**, invoca un runner que no empieza la linea:

    .github/workflows/validate.yml, job validate, paso "Check systematic state pruning"
        run: |
          if ! python scripts/prune_state.py --root . --check; then

Medido con un matcher independiente sobre el mismo documento:

    descubrimiento del gate : 72 invocaciones
    descubrimiento amplio   : 73 invocaciones
    solo en el amplio       : [('validate', 'scripts/prune_state.py')]

No es una extension teorica: es la forma que el fichero gobernado ya usa. A/B con el **mismo**
defecto inyectado en el **mismo** job, cambiando solo el fichero que lo recibe:

    A  import attrs (externo, no declarado) en scripts/prune_state.py          <- NO descubierto
         gate                                    PASS runners=72        EXIT=0
         python scripts/prune_state.py --root . --check   (venv_bare)   EXIT=1
           ModuleNotFoundError: No module named 'attrs'
    B  import attrs en examples/runtime_prune_cases/run_runtime_prune_cases.py <- SI descubierto
         gate                                    FAIL                   EXIT=1
           validate: ...run_runtime_prune_cases.py imports attrs;
           requires one of ['attrs'], declared ['cryptography','jsonschema','pyyaml']

El discriminador no es la dependencia: es la **forma de la invocacion en el YAML**. Y el unico
testigo del recorte es el numero `runners=72`, que nada ata: no hay asercion, ni valor esperado, ni
comparacion contra un inventario. Reproducido:

    M3  mismo runner escrito como `cd . && python ...` + pyyaml quitado
          gate PASS runners=71   EXIT=0     (el contador baja en silencio)
    M5  mismo runner escrito como `python -m examples...` + pyyaml quitado
          gate PASS runners=71   EXIT=0

Es decir: reescribir la invocacion de un runner saca ese runner de la cobertura del gate sin ninguna
senal, y el defecto que M1 mata vuelve a pasar.

## 5. G2 -- la dependencia que llega por un modulo del propio repo es invisible

El gate parsea **solo el fichero del runner**. Todo nombre local se excluye y no se sigue. Demostrado
sin fabricar ninguna dependencia sintetica -- solo modulos de produccion y el idiom de `sys.path`
que los propios runners usan:

    mutante  examples/mailbox_retry_cases/run_mailbox_retry_cases.py  (job falsification-runners,
             que hoy no declara NADA) importa `runtime.turn_validate`, cuyo nivel superior tiene
             `import jsonschema` (runtime/turn_validate.py:12)

         gate                                            PASS runners=72   EXIT=0
         python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    EXIT=1
           File "...\runtime\turn_validate.py", line 12, in <module>
               import jsonschema
           ModuleNotFoundError: No module named 'jsonschema'

Un salto de indireccion y el defecto F1 vuelve entero: el job certifica un runner que muere en el
import. Es la misma consecuencia que ya medi en la primera vuelta, por otra coordenada.

### Y sin embargo hoy NO revienta nada: lo medi runner a runner

Escribi un analizador independiente que calcula, para cada runner que el workflow invoca, el
**cierre transitivo** de modulos locales y los externos alcanzables, y lo compara con lo que declara
su job. Resultado sobre el arbol del ancla:

    todos los externos transitivos del job validate  = cryptography / jsonschema / yaml  -> declarados
    falsification-runners-python: run_runtime_turn_obstacle_cases.py alcanza `cryptography`
        por 24 ficheros de cierre, pero el import es PEREZOSO y guardado
        (runtime/protocol_replay.py:282, dentro de funcion y bajo try) -> no rompe, y lo probe
    connectors/.../run_connector_sqlserver_readonly_cases.py alcanza `pymssql`, tambien perezoso
        y guardado (connector.py:151 -> ConnectorDisabledError) -> no rompe
    powershell-linux-parity: su .ps1 invoca scripts/scan_domain_neutrality.py, stdlib puro

Conclusion honesta: **la clase esta abierta, la instancia no**. Ningun runner del arbol de hoy se
queda sin sus dependencias. Lo que protege el arbol no es el gate, son los `try/except` de los
imports perezosos y la casualidad de que las invocaciones raras apunten a ficheros stdlib.

## 6. G3..G7 -- lo demas que medi

    G3  declaracion contada aunque el paso no se ejecute nunca
        M4  `if: false` sobre el paso "Install falsification runner dependencies"
              gate PASS runners=72  EXIT=0
        `declared_distributions()` recorre los pasos sin mirar `if:` ni el ORDEN: un `pip install`
        posterior al runner, o desactivado, cuenta igual como declarado.

    G4  formas de invocacion no reconocidas: `python -m <modulo>`, `& $pythonRunner`, `python -`.
        Cuatro puntos de entrada `.ps1` que el workflow ejecuta invocan python por dentro
        (run_neutrality_scan_cases.ps1, validate_collaboration_state.ps1, run_sdd_cases.ps1,
        run_compact_comms_cases.ps1) y el gate no abre un solo `.ps1`.

    G5  import dinamico (`importlib.import_module`) invisible. Hoy sin uso externo en los runners.

    G6  superficie de procesos HIJO invisible, y ademas silenciada: `peer_mailbox_cron.ps1` invoca
        `& python ... 2>$null` y decide por `$LASTEXITCODE`, asi que un modulo ausente ahi
        degradaria el resultado en vez de reventar. Hoy los objetivos son stdlib (verificado).

    G7  falso ROJO estructural: el mapa modulo->distribucion sale del interprete del job `validate`,
        pero se aplica a los demas jobs. Un job que declare CORRECTAMENTE algo que `validate` no
        instala se reporta como error. Reproducido:
        D   el job de Windows declara `python -m pip install requests` y su runner importa `requests`
              gate FAIL "imports unmapped external module requests"   EXIT=1
        Es fail-closed (seguro), pero acopla cualquier job futuro a la lista de `validate`. El repo
        ya documenta `python -m pip install pymssql` en connectors/sqlserver_readonly/s9_verify_live.py.

    contador  `runners=72` cuenta INVOCACIONES, no runners distintos
              (scripts/validate_collaboration_state.py se cuenta dos veces).

## 7. F2 -- el saldo, re-derivado por mi de las anclas y de los jobs que el cambio toca

Cuatro corridas del replicador en clon limpio, con `--job`, gateadas por exit code:

    c3 @ 2767b2c7  --job falsification-runners          EXIT=0  declared=4 pass=0 fail=0 unsupported=4
    c3 @ 2767b2c7  --job falsification-runners-python   EXIT=2  (el job no existe en el padre)
    c1 @ 269e5d13  --job falsification-runners          EXIT=0  declared=1 pass=0 fail=0 unsupported=1
    c1 @ 269e5d13  --job falsification-runners-python   EXIT=0  declared=3 pass=3 fail=0 unsupported=0

Cuadra con lo que declara la entrega y **sale de las anclas**, que es lo que faltaba en la primera
vuelta. Los `unsupported` del job de Windows son de mi host (sin `pwsh` 7), no del cambio; por eso
ejecute su runner a mano bajo `venv_bare` (seccion 3): EXIT=0.

Paridad de comandos con parser independiente (PyYAML, no regex de formato):

    2767b2c7 -> 269e5d13
      invocaciones de runner perdidas   : 0
      invocaciones de runner ganadas    : 0
      unica linea de comando perdida    : `python -m pip install jsonschema`  (job Windows; justificada
                                          y verificada por comportamiento en la seccion 3)
      movidas de job/host               : run_post_gate_obstacle_cases.py y
                                          run_runtime_turn_obstacle_cases.py, windows -> ubuntu
    a583e189 -> 269e5d13
      movidas de job/host               : NINGUNA  (la colocacion del AC3 no se toco en la remediacion)

    despues:  powershell-linux-parity ubuntu 5 pasos | validate ubuntu 78 | falsification-runners
              windows 1 | falsification-runners-python ubuntu 3

El AC4 se sostiene en su propia unidad (conjunto de runners: 0 perdidos). Mi conteo de "lineas de
comando" sube de 89 a 155 porque el heredoc del gate aporta 67 lineas; es artefacto de mi unidad,
no cobertura nueva.

Del job `validate` (78 pasos ahora, 77 antes) verifique el paso nuevo y los cuatro primeros en clon
limpio: `STEP 03/78 PASS Verify workflow runner dependency declarations`. La corrida completa de los
78 pasos excede el limite de mi ventana igual que le paso al maker; lo declaro como residual y no lo
presento como acreditado.

## 8. FOCO 3 -- lo que quedo abierto de la primera vuelta

    F3 granularidad     CUMPLIDO. El fichero de tarea declara ahora `github.workflow` + `github.ref`
                        y ACEPTA explicitamente la duplicacion push/pull_request. Era lo que pedia.
    AC2 residual        CUMPLIDO y MEJORADO. Ya no vive solo en un mensaje archivado: esta en
                        Area_comun/tasks/TASK-0354-*.md, donde quien retome la tarea lo va a encontrar.
    AC1 residual        CUMPLIDO. El fichero de tarea dice que la presencia del YAML no lo acredita y
                        que queda pendiente de dos pushes con la primera corrida en `cancelled`.
    F4 cancelacion      CUMPLIDO MARGINAL. Declarado en el fichero de tarea. La salida de la propia
                        puerta sigue sin nombrarlo en su `residuals=`; queda como residual conocido.
    AC3 colocacion      SIN MOVIMIENTO (verificado arriba: ninguna linea cambia de job/host).

## 9. Residuales declarados

1. **Sin CI real.** Todo esto es local; Actions sigue bloqueada por decision del operador. El AC1
   no es acreditable hoy. **El propio gate nunca ha corrido en GitHub Actions**, y su resultado
   depende del entorno del runner de Actions (que paquetes trae la imagen `ubuntu-latest`), que no
   es el mio: G7 dice que ese detalle puede cambiar el veredicto del gate.
2. **La corrida completa de los 78 pasos del job `validate` no la termine** (limite de ventana).
   Verifique el paso nuevo y los cuatro primeros; el resto queda sin medir en esta vuelta.
3. **`pwsh` 7 ausente en mi host:** el job de Windows sale `unsupported` en el replicador. Mitigado
   ejecutando su runner directamente bajo `venv_bare` en Windows (EXIT=0).
4. **Mi analizador transitivo tiene falsos positivos propios** (`scan_encoding`, `runtime`,
   `run_runtime_protocol_materialize_cases` aparecen como "externos" porque no reproduzco la
   manipulacion de `sys.path` de cada runner). No afectan a la conclusion: ningun externo REAL no
   declarado quedo sin explicar.
5. **`runners=72` cuenta invocaciones, no runners distintos**, y nada lo ata a un valor esperado.
6. **No juzgo el ahorro economico.** El reparto de los 2m26s entre los tres runners sigue sin medir;
   ningun AC lo pide.

## 10. Recomendacion de cierre

**CHANGE-REQUIRED.** Y como es la **iteracion 2 de 2**, no pido una tercera vuelta: **escalo al
operador humano** con la decision planteada, tal y como declare al cerrar la primera.

Lo entregado es mejor de lo que pedi: hay un mecanismo real, no una palabra suelta; mata el mutante
que importa; el mapeo distribucion-modulo esta bien resuelto; el borrado del `pip install` de
Windows esta justificado y lo probe en el entorno exacto; y los tres residuales que faltaban por
escrito estan ahora en el fichero de tarea, donde se van a encontrar.

Lo que no puedo certificar es la frase por la que se me pregunta. **El gate no cubre la clase.** Su
criterio de pertenencia es la FORMA de la invocacion (`^python <ruta>.py`), no la propiedad ("lo
invoca el workflow"), y el propio fichero gobernado ya contiene una forma que se le escapa
(`if ! python scripts/prune_state.py ...`). El defecto original vuelve a pasar por dos vias que
reproduje con exit codes: G1 (forma de invocacion) y G2 (una indireccion por un modulo del repo).

La decision que subo al operador, con los dos lados dichos:

- **A favor de cerrar con residual declarado:** medi el arbol entero y **hoy ningun runner se queda
  sin sus dependencias**. El riesgo vivo es cero; el hueco es de certificacion, no de servicio. El
  AC3 nombra "la dependencia se DERIVA del runner" y para los runners que el gate ve, se deriva.
- **A favor de una vuelta mas:** el hueco esta instanciado hoy en el mismo fichero, dos pasos por
  encima del gate, y el unico testigo (`runners=72`) no esta atado a nada, asi que el proximo
  refactor de una linea del YAML lo abre sin dejar senal. Es exactamente el patron de "la
  remediacion estrecha el dano sin cerrar la clase".

### Si el operador pide la vuelta 3, esto es lo minimo que la cierra

1. **Descubrir por propiedad, no por forma:** que el gate reconozca cualquier invocacion de python
   en cualquier posicion de la linea, y la forma `-m`. Se falsa con M3 y M5: el mismo runner escrito
   `cd . && python ...` y `python -m ...` con la dependencia quitada debe dar EXIT=1.
2. **Atar el contador:** que `runners=N` se compare con un inventario esperado y que una bajada sea
   roja. Se falsa con M3: hoy 72 -> 71 en silencio.
3. **Seguir un salto de indireccion local**, o declarar por escrito que la superficie cubierta es el
   fichero del runner y nada mas. Se falsa con el mutante de la seccion 5.
4. **Honrar `if:` y el orden** al contar una declaracion (G3, falsable con M4).
5. **Declarar G4/G6/G7** (formas `.ps1` y procesos hijo fuera de alcance; acoplamiento del mapa al
   entorno de `validate`).

### Puertas afectadas y ciclo

`validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`, `check_falsification_contracts.py --inventory`, mas el propio
gate bajo un interprete con SOLO lo que cada job declara. Iteracion 2 de 2 consumida: la siguiente
la autoriza el operador, no yo.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `269e5d1340f64ff320fd724f5fadfd0a9afaecda`, implementacion `a47bed11`, padre `2767b2c7`.
Alcance: solo el hub, sin producto en alcance.
