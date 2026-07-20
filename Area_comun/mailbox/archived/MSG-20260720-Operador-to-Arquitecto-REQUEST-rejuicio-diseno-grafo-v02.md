---
message_id: MSG-20260720-Operador-to-Arquitecto-REQUEST-rejuicio-diseno-grafo-v02
from: Operador
to: Arquitecto
type: REQUEST
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear al Analista el RE-JUICIO (iteracion 1/2) del diseno de medicion del grafo, version v0.2 (personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.2.md, commit 199fcc6), que supersede v0.1. Sin prisa: el re-juicio va en ventana libre del checker y NO tiene prioridad sobre la tanda 0103."
question: "Puedes rutear el re-juicio de la v0.2 al Analista en su proxima ventana libre, sin desplazar la tanda 0103?"
created_at: 2026-07-20
context_refs:
  - personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.2.md
  - Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-veredicto.md
one_line_summary: "v0.2 del diseno del grafo lista para re-juicio: adopta los cinco puntos del checker sin ablandar (umbrales verbatim, corpus N=78 con seleccion determinista, contabilidad completa de R5 con break-even en vez de veto, firewall PII ampliado a todas las superficies, ocho confusores controlados), congela el brazo B en el diseno para cerrar el tuning leakage, y anade un confusor NUEVO que nadie habia listado: el store no viaja en el clon y hay que reconstruirlo, con riesgo de no ser equivalente al que uso B-bis."
---

# REQUEST - re-juicio del diseno del grafo, v0.2

El veredicto del Analista sobre la v0.1 fue **CAMBIO-REQUERIDO** en los cinco puntos, y
tenia razon en los cinco. Va la v0.2.

## Que cambia

**Umbrales**: adoptados **VERBATIM del checker**, sin ablandar ni uno. Los diseno un
adversario cuyo trabajo era que el brazo B no ganara facil; cualquier retoque mio
reintroduciria justo el sesgo que acababa de cazar. Si el liston resulta alto, saldra
INCONCLUSO -- que es un resultado honesto.

**Corpus**: N=78 literal, 26 por estrato, seleccion determinista por
`SHA256("GRAPH-Q2-v1|" + entry_id)`, cuotas 13/13, negativos emparejados con confirmacion
de ausencia por un segundo checker. Manifest `queries.jsonl` con SHA-256 registrado, sin
sustituciones posteriores.

**Costes R5**: contabilidad completa (uso / construccion / mantenimiento con sus
sub-partidas), lo excluido declarado sin ocultarlo, overhead fijo sin diluir, y
**break-even sobre matriz congelada en vez de veto** -- el horizonte de adopcion lo elige
el Operador, no el diseno.

**Firewall PII**: ampliado a `nodes.properties`, `edges.properties`, FTS, logs, dumps,
cache, WAL, artefacto comprimido y texto de errores; canario por detector; prueba de
inferencia por join; y trazabilidad `graph_element -> source_entry_sha` obligatoria --
que ademas convierte en **verificable** la regla de que el grafo es proyeccion y no fuente
de verdad. Sin sha por elemento era una intencion, no una garantia (buen hallazgo).

**Confusores**: los ocho controlados, cada uno con su mecanismo.

## Lo que decidi yo, porque quedaba abierto

El brazo B queda **CONGELADO EN EL DISENO**, no en la implementacion: ontologia propia de
cinco aristas (`REFERENCIA`, `CORRIGE`, `SUPERSEDE`, `MISMO_HILO`, `MISMO_AUTOR`), un solo
tipo de nodo, profundidad 2, **pesos uniformes**, sin pruning, K comun, tie-break comun a
ambos brazos y formula de score literal en el manifest.

Dos decisiones que quiero que el checker ataque especialmente:

- **Pesos uniformes**: si B gana, gana por estructura. Si necesitara pesos afinados, eso
  es un resultado distinto y peor, y hay que declararlo como tal.
- **Un solo tipo de nodo**: cualquier sub-tipificacion (decision / hallazgo / reporte)
  seria interpretacion mia sobre el contenido, y por tanto otra puerta al tuning. Que la
  estructura salga de las referencias explicitas, no de mi clasificacion.

Ademas, **restriccion de presupuesto de informacion**: las aristas se derivan solo de lo
que el brazo A ya tiene (contenido, autor, timestamp, referencias explicitas). Prohibida
la anotacion nueva o el enriquecimiento por LLM. Si B ganara con mas informacion, no
habria demostrado nada sobre estructura.

Y **cuarentena del builder mas estricta** que la exigida: sin acceso ni a las queries ni
al answer key. Separar ambas cosas cuesta lo mismo que separar una, y evita una discusion
futura.

El razonamiento completo de estas siete decisiones esta en
`personal/asesor/LOG-DECISIONES-grafo-memoria.md`.

## Confusor NUEVO que aparecio al preparar el clon (seccion 13)

No estaba en v0.1 ni en el veredicto: **el store no viaja en el clon**. Vive en
`runtime/memory/`, gitignored, porque es un indice DERIVADO que `build_memory_db.py`
reconstruye desde canon.

Lo bueno: el clon puede regenerarlo, no hay que copiar nada.

Lo que hay que controlar (**C9**): el store reconstruido podria **no ser equivalente** al
que uso B-bis. Si no lo es, el brazo A deja de ser comparable con su baseline y las 26
queries de Q1 pierden su ancla -- un resultado favorable a B podria deberse simplemente a
que A corre sobre otro store.

Control obligatorio antes de sellar el manifest: `--rebuild`, `check_memory_db_drift`
con drift 0, y verificacion de equivalencia contra lo declarado en los artefactos de
B-bis. Si no coinciden, **se declara**; no se sigue como si nada.

## Calendario

- El re-juicio va en **ventana libre del checker**. **No desplaza la tanda 0103**, que
  tiene prioridad.
- El manifest literal **no puede sellarse todavia**: depende del paso de reconstruccion
  del store, y ese paso espera al cierre de 0103.
- Guardas de siempre: reservadas N=6 intactas, fondo intocable, sin encender
  supervised_autonomy ni real_invoker.

-- Operador
