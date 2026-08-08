# Veredicto TASK-0336 re-juicio remediacion 2 -- CHANGE-REQUIRED + ESCALADA: la familia C.1 no esta cerrada, esta cerrada POR UNA CARA. El gate decide "esto es un comentario" por linea FISICA; bash lo decide por linea LOGICA, despues de empalmar. Hay noveno.

Analista, 2026-08-08 09:07 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Tu pregunta era la misma de la vuelta anterior: *queda algun escape vivo, o la
certificacion afirmativa ya se sostiene tal como se emite?* **Queda uno, y es de la MISMA familia
C.1.** No es un descuido del maker sobre lo que le pedi: cerro exactamente las cuatro puertas que le
declare, y las cerro de verdad. Es que la premisa sobre la que se cerro es falsa, y la premisa la
escribi yo en r2 tanto como el en el handoff:

    "Las lineas de comentario no activan esta regla, igual que en bash."

En bash una linea que empieza por `#` **no siempre es un comentario**. Solo lo es si el `#` abre
palabra. Si la linea anterior termina en `\` **pegada al ultimo caracter** (sin espacio), bash
empalma las dos y el `#` queda soldado a la palabra de arriba: deja de abrir comentario, la linea
sigue siendo codigo, y su propio `\` final **sigue continuando**. El gate, que clasifica comentarios
mirando cada linea fisica por separado, corta ahi la cadena y da por invocado un runner que bash se
acaba de tragar.

Medido con bash real, xtrace incluido:

    bloque (shell: bash)          echo x\ / #foo \ / python runner
    bash ejecuta                  echo x#foo python examples/cases/run_cases.py
    runner ejecutado              NO
    exit del paso                 0
    veredicto del gate            exit 0, scope=...direct_invocation...

Es literalmente el mutante `echoed` que el contrato declara muerto, repartido en tres lineas y con
un `#` de por medio. Tercera vez que la misma propiedad reaparece en otra gramatica; y por segunda
vez consecutiva **el que fallo primero fue mi muestreo**, no el del maker. Lo digo con todas las
letras porque el AC1 existe para eso.

## Anclaje

- Juicio anclado en **`1522f08d`** (`origin/main` al abrir la revision).
- Commit de implementacion citado por el handoff: **`e21e617a`**.
  `git diff --stat e21e617a origin/main -- scripts/check_falsification_contracts.py
  scripts/test_falsification_contracts.py Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  .github/workflows/validate.yml` -> **vacio**. Las rutas de alcance son identicas byte a byte entre
  la entrega y la punta canonica. El juicio vale para las dos.
- `e21e617a` toca exactamente tres ficheros: los dos scripts de alcance y el fichero de la tarea.
- Clon limpio en `D:/Aegis_Scratch/mapp/r336c/cc`, **detached en `1522f08d`**, `git status --short`
  vacio, `__pycache__` purgado antes de medir.
- Sondas reproducibles (mias, fuera del arbol atestado, en `D:/Aegis_Scratch/mapp/r336c/mut/`):
  `probe_r3a.py` (familia C.1 + 12 formas nuevas de continuacion), `probe_r3b.py` (semantica de bash
  con xtrace + las cuatro puertas + certificacion emitida), `probe_r3c.py` (AC3 por los dos lados,
  22 formas), `matrix_r3.py` (matriz de falsabilidad de las 25 fronteras, 25 relajaciones dirigidas),
  `probe_r3d.py` (acotacion de la familia: que caracter pegado hace que bash ignore el `#`).
- Bash real: `C:/Program Files/Git/usr/bin/bash.exe`, invocado como GitHub lo hace
  (`bash --noprofile --norc -eo pipefail <script>`). El `bash` del PATH en esta maquina es el de
  WSL y mide ruido; el binario va fijado en todas las sondas.

## Gates recomputados por exit code en clon limpio sobre `1522f08d`

    python scripts/test_falsification_contracts.py                                     EXIT 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml --inventory                          EXIT 0
    python scripts/validate_collaboration_state.py --root .                            EXIT 0
    python scripts/scan_encoding.py --root .                                           EXIT 0
    python scripts/scan_domain_neutrality.py --root .                                  EXIT 0
    python runtime/protocol_replay.py --check-drift --root .   EXIT 0  verdict=CLEAN up_to_seq=7883

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=56/56
      scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure
      residuals=trigger_filters,working_directory,yaml_1_1_scalars
    DECLARED NEG-FALSIFICATION-RUNNER-WIRING boundaries=25

**Drift 0. Los seis gates estan verdes.** Mi objecion no es un gate rojo: es un escape por
comportamiento que los seis gates verdes no ven, otra vez.

### Nota sobre el commit exacto de la entrega (no es un slip de 0336)

Sobre **`e21e617a`** el clon limpio da `validate_collaboration_state.py` **EXIT 1**
(`gap at seq 7854: expected 6826`): a ese commit le falta
`runtime/state/archives/events-006826-007853.jsonl`. Lo verifique tambien en `e21e617a~3`, donde
falla igual: es **preexistente y ajeno a 0336**. Y ya esta resuelto en la punta: el commit
`06e83983` metio los archives al arbol, y por eso `1522f08d` da EXIT 0 en clon limpio. Es decir, la
QUESTION abierta `MSG-20260808-Codex-to-Arquitecto-QUESTION-clean-clone-event-archive` **describe un
bloqueo que ya no existe**; lo senalo por DECISION-0018 para que no se abra tarea por algo cerrado.

## Foco A -- AC3 por los DOS lados. PASA, sin desajustes.

Las 22 formas de r2, recorridas enteras contra el checker entregado. El endurecimiento **no se comio
ninguna forma buena**:

    lado ACEPTACION (la forma SI gatea)          exit   lado RECHAZO (la forma NO gatea)       exit
    A01 linea unica ubuntu                        0     R01 multilinea pwsh por defecto         1
    A02 linea unica windows                       0     R02 shell: pwsh explicito               1
    A03 multilinea shell: bash                    0     R03 JOB pwsh sobre WORKFLOW bash        1
    A04 multilinea ubuntu implicito               0     R04 set +e dentro del bloque            1
    A05 multilinea macos-14 implicito             0     R05 trap 'exit 0' ERR                   1
    A06 JOB defaults.run.shell bash               0     R06 continue-on-error: true de JOB      1
    A07 WORKFLOW defaults.run.shell bash          0     R07 if: false de JOB                    1
    A08 if: always() de paso                      0     R08 needs: de JOB                       1
    A09 continue-on-error: false literal          0     R09 on: solo workflow_dispatch          1
    A10 extras solo comentarios                   0     R10 runner || true                      1
                                                        R11 echo runner                         1
                                                        R12 if: false de paso                   1

    desajustes: 0

Y la cara de aceptacion de la remediacion tambien aguanta, medida contra bash real:

    forma                                          checker  bash  runner corrio
    comentario terminado en `\` + runner              0       3    SI    correcto
    runner + `echo tail \` de cierre                  0       3    SI    correcto
    `echo before \ ` (barra + ESPACIO)                0       3    SI    correcto
    dos barras (par) + runner                         0       3    SI    correcto
    linea en blanco entre continuacion y runner       0       3    SI    correcto
    control echo/runner/echo                          0       3    SI    correcto

**No implementaron "un comando por paso"** y siguen sin implementarlo: el bloque bash de tres
comandos se acepta y gatea. Ese lado de tu pregunta sigue resuelto.

## Foco B -- AC4: las VEINTICINCO fronteras, portantes. PASA, cero vacuas.

Mismo metodo que en r1 y r2 y por la misma razon: **25 relajaciones dirigidas** del checker
entregado, cada una evaluada contra los 27 fixtures **por separado**, nunca a traves de la cadena
ordenada de `assert`, para que ninguna frontera se esconda detras de un fallo anterior.

    frontera                                estado     volteada por
    multiline_pwsh                          PORTANTE   L13, L15
    multiline_bash                          PORTANTE   L14                (lado ACEPTACION)
    multiline_set_plus_e                    PORTANTE   L15, L16
    multiline_trap_err                      PORTANTE   L15, L16
    job_defaults_bash                       PORTANTE   L14, L17, L19      (lado ACEPTACION)
    workflow_defaults_bash                  PORTANTE   L14, L17, L18      (lado ACEPTACION)
    multiline_continuation_step_bash        PORTANTE   L15, L21, L22      NUEVA
    multiline_continuation_ubuntu           PORTANTE   L15, L21, L22      NUEVA
    multiline_continuation_job_bash         PORTANTE   L15, L21, L22      NUEVA
    multiline_continuation_workflow_bash    PORTANTE   L15, L21, L22      NUEVA
    multiline_comment_backslash             PORTANTE   L14, L23           NUEVA (lado ACEPTACION)
    step_if_false                           PORTANTE   L4
    step_if_event                           PORTANTE   L4, L5
    bash_or_true                            PORTANTE   L10, L11, L15
    semicolon_exit                          PORTANTE   L10, L11, L12, L15
    continued_expression                    PORTANTE   L7, L8
    continued_string                        PORTANTE   L7, L8
    continued_literal                       PORTANTE   L7, L9
    job_continue_on_error                   PORTANTE   L6, L9
    echoed                                  PORTANTE   L11, L15
    job_needs                               PORTANTE   L2
    job_if_false                            PORTANTE   L3
    dispatch_only                           PORTANTE   L1
    no_EXECUTION_GUARANTEED                 PORTANTE   L20a               (frontera de texto)
    residuals_declared                      PORTANTE   L20b               (frontera de texto)

    fronteras nunca volteadas: 0

Las cinco nuevas son separables y no se solapan: `L21` (borrar el rechazo por continuacion) y `L22`
(`bash_line_continues` siempre falso) voltean las cuatro de rechazo y **no** tocan la de aceptacion;
`L23` (quitar la guarda del `#`) voltea **solo** `multiline_comment_backslash`. Anadir cinco
fronteras no escondio ninguna de las veinte anteriores: las veinte siguen con los mismos
discriminadores que tenian en r2. Eso era lo que me pediste comprobar en tu foco B, y aguanta.

### B.1 -- dos propiedades REALES sin frontera que las ate (no bloqueante por si solo)

La matriz destapa algo que conviene decir, porque es justo lo que elogiaste en tu lectura del gate:

    relajacion                                        voltea alguna frontera DECLARADA?
    L24  paridad -> cualquier barra final (`>= 1`)     NO   (solo mi centinela no declarado)
    L25  continuacion mirando la linea ya rstrip-eada  NO   (solo mi centinela no declarado)

La **paridad** (`% 2 == 1`, que evita el falso positivo sobre `\\` escapada) y la regla de que **una
barra seguida de espacio no continua** son comportamiento vivo y correcto, pero **ningun assert
declarado se rompe si un maker futuro los sustituye por un `endswith("\\")` ingenuo**. Son
exactamente el patron "declarado en la prosa, no atado por el contrato". No lo cargo como bloqueo
-- ninguna de las dos abre un escape, las dos fallan hacia el lado seguro --, pero si hay una
tercera vuelta, ahi caben dos fronteras de aceptacion baratas.

## Foco C -- AC5: la certificacion. NO CUMPLE. El escape cae DENTRO de `direct_invocation`.

### C.1bis -- SLIP BLOQUEANTE: el `#` que bash no lee como comentario

`bash_line_continues()` devuelve `False` para toda linea cuyo `lstrip()` empieza por `#`, y el
filtro de `indexed_lines` descarta esas lineas antes de mirar nada. Las dos decisiones se toman
**por linea fisica**. Bash decide despues de empalmar: si la linea anterior termina en `\` **pegado
a un caracter de palabra**, el `#` no abre comentario, la linea es codigo, y su `\` final continua.

Medido de punta a punta (bash real + checker entregado), runner que imprime `RUNNER-EXECUTED` y sale
con 3:

    bloque (shell bash)                       exit del PASO  runner ejecutado  veredicto del gate
    echo x\ / #foo \ / runner                       0             NO           acepta  *** ESCAPE ***
    echo 1\ / #foo \ / runner                       0             NO           acepta  *** ESCAPE ***
    python -c exit\ / #foo \ / runner               0             NO           acepta  *** ESCAPE ***
    echo x\ / #a\ / #b \ / runner                   0             NO           acepta  *** ESCAPE ***
    echo x\ / #f \ / runner / echo done             0             NO           acepta  *** ESCAPE ***
    idem con CRLF en el fichero                     0             NO           acepta  *** ESCAPE ***

    control 1: echo x \ / # foo \ / runner          3             SI           acepta  correcto
    control 2: echo x\ / TAB#foo \ / runner         3             SI           acepta  correcto
    control 3: echo x\ / #a / #b \ / runner         3             SI           acepta  correcto

El discriminador exacto es el **espacio antes del `#`**: con espacio (o tabulador) delante, bash si
abre comentario y el runner corre, y el gate acierta al aceptar. Sin espacio, no. Traza de bash del
caso base:

    + echo x#foo python examples/cases/run_cases.py

Una sola orden. El runner nunca se invoca. El paso sale 0 aunque el runner estuviera roto.

El escape entra por **las cuatro** puertas de shell efectivo, las mismas cuatro que la remediacion 2
declara cerradas:

    puerta                                        checker exit
    shell: bash en el paso (windows-latest)             0
    ubuntu-latest con shell implicito                   0
    JOB defaults.run.shell: bash                        0
    WORKFLOW defaults.run.shell: bash                   0

Y la certificacion que el gate emite sobre ese fixture, de punta a punta:

    FALSIFICATION_STATIC_WIRING runners=1/1 contracts=1/1
      scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure
      residuals=trigger_filters,working_directory,yaml_1_1_scalars
    FALSIFICATION_INVENTORY permanent_negatives=1 declared=1 missing=0
    CHECKER_EXIT=0

El escape **no cae en ninguno de los tres residuales declarados**: cae en `direct_invocation`, que la
linea afirma. Por eso AC5 sigue sin cumplirse, y por eso la cifra acotada tampoco se sostiene.

### C.2 -- de quien es el fallo, y por que no es un quinto parche a ciegas

La causa raiz no es "faltaba una forma". Es **una diferencia de nivel de analisis**: el gate razona
sobre lineas fisicas y bash sobre lineas logicas. Mientras esa diferencia exista, cada parche cierra
las formas enumeradas y deja abiertas las que nadie enumero -- que es exactamente lo que ha pasado
dos veces seguidas en esta misma familia. La propiedad que hay que atar es **una sola y es
estructural**: clasificar comentarios, lineas ejecutables e invocaciones **despues** de empalmar las
continuaciones, no antes. Con la linea logica en la mano, `echo x#foo python .../run.py` deja de
casar la invocacion por si sola y el bloque se rechaza sin necesidad de enumerar nada.

La segunda via, si no se quiere tocar el analisis, es la que el propio AC5 autoriza: **no afirmar
`direct_invocation` sin acotarlo**, y declarar el empalme de bash como residual con frontera propia.
Es menos gate y mas honestidad, pero cumple el criterio tal como esta escrito.

No prescribo cual. Prescribir la forma es lo que nos ha traido hasta aqui.

## Foco D -- sin regresion. PASA.

- `git log -1 -- .github/workflows/validate.yml` -> **`f6d88cb7`** (TASK-0330). Intacto: el
  `out_of_scope` se respeto por construccion.
- El job `falsification-runners` sigue con **un paso por runner** e `if: always()` en los dos
  siguientes al primero. La regla endurecida lo acepta sin cambios.
- Corrida canonica en clon limpio: exit 0 con `runners=8/8 contracts=56/56`. El gate duro no rechaza
  el cableado correcto.
- La cifra subio de 53 a 56 contratos por trabajo ajeno a 0336 (rutas de alcance identicas entre
  `e21e617a` y la punta); no es un efecto de esta remediacion.

## Residuales declarados

- **RD1 -- filtros de `on:`**. Declarado por el gate, con frontera. No bloqueante.
- **RD2 -- `working-directory:`**. Declarado. Falla ruidoso en CI, no escape silencioso.
- **RD3 -- escalares YAML 1.1**. Declarado. Sigue sin comprobarse contra el parser real de GitHub.
- **RD4 -- guarda inerte `"needs" in step`**. Codigo defensivo muerto, reconocido.
- **RD5 -- `needs:` de job rechazado de plano**. Falla cerrado.
- **RD6 -- falsos negativos de la excepcion multilinea (NUEVO, severidad baja).** Medidos: un bloque
  cuya linea de invocacion termina en `\` (`runner \` + `echo after`), o que contiene `;` o `|` en
  una linea de `echo`, se **rechaza** aunque bajo bash real el runner si corre (exit 3). Falla
  CERRADO y es preexistente a esta remediacion; lo anoto para que no sorprenda a quien anada un
  bloque legitimo manana.
- **RD7 -- paridad y barra-mas-espacio sin frontera (NUEVO, foco B.1).** Comportamiento correcto y
  vivo, no atado por ningun assert declarado.

## Recomendacion de cierre

**CHANGE-REQUIRED + ESCALADA AL OPERADOR HUMANO.**

    AC1  falsacion previa reproducida         CUMPLE    (L15 reproduce el defecto 0330 y voltea 11 fronteras)
    AC2  los cuatro factores                  PARCIAL   ((c) sigue con la familia de empalme viva)
    AC3  regla cierta por los dos lados       PARCIAL   (22/22 formas correctas; falla solo en C.1bis)
    AC4  contrato falsable, fronteras         CUMPLE    (25/25 portantes, cero vacuas; ver B.1)
    AC5  certificacion honesta                NO CUMPLE (el escape cae DENTRO de direct_invocation)
    AC6  sin regresion, gates verdes          CUMPLE

**Por que escalo y no pido un tercer parche por mi cuenta.** En r2 declare el limite yo mismo:
*"iteracion 2 de un maximo de 2; si hace falta una tercera, escalo al operador humano"*. Esta es la
segunda remediacion juzgada de TASK-0336, el limite esta agotado, y **el proximo movimiento no es
mio**. Lo que tengo que entregar es el hallazgo medido y las opciones; la eleccion entre gastar una
tercera iteracion de codigo o cerrar por la via de acotar la certificacion es una decision de
alcance, y esa es del Arquitecto con el operador, no del checker.

### Si se autoriza una tercera iteracion, la propiedad a atar (una sola, no una lista de formas)

1. **Clasificar despues de empalmar.** Comentario, linea ejecutable e invocacion se deciden sobre la
   **linea logica** resultante de unir las continuaciones, no sobre la fisica. Cuidado con no romper
   la cara de aceptacion ya verificada: comentario terminado en `\` **con** espacio delante, barra
   seguida de espacio, numero par de barras, linea en blanco intermedia, y el bloque bueno
   `echo / runner / echo`.
2. **Fronteras que lo prueben**, con las formas medidas arriba: `echo x\` + `#foo \` + runner por las
   cuatro puertas de bash efectivo (`!= 0`), y las tres de control (`== 0`): espacio antes del `#`,
   tabulador antes del `#`, y linea de comentario sin barra final. Sin ellas la correccion no es
   falsable.
3. **Opcional, barato, y recomendado si se abre el fichero:** las dos fronteras de aceptacion de
   B.1 -- numero par de barras y barra-mas-espacio -- para que la paridad deje de ser prosa.

### Si se opta por acotar en vez de parchear

Sacar `direct_invocation` de la afirmacion o acotarlo explicitamente, y declarar el empalme de
continuaciones de bash como cuarto residual con su frontera de texto propia (la frontera
`residuals_declared` ya es portante, asi que el patron esta probado). Con eso AC5 se cumple tal como
esta escrito, y la familia queda **declarada** en vez de **certificada como cerrada**, que es la
diferencia que esta tarea existe para defender.

### Gates afectados por cualquiera de las dos vias

    python scripts/test_falsification_contracts.py                                  exit 0
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml --inventory                       exit 0
    python scripts/validate_collaboration_state.py --root .                         exit 0
    python scripts/scan_encoding.py --root .                                        exit 0
    python scripts/scan_domain_neutrality.py --root .                               exit 0
    python runtime/protocol_replay.py --check-drift --root .                        exit 0

Mas la no-regresion del foco D: la corrida canonica debe seguir dando `runners=8/8` y
`.github/workflows/validate.yml` debe seguir sin tocarse.

### Re-juicio antes del commit de cierre

Si el operador autoriza una tercera vuelta, vuelvo a correr en clon limpio sobre el commit de
remediacion: la matriz de falsabilidad completa (las 25 mas las nuevas, para que ninguna quede
vacua), las 22 formas del foco A enteras, la familia C.1 entera, y las nueve formas de C.1bis con
sus tres controles, todo contra bash real con el binario de Git fijado. Sin ese re-juicio no hay
OK-CLOSABLE.

## Nota de disciplina heredada

Mientras la familia siga viva, la linea `FALSIFICATION_STATIC_WIRING runners=8/8 contracts=56/56`
**no se cita como prueba de ejecucion** en ningun handoff ni reporte. Es la condicion dura que la
tarea hereda de 0330 y del "47".

Y una cosa sobre tu nota. Dijiste que si esto cierra, cierra la cadena de ocho niveles, y me pediste
que no lo cerrara con prisa por eso. **Habia noveno.** No lo destapo una sospecha: lo destapo dejar
de creerme mi propia tabla de r2 y volver a preguntarle a bash, que es la unica autoridad sobre lo
que bash hace. Si hay decimo, saldra igual: midiendo, no razonando.

-- Analista
