# ANALISTA OPS - diseno grafo sobre memoria hibrida - veredicto

Firma: Analista  
Fecha: 2026-07-20  
Veredicto: **CAMBIO-REQUERIDO / NO CERRABLE**

El diseno v0.1 identifica la pregunta correcta, separa uso/construccion/
mantenimiento y reconoce que el grafo es una proyeccion. No esta listo para
ejecucion. El brazo B, el corpus literal, el grading y el umbral economico siguen
abiertos; asi el implementador puede elegir despues de conocer el store que aristas,
pesos, profundidad, K, desempate y horizonte hacen ganar a B. Tambien hay escapes de
PII en propiedades/aristas/indices/artefactos y confusores que invalidarian la
comparacion aunque los numeros parezcan verdes.

## Ancla canonica y alcance

- Instruccion canonica: commit de protocolo
  `704652e96d7a95e01740d1566ca6a165b7706df0`, mensaje
  `MSG-20260720-Arquitecto-to-Analista-REVIEW-diseno-grafo-memoria-hibrida.md`.
- Diseno revisado: blob canonico
  `5b39ca9a3f1b81305b484962072bc148a1c885fd` en ese commit.
- DRAFT-DECISION-0104 revisada: blob canonico
  `65d731b6c8b36c818dd0c79a8036c19f15eeae57`.
- Producto: NOT_RUN. La instruccion declara `SIN PRODUCTO EN ALCANCE`, no cita
  commit de producto y prohibe tocar el clon experimental. `npm test` no aplica.
- Fuente externa: clon limpio de `github.com/DeusData/codebase-memory-mcp`, commit
  `7d6cdb23ef5ca2fd51f5d5b7509b33e112ef15f3` (2026-07-18).

## Cinco puntos de apriete

### 1. Umbrales: SLIPS

No existen aun: la seccion 8 delega al revisor el margen de ranking y el horizonte
economico. `precision@1 B > A` sin magnitud, incertidumbre ni regla para empates deja
ganar a B por una sola consulta. `fidelidad/tokens inyectados` permite mejorar el
cociente reduciendo contexto aunque empeoren tokens totales, respuesta final o
abstencion. Tampoco define denominador para una distractora con cero hechos.

Umbral propuesto, a congelar antes de implementar B:

- dos cohortes positivas independientes, Q1 y Q2, deben cumplir cada una
  `delta precision@1 >= 4/26` (15.38 puntos porcentuales) y mediana de mejora de
  rango >= 2 puestos;
- sobre Q1+Q2, comparacion pareada de wins/losses con test binomial exacto bilateral
  `p <= 0.05`; los empates no son wins;
- Q3 debe conservar abstencion correcta >= 25/26 y no admitir mas falsos positivos
  que A;
- fidelidad no inferior por cohorte, y tokens TOTALES a fidelidad constante no
  peores en mas de 5 por ciento; reportar tambien tokens inyectados por separado;
- todas las guardas pasan. Si una cohorte pasa y otra no, INCONCLUSO. No promediar
  cohortes para rescatar un split.

Esto no favorece a B: exige efecto material replicado fuera de B-bis y controla error
pareado. El umbral economico no debe convertir R5 en veto: reportar break-even bajo
una matriz congelada de 100, 1,000 y 10,000 consultas y 1, 10 y 100 mutaciones; el
Operador decide el horizonte de adopcion.

### 2. Corpus: SLIPS; tamano y seleccion fijados

Tamano exacto: **N=78 consultas, 26 por estrato**, sin usar N=6 reservado.

- Q1: las 26 queries selladas de B-bis, byte-identicas y con el mismo answer key.
- Q2: 26 positivos holdout de 26 entradas no usadas por B/B-bis. Universo elegible:
  entradas atestadas, PII-clean, con al menos dos hechos verificables y autor distinto
  del autor de la query. Ordenar IDs canonicos por
  `SHA256("GRAPH-Q2-v1|" + entry_id)` y tomar los primeros 26 despues de aplicar
  cuotas 13/13 para las dos direcciones cross-agente. Si una cuota no tiene 13,
  CAMBIO-REQUERIDO; no rellenar con Q1. Texto redactado solo desde una necesidad
  neutral, sin copiar key, ID, hash, nombre de fichero ni token unico del target.
- Q3: 26 negativos. Para cada Q2, una query emparejada conserva tema y forma pero
  pide un hecho ausente del store; un segundo checker confirma ausencia mediante
  busqueda exhaustiva exacta y semantica antes de sellar. No se aceptan negativos
  aleatorios faciles.

La regla fija tamano y seleccion, pero v0.1 aun no contiene el manifest literal. Antes
de ejecutar debe existir `queries.jsonl` con 78 IDs, texto, estrato, target o
`NO-DERIVADO`, hechos requeridos y SHA-256 del source snapshot. Su SHA-256 se registra
en el diseno y un checker distinto lo confirma. Ninguna sustitucion posterior.

### 3. Costes R5: SLIPS

Los tres nombres estan, pero la contabilidad es incompleta.

- Uso: medir tokens de tool request/response, contexto inyectado, prompt completo y
  completion; wall-clock p50/p95, CPU, peak RSS y bytes leidos/escritos. Separar cold,
  warm y cache hit. Igual numero maximo de tool calls y mismo K/budget en ambos brazos.
- Construccion: incluir parse/extraccion, generacion o validacion de aristas, retries,
  serializacion, indices, compresion, validacion PII, artefactos temporales y trabajo
  del agente/LLM. Reportar full build e incremental inicial.
- Mantenimiento: medir add/update/delete, invalidacion de aristas, full rebuild,
  deteccion de drift, recovery y coste de servir una proyeccion stale. Congelar
  mutaciones y orden antes de correr.
- Declarar fuera de metrica, sin ocultarlo: desarrollo humano, operacion, review,
  backup y coste de incidente. No diluir overhead fijo.

### 4. Firewall PII: SLIPS

Pre-scan y post-scan del artefacto final no cubren toda la familia. El grafo puede
copiar o derivar contenido prohibido en `nodes.properties`, `edges.properties`, FTS,
logs, dumps, cache, WAL, artefacto comprimido y texto de errores. Tambien puede unir
dos hechos inocuos que juntos reidentifican una persona.

Correccion minima: allowlist de campos indexables; exclusiones por ruta y content
hash; escaneo de todos los campos y superficies persistidas/temporales; borrado
verificado de WAL/temp; prueba canario por cada detector; prueba de inferencia por
join; 0 matches antes y despues; y trazabilidad `graph_element -> source_entry_sha`.
Una arista sin fuente atestada o una propiedad libre pierde la celda. Los 60 IBAN
sinteticos quedan fuera por ruta/hash, no por inferir si son reales.

### 5. Confusores faltantes: SLIPS

- **Brazo B subespecificado/tuning leakage:** tipos de nodo/arista, direccion, pesos,
  profundidad, pruning, K, tie-break y algoritmo de score no estan congelados.
- **Baseline de empate:** A ordena familias con score BM25 identico y tie-break
  alfabetico. Comparar top-1 contra un B con otro tie-break puede medir desempate, no
  valor del grafo. Congelar tie-break comun y reportar expected rank dentro de ties.
- **Information-budget leakage:** B puede usar metadata/aristas que A no recibe.
  Toda informacion fuente debe estar disponible a ambos; solo cambia el ranking.
- **Query/answer leakage:** construir aristas despues de leer queries o keys contamina
  B. Sellar corpus antes y negar acceso del builder al answer key.
- **Orden, cache y staleness:** alternar A/B con seed congelado, medir cold/warm por
  separado y aplicar el mismo snapshot. No correr todos A antes de B.
- **Hub-degree/popularity bias:** nodos de alto grado pueden mejorar queries frecuentes
  y degradar cola larga. Reportar por terciles de grado y no solo agregado.
- **Dependencia de autor/familia:** queries de un mismo molde no son observaciones
  independientes. Cohortes y resultado se reportan por familia y direccion de autor.
- **Grader no ciego:** el grader no conoce brazo ni ranking original.

## Set de verificacion EX-ANTE

Cada item del manifest contiene `query_id`, `stratum`, `query_text`, `source_entry_sha`,
`required_facts[]`, `forbidden_facts[]`, `answer_type`, `normalization_version` y
`negative_reason`. Reglas congeladas:

1. Unicode NFKC, trim, whitespace colapsado y casefold solo para comparacion; conservar
   raw answer. No stemming, sinonimos ni fuzzy matching.
2. Palabras numericas espanolas cero..veinte equivalen a cifras 0..20 solo cuando el
   campo esperado es entero. Fuera de ese rango, forma exacta predeclarada.
3. Decimales: coma y punto equivalen; parse Decimal, no float; tolerancia solo si el
   item la declara, por defecto exacto tras quitar ceros finales. Porcentajes no se
   convierten a fracciones salvo regla del item.
4. Fechas se comparan ISO `YYYY-MM-DD`; timezone debe coincidir cuando sea un hecho.
5. Multi-campo: score atomico por campo; un item pasa solo si todos sus campos
   obligatorios pasan. Campos extra falsos activan `forbidden_facts` y hacen fallar.
6. Q3 acierta solo con abstencion explicita `NO-DERIVADO` y sin afirmar hechos. Silencio,
   respuesta vaga o una conexion plausible no cuenta.
7. Dos graders ciegos evaluan; desacuerdo no se resuelve creando una regla: se aplica
   la regla predeclarada o el item queda INCONCLUSO. Ninguna regla nueva al calificar.

## Fuente externa: que aporta y que se descarta

El commit externo confirma una representacion util: tablas separadas de `nodes` y
`edges`, labels/tipos explicitos, propiedades JSON, direccionalidad y unicidad por
`source,target,type`; el README enumera aristas como `CALLS`, `IMPORTS`, `DEFINES`,
`IMPLEMENTS`, `INHERITS`, `DATA_FLOWS` y relaciones cross-service. Tambien aporta dos
ideas operativas: hashes por fichero para incrementalidad e `index_coverage` separado
del grafo para declarar cobertura incompleta.

No se traslada su ontologia de codigo ni su ranking. Su pipeline principal deriva el
grafo de fuentes re-derivables y no prueba procedencia semantica de decisiones no
re-derivables. `manage_adr` ademas introduce registros persistidos, asi que ni siquiera
todo su contenido debe asumirse re-derivable. Las firmas/checksums de release y la
verificacion del artefacto protegen distribucion/bytes; no demuestran que una respuesta
sea fiel. Los claims de README (incluidos 120x en una seccion y 10x en el resumen de
research) son no verificados y quedan fuera. `LICENSE` en el commit es MIT: ideas son
insumo; si se copia codigo, conservar copyright/licencia y revisar terceros por archivo.

## Matriz adversarial

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Pregunta e hipotesis ranking | PASA | Defecto BM25 previo identificado |
| Umbral material y estadistico | SLIPS | Margen y horizonte siguen delegados |
| Corpus exacto no sobreajustado | SLIPS | No existe manifest literal ni hash |
| Q3 detecta alucinacion | SLIPS | Sin negativos near-miss ni regla de abstencion |
| Tres costes R5 | SLIPS | Omite total tokens, recursos, cache, retries y recovery |
| Firewall PII de toda superficie | SLIPS | Solo precontenido y artefacto final |
| Mismo contenido/information budget | SLIPS | Aristas/metadata y score B no definidos |
| Atestacion/proyeccion | PASA parcial | Regla fuente-gana existe; falta source SHA por elemento |
| External repo como referencia | PASA acotado | Typed edges/schema/coverage utiles; claims descartados |
| Ejecucion retenida hasta 0103 | PASA | Instruccion canonica lo exige |

## Fix-loop esperado

Iteracion 1/2: el Asesor materializa v0.2 con especificacion cerrada del brazo B,
manifest literal N=78 y SHA-256, answer key separado, reglas de grading anteriores,
umbrales anteriores, matriz R5 y firewall ampliado. Gates afectados: coherencia del
diseno, sello/hash del corpus, ausencia de PII en todas las superficies y prueba de
igualdad de snapshots/budgets. Re-juicio Analista obligatorio antes de ejecutar o
cerrar. Si la segunda iteracion conserva un grado de libertad post-resultado o un
escape PII, escalar al Operador.

task_id: OPS-GRAFO-MEMHIB-DISENO
status: CAMBIO-REQUERIDO
executive_summary: El diseno acierta la pregunta pero deja libres brazo B, corpus, grading, costes y firewall; hoy puede ajustarse para fabricar una victoria.
artifacts: Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-diseno-grafo-memoria-hibrida-NOGO.md
gates: diseno 3 PASA/parcial y 6 SLIPS; fuente externa commit 7d6cdb2 revisada; producto/npm NOT_RUN por alcance; protocolo validate/domain/encoding/drift/#4 se detallan tras materializacion
next_recommended: Materializar v0.2 y manifest N=78 sellado, cerrar algoritmo/umbrales/costes/PII y pedir re-juicio Analista (iteracion 1/2).
risks: Tuning leakage, tie-break BM25 injusto, query leakage, PII derivada, cache/staleness y pseudorreplicacion pueden producir falso verde.
