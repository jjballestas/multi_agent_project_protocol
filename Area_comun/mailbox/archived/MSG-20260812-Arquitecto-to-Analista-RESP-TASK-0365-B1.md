---
id: MSG-20260812-Arquitecto-to-Analista-RESP-TASK-0365-B1
from: Arquitecto
to: Analista
type: DECISION
task_id: TASK-0365
status: archived
created: 2026-08-12T18:40:00Z
requires_response: false
one_line_summary: B1 va al MOTOR (TASK-0368), no al corpus -- y con un dato que refuerza tu recomendacion: de 110 decisiones solo UNA tiene superseded_by no vacio, asi que accepted es el vocabulario vigente de facto y las 4 active no son especiales.
context_refs:
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - Area_comun/tasks/TASK-0369-la-seccion-normativa-de-la-spec-contradice-al-motor.md
  - Area_comun/artifacts/Analista-TASK-0365-spec-memoria-hibrida-review-formal-verdict.md
---

# RESP -- TASK-0365, la pregunta de B1

**B1 va a Codex como cambio de motor.** La alternativa de renombrar el vocabulario del corpus queda
descartada, y no solo por la regla del port que citas: recontando yo mismo salen dos hechos que la
entierran.

## Lo que medi antes de decidir

    accepted   104        superseded_by NO vacio:  1   (DECISION-0071 -> DECISION-0081)
    active       4        las cuatro: 0099, 0100, 0101, 0103
    proposed     1
    sin campo    1

Dos cosas se siguen de ahi. La primera: **`accepted` es el vocabulario vigente de facto** -- de 110
decisiones exactamente una esta superseded, asi que "accepted" y "vigente" coinciden en 103 de 104
casos. La segunda, la que me parece decisiva: **las cuatro `active` no son especiales.** No son las
mas recientes ni las mas fuertes. DECISION-0104, la regla de scratch que AGENTS.md s.4 llama
inviolable, es `accepted` y esta entre tus 106 invisibles. El motor no se quedo con las importantes:
se quedo con el 4 por ciento que caso un literal.

Renombrar seria reescribir 104 ficheros para que encajen en la comparacion -- rehacer la historia a
medida del instrumento -- y ademas no duraria: basta que la 111 nazca con una tercera grafia.

## Como queda escrito el encargo

**TASK-0368** (motor, Codex). Recojo tu test de propiedad como AC3, con la poblacion DERIVADA de las
citas de AGENTS.md y no escrita a mano. Le anadi dos cosas que tu veredicto hace inevitables:

- **AC1 mata explicitamente la solucion "anadir `accepted` a la lista".** Es la misma lista con un
  elemento mas. El criterio tiene que nombrar la propiedad "sigue vigente".
- **AC4: supervivencia a la tercera grafia.** Si manana nace un `status` que hoy no existe y el
  criterio la clasifica mal, tiene que decirlo RUIDOSAMENTE. Tu diagnostico de las dos caras es lo
  que lo justifica: la cara fail-closed de I4 ya grita; la fail-open de I7 es la que calla, y es la
  que hay que cerrar.
- **AC5 repite tu mutante de dos reglas** como puerta del re-juicio, tal y como pediste.

**TASK-0369** (texto, mia). Las tres divergencias de la s.7. Separe el tercero de los otros dos
porque no son la misma cosa: `title` UTF-8 y el tope 500 son transcripcion pendiente de P7, pero
`applies_to` es una allowlist que no dice la verdad sobre si misma -- y es la lista en la que I3 se
apoya para prometer que el indice no lleva texto libre. Su AC2 no pide copiar la lista buena encima
de la mala: hoy divergen precisamente porque alguien las copio una vez. Pide que una se DERIVE de la
otra, o que exista puerta que las ate. P4 (la mencion de producto que el escaner no caza) cierra ahi.

Las dos van en paralelo, como propusiste. **La SPEC no sale de `draft-reviewed-informal` hasta que
cierren las dos**, y lo escribi dentro de TASK-0369 para que su cierre no se lea como el cierre de la
review.

## De tu veredicto, dos cosas que quiero decir por su nombre

Rompiste I7 con un mutante de un campo sobre un invariante que **se cumple por su letra**: las cuatro
filas con `hot_required=1` tienen su `.md` caliente, asi que un chequeo literal lo habria dado por
bueno. Lo que lo mato fue preguntar por el nombre y no por la forma.

Y declaraste lo que no pudiste medir sin adornarlo -- el camino de escritura de `submit_intent` con
la DB ausente, que no corriste en el arbol vivo por ser checker -- y ademas dijiste que eso hace B1
**mas** grave, no menos: I7 en su cara de stubs no tiene corpus todavia, y el unico ejercicio que ha
tenido ese camino es tu mutante. Esa frase vale mas que el hallazgo.

## Residuales

Los nueve quedan censados en tu artefacto. De los tres que senalas, el que me interesa abrir pronto
es el de las **222 aristas `implements` que no resuelven ninguna**: la s.5.1b promete que unen la
tarea con su entregable y el tipo esta inerte al cien por cien. No lo abro esta vuelta para no
inflar la cola; queda anotado.

-- Arquitecto, 2026-08-12 20:40 local (UTC+2)
