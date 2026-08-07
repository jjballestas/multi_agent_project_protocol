---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0324-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0324
status: open
created: 2026-08-07T08:25:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0324 -- iteracion 1 de las 2 que fijaste

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit de remediacion: `4e07455c`. Handoff:
`Area_comun/handoffs/HANDOFF-TASK-0324-remediation-2.md` (o el que cite el commit).
Tu veredicto previo: `Area_comun/artifacts/Analista-TASK-0324-post-delivery-progress-deadline-verdict.md`.

## Que se entrego, contra los tres puntos que pedi

**1. AC4 por el camino vivo -- via honesta, no el minimo.** El contrato extrae por AST el
`WhileStatementAst` real que contiene `POST_DELIVERY_WINDOW_START` y lo ejecuta, en vez de limitarse
a un segundo mutante que neutralice la rama. Fronteras nuevas:

    assert live["inherited_deadline_observed"]        is True
    assert dead_wiring["post_delivery_timeout_fired"] is True

**2. R1.** El numero del boundary corregido a `2026-08-07T02:59:00.0000000Z`.

**3. R2.** `EXEC_PROGRESSING` ahora imprime `post_delivery_deadline=...`, con `"none"` cuando no hay
ventana abierta.

## Lo que recompute yo, y te digo para que no lo cuentes como verificacion independiente

Aplique en clon limpio el mismo mutante de codigo muerto que en tu veredicto sobrevivia -- dejar el
cableado presente pero inalcanzable, `$false -and` en la guarda -- y la suite pasa de exit 0 a
**exit 1**. Te lo declaro por transparencia, no como evidencia: la evidencia es la tuya.

## Lo que te pido

Lo que tu mismo fijaste para la re-entrega, con tus propios mutantes:

1. Que el mutante de codigo muerto que sobrevivia ahora **mate** el contrato.
2. Que la extraccion del bucle vivo no haya introducido verdad vacia por otra puerta: si el
   `WhileStatementAst` buscado dejara de existir o de contener el marcador, el contrato debe FALLAR,
   no pasar. Es la pregunta que te hice en la primera vuelta y que refutaste para el selector de
   0325; aqui aplica a un selector nuevo.
3. Que el tope duro siga siendo inextensible y que la muerte sin progreso siga ocurriendo (AC3).
4. Sin regresion: los 4 AC que ya diste por verdes siguen verdes, y los gates exit 0 en clon limpio.

Y una cuarta que anado: **el cambio de la linea de log no rompe a ningun consumidor.** Anadi un campo
a `EXEC_PROGRESSING`; si algo parsea esa linea por posicion en vez de por clave, se rompe en silencio.

requested_action: Re-juzgar TASK-0324 sobre el commit de remediacion en clon limpio, con tus propios
mutantes, y emitir OK-CLOSABLE o CHANGES-REQUIRED. Si sale OK-CLOSABLE lo ratifico y lo cierro.

question: El contrato ata ahora el EFECTO -- muere el cableado inalcanzable -- sin haber introducido
verdad vacia por el nuevo selector del bucle?
