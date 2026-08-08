# Veredicto TASK-0336 re-juicio remediacion 1 -- CHANGE-REQUIRED (muy estrecho): las tres familias que bloqueaban estan MUERTAS y las VEINTE fronteras son PORTANTES, pero queda viva una familia de escape PREEXISTENTE que mi muestreo de r1 no toco, y cae dentro del alcance que la certificacion acotada afirma

Analista, 2026-08-08 04:58 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Tu pregunta era binaria: *queda algun escape vivo, o la certificacion afirmativa ya se
puede sostener tal como se emite?* **Queda uno.** No es el que te reporte en r1 -- ese esta muerto,
lo verifique --, y no lo introdujo esta remediacion: **es anterior a ella**, lo probe contra el
checker de `a6dc0c6e` y tambien lo aceptaba. Es una familia que mi muestreo de r1 **no toco**, y lo
digo asi porque el hallazgo no habla peor del maker que de mi sondeo anterior.

Lo que la remediacion cierra, lo cierra de verdad:

    familia de r1                          r2
    set +e / set +o errexit dentro          MUERTA   (rechazada, exit 1)
    trap ... ERR dentro                     MUERTA   (rechazada, exit 1)
    defaults.run.shell rechazado (falso -)  CORREGIDO por los DOS niveles (job y workflow)
    continue-on-error de JOB sin frontera   CORREGIDA (frontera nueva, y es PORTANTE)
    certificacion afirmativa sin acotar     ACOTADA + residuales declarados y con frontera propia

Y las **veinte** fronteras declaradas son portantes: cero vacuas, matriz por frontera, cada una con
discriminador propio. El AC4 se cumple en su version dura, otra vez.

Lo que bloquea es una sola propiedad, y es la misma de siempre expresada en otra gramatica: **el
gate normaliza `\` a `/` antes de mirar las lineas, y con eso borra el marcador de continuacion de
linea de bash.** Un bloque cuya primera linea termina en `\` hace que la invocacion del runner se
convierta en un ARGUMENTO de la linea anterior. El runner **no se ejecuta**, el paso sale **0**, y
el gate lo certifica con exit 0 dentro de `scope=...direct_invocation...`.

Es exactamente la familia `echoed` -- la mutacion que el propio contrato declara como muerta
(`run: echo python examples/orphan/run_orphan.py`) -- repartida en dos lineas.

## Anclaje

- Juicio anclado en **`7b33440c00a4301cdafadb3565f11398328cb51d`** (`origin/main` al abrir la
  revision, y `HEAD` del arbol vivo).
- Commit de implementacion citado: **`a69207a4`**.
  `git diff --stat a69207a4 origin/main -- scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py Area_comun/protocol/FALSIFICATION_CONTRACTS.json .github/workflows/validate.yml`
  -> **vacio**. Las rutas de alcance son identicas byte a byte entre la entrega y la punta canonica;
  los cuatro commits intermedios (`1607de7b`, `916e7338`, `d4daa115`, `7b33440c`) son memoria,
  mailbox y coordinacion. El juicio vale para las dos.
- Clon limpio en `D:/Aegis_Scratch/mapp/r0336/cc`, **detached en `7b33440c`**, `git status --short`
  vacio, `__pycache__` purgado antes de medir.
- Sondas reproducibles (mias, fuera del arbol atestado, en `D:/Aegis_Scratch/mapp/r0336/mut/`):
  `probe_r2.py` (checker vs bash real), `probe_r2b.py` (familia de continuacion),
  `probe_r2c.py` (AC3 por los dos lados, 22 formas), `probe_r2d.py` (las cuatro puertas de shell +
  residuales), `probe_r2e.py` (preexistencia contra el checker de `a6dc0c6e`),
  `matrix_r2.py` (matriz de falsabilidad de las 20 fronteras).
- Bash real: `C:/Program Files/Git/usr/bin/bash.exe`, invocado como GitHub lo hace
  (`bash --noprofile --norc -eo pipefail <script>`).
  **Nota de metodo:** el `bash` que resuelve por PATH desde Python en esta maquina es el de **WSL**,
  no el de Git; con el, todas las medidas salen `exit 1` por `execvpe(/bin/bash) failed`. Un
  muestreo que no fije el binario mide ruido. Lo dejo escrito porque me costo dos vueltas.
- Estado canonico del arbol vivo antes de empezar: `validate_collaboration_state.py` **exit 0**.

## Gates recomputados por exit code en clon limpio sobre `7b33440c`

    python scripts/test_falsification_contracts.py                                     EXIT 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml --inventory                          EXIT 0
    python scripts/validate_collaboration_state.py --root .                            EXIT 0
    python scripts/scan_encoding.py --root .                                           EXIT 0
    python scripts/scan_domain_neutrality.py --root .                                  EXIT 0
    python runtime/protocol_replay.py --check-drift --root .   EXIT 0  verdict=CLEAN up_to_seq=7813

**Drift 0.** Los seis gates que el handoff declara verdes lo son. Mi objecion no es un gate rojo:
es un escape por comportamiento que los seis gates verdes no ven.

## Foco A -- AC3 por los DOS lados. PASA.

22 formas, cada una un fixture propio, gateadas por exit code del checker entregado.

    lado ACEPTACION (debe aceptar: la forma SI gatea)                        exit  correcto
    A01 linea unica, ubuntu-latest                                            0     si
    A02 linea unica, windows-latest                                           0     si
    A03 multilinea con shell: bash (windows)                                  0     si
    A04 multilinea, ubuntu-latest, shell implicito                            0     si
    A05 multilinea, macos-14, shell implicito                                 0     si
    A06 multilinea con JOB defaults.run.shell: bash        <- fallaba en r1   0     si
    A07 multilinea con WORKFLOW defaults.run.shell: bash   <- fallaba en r1   0     si
    A08 if: always() de paso                                                  0     si
    A09 continue-on-error: false literal                                      0     si
    A10 multilinea donde las extra son comentarios                            0     si

    lado RECHAZO (debe rechazar: la forma NO gatea)                          exit  correcto
    R01 multilinea con shell por defecto de windows (pwsh)                    1     si
    R02 multilinea con shell: pwsh explicito                                  1     si
    R03 JOB defaults pwsh sobre WORKFLOW defaults bash (precedencia)          1     si
    R04 set +e dentro del bloque bash                      <- vivo en r1      1     si
    R05 trap 'exit 0' ERR dentro del bloque bash           <- vivo en r1      1     si
    R06 continue-on-error: true a nivel de JOB                                1     si
    R07 if: false a nivel de JOB                                              1     si
    R08 needs: a nivel de JOB                                                 1     si
    R09 on: solo workflow_dispatch                                            1     si
    R10 runner || true                                                        1     si
    R11 echo runner                                                           1     si
    R12 if: false de paso                                                     1     si

    desajustes: 0

Los dos falsos negativos de r1 (`defaults.run.shell` en job y en workflow) estan corregidos, y la
precedencia esta bien: el shell del PASO manda sobre el del JOB, y el del JOB sobre el del WORKFLOW
(R03 lo discrimina). **No implementaron "un comando por paso"**: un bloque bash de tres comandos se
sigue aceptando y sale con 3 bajo bash real cuando el runner sale con 3. Ese lado de tu pregunta,
que era el que fallaba, esta resuelto por ambos extremos.

## Foco B -- AC4: las VEINTE fronteras, portantes. PASA, sin hueco.

Metodo igual que en r1 y por la misma razon: **21 relajaciones dirigidas del checker**, y cada una
evaluada contra los 21 fixtures **por separado**, no a traves de la cadena ordenada de `assert`, para
que ninguna frontera redundante se esconda detras de un fallo anterior.

    relajacion                                        fronteras que VOLTEA
    L1  sin comprobacion de claves de on:             dispatch_only
    L2  sin needs de job                              job_needs
    L3  sin if: de job                                job_if_false
    L4  sin if: de paso                               step_if_false, step_if_event
    L5  if: acepta cualquier string                   step_if_event
    L6  sin continue-on-error de JOB                  job_continue_on_error      <- el hueco de r1
    L7  sin continue-on-error de paso                 continued_expression/string/literal
    L8  coe: solo bool True rechazado                 continued_expression, continued_string
    L9  coe: solo strings rechazados                  continued_literal, job_continue_on_error
    L10 ancla solo al INICIO (camino del comando)     bash_or_true, semicolon_exit, no_op_help
    L11 ancla solo al FINAL (camino del comando)      bash_or_true, echoed, semicolon_exit, no_op_help
    L12 partir la linea por ';' antes de casar        semicolon_exit
    L13 aceptar CUALQUIER multilinea sin razonar shell multiline_pwsh
    L14 ENDURECE: quitar la excepcion multilinea      multiline_bash, job_defaults_bash, workflow_defaults_bash
    L15 mencion textual de la ruta (defecto 0330)     bash_or_true, echoed, multiline_pwsh,
                                                      multiline_set_plus_e, multiline_trap_err,
                                                      semicolon_exit, no_op_help
    L16 bash_block_preserves_abort desactivado        multiline_set_plus_e, multiline_trap_err
    L17 shell resuelto solo desde el paso (pre-fix)   job_defaults_bash, workflow_defaults_bash
    L18 defaults: solo los del job                    workflow_defaults_bash
    L19 defaults: solo los del workflow               job_defaults_bash
    L20a renombrar a FALSIFICATION_EXECUTION_GUARANTEED  no_EXECUTION_GUARANTEED
    L20b borrar la declaracion de residuales          residuals_declared

    frontera                    estado      volteada por
    multiline_pwsh              PORTANTE    L13, L15
    multiline_bash              PORTANTE    L14          (lado ACEPTACION)
    multiline_set_plus_e        PORTANTE    L15, L16     NUEVA
    multiline_trap_err          PORTANTE    L15, L16     NUEVA
    job_defaults_bash           PORTANTE    L14, L17, L19  NUEVA (lado ACEPTACION)
    workflow_defaults_bash      PORTANTE    L14, L17, L18  NUEVA (lado ACEPTACION)
    step_if_false               PORTANTE    L4
    step_if_event               PORTANTE    L4, L5
    bash_or_true                PORTANTE    L10, L11, L15
    semicolon_exit              PORTANTE    L10, L11, L12, L15
    continued_expression        PORTANTE    L7, L8
    continued_string            PORTANTE    L7, L8
    continued_literal           PORTANTE    L7, L9
    job_continue_on_error       PORTANTE    L6, L9       NUEVA
    echoed                      PORTANTE    L11, L15
    job_needs                   PORTANTE    L2
    job_if_false                PORTANTE    L3
    dispatch_only               PORTANTE    L1
    no_EXECUTION_GUARANTEED     PORTANTE    L20a         NUEVA (frontera de texto)
    residuals_declared          PORTANTE    L20b         NUEVA (frontera de texto)
    no_op_help (extra, no decl) PORTANTE    L10, L11, L15

    fronteras nunca volteadas: 0

Tres cosas que quiero dejar dichas:

1. **El hueco de r1 esta cerrado y no de forma decorativa.** `L6` (borrar `failure_reaches_job(job)`)
   ahora voltea `job_continue_on_error`, y `L9` la voltea por un camino distinto. Tiene dos
   discriminadores, no uno.
2. **Las dos fronteras de TEXTO son portantes y separables.** `L20a` (renombrar la linea) voltea
   solo la frontera del nombre; `L20b` (borrar los residuales) voltea solo la del residual. Un maker
   futuro no puede reponer la certificacion afirmativa ni borrar la acotacion sin romper el contrato.
   Eso convierte la honestidad de la salida en una propiedad **verificada**, no en una promesa de
   handoff. Es la mejor pieza de esta remediacion.
3. **`L18`/`L19` discriminan los dos niveles de `defaults` por separado**, igual que `L10`/`L11`
   discriminan los dos extremos del ancla. No son una frontera duplicada.

Nota de honestidad sobre la matriz: en mi primera pasada `L10`/`L11` no voltearon nada porque la
linea del ancla aparece **dos veces** en el fichero y mi sustitucion toco solo la primera (la del
helper de bloque). Repeti las dos relajaciones apuntando a la ocurrencia del camino del comando
(`L10b`/`L11b` en la corrida) y volvieron a discriminar. La conclusion no cambia -- esas fronteras ya
eran portantes por `L15` --, pero el numero de la tabla es el de la sustitucion correcta.

## Foco C -- AC5: la certificacion. NO CUMPLE, por poco y por dentro de su propio alcance.

La salida entregada ya no afirma ejecucion garantizada:

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=53/53
      scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure
      residuals=trigger_filters,working_directory,yaml_1_1_scalars

Eso es la disciplina del "47" bien aplicada: nombra lo que afirma y nombra lo que no. Verifique los
tres residuales uno a uno y son exactamente los declarados (los tres se aceptan con exit 0:
`on: paths: ['docs/**']`, `working-directory:`, `continue-on-error: no`). Estan **acotados**, ya no
son afirmaciones falsas.

El problema es que el escape que sigue vivo **no** cae en ningun residual declarado: cae dentro de
`direct_invocation`, que la linea afirma. Mientras eso sea asi, la cifra acotada tampoco se sostiene.

### C.1 -- SLIP BLOQUEANTE: la continuacion de linea borra la invocacion, y el gate no la ve

`command_gates_runner` normaliza cada linea con `line.strip().replace("\\", "/")` antes de casar. Esa
sustitucion existe para tolerar separadores de Windows en la ruta, pero convierte el marcador de
continuacion de bash en una barra inocua. La linea deja de terminar en `\` **para el gate**, mientras
que **para bash sigue terminando en `\`**.

Medido con bash real (invocacion exacta de GitHub) y con el checker entregado de punta a punta, con
un runner que imprime `RUNNER-EXECUTED` y sale con 3:

    bloque (shell bash)                      exit del PASO  runner ejecutado  veredicto del gate
    echo before / runner / echo after              3             SI           acepta   correcto
    echo before \ / runner / echo after            0             NO           acepta   *** ESCAPE ***
    echo \ / runner                                0             NO           acepta   *** ESCAPE ***
    python -c exit \ / runner                      0             NO           acepta   *** ESCAPE ***
    echo x \ / runner / echo done                  0             NO           acepta   *** ESCAPE ***
    # comentario \ / runner                        3             SI           acepta   correcto
    runner / echo tail \                           3             SI           acepta   correcto

Bash une `echo before \` con la linea siguiente: el comando efectivo es
`echo before python examples/cases/run_cases.py`. **El runner nunca se invoca.** El paso sale 0
aunque el runner estuviera roto.

Y la certificacion que el gate emite sobre ese fixture, de punta a punta:

    FALSIFICATION_STATIC_WIRING runners=1/1 contracts=1/1
      scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure
      residuals=trigger_filters,working_directory,yaml_1_1_scalars
    FALSIFICATION_INVENTORY permanent_negatives=1 declared=1 missing=0
    CHECKER_EXIT=0

El escape entra por las **cuatro** puertas de shell, incluidas las dos que esta remediacion abrio:

    puerta                                        checker exit
    shell: bash en el paso (windows-latest)             0
    ubuntu-latest con shell implicito                   0
    JOB defaults.run.shell: bash                        0     <- puerta nueva
    WORKFLOW defaults.run.shell: bash                   0     <- puerta nueva

No lo cargo como regresion: **la remediacion no introdujo el defecto, lo heredo** (ver C.2). Pero al
ampliar las puertas de shell de dos a cuatro, amplio tambien la superficie por la que se alcanza.

### C.2 -- de quien es el fallo: preexistente, y mi muestreo de r1 no lo toco

Corri el MISMO fixture generado contra el checker anterior a la remediacion (`a6dc0c6e`) y contra el
entregado (`a69207a4`), con un solo generador para que ninguna diferencia de escapado del shell
contaminara la comparacion:

    caso                                   prev a6dc0c6e   entregado a69207a4
    control echo/runner/echo                   exit=0          exit=0
    continuacion que traga el runner           exit=0          exit=0     <- vivo en los dos
    echo \ pelado + runner                     exit=0          exit=0     <- vivo en los dos
    python -c exit \ + runner                  exit=0          exit=0     <- vivo en los dos
    set +e (escape de r1)                      exit=0          exit=1     <- muerto por la remediacion
    trap ERR (escape de r1)                    exit=0          exit=1     <- muerto por la remediacion

Es un escape **anterior a la remediacion 1**. Mi tabla B.3 de r1 construyo los bloques con saltos de
linea limpios y nunca probo una linea terminada en `\`; el maker cerro fielmente lo que le declare y
esta familia no estaba en mi declaracion. Lo digo aqui con todas las letras porque el AC1 de esta
tarea existe precisamente para que los escapes se reproduzcan antes de certificar que mueren, y esta
vez el que fallo primero fue el muestreo del checker.

### C.3 -- honestidad del muestreo r2: lo que probe y NO escapo

    forma                                                  exit  lectura
    escalar plegado `run: >` que colapsa a una sola linea    1    falla cerrado, correcto
    escalar plegado `run: >` que conserva 3 lineas           0    acepta y gatea (medido: exit 3)
    `echo before \ ` (barra + espacio, NO continua en bash)  0    acepta y gatea (medido: exit 3)
    `python ./examples/...` (prefijo relativo)               1    falla cerrado
    `python runner &` (segundo plano)                        1    falla cerrado
    `needs:` a nivel de paso (guarda inerte)                 1    falla cerrado
    `continue-on-error: 'false'` (string)                    1    falla cerrado
    `if: success()`                                          0    acepta, correcto
    linea extra `python -c exit` sin continuacion            0    acepta y gatea (medido: exit 3)
    comentario terminado en `\`                              0    acepta y gatea (medido: exit 3)

La familia que falla es concretamente **la linea ejecutable (echo o python) terminada en `\` dentro
de un bloque multilinea**. Ni el comentario terminado en `\` ni la barra seguida de espacio escapan:
en bash ninguno de los dos continua la linea, y el gate acierta al aceptarlos.

## Foco D -- AC2, factor (a): los filtros de `on:`. DECLARADO, no implementado.

`workflow_steps` sigue comprobando solo que las CLAVES `push` y `pull_request` existan; un
`on: push: paths: ['docs/**']` se acepta con exit 0 y ese workflow no corre ante un cambio de codigo.
Lo verifique: exit 0.

**No lo cargo como slip**, y este es el cambio respecto a r1: el AC2 pide para (a) literalmente
*"`if:` y `needs:` de paso y job"*, y eso esta; los filtros los nombra el intake, y el AC5 admite
explicitamente *"o lo emite acotado a lo que de verdad garantiza"*. La salida dice `scope=trigger_keys`
-- no "triggers" -- y lista `trigger_filters` entre los residuales, con una frontera que lo protege.
Eso es acotar bien. Queda como **residual declarado**, no como afirmacion falsa.

## Foco E -- sin regresion en lo probado. PASA.

- `git log -1 -- .github/workflows/validate.yml` -> **`f6d88cb7`** (TASK-0330). `a69207a4` toca
  exactamente tres ficheros: los dos scripts de alcance y el fichero de la tarea. El `out_of_scope`
  se respeto por construccion.
- El job `falsification-runners` sigue intacto: `runs-on: windows-latest`, un paso por runner,
  invocaciones directas de una linea, `if: always()` en los dos siguientes.
- La regla endurecida **acepta la forma buena**: corrida canonica exit 0 con `runners=8/8
  contracts=53/53`. El gate duro no rechaza el cableado correcto. No hay ironia.

## Residuales declarados

- **RD1 -- filtros de `on:`** (foco D). Declarado por el gate y con frontera. No bloqueante.
- **RD2 -- `working-directory:`**. Verificado: exit 0 con `working-directory: examples`. Declarado.
  Falla ruidoso en CI (fichero no encontrado), no escape silencioso. Severidad baja.
- **RD3 -- escalares YAML 1.1**. Verificado: `continue-on-error: no` se acepta (PyYAML lo resuelve a
  `False`). Declarado. **No lo verifique contra el parser real de GitHub**; sigue siendo residual a
  comprobar, no hallazgo.
- **RD4 -- guarda inerte `"needs" in step`**. Los pasos de GitHub Actions no tienen clave `needs:`.
  Codigo defensivo muerto, reconocido en el handoff, fuera del alcance afirmativo.
- **RD5 -- `needs:` de job rechazado de plano.** Un job con `needs:` legitimo se rechaza (exit 1).
  Falla cerrado; solo lo anoto para que no sorprenda si alguien encadena jobs manana.

## Recomendacion de cierre

**CHANGE-REQUIRED (muy estrecho).** Iteracion **2 de un maximo de 2**; si hace falta una tercera,
escalo al operador humano segun lo que declare en r1.

    AC1  falsacion previa reproducida         CUMPLE    (L15 reproduce el defecto 0330 y voltea 7 fronteras)
    AC2  los cuatro factores                  PARCIAL   ((c) tiene viva la familia de continuacion)
    AC3  regla cierta por los dos lados       PARCIAL   (22/22 formas correctas; falla solo en la familia C.1)
    AC4  contrato falsable, fronteras         CUMPLE    (20/20 portantes, cero vacuas, hueco de r1 cerrado)
    AC5  certificacion honesta                NO CUMPLE (acotada bien, pero el escape cae DENTRO de direct_invocation)
    AC6  sin regresion, gates verdes          CUMPLE

### Remediacion pedida (una sola propiedad; no prescribo la forma)

1. **Cerrar la familia C.1.** La continuacion de linea de bash no puede ser invisible al gate. Dos
   caminos posibles, los dos satisfacen la propiedad: **unir** las lineas continuadas antes de casar
   (la linea logica `echo before python .../run_orphan.py` deja de casar la invocacion y el bloque se
   rechaza), o **fallar cerrado** ante cualquier linea cruda terminada en `\` dentro de un bloque
   multilinea. Si se elige unir, cuidado con no romper A10 (comentarios) ni el comentario terminado
   en `\`, que en bash **no** continua.
2. **Una frontera nueva que lo pruebe**, con la forma medida arriba: bloque `shell: bash` con
   `echo before \` seguido de la invocacion, `!= 0`. Sin ella la correccion no es falsable.
   Si el arreglo se hace por union de lineas, conviene una segunda frontera `== 0` para el
   comentario terminado en `\`, que debe seguir aceptandose.
3. **Nada mas.** No pido tocar la acotacion (esta bien), ni los residuales (estan bien declarados y
   con frontera), ni el cableado del workflow (intacto y correcto).

### Gates afectados por la remediacion

    python scripts/test_falsification_contracts.py                                  exit 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml --inventory                       exit 0
    python scripts/validate_collaboration_state.py --root .                         exit 0
    python scripts/scan_encoding.py --root .                                        exit 0
    python scripts/scan_domain_neutrality.py --root .                               exit 0
    python runtime/protocol_replay.py --check-drift --root .                        exit 0

Mas la no-regresion del foco E: la corrida canonica debe seguir dando `runners=8/8 contracts=53/53`
y `.github/workflows/validate.yml` debe seguir sin tocarse.

### Re-juicio antes del commit de cierre

Vuelvo a correr, en clon limpio sobre el commit de remediacion: la matriz de falsabilidad completa
(las 20 de hoy mas la nueva, para que ninguna quede vacua), las 22 formas del foco A enteras (para
que el endurecimiento no se coma ninguna forma buena, en particular A10 y el comentario terminado en
`\`), y la familia C.1 completa contra bash real fijando el binario de Git. Sin ese re-juicio no hay
OK-CLOSABLE.

## Nota de disciplina heredada

Mientras C.1 siga viva, la linea `FALSIFICATION_STATIC_WIRING runners=8/8 contracts=53/53` **no se
cita como prueba de ejecucion** en ningun handoff ni reporte. Es la condicion dura que la tarea
hereda de 0330 y del "47". Cuando C.1 muera, la linea sigue sin ser prueba de ejecucion -- es una
afirmacion de CABLEADO ESTATICO, y asi la nombra --, pero entonces sera cierta dentro de su alcance,
que es lo unico que se le pide.

-- Analista
