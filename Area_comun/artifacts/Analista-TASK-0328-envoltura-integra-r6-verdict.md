---
artifact_id: Analista-TASK-0328-envoltura-integra-r6-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-09T18:37:52Z
anchor_commit: df5de987a0eda5106d1267cd2b052e6c55686692
verdict: CHANGE-REQUIRED
iteration: 7 (r6 del maker; septimo juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 5, envolturas de coordenada integras (commit `df5de987`)

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Commit bajo revision: `df5de987a0eda5106d1267cd2b052e6c55686692`
  (`fix(TASK-0328): delimit integral coordinate envelopes`). Ancestro de `origin/main`.
  Los cinco commits posteriores tocan estado, mailbox, veredictos y memoria:
  `git diff --stat df5de987 origin/main -- scripts/` sale VACIO. **Ningun cambio de codigo
  despues del anclaje.**
- Clon limpio detached en `D:/Aegis_Scratch/multi_agent_project_protocol/an0328r6`
  (DECISION-0104). `git status --short` vacio. Los tres motores se cargan como MODULOS
  INDEPENDIENTES extraidos por `git show`, ninguna regex copiada a mano:
  - `f732292a:scripts/memory/build_memory_db.py` -- estado ANTES de TASK-0328 (base).
  - `8ab9d575:...` -- remediacion 4 (r5, la que refute en 4 clases).
  - `df5de987:...` -- el entregable (r6).
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri
  ningun gate de producto.
- Hora local del juicio: 2026-08-09 20:37 (UTC+2).

## Reproduccion -- gates en clon limpio sobre el commit exacto

    python scripts/memory/test_memory_db.py                   EXIT=0   (72 tests, 358.2 s)
    python scripts/check_falsification_contracts.py --root .   EXIT=0
    python scripts/validate_collaboration_state.py --root .    EXIT=0
    python scripts/scan_domain_neutrality.py --root .          EXIT=0
    python scripts/scan_encoding.py --root .                   EXIT=0

Los cinco gates estan verdes. Nada de lo que documento abajo lo ve ninguno.

## Respuesta directa a tu pregunta

> Queda alguna clase de payload donde la exencion suprima el heuristico sobre una parte del
> token que la gramatica de la coordenada NO explica?

**Si, y ademas hay una clase peor: la exencion suprime el heuristico sobre el token ENTERO.**

Dos mecanismos nuevos, los dos dentro de `unexplained_identity_parts`:

**Mecanismo 3 -- la trituracion del remanente.** Tras quitar la envoltura, el resto se parte con
`re.split(r"[-._]+", remainder)` y cada fragmento se evalua POR SEPARADO. Un identificador de
cuenta o un telefono agrupado por `-`, `.` o `_` -- que son exactamente tres de los separadores
que el propio motor admite en `ACCOUNT_IDENTIFIER_SEPARATORS_RE` -- se convierte en trozos de
2 a 6 caracteres, ninguno de los cuales alcanza el minimo estructural de 14 ni la banda
telefonica de 9-15 digitos. La presentacion agrupada, que es el objeto entero de TASK-0328,
queda ciega dentro de toda envoltura gobernada.

**Mecanismo 4 -- la exencion total.** `COORDINATE_COMPLETE_OPERATIONAL_ID_RE` devuelve `()`.
Con `pii_values` vacio, los tres `any(...)` de `contains_pii` son False por vacuidad: **no se
ejecuta ningun heuristico**. Y el patron es `^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*(?:\.\d+)*)+-(?:19|20)\d{6}$`
con `re.I`: el bloque `[A-Z][A-Z0-9]*` acepta un identificador de cuenta contiguo completo.
Lo mismo `COORDINATE_MESSAGE_ENVELOPE_RE`, cuyo hueco de actor `-[A-Z][A-Z0-9]*` se traga un
identificador contiguo entero y deja remanente vacio.

    valor                                                  coord        base   r5     r6
    REQ-ES9121000418450200051332-20260809                  task_id      True   True   False
    REQ-ES0021000418450200051332-20260809                  task_id      True   True   False
    TASK-ES9121000418450200051332-20260809                 task_id      True   True   False
    DEC-ES9121000418450200051332-19991231                  decision_id  True   True   False
    MSG-20260809-ES9121000418450200051332                  message_id   True   True   False
    MSG-20260809-ES9121000418450200051332-to-Arquitecto    message_id   True   True   False
    Area_comun/tasks/REQ-ES9121000418450200051332-20260809.md   file    True   True   False

`ES9121000418450200051332` es la forma CONTIGUA, mod-97 valida. La entrega declara la cobertura
contigua "incondicional". No lo es.

## Foco A -- las cuatro clases refutadas en r5: LAS CUATRO MUERTAS (PASS)

Los dos mecanismos que refute en r5 estan retirados de raiz: `coordinate_bound = False`
incondicional (muere el salto por adyacencia) y `without_coordinate_timestamp` eliminado
(muere la neutralizacion de fecha). Recuento sobre el commit:

    payload                              coord        base   r5      r6      estado
    tel34600123456                       file         True   False   True    PERDIDA CERRADA
    tel34600123456                       path         True   False   True    PERDIDA CERRADA
    34600123456tel                       file         True   False   True    PERDIDA CERRADA
    34600123456tel                       path         True   False   True    PERDIDA CERRADA
    tel34600123456                       task_id      False  False   True    GANADA
    34600123456tel                       message_id   False  False   True    GANADA
    ES91-21000418450-20005133-2          file/path    False  False   True    RECUPERADA
    ES91-21000418450-20005133-2          task_id      False  False   True    RECUPERADA
    ES91-21000418450-20005133-2          message_id   False  False   True    RECUPERADA

**Las dos clases de PERDIDA contra el motor previo estan cerradas.** Es el foco que pusiste
primero y esta resuelto. Lo digo sin matiz porque es merito real.

Queda una de las cuatro viva, y por causa nueva:

    cuentaES91.2100.0418.4502.0005.1332  bare/title/file/path  r6 = True
    cuentaES91.2100.0418.4502.0005.1332  task_id / message_id  r6 = False   <== mecanismo 3

## Foco B -- el token explicado SOLO EN PARTE: REFUTADO

Es la prueba que pediste literalmente. Token con envoltura valida mas resto:

    TASK-0328-ES91-2100-0418-4502-0005-1332          task_id      base False  r5 True  r6 False
    TASK-0328-ES91.2100.0418.4502.0005.1332          task_id      base False  r5 True  r6 False
    TASK-0328-ES91_2100_0418_4502_0005_1332          task_id      base False  r5 True  r6 False
    REQ-885632826E-ES91-2100-0418-4502-0005-1332     task_id      base False  r5 True  r6 False
    ANALISTA-TASK-0328-ES91-2100-...-1332            task_id      base False  r5 True  r6 False
    MSG-20260809-Analista-to-Arquitecto-REVIEW-ES91-2100-...      base False  r5 True  r6 False
    Area_comun/tasks/TASK-0328-ES91-2100-...-1332.md file         base False  r5 True  r6 False
    Area_comun/archive/TASK-0328-ES91-2100-...-1332/pack.manifest.json  path  r5 True  r6 False
    Area_comun/tasks/TASK-0328-346-001-234-56.md     file         base TRUE   r5 True  r6 False
    Area_comun/archive/TASK-0328-346-001-234-56/pack.manifest.json path base TRUE r5 True r6 False

La gramatica de `task_id` explica `TASK-0328-`. NO explica `ES91-2100-0418-4502-0005-1332`.
La parte sobrante **si se exime**: se tritura y desaparece. Las dos ultimas filas son ademas
**perdida contra el motor previo a la tarea** en `validate_metadata(file=...)` y
`require_safe_text(field='path')` -- los mismos dos campos de produccion de la vuelta anterior,
con otro payload.

Los dos sitios de llamada de produccion, verificados directamente:

    validate_metadata({"task_id": "TASK-0328-ES91-2100-0418-4502-0005-1332"})
      -> accepted={'task_id': 'TASK-0328-ES91-2100-0418-4502-0005-1332'}   warnings=[]
    validate_metadata({"task_id": "REQ-ES9121000418450200051332-20260809"})
      -> accepted={'task_id': 'REQ-ES9121000418450200051332-20260809'}      warnings=[]
    validate_metadata({"file": "Area_comun/tasks/TASK-0328-346-001-234-56.md"})
      -> accepted={...}   warnings=[]
    require_safe_text("Area_comun/archive/TASK-0328-346-001-234-56/pack.manifest.json", "path")
      -> ACCEPTED (no raise)
    require_safe_text("Area_comun/archive/REQ-ES9121000418450200051332-20260809/pack.manifest.json", "path")
      -> ACCEPTED (no raise)

## Foco C -- el corpus deriva de la condicion: PASS en el eje del payload, REFUTADO en el eje de la coordenada

Reconozco lo ganado: las formas agrupadas ya no son una tupla literal. Salen de
`ACCOUNT_IDENTIFIER_SEPARATORS_RE` recorrida por puntos de codigo, de `ACCOUNT_IDENTIFIER_MIN_LENGTH`
/ `MAX_LENGTH` y de longitudes de bloque `range(1, len(compact))`. Ese eje esta bien hecho y es
lo que pediste.

El eje que quedo sin derivar es el otro, y es el que importa: **la RENDERIZACION en coordenada
sigue siendo una tupla literal escrita a mano** --

    ("file",       f"Area_comun/tasks/{payload}.md"),
    ("task_id",    f"TASK-{payload}"),
    ("path",       f"Area_comun/archive/{payload}/pack.manifest.json"),
    ("message_id", f"MSG-{payload}"),

-- y ninguna de esas cuatro formas produce una envoltura gobernada valida. `TASK-<IBAN>` no
casa `COORDINATE_ID_ENVELOPE_RE` (exige `\d{4}`); `MSG-<IBAN>` no casa
`COORDINATE_MESSAGE_ENVELOPE_RE` (exige `(?:19|20)\d{6}`). En los cuatro casos
`unexplained_identity_parts` cae al ramal de escape `return (value,)` y devuelve el valor
INTACTO. Medido sobre el corpus que el propio contrato genera:

    payloads generados desde la condicion del motor                     202
    renderizaciones de identidad cuya envoltura CASA (ramal de exencion)  0

**El corpus de coordenada no ejerce la exencion ni una sola vez.** Prueba las 202 formas contra
el ramal de escape. Las unicas cadenas que si llegan al ramal de exencion son las de
`clean_coordinates`, que son controles LIMPIOS: nunca llevan payload. Los tres mutantes nuevos
(`coordinate_blind`, `coordinate_adjacency_blind`, `coordinate_date_blind`) mueren, si -- pero
mueren en el ramal de escape, no en el codigo que la remediacion escribio.

### Prueba falsable, sin tocar el motor ni las aserciones

Replico las aserciones de `NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` tal como se entregan,
primero sobre el corpus enviado y despues sobre el MISMO corpus con **una** renderizacion mas:
la envoltura gobernada real. Mismo motor, mismo commit.

    corpus TAL COMO SE ENVIA (n=940)
      assertGreater(sum(coordinate_previous_results), 0)      44      PASS
      assertTrue(all(coordinate_current_results))          940/940    PASS
      previous and not current                                 0      PASS

    mismo corpus + envoltura gobernada real (n=1880)
      assertGreater(sum(coordinate_previous_results), 0)      88      PASS
      assertTrue(all(coordinate_current_results))         1676/1880   FAIL  (204 ciegas)
      assertEqual({}, accepted_file)   sobre 85 payloads     51 ACEPTADOS   FAIL
      assertRaisesRegex("path contains prohibited PII")      51 NO LANZAN   FAIL

Las dos aserciones de produccion que la remediacion 5 anadio -- que son su mejor idea -- fallan
sobre sus propios payloads en cuanto el nombre del fichero lleva la envoltura que un fichero
gobernado lleva siempre.

### Formas que el autor no anticipo (las anado como pediste)

1. **Mezcla de separadores dentro de la envoltura.** El corpus fija UN separador por forma;
   la condicion del motor admite mezclarlos.

        ES91-2100.0418_4502-0005.1332                     desnudo    r6 = True
        TASK-0328-ES91-2100.0418_4502-0005.1332           task_id    r6 = False
        MSG-20260809-Codex-ES91-2100.0418_4502-0005.1332  message_id r6 = False
        Area_comun/tasks/TASK-0328-ES91-2100.0418_4502-0005.1332.md  file  base=True r6=False

2. **El identificador de exencion total usado como segmento de ruta.** El corpus solo lo
   probaria como valor de identidad; la ruta lo hereda por `pii_values_for_coordinate`.

        Area_comun/tasks/REQ-ES9121000418450200051332-20260809.md    base=True  r6=False
        Area_comun/archive/REQ-ES9121000418450200051332-20260809/pack.manifest.json
                                                        require_safe_text -> ACEPTA

3. **La envoltura de actor recursiva.** `ANALISTA-TASK-0328-<payload>` consume dos envolturas
   antes de triturar; el corpus nunca la ejercita.

## Foco D -- sin regresion: REFUTADO en la cobertura contigua

    prometido                                        resultado
    las 12 detecciones recuperadas siguen            PASS (12/12 recontadas, ver foco A)
    la cobertura contigua sigue incondicional        REFUTADO: 7 formas de exencion total
                                                     apagan un contiguo mod-97 VALIDO
                                                     (base True -> r6 False)
    contaminacion cerrada por las tres posiciones    PASS en valor desnudo, title, file, path;
                                                     REFUTADO en task_id/message_id para la
                                                     forma agrupada (mecanismo 3)

## Poblacion con potencia y cifras

Poblacion derivada de la condicion del motor (separadores admitidos x bloques 2/3/4/6 +
telefono agrupado + contiguo) renderizada en las envolturas gobernadas REALES que las
propias regex del motor definen (`TASK-####-`, `DECISION-####-`, `SPEC-####-`, `REQ-<hex>-`,
`<ACTOR>-TASK-####-`, `MSG-<fecha>-<actor>[-to-<actor>][-TIPO]-`, y sus derivados en `file`
y `path`):

    renderizaciones evaluadas                    153
    positivos motor r5 (8ab9d575)                144      <-- potencia real
    positivos motor r6 (df5de987)                 18
    PERDIDAS vs r5                               126
    PERDIDAS vs el motor previo a la tarea         4      (telefono agrupado en `file` y `path`)
                                                          + las 7 de exencion total del foco B

    las mismas 4 renderizaciones que ENVIA el contrato, mismo payload:
    renderizaciones evaluadas                     68
    positivos r5                                  64
    positivos r6                                  64
    PERDIDAS                                       0      <-- por eso el gate esta verde

Y el precio, que es la cifra que pediste antes de decidir. Medido sobre el corpus gobernado
real del propio commit (`iter_source_paths` + `parse_frontmatter` + `ALLOWLIST_KEYS`, parser
independiente):

    ficheros gobernados                                        4.603
    cadenas gobernadas en clave permitida                     22.663
    cadenas de identidad que LLEGAN al ramal de exencion       6.660
      de esas, remanente TRITURADO en mas de un trozo          1.970
      de esas, valor DESCARTADO entero (parts = ())            4.371

    PRECIO de conservar el remanente ENTERO (sin partir por [-._]):
      10 falsos positivos nuevos sobre 6.446 cadenas de identidad
      (p.ej. MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio-NOGO,
             OPS-MEDICION-H1-H3-20260630, DIRECTIVA-OPERADOR-F0.1-20260702)

    PRECIO de `COORDINATE_COMPLETE_OPERATIONAL_ID_RE`:
      exime 7 valores gobernados distintos; de esos, solo 2 serian falsos positivos
      (DIRECTIVA-OPERADOR-F0.1-20260702 y OPS-MEDICION-H1-H3-20260630).
      Compra 2 supresiones y paga ceguera TOTAL sobre un contiguo valido.

La trituracion compra **10** y paga **126**. La exencion total compra **2** y paga la unica
propiedad que el gate tenia incondicional.

## Tabla vector-a-vector

    foco  criterio prometido                                          resultado
    A     tel34600123456 en `file`/`path` vuelve a marcar             PASS
    A     34600123456tel en `file`/`path` vuelve a marcar             PASS
    A     cuentaES91.2100... invariante                               SLIP (False en task_id
                                                                       y message_id)
    A     ES91-21000418450-20005133-2 invariante                      PASS (6/6 coordenadas)
    A     salto por adyacencia retirado                               PASS (coordinate_bound=False)
    A     neutralizacion de fecha retirada                            PASS (funcion eliminada)
    B     la parte sobrante NO se exime                               REFUTADO (mecanismo 3,
                                                                       126/144 perdidas)
    B     la exencion nunca cubre el token entero                     REFUTADO (mecanismo 4,
                                                                       7 formas, contiguo valido)
    C     el corpus deriva de la condicion (payload)                  PASS
    C     el corpus deriva de la condicion (coordenada)               REFUTADO (0 de 202
                                                                       renderizaciones alcanzan
                                                                       el ramal de exencion)
    C     forma no anticipada por el autor                            APORTADAS 3, las tres pasan
    D     las 12 detecciones recuperadas siguen                       PASS (12/12)
    D     cobertura contigua incondicional                            REFUTADO (7 formas)
    D     contaminacion cerrada por las tres posiciones               PASS en 4 coordenadas,
                                                                       GAP en task_id/message_id
    -     los 5 gates verdes en clon limpio                           PASS (exit 0 los cinco)

## Residuales declarados

- No re-juzgue R1-R5 de la remediacion 2 (separadores no admitidos, minimo estructural de 14,
  identificadores nacionales sin mod-97, tasa de sobre-deteccion de la forma agrupada). Quedan
  como estaban.
- Sigue en pie del veredicto anterior: el "motor anterior" del contrato es una regex copiada a
  mano (`\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b`), que no ve ninguna forma agrupada; por eso la
  asercion de direccion de perdida (`previous and not current`) da 0 incluso sobre mi corpus
  ampliado. La asercion es correcta y su oraculo sigue siendo ciego a la clase que mide.
- No corri gates de producto: SIN PRODUCTO EN ALCANCE.
- No medi coste en tiempo ni memoria del troceado; irrelevante para este veredicto.
- Los 4.371 valores con `parts = ()` incluyen el caso legitimo y correcto en que la envoltura
  agota el valor (`TASK-0229`). Lo separo del mecanismo 4 y no lo cuento como defecto.
- Las advertencias de `context_refs` del validador son preexistentes y ajenas a esta tarea.

## Propiedad que la remediacion debe satisfacer (no propongo la forma)

Sin cambiarla y sin ampliarla, con la precision que esta vuelta obliga a anadir:

**Una exencion solo puede suprimir el heuristico sobre la parte del token que la gramatica de
la coordenada explica integramente; sobre el resto, el heuristico corre sin atenuar Y SIN
FRAGMENTAR.** Quitar la envoltura no autoriza a partir lo que queda: el remanente se evalua
como una sola cadena, porque los separadores por los que se parte son separadores que el propio
motor admite dentro de un identificador. Y ninguna coordenada puede producir remanente vacio
sobre un token cuyo cuerpo no ha sido explicado pieza a pieza.

Sobre la medicion: el corpus ya deriva sus payloads de la condicion; **debe derivar tambien sus
renderizaciones**. Si la renderizacion no produce una envoltura que las regex de exencion
reconocen, el corpus no esta midiendo la exencion -- esta midiendo el ramal de escape. Una
comprobacion barata y falsable: afirmar que un numero >0 de renderizaciones del corpus llega al
ramal de exencion (`pii_values_for_coordinate(item, coord) != (item,)`).

## Recomendacion de cierre

**CHANGE-REQUIRED.**

## Bucle de correccion declarado -- presupuesto AGOTADO, escalo

- En el veredicto r5 declare maximo 2 iteraciones antes de escalar y dije que aquella era la
  segunda. Esta es la tercera. **Mi presupuesto esta agotado: escalo al operador humano.**
- Gates afectados si se abre una remediacion 6: `scripts/memory/test_memory_db.py`,
  `scripts/check_falsification_contracts.py`, `scripts/validate_collaboration_state.py`,
  `scripts/scan_domain_neutrality.py`, `scripts/scan_encoding.py`. Re-juicio del checker ANTES
  del commit de cierre.
- **Senal explicita para el Arquitecto y el operador (DECISION-0018).** Anunciaste que, si no
  cerraba, subirias al operador la opcion de cerrar declarando las dos perdidas conocidas con
  sus cifras. Esa opcion ya no es la que esta sobre la mesa, y quiero que quede escrito por que:
  **las dos perdidas que ibas a declarar como residual estan CERRADAS por esta remediacion.**
  Lo que queda abierto es otra cosa y es mas grande: un identificador de cuenta contiguo,
  mod-97 valido, atraviesa `validate_metadata` y `require_safe_text` en tres formas de
  identidad gobernada, y toda presentacion agrupada queda ciega dentro de cualquier envoltura
  gobernada. Cerrar hoy no seria cerrar con dos perdidas declaradas: seria cerrar con la
  cobertura contigua -- la unica que el gate tenia incondicional desde antes de la tarea --
  perdida en produccion.
- La decision es del operador, no mia. Le doy las cifras que necesita para tomarla: la
  trituracion compra 10 falsos positivos y paga 126 detecciones; la exencion total compra 2 y
  paga la cobertura contigua. Y le doy la comprobacion que habria hecho visible todo esto y que
  cuesta una linea: exigir que el corpus de coordenada alcance el ramal de exencion al menos
  una vez.

-- Analista
