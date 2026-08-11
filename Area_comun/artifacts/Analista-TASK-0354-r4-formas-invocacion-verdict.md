# VEREDICTO TASK-0354 r4 -- el reconocedor de formas de invocacion

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0354-r4.md
    escrito             2026-08-11 16:04 local (UTC+2)  ==  2026-08-11T14:04Z
    veredicto           CHANGE-REQUIRED
    alcance             SOLO hub, sin producto. G2 fuera de alcance (aceptado, ver seccion 5).
    iteracion           vuelta 1 de la remediacion G1 autorizada por el operador; 1 de 2

## 0. Ancla canonica

    ancla de la instruccion   02c58629d11c7f5b4b6f109e313c8bd656cd3658
    implementacion            736b03f2434bba43c830784e03b6fab49d0573cc
    origin/main               0e937f4e

`.github/workflows/validate.yml` es byte-identico en los tres:

    git diff --stat 736b03f2 02c58629 -- .github/workflows/validate.yml   -> (vacio)
    git diff --stat 02c58629 origin/main -- .github/workflows/validate.yml -> (vacio)

Juzgo en el ancla.

## 1. Reproduccion -- clon limpio, entorno fiel, gate por exit code

Dos clones `--shared --no-hardlinks` bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/r54r4/` (DECISION-0104), nunca en el arbol caliente:

    c1  @ 02c58629   (medicion; `git status --short` vacio)
    c2  @ 02c58629   (mutantes; `git checkout -- .` y verificado limpio tras cada tanda)

Interprete fiel al job `validate`, con exactamente lo que ese job instala y nada mas
(`cryptography jsonschema pyyaml` + transitivas), porque este gate lee `packages_distributions()`
del interprete en el que corre y un host gordo miente en las dos direcciones.

Puertas de protocolo en `c1`, gateadas por `$?` del comando, nunca detras de un pipe:

    python scripts/validate_collaboration_state.py --root .        EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                       EXIT=0  OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .              EXIT=0
    python runtime/protocol_replay.py --check-drift --root .       EXIT=0  verdict=CLEAN up_to_seq=8769
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      EXIT=0  runners=12/12 contracts=73/73

El gate bajo revision lo extraje del YAML con un **parser independiente** (PyYAML sobre el
documento, localizando el paso por `name`, no copy-paste), quitando solo el envoltorio
`python - <<'PY'` / `PY`: 4073 bytes, 104 lineas. Todo mutante de abajo corre ese mismo cuerpo.

    U0  c1 intacto      WORKFLOW_RUNNER_DEPENDENCIES PASS runners=73   EXIT=0

Reproduce el baseline que declara la instruccion.

## 2. La pregunta unica -- NO, la clase de FORMAS sigue abierta

Ataque en las **dos direcciones**, con un probe real
(`examples/probe_cases/run_probe_cases.py`, cuyo unico import es `attrs`, externo y **no**
declarado por el job `falsification-runners`, que no declara nada):

- **direccion A (ALTA):** anado un paso nuevo con la forma X. Si el gate la descubre -> ROJO
  (dependencia no declarada). Si no la descubre -> `checked` sigue en 73 y **PASS silencioso**.
- **direccion B (REESCRITURA):** reescribo la invocacion que ya existe con la forma X. Si el gate
  la pierde, el contador baja 73 -> 72 y enrojece.

28 formas probadas. **14 escapan al descubrimiento.** Tabla completa (EXIT del gate):

    forma                                             A: alta   B: reescritura   descubierta?
    ------------------------------------------------- --------- ---------------- ------------
    K0  python <ruta>                    (control)    1 dep     0 (sigue 73)     SI
    K8  python "<ruta>"                  (control)    1 dep     0                SI
    K9  python3.12 <ruta>                (control)    1 dep     0                SI
    K11 env python <ruta>                (control)    1 dep     0                SI
    K12 cd . && python <ruta>            (mi M3 r2)   1 dep     0                SI
    K13 python -m <modulo>               (mi M5 r2)   1 dep     0                SI
    K14 exec python <ruta>                            1 dep     0                SI
    K15 uv run python <ruta>                          1 dep     0                SI
    K17 python ./<ruta>                               1 dep     0                SI
    K18 if ! python <ruta>; then ...     (G1 de r2)   1 dep     0                SI
    K19 timeout 60 python <ruta>                      1 dep     0                SI
    K22 & python <ruta>                  (pwsh)       1 dep     0                SI
    K24 python "<ruta con backslash>"                 1 dep     0                SI
    K27 python.exe <ruta con /  >                     1 dep     0                SI
    ------------------------------------------------- --------- ---------------- ------------
    K1  python -u <ruta>                              0 MUDO    1 (contador)     NO
    K10 python -X utf8 <ruta>                         0 MUDO    1 (contador)     NO
    K16 python -W ignore <ruta>                       0 MUDO    1 (contador)     NO
    K2  python \ <LF> <ruta>                          0 MUDO    1 (contador)     NO
    K3  PY=python <LF> $PY <ruta>                     0 MUDO    1 (contador)     NO
    K4  sh -c "python <ruta>"                         0 MUDO    1 (contador)     NO
    K6  for f in <ruta>; do python "$f"; done         0 MUDO    1 (contador)     NO
    K20 echo <ruta> | xargs python                    0 MUDO    1 (contador)     NO
    K5  py -3 <ruta>                                  0 MUDO    1 (contador)     NO
    K7  python "$GITHUB_WORKSPACE/<ruta>"             0 MUDO    1 (contador)     NO
    K21 python <ruta con backslash>                   0 MUDO    1 (contador)     NO
    K23 python .\<ruta con backslash>                 0 MUDO    1 (contador)     NO
    K25 & python <ruta con backslash>     (pwsh)      0 MUDO    1 (contador)     NO
    K26 python.exe <ruta con backslash>               0 MUDO    1 (contador)     NO

Cuatro familias, y cada una tiene su mecanismo concreto:

**a) Cualquier flag del interprete antes del script (K1, K10, K16).** El descubrimiento solo mira
`parts[index+1]`: si ahi hay un `-u`, un `-X` o un `-W`, no acaba en `.py`, no es `-m`, y el
generador **no sigue buscando**. `python -u foo.py` es la forma canonica en CI para que el log no
se quede en el buffer.

**b) El modelo de linea (K2, K3, K4, K6, K20).** El generador trocea `command.splitlines()` **antes**
de tokenizar, asi que la continuacion de linea de Bash no existe para el, y cualquier indireccion
--variable, `sh -c`, bucle, `xargs`-- deja el nombre del script en un token que no es el siguiente
al ejecutable. Evidencia del mecanismo, `shlex.split(..., posix=True)`:

    'python -u a.py'                     -> ['python', '-u', 'a.py']
    'python \'                           -> ValueError: No escaped character      (linea descartada)
    'PY=python'                          -> ['PY=python']                         (no casa el regex)
    'sh -c "python a.py"'                -> ['sh', '-c', 'python a.py']           (un solo token)
    'echo a.py | xargs python'           -> ['echo', 'a.py', '|', 'xargs', 'python']
    'python $GITHUB_WORKSPACE/a.py'      -> ['python', '$GITHUB_WORKSPACE/a.py']  (no resuelve)

**c) `py -3` (K5).** El lanzador de Windows. `py` no casa
`python(?:3(?:\.\d+)?)?(?:\.exe)?`. Y esto **no es teorico en este repo**: el gemelo
`scripts/check_falsification_contracts.py` que ya vive aqui SI lo reconoce
(`py(?:\.exe)?(?:\s+-3)?`, linea 152). El repo tiene dos reconocedores de la misma pregunta y solo
uno cubre esta forma.

**d) La ruta con backslash sin comillas (K21, K23, K25, K26) -- la mas grave.** `posix=True` trata
`\` como caracter de escape y **se lo come**:

    'python examples\cases\run_x.py'  ->  ['python', 'examplescasesrun_x.py']

El token resultante no existe como fichero y la invocacion desaparece. El job
`falsification-runners` corre en **windows-latest**, donde `\` es separador de rutas, no escape; y
los mensajes de error del propio gate imprimen las rutas con backslash
(`examples\probe_cases\run_probe_cases.py`). El gate **no sabe leer el formato que el mismo emite**.
Con comillas dobles sobrevive (K24), sin comillas no (K21). Elegir `posix=True` para un workflow
que tiene un job de Windows es un error de categoria, no un hueco de lista.

**Contra el criterio de la propia instruccion** -- "si hay que anadir una forma mas al patron, es que
sigue siendo una lista" -- hay que anadir catorce. Sigue siendo una lista.

### Y el escape es de SERVICIO, no de certificacion

No me quedo en el contador. Con el probe anadido como `python -u`:

    gate                                                        PASS runners=73   EXIT=0
    <interprete con SOLO lo que instala ese job> -u examples/probe_cases/run_probe_cases.py
        ModuleNotFoundError: No module named 'attrs'            EXIT=1

Es decir: el runner **muere en el import** en el entorno exacto del job, y la puerta que existe para
impedirlo dice PASS. Es el defecto original de TASK-0354, entero, por una forma nueva.

## 3. El contador -- ata la reescritura, no ata la clase, y se desata a si mismo

Lo bueno primero, y lo verifique: `!=` enrojece en **las dos direcciones** y la direccion B de la
tabla lo confirma **14 de 14**: reescribir una invocacion existente con cualquiera de las formas que
se escapan ya no es silencioso. Ese era mi punto 2 de r2 y esta cumplido.

Pero el contador cuenta el **cardinal del conjunto descubierto**, no el conjunto invocado. De ahi
dos consecuencias medidas:

**3.1 Ciego a las altas.** Columna A de la tabla: 14 formas dan `checked = 73` y **EXIT=0 sin una
sola linea de aviso**. Un runner nuevo escrito `python -u ...` entra en CI sin declarar sus
dependencias y el testigo no se mueve. El contador solo vigila que no se caiga lo que ya estaba.

**3.2 El testigo se desata con la edicion que su propio mensaje nombra.** Cadena completa, mismo
arbol, medida de punta a punta:

    paso 1  reescribo la invocacion del job de Windows como `python -u ...`
            e inyecto `import attrs` en ese runner (tras el `from __future__`)

            gate (expected=73)   FAIL  "workflow runner inventory changed:
                                        expected 73 invocations, discovered 72"   EXIT=1
            comportamiento real  ModuleNotFoundError: No module named 'attrs'     EXIT=1

    paso 2  "arreglo" el rojo como indica su propio mensaje: literal 73 -> 72

            gate (expected=72)   WORKFLOW_RUNNER_DEPENDENCIES PASS runners=72     EXIT=0
            comportamiento real  ModuleNotFoundError: No module named 'attrs'     EXIT=1

El rojo es indistinguible entre las dos situaciones que puede senalar --"quite un runner a proposito"
y "escondi un runner sin darme cuenta"-- y en las dos la reparacion natural es la misma: bajar el
literal. Un testigo cuya unica reparacion documentada lo desactiva no ata la propiedad; ata la
constancia de un numero que el maker edita.

## 4. Si hay fuente independiente de la que derivar el 73 -- SI, y dos

La instruccion lo pregunta como observacion. La respuesta es afirmativa y las dos ya estan en el
repo o cuestan pocas lineas.

**4.1 Ya enviada: el registro de contratos del gemelo.** `scripts/check_falsification_contracts.py`
deriva su poblacion de los **duenos de contrato** (`owners[contract.id]`), no de un literal, y
reconoce la invocacion con una **lista blanca fail-closed** (`recognized_command_form`) que exige
`fullmatch`, acepta `[\\/]` como separador, trata `py -3`, **rechaza** las continuaciones de linea, y
honra `if:`, `needs` y `continue-on-error`. Medido sobre el mismo arbol del paso 1 de la cadena:

    gemelo   ERROR: retry-ledger-preservation-property: runner is not executed by workflow:
             examples\mailbox_retry_cases\run_mailbox_retry_cases.py
             FALSIFICATION_STATIC_WIRING runners=11/12                             EXIT=1

Nombra el **runner**, no un cardinal, y `11/12` sale del registro: no hay literal que bajar. Cubre 12
de las 73 invocaciones (las que tienen contrato), asi que no basta por si sola, pero prueba que la
casa ya tiene la pieza y que el gate nuevo **divergio de ella hacia fail-open**. Dos puertas, un
mismo YAML, dos reconocedores, posturas opuestas: eso es la trampa de paridad de gemelos.

**4.2 Derivar la poblacion de la CONDICION, no reconocer la forma.** El criterio de pertenencia de
la clase no es "como se invoca python", es **"el workflow nombra un fichero .py del repo en un
bloque `run`"**. Eso no depende de la forma. Lo implemente y lo medi (regex sobre el texto crudo del
`run`, normalizando `\` a `/`, resolviendo por sufijo para que `$VAR/` y `.\` sigan aterrizando en el
fichero):

    arbol del ancla:   descubierto por el gate = 73   derivado de la condicion = 73   (coinciden)
    los 14 escapes:    descubierto = 73               derivado = 74   -> CATCHES  14 de 14

Cero divergencia sobre el arbol de hoy --no introduce ni un falso rojo-- y **mata las catorce**,
incluidas las cuatro de backslash y la de `$GITHUB_WORKSPACE`. Con eso el `expected_runner_invocations`
literal desaparece: la asercion pasa a ser "todo fichero .py del repo nombrado en un `run` esta en el
conjunto descubierto", y el error nombra la **ruta** concreta en vez de un numero. Los falsos
positivos que pueda tener (un `.py` mencionado como argumento de otra cosa) son **fail-closed**:
obligan a declarar o a exceptuar explicitamente, no a callar.

Es una recomendacion, no una implementacion: yo no implemento.

## 5. Lo que esta bien, y lo verifique mas fuerte que la entrega

**Las dos falsaciones que la entrega declara son honestas.** Las corri yo, no las lei:

    M1  quito pyyaml del job python                    FAIL EXIT=1  "imports yaml; requires
                                                       one of ['pyyaml'], declared ['jsonschema']"
    M3  el mismo runner como `cd . && python ...`
        + pyyaml quitado                               FAIL EXIT=1  (mensaje de dependencia, no contador)
    M5  el mismo runner como `python -m <modulo>`
        + pyyaml quitado                               FAIL EXIT=1  (mensaje de dependencia, no contador)

M3 y M5 son **literalmente** los dos falsadores que puse en mi minimo de r2, y los dos matan al
mutante por la razon correcta: la dependencia, no el cardinal. La forma `if ! python ...` que era el
**G1 instanciado** de r2 esta cerrada (K18 descubierta). `cd . &&`, `python -m`, `python3.12`,
`python.exe`, `./`, comillas, y los envoltorios `env` / `exec` / `timeout` / `uv run` / `&` de pwsh
tambien. El avance es real: de las 28 formas que probe, 14 estan cerradas y antes lo estaban muchas
menos.

**El contador esta atado con `!=`,** no solo contra bajadas, y su rojo es ruidoso (EXIT=1). Es el
testigo que pedi; lo que le falta es de donde sale el numero (seccion 3.2 y 4).

**G2 esta cerrado por declaracion escrita, que es exactamente la alternativa que ofrecio mi r2.** El
fichero de tarea dice ahora: "la superficie de la puerta termina en el fichero del runner descubierto.
No calcula clausura transitiva de imports locales ni certifica procesos hijo." Eso satisface mi punto
3 de r2 en su rama declarativa y cubre tambien G6. Lo acepto y no lo vuelvo a gatear.

**No hay instancia viva del hueco en el arbol de hoy.** Lo medi, no lo supongo: descubierto = 73 y
derivado de la condicion = 73, sin una sola divergencia. A diferencia de r2 --donde G1 vivia dentro
del propio fichero, dos pasos por encima del gate-- hoy **la clase esta abierta y la instancia
cerrada**. El riesgo es del proximo paso que alguien escriba, no del arbol actual. Lo digo porque
cambia el calculo de urgencia y no quiero que mi rojo se lea como "hay algo roto en CI hoy".

## 6. Residuales declarados

1. **Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate **nunca
   ha corrido en GitHub Actions** y su veredicto depende de que paquetes trae la imagen del runner,
   que no es mi host. Sigue vivo el G7 de r2 (el mapa modulo->distribucion sale del interprete de
   `validate` y se aplica a los otros jobs); no lo re-medi en esta vuelta, no estaba en alcance.
2. **G3 sigue abierto y no declarado.** Re-medido: un `if: false` sobre el paso
   "Install falsification runner dependencies" deja `PASS runners=73 EXIT=0`. `declared_distributions`
   sigue sin mirar `if:` ni el orden. No estaba en el alcance autorizado de esta vuelta; lo dejo
   senalado, no lo gateo.
3. **Asimetria nueva descubrimiento/declaracion.** La remediacion ensancho el descubrimiento (token,
   cualquier posicion, `python3`/`.exe`/ruta) y **dejo la declaracion anclada** a
   `parts[:4] == ["python","-m","pip","install"]` en la posicion 0. Medido: escribir la instalacion
   como `python3 -m pip install jsonschema pyyaml` deja `declared []` y la puerta ROJA (EXIT=1). Es
   **fail-closed**, o sea seguro, pero es un falso rojo esperando a la primera reescritura de la
   linea de instalacion, y es la prueba de que ahora hay **dos** listas de formas que mantener en vez
   de una.
4. **No corri los 78 pasos del job `validate`.** Verifique el paso del gate y las cuatro puertas de
   protocolo. El resto queda sin medir, como en r2.
5. **La superficie `.ps1` (G4 de r2) sigue fuera.** Cuatro puntos de entrada `.ps1` que el workflow
   ejecuta invocan python por dentro y el gate no abre un solo `.ps1`. La declaracion escrita de la
   entrega cubre "procesos hijo", asi que lo cuento cubierto por declaracion, no por mecanismo. Mi
   alternativa de la seccion 4.2 **tampoco** lo cierra: si el `.py` no se nombra en el YAML, no esta
   en la poblacion. Lo digo para no vender la recomendacion como mas de lo que es.
6. **Mi probe es sintetico** (`examples/probe_cases/run_probe_cases.py`, `import attrs`). Vive solo
   en el clon de mutantes `c2`, jamas en el arbol gobernado, y `c2` quedo restaurado y verificado
   (`git checkout -- .`, YAML byte-identico al original en cada tanda).
7. **No juzgo el ahorro economico** de la concurrencia ni la colocacion; ningun AC lo pide y no
   cambio de opinion respecto a r2.

## 7. Recomendacion de cierre

**CHANGE-REQUIRED.** La respuesta a la pregunta unica es **no**: tokenizar es mejor que anclar al
principio de linea --y cierra el G1 que estaba instanciado-- pero sigue siendo un reconocedor de
formas, y catorce formas realistas lo atraviesan sin dejar senal en la direccion de ALTA. La mas
grave no es exotica: es la ruta con backslash sin comillas en el unico job que corre en Windows, en
un gate que imprime sus propios errores con backslash.

Y lo digo tambien de mi parte, porque el defecto empieza en mi encargo: **mi minimo de r2 enumero dos
falsadores (M3, M5) y la remediacion me devolvio exactamente esos dos, verdes**. Pedir "que reconozca
cualquier invocacion de python en cualquier posicion de la linea" nombraba un espacio de formas, no
la propiedad. El maker cumplio la letra de lo que escribi. La letra era estrecha.

### Lo minimo que cierra esta vuelta

1. **Derivar la poblacion de la condicion** ("un fichero .py del repo nombrado en un bloque `run`"),
   y asertar que el conjunto descubierto la contiene, nombrando la **ruta** que falta. Medido en la
   seccion 4.2: coincide con el arbol de hoy (73 == 73, cero falsos rojos) y mata las 14.
   Se falsa con las 14 filas MUDO de la tabla: cada una debe pasar a EXIT=1.
2. **Que desaparezca `expected_runner_invocations = 73`** como literal, o que su unica reparacion
   documentada deje de ser bajarlo. Se falsa con la cadena de la seccion 3.2: si editar el literal
   vuelve verde un arbol donde un runner muere en el import, el testigo no ata nada.
3. **No aceptar `posix=True` para un YAML con un job de Windows**, o declarar por escrito que las
   rutas en los `run` deben ir siempre con `/` o entre comillas y gatearlo. Se falsa con K21/K23/K25/K26.

Si el maker prefiere no ampliar el mecanismo, la salida alternativa --como con G2-- es **declarar por
escrito y con precision** que la superficie cubierta es "invocaciones donde el nombre del script es
el token inmediatamente posterior al ejecutable, sin flags intermedios, en una sola linea fisica, con
separador `/`", y aceptar que cualquier otra forma entra en CI sin gate. Es una frase honesta y
verificable; lo que no sostiene el cierre es "reconoce una invocacion de Python en cualquier posicion"
tal como esta escrito hoy en el fichero de tarea, porque mide la posicion y no la forma.

### Puertas afectadas y ciclo de la remediacion

Puertas: `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`, `check_falsification_contracts.py --inventory`, mas el propio gate
bajo un interprete con **solo** lo que declara cada job.

Ciclo: **maximo 2 iteraciones** desde esta. Esta es la vuelta 1 de la remediacion G1 autorizada por el
operador. Re-juicio mio antes del commit de cierre; si la vuelta 2 vuelve a estrechar la lista en vez
de cambiar el criterio de pertenencia, **escalo al operador humano** en lugar de pedir una tercera.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `02c58629d11c7f5b4b6f109e313c8bd656cd3658`, implementacion `736b03f2`.
Alcance: solo el hub, sin producto en alcance.
