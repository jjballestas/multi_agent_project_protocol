---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-F-0280R4-02-poder-falsador
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Reparacion acotada de TASK-0280 a UN solo punto: F-0280R4-02. El brazo de events.jsonl del negativo permanente perdio su PODER FALSADOR -- el checker lo midio con control positivo: el test pasa igual con el arreglo y sin el, asi que ya no prueba nada. Restaurar la falsabilidad de ese brazo: con el arreglo revertido el test debe FALLAR, y hay que demostrarlo dejando constancia del control positivo en la propia entrega. NO anadir un guard de torn_tail dentro de 0280 (eso queda cerrado por construccion con la ventana de bytes de TASK-0281, ya entregada). NO reabrir nada mas de 0280. Entregar in_review + handoff + release."
question: "ETA, y confirmas que dejas registrado el control positivo (test rojo con el arreglo revertido) en el handoff?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter4-cierre-verdict.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
one_line_summary: "Un negativo permanente que no puede fallar es peor que no tenerlo: restaurar el poder falsador del brazo de events.jsonl, con control positivo demostrado."
---

# ACTION - restaurar el poder falsador de un negativo permanente

Hora local: 2026-07-21 05:30. Punto unico, pequeno, y mas importante de lo que parece.

## Que pasa

El checker midio el brazo de `events.jsonl` del negativo permanente **con control
positivo**: revirtio el arreglo y el test **siguio pasando**. Es decir, ese brazo ya no
distingue el codigo arreglado del roto. No es un test debil: es un test **muerto que parece
vivo**.

Un negativo permanente que no puede fallar es peor que no tenerlo, porque da confianza sin
sostenerla. Toda la cadena 0272-0281 se apoya en que estos negativos detendrian una
regresion; uno que no puede fallar rompe esa promesa en silencio, que es justo la clase de
fallo contra la que venimos peleando toda la noche.

## Que quiero

Restaurar la falsabilidad de ese brazo y **demostrarla**: con el arreglo revertido el test
tiene que ponerse rojo, y ese control positivo queda escrito en el handoff. No me vale
"pasa"; quiero "pasa, y con el arreglo revertido falla".

Aplicalo como criterio general en lo que escribas a partir de ahora: un negativo nuevo se
entrega con su control positivo, o no esta terminado.

## Que NO quiero

- **Nada de un guard de `torn_tail` dentro de 0280.** Ese camino queda cerrado por
  construccion con la ventana por bytes anadidos que ya entregaste en TASK-0281: una cola
  desgarrada no puede desplazar la ventana hacia atras. Anadir una rama para el caso recien
  encontrado es el patron de enumeracion que nos costo cuatro iteraciones.
- Reabrir cualquier otra cosa de 0280.

## Orden de cierre

0280 se cierra **despues** de que el checker juzgue 0281, apoyandose en esa ventana por
bytes. Tu reparacion de hoy entra en ese mismo cierre.

Trailers en bloque final sin linea en blanco. No redesplegar el harness vivo.
