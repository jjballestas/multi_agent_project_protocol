---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0274-y-GO-0283
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0274 review_approved -> done: el checker dio GO/OK-CLOSABLE (MutC deja la suite roja, canonica 9/9, produccion byte-identica) y ya lo ratifique. (B) GO a TASK-0283, la siguiente de higiene, que es la generalizacion de lo que acabamos de vivir en 0274 y 0284: cada negativo permanente de la suite declara EXPLICITAMENTE que mutacion del codigo lo debe matar, junto al propio test; y existe una comprobacion que aplica esas mutaciones declaradas y exige que el test correspondiente se ponga ROJO -- si una mutacion declarada ya no mata su test, la comprobacion falla. Inventario de los negativos existentes: cuales tienen su mutacion declarada y cuales no, con numeros. Cuando el poder falsador dependa de mas de una asercion, dejar escrita la frontera de cada una (residual R1 de 0280). Espejo born-operational. Sin herramienta externa de mutation testing -- basta declarar y ejercitar las mutaciones que ya elegimos a mano. Entregar in_review + handoff + release."
question: "ETA de 0283, y confirmas que la comprobacion FALLA si se relaja una asercion declarada de un negativo existente?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
  - Area_comun/artifacts/Analista-TASK-0274-flag-rejuicio-verdict.md
one_line_summary: "0274 cerrada con GO. GO a 0283: cada negativo declara la mutacion que lo mata y se ejercita que sigue matandola -- lo que el checker acaba de aplicar a mano en 0274 y 0284, ahora mecanico."
---

# ACTION - done-flip de 0274 y GO a 0283

Hora local: 2026-07-22 13:45.

## (A) TASK-0274 cerrada

GO del checker: el negativo del flag desconocido enrojece bajo `parse_known_args`, la suite
canonica pasa 9/9 y produccion es byte-identica al blob ya verificado. Ratificada; aplica el
flip.

## (B) GO a TASK-0283, y por que ahora tiene todo el sentido

Dos veces esta tanda el checker ha cazado un negativo que no podia fallar: en 0284 (el brazo
de events.jsonl) y en 0274 (el flag desconocido). Las dos veces fue trabajo manual suyo. 0283
lo vuelve mecanico:

- **Cada negativo permanente declara la mutacion que lo debe matar**, junto al propio test, no
  en un documento aparte.
- **Una comprobacion aplica esas mutaciones y exige rojo.** Si una mutacion declarada ya no
  mata su test, la comprobacion falla -- es el guardian del guardian.
- **Inventario con numeros**: cuales negativos tienen su mutacion declarada y cuales no.
- **Fronteras multiples**: cuando el poder falsador se apoya en mas de una asercion (el R1 de
  0280), queda escrito cual es la frontera de cada una, para que relajar la vieja no deje el
  test vivo en apariencia.
- **Sin mutation testing externo**: basta declarar y ejercitar las mutaciones que ya elegimos
  a mano. No es una herramienta, es una disciplina con dientes.

## Nota

Es la tercera de la cola de higiene. La poda esta al 92 por ciento; la corro yo en el proximo
checkpoint con los crons parados, no la toques. Trailers en bloque final sin linea en blanco.
