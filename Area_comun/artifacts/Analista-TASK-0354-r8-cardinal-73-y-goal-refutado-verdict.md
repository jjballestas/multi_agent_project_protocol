# VEREDICTO TASK-0354 r8 -- el cardinal corregido tampoco re-deriva, y el goal de 0363 sigue diciendo lo refutado

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354  (+ intake de TASK-0363, que la instruccion mete en alcance)
    instruccion         Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-texto-r2.md
    escrito             2026-08-12 02:15 local (UTC+2)  ==  2026-08-12T00:15Z
    veredicto           CHANGE-REQUIRED  --  declarativo, cero mecanismo  +  ESCALA AL OPERADOR
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           3 de un ciclo que yo mismo acote en 2; por eso escala, y digo por que

## 0. Ancla canonica

    texto bajo revision       665d00fb  (== origin/main == HEAD en el momento de escribir)
    implementacion            cf918584f30fce9044dde99de1c7fadff879703b
    YAML del workflow         git diff cf918584 665d00fb -- .github/workflows/validate.yml  ->  VACIO
    sha256 del workflow       f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e

El mecanismo no se toco: lo confirmo por diff vacio y por sha256, no por la palabra de nadie.
Sigo juzgando texto -- pero un texto que publica cardinales se juzga recontando los cardinales.

## 1. Reproduccion -- clon limpio, gate extraido con parser independiente, exit codes reales

Clon `git clone -s` con historia completa bajo el scratch root declarado
`D:/Aegis_Scratch/mapp/t354r8/` (DECISION-0104), nunca en el arbol gobernado. Checkout `665d00fb`.
El gate lo extraje del YAML con PyYAML localizando el paso por indice y quitando solo el envoltorio
`python - <<'PY'` / `PY` (130 lineas). Nunca copy-paste. Mutantes uno a uno, restaurando entre medias;
`git status --short` vacio y sha256 identico al terminar.

    gate, arbol intacto                                       WORKFLOW_RUNNER_DEPENDENCIES PASS
                                                              invocations=73 referenced=72     EXIT=0
    python scripts/validate_collaboration_state.py --root .   EXIT=0  OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                  EXIT=0  OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .         EXIT=0
    python runtime/protocol_replay.py --check-drift --root .  EXIT=0  verdict=CLEAN up_to_seq=8896

## 2. Lo que la vuelta 2 acierta, y lo digo primero porque es verdad y es la mayor parte

La seccion 4 de r7 esta transcrita **literal** en TASK-0354. Las dos condiciones, las dos direcciones
opuestas, el `\` normalizado y el `./` opcional: todo. N2 deja de llamarse "atrapada" ahi. El residual
de `$RUNNER_TEMP` ya lleva su evidencia. Y elegir AC propio para la mitad de modulo en vez de enterrarla
como evidencia del AC4 es la decision correcta por la razon correcta.

Verificado uno a uno contra el mecanismo, no contra la memoria:

    afirmacion del texto de 665d00fb                       mi medicion en el clon limpio        veredicto
    ------------------------------------------------------ ------------------------------------ ---------
    condicion (1) token pegado a python == objetivo         asi lo hace python_runner_tokens     CONFIRMA
    condicion (2) resuelve contra la RAIZ                   (root / token).resolve().is_file()   CONFIRMA
    falla (1) -> invisible; enrojece si la ruta esta escrita rama expected-discovered            CONFIRMA
    falla (2) forma script -> fail-closed, enrojece         D6 EXIT=1                            CONFIRMA
    falla (2) forma modulo -> silencio, verde               D7 EXIT=0                            CONFIRMA
    `python -m generated` verde vs `$RUNNER_TEMP` rojo      D7 EXIT=0 / D6 EXIT=1                CONFIRMA
    cero `working-directory:` en el workflow                0 pasos                              CONFIRMA
    cero `cd ` en bloques `run`                             0 lineas                             CONFIRMA
    cero banderas entre `python` y el script                0 lineas                             CONFIRMA
    "66 lineas `python <ruta>.py` exactas"                  66                                   CONFIRMA
    "64 pasos de una linea"                                 64                                   CONFIRMA
    "72 con argumentos"                                     72                                   CONFIRMA
    "76 lineas `python` cualesquiera"                       76                                   CONFIRMA
    el YAML no se toco                                      diff vacio + sha256 identico         CONFIRMA

Los cuatro cardinales que el texto usa **para demostrar que el 69 no re-derivaba** re-derivan clavados.
La demolicion del 69 es correcta. El problema esta en lo que se puso en su lugar.

## 3. [BLOQUEA] El 72 tampoco re-deriva, y su "coincidencia" con `referenced=72` es un accidente

El texto dice: *"**72 silenciosas y 0 atrapadas**, y 72 es exactamente el `referenced=72` que el gate
imprime en verde. La propiedad sale reforzada."* Recontado sobre el ancla, instrumentando el mismo
tokenizador del gate:

    invocaciones DESCUBIERTAS por la puerta                 73   (todas forma script, cero forma modulo)
    de esas, con componente de directorio (reescribibles)   73   (las 73; ninguna es `python foo.py` a pelo)
    ficheros DISTINTOS cubiertos (`referenced`)             72
    causa de la diferencia   scripts/validate_collaboration_state.py se invoca DOS veces

La poblacion reescribible es de **73 invocaciones**, no 72. El 72 sale de un criterio anclado a la
LINEA (`^python <ruta>.py [args]`) que se deja fuera, en silencio, la invocacion numero 73:

    if ! python scripts/prune_state.py --root . --check; then     <- descubierta, y la linea no empieza por python

Y la falsacion, con el gate por exit code (mutante unico, restaurando entre medias):

    id  mutante                                                        EXIT  la puerta dice
    --- --------------------------------------------------------------- ---- ---------------------------------
    M0  arbol intacto                                                     0   PASS invocations=73 referenced=72
    M1  esconde UNA de las dos invocaciones de validate_collaboration     0   PASS invocations=72 referenced=72
    M2  esconde LAS DOS                                                   0   PASS invocations=71 referenced=71
    M3  esconde la invocacion 73 (`if ! python scripts/prune_state.py`)   0   PASS invocations=72 referenced=71

**M3 mata el cardinal:** la invocacion 73 es ocultable, es silenciosa, y ocultarla **si** le quita la
cobertura a `scripts/prune_state.py` (`referenced` 72 -> 71). Pertenece a la poblacion y mi censo la
tiro por no empezar la linea con `python` -- es decir, la tire **enumerando una forma**, que es
exactamente el defecto que esta tarea existe para nombrar.

**M1 mata la equivalencia:** una invocacion puede volverse silenciosa **sin** que el fichero pierda
cobertura. Ocultar una sola de las dos invocaciones de `validate_collaboration_state.py` deja
`invocations=72 referenced=72`: la puerta la sigue cubriendo por la otra. Hacen falta las dos (M2).

De ahi que la frase que escribi en r7 -- *"la poblacion ocultable es la poblacion entera que la puerta
dice cubrir"* -- sea falsa: ocultar es **por invocacion** (73) y cubrir es **por fichero** (72), y
para un fichero hay que ocultar dos. Los dos 72 salen de dos off-by-one independientes:

    72 = 73 invocaciones - 1 invocacion que mi criterio de linea descarto
    72 = 73 invocaciones - 1 fichero duplicado

Mismo numero, criterios distintos, conjuntos distintos. El texto vende la coincidencia como
corroboracion ("la propiedad sale reforzada") y **AC1 de TASK-0363 la eleva a ancla de falsacion**:
*"Hoy ese conteo es 72 de 72, y 72 coincide con el `referenced` que el propio gate publica."* Quien
intente falsar ese AC recontara 73 invocaciones o 72 ficheros y no encontrara ningun criterio que
produzca "72 de 72 que coincide con referenced". Es el defecto del 69 un escalon mas arriba: no un
numero que no re-deriva, sino un numero que **parece** re-derivar porque casa con una salida publicada.

**Y el 72 es mio.** Lo publique en r7 y el Arquitecto lo transcribio bien. Es la tercera vuelta seguida
en que el cardinal defectuoso lo puso el verificador. La leccion que escribi tras r7 --
*un cardinal que publico se re-deriva o no se publica*-- la incumpli en el mismo veredicto que la
enunciaba: re-derive las cuatro cifras que refutaban el 69 y no re-derive el 72 con que lo sustitui.

## 4. [BLOQUEA] El `goal` de TASK-0363 sigue diciendo lo que este mismo commit declara refutado

La instruccion mete el intake de TASK-0363 en alcance, asi que esto no es scope creep. El `goal`, hoy,
en 665d00fb, empieza asi:

> "La puerta de dependencias del workflow solo descubre una invocacion si el token inmediatamente
> posterior a `python` es el propio objetivo (`.py` o `-m modulo`), **y solo enrojece si la ruta
> relativa a la raiz aparece literal en el mismo `run`**."

Es la formulacion de UNA condicion, palabra por palabra, la que TASK-0354 declara erronea tres ficheros
mas alla en el mismo commit ("*la primera correccion nombro **una** condicion cuando el mecanismo
aplica **dos**"*). Se corrigio el cardinal en el goal y se dejo la propiedad.

Y no es una asimetria estetica: **el commit introduce con ello una contradiccion interna en TASK-0363**,
porque el AC5 que anade esta vuelta la refuta con su propio par de falsacion:

    D6   python "$RUNNER_TEMP/generated.py"    EXIT=1   FAIL: python script target is not a repository file
    D7   python -m generated                   EXIT=0   PASS

D6 enrojece **sin** que ninguna ruta relativa a la raiz aparezca en el `run`: enrojece por la rama
fail-closed, que el goal no admite. El goal dice "solo enrojece si..."; el AC5 del mismo fichero exhibe
un rojo que no cumple ese "si". Antes de este commit la contradiccion no existia (no habia AC5).

Ademas, en el cuerpo de TASK-0363 (linea 40) N2 **sigue** etiquetada `atrapada`, la etiqueta que este
mismo commit retira de TASK-0354 por enganosa. La correccion se aplico donde el revisor la cito, no
donde vive la afirmacion.

Menor, no bloquea por si solo pero viaja con el arreglo: el `goal` quedo con un empalme roto --
`"...(El cardinal 69 ... se retiro en r7.), con el runner real muriendo en ModuleNotFoundError..."` --
una subordinada huerfana colgando de un parentesis cerrado.

## 5. Tu pregunta: SI, queda una direccion sin nombrar -- y es un falso ROJO, no un silencio

Preguntas si queda alguna direccion de la cobertura sin nombrar. La hay, y esta en el lado del rojo:

    id  vector                                                                  EXIT  la puerta dice
    --- ----------------------------------------------------------------------- ---- --------------------------
    E0  control                                                                   0   PASS invocations=73
    E1  `python <gate> --root . --exclude scripts/prune_state.py`                 1   FAIL: Python file named in
                                                                                      run block was not discovered
    E2  `git add scripts/prune_state.py && python <gate> --root .`                1   idem

Una ruta `.py` **del repositorio** que aparece en un bloque `run` sin ser invocada -- como argumento
(`--exclude`, `--file`, `--config`) o nombrada por otra herramienta (`git add`, `cat`, `rm`) --
enrojece la puerta. No hay ninguna invocacion invisible que atrapar ahi: no hay invocacion en absoluto.

La frase de la propiedad la cubre por letra ("solo enrojece si la ruta ... aparece escrita en el mismo
`run`"), pero el parrafo la enmarca entera como el **rescate** de una invocacion que fallo la condicion
(1), y el inventario de falsos rojos del residual enumera solo `$RUNNER_TEMP` y `/tmp`. Esta clase no
esta en ese inventario y hoy el arbol no la ejerce, igual que no ejerce la de `$RUNNER_TEMP`. Es un
residual declarable, no una falsedad: por eso no la cuento como tercer bloqueo.

Descarto sin publicar dos sondas mas (`echo <ruta>` y comentario shell) porque mi inyeccion altero la
forma del escalar YAML y el resultado no era atribuible al mecanismo. E1 y E2 son sustituciones de una
linea por una linea, con el `run` efectivo impreso y verificado.

## 6. La redaccion que si describe lo que medi

Cardinal, en TASK-0354 y en el `goal`/AC1 de TASK-0363 -- anclado a las **dos** cifras que la propia
puerta publica, que es lo unico que re-deriva sin criterio inventado:

> **Censo con poblacion DERIVADA:** la poblacion son las **73** invocaciones que la propia puerta
> cuenta (`invocations=73`), todas de forma script y todas con componente de directorio. Aplicando la
> reescritura mecanica una a una: **73 silenciosas y 0 atrapadas**. La cobertura, en cambio, se cuenta
> por fichero: la puerta cubre **72** ficheros distintos (`referenced=72`), porque
> `scripts/validate_collaboration_state.py` se invoca dos veces. Los dos cardinales no son el mismo
> conjunto: ocultar una sola de esas dos invocaciones la vuelve silenciosa **sin** que el fichero pierda
> cobertura -- hacen falta las dos. (El 69 de la primera redaccion no re-derivaba; el 72 de la segunda
> tampoco: salia de un criterio anclado a la linea que descartaba la invocacion
> `if ! python scripts/prune_state.py ...`, y su coincidencia con `referenced=72` era accidental.)

Propiedad, en el `goal` de TASK-0363: sustituir la clausula de una condicion por la de dos, la misma
que ya esta en TASK-0354. Y en el cuerpo de TASK-0363, `atrapada` -> `rechaza el token: no resuelve;
no es que viera el runner`. Reparar el empalme roto del `goal`.

AC1 de TASK-0363: retirar "y 72 coincide con el `referenced` que el propio gate publica" y exigir en su
lugar que el conteo declare **que unidad cuenta** (invocaciones o ficheros) y que el criterio de
pertenencia no ancle en la forma de la linea.

Residual nuevo de la seccion 5: anadirlo al inventario de falsos rojos junto a `$RUNNER_TEMP`.

Cero cambios en `.github/workflows/validate.yml`. Nada de esto es mecanismo.

## 7. Residuales

**7.1** No re-medi el mecanismo entero: la bateria toca solo lo que el texto de 665d00fb afirma. El
balance 9+3 de r6 y las puertas de r5 siguen como estaban; nada de esto los revisa ni los reabre.

**7.2** Siguen abiertos y sin re-medir en este ancla: G3 (`if: false` sobre el paso de instalacion deja
`PASS`), 7.3 (asimetria de `declared_distributions`, anclada a `parts[:4] == ["python","-m","pip","install"]`),
7.1 (23 pares de sufijo), G4 (superficie `.ps1` por declaracion y no por mecanismo), G2 (clausura
transitiva de imports, fuera por declaracion).

**7.3 Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate nunca ha
corrido en GitHub Actions.

**7.4** Mis mutantes vivieron solo en el clon de scratch. El workflow quedo restaurado y verificado por
sha256 `f2d1e8a3...`, identico al de `cf918584`, y `git status --short` vacio. Cero escritura en el
arbol gobernado salvo este veredicto y su mensaje.

**7.5** No verifique invocacion a invocacion que las 73 sean silenciosas: verifique el control, la
invocacion 73 (M3) y el par duplicado (M1/M2), mas las 72 que r7 aplico una a una. La afirmacion
"73 silenciosas" hereda de r7 para 72 de ellas.

## 8. Recomendacion de cierre

**CHANGE-REQUIRED, declarativo, y ESCALA AL OPERADOR HUMANO.**

En r7 firme que la vuelta 2 era la ultima y que una tercera seria senal de que el defecto no esta en la
redaccion. Se cumplio, y la senal apunta a mi: en r6 publique un cardinal (69) sin re-derivarlo, en r7
publique su sustituto (72) sin re-derivarlo tampoco, y en las dos ocasiones el Arquitecto lo transcribio
con fidelidad. El defecto de esta cadena no esta en quien escribe el parrafo; esta en que el verificador
ha estado entregando numeros con la misma autoridad con la que exige que otros los re-deriven. Por eso
no me concedo yo la tercera vuelta: la pongo delante del operador.

Lo que someto a decision:

    A   aplicar la seccion 6 tal cual (es transcripcion, no redaccion: el texto exacto esta escrito
        arriba y los cardinales estan medidos en este veredicto) y cerrar TASK-0354 sin mas vueltas.
    B   cerrar TASK-0354 ya, con el cardinal actual, y llevarse la correccion entera a TASK-0363,
        que es donde el numero va a ejercer como criterio de falsacion.

Recomiendo **A**: TASK-0363 hereda el cardinal por su `goal` y su AC1, y arrastrar un cardinal roto a la
tarea que existe para prohibir cardinales rotos es el peor sitio donde dejarlo. Pero la eleccion es del
operador, no mia, porque el presupuesto que yo mismo acote ya esta agotado.

### Ciclo de la remediacion, si el operador autoriza A

    remediacion    seccion 6 sobre Area_comun/tasks/TASK-0354-*.md y TASK-0363-*.md (goal, AC1, cuerpo).
                   Cero cambios en .github/workflows/validate.yml.
    puertas        validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py,
                   protocol_replay.py --check-drift   (todas EXIT=0 antes del commit de cierre)
    re-juicio      mio, sobre el texto, antes del commit de cierre; no re-mido mecanismo
    iteraciones    UNA, y de transcripcion. Si hiciera falta otra, no la resuelvo yo.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Texto en `665d00fb`, implementacion en `cf918584f30fce9044dde99de1c7fadff879703b` (sha256 del workflow
`f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e`).
Alcance: solo el hub, sin producto en alcance.
