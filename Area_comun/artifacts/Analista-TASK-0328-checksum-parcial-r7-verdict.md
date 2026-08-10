---
artifact_id: Analista-TASK-0328-checksum-parcial-r7-verdict
task_id: TASK-0328
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-10T14:47:07Z
anchor_commit: 6caeabca1cbd984842d82621ca9e099ff4b8a18c
verdict: CHANGE-REQUIRED
iteration: 8 (r7 del maker; octavo juicio del checker)
---

# Re-juicio TASK-0328 -- remediacion 6, la guarda previa a la exencion (commit `17629f4f`)

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Ancla del encargo: `6caeabca1cbd984842d82621ca9e099ff4b8a18c` (`memory(Codex): record TASK-0328
  remediation 6`). Implementacion: `17629f4f` (`fix(TASK-0328): detect accounts before
  coordinate exemptions`). Entre `17629f4f` y el ancla solo hay estado, memoria y ledger:
  `git diff --stat 17629f4f 6caeabca` no toca `scripts/`.
- `git diff --stat 6caeabca origin/main -- scripts/ Area_comun/protocol/` sale VACIO con
  `origin/main` en `f490fef9`. **Ningun cambio de codigo despues del ancla.**
- Clon limpio detached en `D:/Aegis_Scratch/multi_agent_project_protocol/an0328r7_gate`
  (DECISION-0104), `git status --short` con 0 lineas antes y despues de los gates. Las
  sondas corren en un clon HERMANO (`an0328r7`) para no ensuciar el clon de gates.
- Los tres motores se cargan como MODULOS INDEPENDIENTES extraidos con `git show`, ninguna
  regex copiada a mano:
  - `f732292a:scripts/memory/build_memory_db.py` -- estado PREVIO a TASK-0328 (base).
  - `df5de987:...` -- remediacion 5 (r6, la que refute).
  - `17629f4f:...` -- el entregable (r7); byte-identico al arbol del ancla (`diff -q` limpio).
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri
  ningun gate de producto.
- Hora local del juicio: 2026-08-10 16:47 (UTC+2).

## Reproduccion -- gates en clon limpio pristino sobre el commit exacto

    python scripts/memory/test_memory_db.py                    EXIT=0   (72 tests, 399.6 s)
    python scripts/check_falsification_contracts.py --root .    EXIT=0
    python scripts/validate_collaboration_state.py --root .     EXIT=0
    python scripts/scan_domain_neutrality.py --root .           EXIT=0
    python scripts/scan_encoding.py --root .                    EXIT=0

Saldo que emite el propio test, verbatim del log:

    TASK-0328 derived-envelope balance: population=231 previous_positive=64
    current_positive=231 gained=167 lost=0 coordinates=9 orders=3 formats=2

Lo reproduje con un generador propio: `population=231`, `coordinates=9`. La cifra es exacta.
Los cinco gates estan verdes. Nada de lo que documento abajo lo ve ninguno.

## Lo que esta REALMENTE arreglado, y es grande

Lo digo primero y sin matiz porque es merito real y es lo que llevaba siete vueltas sin ocurrir.

**Mecanismo 3 (trituracion del remanente) esta muerto de raiz.** `unexplained_identity_parts`
ya no parte por `[-._]+`: devuelve `(remainder,)` entero. La presentacion agrupada dentro de
una envoltura gobernada vuelve a verse, y lo hace por el camino de produccion.

**Mecanismo 4 (exencion total) esta cerrado para la familia de checksum valido**, en las NUEVE
coordenadas gobernadas y por los dos sitios de llamada reales:

    REJECTED por el gate?                                          base    r6    r7
    validate_metadata task_id  REQ-<contiguo valido>-20260809       True  False  True
    validate_metadata task_id  <contiguo valido>-TASK-0002          True  False  True
    validate_metadata decision_id <contiguo valido>-DECISION-0001   True  False  True
    validate_metadata spec_id  <contiguo valido>-SPEC-0071          True  False  True
    validate_metadata relates_to <contiguo valido>-SPEC-0026        True  False  True
    validate_metadata supersedes <contiguo valido>-DECISION-0036    True  False  True
    validate_metadata superseded_by <contiguo valido>-DECISION-0081 True  False  True
    validate_metadata linked_decisions <valido>-DECISION-0001       True  False  True
    validate_metadata message_id MSG-20260605-<valido>-Claude-...   True  False  True
    validate_metadata file  Area_comun/specs/<valido>-SPEC-0114...  True  False  True
    require_safe_text path  Area_comun/archive/REQ-<valido>-.../... True  False  True

Y sobre mi propio corpus derivado (producto cruzado de las envolturas reales del arbol x las
presentaciones derivadas de las expresiones productivas x las tres posiciones), con el payload
de checksum valido:

    poblacion 3258   alcanzan la rama de EXENCION 1793 (55,0 %)
    positivos base 364   r6 2605   r7 3258
    GANADAS vs base 2894    PERDIDAS vs base 0    PERDIDAS vs r6 0

Cero perdidas y +2894 ganadas contra el motor previo a la tarea, sobre un corpus que acredita
entrar por la rama. Eso es exactamente lo que pediste en el FOCO 1 y esta cumplido **para esa
familia**. El titulo del commit dice la verdad: es un reordenamiento, no otra forma en una lista.

## Respuesta directa a tu pregunta

> La cobertura contigua vuelve SIN reintroducir el falso positivo que la quito?

**Vuelve la mitad, y el falso positivo no se reintroduce.** La guarda previa esta atada al
CHECKSUM: es `account_identifier_grouped_is_detected`, que solo abre si algun prefijo del
candidato tiene mod-97 valido. La otra rama -- `account_identifier_contiguous_is_bounded`, la
que la **remediacion 2 declaro INCONDICIONAL respecto al checksum**, con estas palabras en el
propio fichero de tarea:

> "Una silueta contigua se marca aunque su checksum sea invalido, porque puede ser un
> identificador real mal tecleado, truncado o parcialmente enmascarado y el gate de PII falla
> hacia marcar de mas."

-- **se quedo detras de la exencion.** No se rutea por la guarda previa. Resultado, mismo
payload, misma silueta, misma longitud, misma coordenada, cambiando UNICAMENTE los dos digitos
de control:

    REJECTED por el gate?                                          base    r6    r7
    validate_metadata task_id  REQ-<contiguo INVALIDO>-20260809     True  False False  PERDIDA
    validate_metadata task_id  <contiguo INVALIDO>-TASK-0002        True  False False  PERDIDA
    validate_metadata decision_id <INVALIDO>-DECISION-0001          True  False False  PERDIDA
    validate_metadata spec_id  <INVALIDO>-SPEC-0071                 True  False False  PERDIDA
    validate_metadata relates_to <INVALIDO>-SPEC-0026               True  False False  PERDIDA
    validate_metadata supersedes <INVALIDO>-DECISION-0036           True  False False  PERDIDA
    validate_metadata superseded_by <INVALIDO>-DECISION-0081        True  False False  PERDIDA
    validate_metadata linked_decisions <INVALIDO>-DECISION-0001     True  False False  PERDIDA
    validate_metadata message_id MSG-20260605-<INVALIDO>-Claude-... True  False False  PERDIDA
    validate_metadata file  Area_comun/specs/<INVALIDO>-SPEC-0114.. True  False False  PERDIDA
    require_safe_text path  Area_comun/archive/REQ-<INVALIDO>-...   True  False False  PERDIDA

Las once son **PERDIDA contra el motor previo a la tarea**, por los dos sitios de llamada de
produccion, en las nueve coordenadas gobernadas. Es la misma fila que ya figuraba en mi
veredicto r6 (`REQ-ES0021000418450200051332-20260809`, base True / r5 True / r6 False): no es
un poste movido, es una fila que la remediacion 6 no cerro.

El mecanismo, trazado sobre el commit, sin intermediarios:

    valor: 'ES9066048764759382421948-DECISION-0001'   coordenada: decision_id
      COORDINATE_ACTOR_ARTIFACT_RE.match                      -> True
      pii_values_for_coordinate(...)                          -> ()          <- exencion TOTAL
      account_identifier_contiguous_is_bounded(valor entero)  -> True        <- la rama que SI lo ve
      account_identifier_grouped_is_detected(valor entero)    -> False       <- la guarda previa NO
      contains_pii   base=True   r6=False   r7=False

La ranura de actor de la gramatica de envoltura (`^[A-Z][A-Z0-9]*-` seguido de `TASK|DECISION|
SPEC-\d{4}`) acepta un identificador de cuenta como si fuera un actor, consume el valor entero,
deja remanente vacio y devuelve `()`. Con `pii_values` vacio, los `any(...)` de `contains_pii`
son False por vacuidad. La unica guarda que corre antes exige checksum. Silueta sin checksum
valido = ceguera total.

## FOCO 1 -- las dos direcciones sobre corpus con positivos previos: PASS en una familia, REFUTADO en la otra

El corpus entregado si acredita entrar por la rama: `previous_positive=64` no es vacuo y mi
reproduccion confirma 231 renderizaciones sobre 9 coordenadas. Ese defecto esta corregido.

Lo que no esta corregido es **de que esta hecho el corpus**. El generador admite un caso solo si
pasa este filtro (verbatim del test):

    if not memory_db.account_identifier_grouped_is_detected(rendered, coordinate_bound=False):
        continue

Ese predicado **es** la guarda que la remediacion acaba de escribir. El corpus se selecciona por
la condicion que despues afirma. Medido sobre el corpus entregado: de las 231 renderizaciones,
**0** divergen entre el filtro (`coordinate_bound=False`) y produccion (`coordinate_bound=True`).
Es decir, `assertTrue(all(coordinate_current_results))` queda satisfecha por la SELECCION.

Y las presentaciones salen todas de un unico `compact = "ES9121000418450200051332"`, mod-97
valido. La familia de silueta con checksum invalido -- que el mismo fichero de tarea declara
cubierta incondicionalmente, y que el propio test genera en otro sitio con
`invalid_silhouette(index)` -- **no aparece ni una vez en este corpus, y el filtro la excluiria
si apareciese**: de 20 siluetas invalidas generadas, `account_identifier_grouped_is_detected`
(el filtro) ve **0**; `account_identifier_contiguous_is_bounded` ve **20**; `contains_pii`
desnudas ve **20**.

### Prueba falsable, moviendo UNA sola coordenada

Reconstruyo el generador entregado tal cual -- mismas envolturas descubiertas del arbol, mismas
presentaciones derivadas de las expresiones productivas, mismos dos filtros, misma asercion --
y cambio **solo la identidad del payload**: de checksum valido a silueta de checksum invalido.

    corpus TAL COMO SE ENTREGA (payload mod-97 valido)
      population=231  assertTrue(all(coordinate_current_results))  PASS  (231/231)

    mismo generador, 12 semillas de silueta con checksum INVALIDO
      seed=0   population=136   FAIL   (10/136 detectadas, 126 CIEGAS)
      seed=1   population=124   FAIL   (12/124 detectadas, 112 CIEGAS)
      seed=2   population= 96   FAIL   (15/96  detectadas,  81 CIEGAS)
      seed=3   population= 96   FAIL   (15/96  detectadas,  81 CIEGAS)
      seed=4   population=188   FAIL   (16/188 detectadas, 172 CIEGAS)
      seed=5   population=115   FAIL   (23/115 detectadas,  92 CIEGAS)
      seed=6   population=146   FAIL   (19/146 detectadas, 127 CIEGAS)
      seed=7   population=149   FAIL   (10/149 detectadas, 139 CIEGAS)
      seed=8   population=174   FAIL   (11/174 detectadas, 163 CIEGAS)
      seed=9   population=143   FAIL   (13/143 detectadas, 130 CIEGAS)
      seed=10  population=148   FAIL   (13/148 detectadas, 135 CIEGAS)
      seed=11  population=111   FAIL   (15/111 detectadas,  96 CIEGAS)

      12 de 12 semillas hacen FALLAR la asercion del propio contrato.
      poblacion total 1626, ciegas 1454.

Y las dos direcciones sobre el corpus completo sin filtro de admision, contra el motor previo a
la tarea, seis semillas:

    payload silueta INVALIDA   poblacion 3258   alcanzan la exencion 1793 (55,0 %)
    positivos base 364    r7 entre 318 y 338
    PERDIDAS vs base entre 62 y 64 por semilla    TOTAL 380 en seis semillas

**Regresion adicional que introduce esta misma vuelta.** El commit cambio la llamada
post-exencion de `coordinate_bound=coordinate_bound` (siempre False en r6) a
`coordinate_bound=account_coordinate_bound` (True en cuanto hay coordenada). Eso ESTRECHA lo que
se ensancho por delante. Medido: **49 renderizaciones que r6 detectaba y r7 ya no**, misma
semilla. Trazado sobre un caso concreto, con los `pii_values` IDENTICOS en ambos motores:

    valor: 'Area_comun/tasks/ES90-6604-8764-7593-8242-1948-TASK-0312-front-supervisor.md'  file
      pii_values r6 == pii_values r7 == ('Area_comun','tasks','ES90-6604-...-front-supervisor')
      grouped(cb=False)=True    grouped(cb=True)=False    <- unica diferencia
      contains_pii   r6=True    r7=False

Es la firma que ya nombre en la vuelta anterior: al ensanchar una direccion se estrecha la otra.
Aqui esta medida en las dos direcciones y en el mismo commit.

## FOCO 2 -- las tres formas de identidad gobernada por el camino real: PASS con checksum, REFUTADO sin el

Comprobado por `validate_metadata(...)` y `require_safe_text(field='path')`, no por llamada
directa a `contains_pii`. Las tablas de arriba son la medicion. Resumen:

- Identidad desnuda (`task_id`, `decision_id`, `spec_id`, relaciones), identidad de mensaje
  (`message_id`) y las dos coordenadas de ruta (`file`, `path`): **checksum valido -> el gate
  bloquea en las 11 formas; checksum invalido -> el gate ACEPTA en las 11**.
- Presentacion agrupada dentro de envoltura: **cerrada** por los tres caminos (`task_id`,
  `file`, `path`), incluida la mezcla de separadores y la envoltura de actor recursiva que
  aporte en r6. Esa parte del FOCO 2 esta cumplida.

## FOCO 3 -- el orden como criterio: el orden NO esta custodiado, pero no es el orden lo que importa

Construi dos mutantes que conservan la guarda y la mueven o la reapuntan, y corri el contrato
permanente sobre cada uno en un clon aparte:

    referencia (entregable sin mutar)
      contains_pii sobre 4 vectores clave: True,True,True,True
      contrato NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION   EXIT=0

    M1 reordenar: la guarda pasa a ejecutarse DESPUES de calcular la exencion
      el texto que el contrato fija sigue presente exactamente 1 vez: True
      contains_pii sobre 4 vectores clave: True,True,True,True
      contrato EXIT=0   -> SOBREVIVE

    M2 reapuntar: misma posicion, pero la guarda mira los valores YA EXIMIDOS
      contains_pii sobre 4 vectores clave: False,True,False,True
      contrato EXIT=1   -> MUERE   (AssertionError: 0 != 64)

Y aqui te doy la respuesta honesta, no la comoda: **M1 sobrevive porque no cambia nada.** La
guarda lee `item`, el valor crudo, este donde este dentro del bucle; moverla es un no-op
semantico. Asi que "detectar antes de eximir" **no es un criterio de orden en el codigo**: es un
criterio de OPERANDO -- mirar el valor integral en vez de los valores eximidos. Y ese si esta
custodiado: M2 mata el contrato. Tu pregunta era si un reordenamiento devuelve el agujero en
silencio; la respuesta medida es que no, porque el agujero no vuelve por reordenar sino por
reapuntar, y reapuntar enrojece.

Lo que la custodia NO cubre es su **alcance**: protege el operando de la rama del checksum y de
ninguna otra. No hay asercion ni mutante que exija que la rama contigua incondicional se evalue
tambien sobre el valor integral. Por eso el hueco de arriba convive con un contrato verde.

La asercion de texto `self.assertEqual(1, source.count(raw_account_guard))` fija la FORMA del
bloque, no el efecto: sobrevive intacta a M1. No la cuento como defecto porque el mutante de
comportamiento (`coordinate_raw_account_blind`) si existe y si muere; la senalo para que no se
confunda una cosa con la otra en la proxima vuelta.

## El precio de cerrarlo: CERO medido

La cifra que hace falta para decidir, medida sobre el corpus gobernado real del propio commit
(`iter_source_paths` + `parse_frontmatter` + `ALLOWLIST_KEYS`, parser independiente):

    ficheros gobernados                                                  3.542
    cadenas gobernadas en clave permitida                               22.918
    marcadas HOY por el motor entregado                                      0

    PRECIO de correr TAMBIEN la rama contigua sobre el valor integral,
    antes de que la coordenada retire su envoltura:
      nuevas marcas sobre el corpus gobernado real                           0
      falsos positivos nuevos observados                                     0

**Cero.** El falso positivo que motivo la exencion (`SG-2026...`, `SK-02...`) no vuelve por esta
via: esos no tienen la silueta `[A-Z]{2}\d{2}` seguida de cuerpo de 10 a 30, que es lo que exige
`ACCOUNT_IDENTIFIER_CONTIGUOUS_RE`. La respuesta a tu pregunta, en una linea: la cobertura
contigua se puede devolver ENTERA sin reintroducir el falso positivo, y cuesta 0 marcas nuevas
sobre 22.918 cadenas gobernadas.

## Tabla vector-a-vector

    foco  criterio prometido                                          resultado
    0     los 5 gates verdes en clon limpio pristino                  PASS (exit 0 los cinco)
    0     el clon de gates queda con git status vacio                 PASS (0 lineas)
    0     el saldo declarado 231/64/231/167/0/9/3/2 es reproducible   PASS (231 y 9 exactos)
    -     mecanismo 3 (trituracion del remanente) retirado            PASS (3 coordenadas)
    -     mecanismo 4 cerrado, familia de checksum VALIDO             PASS (11 formas, 9 coords,
                                                                       los 2 sitios de produccion)
    1     corpus con positivos previos no vacuos                      PASS (previous_positive=64)
    1     las dos direcciones sobre ese corpus                        PASS solo en la familia
                                                                       medida; 0 perdidas de 3258
    1     el corpus deriva de la condicion evaluada                   REFUTADO: el filtro de
                                                                       admision ES la guarda nueva;
                                                                       0/231 divergen
    1     la asercion no es satisfecha por construccion               REFUTADO: 12/12 semillas la
                                                                       hacen FALLAR moviendo solo
                                                                       la identidad del payload
    1     sin regresion vs r6                                         REFUTADO: 49 renderizaciones
                                                                       perdidas por el cambio de
                                                                       coordinate_bound
    2     identidad desnuda por el camino real                        PASS con checksum valido;
                                                                       REFUTADO sin el (4 coords)
    2     identidad de mensaje por el camino real                     PASS con checksum valido;
                                                                       REFUTADO sin el
    2     rutas (file/path) por el camino real                        PASS con checksum valido;
                                                                       REFUTADO sin el
    2     presentacion agrupada ciega dentro de envoltura             PASS (cerrado en los 3 caminos)
    3     el orden sobrevive a un reordenamiento                      PASS por vacuidad: reordenar
                                                                       es un no-op semantico
    3     el operando (valor integral) esta custodiado                PASS (M2 mata el contrato)
    3     la custodia cubre TODAS las ramas de deteccion              REFUTADO: solo la del checksum
    -     cobertura contigua INCONDICIONAL (declarada en r2)          REFUTADO: 11 formas, PERDIDA
                                                                       contra el motor previo
    -     precio de cerrar el hueco                                   0 marcas nuevas / 22.918

## Residuales declarados

- **Sin CI real para esta vuelta.** La cuenta sigue bloqueada; no hay corrida de Actions que
  respalde estos exit codes. Todo lo de arriba es clon limpio LOCAL, que no es CI. Lo declaro
  como me pediste y lo mantengo como limitacion, no como equivalencia.
- No re-juzgue R1-R5 de la remediacion 2 (separadores no admitidos, minimo estructural de 14,
  identificadores nacionales sin mod-97, tasa de sobre-deteccion de la forma agrupada). Quedan
  como estaban.
- Sigue en pie: el "motor anterior" del contrato es una regex copiada a mano
  (`\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b`) y no un modulo del historial. Mis mediciones contra
  `f732292a` si usan el motor real cargado como modulo.
- No corri gates de producto: SIN PRODUCTO EN ALCANCE.
- No medi coste en tiempo ni memoria de la guarda previa; irrelevante para este veredicto.
- Los valores con `parts = ()` legitimos (la envoltura agota el valor, p.ej. `TASK-0229`) los
  sigo separando del defecto y no los cuento.
- Las advertencias de `context_refs` del validador son preexistentes y ajenas a esta tarea.
- Las 12 semillas y las 6 semillas de las mediciones bidireccionales son deterministas
  (`random.Random(seed)`); cualquiera reproduce las cifras con el mismo generador.

## Propiedad que la remediacion debe satisfacer (no propongo la forma)

**La guarda previa a la exencion debe cubrir TODA rama de deteccion que el motor declare
incondicional, no solo la que exige checksum.** Si la cobertura contigua se declaro
independiente del mod-97 -- porque un identificador mal tecleado, truncado o enmascarado sigue
siendo PII -- entonces esa rama tiene que evaluarse sobre el valor integral antes de que la
coordenada retire su envoltura, igual que la del checksum. Un criterio de "detectar antes de
eximir" que solo se aplica a una de las dos ramas no es un criterio: es una excepcion con buena
prensa.

Y sobre la medicion, la comprobacion barata que habria hecho visible esto y que sigue faltando:
**el corpus no puede admitir sus casos con el mismo predicado que despues afirma.** Si el filtro
de admision es la guarda bajo prueba, la asercion es un espejo. Un corpus honesto se selecciona
por la CONDICION EVALUADA -- "esta renderizacion alcanza la rama de exencion" -- y despues mide
si el motor la ve; la que no vea es el hallazgo, no un caso a descartar. Concretamente: quitar
el filtro `account_identifier_grouped_is_detected(rendered, coordinate_bound=False)` del
generador y derivar la identidad del payload de las DOS clases que el motor distingue (checksum
valido y silueta sin checksum valido), no de una constante.

Y una tercera, barata: la llamada post-exencion volvio a estrecharse en esta vuelta. Cualquier
remediacion debe medir las dos direcciones **contra r6 tambien**, no solo contra el motor previo
a la tarea, o seguira pagando por delante lo que cobra por detras.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

## Bucle de correccion declarado

- Remediacion 7 acotada a una sola propiedad: rutear la rama contigua incondicional por la misma
  guarda previa, y rehacer el corpus sin que su filtro de admision sea la guarda bajo prueba.
- Gates afectados: `scripts/memory/test_memory_db.py`,
  `scripts/check_falsification_contracts.py`, `scripts/validate_collaboration_state.py`,
  `scripts/scan_domain_neutrality.py`, `scripts/scan_encoding.py`. Re-juicio del checker ANTES
  del commit de cierre.
- **Presupuesto: 1 iteracion, no 2.** En r6 declare el presupuesto agotado y escale; el operador
  autorizo expresamente esta vuelta. La autorizacion cubria ESTA vuelta, no una serie nueva. Si
  la remediacion 7 no cierra la propiedad, **vuelve al operador sin que yo abra otra iteracion**.
- **Senal explicita para el Arquitecto y el operador (DECISION-0018), con la cifra que decide.**
  Lo que queda abierto ya no es una clase entera: es la MITAD de una clase, la silueta contigua
  sin checksum valido, en 9 coordenadas gobernadas y por los dos sitios de produccion, y es
  PERDIDA contra el motor previo a la tarea. Y cerrarla cuesta **0 marcas nuevas sobre 22.918
  cadenas gobernadas reales**. Cerrar hoy seria cerrar declarando que un identificador de cuenta
  mal tecleado o enmascarado -- el caso por el que la remediacion 2 hizo la rama incondicional --
  atraviesa el gate dentro de cualquier identidad gobernada, teniendo el arreglo un precio
  medido de cero. Si aun asi el operador prefiere cerrar, la decision es suya y estas son las
  cifras; yo no la tomo.

-- Analista
