# VEREDICTO TASK-0354 r9 -- el cardinal vivo re-deriva entero; los dos cardinales RETIRADOS tambien, y el texto dice que no

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354  (+ goal / AC1 / cuerpo de TASK-0363, que la instruccion mete en alcance)
    instruccion         Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-texto-r3.md
    escrito             2026-08-12 10:45 local (UTC+2)  ==  2026-08-12T08:45Z
    veredicto           CHANGE-REQUIRED  --  declarativo, cero mecanismo, UNA vuelta de transcripcion
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           1 de las 2 que la instruccion concede tras la autorizacion del operador

## 0. Ancla canonica

    texto bajo revision       153ca6b1  (los dos ficheros de tarea son identicos en origin/main 9f4f844d:
                              git diff --name-status 153ca6b1 9f4f844d NO toca TASK-0354 ni TASK-0363)
    implementacion            cf918584f30fce9044dde99de1c7fadff879703b
    YAML del workflow         git diff cf918584 153ca6b1 -- .github/workflows/validate.yml  ->  VACIO
    sha256 del workflow       f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e
                              (identico al de r8; el mecanismo sigue sin tocarse)

Clon `git clone -s` con historia completa bajo el scratch root declarado `D:/Aegis_Scratch/mapp/t354r9/`
(DECISION-0104), nunca en el arbol gobernado. Checkout `153ca6b1`, `git status --short` vacio al entrar.

## 1. Reproduccion -- puertas del protocolo en el clon limpio

    python scripts/validate_collaboration_state.py --root .    EXIT=0
    python scripts/scan_encoding.py --root .                   EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    python runtime/protocol_replay.py --root . --check-drift   EXIT=0   verdict=CLEAN up_to_seq=8899
    gate WORKFLOW_RUNNER_DEPENDENCIES, arbol intacto           EXIT=0   PASS invocations=73 referenced=72

El gate lo extraje del YAML con PyYAML (job `validate`, paso 4, `Verify workflow runner dependency
declarations`) quitando solo el envoltorio `python - <<'PY'` / `PY`: 130 lineas. Nunca copy-paste.

## 2. El censo completo, por primera vez invocacion a invocacion -- CONFIRMA 73/73

En r8 declare como residual 7.5 que **no** habia verificado una a una que las 73 fueran silenciosas:
72 venian heredadas de r7 y la numero 73 solo estaba probada por ocultacion, no por la reescritura.
Esta vuelta lo cierro. Instrumento:

1. Enumero las invocaciones con el tokenizador **del propio gate** (`python_runner_tokens`), no con uno
   mio: 76 tokens producidos, 73 resuelven a fichero del repo, 3 son `python -m pip install` (forma
   modulo que no resuelve y se descarta en silencio: la clase del AC5).
2. Anclo cada invocacion a su linea cruda del YAML y **verifico que los dos multiconjuntos coinciden**
   antes de tocar nada: `YAML_derived=73  raw_line_sites=73  multisets_equal=True`. Si no coincidieran,
   el instrumento estaria midiendo otra cosa y el censo no valdria.
3. Para cada una de las 73, **sustitucion de una linea por una linea** con la reescritura mecanica que
   el texto publica -- `python <dir>/<base>.py [args]` -> `cd <dir> && python -u <base>.py [args]` --,
   ejecuto el gate real como proceso, restauro, y sigo. 74 ejecuciones del gate.
4. Al terminar: sha256 del workflow **identico** a `f2d1e8a3...` y `git status --short` vacio en el clon.

Resultado:

    M0  control, arbol intacto                                  EXIT=0  invocations=73 referenced=72
    ... 73 mutantes, uno por invocacion, restaurando entre medias ...
    === CENSO: SILENCIOSAS=73  ATRAPADAS=0  de 73 ===

Y las dos filas que el texto usa como argumento, medidas y no citadas:

    #    invocacion reescrita                                   EXIT  la puerta dice
    ---- ------------------------------------------------------ ---- ---------------------------
    2    scripts/validate_collaboration_state.py (1a de 2)         0   invocations=72 referenced=72
    4    scripts/validate_collaboration_state.py (2a de 2)         0   invocations=72 referenced=72
    15   scripts/prune_state.py  (`if ! python ...`, la n. 73)     0   invocations=72 referenced=71
    resto (70 invocaciones)                                       0   invocations=72 referenced=71

La asimetria que el texto afirma queda medida en las dos direcciones: ocultar **cualquiera** de las dos
invocaciones del duplicado deja `referenced=72` -- el fichero conserva cobertura --, y ocultar la numero
73 si baja `referenced` a 71. Son dos unidades distintas, exactamente como el texto dice.

## 3. Tabla vector por vector -- lo que el texto de 153ca6b1 afirma contra lo que yo medi

    afirmacion del texto                                        mi medicion en el clon limpio    veredicto
    ----------------------------------------------------------- -------------------------------- ---------
    poblacion = 73 invocaciones que la puerta cuenta             invocations=73                   CONFIRMA
    todas de forma script                                        script=73, module=0              CONFIRMA
    todas con componente de directorio                           sin directorio = 0               CONFIRMA
    73 silenciosas y 0 atrapadas                                 censo 73/73, ATRAPADAS=0         CONFIRMA
    cobertura por fichero = 72 (`referenced=72`)                 referenced=72                    CONFIRMA
    causa de la diferencia: validate_collaboration_state x2      unico fichero con 2 invocaciones CONFIRMA
    ocultar UNA de las dos no le quita cobertura al fichero      #2 y #4 -> referenced=72         CONFIRMA
    hacen falta las dos                                          se sigue de #2/#4 + M2 de r8     CONFIRMA
    N2 "rechaza el token: no resuelve; no es que viera el runner" transcrito literal, tambien 0363 CONFIRMA
    propiedad de DOS condiciones, dos direcciones opuestas       misma redaccion en 0354 y 0363   CONFIRMA
    AC1 exige declarar la UNIDAD y no anclar en la forma         escrito; se retiro `referenced`  CONFIRMA
    empalme roto del goal reparado                               el parentesis cierra al final    CONFIRMA
    cero cambios en .github/workflows/validate.yml               diff vacio + sha256 identico     CONFIRMA
    "66 lineas `python <ruta>.py` exactas"                       66                               CONFIRMA
    "64 pasos de una linea"                                      64 (pasos de 1 linea, forma exacta) CONFIRMA
    "72 con argumentos"                                          72 (lineas, argumentos admitidos)   CONFIRMA
    "76 lineas `python` cualesquiera"                            76 solo si "cualesquiera" = "que    SLIP S3
                                                                 EMPIEZAN por python"; 78 si no
    "el 69 de la primera redaccion no re-derivaba"               69 = pasos de 1 linea con args      SLIP S1
    "el 72 de la segunda tampoco [re-derivaba]"                  72 = lineas con args; y referenced  SLIP S2

La transcripcion de mi seccion 6 es **fiel**, el cardinal vivo es **correcto y ahora esta medido entero**,
y el mecanismo no se toco. Todo lo que bloquea vive en un parentesis sobre los cardinales **retirados**.

## 4. [BLOQUEA] S1 -- el 69 si re-deriva: es la celda que el propio texto se salta

El texto refuta el 69 **enumerando** cuatro cifras y concluyendo *"y ninguna da 69"*. Las cuatro cifras
no son cuatro criterios independientes: son tres esquinas de una tabla de dos ejes -- **que unidad**
(linea de `run` / paso de `run` de una sola linea) por **que forma** (`python <ruta>.py` exacta / con
argumentos). Medida entera en el ancla:

    unidad \ forma                 exacta `python <ruta>.py`     admitiendo argumentos
    linea de `run`                            66                          72
    paso de `run` de una linea                64                        **69**

El texto cita 66, 64 y 72 -- y omite la cuarta esquina, que vale exactamente **69**. El cardinal que la
primera redaccion publico no es un numero sin origen: es el conteo de **pasos de una sola linea que
invocan `python <ruta>.py`**, el criterio mas natural para quien cuenta "invocaciones" por pasos en vez
de por lineas. Un comando lo re-deriva.

Es la leccion de esta instancia aplicada a si misma: *el encargo que enumera recibe la enumeracion*.
Refutar un cardinal enumerando cuatro criterios alternativos tiene el mismo defecto que reconocer
invocaciones enumerando formas -- cierra las que alguien listo y deja abierta la que no.

## 5. [BLOQUEA] S2 -- el 72 tambien re-deriva, y la misma frase que lo niega nombra su criterio

El texto dice: *"el 72 de la segunda tampoco [re-derivaba]: **salia de un criterio anclado a la linea**
que descartaba la invocacion `if ! python scripts/prune_state.py ...`"*. Una cifra que **sale de un
criterio** re-deriva por definicion bajo ese criterio. Medido: lineas `python <ruta>.py` admitiendo
argumentos = **72**, la celda superior derecha de la tabla. Y hay una segunda derivacion del mismo 72 en
el mismo parrafo: `referenced=72`, los ficheros cubiertos.

Lo que r8 establecio -- y sigue en pie -- no es que el 72 no se pudiera re-derivar, sino que **contaba
la unidad equivocada** bajo un criterio anclado a la forma del texto, y que su coincidencia con
`referenced=72` era accidental. Esas dos cosas no son la misma, y el texto publica la que es falsa.

## 6. [BLOQUEA] S3 -- "cualesquiera" no es cualesquiera, y lo que excluye es justo la invocacion 73

*"76 lineas `python` cualesquiera"*. Medido sobre los bloques `run` del ancla:

    lineas que EMPIEZAN por `python`                    76
    lineas con un token `python` en cualquier posicion  78

El 76 solo sale bajo el criterio "empiezan por `python`". Las dos lineas que separan 78 de 76 son:

    errors.append(f"{job_name}: python script target is not a repository file: ...")   <- fuente del gate
    if ! python scripts/prune_state.py --root . --check; then                          <- LA INVOCACION 73

La cifra que el parrafo presenta como cota superior "cualquiera" de la familia esta calculada con un
filtro de inicio de linea que descarta precisamente la invocacion cuyo descarte es el hallazgo entero de
r8. En un texto cuya tesis es *declara la unidad y no ancles en la forma de la linea*, publicar una cota
llamada "cualesquiera" que en realidad ancla en el inicio de la linea es el defecto en su propia vitrina.

## 7. [BLOQUEA] S4 -- S1 y S2 estan dentro de un criterio de aceptacion, no solo en la prosa

    TASK-0363, goal   "(Los cardinales 69 y 72 de las dos primeras redacciones no re-derivaban y se
                       retiraron en r7 y r8.)"
    TASK-0363, AC1    "Un cardinal que no se pueda re-derivar del arbol no vale: ni el 69 de la primera
                       redaccion ni el 72 de la segunda lo eran."

AC1 es un criterio de **falsacion**: quien lo false recontara. Recontara 69 y recontara 72, y encontrara
la tabla de la seccion 4. Peor que el dato falso es la regla que AC1 enuncia con el: *"un cardinal que no
se pueda re-derivar no vale"* no es la regla que sobrevive a esta medicion, porque **los dos cardinales
defectuosos re-derivan**. La regla que sobrevive es la que la primera mitad del propio AC1 ya dice bien:
un cardinal vale si declara **que unidad** cuenta y su criterio de pertenencia **no ancla en la forma del
texto**. La frase de cierre contradice a la de apertura en el mismo criterio.

## 8. La redaccion exacta, para que siga siendo transcripcion y no redaccion

**8.1 -- TASK-0354, sustituir el parentesis entero** (desde `(El 69 de la primera redaccion` hasta
`era accidental.)`) por:

> (Los dos cardinales retirados **si** se re-derivan; lo que fallaba era su unidad y su criterio,
> anclados a la forma del texto y no a lo que la puerta descubre. Todos salen de la misma familia,
> medida en el ancla:
>
>     unidad \ forma                 exacta `python <ruta>.py`   admitiendo argumentos
>     linea de `run`                            66                        72
>     paso de `run` de una sola linea           64                        69
>
> mas 76 lineas que **empiezan** por `python` (78 si se cuenta el token en cualquier posicion). El **69**
> de la primera redaccion es la celda paso+argumentos; el **72** de la segunda es la celda
> linea+argumentos, y su coincidencia con `referenced=72` -- que cuenta ficheros -- era accidental.
> Ninguna celda de esa tabla es la poblacion: la poblacion es lo que la puerta descubre, 73.)

**8.2 -- TASK-0363, `goal`, sustituir** `(Los cardinales 69 y 72 de las dos primeras redacciones no
re-derivaban y se retiraron en r7 y r8.)` por:

> (Los cardinales 69 y 72 de las dos primeras redacciones se retiraron en r7 y r8: no por
> irre-derivables -- se re-derivan --, sino por contar la unidad equivocada bajo un criterio anclado a la
> forma del texto.)

**8.3 -- TASK-0363, AC1, sustituir la frase de cierre** `Un cardinal que no se pueda re-derivar del
arbol no vale: ni el 69 de la primera redaccion ni el 72 de la segunda lo eran.` por:

> Un cardinal no vale por re-derivarse: vale si declara su unidad y un criterio de pertenencia que no
> ancle en la forma del texto. El 69 y el 72 de las dos primeras redacciones **se re-derivan** -- son
> celdas de la tabla forma-por-unidad de TASK-0354 -- y aun asi eran falsos, porque contaban la unidad
> equivocada.

Cero cambios en `.github/workflows/validate.yml`. Nada de esto es mecanismo.

## 9. Tus dos preguntas

**9.1 -- La inclusion de las cuatro cifras: SI, quedatelas, pero no como prueba de lo que prueban.**
Las cuatro re-derivan; las medi una a una y estan en la tabla de la seccion 3. Lo que no se sostiene es
la conclusion que cuelga de ellas (*"y ninguna da 69"*), porque son tres esquinas de un cuadrado cuya
cuarta esquina es 69. Mi seccion 6 comprimia la clausula a *"El 69 no re-derivaba"*, que es **la misma
afirmacion falsa sin siquiera ensenar el trabajo**: el defecto es mio y tu inclusion no lo introdujo, solo
lo dejo a la vista. Por eso la respuesta no es "literal o no literal", sino la sustitucion 8.1.

**9.2 -- El AC4 de TASK-0363: si debe cubrir la clase mencion-no-invocada, pero no anadiendo un tercer
elemento a la lista.** Hoy AC4 enumera `$RUNNER_TEMP` y `/tmp`, que es la misma enumeracion-de-instancias
que esta tarea existe para desterrar; anadir "y las rutas del repo nombradas sin invocar" cierra la
grafia que acabo de encontrar y deja abierta la siguiente. Si lo tocas, dale criterio: *el rojo se
reserva a una invocacion descubierta cuyo objetivo no resuelve; ninguna ruta `.py` que no sea una
invocacion puede enrojecer, este dentro o fuera del repositorio*. Con ese criterio, `$RUNNER_TEMP`,
`/tmp` y `git add scripts/prune_state.py` caen por pertenencia y no por lista. Dicho esto: **esto no
gatea el cierre de TASK-0354**. TASK-0363 esta en `proposed` y su intake es tuyo; lo digo como
recomendacion, no como condicion.

## 10. Residuales

**10.1** No re-medi el mecanismo. El balance 9+3 de r6, las puertas de r5 y las filas B4/B5/B6 del
cuerpo siguen como estaban; este veredicto no los revisa ni los reabre.

**10.2** El censo usa **una** forma de reescritura (`cd <dir> && python -u <base>`) aplicada a **una**
invocacion por vez. No probe composiciones de dos reescrituras simultaneas ni otras banderas; la clase
esta cubierta por la condicion (1), pero el cardinal 73/73 esta medido solo para esa forma.

**10.3** Las filas E1/E2 del inventario de falsos rojos las mido como **heredadas de r8**: no las re-corri
en esta vuelta. El workflow es byte-identico (`f2d1e8a3...`), asi que el resultado no puede haber cambiado,
pero lo declaro en vez de presentarlo como medicion de hoy.

**10.4** Siguen abiertos y sin re-medir en este ancla: G3 (`if: false` sobre el paso de instalacion deja
`PASS`), 7.3 (asimetria de `declared_distributions`, anclada a `parts[:4] == ["python","-m","pip","install"]`),
7.1 (23 pares de sufijo), G4 (superficie `.ps1` por declaracion y no por mecanismo), G2 (clausura
transitiva de imports, fuera por declaracion).

**10.5 Sin CI real.** Todo local; Actions sigue bloqueada por decision del operador. Este gate nunca ha
corrido en GitHub Actions.

**10.6** Mis mutantes vivieron solo en el clon de scratch `D:/Aegis_Scratch/mapp/t354r9/`. El workflow
quedo restaurado y verificado por sha256, `git status --short` vacio salvo mis instrumentos, que no salen
de ahi. Cero escritura en el arbol gobernado salvo este veredicto y su mensaje.

## 11. Recomendacion de cierre

**CHANGE-REQUIRED**, declarativo, cero mecanismo, **una** vuelta de transcripcion: las tres sustituciones
de la seccion 8, con el texto exacto ya escrito.

Lo digo con la proporcion que le corresponde, porque el reparto importa: **el contenido operativo de esta
vuelta pasa entero**. La transcripcion de mi seccion 6 es fiel, el cardinal vivo 73/72 re-deriva y por
primera vez esta medido invocacion a invocacion, la asimetria del duplicado esta medida en las dos
direcciones, el empalme roto esta reparado y el YAML no se toco. Lo que bloquea es un parentesis sobre
cardinales **ya retirados** que afirma tres cosas falsas -- y una de ellas vive dentro de un criterio de
aceptacion que existe justamente para prohibirlas.

Y el defecto es mio otra vez: la frase *"El 69 de la primera redaccion no re-derivaba"* la escribi yo en
la seccion 6 de r8, sin re-derivarla. Tercera vuelta consecutiva en que el cardinal defectuoso lo pone el
verificador y el Arquitecto lo transcribe con fidelidad. La diferencia esta vez es que la correccion no
pide medir nada nuevo: el trabajo esta hecho arriba y la seccion 8 es texto listo para pegar.

### Ciclo de la remediacion

    remediacion    secciones 8.1, 8.2 y 8.3 sobre Area_comun/tasks/TASK-0354-*.md y TASK-0363-*.md.
                   Cero cambios en .github/workflows/validate.yml.
    puertas        validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py,
                   protocol_replay.py --check-drift   (todas EXIT=0 antes del commit de cierre)
    re-juicio      mio, sobre el texto, antes del commit de cierre; no re-mido mecanismo
    iteraciones    UNA. Es la primera de las dos que la instruccion concede. Si hiciera falta la
                   segunda, la agoto ahi y escalo al operador humano sin resolverla yo.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Texto en `153ca6b1` (identico en `9f4f844d` para los dos ficheros de tarea), implementacion en
`cf918584f30fce9044dde99de1c7fadff879703b`, sha256 del workflow
`f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e`.
Alcance: solo el hub, sin producto en alcance.
