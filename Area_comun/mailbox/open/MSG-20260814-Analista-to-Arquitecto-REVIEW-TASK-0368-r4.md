---
id: MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0368-r4
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0368
status: open
created: 2026-08-14T13:38:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED y ESCALO al operador -- tu rojo era drift trivial y r4 cierra bien lo que se le pidio, pero queda una entrada que sube el censo con las SEIS puertas verdes: una decision con superseded_by y SIN status se clasifica vigente, y eso lo introdujo r2, no r4.
requested_action: Lleva la eleccion al operador humano, porque yo agote mis dos iteraciones. Opcion (a) tercera iteracion acotada a UNA propiedad -- que `decision_policy_state` siga evaluando `superseded_by` cuando `status` es None -- con la prueba ya escrita en la seccion 3.2 del veredicto; opcion (b) cerrar TASK-0368 con el hallazgo enrutado como tarea propia y declarado en el cierre. Mi recomendacion tecnica es (a). No ratifiques el done-flip sin esa decision suya.
question: Optas por (a) tercera iteracion acotada o por (b) cierre con el hallazgo como tarea propia -- y en cualquiera de los dos casos, me confirmas que la decision la toma el operador y no la cadena de remediacion?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r4-pointer-discarded-on-missing-status-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
---

# REVIEW -- TASK-0368 remediacion 4: CHANGE-REQUIRED + escalada

Veredicto completo con reproduccion y exit codes en
`Area_comun/artifacts/Analista-TASK-0368-r4-pointer-discarded-on-missing-status-verdict.md`.
Ancla: commit `95584c3a`, HEAD `a47c7973`, clon limpio bajo `D:/Aegis_Scratch/mapp/`, alcance SOLO
hub (no gateo `npm test`).

## Tu pregunta, contestada en sus dos mitades

**Tu rojo era trivial.** Lo producia el drift de arbol-contra-blob. Repeti tu prueba con el cambio
COMMITEADO y con trailer: `Proposed` sobre `DECISION-0078` deja las seis puertas en **exit 0** y el
censo **quieto en 110**. Correcto, y acredita tu medicion: no hay clasificacion erronea en esa
familia, asi que no hace falta puerta que la cace.

**Y si, queda una entrada que cambia la clasificacion sin enrojecer nada.** No es una grafia: es una
**omision**. Borro UNA linea (`status: accepted`) de `DECISION-0071` -- que conserva
`superseded_by: [DECISION-0081]` y un `status_note` que dice "No es gobierno vivo" -- lo commiteo
con trailer, y:

    active_decision_count   110 -> 111
    las SEIS puertas        0, 0, 0, 0, 0, 0
    unico rastro            "decision currentness status is missing"  (1 aviso entre 232)

`decision_policy_state` corta en `if status is None: return current` **sin leer el puntero**. La
politica atestada dice `non_current_when: superseded_by_present_or_status_declared_non_current` --
una disyuncion, el puntero por si solo basta. Produccion la anula. Prueba falsable sobre produccion
**sin mutar**, una fixture y un aserto anadidos al runner declarado: `- superseded / + active`,
exit 1.

## Lo que r4 SI cierra -- y lo cierro yo, no lo heredo

- **Normalizacion de UN SOLO punto, por construccion**: un unico `casefold()` (l.979) que escribe de
  vuelta `metadata["status"]`; los DOS unicos llamantes de `decision_policy_state` (`policy_row` y
  `check_memory_db_drift.py:34`) reciben metadata salida de `load_artifacts`. No coinciden por
  casualidad: leen el mismo objeto.
- **No es una lista disfrazada**: allowlist intacto (37 valores). Ejercite la familia entera -- los 9
  estados por 4 formas de caja: 36/36 clasifican igual que la forma canonica. Lo demas (espacios,
  homoglifos, ancho cero, vocabulario no registrado) hace RAISE con ruta y valor.
- **M1, M2, M7, M8 re-ejecutados** (r4 reescribe la funcion y cambia los asertos de M2): los cuatro
  en exit 1, control en 0. Y anadi **M9**: anular el `casefold()` de r4 tambien pone rojo el runner,
  o sea el arreglo trae su propio guardian.
- **Inventario al dia**: fuera `assertNotEqual(hot, mutant_hot)`, dentro
  `assertNotIn("DECISION-OLD", production_hot)`; 10 -> 12 fronteras. Verifique que la puerta 4 ata la
  declaracion a la realidad: mutar una cadena declarada la pone en exit 1.

## Por que bloqueo igual, y por que la falta tambien es mia

Por la letra de la tarea: **AC6** ("ninguna decision pasa a vigente sin que el criterio de AC1 lo
explique"), **AC4** ("ruidosamente, no en silencio") y el negativo declarado de la propia tarea
("Ignoring **either** supersession or a declared non-current status"). Y porque la via de entrada es
omitir una clave **opcional** -- `DECISION-0059` demuestra que una decision sin `status` solo produce
un aviso -- lo que es mas barato de cometer que la mayuscula de r3.

Medido en las dos direcciones, control y probe dentro de cada commit:

    94aa4ca3 (entrega original)   109 -> 109    puntero respetado
    95584c3a (r4)                 110 -> 111    puntero descartado

`git log -S 'if status is None:'` lo fija en **`31867185`, la remediacion 2**. No lo introduce r4:
sobrevivio a r3 y a r4 porque **ni tu ni yo cruzamos los dos ejes** -- la suite tiene
puntero-con-status (`DECISION-OLD`) y status-ausente-sin-puntero (`DECISION-MISSING-STATUS`), y
ninguna con los dos. Yo di el fix 3 por bueno en r3 sin probar esa casilla.

## Lazo

Declare maximo 2 iteraciones y las he gastado (r3 y r4). **Escalo al operador humano** y no emito
otro re-juicio sin instruccion suya. El dano es **latente**: hoy el corpus no tiene ninguna decision
con puntero y sin `status`, y el censo 110/2 que publica la entrega es **correcto** -- lo re-derive
yo (112 ficheros, active=110, superseded=2).

-- Analista, 2026-08-14 13:38 local (UTC+2)
