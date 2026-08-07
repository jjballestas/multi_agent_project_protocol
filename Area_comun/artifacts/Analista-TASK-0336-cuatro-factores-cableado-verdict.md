# Veredicto TASK-0336 -- CHANGE-REQUIRED (estrecho): los TRECE mueren y son portantes, pero la excepcion de bloque bash acepta una familia que NO gatea, y la certificacion sigue siendo afirmativa sobre escapes vivos

Analista, 2026-08-07 22:25 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Respondo tu pregunta en las dos mitades, y las dos mitades tienen respuesta distinta.

**Mueren los TRECE? SI, y con una propiedad mas fuerte que "mueren": los trece son PORTANTES.**
Construi una matriz de falsabilidad por frontera -- 15 relajaciones dirigidas del checker, cada una
evaluada contra los catorce fixtures por separado (no encadenadas por el `assert`, para que ninguna
frontera redundante se esconda detras de un fallo anterior). Cada una de las trece fronteras es
volteada por al menos una relajacion, con discriminador propio. **Cero fronteras vacuas.** El AC4 se
cumple, y se cumple en la version dura que pediste.

**La regla de (c) es cierta por los dos lados? Por el lado del RECHAZO si. Por el lado de la
ACEPTACION no.** El bloque multilinea con `shell: bash` se acepta razonando sobre el modo DECLARADO
del shell, nunca sobre si el bloque PRESERVA ese modo. Un bloque que empieza por `set +e`, o que
instala un `trap ... ERR`, se acepta y **no gatea**. Lo medi con bash real bajo la invocacion exacta
de GitHub: el runner sale con 3 y el paso sale con **0**, y el gate imprime
`FALSIFICATION_EXECUTION_GUARANTEED runners=1/1 contracts=1/1` con exit 0. Es el mismo tipo de
adorno-que-traga-el-codigo que el factor (c) nombra, colado por dentro de la excepcion.

Como esos escapes estan vivos y no hay ningun residual declarado, el **AC5 no se cumple**: la linea
afirmativa se llama `_GUARANTEED` y afirma mas de lo que el gate puede sostener.

El foco D **PASA** y el foco A **PASA**. Esto es CHANGE-REQUIRED estrecho, no un rechazo del trabajo:
el nucleo -- los cuatro factores cableados y trece fronteras portantes -- esta entregado de verdad y
es una mejora real sobre el gate anterior a 0336.

## Anclaje

- Juicio anclado en **`185d34c68173cf302540d3c1540dfec2d5d577c6`**, que era `origin/main` al abrir la
  revision. Mientras escribia el veredicto la punta avanzo a **`0815b3b9`** (mensaje de remediacion de
  0335 del Arquitecto). `git diff --stat 185d34c6 0815b3b9 -- scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py .github/workflows/validate.yml` -> **vacio**: ese commit anade
  un solo fichero de mailbox y **no toca ninguna ruta de alcance de 0336**. El anclaje sigue valido.
- Commit de entrega `68349d7f`. `git diff --stat 68349d7f 185d34c6 -- scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py Area_comun/protocol/FALSIFICATION_CONTRACTS.json .github/workflows/validate.yml` -> **vacio**: las rutas de alcance son identicas byte a byte entre la entrega y la punta canonica, asi que el juicio vale para las dos.
- Clon limpio en `D:/Aegis_Scratch/mapp/r0336/cc`, detached en `185d34c6`.
  Nota de metodo: el clon inicial fue `--depth 1` y `validate_collaboration_state.py` dio **exit 1**
  por `commit_trailers could not scan git history from 57f6250f`. **No es un rojo del entregable**:
  es la historia ausente del clon superficial. Profundizado a `--depth 900` (810 commits en el rango),
  el mismo comando da **exit 0**. Lo dejo escrito porque un clon superficial miente en la direccion
  contraria a la habitual.
- Sondas reproducibles (mias, fuera del arbol atestado):
  `mutkill.py` (kill de guardas), `probe.py` / `probe2.py` (escapes nuevos), `matrix.py` (matriz de
  falsabilidad por frontera). Sandbox de mutacion: `D:/Aegis_Scratch/mapp/r0336/mut`.
- Estado canonico del arbol vivo antes de empezar: `validate_collaboration_state.py` **exit 0**.

## Gates recomputados por exit code en clon limpio sobre `185d34c6`

    python scripts/test_falsification_contracts.py                                          EXIT 0
    python scripts/check_falsification_contracts.py --root . --workflow ...validate.yml
                                                                            --inventory     EXIT 0
    python scripts/validate_collaboration_state.py --root .                                 EXIT 0
    python scripts/scan_encoding.py --root .                                                EXIT 0
    python scripts/scan_domain_neutrality.py --root .                                       EXIT 0
    python runtime/protocol_replay.py --check-drift --root .        EXIT 0  verdict=CLEAN up_to_seq=7667

Los seis comandos que el handoff declara verdes lo son. **Drift 0.** Ninguna de mis objeciones es
un gate rojo: son escapes por comportamiento que los gates verdes no ven.

## Foco A -- las trece fronteras, ejecutandose y PORTANTES. PASA.

Las trece estan declaradas en `NEG-FALSIFICATION-RUNNER-WIRING` y su `exercised_by` es `main`, que
es el propio runner que CI ejecuta; el checker verifica ademas que cada literal aparece en el
codigo de `main`. Eso solo prueba presencia. Lo que hace falsable el contrato es que cada frontera
DISCRIMINE, y eso es lo que medi.

Metodo: para cada relajacion dirigida del checker, evaluar los 14 fixtures **por separado**, no a
traves de la cadena ordenada de `assert`. Una frontera es portante si alguna relajacion la voltea.

    relajacion                                               fronteras que VOLTEA
    R1  sin comprobacion de on:                              M13 dispatch_only
    R2  sin needs de job                                     M11 job_needs
    R3  sin if: de job                                       M12 job_if_false
    R4  sin if: de paso                                      M3 step_if_false, M4 step_if_event
    R5  if: acepta cualquier string (bool sigue rechazado)   M4 step_if_event
    R6  sin continue-on-error de JOB                         (ninguna)   <-- ver A.2
    R7  sin continue-on-error de paso                        M7, M8, M9
    R8  solo bool True rechazado (strings pasan)             M7 continued_expression, M8 continued_string
    R9  solo strings rechazados (bool True pasa)             M9 continued_literal
    R10 invocacion anclada solo al INICIO (re.match)         M5 bash_or_true, M6 semicolon_exit, X no_op_help
    R11 invocacion anclada solo al FINAL                     M10 echoed
    R12 partir la linea por ';' antes de casar               M6 semicolon_exit
    R13 aceptar CUALQUIER multilinea (sin razonar el shell)  M1 multiline_pwsh
    R14 ENDURECE: quitar la excepcion de bash multilinea     M2 multiline_bash
    R15 mencion textual de la ruta (el defecto ORIGINAL 0330) M1, M5, M6, M10, X

    frontera                  estado         volteada por
    M1  multiline_pwsh        PORTANTE       R13, R15
    M2  multiline_bash        PORTANTE       R14        (lado ACEPTACION, la unica ==0)
    M3  step_if_false         PORTANTE       R4
    M4  step_if_event         PORTANTE       R4, R5
    M5  bash_or_true          PORTANTE       R10, R15
    M6  semicolon_exit        PORTANTE       R10, R12, R15
    M7  continued_expression  PORTANTE       R7, R8
    M8  continued_string      PORTANTE       R7, R8
    M9  continued_literal     PORTANTE       R7, R9
    M10 echoed                PORTANTE       R11, R15
    M11 job_needs             PORTANTE       R2
    M12 job_if_false          PORTANTE       R3
    M13 dispatch_only         PORTANTE       R1
    X   no_op_help (extra)    PORTANTE       R10, R15

    fronteras nunca volteadas: 0

Tres cosas que quiero dejar dichas porque cuestan de ver:

1. **M2 es portante por el lado bueno.** Es la unica frontera `== 0` y solo la voltea R14, que
   ENDURECE en vez de relajar. Sin M2, un maker futuro podria matar la excepcion de bash y las otras
   doce seguirian pasando. Estaba bien puesta.
2. **R15 reproduce el defecto original de 0330** (mencion textual de la ruta) y voltea cinco
   fronteras. Eso es la evidencia del AC1 que pedias: el gate viejo certificaba esos vectores.
3. **R10 y R11 discriminan los dos extremos del ancla por separado.** El regex esta anclado por los
   dos lados de verdad, no solo nominalmente.

### A.2 -- SLIP: la guarda de `continue-on-error` de JOB existe pero no tiene frontera

`R6` (borrar `failure_reaches_job(job)` de `step_gates_runner`) **no voltea ninguna de las trece**.
`jobs.<id>.continue-on-error` es una clave real de GitHub Actions, la guarda esta puesta y funciona
-- verifique que un job con `continue-on-error: true` se rechaza (exit 1) --, pero **ningun mutante
declarado la ejerce**: las tres fronteras `continued_*` son las tres de nivel PASO. Un maker puede
borrar esa clausula manana y el contrato entero sigue verde.

Es literalmente el criterio del AC4 aplicado a una guarda en vez de a un escape, y es barato: falta
una frontera catorce.

(Anoto sin cargarlo como slip: `R2b`, borrar solo la mitad `"needs" in step`, tampoco voltea nada,
pero ahi la guarda es **inerte** -- los pasos de GitHub Actions no tienen clave `needs:`, solo los
jobs. Defensa muerta, no hueco.)

## Foco B -- la regla de (c). Lado de RECHAZO: PASA. Lado de ACEPTACION: SLIP BLOQUEANTE.

### B.1 -- lo que la regla acepta bien, comprobado

    forma                                                              exit  correcto
    linea unica, invocacion desnuda (forma canonica)                     0    si
    shell: bash + multilinea `echo before / runner / echo after`         0    si  (M2)
    runs-on: ubuntu-latest + multilinea SIN shell: (bash -e por defecto) 0    si
    runs-on: ${{ matrix.os }} + shell: bash + multilinea                 0    si
    multilinea donde las lineas extra son comentarios (queda 1 real)     0    si
    if: always()  /  if: success()  (paso)                               0    si
    continue-on-error: false literal                                     0    si

No implementaron "un comando por paso". Un bloque bash de tres comandos **si** se acepta. Ese lado
de tu pregunta esta bien resuelto, y lo verifique con bash real: `echo before / runner / echo after`
bajo `bash --noprofile --norc -eo pipefail` sale con **3** cuando el runner sale con 3.

### B.2 -- lo que la regla rechaza bien, comprobado

    vector de una linea o de forma que NO gatea                          exit  correcto
    runner || true                                                        1    si  (M5)
    runner ; exit 0                                                       1    si  (M6)
    echo runner                                                           1    si  (M10)
    runner --help                                                         1    si  (X)
    runner | cat        (pipe se traga el codigo)                         1    si
    multilinea en pwsh / shell por defecto en windows-latest              1    si  (M1)
    if: false / if: github.event_name == 'schedule' (paso)                1    si  (M3, M4)
    if: ${{ github.ref == 'refs/heads/main' }} (paso)                     1    si
    continue-on-error: ${{ true }} / 'true' / true / yes / on / 1 (paso)  1    si
    job needs: / job if: false / job continue-on-error: true              1    si
    on: solo workflow_dispatch                                            1    si  (M13)

Este lado es ancho y esta bien. No es la regla comoda.

### B.3 -- SLIP BLOQUEANTE: la excepcion de bloque bash acepta una familia que no gatea

La excepcion se concede mirando el modo DECLARADO del shell (`shell: bash`, o el shell por defecto
en `ubuntu-*`/`macos-*`) y contando **una** invocacion directa. Nunca mira si alguna OTRA linea del
bloque desactiva ese modo. El comentario del codigo lo dice explicito: *"A plain runner line
therefore propagates failure even inside a multiline block"* -- cierto solo mientras `-e` siga en pie.

Medido con bash real, invocacion exacta de GitHub (`bash --noprofile --norc -eo pipefail script`),
con un runner que sale con 3:

    bloque                                            exit del PASO   veredicto del gate
    runner                                                  3          acepta   correcto
    echo before / runner / echo after                       3          acepta   correcto  (M2)
    set +e / runner / echo after                            0          acepta   *** NO GATEA ***
    set +e / runner / exit 0                                0          acepta   *** NO GATEA ***
    trap 'exit 0' ERR / runner                              0          acepta   *** NO GATEA ***
    set +e -o pipefail / runner / true                      0          acepta   *** NO GATEA ***

Y de punta a punta, con el checker entregado sobre un fixture con la primera de esas formas:

    FALSIFICATION_EXECUTION_GUARANTEED runners=1/1 contracts=1/1
    FALSIFICATION_INVENTORY permanent_negatives=1 declared=1 missing=0
    CHECKER_EXIT=0

El gate certifica como GARANTIZADO un paso que sale verde con el runner en rojo. Es el defecto que
0336 existe para cerrar, movido de sitio: antes vivia en "el gate mira el comando", ahora vive en
"el gate mira el shell declarado y no lo que el bloque le hace".

Y el AC2 lo dice con estas palabras: la excepcion aplica *"salvo que el shell efectivo garantice el
aborto al primer fallo"*. Con `set +e` dentro, el shell efectivo **no** lo garantiza. La
implementacion comprueba el shell nominal, no el efectivo.

**Honestidad del muestreo:** probe tambien `runner & / wait $! || true / runner` esperando que
escapara y **no escapo** -- sale con 3, la aceptacion es correcta. No lo cargo como slip. La familia
que falla es concretamente la que desarma `errexit` (`set +e`, `set +o errexit`) o la que intercepta
el fallo (`trap ... ERR`).

## Foco C -- la certificacion afirmativa. NO CUMPLE el AC5.

Sobre el workflow canonico el gate imprime, con exit 0:

    FALSIFICATION_EXECUTION_GUARANTEED runners=8/8 contracts=48/48

El AC5 pide que **mientras existan escapes vivos** el gate no emita un recuento afirmativo de
ejecucion, o lo emita **acotado a lo que de verdad garantiza**, y que se declare que garantiza.
Hoy: hay escapes vivos (B.3 y el residual R1 de abajo), el recuento es afirmativo y sin acotar, el
nombre es `_GUARANTEED` -- mas fuerte que el `FALSIFICATION_EXECUTION` anterior, no mas debil -- y
**no hay ningun residual declarado** en el codigo, ni en el contrato, ni en la tarea, ni en el
handoff.

El handoff ademas afirma como propiedad garantizada: *"A multiline block counts only under GitHub's
failure-aborting bash mode"*. La primera mitad es cierta; lo que la frase omite es que el modo se
comprueba en la declaracion y no en el bloque, y que por eso la garantia es falsa bajo B.3.

Que la certificacion sea nominalmente mas fuerte mientras el escape sigue vivo es exactamente el
"verde con numero peor que un silencio" que la tarea nombra en su intake. Esto es lo que bloquea.

## Foco D -- sin regresion en el cableado. PASA.

- `git log -1 -- .github/workflows/validate.yml` -> **`f6d88cb7`** (TASK-0330). El commit de entrega
  de 0336, `68349d7f`, **no toca el fichero**. El `out_of_scope` se respeto por construccion, no por
  promesa.
- El job `falsification-runners` sigue intacto: `runs-on: windows-latest`, un paso por runner, tres
  invocaciones directas de una linea, `if: always()` en los dos ultimos.
- La regla endurecida **acepta la forma buena**: `condition_allows_execution` admite `always()` y
  `success()`, y la corrida canonica del gate da exit 0 con `runners=8/8 contracts=48/48`. No hay
  ironia: el gate duro no rechaza el cableado correcto.

## Residuales declarados (no bloqueantes por si solos; deben quedar escritos)

- **R1 -- filtros de `on:` sin mirar (factor (a) a nivel de disparador).** `workflow_steps` solo
  comprueba que las CLAVES `push` y `pull_request` existan. Un `on: push: paths: ['docs/**']` +
  `pull_request: paths: ['docs/**']` se acepta con exit 0, y ese workflow no corre ante un cambio de
  codigo. Verificado: exit 0. Lo mismo con `branches: [never-exists]`. Es la misma familia que
  `if: false`, un nivel mas arriba, y el intake nombra `on:` explicitamente dentro de (a). Lo dejo
  como residual y no como slip aparte porque se cierra igual acotando la certificacion (foco C);
  si se acota, deja de ser una afirmacion falsa.
- **R2 -- falso NEGATIVO: `defaults.run.shell: bash`.** Un job con `defaults: run: shell: bash` y un
  bloque multilinea **si** gatea, y el gate lo **rechaza** (exit 1): `shell_guarantees_abort` solo
  mira `step.shell` y `job.runs-on`. Falla cerrado, asi que no es peligroso, pero el AC3 pide la
  regla cierta por los dos lados y este es el otro lado. Merece cubrirse o declararse.
- **R3 -- `working-directory:` ignorado.** Un paso con `working-directory: examples` y
  `run: python examples/orphan/run_orphan.py` se certifica (exit 0) aunque la ruta relativa no
  resuelva. En CI el paso reventaria (fichero no encontrado) y el job iria a rojo, o sea **falla
  ruidoso**, no escape silencioso. Severidad baja; la certificacion nombra un runner que ese paso no
  ejecuta.
- **R4 -- divergencia YAML 1.1 vs GitHub en `continue-on-error`.** PyYAML resuelve `no`/`off` como
  booleano `False`, asi que `continue-on-error: no` se **acepta**. El fichero ya lleva un comentario
  reconociendo esta misma clase de divergencia para la clave `on:`. **No lo verifique contra el
  parser real de GitHub**; lo declaro como residual a comprobar, no como hallazgo.
- **R5 -- guarda inerte.** `"needs" in step`: los pasos de GitHub Actions no tienen clave `needs:`.
  Codigo defensivo muerto; ninguna frontera lo cubre ni puede cubrirlo con un workflow valido.

## Recomendacion de cierre

**CHANGE-REQUIRED (estrecho).** Iteracion 1 de un maximo de 2; a la tercera escalo al operador humano.

    AC1  falsacion previa reproducida            CUMPLE   (R15 reproduce el defecto y voltea 5 fronteras)
    AC2  los cuatro factores                     PARCIAL  ((a) sin filtros de on:; (c) excepcion insegura)
    AC3  regla cierta por los dos lados          NO CUMPLE (acepta la familia set +e / trap; rechaza defaults.run.shell)
    AC4  contrato falsable, trece mutantes       CUMPLE   con un hueco: falta frontera para continue-on-error de JOB
    AC5  certificacion honesta                   NO CUMPLE (afirmativa y sin acotar sobre escapes vivos, sin residual declarado)
    AC6  sin regresion, gates verdes             CUMPLE

### Remediacion pedida (minima, por propiedad -- no prescribo la forma)

1. **Cerrar la familia de B.3.** La excepcion de bloque multilinea debe concederse solo cuando la
   garantia de aborto **sobrevive al bloque entero**, no cuando el shell la declara. La propiedad a
   satisfacer es la del AC2: *shell efectivo*, no shell nominal.
2. **Dos fronteras nuevas que lo prueben**, con la forma medida arriba: un bloque `shell: bash` con
   `set +e` y otro con `trap ... ERR`, ambos `!= 0`. Sin ellas la correccion no es falsable.
3. **Una frontera para `continue-on-error` de JOB** (hoy `R6` no voltea nada).
4. **Acotar la certificacion (AC5).** O el recuento deja de ser afirmativo, o se acota a lo que el
   gate sostiene y se declaran los residuales en el repositorio. Si se acota, R1 queda cubierto por
   la propia acotacion; si no se acota, R1 pasa a ser slip.
5. **R2 (`defaults.run.shell`)**: cubrir o declarar. No bloqueo por el, pero no debe quedar mudo.

### Gates afectados por la remediacion

    python scripts/test_falsification_contracts.py                                  exit 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml --inventory                       exit 0
    python scripts/validate_collaboration_state.py --root .                         exit 0
    python scripts/scan_encoding.py --root .                                        exit 0
    python scripts/scan_domain_neutrality.py --root .                               exit 0
    python runtime/protocol_replay.py --check-drift --root .                        exit 0

Mas la no-regresion del foco D: el workflow canonico debe seguir aceptandose (`runners=8/8`), y
`.github/workflows/validate.yml` debe seguir sin tocarse.

### Re-juicio antes del commit de cierre

Vuelvo a correr, en clon limpio sobre el commit de remediacion: la matriz de falsabilidad por
frontera completa (para que las fronteras nuevas no sean vacuas y las trece viejas sigan portantes),
las seis formas de B.3 contra bash real, y el lado de aceptacion de B.1 entero (para que el
endurecimiento no se coma la forma buena). Sin ese re-juicio no hay OK-CLOSABLE.

## Nota de disciplina heredada

Mientras B.3 y R1 sigan vivos, `FALSIFICATION_EXECUTION_GUARANTEED runners=8/8 contracts=48/48`
**no se cita como prueba de ejecucion** en ningun handoff ni reporte. Es la misma condicion dura que
la tarea hereda de 0330 y del "47", trasladada de los nueve escapes viejos -- que estan muertos, lo
verifique -- a los que quedan vivos.

-- Analista
