# VEREDICTO TASK-0354 r6 -- la puerta solo ve el token que va pegado al interprete

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-r6.md
    escrito             2026-08-12 01:03 local (UTC+2)  ==  2026-08-11T23:03Z
    veredicto           CHANGE-REQUIRED  --  SOLO DECLARATIVO, no pido cuarta vuelta de mecanismo
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           vuelta 1 de 1 de la autorizacion del operador

## 0. Ancla canonica

    implementacion            cf918584f30fce9044dde99de1c7fadff879703b
    control pre-fix           90fa8ffa48ea7722679aca3d0c5a12d019d2b2e4
    origin/main               39e73411 al empezar; 567447dd al firmar (avanzo durante la review,
                              solo Area_comun/tasks/TASK-0359-*.md, sin tocar nada de esta revision)
    ancestro                  git merge-base --is-ancestor cf918584 origin/main  -> SI

Juzgo en `cf918584`, nunca en el arbol caliente (que hoy tiene ficheros sin commitear de otros
participantes; rutas ajenas que no toco).

## 1. Reproduccion -- clones limpios, interprete fiel, gate por exit code

Dos clones `--shared --no-hardlinks` con historia completa bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/an0354r6/` (DECISION-0104), nunca en el arbol gobernado:

    c1  @ cf918584   (medicion; `git status --short` vacio)
    c2  @ cf918584   (mutantes; workflow verificado byte-identico contra cf918584 al terminar)

Interpretes: el mismo par de r5. `venvjob` = 3.12.10 con exactamente `cryptography jsonschema
pyyaml` y transitivas (el interprete del job `validate`, que es de donde este gate lee
`packages_distributions()`); `venvbare` = venv vacio, que representa a los jobs que no declaran nada.

Puertas de protocolo en `c1`, gateadas por `$?` real, jamas detras de un pipe:

    python scripts/validate_collaboration_state.py --root .        EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                       EXIT=0  OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .              EXIT=0
    python runtime/protocol_replay.py --check-drift --root .       EXIT=0  verdict=CLEAN up_to_seq=8872
    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      EXIT=0

El gate bajo revision lo extraje del YAML con un **parser independiente** (PyYAML sobre el
documento, localizando el paso por `name`; no copy-paste), quitando solo el envoltorio
`python - <<'PY'` / `PY`. Lo mismo con el ancla pre-fix. Diff entre los dos cuerpos extraidos:

    -                     yield script                          +                     yield "script", script
    -                 yield module.replace(".", "/") + ".py"    +                 yield "module", module...
    -         for runner_token in python_runner_tokens(...)     +         for kind, runner_token in ...
                                                                +                 if kind == "script":
                                                                +                     errors.append(...)

Cuatro lineas. Es exactamente lo que recomende en r5 seccion 8, ni una mas.

    U0  c1 intacto, gate NUEVO       PASS invocations=73 referenced=72   EXIT=0
    U0  c1 intacto, gate PRE-FIX     PASS invocations=73 referenced=72   EXIT=0

## 2. Lo que declara el maker -- verificado uno a uno, y sale entero

    afirmacion del maker                                       mi medicion                     veredicto
    ---------------------------------------------------------- ------------------------------- ---------
    pre-fix EXIT=0 en las CATORCE                              14/14 EXIT=0                    CONFIRMA
    nuevo EXIT=1 en N1 N11 N2 N13 N9 N6 N3 N4 N5 B2 B3         11/11 EXIT=1                    CONFIRMA
    supervivientes N8 ($BASE), N10 (find -exec), N14 (bash -c) 3/3 EXIT=0                      CONFIRMA
    arbol intacto EXIT=0, invocations=73 referenced=72         identico                        CONFIRMA
    el reconocedor NO se ensancho                              cero alternativas nuevas al     CONFIRMA
                                                               `re.fullmatch` del ejecutable
    los objetivos de modulo siguen exentos                     `-m pip` no enrojece            CONFIRMA
    puertas de protocolo verdes, drift limpio                  seccion 1                       CONFIRMA

El balance 9+3 que corrige la instruccion es el correcto y es el que mido. B0 (control: quitar
`pyyaml` **sin** ocultar la invocacion) sigue en `EXIT=1` en ambos gates: la puerta funciona cuando ve.

Y una cosa mas, que digo antes que lo malo porque es verdad: **el cambio no introduce ni un solo
falso rojo sobre el arbol vivo**, no revierte nada de r5, y mata once escapes reales con cuatro
lineas. Es una remediacion limpia. El problema no esta en lo que hizo.

## 3. La pregunta de la instruccion -- NO, los tres no son los unicos que quedan

Bateria en direccion ALTA sobre el mismo probe real de r5
(`examples/probe_cases/run_probe_cases.py`, unico import `attrs`), por rutas que **no** son `$BASE`
compuesto, **no** son `find -exec` y **no** son `bash -c`:

    vector                                              PRE-FIX   NUEVO   la puerta dice
    --------------------------------------------------- -------   -----   ---------------------------
    F1  cd <dir> && python -u <base>                        0        0     PASS invocations=73
    F2  working-directory + python -X utf8 <base>           0        0     PASS invocations=73
    F3  cd <dir> && python -W ignore <base>                 0        0     PASS invocations=73
    F4  cd <dir> && python3 -u <base>                       0        0     PASS invocations=73
    F5  working-directory + python -u <base>  (job WIN)     0        0     PASS invocations=73
    F6  cd <dir> && python -B -u <base>                     0        0     PASS invocations=73
    K2  cd <dir> && python -u ./<base>                      0        0     PASS invocations=73
    G1  cd <dir> && python -m <mod>                         0        0     PASS invocations=73
    G2  working-directory + python -m <mod>                 0        0     PASS invocations=73
    H1  cd <dir>;python <base>      (sin espacio)           0        0     PASS invocations=73
    I1  cd <dir> && python -c "import <mod>"                0        0     PASS invocations=73
    J1  cd <dir> && ./<base>        (shebang)               0        0     PASS invocations=73
    --------------------------------------------------- -------   -----   ---------------------------
    K1  cd <dir> && env python <base>                       0        1     CAUGHT (nueva)
    J2  ./<ruta completa>           (shebang)               1        1     CAUGHT (ruta literal)

Doce filas SILENT que no estan declaradas. La cabeza de la lista, **F1, es un solo caracter de
distancia de N2**, que si muere: `cd <dir> && python <base>` enrojece y `cd <dir> && python -u
<base>` no. `-u` es la bandera mas comun en CI de Python (salida sin bufferizar para ver el log en
vivo). La instruccion pedia literalmente que el veredicto no dependiera de "orden de flags". Depende.

**Ejecutan de verdad**, no solo parecen validas (medido en `c2`, salida real):

    cd examples/probe_cases && python -u run_probe_cases.py     venvjob  -> "probe attrs"          EXIT=0
                                                                venvbare -> ModuleNotFoundError    EXIT=1
    cd examples/probe_cases && python -m run_probe_cases        venvjob  -> "probe attrs"          EXIT=0
                                                                venvbare -> ModuleNotFoundError    EXIT=1
    cd examples/probe_cases && python -c "import run_probe..."  venvjob  -> "probe attrs"          EXIT=0
    cd examples/probe_cases;python run_probe_cases.py           venvjob  -> "probe attrs"          EXIT=0

J1 (shebang) queda SILENT en la puerta pero **su comportamiento no lo pude medir en este host**
(Windows, sin `python3` en PATH); dos de los tres jobs corren en `ubuntu-latest`, donde es idiom
corriente. Lo declaro como candidato no medido y no lo cuento entre los confirmados.

## 4. Censo, no anecdota: 69 de 69 invocaciones vivas se pueden ocultar

Que haya una forma que escapa importa poco si no hay nada que ocultar. Lo hay. Tome **todos** los
pasos del workflow de la forma `run: python <ruta>.py` (69 en `cf918584`), y para cada uno, uno a
uno y restaurando entre medias, aplique la reescritura mecanica
`python <dir>/<base>` -> `cd <dir> && python -u <base>`:

    pasos single-line `run: python <ruta>.py`     69
    SILENT tras la reescritura (gate EXIT=0)      69
    CAUGHT tras la reescritura                     0

Ni uno se salva. El contador cae de 73 a 72 sin una senal.

## 5. La direccion B: el defecto original de TASK-0354 vuelve entero, sobre un runner REAL

`examples/neutrality_scan_cases/run_powershell_host_cases.py` importa `yaml` y vive en el job
`powershell-linux-parity`, que declara exactamente `pyyaml`. Reescribo su invocacion y quito
`pyyaml` de la linea de instalacion de ESE job:

    B4  working-directory: <dir>  +  python -u <base>   +  sin pyyaml
        gate           -> WORKFLOW_RUNNER_DEPENDENCIES PASS invocations=72 referenced=71   EXIT=0
        comportamiento -> ModuleNotFoundError: No module named 'yaml'                      EXIT=1

    B5  cd <dir> && python -m <mod>                     +  sin pyyaml
        gate           -> PASS invocations=72 referenced=71                                EXIT=0
        comportamiento -> ModuleNotFoundError: No module named 'yaml'                      EXIT=1

    B6  cd <dir> && python -u <base>                    +  sin pyyaml
        gate           -> PASS invocations=72 referenced=71                                EXIT=0
        comportamiento -> ModuleNotFoundError: No module named 'yaml'                      EXIT=1

    B0  control: quito pyyaml SIN ocultar la invocacion
        gate           -> FAIL                                                             EXIT=1

Esto es exactamente B2/B3 de r5 con una bandera de mas. La puerta que existe para impedir que un
runner entre en CI sin su dependencia dice PASS mientras el runner muere en el import, y la
coordenada que lo consigue no toca el runner: son dos lineas del YAML.

## 6. El criterio real de la puerta, escrito como propiedad

Lo que el mecanismo implementa hoy, dicho sin adornos y comprobado con las catorce filas de arriba:

> La puerta descubre una invocacion **solo si el token que va inmediatamente despues del ejecutable
> `python` es el propio objetivo** -- una ruta terminada en `.py`, o `-m <modulo>`. Cualquier cosa
> que ocupe esa posicion (una bandera `-u`/`-X`/`-W`/`-B`, un `-c`, un envoltorio `bash -c` o
> `find -exec`, un token compuesto o con variable) deja la invocacion **invisible**. Una invocacion
> invisible solo enrojece si la ruta relativa a la RAIZ del repositorio aparece escrita literalmente
> en el texto del mismo `run`.

Son **dos** condiciones de forma, no una, y la segunda es la que sostiene todo lo demas. La
remediacion de `cf918584` cierra el caso "el token pegado al interprete es una ruta `.py` que no
resuelve". No toca el caso "el token pegado al interprete no es el objetivo".

## 7. Por que esto invalida la declaracion, y solo la declaracion

El fichero de tarea dice hoy:

    "La cobertura no alcanza tokens compuestos que no presentan una ruta .py al analizador:
     $BASE compuesto, find -exec y bash -c sobreviven y quedan declarados como residual."

Dos problemas medibles:

1. `-u run_probe_cases.py` **no es un token compuesto**. El criterio escrito no lo describe, asi que
   la frase no lo cubre ni por lectura generosa.
2. Los tres ejemplos van detras de dos puntos y se leen como la lista completa. Un lector concluye
   que quedan tres. Quedan al menos cuatro familias (bandera, `-m` tras cambio de cwd, separador sin
   espacio, `-c`), y J1 posiblemente una quinta.

Es el patron que ya nombre dos veces en esta tarea: **una enumeracion vestida de criterio**. La
diferencia con r4 y r5 es que ahora el enunciado del residual es lo unico que falla; el mecanismo
entregado hace lo que dice que hace.

## 8. Residuales

**8.1 NUEVO, coste de mi propia recomendacion de r5.** La rama de error que propuse enrojece
tambien invocaciones legitimas cuyo objetivo **no es** del repositorio:

    python "$RUNNER_TEMP/generated.py"     PRE-FIX EXIT=0   NUEVO EXIT=1 (falso rojo)
    python /tmp/generated.py               PRE-FIX EXIT=0   NUEVO EXIT=1 (falso rojo)

No hay ninguno en el arbol de hoy (U0 verde), es fail-closed y por tanto seguro. Pero su reparacion
"natural" para un maker apurado es reescribir la invocacion en una forma que el analizador no
tokenice -- es decir, empujarla justo a la clase silenciosa de la seccion 3. Es el molde del
auto-desarme otra vez, en version pequena. En r5 solo medi "arbol intacto, cero falsos rojos" y no
medi este caso; lo declaro yo, no el maker.

**8.2 El arbol de hoy NO esta roto.** Cero `working-directory:`, cero `cd ` en bloques `run`, cero
banderas entre `python` y el script en `cf918584`. Lo comprobe. El riesgo es futuro, no presente.

**8.3 G3 sigue abierto** (un `if: false` sobre el paso de instalacion deja `PASS`), **7.3** la
asimetria descubrimiento/declaracion sigue (`declared_distributions` anclada a
`parts[:4] == ["python","-m","pip","install"]`), **7.1** los 23 pares de sufijo siguen, **G4** la
superficie `.ps1` sigue cubierta por declaracion y no por mecanismo, **G2** la clausura transitiva
de imports sigue explicitamente fuera. No los re-medi todos en este ancla; no estaban en alcance.

**8.4 Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate nunca
ha corrido en GitHub Actions.

**8.5 El replicador.** `scripts/replay_validate_job.py --root .` corrio en `c1` y su paso 03
("Verify workflow runner dependency declarations") sale `PASS exit=0`. No espere a los 78 pasos; el
saldo completo del replicador no forma parte de esta vuelta y sigue como residual de r5 7.6.

**8.6 Mi probe es sintetico** y vivio solo en el clon de mutantes `c2`, jamas en el arbol
gobernado. El workflow de `c2` quedo restaurado y verificado byte-identico contra `cf918584`.

## 9. Recomendacion de cierre

**CHANGE-REQUIRED, y de un solo tipo: declarativo.** No pido una cuarta vuelta de mecanismo, y lo
digo porque lo firme en r5: *"si esa remediacion vuelve a dejar la clase abierta, no pido otra: la
tarea se cierra por declaracion"*. La clase sigue abierta y sostengo mi palabra.

Lo unico que bloquea el cierre es que **el residual escrito hoy afirma una cobertura que la medicion
refuta**. La remediacion es un parrafo en el fichero de tarea, sin tocar el YAML, sustituyendo los
tres ejemplos por la propiedad de la seccion 6 y anadiendo el censo de la seccion 4 (69 de 69
ocultables, con B4/B5/B6 medido de punta a punta). Con esa frase corregida el cierre es honesto:
declara lo que la puerta hace y lo que no, y el siguiente que la lea no descubre por accidente que
la lista tenia mas elementos.

Y **escalo al operador humano** el hecho de fondo, sin pedirle nada: la clase "el token pegado al
interprete no es el objetivo" queda abierta tras tres remediaciones, y su cierre real no cabe en el
tokenizador -- pide otro mecanismo (derivar la invocacion del comando ejecutado, no de su texto) y
por tanto otra tarea. Esa decision no es mia.

### Ciclo de la remediacion declarativa

    remediacion    1 parrafo en Area_comun/tasks/TASK-0354-*.md (residual G1), cero cambios en el YAML
    puertas        validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py,
                   protocol_replay.py --check-drift  (todas EXIT=0 antes del commit de cierre)
    re-juicio      mio, sobre el texto, antes del commit de cierre; no re-mido mecanismo
    iteraciones    1, maximo 2; a la tercera vuelve al operador humano

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `cf918584f30fce9044dde99de1c7fadff879703b`, `origin/main` `567447dd` al firmar.
Alcance: solo el hub, sin producto en alcance.
