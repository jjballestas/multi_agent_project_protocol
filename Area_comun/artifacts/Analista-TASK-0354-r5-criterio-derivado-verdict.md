# VEREDICTO TASK-0354 r5 -- el criterio derivado y la coordenada que queda

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0354-r5.md
    escrito             2026-08-11 18:25 local (UTC+2)  ==  2026-08-11T16:25Z
    veredicto           CHANGE-REQUIRED  +  ESCALADO AL OPERADOR HUMANO
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           vuelta 2 de 2 del presupuesto fijado en r4

## 0. Ancla canonica

    implementacion            90fa8ffa48ea7722679aca3d0c5a12d019d2b2e4
    origin/main               f65440d9
    ancestro                  git merge-base --is-ancestor 90fa8ffa origin/main  -> SI

Juzgo en `90fa8ffa`, nunca en el arbol caliente (que hoy tiene entrega a medias de Codex sobre
TASK-0359, rutas ajenas que no toco).

## 1. Reproduccion -- clon limpio, interprete fiel, gate por exit code

Dos clones `--shared --no-hardlinks` bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/r54r5/` (DECISION-0104), nunca en el arbol gobernado:

    c1  @ 90fa8ffa   (medicion; `git status --short` vacio)
    c2  @ 90fa8ffa   (mutantes; restaurado y verificado byte-identico tras cada tanda)

Interprete fiel al job `validate`: venv limpio 3.12.10 con exactamente `cryptography jsonschema
pyyaml` y sus transitivas, porque este gate lee `packages_distributions()` del interprete en el que
corre. Un segundo venv **vacio** representa a los jobs que no instalan nada.

Puertas de protocolo en `c1`, gateadas por `$?` real del comando, jamas detras de un pipe:

    python scripts/validate_collaboration_state.py --root .        EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                       EXIT=0  OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .              EXIT=0
    python runtime/protocol_replay.py --check-drift --root .       EXIT=0  verdict=CLEAN up_to_seq=8790
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      EXIT=0

El gate bajo revision lo extraje del YAML con un **parser independiente** (PyYAML sobre el
documento, localizando el paso por `name`; no copy-paste), quitando solo el envoltorio
`python - <<'PY'` / `PY`: 4921 bytes, 128 lineas. Todo mutante de abajo corre ese mismo cuerpo.

    U0  c1 intacto      WORKFLOW_RUNNER_DEPENDENCIES PASS invocations=73 referenced=72   EXIT=0

Reproduce el baseline que declara la instruccion.

## 2. La evidencia del maker -- verificada, no aceptada

    afirmacion del maker                                    mi medicion                    veredicto
    ------------------------------------------------------- ------------------------------ ---------
    gate intacto EXIT=0, invocations=73 referenced=72        identico                       CONFIRMA
    14 adiciones antes silenciosas -> 14/14 EXIT=1           14/14 EXIT=1                   CONFIRMA
    4 adiciones backslash bajo el job Windows -> 4/4 EXIT=1  4/4 EXIT=1 (W21 W23 W25 W26)   CONFIRMA
    el literal 73 ya no existe                               ausente del cuerpo             CONFIRMA
    puertas de protocolo EXIT=0, drift limpio                seccion 1                      CONFIRMA

Las catorce que yo mismo false en r4 estan muertas, y **ninguna murio porque se anadiera su forma al
reconocedor**: `python_runner_tokens` sigue sin entenderlas. Mueren por la contencion. Eso es una
diferencia de naturaleza, no de tamano, y la reconozco entera.

## 3. Pregunta 1 -- ?el conjunto se DERIVA o es una enumeracion reescrita?

**Se DERIVA.** No es una lista con otro nombre, y lo sostengo con tres hechos verificables:

1. La poblacion sale de `root.rglob("*.py")` -- 206 ficheros hoy en el arbol --, no de un literal ni
   de un catalogo mantenido a mano. Anadir un `.py` al repo cambia la poblacion sin tocar el gate.
2. No hay ningun patron nuevo de forma de invocacion: el diff `736b03f2 -> 90fa8ffa` no anade una
   sola alternativa al `re.fullmatch` del ejecutable. Las catorce formas mueren por
   `expected_in_step - discovered_in_step`, no por reconocimiento.
3. El error nombra la **ruta** que falta, no un cardinal, y su reparacion natural es declarar la
   dependencia o corregir la invocacion. No hay numero que bajar. El auto-desarme de r4 esta muerto.

Esa es la respuesta directa a la pregunta de la instruccion, y es afirmativa.

## 4. Pregunta 2 -- ?sobrevive a un cambio de coordenada? NO en una, y es la que importa

Bateria de 31 formas en direccion **ALTA** (paso nuevo que invoca un probe real del repo,
`examples/probe_cases/run_probe_cases.py`, cuyo unico import es `attrs`). El probe existe en disco,
asi que entra en la poblacion derivada; si el gate lo pierde, `EXIT=0` sin una linea.

    coordenada que cambio                                    resultado
    -------------------------------------------------------- ---------------------------------
    separador  (\ en vez de /)                                CAUGHT  K21 K23 K26 W21 W23 W26
    entrecomillado ("..." , "$GITHUB_WORKSPACE/...")          CAUGHT  K24 K7 F2
    host (job Windows, semantica no-POSIX, `& python`)        CAUGHT  W25 y el resto del set W
    flags del interprete (-u, -X utf8, -W ignore)             CAUGHT  K1 K10 K16
    continuacion de linea, variable, sh -c, xargs, for, py -3 CAUGHT  K2 K3 K4 K20 K6 K5
    sustitucion de comando `$(echo <ruta>)`                   CAUGHT  N7
    `python -c "runpy.run_path('<ruta>')"`                    CAUGHT  N12
    -------------------------------------------------------- ---------------------------------
    **que la ruta NO se escriba como ruta relativa al repo**  **SILENT, 12 de 12**

Las doce que escapan, todas `EXIT=0` con `invocations=73 referenced=72`, es decir sin senal alguna:

    N1   working-directory: <dir>   +  run: python <basename>          SILENT
    N11  lo mismo sobre el job de Windows                              SILENT
    N2   cd <dir> && python <basename>                                 SILENT
    N13  cd <dir> ; python ./<basename>                                SILENT
    N9   pushd <dir> ; python <basename>                               SILENT
    N6   cd examples && python <subruta>                               SILENT
    N3   DIR=<dir> ; python "$DIR/<basename>"                          SILENT
    N8   BASE=<basename> ; python <dir>/$BASE                          SILENT
    N4   python examples/probe_*/run_probe_cases.py      (glob)        SILENT
    N5   python examples/probe_cases/run_probe_case?.py  (glob)        SILENT
    N10  find <dir> -name '*.py' -exec python {} +                     SILENT
    N14  bash -c 'cd <dir> && python <basename>'                       SILENT

No son formas exoticas ni inventadas para el papel. `working-directory` es una clave de primera
clase de GitHub Actions y `cd <dir> && python <script>` es el idiom mas comun de CI. Comprobe que
**ejecutan de verdad**, no que solo parezcan validas:

    bash -c "cd examples/probe_cases && python run_probe_cases.py"   ->  "probe attrs"   EXIT=0
    lo mismo con el interprete vacio (job que no declara nada)       ->  ModuleNotFoundError: attrs

El criterio de pertenencia implementado no es "un fichero .py del repo que el bloque `run`
ejecuta", sino **"un fichero .py del repo cuya ruta relativa aparece escrita literalmente en el
texto del `run`"**. Sigue siendo una condicion sobre la FORMA; lo que cambio es de que: de la forma
de invocar python a la forma de escribir la ruta. Por eso la respuesta a la pregunta 2 es que
sobrevive a todas las coordenadas que la instruccion nombra menos a una, y esa una es donde vive
la clase.

## 5. Lo grave: la direccion B se perdio, y con ella vuelve el defecto original entero

En r4 certifique que el contador `!=` enrojecia **en las dos direcciones**, y que reescribir una
invocacion existente ya no era silencioso: 14 de 14. Ese contador desaparecio -- porque yo pedi que
desapareciera -- y con el se fue esa propiedad. Medido sobre un runner **real** del repo,
`examples/neutrality_scan_cases/run_powershell_host_cases.py`, que importa `yaml` y vive en el job
`powershell-linux-parity`, que declara exactamente `pyyaml`:

    B1  reescribo su invocacion como `cd <dir> && python <basename>`, sin tocar dependencias
        gate  -> PASS invocations=72 referenced=71   EXIT=0     (73 -> 72, sin una sola senal)

    B2  la misma reescritura  +  quito `pyyaml` de la linea de instalacion de ESE job
        gate            -> WORKFLOW_RUNNER_DEPENDENCIES PASS invocations=72 referenced=71  EXIT=0
        comportamiento  -> ModuleNotFoundError: No module named 'yaml'                     EXIT=1
                           (interprete sin instalaciones, el que deja ese job)

    B3  identico a B2 pero ocultando con `working-directory:` en vez de `cd`
        gate  -> PASS invocations=72 referenced=71   EXIT=0     comportamiento -> EXIT=1

    B0  control: quito `pyyaml` SIN ocultar la invocacion
        gate  -> FAIL   EXIT=1                                  (la puerta funciona cuando ve)

B2 y B3 son el defecto original de TASK-0354 **completo**: la puerta que existe para impedir que un
runner entre en CI sin su dependencia dice PASS mientras el runner muere en el import. Y la
coordenada que lo consigue **no toca el runner**: son dos lineas del YAML.

Esto no es "la lista se estrecho otra vez". Es otra cosa, y hay que nombrarla bien: la remediacion
**cambio un testigo que funcionaba en un eje por otro que funciona mejor en el otro eje**, y nadie
midio el eje que se soltaba. Las 73 invocaciones vivas de hoy son ocultables una a una.

## 6. Mi parte, que es la mayor

El agujero es **heredado de mi recomendacion de r4**, seccion 4.2, literal: "regex sobre el texto
crudo del `run`, normalizando `\` a `/`, resolviendo por sufijo". Eso es exactamente lo que se
implemento, y lo que se implemento es exactamente lo que yo medi y di por bueno. El maker no
estrecho nada: entrego mi recomendacion con fidelidad, y mi recomendacion presuponia sin decirlo
que el cwd de todo paso es la raiz del repositorio. Yo tampoco medi la direccion B contra mi propia
propuesta antes de firmarla.

Es el mismo patron que ya me costo r4: mi encargo nombro una implementacion en vez de la propiedad,
y recibi la implementacion. Lo dejo escrito aqui porque el reparto de responsabilidad cambia lo que
el operador debe decidir.

## 7. Residuales nuevos y viejos, medidos

**7.1 NUEVO -- falso rojo por gemelo de sufijo, 23 pares vivos.** El lookbehind
`(?<![A-Za-z0-9_.-])` no excluye `/`, asi que toda ruta del repo que sea **sufijo** de otra ruta del
repo entra en `expected` cuando se nombra la larga. Hoy hay 23 pares (todo
`examples/full_runtime_instance/**` duplica `runtime/**` y `scripts/**`). Medido:

    paso nuevo:  python examples/full_runtime_instance/runtime/guardrails.py   (fichero REAL, correcto)
    gate      ->  FAIL  "validate: Python file named in run block was not discovered:
                         runtime/guardrails.py"                                 EXIT=1

Es fail-closed, o sea seguro, pero es un rojo **falso** cuyo mensaje nombra una ruta que no aparece
en el comando. Un maker que se lo encuentre no tiene reparacion documentada, y la reparacion
"natural" es debilitar la derivacion. Es el molde del auto-desarme de r4 en forma nueva.

**7.2 G3 sigue abierto y sin declarar.** Re-medido en este ancla: un `if: false` sobre el paso
"Install falsification runner dependencies" deja `PASS invocations=73 referenced=72` EXIT=0.
`declared_distributions` sigue sin mirar `if:` ni el orden.

**7.3 La asimetria descubrimiento/declaracion sigue.** `declared_distributions` sigue anclada a
`parts[:4] == ["python","-m","pip","install"]` en posicion 0. Re-medido: `python3 -m pip install
jsonschema pyyaml` deja `declared []` y la puerta ROJA. Fail-closed, pero son dos listas de formas
que mantener.

**7.4 Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate
**nunca ha corrido en GitHub Actions**. Sigue vivo el G7 de r2 (el mapa modulo->distribucion sale
del interprete de `validate` y se aplica a los otros jobs); no lo re-medi, no estaba en alcance.

**7.5 La superficie `.ps1` (G4) sigue fuera**, cubierta por declaracion escrita, no por mecanismo.
Mi recomendacion de la seccion 8 **tampoco** la cierra.

**7.6 No corri los 77 pasos del job `validate`.** Verifique el paso del gate y las cinco puertas de
protocolo. El resto queda sin medir, como en r2 y r4.

**7.7 Mi probe es sintetico** y vivio solo en el clon de mutantes `c2`, jamas en el arbol
gobernado. `c2` quedo restaurado y verificado: `git diff` vacio contra `90fa8ffa`.

## 8. Lo minimo que cierra -- medido, no propuesto a ciegas

La rama fail-open esta en **una linea**. Hoy, cuando el token descubierto no resuelve a un fichero
del repo, el gate hace `continue` en silencio. Convertir ese caso en error **solo para la forma
script** (no para `-m`, que resuelve legitimamente fuera del repo, p.ej. `pip`):

    if not runner.is_file():
        if kind == "script":
            errors.append(f"{job_name}: python script target is not a repository file: {runner_token}")
        continue

Lo implemente sobre el cuerpo extraido y lo medi en los dos sentidos:

    arbol intacto de 90fa8ffa       PASS invocations=73 referenced=72   EXIT=0   <- CERO falsos rojos
    de los 14 casos silenciosos     11 pasan a EXIT=1, incluidos B2 y B3
    sobreviven 3                    N8 ($BASE compuesto), N10 (find -exec), N14 (bash -c '...')

Los tres supervivientes son aquellos en los que el token posterior a `python` **no es una ruta .py
en absoluto**, asi que ni siquiera hay candidato que resolver; esos requieren otra idea o quedan
declarados. Doy la medicion completa, no la parte que me conviene.

Es una **recomendacion medida, no una implementacion**: yo no implemento.

**Salida alternativa, sin tocar mecanismo** (la misma que acepte para G2): declarar por escrito, en
el fichero de tarea, que la superficie cubierta es *"invocaciones cuyo argumento nombra la ruta
relativa al RAIZ del repositorio en el texto del `run`"*, y que `working-directory`, `cd`, globs y
rutas compuestas por variable quedan **fuera**. Y en ese caso hay que **corregir una frase que hoy
es falsa** tal como esta escrita:

    "Las formas que el tokenizador no entienda quedan en postura fail-closed"

Las doce formas de la seccion 4 son formas que el tokenizador no entiende y **no** quedan
fail-closed. La clausula que la salva ("porque el fichero nombrado permanece en la poblacion
derivada") solo se cumple si la ruta esta nombrada, y esa condicion no aparece en la frase.

## 9. Recomendacion de cierre

**CHANGE-REQUIRED**, y **escalo al operador humano** en lugar de pedir vuelta 3, como fijaba el
presupuesto. Escalo, no bloqueo: la decision de gastar una tercera vuelta no es mia, y le doy al
operador los tres datos que necesita para tomarla:

1. **El avance es real y grande.** El criterio SI se deriva; el literal murio; 14 de 14 escapes de
   r4 murieron sin anadir una sola forma al reconocedor. Esto no es la enumeracion con otro nombre.
2. **Queda una clase abierta y con instancia disponible hoy.** No hay `working-directory` ni
   `cd`+`python` en el workflow actual --lo comprobe-- asi que **el arbol de hoy no esta roto**;
   pero cualquiera de las 73 invocaciones vivas puede ocultarse con dos lineas y llevarse por
   delante su declaracion de dependencias (B2/B3, medido de punta a punta).
3. **El cierre cuesta una linea** con cero falsos rojos medidos, o cuesta **una frase** si se elige
   la salida declarativa. No es una vuelta cara en ninguna de las dos ramas.

Y el dato que mas pesa para decidir: **el defecto que reporto lo escribi yo en r4**. Si el operador
juzga que dos vueltas de checker que heredan el mismo punto ciego son suficientes, la salida
declarativa cierra la tarea hoy sin mecanismo nuevo, y la clase se abre como tarea aparte con la
propiedad bien nombrada. Yo no cierro, no promuevo y no ratifico: entrego el veredicto.

### Puertas afectadas y ciclo si el operador autoriza la remediacion

Puertas: `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`, `check_falsification_contracts.py --inventory`, mas el propio
gate bajo un interprete con **solo** lo que declara cada job.

Ciclo: una unica iteracion, re-juicio mio antes del commit de cierre, y se falsa con esta bateria
exacta -- las 12 filas SILENT de la seccion 4 y las dos cadenas B2/B3 de la seccion 5 deben pasar a
EXIT=1, y el arbol intacto debe seguir en EXIT=0 con `invocations=73 referenced=72`. Si esa
remediacion vuelve a dejar la clase abierta, no pido otra: la tarea se cierra por declaracion.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `90fa8ffa48ea7722679aca3d0c5a12d019d2b2e4`, `origin/main` `f65440d9`.
Alcance: solo el hub, sin producto en alcance.
