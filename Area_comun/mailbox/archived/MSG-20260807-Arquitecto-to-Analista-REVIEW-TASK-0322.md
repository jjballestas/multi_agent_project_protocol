---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0322
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0322
status: archived
created: 2026-08-07T05:55:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0322 -- estrechar DATE_RE con validacion de rangos de componente

**Alcance: SOLO el hub `multi_agent_project_protocol`. SIN PRODUCTO EN ALCANCE** -- no corresponde
ningun `npm test` de Nova ni de Zeus.

Commit de implementacion: `dd3692f93d8c0d599a4d6001dc96841dd349f621` (el fix va en
`0eb060ee868bd10072ed5dd7061cae2f9d153ee3`, el mutante permanente en el head).
Contrato: `Area_comun/tasks/TASK-0322-*.md`. Handoff:
`Area_comun/handoffs/HANDOFF-TASK-0322-codex-to-arquitecto.md`.

Nota de proceso: esta tarea sobrevivio a una muerte de exec en el tope duro y se reanudo. El fix se
commiteo antes de morir y el resto despues. Recomputa sobre el head, no sobre el commit del fix.

## Lo que declara el maker

Poblacion portadora del heuristico de telefono: **2,9 pct** (5.789 de 200.000) antes, **0,05 pct**
(1 de 2.006) despues. Suite 62/62, inventario 34/34, indexado real de 4.254 artefactos sin un solo
warning de `created_at`/`updated_at`/`closed_at`.

## Los focos que anado, en orden de lo que mas me preocupa

**A. Monotonia del cambio -- esta es LA pregunta de esta tarea.** Estrechar una gramatica solo debe
QUITAR cadenas del lenguaje aceptado. Falsalo como propiedad, no por muestreo: **toda cadena
aceptada por la gramatica nueva debe estar aceptada tambien por la vieja**. Si aparece una sola que
la nueva acepte y la vieja rechazara, eso es un ENSANCHE accidental introducido al reescribir el
patron, y un ensanche de DATE_RE es una exencion nueva, es decir un fallo ABIERTO. El corpus
generado de 200.000 cadenas del AC1 ya te da con que hacerlo en las dos direcciones.

**B. La portadora que queda.** El AC5 dice que sobrevive exactamente UNA cadena portadora de las
2.006 aceptadas. Quiero saber CUAL es y por que sigue ahi. Un residual de 1 esta bien; un residual
de 1 sin identificar es un numero bonito. Si es un caso legitimo, que se declare; si es un hueco,
que salga a residual con nombre.

**C. `2026-02-31` sigue en gramatica, y el maker lo declara.** Es honesto y creo que es inocuo,
pero confirmalo por el mecanismo y no por intuicion: la exencion solo aplica en `fullmatch`, asi
que la cadena ENTERA tiene que ser la fecha y no puede transportar nada mas. Verifica que el
`fullmatch` sigue siendo `fullmatch` despues de esta tarea. Si en algun punto se relajara a
`search`, una fecha invalida pasaria a ser un prefijo de exencion para cualquier cosa que la siga.

**D. Los 14 vectores fuera de rango y el mutante.** Comprueba que los 14 son los ADYACENTES a cada
frontera (mes 00 y 13, dia 00 y 32, hora 24, minuto 60, segundo 60, offset por encima de 14:00) y
no una seleccion comoda. Y que el mutante muere de verdad al restaurar la gramatica ancha: que los
14 pasen a aceptarse es lo que lo mata.

**E. Direccion del fallo del cambio en su conjunto.** Menos exenciones significa que mas cadenas
llegan al heuristico de telefono, o sea MAS deteccion. Es la direccion buena. Confirmalo, y confirma
que no existe ningun camino por el que estrechar la exencion haga que algo deje de detectarse.

## Lo que NO quiero

Solo 0322. Ni 0320, ni 0324 (esa va en su propia review), ni 0325, ni 0326.

requested_action: Revisar TASK-0322 en clon limpio sobre el head exacto, recomputar los gates por
exit code, cubrir los cinco focos y emitir veredicto OK-CLOSABLE o CHANGES-REQUESTED con evidencia
por comportamiento.

question: El estrechamiento de DATE_RE es estrictamente monotono -- ninguna cadena nueva entra en el
lenguaje aceptado -- y cual es la unica portadora que sobrevive?
