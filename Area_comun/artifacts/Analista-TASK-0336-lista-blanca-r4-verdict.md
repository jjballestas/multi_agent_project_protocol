# Veredicto TASK-0336 r4 (lista blanca) -- CHANGE-REQUIRED. La inversion a fail-closed esta bien tomada y cierra los nueve, pero la lista blanca CASA DOS FORMAS SINTACTICAS: decide que es una "linea" con `str.splitlines()`, y bash decide otra cosa. Hay decimo escape, con seis caracteres y por las cuatro fuentes de shell. Y la certificacion honesta de AC5 sigue sin estar atada: puedo devolver el recuento afirmativo con las 31 fronteras verdes.

Analista, 2026-08-08 14:15 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Preguntaste cual de las dos cosas compramos. Compramos la segunda, y lo tengo medido
por comportamiento, no por lectura. La lista blanca no comprueba la garantia de que el paso
contribuye al veredicto del job; comprueba que el texto del `run:` encaja en dos plantillas, y las
calcula sobre la nocion de "linea" de **Python**, que reconoce siete separadores, en vez de sobre la
de **bash**, que reconoce uno. Esa diferencia no es teorica: es un escape vivo hoy, en el mismo
commit que dice `runners=8/8 contracts=57/57`.

La inversion en si NO es el error. Fue la decision correcta y la sostengo: el criterio ahora falla
CERRADO y eso es infinitamente mejor que enumerar adornos. El error es que la region que la lista
blanca declara controlada -- `recognized_step_form` -- se calcula con la regla equivocada, asi que
hay comandos que caen DENTRO de la lista blanca y aun asi no ejecutan el runner.

---

## 1. Anclaje

- Commit juzgado: **`73822f50`** (`fix(TASK-0336): whitelist proven runner step forms`).
- HEAD del protocolo al emitir: **`87c23751`**.
- `git log --oneline 73822f50..87c23751 -- scripts/check_falsification_contracts.py
  scripts/test_falsification_contracts.py .github/workflows/validate.yml` -> **vacio**. Las tres
  rutas de alcance son identicas entre la entrega y la punta canonica; el juicio vale para las dos.
- Clon limpio: `D:/Aegis_Scratch/protocol/analista-0336r4/clone`, detached en `73822f50`,
  `git status --short` vacio. Todos los gates corridos AHI, nunca en el arbol caliente.
- Sondas y mutantes fuera del arbol atestado, bajo
  `D:/Aegis_Scratch/protocol/analista-0336r4/{matrix,m2,m3,m4,beh4,legit}`.

## 2. Reproduccion -- gates declarados, en el clon limpio (exit codes reales)

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      exit 0
    python scripts/test_falsification_contracts.py                 exit 0
    python scripts/validate_collaboration_state.py --root .        exit 0
    python scripts/scan_domain_neutrality.py --root .              exit 0
    python scripts/scan_encoding.py --root .                       exit 0
    python runtime/protocol_replay.py --check-drift --root .       exit 0
                                                 -> PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=7940

Salida certificadora tal cual la emite el commit juzgado:

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=57/57
      scope=trigger_keys+conditions+recognized_step_form+job_failure
      residuals=trigger_filters,working_directory,yaml_1_1_scalars
    FALSIFICATION_INVENTORY permanent_negatives=57 declared=57 missing=0

Los gates estan verdes. El problema no es un gate rojo; es lo que el verde afirma.

## 3. La pregunta que decide: garantia, o dos formas casadas

**Respuesta: dos formas casadas.** Tres medidas independientes lo demuestran, y ninguna depende de
mi lectura del codigo.

**(i) El primer miembro no mira el shell en absoluto.** `recognized_command_form` devuelve
`single_runner` en la primera comprobacion, ANTES de consultar `shell_guarantees_abort`. El gate
certifica que el runner se ejecuta sin poder decir que shell lo va a ejecutar. Un criterio que atara
la garantia tendria que nombrar el shell para afirmarla; este la afirma sin nombrarlo. Que hoy
todos los shells de GitHub propaguen el exit code de un unico comando es cierto, pero es una premisa
NO comprobada y NO declarada, exactamente la clase de premisa que ya nos fallo dos veces en esta
misma tarea ("los comentarios no continuan", r3).

**(ii) El criterio se calcula sobre la nocion de linea de Python, no la del shell.** Toda la
gramatica (`executable_lines`, el recuento de invocaciones, `bash_line_continues`) parte de
`command.splitlines()`. `str.splitlines()` corta por `\n`, `\r`, `\v`, `\f`, `\x1c`, `\x1d`, `\x1e`,
`\x85`, `\u2028` y `\u2029`. Bash corta por `\n`. Ese desajuste es el hallazgo B1, medido abajo.

**(iii) Una forma con garantia IDENTICA se rechaza.** `python runner.py --root .` propaga el exit
code exactamente igual que `python runner.py`, y la lista blanca la rechaza bajo TODOS los shells
(medicion en 7). Un criterio que atara la garantia la aceptaria; uno que casa plantillas no puede.

Que pasa el dia que aparezca una tercera forma legitima: **se rechaza, sin motivo que nombre la
garantia**, y el autor no tendra forma de saber si su forma es insegura o simplemente no esta en la
plantilla. Rechazar es lo correcto, coincido; lo que falta es que el rechazo diga QUE garantia no ha
podido comprobar.

## 4. B1 (BLOQUEANTE) -- decimo escape: la linea del gate no es la linea de bash

**Clase.** La misma familia C.1 de r3 (el gate y bash discrepan sobre donde empieza una linea), en
otra gramatica. En r3 discrepaban por la continuacion con `\`; aqui discrepan por el CARACTER
SEPARADOR. La inversion a lista blanca no cierra esta cara: la empeora, porque el separador extra
hace que un comando de UNA sola linea de bash se le presente al gate como un bloque de dos lineas
que encaja perfectamente en el miembro `bash_abort_block`.

**Vector.** Un paso escrito como escalar YAML entre comillas dobles, con un separador que Python
reconoce y bash no, entre un `echo` inerte y la invocacion del runner:

    - run: "echo before\rpython examples/cases/run_cases.py"

**Lo que ve el gate** (`scripts/check_falsification_contracts.py`, via PyYAML, el mismo parser que
usa el gate): dos lineas, `echo before` (encaja en `safe_echo`) y la invocacion (encaja en
`invocation`), exactamente una invocacion, ningun `\` de continuacion, shell efectivo con aborto
garantizado -> **`bash_abort_block`, WIRED, exit 0**.

**Lo que hace bash** (`bash --noprofile --norc -eo pipefail`, GNU bash 5.2.37, medido):

    caso    bash_exit  runner_ejecutado
    LF(ctl) 1          SI      <- control: con salto de linea real el runner corre y el paso enrojece
    CR      0          NO
    VT      0          NO
    FF      0          NO
    NEL     0          NO
    LS      0          NO
    PS      0          NO

Es decir: `echo` se traga la invocacion como argumento, el runner **no se ejecuta**, y el paso
**sale 0**. Verde silencioso con recuento afirmativo. Es literalmente el mutante `echoed` que el
contrato declara muerto, reescrito con otro separador.

**Cobertura del escape, medida** (sonda `probe2.py`, gate del clon limpio):

    separador        parser  lineas_py  lineas_bash  veredicto_gate   ejecuta_el_runner
    \r   (CR)        ok      2          1            WIRED (exit 0)   NO
    \v   (VT)        ok      2          1            WIRED (exit 0)   NO
    \f   (FF)        ok      2          1            WIRED (exit 0)   NO
    \x85 (NEL)       ok      2          1            WIRED (exit 0)   NO
    \u2028 (LS)      ok      2          1            WIRED (exit 0)   NO
    \u2029 (PS)      ok      2          1            WIRED (exit 0)   NO
    control: echo + salto de linea real                WIRED (exit 0)  SI (correcto)
    control: echo <runner> en una linea plana          rechazado       -- (correcto)

Y por las **cuatro fuentes de shell efectivo**, con `\r` (sonda `probe.py`): `shell: bash` en el
paso, runner Unix implicito (`runs-on: ubuntu-latest`), `defaults.run.shell` del job y
`defaults.run.shell` del workflow -> **exit 0, WIRED, las cuatro**. Es la misma matriz de cuatro
puertas que r3 cerro para la continuacion, abierta otra vez para el separador.

**Alcance en el workflow real.** El job `falsification-runners` es `windows-latest` sin `shell:`, asi
que `shell_guarantees_abort` es falso y ese job NO es vulnerable por esta via. El job `validate` es
`ubuntu-latest` y SI lo es, y aloja runners que poseen contratos: al romper su paso de contratos, el
gate reporta `runners=6/8 contracts=46/57` y nombra `scripts/test_falsification_contracts.py`,
`scripts/memory/test_memory_db.py`. Con la variante separador ese mismo paso quedaria en 8/8.

**Por que no basta con anadir estos seis caracteres a una lista negra.** Es exactamente el patron que
ya reincidio tres veces en esta cadena: estrechar la forma reduce el dano sin cambiar la clase. La
propiedad que hay que atar es *el gate y el shell tienen que estar de acuerdo sobre donde acaba un
comando*. Cualquier remediacion que sobreviva solo a los seis caracteres que yo nombre, y no a un
cambio de coordenada, vuelve aqui en r5.

**Residual honesto sobre B1.** Verifique la ruta YAML contra **PyYAML**, que es el parser que el
gate usa y sobre el que emite su veredicto -- ahi el fallo es completo y no depende de nadie mas: el
gate certifica como ejecutado un comando que ningun shell ejecuta. El eslabon que **no** ejecute es
la descodificacion del mismo escape por el parser de GitHub Actions (`\r`, `\v`, `\f`, `\N`, `\L`,
`\P`, `\xNN`, `\uNNNN` son escapes estandar de YAML 1.2 en escalar entre comillas dobles, pero no lo
corri contra su parser). Si GitHub los rechazara, el falso verde no llegaria a CI y B1 bajaria de
"escape en produccion" a "certificacion falsa del gate sobre su propia entrada" -- que sigue siendo
bloqueante para AC2/AC5, porque el gate afirma una ejecucion que su propio criterio no sostiene.
Los caracteres LITERALES (sin escape) dentro de un bloque `|` no son ruta: PyYAML los rechaza con
`ReaderError`/`ScannerError` y el gate sale rojo. Fail-closed por ahi, correcto.

## 5. B2 (BLOQUEANTE) -- la certificacion honesta de AC5 sigue sin estar atada

Mi condicion dura de 0330 era: mientras vivan escapes, no se cita un recuento afirmativo de
ejecucion. La entrega cumple la LETRA -- renombro la salida a `FALSIFICATION_STATIC_WIRING` y anadio
`scope=` y `residuals=` -- pero el contrato **no ata la propiedad**. Medido:

Mutante en `D:/Aegis_Scratch/protocol/analista-0336r4/m4`: devolver la certificacion afirmativa.

    print("FALSIFICATION_EXECUTION guaranteed=yes " ... "scope=full_execution_guarantee " ...)

Resultado:

    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml
      -> FALSIFICATION_EXECUTION guaranteed=yes runners=8/8 contracts=57/57
         scope=full_execution_guarantee residuals=trigger_filters,working_directory,yaml_1_1_scalars
    python scripts/test_falsification_contracts.py                 exit 0   <-- LAS 31 FRONTERAS VERDES

La unica frontera que mira la honestidad de la certificacion es
`assert "FALSIFICATION_EXECUTION_GUARANTEED" not in wired.stdout`. Prohibe una cadena literal que
nadie escribiria nunca; el reclamo afirmativo que AC5 prohibe de verdad pasa por debajo sin tocarla.
Es un espantapajaros: ata la FORMA (un token concreto) en vez de la PROPIEDAD (que la salida no
afirme ejecucion garantizada). El token `scope=` tampoco esta atado por ninguna frontera, asi que
puede reescribirse a `full_execution_guarantee` sin que nada enrojezca.

Anadido: con B1 vivo, el propio token actual `scope=...recognized_step_form...` sobre-afirma. La
region que la lista blanca reconoce no es la region que ejecuta.

## 6. Vector por vector

    vector                                                    veredicto  evidencia
    A. Los NUEVE escapes siguen muriendo                      PASS       matriz de 31 mutantes,
       (+ los 13 mutantes de r2 y la continuacion de r3)                 0 desviaciones (7)
    B. Ninguna forma legitima ACTUAL queda fuera              PASS       L1-L8 verdes; workflow real
       (cableado 0330 con if: always() aceptado)                         8/8 57/57 exit 0
    C. Las 31 fronteras, todas PORTANTES y EJERCIDAS          PARCIAL    31 declaradas, 31 presentes
                                                                         una sola vez, 31 ejecutadas;
                                                                         8 no discriminan (7)
    D. La certificacion afirmativa, ya se sostiene?           FAIL       B1 vive -> NO se sostiene;
                                                                         y AC5 no esta atado (5)
    E. Sin regresion en el cableado de 0330                   PASS       validate.yml intacto entre
                                                                         73822f50 y 87c23751

**Detalle de A.** Reconstrui los 31 mutantes del contrato y los corri uno a uno contra el gate del
clon limpio: `multiline_pwsh`, `step_if_false`, `step_if_event`, `bash_or_true`, `semicolon_exit`,
`continued_expression`, `continued_string`, `continued_literal`, `echoed`, `job_needs`,
`job_if_false`, `dispatch_only`, `multiline_set_plus_e`, `multiline_trap_err`,
`job_continue_on_error`, las cuatro `multiline_continuation_*`, las cuatro `multiline_splice_*`,
`multiline_unknown_command`, `no_op_help` -> **todos rechazados**; `wired`, `multiline_bash`,
`job_defaults_bash`, `workflow_defaults_bash`, `multiline_comment_backslash`, `current_step_always`
-> **todos aceptados**. **0 desviaciones respecto a lo declarado.** Los nueve estan muertos. Lo
digo sin matices: en la direccion en que se pidio, la inversion funciona.

**Detalle de D.** Con B1 vivo, `runners=8/8 contracts=57/57` NO puede citarse como prueba de
ejecucion; sigue acotado. Y por separado, aunque B1 se cerrara: `57/57 contratos` es una cuenta de
contratos cuyo runner tiene un paso reconocido, no una medida de que los 57 se EJECUTEN. Eso sigue
siendo DECLARACION, es el residual heredado de 0330, y no debe leerse como cobertura en ningun
handoff ni reporte.

## 7. C -- cuantas de las 31 son portantes de verdad

Metodo (falsable, no lectura): reconstrui los 31 mutantes y los corri contra el gate original y
contra **14 debilitamientos de un solo punto** del gate. Una frontera es portante si algun
debilitamiento la voltea; dos fronteras son distinguibles si algun debilitamiento voltea una y no la
otra. Matriz completa en `D:/Aegis_Scratch/protocol/analista-0336r4/matrix/`.

    presentes en main() exactamente una vez        31 / 31
    ejecutadas al correr el runner                 31 / 31   (main no tiene salida temprana)
    discriminan algun debilitamiento               23 / 31

Las ocho que no discriminan ninguno de los 14: `wired`, `multiline_pwsh`, `multiline_bash`,
`step_if_false`, `job_if_false`, `multiline_comment_backslash`,
`multiline_continuation_step_bash`, `multiline_splice_step_bash`.

**Y la respuesta directa a tu pregunta sobre si las nuevas hacen redundante a alguna vieja: si.**
Medido en `D:/Aegis_Scratch/protocol/analista-0336r4/m2` -- deje `bash_line_continues` en
`return False` y borre su punto de llamada, es decir **elimine entero el mecanismo de la
remediacion 2**:

    python scripts/test_falsification_contracts.py                 exit 0   <-- 31 fronteras verdes
    python scripts/check_falsification_contracts.py ... --workflow  exit 0, runners=8/8 contracts=57/57

La lista blanca ya rechaza esos bloques por otra via (una linea acabada en `\` no encaja en
`safe_echo` ni en `safe_python`), asi que las ocho fronteras de continuacion y empalme -- cuatro
viejas y cuatro nuevas -- **no fijan el guardia que nombran**. Simetricamente, al quitar la lista
blanca (`W3`) esas ocho tampoco se voltean, porque entonces las cubre el guardia. La PROPIEDAD esta
cubierta dos veces, que esta bien; lo que no esta atado es NINGUNO de los dos mecanismos por
separado, asi que el contrato no impide que un futuro refactor borre uno de los dos y se quede sin
red. No lo cuento como bloqueante -- la propiedad se sostiene hoy -- pero si como deuda declarada, y
es prima hermana de lo que ya esta registrado en TASK-0341.

Nota menor del mismo bloque: `assert wired.returncode == 0` (el ancla POSITIVA de todo el contrato)
y `assert no_op_help.returncode != 0` (el anclaje por los dos extremos del regex, que AC2 exige)
estan en `main()` pero **no** figuran entre las 31 fronteras declaradas. Se ejecutan; no se declaran.

## 8. B -- formas legitimas: lo que la inversion deja fuera, medido

Rechazar formas legitimas es el precio aceptado de invertir, y lo firmaste. Lo que pido es que
quede DECLARADO, porque hoy no lo esta y el proximo autor se lo comera de frente:

    forma                                                      veredicto del gate
    windows, una linea, sin argumentos                         ACEPTADA   <- unica forma viable
    windows, una linea, CON argumentos                         rechazada     en falsification-runners
    ubuntu,  una linea, CON argumentos                         rechazada
    shell: bash, una linea, CON argumentos                     rechazada
    shell: pwsh, bloque multilinea                             rechazada  (correcto: pwsh no aborta)
    runs-on: [self-hosted, linux], bloque multilinea           rechazada
    runs-on: ${{ matrix.os }}, bloque multilinea               rechazada
    step if: success()                                         ACEPTADA
    step continue-on-error: false                              ACEPTADA
    job needs: <dep>                                           rechazada  (correcto por diseno)

Consecuencia concreta: en `falsification-runners` (windows-latest, sin `shell:`) la **unica** forma
aceptada es la invocacion pelada sin un solo argumento. Anadir `--verbose` a cualquiera de los ocho
runners pone CI en rojo con "runner is not executed by workflow". Es fail-closed, no es un fallo, y
por eso mismo tiene que estar en `residuals=` o en el fichero de la tarea.

## 9. Residuales declarados por mi

- No ejecute la descodificacion de los escapes YAML contra el parser de GitHub Actions (seccion 4).
- Los 14 debilitamientos de la seccion 7 son un espacio de sonda finito: "no discrimina ninguno de
  los 14" es evidencia de redundancia, no demostracion de ella.
- No revise el resto de jobs del workflow ni contratos ajenos a los ocho runners.
- Sin producto en alcance: no corri `npm test` ni ningun gate de Nova/Zeus.

## 10. Recomendacion de cierre

**CHANGE-REQUIRED.** Dos bloqueantes:

- **B1** -- el criterio de forma reconocida tiene que decidir sobre la misma nocion de comando que
  el shell que va a ejecutarlo. Atar la propiedad, no los seis caracteres que yo he nombrado: la
  remediacion debe sobrevivir a un cambio de separador, de coordenada y de formato. Y `single_runner`
  debe declarar bajo que shell afirma lo que afirma, o comprobarlo.
- **B2** -- atar AC5 por comportamiento: una frontera que muera si la salida vuelve a afirmar
  ejecucion garantizada, verificada por MUTACION del texto certificador, no por presencia de un
  token concreto.

No bloqueantes, a declarar (no exijo codigo): la deuda de la seccion 7 (ningun mecanismo fijado por
separado; dos asserts sin declarar) y las formas legitimas rechazadas de la seccion 8 en
`residuals=`.

**Lo que NO hay que tocar:** la inversion a lista blanca se queda. Es correcta y cierra los nueve.
El arreglo es dentro de ella, no volviendo a enumerar escapes.

## 11. Bucle de arreglo esperado

1. Remediacion 4 del maker sobre `scripts/check_falsification_contracts.py` y
   `scripts/test_falsification_contracts.py`. Sin tocar `.github/workflows/validate.yml`.
2. Gates afectados: `check_falsification_contracts.py --inventory`,
   `test_falsification_contracts.py`, `validate_collaboration_state.py`, `scan_encoding.py`,
   `scan_domain_neutrality.py`, todos exit 0 en clon limpio.
3. Re-juicio mio ANTES del commit de cierre, con AC1 rehecho: los nueve mas el decimo, y la mutacion
   del texto certificador.
4. **Maximo 2 iteraciones** antes de escalar al operador humano. Esta es la iteracion 1 del bucle de
   la lista blanca; la cadena 0330 -> 0336 ya consumio una escalada, asi que si r5 no cierra B1 esto
   sube al humano con la particion propuesta, no una tercera vuelta.

-- Analista
