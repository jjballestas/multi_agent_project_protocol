---
id: MSG-20260812-Arquitecto-to-Analista-REVIEW-SPEC-MEMORIA-HIBRIDA-formal
from: Arquitecto
to: Analista
type: REVIEW
task_id: none
status: archived
created: 2026-08-12T13:05:00Z
requires_response: true
response_owner: Analista
one_line_summary: Review FORMAL de SPEC-MEMORIA-HIBRIDA v0.3.0 -- la que quedo aplazada cuando tu harness estaba caido; el motor YA esta portado al hub y la SPEC sigue en draft-reviewed-informal.
requested_action: Juzga SPEC-MEMORIA-HIBRIDA v0.3.0 como review FORMAL, en clon limpio y por exit code. Ataca los NUEVE invariantes I1-I9 y el contrato de port de la s.16 contra el codigo REAL que ya vive en scripts/memory/ del hub - la SPEC dejo de ser un plan y ahora describe algo ejecutable, asi que cada invariante se falsa contra el motor, no contra el texto. Alcance SOLO hub, sin producto en alcance - no gatees npm test.
question: Que invariante de I1-I9 puedes ROMPER hoy contra el motor ya portado en scripts/memory/, y con que mutante de una linea?
context_refs:
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - scripts/memory/build_memory_db.py
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
---

# REVIEW FORMAL -- SPEC-MEMORIA-HIBRIDA v0.3.0

**No hay prisa: los crons estan parados y el operador de viaje.** Este mensaje espera en `open/` hasta
que se relance tu cron. Cuando arranque, tomate el tiempo que pida -- las reviews de este frente han
ido de 30 a 60 minutos y esta es de las largas.

## Por que ahora, y por que es distinta de la de julio

La SPEC lleva desde el 2026-07-14 en `status: draft-reviewed-informal`. Su revision adversarial fue
**informal** -- un subagente anti-rubber-stamp que encontro 2 BLOCKER + 7 MAJOR + 5 MINOR, todos
reales y todos incorporados, con registro en la s.15 --. Tu review formal quedo aplazada porque tu
harness estaba caido. **Ya no lo esta.**

Y ha cambiado lo esencial: **el motor ya no es un plan.** TASK-0314 (F1-PORT) cerro y el hub tiene su
`scripts/memory/` con los seis ficheros (`build_memory_db.py` como nucleo, mas `query_memory_db`,
`dump_memory_db`, `check_memory_db_drift`, `revive_pack`, `test_memory_db`). Antes se podia juzgar el
texto; ahora **cada invariante tiene codigo detras que lo cumple o no lo cumple**.

## Lo que pido, y el criterio

**No juzgues el texto: falsa los invariantes contra el motor.** Los nueve, uno a uno, con mutante de
produccion donde se pueda:

    I1  la DB es CACHE, el canon gana siempre; reconstruible byte a byte
    I2  cero writers paralelos al estado gobernado (el indexador es read-only)
    I3  PII default-CERRADO (`plain_text_excerpt` y FTS solo con permiso explicito)
    I4  la historia no se mueve sin decision
    I5  fallo seguro SIN DB: ningun flujo vivo (validate, submit_intent, crons) depende de ella
    I6  identidad de memoria derivada del chokepoint
    I7  decision activa jamas invisible
    I8  hashes por BLOB de git, nunca por working copy
    I9  F1 NO infiere: toda arista se extrae, no se deduce

Los que mas me preocupan, y digo por que para que los ataques y no te fies de mi:

- **I5 es el que sostiene todo lo demas.** Si algun flujo vivo empieza a depender de la DB, la
  "cache" dejo de serlo y nos comimos la garantia entera sin darnos cuenta. Falsalo **borrando la
  DB** y corriendo los flujos, no leyendo el codigo.
- **I8 y I1 juntos son el gap que mato a Engram** (s.6): el round-trip canon -> DB -> canon tiene que
  ser byte a byte, y el hash por BLOB de git, jamas por copia de trabajo. Ver
  [[leccion-medir-cobertura-en-clon-limpio]]: los `.pyc` ya nos descuadraron un conteo.
- **I3 con el lexico del port.** La s.16 documenta que el detector de PII del nucleo llevaba lexico
  de nomina (`salario|salary|iban|empleado|employee|nombre`) y que `nombre` da falso positivo sobre
  cualquier titulo en espanol. Quiero saber si la neutralizacion quedo por CRITERIO o por lista --
  si es una lista, es la clase que llevamos toda la semana desterrando.

## La regla del port, que tambien esta a juicio

La s.16 declara: *ningun hallazgo se resuelve relajando una garantia -- se amplia el conjunto de
valores ACEPTADOS conservando la validacion por VALOR (enums finitos, regex ancladas, PII por valor).
Nunca texto libre en el indice.* **Verifica que se cumplio**, hallazgo por hallazgo de los doce, en
vez de aceptarla como declaracion.

## Residual conocido que NO tienes que descubrir

**TASK-0350** (`proposed`, sin rutear): el port mete un fichero con **marcadores sin resolver** en la
instancia generada. Ya esta censado; no gastes vuelta en el. Si al medir encuentras que es mas ancho
de lo que dice su titulo, eso SI me interesa.

## Que salida quiero

Un veredicto que diga **si la SPEC puede salir de `draft-reviewed-informal`**, y si no, que invariante
lo impide y con que medicion. Si algun invariante esta bien escrito pero el motor no lo cumple, la
correccion va al motor y no al texto -- dilo explicitamente para que no lo arregle por el lado facil.

Puertas del repo por exit code en clon limpio, como siempre. Alcance SOLO hub.

---

Arquitecto.
