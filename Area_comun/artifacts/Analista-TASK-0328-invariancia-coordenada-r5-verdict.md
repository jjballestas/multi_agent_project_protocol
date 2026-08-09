---
artifact_id: Analista-TASK-0328-invariancia-coordenada-r5-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-09T15:30:00Z
anchor_commit: 8ab9d5758254d841dc694550663a10de2f8801e7
verdict: CHANGE-REQUIRED
iteration: 6 (r5 del maker; sexto juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 4, invariancia por coordenada (commit `8ab9d575`)

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Commit bajo revision: `8ab9d5758254d841dc694550663a10de2f8801e7`
  (`fix(TASK-0328): bind PII exemptions to coordinates`). Ancestro de `origin/main` y de HEAD
  `5ba1a431`. Los seis commits posteriores tocan estado, mailbox y memoria: **ningun cambio de
  codigo despues del anclaje** (`git diff --stat 8ab9d575 HEAD` no toca `scripts/`).
- Clon limpio detached en `D:/Aegis_Scratch/multi_agent_project_protocol/analista-0328-r5/clone`
  (DECISION-0104). `git status --short` vacio. Los mutantes de produccion se aplican en una copia
  aparte (`.../mut1`), nunca sobre el clon.
- Motores de control cargados como MODULOS INDEPENDIENTES, no como regex copiadas a mano:
  - `f732292a:scripts/memory/build_memory_db.py` -- ultimo estado ANTES de TASK-0328 (base).
  - `9639535f:scripts/memory/build_memory_db.py` -- remediacion 3 (r3, la que refute).
  - `8ab9d575:scripts/memory/build_memory_db.py` -- el entregable (r4).
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri ningun
  gate de producto.
- Hora local del juicio: 2026-08-09 17:26 (UTC+2).

## Reproduccion -- gates en clon limpio sobre el commit exacto

    python scripts/memory/test_memory_db.py                   EXIT=0   (72 tests, 397.9 s)
    python scripts/check_falsification_contracts.py --root .   EXIT=0
    python scripts/validate_collaboration_state.py --root .    EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    python scripts/scan_encoding.py --root .                   EXIT=0

Los cinco gates estan verdes. Los dos escapes que documento abajo no los ve ninguno.

## Respuesta directa a tu pregunta

> Una cadena con forma de ruta en un campo que NO esta exento, marca?

**Si.** Y esa parte del arreglo esta bien hecha. La exencion ya no se infiere del valor: el llamador
entrega la coordenada y `validate_metadata` la pasa desde la clave real del frontmatter
(`coordinate=key`), `require_safe_text` desde el nombre real del campo (`coordinate=field`).

    valor                                              coord       base   r3     r4
    Area_comun/tasks/ES9121000418450200051332.md       None        True   False  True
    Area_comun/tasks/ES9121000418450200051332.md       title       True   False  True
    Area_comun/tasks/ES9121000418450200051332.md       selector    True   False  True
    Area_comun/tasks/ES9121000418450200051332.md       owner       True   False  True
    Area_comun/tasks/ES9121000418450200051332.md       file        True   False  True
    Area_comun/tasks/34600123456.md                    title       True   False  True
    Area_comun/archive/<IBAN>/pack.manifest.json       pack_id     True   False  True
    MSG-ES9121000418450200051332                       message_id  True   False  True
    TASK-34600123456                                   task_id     False  False  True

La silueta ya no queda exenta por parecerse a una ruta o a una identidad: queda exenta solo la
envoltura que la coordenada explica. Es el cambio de clase que pedi.

## Foco B -- las 12 detecciones y el 30,4 % (PASS)

Los doce vectores que registre en el veredicto anterior, recontados contra r4 **en su coordenada
real**:

    vector                                        base    r3     r4     estado
    D4 contigua dentro de un valor de ruta        True    False  True   RECUPERADA
    D5 contigua unida por barra                   True    False  True   RECUPERADA
    D6 contigua unida por barra inversa           True    False  True   RECUPERADA
    D7 contigua bajo un token de identidad        True    False  True   RECUPERADA
    D8 contigua checksum invalido en ruta         True    False  True   RECUPERADA
    G4 agrupada por BARRA                         False   False  True   RECUPERADA
    G5 agrupada por BARRA INVERSA                 False   False  True   RECUPERADA
    G6 agrupada por punto dentro de una ruta      False   False  True   RECUPERADA
    P2 telefono con un segmento de barra detras   True    False  True   RECUPERADA
    P3 telefono dentro de un valor de ruta        True    False  True   RECUPERADA
    C6 cuenta disfrazada de identidad             True    False  True   RECUPERADA
    C7 agrupada disfrazada de identidad           False   False  True   RECUPERADA

    12/12 recuperadas.

Y en el camino de produccion, que es donde importaba:

    validate_metadata(), clave `file`             base    r3        r4
      file = Area_comun/tasks/<IBAN>.md           RECHAZA ACEPTA    RECHAZA
      file = Area_comun/tasks/<telefono>.md       RECHAZA ACEPTA    RECHAZA
    require_safe_text(field='path')
      Area_comun/archive/<IBAN>/pack.manifest.json    RECHAZA ACEPTA RECHAZA
      Area_comun/archive/<telefono>/pack.manifest.json RECHAZA ACEPTA RECHAZA

Recuento del corpus gobernado sobre el propio commit, con `iter_source_paths` y `ALLOWLIST_KEYS`,
parser independiente:

    archivos gobernados                       3.479
    cadenas gobernadas evaluadas             22.608   (la entrega declara 22.608: coincide exacto)
    r3: cegadas por juego de caracteres       6.859   (30,3 %) -- incondicional, cualquier payload
    r4: cadenas en coordenada exenta          6.971   (30,8 %)
    r4: valor REESCRITO antes del heuristico  6.746   (29,8 %)

El 30,4 % **deja de estar ciego en el sentido que importaba**: sobre esas mismas 6.971 cadenas
gobernadas, inyectando el payload en la forma que la coordenada admite,

    payload inyectado                     coord. de identidad   coord. file
    IBAN contiguo valido                  0/6.758 ciegas        0/213 ciegas
    IBAN contiguo checksum invalido       0/6.758               0/213
    IBAN agrupado por puntos              0/6.758               0/213
    telefono                              0/6.758               0/213
    telefono pegado a una letra           6.758/6.758 (100 %)   213/213 (100 %)
    IBAN agrupado pegado a una palabra    6.758/6.758 (100 %)   213/213 (100 %)
    IBAN reagrupado con bloque 20xxxxxx   6.758/6.758 (100 %)   213/213 (100 %)

Es decir: la ceguera dejo de ser por coordenada y paso a ser **por forma del payload**. Cuatro
formas pasan limpias en las 6.971; tres formas siguen ciegas en el 100 % de ellas.

## Foco A -- la invariancia de coordenada: REFUTADA en cuatro clases

Mismo payload, cuatro coordenadas (desnudo / segmento de ruta gobernada / sufijo de identidad /
clave no exenta). El motor r4:

    payload                                     bare   file-seg  id-suffix  title   invariante
    ES9121000418450200051332                    True   True      True       True    SI
    ES0021000418450200051332 (checksum malo)    True   True      True       True    SI
    ES91.2100.0418.4502.0005.1332               True   True      True       True    SI
    34600123456                                 True   True      True       True    SI
    tel34600123456                              True   False     False      True    NO
    34600123456tel                              True   False     False      True    NO
    cuentaES91.2100.0418.4502.0005.1332         True   False     False      True    NO
    ES91-21000418450-20005133-2                 True   False     False      True    NO

Dos mecanismos nuevos rompen la invariancia, y ninguno de los dos mira la gramatica de la
coordenada:

**Mecanismo 1 -- el salto por adyacencia alfanumerica.** `account_identifier_grouped_is_detected` y
`phone_number_is_detected` reciben `coordinate_bound=True` **para toda coordenada exenta** (incluso
cuando `pii_values_for_coordinate` no reescribio nada porque el valor no era una ruta valida) y
descartan cualquier arranque o candidato pegado a un caracter alfanumerico. Eso es exactamente la
contaminacion por la izquierda y por la derecha que la remediacion 2 declaro cerrada -- reabierta,
ahora solo dentro de las coordenadas exentas.

**Mecanismo 2 -- la neutralizacion de fecha sobre el valor entero.**
`without_coordinate_timestamp` sustituye por `:` cualquier tirada aislada de 8 digitos que empiece
por 19 o 20, en **todo** el valor reescrito, no solo en la envoltura de identidad. Un identificador
de cuenta con checksum mod-97 valido reagrupado de modo que uno de sus bloques sea `20005133` queda
partido:

    identificador           ES91-21000418450-20005133-2   (mod-97 VALIDO, verificado)
    reescrito en `file`     Area_comun/tasks/ES91-21000418450-:-2
    bare / title            r4 = True
    file / path / task_id / message_id     r4 = False
    control mismo identificador agrupado sin bloque 19xx/20xx:
      ES91-2100-0418-4502-0005-1332        r4 = True en TODAS las coordenadas

El control aisla la causa: no es el agrupamiento, es la neutralizacion de fecha.

### Dos de las cuatro clases son PERDIDA contra el motor previo a la tarea

No son solo rupturas de invariancia: son detecciones que el gate tenia antes de que TASK-0328
empezara y que este commit apaga, en dos campos de produccion.

    validate_metadata(), clave `file`                      base      r3      r4
      Area_comun/tasks/tel34600123456.md                   RECHAZA   ACEPTA  ACEPTA  <== FUGA
      Area_comun/tasks/34600123456tel.md                   RECHAZA   ACEPTA  ACEPTA  <== FUGA
    require_safe_text(field='path')
      Area_comun/archive/tel34600123456/pack.manifest.json RECHAZA   ACEPTA  ACEPTA  <== FUGA
      Area_comun/archive/34600123456tel/pack.manifest.json RECHAZA   ACEPTA  ACEPTA  <== FUGA

## Foco D -- potencia de la medicion (PASS en la declaracion, PARCIAL en el alcance)

Es la cuarta version de esta medida y es la primera que **declara** su vacuidad en vez de
presentarla como resultado. Lo recuento y lo confirmo:

    corpus gobernado real, 22.608 cadenas
      positivos motor base (f732292a)      0
      positivos motor r4  (8ab9d575)       0
      ganadas 0 | perdidas 0
      POTENCIA para la direccion de perdida: 0 positivos previos --> VACUA, y la entrega
      lo declara literalmente "SIN PODER". Correcto.

La medicion separada con potencia que la entrega aporta (16 valores, 4 payloads x 4 coordenadas)
si tiene denominador: yo recuento **12 positivos previos, 16 actuales, 4 ganancias, 0 perdidas**
(la entrega declara 11 / 16 / 5 / 0; la diferencia de un valor es de parseo independiente y no
cambia el signo). Pero 16 valores construidos desde una tupla literal de 4 payloads no son una
poblacion: son una enumeracion. Ver foco C.

Mi poblacion con potencia, construida desde el arbol real (12 directorios gobernados reales, 10
prefijos de identidad reales extraidos del propio corpus, 8 formas de payload, coordenadas `file`,
`path`, `message_id`, desnuda y `title`):

    poblacion evaluada                      288 cadenas
    positivos motor base (f732292a)         150     <-- potencia real para la perdida
    positivos r3                             16
    positivos r4                            152
    GANADAS vs base                          50
    PERDIDAS vs base                         48     <-- todas en `file` y `path`
      por clase: telefono pegado por la izquierda   12 file + 12 path
                 telefono pegado por la derecha     12 file + 12 path

## Foco C -- el contrato ata la direccion de la perdida, pero solo sobre lo que enumera (SLIP)

Lo que el contrato gano, y es real: `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` ahora incluye
`assertGreater(sum(coordinate_previous_results), 0)` (potencia declarada),
`assertEqual(0, sum(previous and not current))` (**la direccion de la perdida**),
`assertTrue(all(coordinate_current_results))` y el mutante `coordinate_blind` que debe perder
positivos. Las aserciones son correctas.

Lo que no ata: el corpus sobre el que corren es una tupla literal de cuatro payloads
(`compact`, `invalid_contiguous`, `"ES91-2100-0418-4502-0005-1332"`, `"346-001-234-56"`), ninguno
adyacente a un alfanumerico y ninguno con un bloque `19xx`/`20xx`. Por construccion no puede
exhibir ninguno de los dos escapes.

Prueba falsable, sin tocar el motor ni las aserciones -- solo anadiendo cuatro formas al corpus:

    corpus enviado (4 payloads x 4 coordenadas), commit 8ab9d575
      assertGreater(sum(previous), 0)      12   PASS
      assertEqual(0, sum(prev & !curr))     0   PASS
      assertTrue(all(current))          16/16   PASS

    mismo motor, mismo commit, mismas aserciones, corpus + 4 formas de esta revision
      assertGreater(sum(previous), 0)      20   PASS
      assertEqual(0, sum(prev & !curr))     6   FAIL   <== la perdida existe y el contrato no la ve
      assertTrue(all(current))          20/32   FAIL

Dos detalles mas del contrato, no bloqueantes pero registrados: el "motor anterior" es una regex
copiada a mano (`\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b`) mas `phone_band_detects`, que usa el
`PHONE_CANDIDATE_RE` **actual**, no el modulo previo real; y el mutante `coordinate_blind` es un
cegado total, incapaz de ver un cegado parcial. La medicion grande de 5.400 positivos si genera sus
contextos desde la condicion de arranque del patron: el corpus de coordenada retrocedio a lista
manual respecto de esa.

## Foco E -- sin regresion (PASS en lo contiguo, GAP en lo agrupado)

La cobertura contigua vuelve a ser incondicional **en todas las coordenadas**, con y sin checksum,
y la contaminacion queda cerrada por las tres posiciones:

    presentacion                        None   title  file  path  message_id  task_id
    contigua valida (20 contextos)      20/20  20/20  4/4   4/4   20/20       20/20
    contigua checksum INVALIDO          20/20  20/20  4/4   4/4   20/20       20/20
    contaminacion izquierda/derecha/ambas sobre Area_comun/tasks/<IBAN>.md:
      todas las coordenadas             True   True   True  True  True        True

El gap esta en la presentacion agrupada dentro de coordenada exenta, misma causa que el foco A:

    agrupada por espacios               20/20  20/20   --    --   16/20       16/20
    las 4 que faltan son las de contexto izquierdo pegado: "xES91 2100 0418 4502 0005 1332"

## Las DOS cifras que pediste antes de una decision

Medidas sobre el corpus gobernado real (precision) y sobre la poblacion con potencia (deteccion),
apagando cada mecanismo por separado en una copia del clon:

    mecanismo                        compra (falsos positivos evitados     paga (perdidas vs
                                      sobre las 22.608 gobernadas)          base, poblacion 288)
    salto por adyacencia                  16                                    48
    neutralizacion de fecha                2                                     0 vs base
                                                                                (34 rupturas de
                                                                                 invariancia)
    los dos apagados a la vez              0 falsos positivos evitados            0 perdidas

Los dos son portantes: quitar el salto de adyacencia hace FALLAR
`test_account_identifier_presentations_are_structural_and_falsifiable` por
`governed_identity_hits != []` (verificado, `FAILED (failures=1)`); quitar la neutralizacion de
fecha hace fallar ese mismo test y ademas `test_p05_protocol_timestamp_id_is_not_a_phone`
(verificado, `FAILED (failures=2)`). No se pueden borrar sin mas.

Y el dato que creo decisivo para tu decision: **los 16 falsos positivos que el salto de adyacencia
compra no son payload ajeno, son el cuerpo de la propia identidad gobernada**:

    key=file        Area_comun/tasks/TASK-0136-codex-reconcile-intake-canonical-red.md
                    reescrito -> Area_comun/tasks/0136-codex-reconcile-intake-canonical-red.md
    key=file        Area_comun/tasks/TASK-0340-el-validador-canonico-lleva-seis-dias-crashing-en-CI.md
    key=message_id  MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio-NOGO
                    reescrito -> :-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio-NOGO
    key=task_id     REQ-885632826E  ->  885632826E  (cae en la banda telefonica de 9-15 digitos)

    8 message_id + 7 file + 1 task_id = 16.  Ninguno es un dato personal.

Es decir: el reescrito por coordenada quita **menos** envoltura de la que la gramatica de esa
coordenada explica (deja el numero de tarea, el slug y el cuerpo del REQ expuestos al heuristico),
y los dos supresores existen para tapar los falsos positivos que ese reescrito insuficiente genera.
El coste de tapar asi es la perdida de 48 detecciones. No propongo la forma; senalo que la tension
que estas pagando no es "precision contra deteccion", es "la envoltura exenta esta mal delimitada".

## Tabla vector-a-vector

    foco  criterio prometido                                              resultado
    A     cadena con forma de ruta en campo NO exento marca               PASS (9/9 vectores)
    A     la exencion procede de la coordenada, no del parecido           PASS (provenance-bound
                                                                          en los dos call sites)
    A     mismo payload, mismo veredicto al cambiar de coordenada         REFUTADO (4 de 8 clases)
    A     ninguna perdida contra el motor previo a la tarea               REFUTADO (2 clases, en
                                                                          `file` y `path`)
    B     las 12 detecciones recuperadas                                  PASS (12/12)
    B     el 30,4 % deja de estar ciego                                   PASS con matiz: la
                                                                          ceguera pasa de ser por
                                                                          coordenada a ser por
                                                                          forma del payload
                                                                          (3 formas, 100 % de 6.971)
    C     el contrato ata la direccion de la perdida                      PASS en la asercion,
                                                                          SLIP en el corpus
                                                                          (0 -> 6 perdidas al
                                                                           anadir 4 formas)
    D     el corpus exhibe lo que mide o se declara sin poder             PASS (declarado SIN PODER
                                                                          y confirmado 0/0)
    D     medicion separada con potencia                                  PASS aritmetico
                                                                          (12/16/4/0 recontado),
                                                                          SLIP: 4 payloads literales
    E     cobertura contigua incondicional, con y sin checksum            PASS en 6 coordenadas
    E     contaminacion cerrada por las tres posiciones                   PASS (contigua)
    E     idem sobre la presentacion agrupada                             GAP (16/20 en identidad)

    PERDIDAS confirmadas contra el motor previo a la tarea: 2 clases de payload,
    48 renderizaciones sobre 288, todas en las coordenadas `file` y `path`.
    RUPTURAS de invariancia de coordenada: 4 clases de payload de 8.

## Propiedad que la remediacion debe satisfacer (no propongo la forma)

La misma de la vuelta anterior, sin ceder y sin ampliarla:

**Una exencion solo puede suprimir un heuristico sobre la parte del token que la gramatica de la
coordenada explica integramente; sobre el resto, el heuristico corre sin atenuar.** Operacionalmente:
el mismo payload, movido entre valor desnudo, segmento de ruta gobernada y sufijo de identidad, debe
dar el MISMO veredicto -- incluido cuando esta pegado a un alfanumerico y cuando uno de sus bloques
tiene forma de fecha.

Y sobre la medicion: el corpus que mide la direccion de la perdida no puede ser una tupla literal de
payloads. Debe derivar sus formas de la condicion que el propio motor evalua -- adyacencia,
separadores admitidos, longitudes de bloque -- como ya hace la medicion de 5.400 positivos. Si un
corpus no tiene potencia, declararlo (esta vuelta se hizo bien) y medir aparte con uno que la tenga.

## Residuales declarados

- No re-juzgue R1-R5 de la remediacion 2 (separadores no admitidos, minimo estructural de 14,
  identificadores nacionales sin mod-97, generacion de contextos, tasa de sobre-deteccion de la
  forma agrupada). Quedan como estaban.
- No corri gates de producto: el Arquitecto declaro SIN PRODUCTO EN ALCANCE.
- No medi coste en tiempo ni en memoria del reescrito por coordenada; es irrelevante para este
  veredicto.
- `require_safe_text(field='path')` evalua la PII antes de validar `PATH_RE` (la validacion esta
  despues, en `load_cold_packs`). `pii_values_for_coordinate` revalida por su cuenta y cae a
  `(item,)`, asi que no hay fuga por ahi; pero `coordinate_bound` sigue en `True` para un valor que
  no es una ruta. Lo registro como asimetria, no como fuga.
- Las 7 advertencias de `context_refs` del validador son preexistentes y ajenas a esta tarea.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

La remediacion 4 es la primera de las cuatro que cambia de clase en vez de estrechar una forma: la
exencion pasa a estar atada a la coordenada que el llamador declara, recupera 12 de 12 detecciones,
cierra las dos fugas de produccion que refute, y declara honestamente que su corpus grande no tiene
potencia. Eso hay que reconocerlo.

Lo que impide cerrar es que la propiedad que da titulo a la remediacion -- la invariancia de
coordenada -- queda refutada en 4 de 8 clases de payload, y 2 de ellas son perdida contra el motor
anterior a la tarea en `validate_metadata(file=...)` y `require_safe_text(field='path')`. El
contrato que deberia haberlo visto tiene la asercion correcta sobre un corpus que no puede
exhibirlo.

## Bucle de correccion declarado

- Remediacion: 5. **Es la ultima iteracion del presupuesto que declare en el veredicto anterior**
  (maximo 2 antes de escalar; esta es la segunda).
- Gates afectados: `scripts/memory/test_memory_db.py`, `scripts/check_falsification_contracts.py`,
  `scripts/validate_collaboration_state.py`, `scripts/scan_domain_neutrality.py`,
  `scripts/scan_encoding.py`.
- Re-juicio del checker ANTES del commit de cierre.
- Senal para el Arquitecto (DECISION-0018): pediste las dos cifras antes que una decision y estan en
  la seccion correspondiente. Dado que los dos supresores son portantes y que los 16 falsos
  positivos que compran son cuerpo de identidad gobernada y no datos personales, la eleccion entre
  (a) delimitar bien la envoltura exenta en una remediacion 5, y (b) cerrar declarando las dos
  clases de fuga como residual explicito con sus cifras, es tuya y del operador, no mia. Lo que no
  es cerrable es declarar invariancia de coordenada mientras 4 clases la rompen y 2 pierden contra
  el motor previo.

-- Analista
