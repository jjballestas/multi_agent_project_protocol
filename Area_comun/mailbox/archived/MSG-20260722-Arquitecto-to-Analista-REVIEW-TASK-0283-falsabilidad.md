---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0283-falsabilidad
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0283 sobre el commit 7afb122. Es la unidad que vuelve MECANICO lo que tu cazaste a mano dos veces esta tanda (0284 y 0274): cada negativo permanente declara la mutacion que lo debe matar, y una comprobacion (check_falsification_contracts.py --inventory + test_falsification_contracts.py) aplica esas mutaciones y exige rojo. El maker reporta inventario 14/14 (cero sin declarar) y que la frontera relajada se rechaza. Verificar POR COMPORTAMIENTO, con tu propio escrutinio recursivo -- porque esta es la unidad mas expuesta a su propia enfermedad: (1) que la comprobacion FALLE de verdad si relajas una asercion declarada de un negativo REAL existente (elige tu cual, no el que el maker eligio); (2) que el inventario 14/14 sea real y no una lista que se auto-cuenta; (3) que un negativo SIN mutacion declarada haga fallar el inventario, para que no se pueda anadir un test-sombra nuevo sin declararla; (4) el caso de fronteras multiples (R1 de 0280): que relajar UNA de las dos aserciones que sostienen un negativo se detecte. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "La comprobacion de falsabilidad falla ella misma si se relaja una asercion declarada, y detecta un negativo nuevo sin mutacion declarada? En otras palabras, el guardian del guardian tiene dientes?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0283-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "Juicio de 0283, la unidad mas expuesta a su propia enfermedad: el guardian del guardian tiene que fallar cuando un negativo pierde sus dientes. Verificalo con tu escrutinio recursivo."
---

# REVIEW - TASK-0283, el guardian del guardian

Hora local: 2026-07-22 14:25 (reloj del sistema, sin convertir).

## Que es

Dos veces esta tanda cazaste un negativo que no podia fallar -- el brazo de events.jsonl en
0284 y el flag desconocido en 0274 -- y las dos fueron trabajo manual tuyo. 0283 lo mecaniza:
cada negativo declara la mutacion que lo mata, y una comprobacion la aplica y exige rojo. Si
una mutacion declarada ya no mata su test, la comprobacion falla.

## Por que esta es la que mas hay que atacar

Es recursiva: un guardian que verifica que los tests pueden fallar. Si el guardian mismo no
puede fallar, hemos movido la sombra una capa mas arriba y nada mas. Asi que tu escrutinio de
0283 va sobre 0283:

1. **Relaja una asercion declarada de un negativo REAL** que elijas tu (no el del maker) y
   exige que la comprobacion se ponga ROJA.
2. **El inventario 14/14**: que sea real, que cuente los negativos que existen y no una lista
   que se auto-satisface.
3. **Un negativo nuevo sin mutacion declarada** debe hacer FALLAR el inventario -- que no se
   pueda colar un test-sombra sin declarar como lo mata.
4. **Fronteras multiples** (el R1 de 0280): un negativo sostenido por dos aserciones -- relajar
   UNA debe detectarse, para que quitar la vieja no deje el test vivo en apariencia.

## Contexto

Tercera de la cola de higiene. La entrega tuvo un traspie (exec de Codex muerto, claims
colgantes) que su propio reintento corrigio -- la maquinaria de integridad, otra vez, sin
quemar nada ni dejar el arbol roto. Commit final 7afb122, validate verde. No cuenta contra la
unidad.
