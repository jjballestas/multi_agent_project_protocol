---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0343
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0343
status: open
created: 2026-08-09T06:39:51Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0343 -- la asercion de rollback atada a contadores

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Esta tarea **ya tiene su efecto verificado en Actions**: el job `falsification-runners` recupero el verde y el run
`31270228630` lo respalda. Eso es evidencia fuerte y poco habitual aqui, asi que el foco no es si
funciona sino **por que propiedad**.

## Los focos

**A. El arreglo ata la propiedad o la ocurrencia.** Falsalo con una variante que no sea la que
fallaba: si solo cubre el caso exacto que rompio, seguimos en la misma clase.

**B. El negativo permanente existe y MUERE por mutacion**, incluida la forma de codigo muerto.

**C. Lo declarado corresponde a lo medido.** El handoff no debe afirmar mas de lo que su evidencia
sostiene; si algo quedo sin medir, debe ir declarado como residual.

**D. Sin regresion** en lo que ya estaba verde.

## Nota

Estas tareas nacieron de la jornada en que descubrimos que **CI llevaba 300 runs sin un solo
verde**. Su valor no es el parche sino que el fallo vuelva a ser visible al introducirlo. Juzga eso.

requested_action: Revisar TASK-0343 en clon limpio sobre el commit de entrega, falsar el arreglo con
una variante distinta de la que fallaba, verificar el negativo por mutacion, comprobar que lo
declarado corresponde a lo medido, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El arreglo cubre solo la variante que fallaba, o cualquier miembro de su clase?
