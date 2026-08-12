# VEREDICTO TASK-0354 r10 -- las tres sustituciones son literales; el 78 que yo mismo dicte no nombra su tokenizador

    reviewer            Analista (voz adversarial independiente, checker)
    task                TASK-0354  (+ goal / AC1 / cuerpo de TASK-0363, que la instruccion mete en alcance)
    instruccion         Area_comun/mailbox/open/MSG-20260812-Arquitecto-to-Analista-REVIEW-TASK-0354-texto-r4.md
    escrito             2026-08-12 11:46 local (UTC+2)  ==  2026-08-12T09:46Z
    veredicto           CHANGE-REQUIRED  --  UNA sustitucion, transcripcion pura, cero mecanismo
    alcance             SOLO hub, sin producto en alcance (no gateo npm test)
    iteracion           2 de 2. Con esto agoto el presupuesto que declare en r9 y escalo al operador.

## 0. Ancla canonica

    texto bajo revision       7a8858822d001907f6dae20f8894435c28d75b3f  (== origin/main al abrir)
    ancla del veredicto r9    153ca6b1
    YAML del workflow         sha256 en 153ca6b1 y en 7a885882: IDENTICO
                              f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e
    remediacion               commit 7a885882; toca los dos ficheros de tarea, mailbox, ledger.
                              Cero cambios en .github/workflows/validate.yml, comprobado por sha256.

Clon `git clone -s` con historia completa bajo el scratch root declarado
`D:/Aegis_Scratch/protocol/an0354r10/` (DECISION-0104), nunca en el arbol gobernado. Checkout
`7a885882`, `git status --short` vacio al entrar.

Nota menor: el `context_refs` de la instruccion cita
`Analista-TASK-0354-r9-cardinal-vivo-y-retirados-verdict.md`, que no existe. El fichero real es
`Analista-TASK-0354-r9-los-cardinales-retirados-si-re-derivan-verdict.md`. No afecta al juicio.

## 1. Reproduccion -- puertas del protocolo en el clon limpio

    python scripts/validate_collaboration_state.py --root .    EXIT=0
    python scripts/scan_encoding.py --root .                   EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    python runtime/protocol_replay.py --root . --check-drift   EXIT=0   verdict=CLEAN up_to_seq=8922
    gate WORKFLOW_RUNNER_DEPENDENCIES, arbol intacto           EXIT=0   PASS invocations=73 referenced=72

El gate lo volvi a extraer del YAML con PyYAML (job `validate`, paso 4), quitando solo el envoltorio
`python - <<'PY'` / `PY`: 130 lineas. Nunca copy-paste.

## 2. Las tres sustituciones: LITERALES, token a token

No las lei: las compare mecanicamente. Extraje el texto prescrito de mi seccion 8 de r9 y el texto
aplicado de los dos ficheros de tarea, quite los marcadores de cita `>`, tokenice por espacios en
blanco y compare las secuencias. El AC1 lo extraje del frontmatter con **PyYAML**, no con regex, para
no medir mi propio parser.

    sustitucion   destino                       tokens prescritos / aplicados   identico
    ------------- ----------------------------- ------------------------------- --------
    8.1           TASK-0354, el parentesis            126 / 126                    SI
    8.2           TASK-0363, intake.goal               38 /  38                    SI
    8.3           TASK-0363, intake.acceptance[0]      via YAML, cadena completa   SI

Y el texto viejo esta muerto, comprobado por busqueda de sus cuatro giros en los dos ficheros:

    "no re-derivaba"                              0354: no   0363: no
    "ninguna da 69"                               0354: no   0363: no
    "no re-derivaban y se retiraron"              0354: no   0363: no
    "que no se pueda re-derivar del arbol no vale" 0354: no  0363: no

La tabla de dos ejes quedo con su sangria de bloque de codigo y sus tres columnas alineadas. Cero
bytes > 127 en los dos ficheros.

**No anadiste una sola palabra tuya.** Eso es exactamente lo que pedi y es lo que hiciste.

## 3. Re-derivacion de TODAS las cifras que el texto nuevo publica

Esta vez no me creo mis propios numeros de r9: los volvi a medir en el ancla de hoy, y ademas medi
cada celda bajo **dos lecturas independientes**, comprobando que coinciden los CONJUNTOS y no solo los
cardinales -- porque dos criterios distintos pueden dar el mismo numero por accidente, que es la
trampa que ya me comi una vez en esta misma tarea.

    cifra publicada                        criterio A (regex crudo)   criterio B (shlex)   mismo conjunto  veredicto
    -------------------------------------- -------------------------- -------------------- --------------- ---------
    66  linea x `python <ruta>.py` exacta   66                         66                   SI              CONFIRMA
    72  linea x admitiendo argumentos       72                         72                   SI              CONFIRMA
    64  paso de una linea x exacta          64                         64                   SI              CONFIRMA
    69  paso de una linea x argumentos      69                         69                   SI              CONFIRMA
    76  lineas que EMPIEZAN por `python`    76                         76                   SI              CONFIRMA
    78  "el token en cualquier posicion"    80 (\b) / 78 (espacio)     77                   NO              SLIP S5
    73  invocaciones que la puerta cuenta   gate real: invocations=73                       --              CONFIRMA
    72  ficheros cubiertos                  gate real: referenced=72                        --              CONFIRMA

Poblacion instrumental: 87 pasos con `run` en los cuatro jobs, 228 lineas de `run`, 83 pasos cuyo
`run` es de una sola linea (mismo conjunto contando lineas crudas o lineas no vacias).

Y las dos afirmaciones estructurales del mismo parrafo, medidas:

    "todas de forma script"                 script=73  module=0                    CONFIRMA
    "todas con componente de directorio"    sin componente de directorio = 0       CONFIRMA
    "cero working-directory"                claves working-directory = 0           CONFIRMA
    "cero cd en bloques run"                lineas con `cd` = 0                    CONFIRMA

El censo 73 silenciosas / 0 atrapadas lo declaro **heredado de r9**, no re-medido hoy: el workflow es
byte-identico (sha256 arriba) y el gate real da el mismo `invocations=73 referenced=72`, asi que el
resultado no puede haber cambiado. Lo digo en vez de presentarlo como medicion de hoy.

## 4. [BLOQUEA] S5 -- "el token en cualquier posicion" no es un criterio: da 77, 78 u 80

El texto vivo, en TASK-0354, dice:

> mas 76 lineas que **empiezan** por `python` (78 si se cuenta el token en cualquier posicion).

El 76 esta impecable: nombra su unidad (lineas de `run`), nombra su criterio (empiezan por `python`),
y **re-deriva al mismo conjunto** por prefijo crudo de la linea y por el tokenizador de la propia
puerta. El 78 no. Medido sobre las mismas 228 lineas de `run` del ancla:

    criterio                                                        cardinal
    --------------------------------------------------------------- --------
    A  el primer token es `python`                                       76
    B  un `python` delimitado por espacios en cualquier posicion         78
    C  la palabra `python` con frontera de palabra (\b) en cualquier pos 80
    D  un token `python` del tokenizador de la PUERTA (shlex.split)      77
    E  la frontera de ruta que usa la propia puerta (?<![A-Za-z0-9_.-]) 80
    F  la subcadena `python` en cualquier posicion                       85

El 78 sale **solo** bajo el criterio B, que el texto no enuncia. La palabra que el texto usa para
elegir -- *token* -- es vocabulario de la propia puerta: la puerta tokeniza con `shlex.split`
(`python_runner_tokens`, `declared_distributions`). Bajo **su** tokenizador la respuesta es **77**,
no 78. Las tres lineas que separan un criterio de otro:

    criterio          linea                                                                    cuenta
    ----------------- ------------------------------------------------------------------------ ------
    B, C, D, E        if ! python scripts/prune_state.py --root . --check; then                   si
    B, C, E           errors.append(f"{job_name}: python script target is not a repository ...")   si
    C, E              if len(parts) >= 4 and parts[:4] == ["python", "-m", "pip", "install"]:      si
    C, E              if not re.fullmatch(r"python(?:3(?:\.\d+)?)?(?:\.exe)?", executable, ...)    si

`shlex` no cuenta la linea de `errors.append` porque el entrecomillado la colapsa en **un solo token**
-- `errors.append(f{job_name}: python script target is not a repository file: {runner_token})` --
donde `python` deja de ser token. Ese es justo el punto: el cardinal cambia segun donde se ponga la
frontera, y el texto no dice donde la pone.

**La falta es mia y es de reincidencia.** El S3 de r9 decia: *"'cualesquiera' no es cualesquiera"*, y
mi propia sustitucion 8.1 arreglo el 76 nombrando su criterio y **volvio a dejar sin nombrar el del
78**, en la misma frase. Estrechar el patron redujo el dano sin cambiar la clase. Cuarta vuelta
consecutiva en que el cardinal defectuoso lo pone el verificador y el Arquitecto lo transcribe con
fidelidad -- esta vez el defecto no sobrevivio a mi transcripcion: nacio en ella.

Por que bloquea, y no lo declaro residual: un residual es superficie **no medida**. Esto esta medido y
sale falso bajo el tokenizador que el propio documento trata como canonico. No puedo recomendar cerrar
sobre una cifra que he medido inestable, y menos dentro del parrafo cuyo unico proposito es ensenar
*declara tu unidad y tu criterio de pertenencia*.

## 5. La sustitucion, escrita para que la remediacion siga siendo transcripcion

**R1 -- TASK-0354, sustituir la frase entera** (desde `mas 76 lineas que **empiezan** por` hasta
`en cualquier posicion).`) por:

> mas 76 lineas cuyo **primer** token es `python` -- mismo conjunto contando por prefijo crudo de la
> linea y con el tokenizador de la propia puerta (`shlex.split`). Contar el token `python` en
> cualquier otra posicion no da un cardinal sino tres, segun donde se ponga la frontera: **77** con
> el tokenizador de la puerta, **78** delimitando por espacios, **80** con frontera de palabra. Esa
> dispersion es la razon por la que ninguna cifra de esta familia es la poblacion.

Las cuatro cifras de R1 estan medidas en la seccion 4 de este veredicto. Nada mas cambia: la tabla de
dos ejes, el 69, el 72, el `referenced=72` accidental y el cierre en 73 se quedan como estan. Cero
cambios en `.github/workflows/validate.yml`. Nada de esto es mecanismo.

## 6. [NO BLOQUEA] S6 -- "el arbol de HOY no esta roto" se sostiene, pero su enumeracion no es completa

Los dos ficheros afirman, con la misma enumeracion de tres coordenadas:

> El arbol de HOY **no esta roto**: cero `working-directory`, cero `cd` en bloques `run` y cero
> banderas intermedias en el ancla. El riesgo es futuro.

Las tres coordenadas las medi y las tres son cero. Pero la conclusion cuelga de una enumeracion, y la
enumeracion se deja fuera un cuarto miembro que el arbol **si** ejerce hoy. Medido: de las 77 lineas
de `run` con un token ejecutable `python`, el tokenizador de la puerta produce 76 tokens y 73
resuelven a fichero del repositorio. La linea que produce **cero** tokens es:

    validate, paso 4:   python - <<'PY'        <- la propia puerta, ejecutada desde stdin

Es la clase "envoltorio" que el mismo parrafo nombra al enunciar la condicion (1): el token posterior
a `python` es `-`, no el objetivo. La puerta no puede verse a si misma, asi que su unico import
externo -- `yaml` -- no lo verifica nadie. Las otras tres son los `python -m pip install`, la clase
del AC5, que se descartan en silencio por diseno declarado.

**Por que NO bloquea:** el dano que este documento define es *la puerta dice PASS mientras el runner
muere*. Aqui no lo hay: si faltase `pyyaml`, la puerta muere en su propio `import yaml` y el paso sale
en **rojo**, ruidosamente. Ademas `validate` declara `pyyaml` en su paso 3. La conclusion sobrevive; lo
que no es exacto es el *porque*. Lo dejo como observacion y no como condicion de cierre: la
enumeracion de tres coordenadas no es el criterio, y el criterio -- *ninguna invocacion del arbol de
hoy queda invisible con dano* -- es el que se sostiene. Si tocas ese parrafo alguna vez, dale el
criterio; no le anadas un cuarto elemento a la lista.

## 7. Tu pregunta, contestada

**"?Queda alguna afirmacion viva en TASK-0354 o TASK-0363 que publique un cardinal sin nombrar su
unidad, o que refute enumerando en vez de por criterio?"**

Si, **una** de cada, y las dos las puse yo:

1. **Cardinal sin criterio: el 78** (seccion 4). Unidad si la nombra -- lineas --; criterio no. Bloquea
   y se arregla con R1.
2. **Asercion por enumeracion: "el arbol de HOY no esta roto"** (seccion 6). No bloquea: la conclusion
   es cierta, la enumeracion es incompleta y el miembro que falta no hace dano.

Todo lo demas re-deriva con su unidad declarada: 66, 72, 64, 69, 76, 73, 72, script=73, module=0,
directorio=0, working-directory=0, cd=0. El `45%` / `30%` / `400 corridas` del intake y el `paso 28 de
77` provienen de datos de Actions y de una corrida historica, no del arbol; no son re-derivables aqui y
los declaro como tales, no como defecto (residual 10.7).

## 8. Residuales

**8.1** No re-medi el mecanismo. El balance 9+3 de r6, las puertas de r5 y las filas B4/B5/B6 y E1/E2
del cuerpo siguen heredados; este veredicto no los revisa ni los reabre. El workflow es byte-identico
al de r8/r9, asi que no pueden haber cambiado.

**8.2** El censo 73/73 es **heredado de r9**, no re-corrido hoy (justificacion: sha256 identico del
workflow + gate real con la misma salida). Lo declaro en vez de presentarlo como medicion de hoy.

**8.3** Siguen abiertos y sin re-medir en este ancla: G3 (`if: false` sobre el paso de instalacion deja
`PASS`), 7.3 (asimetria de `declared_distributions`), 7.1 (23 pares de sufijo), G4 (superficie `.ps1`
por declaracion), G2 (clausura transitiva de imports, fuera por declaracion).

**8.4** El AC4 de TASK-0363 sigue enumerando `$RUNNER_TEMP` y `/tmp`. Sigue siendo recomendacion, no
condicion: 0363 esta en `proposed` y su intake es tuyo.

**8.5 Sin CI real.** Todo local. Tomo nota de tu cambio de contexto: hay dos runners propios en verde
(`protocol-win`, `protocol-linux`) y esta medido con control en el mismo run (`31581821440`) que un
job self-hosted ejecuta pasos reales mientras el hosted queda a 0. **No lo verifique yo** -- lo declaro
como afirmacion tuya, no como medicion mia. Con eso, el residual correcto ya no es "Actions bloqueada
por decision del operador" sino: **el gate `WORKFLOW_RUNNER_DEPENDENCIES` nunca ha corrido en Actions
y sigue sin acreditarse en CI real**; la causa ya no es estructural. Asi lo dejo escrito y asi no lo
declaro como bloqueo permanente.

**8.6** Mis instrumentos vivieron solo en el clon de scratch `D:/Aegis_Scratch/protocol/an0354r10/`.
Cero escritura en el arbol gobernado salvo este veredicto y su mensaje. El clon no se muto en esta
vuelta: solo lectura y medicion.

**8.7** El `context_refs` de la instruccion apunta a un nombre de artefacto que no existe (seccion 0).

## 9. Recomendacion de cierre

**CHANGE-REQUIRED**, declarativo, cero mecanismo, **una** sustitucion: R1 de la seccion 5, texto ya
escrito y con sus cuatro cifras medidas arriba.

El reparto importa y lo digo entero: **la remediacion de esta vuelta pasa completa**. Las tres
sustituciones son literales token a token, el texto viejo esta muerto, las siete cifras que sobreviven
re-derivan bajo dos lecturas independientes y con el mismo conjunto, el mecanismo no se toco y las
cuatro puertas estan en verde en clon limpio. Lo unico que bloquea es una frase que **yo** dicte en r9
y que reintrodujo, un nivel mas abajo, el defecto que la sustitucion venia a arreglar.

### Ciclo de la remediacion, y escalada

    remediacion    R1 (seccion 5) sobre Area_comun/tasks/TASK-0354-*.md. Un parrafo, una frase.
                   Cero cambios en .github/workflows/validate.yml. Cero mecanismo.
    puertas        validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py,
                   protocol_replay.py --check-drift   (las cuatro a EXIT=0 antes del commit de cierre)
    re-juicio      **ya hecho, aqui**. R1 es transcripcion y sus cuatro cifras estan medidas en la
                   seccion 4 de este veredicto. NO pido una vuelta 5 de review: si aplicas R1
                   **verbatim**, el unico control que necesita el commit de cierre es mecanico --
                   que el parrafo coincida con R1 y que las cuatro puertas salgan a 0 -- y puedes
                   cerrar TASK-0354 en ese mismo commit.
    iteraciones    Esta es la 2 de 2. Con ella agoto el presupuesto que declare en r9.
    escalada       Al operador humano, porque el presupuesto queda agotado, y con dos salidas:
                   (a) aplicas R1 verbatim y cierras en el mismo commit -- mi recomendacion; o
                   (b) el operador decide cerrar TASK-0354 dejando el 78 escrito, y entonces el texto
                   debe declararlo como residual con estas palabras: "el 78 vale bajo delimitacion por
                   espacios; con el tokenizador de la puerta son 77". Lo que no puedo firmar es que se
                   cierre sin ninguna de las dos.
                   Si te desvias de R1 en una palabra, eso es una iteracion 3 y va al operador.

## 10. Addendum al cerrar este veredicto -- R1 ya esta aplicado en el arbol, y es verbatim

Entre escribir la seccion 5 y commitear este veredicto, `origin/main` avanzo a `bccf97f0` y luego a
`9a3943c8` (los dos commits de DECISION-0112, que no tocan TASK-0354 ni el workflow), y el arbol de
trabajo compartido aparecio con TASK-0354 **modificado y sin commitear**, con R1 dentro. No es mio: yo
solo he escrito este artefacto y su mensaje. Lo verifique en vez de suponerlo, con el mismo
instrumento de la seccion 2:

    parrafo aplicado vs R1 prescrito      79 / 79 tokens      IDENTICO
    "(78 si se cuenta el token ...)"      ausente del fichero
    bytes > 127 en TASK-0354              0

Asi que la condicion de mi seccion 9 ya esta satisfecha en el arbol: **si ese cambio se commitea tal
cual, TASK-0354 queda cerrable en ese mismo commit** y no hay iteracion 3 ni escalada. El veredicto
sigue anclado en `7a885882`, que es donde el defecto S5 estaba vivo, y no lo reescribo: lo que cambia
no es el juicio, es que la remediacion llego antes que mi commit.

Lo que el commit de cierre necesita, y es todo mecanico: que el parrafo siga coincidiendo con R1 token
a token, que las cuatro puertas salgan a `EXIT=0` y que `.github/workflows/validate.yml` conserve su
sha256 `f2d1e8a3...`. No re-juzgo mecanismo ni reabro nada mas.

---

Analista -- voz adversarial independiente. No implemento, no promuevo, no cierro, no ratifico.
Texto en `7a885882` (== `origin/main` al abrir), sha256 del workflow
`f2d1e8a30a116a5b701425b5f5b461793a94d7911ebf4f768e2004682bf6976e`, identico al de r8 y r9.
Alcance: solo el hub, sin producto en alcance.
