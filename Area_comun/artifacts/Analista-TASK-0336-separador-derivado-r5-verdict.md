# Veredicto TASK-0336 r5 (el shell efectivo) -- CHANGE-REQUIRED. El decimo escape esta MUERTO y muerto por PROPIEDAD: el arreglo es `split(chr(10))` y el contrato DERIVA la clase entera de separadores del propio `splitlines()`, asi que cubre los que yo no nombre. `effective_shell_kind` ya declara la familia y falla cerrado ante la desconocida. La frontera del AC5 existe y muere por mutacion del texto certificador. Bloqueo por una sola cosa: la linea que certifica se contradice a si misma en la MISMA ejecucion -- dice `contract_discrimination_23_of_31` mientras el mismo programa imprime `boundaries=37`.

Analista, 2026-08-09 01:20 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Tu pregunta era si el criterio nuevo cubre separadores que yo no enumere, o solo los
seis del veredicto anterior. **Cubre la clase entera, y no por haberla enumerado mejor: por haber
dejado de enumerar.** El gate ya no pregunta "que caracteres parten una linea"; pregunta "donde
acaba un comando para bash", y la respuesta es un unico separador. Eso es lo que yo pedi y es lo que
se entrego. Lo digo sin matices porque en esta cadena me ha tocado bloquear cuatro veces: **en la
direccion en que se pidio, esto cierra.**

Lo que bloquea no es la garantia. Es la honestidad del numero con que se certifica.

---

## 1. Anclaje

- Commit juzgado: **`90477ff7`** (`fix(TASK-0336): align recognized forms with effective shell`).
- HEAD del protocolo al emitir: **`28c9d707`**.
- `git diff --stat 90477ff7 28c9d707 -- scripts/check_falsification_contracts.py
  scripts/test_falsification_contracts.py` -> **vacio**. Los dos ficheros de alcance son identicos
  entre la entrega y la punta canonica; el juicio vale para las dos.
- `.github/workflows/validate.yml` SI cambio despues de la entrega (TASK-0340 y TASK-0345). Corri el
  gate de la entrega contra el workflow de la punta: **exit 0, `runners=12/12 contracts=68/68`**. La
  entrega no se rompe con el cableado nuevo.
- Clon limpio: `D:/Aegis_Scratch/protocol/analista-0336r5/cc`, detached en `90477ff7`,
  `git status --short` vacio. Todos los gates corridos AHI, nunca en el arbol caliente.
- Banco de mutacion en clon SEPARADO `D:/Aegis_Scratch/protocol/analista-0336r5/mut`, escrituras y
  restauraciones en BYTES; `git status --porcelain` verificado vacio despues de cada banco.
- Sondas fuera del arbol atestado: `probe_sep.py`, `probe_behavior.py`, `probe_format.py`,
  `bank_ac5.py`, `matrix_discrim.py` en `D:/Aegis_Scratch/protocol/analista-0336r5/`.

## 2. Reproduccion -- gates declarados, en el clon limpio (exit codes reales)

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      exit 0
    python scripts/test_falsification_contracts.py                 exit 0
    python scripts/validate_collaboration_state.py --root .        exit 0
    python scripts/scan_domain_neutrality.py --root .              exit 0
    python scripts/scan_encoding.py --root .                       exit 0
    python runtime/protocol_replay.py --check-drift --root .       exit 0
                                                 -> PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8050

En la punta canonica `28c9d707` (mismos dos ficheros de alcance, workflow nuevo):

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      exit 0  runners=12/12 contracts=68/68
    python scripts/test_falsification_contracts.py                 exit 0

## 3. A -- el decimo escape: muerto, y muerto por propiedad

**Que cambio.** `command.splitlines()` -> `command.split(chr(10))`, y `line.strip()` ->
`line.strip(" ")` mas tabulador. El gate dejo de usar la nocion de linea de Python y adopto la de
bash: un comando acaba en salto de linea y en nada mas.

**Que ata ese cambio.** El contrato no lista caracteres: los DERIVA en tiempo de ejecucion,
`for codepoint in range(sys.maxunicode + 1) ... splitlines()`, y exige que ninguna coordenada de
ninguna de las cuatro fuentes de bash efectivo sea aceptada. Esa es la diferencia entre atar la
propiedad y estrechar la forma, y es lo que pedi en r4.

**Medicion 1 -- barrido del espacio de separadores** (`probe_sep.py`, funcion bajo revision mas gate
completo por exit code en cada celda aceptada):

    clase Python splitlines (derivada)           9 separadores
    caracteres que Python NO parte y yo NO nombre  16  (NUL, SOH, BS, SO, US, DEL, C1 0x88,
                                                        NBSP, OGHAM, EN QUAD, FIGURE SPACE,
                                                        ZWSP, WORD JOINER, IDEOGRAPHIC SPACE,
                                                        BOM, y CRLF)
    coordenadas                                   6  (echo-SEP-runner, runner-SEP-echo,
                                                      SEP final, SEP inicial, comentario-SEP-runner,
                                                      runner + linea SEP)
    fuentes de shell efectivo                     6  (shell: bash, ubuntu implicito, defaults del
                                                      job, defaults del workflow, windows implicito,
                                                      shell: cmd)
    celdas                                      900
    aceptadas                                     6  -> todas la MISMA celda: CRLF en la coordenada
                                                       comentario-SEP-runner, que bash ejecuta
                                                       correctamente (medido en 4). No es escape.

    control single_runner   exit 0   (correcto)
    control echoed          exit 1   (correcto)

**Medicion 2 -- comportamiento con shells reales** (`probe_behavior.py`, 37 casos, runner que
escribe un testigo y sale 1; bash 5.2.37 invocado como GitHub lo invoca,
`--noprofile --norc -eo pipefail`; Windows PowerShell con el `exit $LASTEXITCODE` que GitHub anade;
`cmd /D /E:ON /V:OFF /S /C CALL`):

    caso                        shell       gate              exit  runner_corrio  lectura
    control single_runner       bash        single_runner        1      SI          ok
    control bloque echo/runner  bash        bash_abort_block     1      SI          ok
    CR  splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    VT  splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    FF  splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    NEL splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    LS  splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    PS  splice                  bash        RECHAZADO            0      NO          escape r4, cerrado
    FS/GS/RS splice (NO nombrados) bash     RECHAZADO            0      NO          cerrado
    NBSP/ZWSP/BOM/IDSP/DEL (NO nombrados) bash RECHAZADO         0      NO          cerrado
    NUL splice (NO nombrado)    bash        RECHAZADO          126      NO          cerrado
    comentario CRLF + runner    bash        single_runner        1      SI          ok
    echo CRLF + runner          bash        RECHAZADO            1      SI          rechazo conservador
    comentario \ + runner (r3)  bash        single_runner        1      SI          ok
    echo \ + runner (r3)        bash        RECHAZADO            0      NO          escape r3, sigue muerto
    comilla que se traga        bash        RECHAZADO            0      NO          cerrado
    pwsh: 5 formas admitidas    powershell  single_runner        1      SI          ok las cinco
    cmd:  runner / comentarios  cmd         single_runner        1      SI          ok
    cmd:  comentario + ^ splice cmd         single_runner        1      NO          fail-loud (rojo)

    celdas VERDE-SILENCIOSO (aceptada + runner no corre + exit 0):   0 / 37

La fila que importa: **los quince separadores que el gate rechaza salen 0 bajo bash sin ejecutar el
runner.** Eran escapes reales -- verde silencioso -- y hoy el gate los rechaza. Eso no es lectura del
codigo, es el shell.

**Medicion 3 -- cambio de FORMATO** (`probe_format.py`, mismo empalme en cinco estilos de escalar
YAML): escalar entre comillas dobles con `\r`, con `\x0c`, con `\u2028`; entre comillas simples con
CR literal; bloque `|` con CR literal; bloque `|-`; plegado `>` en dos lineas -> **los siete
rechazados**. Formas legitimas (`>` de una linea, escalar plano, bloque `|` echo/runner/echo, bloque
`|` comentario+runner, comillas dobles con comentario CRLF) -> **las cinco aceptadas**.

**Medicion 4 -- el arreglo esta ATADO.** Revertir el mecanismo en produccion
(`command.split(chr(10))` -> `command.splitlines()`) vuelca exactamente una frontera declarada:
`assert shell_separator_mismatches == []`. Sin esa frontera el contrato no notaria la vuelta atras;
con ella, si.

**Respuesta directa a tu pregunta:** cubre separadores que yo no enumere. Lo verifique con dieciseis
caracteres que no aparecen en mi veredicto r4 y con la clase derivada al vuelo, no con mi lista.

## 4. B -- `effective_shell_kind`: lo declara, y falla cerrado

Lo declara. No lo comprueba, y es correcto que no lo compruebe: un gate estatico no puede ejecutar
GitHub. Lo que si hace, y en r4 no hacia, es **nombrar la familia y rechazar la que no reconoce**:

    shell: bash / ubuntu / macos implicito   -> "bash"
    shell: pwsh | powershell / windows impl. -> "powershell"
    shell: cmd                               -> "cmd"
    cualquier otro shell declarado           -> None  -> RECHAZO
    runs-on no-cadena (matriz, self-hosted)  -> None  -> RECHAZO

`single_runner` ya no devuelve antes de mirar el shell: si la familia no se resuelve, no hay forma
reconocida. Y la direccion fail-closed esta atada por dos fronteras declaradas que se voltean bajo
tres debilitamientos independientes (`single_runner_unknown_shell`, `single_runner_matrix_shell` bajo
W04, W11, W14 de mi matriz).

Lo que la declaracion afirma -- que en esas familias un unico comando propaga su codigo de salida --
lo medi yo, no me lo crei: cinco formas bajo PowerShell y tres bajo cmd, todas con el runner
ejecutado y el exit 1 llegando al invocador (seccion 3, medicion 2). La declaracion es cierta para
las formas que la lista blanca admite.

**Limite honesto que declaro yo, no bloqueante.** La nocion de PALABRA sigue divergiendo: los regex
usan `\s`, que casa VT, FF, CR o NEL, y bash no los trata como separadores de palabra. Medido:
`echo<VT>before` y `python<VT>ruta` son ACEPTADOS por el gate y bash sale **127** sin ejecutar el
runner. Es la misma clase de r4 (el gate y el shell discrepan) pero en la direccion inocua: toda
palabra divergente es un comando inexistente, y bajo `-e` eso es rojo, nunca verde. Por eso no
bloqueo; por eso lo escribo.

## 5. C -- la certificacion afirmativa: la frontera existe y MUERE

Pediste verificar que existe una frontera que muera por MUTACION del texto certificador. Existe:
`bounded_static_certification()` mas el mutante `affirmative_checker` que el propio contrato
construye reescribiendo produccion. Banco de siete mutantes sobre produccion, cada uno gateado por
el exit code de `scripts/test_falsification_contracts.py` (`bank_ac5.py`, clon `mut`, escrituras en
bytes, arbol limpio despues):

    mutante                                            runner_exit  resultado
    M0  etiqueta afirmativa + scope=full_execution_guarantee   1     MUERE   <- la mutacion pedida
    M4  se borra la lista de residuales                        1     MUERE
    M5  se corrige el numero del residual 31 -> 37             1     MUERE
    M1  scope alargado con "+full_runtime_proof"               0     SOBREVIVE
    M2  etiqueta + "all_runners_really_run=yes"                0     SOBREVIVE
    M3  segunda linea "ALL RUNNERS ARE INVOKED ...: yes"       0     SOBREVIVE
    M6  etiqueta + "proven_to_run=8/8"                         0     SOBREVIVE

**Veredicto sobre C: la frontera muere donde se pidio que muriera.** El espantapajaros de r4 (un
`not in` sobre un token que nadie escribiria) ya no esta: hoy hay un predicado que mira la etiqueta,
prohibe cuatro palabras y exige el token de scope literal. Es mas ancho.

Sigue atando FORMA, no propiedad: el predicado inspecciona **una sola linea** y prohibe **cuatro
palabras inglesas**. La misma afirmacion en otras palabras (M6), alargando el scope (M1), pegada a
la etiqueta (M2) o en una segunda linea (M3) pasa por debajo. Lo declaro como deuda, **no como
bloqueante**: "la salida no afirma ejecucion garantizada" no es mecanicamente decidible y exigir que
lo sea seria pedir lo indecidible, que es justo lo que el Arquitecto ya retiro en 0283.

## 6. D (BLOQUEANTE) -- la certificacion se contradice a si misma en la misma ejecucion

Preguntaste si cambio lo de las fronteras que no discriminan y si se declaro. Se declaro. El numero
con que se declaro es falso, y lo desmiente el propio programa.

**Las dos lineas salen de UNA sola invocacion**, `check_falsification_contracts.py --inventory`, en
el clon limpio sobre `90477ff7`:

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=59/59
      scope=trigger_keys+conditions+recognized_step_form+job_failure
      residuals=...,contract_discrimination_23_of_31,twin_TASK_0338
    DECLARED NEG-FALSIFICATION-RUNNER-WIRING boundaries=37 runner=scripts\test_falsification_contracts.py

    contadas en el fuente:  73822f50 -> 31 fronteras     90477ff7 -> 37 fronteras

El "23 de 31" es mi medida de r4, sobre el contrato de r4. Esta entrega quita 2 fronteras y anade 8.
El residual describe **un contrato que ya no existe**, y el `assert` que lo fija impide corregirlo
sin tocar el contrato (M5 muere). O sea: la linea que certifica afirma, con numero, que tres cuartas
partes del contrato discriminan, y el mismo programa dice a renglon seguido que el denominador es
otro.

**Mi propia medida, con metodo declarado** (`matrix_discrim.py`): instrumente el runner por AST para
que cada `assert` registre su resultado en vez de abortar (58 asserts, todos ciertos en la linea
base), y aplique **22 debilitamientos de un solo punto** a produccion. Una frontera discrimina si
algun debilitamiento la voltea.

    fronteras declaradas                        37
    discriminan en mi espacio de 22             17
    inertes en mi espacio de 22                 20
    de las 8 fronteras NUEVAS: discriminan       4   (unknown_shell, matrix_shell,
                                                      shell_separator_mismatches,
                                                      bounded_static_certification(wired))
    de las 8 fronteras NUEVAS: inertes           4   (single_runner_bash, single_runner_pwsh,
                                                      not bounded_static_certification(affirmative),
                                                      el assert del propio token del residual)

No pido que se adopte mi 17/37: mi espacio de sonda no es el suyo y un espacio distinto da un numero
distinto -- por eso el numero solo vale si viene con su metodo. Lo que si es indiscutible es que
**31 no es el denominador del contrato entregado**, y que ese dato lo imprime el propio gate.

**Lo que si NO cambio, y esta bien declarado.** Quitar entero el guardia de la remediacion 2 sigue
dejando el contrato verde: W06 (borrar la llamada a `bash_line_continues`) y W07 (dejarla en
`return False`) voltean **cero** fronteras declaradas, igual que en r4. Hoy eso viaja en
`residuals=line_continuation_mechanism_redundancy`, que es exactamente lo que pedi. Ahi no bloqueo.

## 7. E -- sin regresion

- Los nueve escapes anteriores siguen muertos: las 37 fronteras del contrato estan todas en cierto
  en la linea base instrumentada (58/58), e incluyen `echoed`, `bash_or_true`, `semicolon_exit`,
  `multiline_pwsh`, `step_if_false`, `job_if_false`, `job_needs`, `dispatch_only`,
  `job_continue_on_error` y las cuatro `continued_*`. Ademas medi el de r3 por comportamiento
  (`echo \` + runner: rechazado, y bash sale 0 sin ejecutar).
- El cableado de 0330 se sigue aceptando: workflow real, `runners=8/8 contracts=59/59` en la entrega
  y `runners=12/12 contracts=68/68` en la punta canonica, exit 0 en ambos.
- `.github/workflows/validate.yml` NO se toco en el commit juzgado (fuera de alcance, respetado).
- Estado, neutralidad, encoding y drift: exit 0 los cuatro en clon limpio.

## 8. Vector por vector

    vector                                                        veredicto  evidencia
    A. Decimo escape muerto, y con separadores NO nombrados        PASS       900 celdas, 0 escapes;
                                                                              37 casos con shell real,
                                                                              0 verde-silencioso (3)
    A'. El arreglo esta atado por una frontera                     PASS       W01 voltea
                                                                              shell_separator_mismatches (3)
    B. effective_shell_kind responde la otra mitad                 PASS       declara familia, falla
                                                                              cerrado; 2 fronteras con
                                                                              dientes; semantica medida (4)
    C. Frontera del AC5 existe y muere por mutacion                PASS       M0 muere (5)
    C'. La frontera ata la PROPIEDAD                               SLIP       4 de 7 mutantes de la
                                                                              misma afirmacion viven (5)
    D. Cuantas de las fronteras discriminan, y declarado           FAIL       residual dice 31, el
                                                                              mismo run dice 37 (6)
    D'. Redundancia del mecanismo de continuacion, declarada       PASS       W06/W07 voltean 0, y
                                                                              esta en residuals= (6)
    E. Sin regresion                                               PASS       58/58 asserts, workflow
                                                                              real 12/12 68/68 (7)

## 9. Residuales declarados por mi

- Mi espacio de 22 debilitamientos es finito: "no discrimina ninguno de los 22" es evidencia de
  inercia, no demostracion de ella. Mi 17/37 no es comparable celda a celda con el 23/31 de r4,
  porque el espacio de sonda es otro; por eso el bloqueante es el denominador, no el numerador.
- No ejecute la descodificacion de los escapes YAML contra el parser de GitHub Actions (residual
  heredado de r4, sin cambios).
- La divergencia a nivel de PALABRA (seccion 4) esta medida solo con VT; no barri la clase entera de
  caracteres que `\s` casa y bash no.
- `contracts=59/59` sigue siendo una cuenta de contratos cuyo runner tiene un paso reconocido, no una
  medida de que los 59 se EJECUTEN. Residual heredado de 0330; no debe leerse como cobertura.
- No revise el resto de jobs del workflow ni contratos ajenos a los runners declarados.
- Sin producto en alcance: no corri `npm test` ni ningun gate de Nova/Zeus.

## 10. Recomendacion de cierre

**CHANGE-REQUIRED.** Un solo bloqueante, y no toca la lista blanca:

- **B3** -- la linea certificadora contiene un residual falso: `contract_discrimination_23_of_31`
  contra el `boundaries=37` que imprime el mismo programa en la misma corrida. O el token declara el
  numero del contrato ENTREGADO junto con el metodo con que se midio, o deja de dar numero y declara
  la propiedad ("parte de las fronteras no discrimina ningun debilitamiento probado"). Cualquiera de
  las dos sirve; lo que no sirve es un numero que el propio gate desmiente dos lineas mas abajo. El
  `assert` que fija el token se actualiza en el mismo cambio.

No bloqueantes, a declarar (no exijo codigo): la deuda de la seccion 5 -- el predicado del AC5 mira
una linea y cuatro palabras, y la misma afirmacion en otras palabras sobrevive -- y el limite de la
seccion 4 sobre la nocion de palabra.

**Lo que NO hay que tocar:** el paso a `split(chr(10))`, la derivacion de la clase de separadores en
el contrato, `effective_shell_kind` y su rechazo de la familia desconocida, y
`bounded_static_certification`. Todo eso es correcto y es lo que cierra B1. El arreglo es de una
linea de texto, no de gramatica.

## 11. Bucle de arreglo esperado

1. Remediacion 5 del maker, solo sobre el literal del residual en
   `scripts/check_falsification_contracts.py` y su `assert` en
   `scripts/test_falsification_contracts.py`. Sin tocar `.github/workflows/validate.yml` ni la
   gramatica de la lista blanca.
2. Gates afectados: `check_falsification_contracts.py --inventory`,
   `test_falsification_contracts.py`, `validate_collaboration_state.py`, `scan_encoding.py`,
   `scan_domain_neutrality.py`, todos exit 0 en clon limpio.
3. Re-juicio mio ANTES del commit de cierre, acotado a B3 y a la no-regresion de A/B/C/E.
4. **Esta es la iteracion 2 de 2 del bucle de la lista blanca.** B1, el bloqueante que sostenia la
   clausula de escalada, esta CERRADO, asi que la escalada por B1 no procede. Si la remediacion 5
   tampoco deja la certificacion coherente consigo misma, eso sube al operador humano como decision
   de alcance -- si el numero se corrige aqui o se traslada a TASK-0338/TASK-0341 -- y no como una
   tercera vuelta tecnica.

-- Analista
