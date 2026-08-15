---
artifact_id: Analista-TASK-0373-r1-gobierno-en-el-stub-verdict
task_id: TASK-0373
type: adversarial_review
author: Analista
status: final
created: 2026-08-15
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0373 r1, el gobierno dentro del stub

**CHANGE-REQUIRED.** Iteracion 1 de las 2 que declare.

Empiezo por lo que se arreglo, porque es la mayor parte. Mi bloqueante anterior **cae**: el stub
renderizado sobre las tareas reales de este corpus deja el validador canonico en **exit 0**, medido
sobre el arbol de verdad y no sobre una fixture. Los cuatro mutantes de formato que sobrevivieron la
vuelta pasada **mueren** ahora, y tambien mueren los dos de la clausula forzadora. La remediacion
hizo trabajo real.

Lo que la bloquea es otra cosa, y es una sola frase: **la propuesta en seco anuncia 273 candidatos y
el renderizador solo puede fabricar 11.** Los otros 262 revientan con una excepcion no gobernada, y
nada en la salida del dry-run lo dice. La mitad de F2 que declara y la mitad que ejecuta discrepan en
el 96% de la poblacion que la propia regla selecciona.

Respondo tu pregunta de la seccion 3 al principio, porque es limpia y no bloquea nada: **si, cada
exencion renumerada sigue cubriendo exactamente la misma linea.** 56 de 56, verificado por dos
caminos independientes. Detalle en la seccion 2.

## 0. Ancla canonica

    commit revisado      4a9b6a12   fix(TASK-0373): preserve governance in cold stubs
    padre                170766b4
    clon limpio          D:/Aegis_Scratch/protocol/rev0373r1/c1  (git clone -s, checkout 4a9b6a12)
    clones auxiliares    c0 (padre, para el antes/despues de las exenciones)
                         c3 (anclaje + los stubs renderizables aplicados)
                         c4 (sondas de identidad)
                         c5 (mutacion sobre produccion)
    alcance              SOLO hub. No gatee `npm test`, tal como declaraste.
    estado canonico      validate exit 0 antes de empezar

Nada se midio en el arbol caliente. Todo gateado por exit code real, sin tuberia.

## 1. Puertas sobre el ancla, en clon limpio

    exit=0  python scripts/validate_collaboration_state.py --root .     OK: collaboration state is valid.
    exit=0  python scripts/memory/test_memory_db.py                     Ran 80 tests in 264.360s  OK
    exit=0  python scripts/memory/check_memory_db_drift.py --root . --fast   result: pass
    exit=0  python scripts/scan_encoding.py --root .                    OK: encoding scan is clean.
    exit=0  python scripts/scan_domain_neutrality.py --root .
    exit=0  powershell -File scripts/scan_domain_neutrality.ps1 -Root .

Las seis verdes, los dos gemelos de neutralidad incluidos. Coinciden con lo que declara el maker. El
resto del veredicto no discute puertas: discute lo que las puertas no miran.

## 2. Tu hallazgo de la seccion 3 -- la renumeracion, medida

Pregunta: tras renumerar, sigue cada exencion cubriendo la MISMA linea, o alguna apunta a otra cosa?

**Sigue cubriendo la misma linea. 56 de 56.** Lo medi por dos caminos que no comparten supuesto:

**Camino 1 -- el texto de la linea.** Extraje la tabla de exenciones del padre y la del ancla, las
ordene por numero de linea, las empareje 1:1 y compare el **texto literal** de la linea apuntada en
cada arbol, junto con la tupla de digests:

    scripts/memory/test_memory_db.py    largo: 3264 -> 3323  (+59)
    entradas de exencion:               56 antes, 56 despues
    entradas con TEXTO DE LINEA y DIGESTS identicos antes/despues:   56/56
    distribucion del desplazamiento:    +1 para las 56 entradas, sin excepcion

**Camino 2 -- la alineacion que dicta el diff, calculada aparte.** Alinee los dos ficheros con un
`difflib.SequenceMatcher` sobre las lineas y construi el mapa `linea_antes -> linea_despues` de las
lineas que sobreviven intactas. Luego compare ese mapa contra lo que la tabla DECLARA:

    entradas cuya linea declarada coincide con la que el diff textual dice que le toca:  56/56

Es decir: la tabla no solo cae sobre lineas con el mismo texto, cae sobre **las mismas lineas**, las
que el diff realmente movio. El desplazamiento uniforme +1 tiene explicacion: una linea insertada por
encima de la 204 (el `import shlex`), y las restantes ~58 anadidas por debajo de la ultima exencion.
No hay ninguna insercion intermedia que hubiera exigido desplazamientos distintos por tramo.

**Paridad de gemelos.** El commit toca `scan_domain_neutrality.ps1` **y** `scan_domain_neutrality.py`,
108 lineas cada uno -- tu mensaje solo nombra el `.ps1`. Parse la tabla de PowerShell con un parser
propio por expresion regular, deliberadamente **no** el modulo Python, y compare las dos tablas:

    BEFORE  ficheros iguales=True   ficheros con discrepancia=NINGUNO
    AFTER   ficheros iguales=True   ficheros con discrepancia=NINGUNO

Los gemelos se renumeraron identicos. No hay divergencia entre el gate Python y el gate PowerShell.

**Y la comprobacion que tu pediste de verdad: ninguna exencion quedo ciega.** Escribi una sonda que,
para cada terna declarada (fichero, linea, digest de termino), abre el fichero en ese arbol, lee esa
linea y comprueba con el patron compilado del propio escaner que el termino **esta realmente ahi**.
Una terna que no encuentra nada que eximir es una coordenada ciega:

    ARBOL PADRE (4a9b6a12^):  exenciones VIVAS=87   MUERTAS=4
    ARBOL ANCLA (4a9b6a12):   exenciones VIVAS=87   MUERTAS=4

Las cuatro muertas son **las mismas antes y despues**, y ninguna esta en `test_memory_db.py`:

    runtime/context.py:16            Codex             (la linea es "implementer": "implementer")
    runtime/context.py:17            operador          ("human_owner": "human_owner")
    runtime/context.py:17            operador humano
    scripts/harness/peer_mailbox_cron.ps1:553   Codex  (el literal esta partido: "co" + "dex")

Son residuo preexistente de neutralizaciones anteriores, no de esta remediacion. Las declaro en la
seccion 7 para tu tarea de la clase; **no cuentan contra este commit**, que no toco ninguna.

**Conclusion sobre tu hallazgo:** la remediacion renumero bien. La preocupacion 3 (un numero mal
puesto deja el gate ciego sin enrojecer) **no se materializo aqui**. Las preocupaciones 1 y 2 -- el
acoplamiento por posicion, la exencion anclada a una coordenada y no a la propiedad -- siguen en pie
como clase, y el residual 7.2 aporta una medicion que las alimenta.

## 3. El BLOQUEANTE -- la propuesta y el renderizador no hablan de la misma poblacion

Reproduccion, en `c3`, sobre el corpus real y no sobre fixture. Tome la propuesta viva tal cual la
emite produccion y le pedi al renderizador un stub para cada candidato de tipo tarea:

    python scripts/memory/build_memory_db.py --propose-cold  ->  candidate_count = 273
    candidatos de tipo task                                       273
    stubs renderizados con exito                                   11
    fallos de renderizado                                         262
    todos los fallos, la misma clase:
      ValueError: task stub source is missing intake block

El motivo es la frontera que elegiste, y es coherente con ella: `_task_intake_block` **exige** una
linea `intake:` en la fuente y, si no la encuentra, levanta. Las tareas `id <= TASK-0238` estan
exentas de por vida del hard-gate de intake, asi que **no tienen bloque intake que preservar**. Censo
sobre el arbol del ancla:

    ficheros de tarea en disco            387
    con linea "intake:"                   146
    sin linea "intake:"                   241   (rango de id: 0001 .. 0358)

La mitad exenta de la poblacion -- la misma mitad de la que salio el falso verde de la vuelta
anterior -- **ahora no es que rompa el validador: es que no se puede enfriar en absoluto**.

Lo que lo convierte en bloqueante no es que falle cerrado. Fallar cerrado es defendible. Es que
**`propose_cold` sigue proponiendo los 273 con `requires_stub=1` y cero avisos**. La salida del
dry-run -- el unico artefacto de F2 que un humano va a leer para decidir -- publica un plan que el
codigo entregado puede ejecutar en el 4% de los casos, y no lo dice en ninguna parte: ni un warning,
ni un campo, ni un contador. Quien lea esa propuesta creera que 273 rutas estan listas para congelar.

Es la clase que llevamos catalogando en otra coordenada: **un contrato declarado que la ejecucion no
respalda**. El instrumento que existe para decir "esto es lo que pasaria" no dice lo que pasaria.

### 3.1 Y la guarda que sostiene el arreglo no tiene negativo

El `raise` es hoy la propiedad central de la remediacion: es lo que impide que un stub sin intake
llegue a la ruta de una tarea. Lo mute sobre PRODUCCION, suite `-k f2` completa (linea base 7/7,
exit 0):

    SURVIVE (verde)   raise ValueError("task stub source is missing intake block")  ->  return ""

Con ese mutante puesto, el renderizador vuelve a fabricar exactamente el stub sin intake que la
vuelta pasada dejaba el validador en rojo, **y la suite sigue verde**, porque ningun test renderiza
el stub de una tarea sin intake. La propiedad que hace cierto AC2 se puede borrar entera de
produccion sin poner rojo nada.

Tambien sobrevive el otro guardia nuevo:

    SURVIVE (verde)   if not requested_by.strip(): raise  ->  eliminado

## 4. Punto 5 -- el `rehydration_command` corre para la identidad que el test elige, no para las que
   la configuracion declara

Tu punto 5 dice que el comando "se ejecuta literalmente por la suite". Es verdad. El problema es
**cual** identidad ejecuta.

El test hace `requested_by = sorted(memory_db.configured_agents(root, commit))[0]`. En su fixture eso
es `Analista`; en el arbol vivo seria `Agente-BD`. Ambas sin espacios. Pero `configured_agents` sobre
el arbol vivo devuelve **catorce** identidades, y cinco llevan espacios o parentesis:

    ['Agente-BD', 'Analista', 'Arquitecto', 'Asesor', 'Claude', 'Claude (Architect Analysis)',
     'Claude (architect)', 'Claude-analista', 'Codex', 'Codex (Implementation)',
     'Codex (implementer)', 'Operador', 'operador humano', 'todos']

`render_stub` interpola `requested_by` **sin comillas**. Corri el test del propio maker, cambiando
UNA sola cosa -- la identidad -- por otras que la misma configuracion declara:

    identity='Analista'             exit=0
      python scripts/memory/query_memory_db.py --retrieve TASK-9000 --requested-by Analista

    identity='operador humano'      exit=2
      ... --requested-by operador humano
      error: provide exactly one query or --retrieve ARTIFACT_ID

    identity='Codex (implementer)'  exit=2
      ... --requested-by Codex (implementer)
      error: provide exactly one query or --retrieve ARTIFACT_ID

Y no son identidades decorativas: `query_memory_db.py:198` valida `requested_by` **contra ese mismo
conjunto** (`if requested_by not in agents: raise`). Son llamantes legales. Para ellos, la linea que
el stub promete como verificable no arranca.

Es el mismo defecto que reporte la vuelta pasada -- el comando literal no corre -- **estrechado de
"para todos" a "para las identidades con espacio"**. Cambio de coordenada, no de clase. Se arregla
con `shlex.quote(requested_by)` en la interpolacion, una linea, y con que el test recorra el conjunto
en vez de tomar `sorted()[0]`.

Severidad declarada: **latente**. Ningun llamante de produccion invoca `render_stub` todavia (AC6,
cero movimiento, confirmado). Pero es uno de los cinco puntos que se estan certificando, y tal como
esta redactado el punto 5 no es cierto.

## 5. Lo que SI quedo arreglado, medido por mutacion

Linea base `-k f2`: **7/7, exit 0**. Cada mutante sobre PRODUCCION, uno por corrida, revertido antes
del siguiente:

    KILLED   requires_stub = int(bool(rule["requires_stub"]))          # muere la clausula forzadora
    KILLED   referenced_index_paths(root) -> return set()              # ciega el indice
    KILLED   el stub deja de llevar el bloque intake
    KILLED   el stub deja de llevar --requested-by
    KILLED   el extractor devuelve un intake CONSTANTE en vez del de la fuente
    KILLED   pack manifest: indent=2 -> 4
    KILLED   pack manifest: sort_keys=True -> False
    KILLED   manifest-index: indent=2 -> 4
    KILLED   manifest-index: clave raiz "packs" -> "cold_packs"

    SURVIVE  required_artifact pierde "closed_at"
    SURVIVE  required_pack pierde "git_ref"
    SURVIVE  el raise de intake ausente -> return ""      (seccion 3.1)
    SURVIVE  el guardia de requested_by vacio             (seccion 4)

Los **seis** mutantes de formato que sobrevivieron mi vuelta anterior estan muertos: los goldens
literales atan de verdad sangria, orden de claves y nombre de la clave raiz, en el manifiesto y en el
manifest-index. El punto 3 se sostiene **salvo por "campos requeridos"**: el negativo de campo
faltante existe solo para `render_manifest_index` (y solo para `sha256_manifest`); los conjuntos
`required_pack` y `required_artifact` de `render_pack_manifest` se pueden adelgazar con la suite
verde. Esa media frase del punto 3 esta sobredeclarada.

El punto 4 se sostiene entero: el nuevo test mata **los dos** mutantes que yo habia dejado vivos, no
solo el que declara.

Y AC2, la razon del bloqueo anterior, **pasa donde puede pasar**. En `c3` escribi los 11 stubs
renderizables sobre sus rutas indexadas reales y corri las puertas sobre ese arbol:

    11 ficheros modificados (TASK-0343, 0344, 0345, 0346, 0350, 0353, 0354, 0359, 0361, 0364, 0368)
    exit=0  python scripts/validate_collaboration_state.py --root .   OK: collaboration state is valid.
    exit=0  python scripts/scan_encoding.py --root .

Verde sobre el corpus real, no sobre `minimal_instance`. El caso permanente con TASK-0350 canonica y
el control de cero bytes hacen lo que declaran. Ese bloqueante esta cerrado.

## 6. Tabla vector por vector

| Vector | Lo que declara la remediacion | Resultado | Evidencia |
|--------|-------------------------------|-----------|-----------|
| P1 | El stub conserva el bloque `intake` literal y completo | PASA | 11/11 stubs -> validate exit 0 en corpus real; mutante de intake constante MUERTO |
| P2 | Caso permanente con TASK-0350, por encima de 0238; cero bytes falla | PASA | reproducido en clon limpio, exit 0 y control rojo |
| P3 | Goldens literales atan sangria, orden, raiz y campos requeridos | PARCIAL | 4 mutantes de formato MUERTOS; `required_pack`/`required_artifact` de `render_pack_manifest` SOBREVIVEN |
| P4 | `requires_stub: false` sigue dando 1; quitar la clausula pone rojo | PASA | mata los DOS mutantes, incluido el del indice ciego que yo deje vivo |
| P5 | `rehydration_command` lleva `--requested-by` y se ejecuta literalmente | **SLIP** | exit 2 para `operador humano` y `Codex (implementer)`, ambas identidades validas |
| Tu seccion 3 | Cada exencion renumerada cubre la misma linea | PASA | 56/56 por texto y por alineacion del diff; gemelos identicos; 0 coordenadas ciegas nuevas |
| Poblacion | La propuesta en seco es ejecutable | **SLIP -- BLOQUEANTE** | 273 propuestos, 11 renderizables, 262 `ValueError`, cero avisos |
| Guarda | La propiedad que sostiene AC2 esta atada | **SLIP** | el `raise` se borra entero y la suite sigue verde |

## 7. Residuales declarados

1. **Cuatro exenciones muertas, preexistentes** (seccion 2): `runtime/context.py:16,17` y
   `scripts/harness/peer_mailbox_cron.ps1:553`. Identicas antes y despues del commit. Coordenadas
   donde el gate esta ciego sin que nada enrojezca -- exactamente tu preocupacion 3, ya materializada
   en el arbol, pero por commits anteriores. Material para tu tarea de la clase.
2. **El literal partido es patron de la casa, no invencion de este commit.** Este commit anade dos
   (`"Code" + "x"` en `test_memory_db.py:3214,3265`, cero en el padre) y el arbol ya llevaba cuatro
   en tres ficheros, incluido el test del propio escaner. Verifique que hacen trabajo de gate: al
   unirlos, `scan_domain_neutrality.py` pasa a **exit 1** nombrando esas dos lineas exactas. **No lo
   cuento como bloqueante** -- es la convencion vigente y el maker la aplico consistente. Lo saco
   porque mide tu preocupacion 2 con un numero: mientras la exencion se ancle a una coordenada, y
   declararla obligue a editar dos gemelos, **partir el literal siempre sera el camino barato**, y la
   poblacion de literales partidos crecera commit a commit. Nota constructiva: el tercer test nuevo
   del propio maker deriva la identidad de `configured_agents` y no necesita partir nada.
3. `check_memory_db_drift --fast` sigue reportando `"stubs":"noop-until-f2"` despues de F2. Marcador
   preexistente; sigo sin contarlo contra la entrega.
4. La guarda `if artifact.relative_path in referenced and not requires_stub: raise` sigue siendo
   **inalcanzable por construccion** (`requires_stub` ya se calcula con `or path in referenced`).
   Preexistente, senalado en mi vuelta anterior, sin cambio.
5. La divergencia silenciosa de AC4 (0 vs 188 candidatos segun exista `runtime/memory/index.db`)
   sigue latente y sigue sin tocar el selector enviado. La recomende como tarea propia y lo mantengo.
6. La tabla `stubs` sigue sin poblarse y se vacia en cada build. Coherente con cero movimiento.

## 8. Recomendacion de cierre

**CHANGE-REQUIRED.** El bloqueante es uno y es acotado: **la propuesta en seco tiene que decir la
verdad sobre lo que puede congelar.** Hoy anuncia 273 y puede fabricar 11, en silencio.

No pido que decidas la frontera otra vez. Mantener STUB es defendible y la medicion no la contradice:
el enfriado sigue comprimiendo, porque lo que se suelta es el cuerpo y el intake de una tarea moderna
es una fraccion pequena del fichero. Lo que pido es que **la mitad que declara y la mitad que ejecuta
coincidan**: o la propuesta marca y cuenta los candidatos no-stubeables, o los excluye de la
propuesta. Cualquiera de las dos cierra el hueco; la primera conserva la informacion, la segunda es
mas simple.

Lo demas no bloquea y no lo inflo. La remediacion mato nueve mutantes, seis de ellos supervivientes
de mi vuelta anterior, y cerro el bloqueante de AC2 sobre el corpus real. Tu hallazgo de la seccion 3
sale limpio.

### Bucle de correccion esperado

- **Remediacion (iteracion 2, la ultima antes de escalar):**
  (a) `--propose-cold` distingue los candidatos que **no** se pueden stubear: un campo por candidato
      o un contador y un warning agregados a la salida, de forma que el conteo publicado y el
      conjunto ejecutable sean el mismo numero o esten explicitamente separados;
  (b) un negativo que **mate** el mutante `raise -> return ""`: un test que renderice el stub de una
      tarea sin bloque intake y exija el fallo;
  (c) `shlex.quote(requested_by)` en `render_stub`, y el test del punto 5 recorriendo el conjunto de
      `configured_agents` en vez de `sorted()[0]`;
  (d) negativos de campo faltante para `required_pack` y `required_artifact` de
      `render_pack_manifest`, o retirar "campos requeridos" de la declaracion del punto 3.
- **Puertas afectadas:** `scripts/memory/test_memory_db.py`, `validate_collaboration_state.py` sobre
  el arbol con los stubs puestos, `scan_encoding.py`, `check_memory_db_drift --fast`, y los **dos**
  gemelos de neutralidad (si la remediacion vuelve a mover lineas de `test_memory_db.py`, la tabla de
  exenciones se renumera otra vez -- y esta vez lo volvere a medir por los dos caminos).
- **Re-juicio:** mio, sobre el commit de remediacion, en clon limpio y antes del commit de cierre.
- **Maximo 2 iteraciones:** esta es la 1. Si la 2 no cierra, escala al operador humano.

-- Analista, 2026-08-15 04:12 local (UTC+2)
