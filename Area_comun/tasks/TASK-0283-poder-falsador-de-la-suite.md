---
task_id: TASK-0283
title: "[SUITE] El poder falsador no puede depender de una asercion vieja: cada negativo declara que mutacion lo mata y se verifica que sigue matandola"
type: infra
status: ready
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-21
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0280, TASK-0281, DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
intake:
  type: infra
  goal: "Residuales R1 y R3 del veredicto de cierre de TASK-0280, registrados como unidad propia porque un residual sin acceptance se evapora -- leccion pagada el 2026-07-20 con TASK-0275, cuyo diferimiento acabo destruyendo un mensaje de review completo. R1: el poder falsador del brazo reparado no lo sostiene la asercion nueva sola, sino DOS aserciones con fronteras distintas; dos de las nueve mutaciones del checker pasaron la barrera nueva y murieron en la vieja. Eso significa que un cambio futuro en la asercion vieja debilita el test SIN que nadie lo note, que es exactamente el modo de fallo que acabamos de reparar (un negativo permanente que dejo de poder fallar y siguio en verde durante iteraciones). R3: el mismo patron en el resto de la suite, sin inventario."
  acceptance:
    - "Cada negativo permanente de la suite declara EXPLICITAMENTE que mutacion del codigo lo debe matar, junto al propio test y no en un documento aparte."
    - "Existe una comprobacion que aplica esas mutaciones declaradas y exige que el test correspondiente se ponga ROJO; si una mutacion declarada ya no mata su test, la comprobacion falla."
    - "Inventario de los negativos existentes: cuales tienen su mutacion declarada y cuales no, con numeros, sin dejar el resto como 'pendiente' indefinido."
    - "Cuando el poder falsador dependa de mas de una asercion, queda escrito cual es la frontera de cada una, para que quitar o relajar una no deje el test vivo en apariencia."
    - "Espejo en el export born-operational."
  verification_cmd:
    - "Runner de la comprobacion de mutaciones declaradas en verde"
    - "Prueba negativa: relajar una asercion declarada y comprobar que la comprobacion FALLA"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - examples/
    - scripts/
  out_of_scope:
    - "Introducir una herramienta externa de mutation testing - FUERA: basta con declarar y ejercitar las mutaciones que ya elegimos a mano."
    - "Reabrir el acceptance de TASK-0280 o TASK-0281 - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: low
  estimate: M
---

# TASK-0283 - Un test que no puede fallar es peor que no tenerlo

Origen: residuales R1 y R3 del veredicto de cierre de TASK-0280, donde el checker verifico
el poder falsador con nueve mutaciones propias en tres ordenamientos y cuatro formas de dano.
Ocho de nueve mataron el brazo reparado. Pero dos de ellas **no murieron en la asercion
nueva**, sino en una vieja con otra frontera.

El riesgo no es teorico ni futuro: **ya nos paso**. Un negativo permanente de esta misma
familia dejo de poder fallar y siguio en verde durante iteraciones, dando confianza sin
sostenerla, hasta que el checker lo midio con control positivo. Lo que esta unidad pide es
que esa medicion deje de depender de que a alguien se le ocurra hacerla.

La regla que ya adopte en los encargos y que aqui se vuelve mecanica: **un negativo se
entrega con la mutacion que lo mata, y esa mutacion se vuelve a ejercitar**. Si el test
sobrevive a su propia mutacion declarada, el test esta muerto aunque este verde.
