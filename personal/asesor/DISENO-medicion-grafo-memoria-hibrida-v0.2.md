# DISENO DE MEDICION - grafo sobre la memoria hibrida (v0.2)

> **SUPERSEDE a v0.1** (blob `5b39ca9a3f1b81305b484962072bc148a1c885fd`), que quedo
> CAMBIO-REQUERIDO / NO CERRABLE en el veredicto del Analista del 20-jul
> (`Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-veredicto.md`).
> v0.2 adopta los cinco puntos de apriete y cierra lo que v0.1 dejaba abierto.
> Autor: Asesor. Pendiente de RE-JUICIO del Analista (iteracion 1/2).
> Ejecucion: NO arranca hasta que cierre la tanda DECISION-0103.

## 0. DECLARACION PREVIA (sin cambios respecto de v0.1)

- **DECISION-SUPPORT PRIVADO. NO CITABLE.** No alimenta publicacion ni TFM y no
  restringe el diseno de una eventual Fase B. Firewall anti-HARKing intacto.
- Hipotesis, brazos, corpus, metricas y **umbrales** quedan congelados AQUI, antes de
  ejecutar. Lo que aparezca fuera de lo pre-declarado se reporta como EXPLORATORIO.
- Proposito unico: dar al Operador el dato que condiciona su firma de promocion
  (DRAFT-DECISION-0104, R0: el checklist hace ELEGIBLE, la firma promueve).
- **No se ejecuta durante la ventana de medicion del N=6**, y el corpus no toca las
  unidades reservadas.

## 1. Pregunta e hipotesis (PASA en v0.1, se conserva)

**H-RANK (primaria):** el brazo con grafo mejora la POSICION de la entrada correcta
frente al ranking bm25 actual. Fundamento medido: celda B-bis, *"hit 100 discriminante
FUERTE; ranking bm25 no-informativo"*.

**H-TOK (secundaria):** a fidelidad constante, B necesita inyectar menos tokens.

## 2. Brazos - BRAZO B CONGELADO (corrige confusor "subespecificado / tuning leakage")

Ambos brazos comparten store, contenido, snapshot, K, presupuesto y numero maximo de
tool calls. **Lo unico que cambia es el orden.**

### 2.1 Restriccion de presupuesto de informacion (corrige "information-budget leakage")

**Las aristas se derivan EXCLUSIVAMENTE de informacion que el brazo A ya posee**:
contenido de la entrada, autor, timestamp, y referencias explicitas contenidas en el
propio texto (ids de decision/tarea/mensaje, shas citados). **Prohibido**: anotacion
humana nueva, enriquecimiento por LLM que introduzca hechos, o cualquier campo que A no
reciba. Si B gana por tener MAS informacion, no ha demostrado nada sobre estructura.

### 2.2 Ontologia congelada (propia; NO se traslada la de codigo del repo externo)

Tipos de nodo: `entrada` (unidad atomica atestada del store). Sin sub-tipos: cualquier
sub-tipificacion seria interpretacion y abre la puerta al tuning.

Tipos de arista, direccionales, derivables de referencias explicitas:

| tipo | semantica | derivacion |
|---|---|---|
| `REFERENCIA` | A cita a B | id/sha de B aparece literal en el texto de A |
| `CORRIGE` | A enmienda o rectifica a B | referencia + marcador lexico predeclarado |
| `SUPERSEDE` | A sustituye a B | referencia + marcador lexico predeclarado |
| `MISMO_HILO` | A y B pertenecen al mismo hilo | id de hilo/tarea comun |
| `MISMO_AUTOR` | mismo autor | campo autor |

La lista de marcadores lexicos de `CORRIGE` y `SUPERSEDE` se congela en el manifest y
**no se amplia despues de ver resultados**. Si un marcador falta, se declara como
residual, no se anade.

### 2.3 Parametros congelados

- Profundidad maxima de navegacion: **2 saltos**.
- Pesos: **uniformes (1.0) por tipo de arista.** Pesos ajustables serian el vector
  principal de tuning leakage.
- Pruning: ninguno.
- **K identico en ambos brazos**, fijado en el manifest.
- **Tie-break COMUN a ambos brazos** (corrige "baseline de empate"): `entry_id`
  canonico ascendente. Se reporta ademas el **expected rank dentro de empates**, para
  que no se confunda "desempatar mejor" con "valorar mejor".
- Algoritmo de score de B: bm25 base + bonificacion por conectividad a los top-N de bm25,
  con formula literal en el manifest antes de construir.

### 2.4 Cuarentena del builder (corrige "query/answer leakage")

El corpus se sella ANTES de construir el grafo. El proceso constructor **no accede ni a
las queries ni al answer key** -- cuarentena fisica, no promesa. Mas estricto que lo
exigido por el checker (que solo pedia negar el answer key): la separacion fisica es mas
barata de garantizar que de discutir.

## 3. Corpus - N=78 (adoptado literal del veredicto)

**26 por estrato. Ninguna unidad del N=6 reservado.**

- **Q1**: las 26 queries selladas de B-bis, **byte-identicas** y con el mismo answer key.
- **Q2**: 26 positivos holdout sobre entradas no usadas por B/B-bis. Universo elegible:
  atestadas, PII-clean, con >=2 hechos verificables y autor distinto del autor de la
  query. Orden canonico por `SHA256("GRAPH-Q2-v1|" + entry_id)`, primeros 26 tras aplicar
  cuotas **13/13** para las dos direcciones cross-agente. **Si una cuota no llega a 13 ->
  CAMBIO-REQUERIDO; no se rellena con Q1.** Texto redactado desde una necesidad neutral,
  sin copiar key, id, hash, nombre de fichero ni token unico del target.
- **Q3**: 26 negativos **emparejados** con Q2 (mismo tema y forma, hecho ausente del
  store). Un segundo checker confirma la ausencia por busqueda exhaustiva exacta y
  semantica antes de sellar. **No se aceptan negativos aleatorios faciles.**

### 3.1 Manifest literal (bloqueante)

Antes de ejecutar debe existir `queries.jsonl` con los 78 items, cada uno con:
`query_id`, `stratum`, `query_text`, `source_entry_sha`, `required_facts[]`,
`forbidden_facts[]`, `answer_type`, `normalization_version`, `negative_reason`.

Su **SHA-256 se registra en este diseno** y un checker distinto lo confirma. **Ninguna
sustitucion posterior.**

## 4. Umbrales CONGELADOS (adoptados del veredicto, sin ablandar)

- Dos cohortes positivas independientes, **Q1 y Q2, cada una** debe cumplir
  `delta precision@1 >= 4/26` (15.38 pp) **y** mediana de mejora de rango **>= 2 puestos**.
- Sobre Q1+Q2: comparacion **pareada** wins/losses, **test binomial exacto bilateral
  `p <= 0.05`**. Los empates **no** son wins.
- **Q3**: abstencion correcta **>= 25/26** y no mas falsos positivos que A.
- Fidelidad **no inferior por cohorte**; tokens **TOTALES** a fidelidad constante no
  peores en mas de **5 %**. Se reportan ademas tokens inyectados por separado.
- Todas las guardas de la seccion 6 pasan.
- **Si una cohorte pasa y otra no -> INCONCLUSO. No se promedian cohortes para rescatar
  un split.** (Precedente vinculante: A-bis.)

**R5 no es veto.** El resultado economico se reporta como **break-even** sobre matriz
congelada de **100 / 1.000 / 10.000 consultas** y **1 / 10 / 100 mutaciones**. El
horizonte de adopcion lo decide el Operador, no el diseno.

## 5. Los tres costes de R5 (contabilidad completa)

- **USO**: tokens de tool request/response, contexto inyectado, prompt completo y
  completion; wall-clock p50/p95, CPU, peak RSS, bytes leidos/escritos. **Separar cold /
  warm / cache hit.** Mismo maximo de tool calls y mismo K/budget en ambos brazos.
- **CONSTRUCCION**: parse/extraccion, generacion y validacion de aristas, retries,
  serializacion, indices, compresion, validacion PII, artefactos temporales y trabajo del
  agente/LLM. Reportar **full build** e **incremental inicial**.
- **MANTENIMIENTO**: add/update/delete, invalidacion de aristas, full rebuild, deteccion
  de drift, recovery, y **coste de servir una proyeccion stale**. Mutaciones y su orden se
  congelan antes de correr.
- **Declarado FUERA de metrica, sin ocultarlo**: desarrollo humano, operacion, review,
  backup, coste de incidente. **El overhead fijo no se diluye** (precedente A-bis: se
  reporto aparte, no promediado).

## 6. Firewall de PII (ampliado a toda la familia de superficies)

v0.1 cubria contenido; faltaban las superficies derivadas. Correccion minima adoptada:

- **Allowlist de campos indexables** (lo no listado no se indexa).
- **Exclusiones por ruta y content hash** -- los 60 IBAN sinteticos del clon quedan fuera
  **por ruta/hash, NO por inferir si son reales**. La regla no es "no indexes PII real":
  es "no indexes PII".
- **Escaneo de TODAS las superficies persistidas y temporales**: `nodes.properties`,
  `edges.properties`, FTS, logs, dumps, cache, **WAL**, artefacto comprimido y texto de
  errores.
- **Borrado verificado** de WAL y temporales.
- **Prueba canario por cada detector** (si un detector no dispara sobre su canario, el
  detector esta roto y la celda no corre).
- **Prueba de inferencia por join**: dos hechos inocuos que juntos reidentifican.
- **Trazabilidad `graph_element -> source_entry_sha`** obligatoria. **Una arista sin
  fuente atestada, o una propiedad de texto libre, pierde la celda.**

Esto ademas convierte en verificable la regla de proyeccion: sin sha de origen por
elemento, "si grafo y entrada discrepan gana la entrada" es una intencion, no una
garantia (hallazgo del checker).

## 7. Guardas que NO pueden empeorar

- Atestacion intacta: sha, procedencia, drift 0, round-trip.
- 0 matches de PII antes y despues (seccion 6).
- El grafo es **proyeccion**, nunca fuente de verdad: si discrepa con la entrada, gana la
  entrada -- y ahora es comprobable por `source_entry_sha`.

## 8. Confusores controlados (los ocho del veredicto)

| confusor | control |
|---|---|
| B subespecificado / tuning leakage | seccion 2.2-2.3, todo congelado antes de construir |
| Baseline de empate | tie-break comun + expected rank dentro de empates (2.3) |
| Information-budget leakage | 2.1: aristas solo desde informacion que A ya tiene |
| Query/answer leakage | 2.4: corpus sellado antes, builder en cuarentena |
| Orden, cache y staleness | alternancia A/B con seed congelado, cold/warm separados, mismo snapshot. **No se corre todo A y luego todo B** |
| Hub-degree / popularity bias | resultados por **terciles de grado**, no solo agregado |
| Dependencia de autor/familia | cohortes y resultado por familia y direccion de autor |
| Grader no ciego | **dos graders ciegos** a brazo y a ranking original |

Del probe anterior, se conserva: contaminacion por volcado de cold-start del harness
(mordio dos veces), brazos homogeneos verificados antes de cada tanda, cuarentena fisica
de lo prohibido.

## 9. Grading - reglas congeladas (adoptadas del veredicto)

1. Unicode NFKC, trim, whitespace colapsado, casefold **solo para comparacion**;
   conservar raw answer. Sin stemming, sinonimos ni fuzzy.
2. Palabras numericas cero..veinte equivalen a 0..20 **solo** si el campo esperado es
   entero. Fuera de rango, forma exacta predeclarada.
3. Decimales: coma y punto equivalen; parse `Decimal`, no float; tolerancia solo si el
   item la declara (por defecto exacto tras quitar ceros finales). Porcentajes no se
   convierten a fracciones salvo regla del item.
4. Fechas en ISO `YYYY-MM-DD`; timezone debe coincidir cuando sea un hecho.
5. Multi-campo: score atomico por campo; el item pasa solo si todos los obligatorios
   pasan. Campos extra falsos activan `forbidden_facts` y hacen fallar.
6. **Q3 acierta SOLO con abstencion explicita `NO-DERIVADO`** y sin afirmar hechos.
   Silencio, vaguedad o "conexion plausible" **no cuentan**.
7. Dos graders ciegos. **El desacuerdo no se resuelve creando una regla**: se aplica la
   predeclarada o el item queda INCONCLUSO. **Ninguna regla nueva al calificar.**

## 10. Fuente externa - que se toma y que se descarta

Commit revisado por el checker: `7d6cdb23ef5ca2fd51f5d5b7509b33e112ef15f3` (2026-07-18).

**Se toma** (representacion, no ontologia): tablas separadas `nodes` / `edges`, labels y
tipos explicitos, propiedades JSON, direccionalidad, unicidad por `(source, target, type)`.
Mas dos ideas operativas: **hashes por elemento para incrementalidad** y **cobertura del
indice declarada por separado** (poder decir "esto no esta indexado" en vez de fingir
completitud).

**Se descarta**: su ontologia de codigo (nuestro dominio son decisiones, no llamadas), su
ranking, y sus claims de README (120x / 10x) por no verificados. Su pipeline deriva el
grafo de fuentes **re-derivables** y no prueba procedencia semantica de contenido no
re-derivable, que es justo nuestro caso. Sus firmas de release protegen bytes de
distribucion, **no fidelidad de respuestas**.

**Licencia MIT**: las ideas son insumo libre; si se copiara codigo, conservar
copyright/licencia y revisar terceros por archivo.

## 11. Entorno y gobernanza (sin cambios)

- Clon: `D:/Aegis_Scratch/Nova-Payroll/memhib-graph-probe` (DECISION-0098).
- Sin `protocol-secrets`: no hay ceremonia de firmas, y no hace falta -- lo que da validez
  aqui es la medicion, no las firmas.
- El TRABAJO se gobierna en el clon; las DECISIONES y reportes al Operador van por el
  mailbox del HUB citando el sha del clon.

## 12. Lo que este diseno NO cubre (declarado)

- No mide el cruce decision<->codigo. Es producto, se demuestra con un caso, va despues.
- No evalua adoptar `codebase-memory-mcp` como herramienta para los agentes.

## 13. Bloqueantes antes de ejecutar (checklist)

1. `queries.jsonl` con los 78 items y su SHA-256 registrado aqui.
2. Confirmacion del manifest por un checker distinto.
3. Formula literal del score de B y marcadores lexicos congelados en el manifest.
4. Cierre de la tanda DECISION-0103.

-- Asesor, 20-jul-2026. v0.2, pendiente de re-juicio (iteracion 1/2).
