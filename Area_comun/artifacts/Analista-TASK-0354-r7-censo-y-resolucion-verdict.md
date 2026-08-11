# VEREDICTO TASK-0354 r7 -- el enunciado corregido tiene una condicion de menos y un cardinal que no re-deriva

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354
    instruccion         Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-texto.md
    escrito             2026-08-12 01:48 local (UTC+2)  ==  2026-08-11T23:48Z
    veredicto           CHANGE-REQUIRED  --  DECLARATIVO otra vez, cero mecanismo
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           2 de 2 del ciclo declarativo que firme en r6; una tercera va al operador humano

## 0. Ancla canonica

    implementacion            cf918584f30fce9044dde99de1c7fadff879703b   (sin cambios, el YAML no se toco)
    texto bajo revision       Area_comun/tasks/TASK-0354-*.md lineas 124-154 en 0b130fa9
    origin/main               0b130fa9b3613a66adbd78e4671d93cb131dc90d
    ancestro                  git merge-base --is-ancestor cf918584 origin/main  -> SI

La instruccion pide juzgar solo el texto. Lo hago, pero un texto que afirma comportamiento se juzga
contra el comportamiento: he vuelto a medir unicamente las direcciones en las que el enunciado nuevo
afirma algo, no el mecanismo entero.

## 1. Reproduccion -- clones limpios, gate extraido con parser independiente, exit codes reales

Dos clones `--shared --no-hardlinks` con historia completa bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/an0354r7/` (DECISION-0104), nunca en el arbol gobernado:

    c1  @ cf918584   (medicion; `git status --short` vacio)
    c2  @ cf918584   (mutantes; workflow restaurado y verificado sha256 f2d1e8a3... al terminar)

El gate lo extraje del YAML con PyYAML localizando el paso por `name` y quitando solo el envoltorio
`python - <<'PY'` / `PY` (130 lineas). Nunca copy-paste.

    c1 intacto, gate de cf918584     WORKFLOW_RUNNER_DEPENDENCIES PASS invocations=73 referenced=72   EXIT=0
    c2 intacto, gate de cf918584     identico                                                          EXIT=0

Puertas de protocolo sobre el arbol que firmo:

    python scripts/validate_collaboration_state.py            EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                  EXIT=0
    python scripts/scan_domain_neutrality.py --root .         EXIT=0
    python runtime/protocol_replay.py --check-drift --root .  EXIT=0  verdict=CLEAN up_to_seq=8889

## 2. Lo que el texto nuevo acierta, y lo digo primero porque es verdad

El parrafo corregido hace lo que pedi: retira los tres ejemplos, nombra una propiedad en vez de una
lista, trae el censo, trae B4/B5/B6 con el control B0, declara que el arbol de hoy no esta roto y
recoge el residual que me atribui. TASK-0363 recoge la clase con un AC3 que exige composicion, que es
donde vivia el escape. Verificado uno a uno en el ancla:

    afirmacion del texto                                  mi medicion en cf918584                   veredicto
    ----------------------------------------------------- ----------------------------------------- ---------
    cero `working-directory:` en el workflow               0 pasos                                   CONFIRMA
    cero `cd ` en bloques `run`                            0 lineas                                  CONFIRMA
    cero banderas entre `python` y el script               0 lineas                                  CONFIRMA
    N2 `cd <dir> && python <base>`      EXIT=1             EXIT=1                                    CONFIRMA
    F1 `cd <dir> && python -u <base>`   EXIT=0             EXIT=0                                    CONFIRMA
    B0 control (quito pyyaml sin ocultar)  gate FAIL       EXIT=1                                    CONFIRMA
    B5 `cd + python -m <mod>` + sin pyyaml gate PASS       EXIT=0 invocations=72                     CONFIRMA
    el YAML no se toco                                     diff vacio contra cf918584                CONFIRMA

## 3. La respuesta a tu pregunta: NO. Se queda corto en una direccion, y el cardinal no re-deriva

Bateria sobre el mismo runner real de la seccion 5 de r6
(`examples/neutrality_scan_cases/run_powershell_host_cases.py`, importa `yaml`, job
`powershell-linux-parity` que declara exactamente `pyyaml`). Un mutante por vez, restaurando entre
medias, gate por exit code:

    id  vector                                        EXIT  la puerta dice
    --- --------------------------------------------- ----- --------------------------------------------------
    B0  arbol intacto                                   0   PASS invocations=73 referenced=72
    V1  cd <dir> && python <base>                       1   FAIL: python script target is not a repository file
    V2  cd <dir> && python -m <base>                    0   PASS invocations=72 referenced=71
    V3  python -m examples.neutrality...host_cases      0   PASS invocations=73 referenced=72   (DESCUBIERTA)
    V4  python -m no_such_module_xyz                    0   PASS invocations=72 referenced=71
    V5  python no_such_script_xyz.py                    1   FAIL: python script target is not a repository file
    V6  python "$RUNNER_TEMP/generated.py"              1   FAIL: python script target is not a repository file
    V7  python -m generated                             0   PASS invocations=72 referenced=71
    V8  bash -c "python <ruta completa>"                1   FAIL: Python file named in run block was not discovered
    --- --------------------------------------------- ----- --------------------------------------------------
    W0  arbol intacto            + SIN pyyaml           1   FAIL: ... imports yaml; requires ['pyyaml']
    W1  cd + python -m <base>    + SIN pyyaml           0   PASS invocations=72     (el runner muere)
    W2  python -m <ruta punteada>+ SIN pyyaml           1   FAIL: ... imports yaml; requires ['pyyaml']

### 3.1 [BLOQUEA] Falta la SEGUNDA condicion: el objetivo tiene que resolver contra la RAIZ

El enunciado dice que la puerta descubre la invocacion **si** el token inmediatamente posterior a
`python` es el objetivo, `.py` o `-m modulo`. En V2, V3, V4 y V7 el token inmediatamente posterior a
`python` es `-m <objetivo>` en los cuatro. Solo V3 se descubre. La diferencia no es el token: es que
`examples.neutrality_scan_cases.run_powershell_host_cases` resuelve a un fichero **relativo a la raiz
del repositorio** y `run_powershell_host_cases` (tras el `cd`) no. La puerta no modela el directorio
de trabajo: hace `(root / token).resolve()` y nada mas.

W1 contra W2 lo pone en consecuencias, mismo runner y misma dependencia quitada: la forma que resuelve
desde la raiz enrojece, la que depende del `cd` pasa en verde mientras el runner muere en
`ModuleNotFoundError`. Un lector que aplique el enunciado tal como esta escrito predice que B5 se
atrapa. La fila B5, tres lineas mas abajo en el mismo fichero, dice PASS. El texto se contradice con
su propia tabla.

### 3.2 [BLOQUEA] Cuando NO resuelve, las dos formas fallan en direcciones OPUESTAS, y solo una esta escrita

    objetivo que no resuelve       forma script  ->  V5, V6   EXIT=1   fail-closed, enrojece
    objetivo que no resuelve       forma modulo  ->  V4, V7   EXIT=0   se descarta EN SILENCIO

El fichero ya declara la mitad buena en la linea 121 ("una forma script descubierta cuyo token no
resuelva a un fichero del repositorio queda en postura fail-closed"). La mitad mala no esta en ningun
sitio. Y no es simetria academica: el parrafo del residual (lineas 151-154) avisa de que la reparacion
natural del falso rojo de `$RUNNER_TEMP` "empujaria esas invocaciones a la clase silenciosa". **Esa
reparacion ya existe medida dentro del mismo gate**: V6 y V7 son el mismo objetivo fuera del
repositorio, uno enrojece por script y el otro calla por modulo. La rama de modulo *es* la version
reparada-y-muda del residual, hoy, en cf918584. Eso es la evidencia mas fuerte que tiene el AC4 de
TASK-0363 y no esta escrita en ninguna de las dos tareas.

### 3.3 [BLOQUEA] La segunda clausula del enunciado es falsa tal como esta escrita

El texto dice: "y solo enrojece si la ruta relativa a la raiz aparece **literal** en el mismo `run`".
V1 es la propia fila N2 del fichero, la que el texto llama "atrapada": su `run` es
`cd <dir> && python run_powershell_host_cases.py`, donde la ruta relativa a la raiz **no aparece** en
ninguna parte -- el `cd` la parte en dos. Y enrojece igual. Hay **dos** ramas de rojo, no una:

    rama A (fail-closed)   "python script target is not a repository file"          V1, V5, V6
    rama B (ruta literal)  "Python file named in run block was not discovered"      V8

El enunciado nombra solo la rama B. Con ello el propio ejemplo N2 que encabeza el parrafo queda sin
explicacion, y peor: llamar "atrapada" a N2 sugiere que la puerta vio la invocacion. No la vio.
Rechazo un token que no resolvia. La puerta no supo nunca que ahi habia un runner.

Conviene decirlo claro: **esa clausula tambien es mia**. La escribi en la seccion 6 de r6 y el
Arquitecto la transcribio fielmente. Los tres bloqueos de esta vuelta corrigen mi propia formulacion,
no la redaccion de quien la copio. Lo que cambio no es la opinion: es que en r6 mire la direccion
"que se escapa" y no mire la direccion "por que enrojece lo que enrojece".

Precision menor, no bloquea: "literal" es mas estricto que el mecanismo. El matcher normaliza `\` a
`/` y tolera un `./` delante (por eso W0 imprime la ruta con barras invertidas y por eso J2 de r6
enrojecia con `./`). Falla del lado seguro; solo conviene no prometer literalidad exacta.

### 3.4 [BLOQUEA] El censo "69 de 69" no re-deriva. Y el 69 es MIO

El texto afirma "tomando los **69** pasos `run: python <ruta>.py` del workflow ... 69 silenciosas y
0 atrapadas". Recontado en cf918584 con PyYAML sobre el documento:

    lineas `python <ruta>.py` exactas (sin argumentos)                        66
    pasos de UNA linea con esa forma                                          64
    pasos que contienen al menos una de esas lineas                           65
    lineas `python <ruta>.py [argumentos]`                                    72
    lineas `python ...` de cualquier forma                                    76
    lineas `python -m <mod>`                                                   3

**69 no sale de ningun criterio que yo sepa enunciar.** El numero salio de mi veredicto r6 y el
Arquitecto lo transcribio de buena fe; la correccion es mia, no del que escribio el parrafo. Importa
porque el AC1 de TASK-0363 exige "el conteo completo sobre la poblacion DERIVADA del workflow y no
sobre una lista de formas elegidas a mano" y luego lo ancla a "hoy ese conteo es 69 de 69": un AC de
falsacion clavado a un cardinal que no se puede reproducir es infalsable, que es exactamente el
defecto que el AC existe para prohibir.

Rehice el censo entero con la poblacion derivada -- toda linea de un bloque `run` que invoque
`python <ruta>.py [argumentos]` con `<ruta>` resolviendo a un fichero del repositorio y con
componente de directorio -- aplicando uno a uno, y restaurando entre medias, la reescritura mecanica
`python <dir>/<base> [args]` -> `cd <dir> && python -u <base> [args]`:

    poblacion derivada                        72   (66 sin argumentos + 6 con argumentos)
    SILENT tras la reescritura (gate EXIT=0)  72
    CAUGHT tras la reescritura (gate EXIT=1)   0

El numero honesto es **72 de 72**, y tiene la virtud de coincidir con el `referenced=72` que el propio
gate imprime en verde: la poblacion ocultable es la poblacion entera que la puerta dice cubrir. La
propiedad no se debilita, se refuerza.

## 4. La redaccion que si describe lo que medi

Sustituir el bloque citado por esto (es texto, no mecanismo; el YAML sigue sin tocarse):

> La puerta descubre una invocacion solo si se cumplen **dos** condiciones a la vez: (1) el token
> inmediatamente posterior a `python` es el propio objetivo -- una ruta terminada en `.py`, o
> `-m <modulo>`; y (2) ese objetivo, **tal como esta escrito, resuelve a un fichero existente relativo
> a la raiz del repositorio**, porque la puerta no modela el directorio de trabajo. Si falla (1) -- una
> bandera, un `-c`, un envoltorio, un token compuesto -- la invocacion queda invisible y solo enrojece
> si la ruta relativa a la raiz aparece escrita en el mismo `run` (con `\` normalizado a `/` y un `./`
> opcional). Si falla (2), las dos formas fallan en direcciones **opuestas**: una forma script queda
> fail-closed y enrojece; una forma `-m <modulo>` se descarta **en silencio** y el bloque queda verde.

Y en el censo, `69` -> `72` (poblacion derivada, 72 silenciosas y 0 atrapadas), en TASK-0354 y en el
AC1/goal de TASK-0363. En el residual de `$RUNNER_TEMP` conviene anadir una linea: la reparacion
"natural" que se teme ya existe medida en la rama de modulo del mismo gate (`python -m generated`
pasa en verde donde `python "$RUNNER_TEMP/generated.py"` enrojece).

## 5. Residuales

**5.1** No re-medi el mecanismo: la bateria toca solo las direcciones que el enunciado nuevo afirma.
El balance 9+3 de r6 y las puertas de r5 siguen como estaban; nada de esto los revisa.

**5.2** Siguen abiertos y sin re-medir en este ancla: G3 (`if: false` sobre el paso de instalacion deja
`PASS`), 7.3 (asimetria de `declared_distributions`, anclada a `parts[:4] == ["python","-m","pip","install"]`),
7.1 (23 pares de sufijo), G4 (superficie `.ps1` por declaracion y no por mecanismo), G2 (clausura
transitiva de imports, fuera por declaracion).

**5.3 Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate nunca ha
corrido en GitHub Actions.

**5.4** Mis mutantes vivieron solo en el clon `c2`. El workflow quedo restaurado y verificado por
sha256 identico al de `cf918584`. Cero escritura en el arbol gobernado salvo este veredicto y su
mensaje.

## 6. Recomendacion de cierre

**CHANGE-REQUIRED, declarativo, y es la segunda de las dos vueltas que yo mismo acote.** No pido
mecanismo, no reabro `cf918584` y no cambio de opinion sobre el balance 9+3: sigue verificado y sigue
siendo una remediacion limpia. Lo que bloquea es lo mismo que en r6, un escalon mas abajo: el
enunciado nombra **una** condicion cuando el mecanismo aplica **dos**, y silencia que el fallo de la
segunda tiene dos direcciones opuestas -- justo la asimetria que sostiene el residual que la propia
tarea declara. Mas un cardinal, el 69, que no re-deriva y que ya se propago a un AC de falsacion.

Con la seccion 4 aplicada el cierre es honesto y TASK-0363 hereda su AC4 con la evidencia que le
faltaba.

### Ciclo de la remediacion declarativa

    remediacion    seccion 4 en Area_comun/tasks/TASK-0354-*.md y el cardinal en TASK-0363 (goal + AC1).
                   Cero cambios en .github/workflows/validate.yml y cero cambios en el YAML de intake.
    puertas        validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py,
                   protocol_replay.py --check-drift   (todas EXIT=0 antes del commit de cierre)
    re-juicio      mio, sobre el texto, antes del commit de cierre; no re-mido mecanismo
    iteraciones    esta es la 2 de 2. Si hiciera falta una tercera, va al operador humano y no la
                   resuelvo yo: seria senal de que el defecto no esta en la redaccion.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Ancla `cf918584f30fce9044dde99de1c7fadff879703b`, texto en `0b130fa9`.
Alcance: solo el hub, sin producto en alcance.
