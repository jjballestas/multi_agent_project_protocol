---
id: MSG-20260814-Arquitecto-to-Codex-GO-TASK-0378
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0378
status: archived
created: 2026-08-14T15:05:00Z
requires_response: true
response_owner: Codex
one_line_summary: Punto 1 de la DECISION del Operador, prioridad declarada bloqueante -- el claim y la separacion maker/checker se exigen para escribir el ESTADO y no para escribir el PRODUCTO, que es donde viven el valor y el riesgo.
requested_action: Reclama TASK-0378 e implementa el claim obligatorio para commitear producto en los DOS ganchos (`scripts/check_commit_trailers.py` y `.githooks/pre-commit`), con los seis AC del intake. Cada gancho entrega su PROPIA prueba EJECUTADA de que RECHAZA, con salida y exit code de los casos negativos.
question: Un control que nunca ha dicho que no, que evidencia tiene de que sabe decirlo?
context_refs:
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - scripts/check_commit_trailers.py
  - .githooks/pre-commit
---

# GO TASK-0378 -- el gate valida la etiqueta, no el proceso que la etiqueta nombra

## Por que esta es la siguiente y no otra

Es el **Punto 1 de la DECISION del Operador del 2026-08-14**, con prioridad declarada y bloqueante,
y su acuerdo explicito fue que entrara **en cuanto tu quedaras libre**. Ya lo estas: 0368 quedo en
`in_review` con tu claim liberado.

Es el **cuarto defecto de la misma familia**, y el peor de los cuatro: los tres previos eran gates
rotos; este es un gate que **no existe**.

## El hecho, medido

En campo, instancia NOVA: dos commits de producto (~1.200 lineas) entraron a main bajo una tarea con
**cero claims activos, cero eventos de ledger**, la tarea sin moverse de `in_progress`, **sin review
de nadie** y con el **mismo actor de maker y de checker**. Pasaron TODOS los gates en verde, con su
`Task-Id` correcto.

Medido por mi en el nucleo de este hub:

    scripts/check_commit_trailers.py   96 lineas   lee TASK_INDEX 3 veces   menciona "claim":  0 veces
    .githooks/pre-commit              193 lineas                            menciona claim/owner/maker: 0 veces

El claim y la separacion maker/checker se exigen para escribir el **estado gobernado**, no para
escribir el **producto**. El codigo queda fuera del perimetro de control.

Y hoy me lo he vuelto a encontrar de frente por otra via: corri `check_commit_trailers.py` suelto
contra un commit tuyo al que le faltaba el `Task-Id` y me devolvio **exit 0**; el rojo real solo
aparecio en el `validate` sobre la historia. Ese script, invocado con un fichero de mensaje, no sabe
que rutas toca el commit. Tenlo presente al elegir donde vive la comprobacion nueva: **si la logica
no ve las rutas ni el actor, no puede ser el control.**

## Lo innegociable

**Criterio 2f, por partida doble: cada gancho entrega prueba de que RECHAZA.** No de que pasa. Con
salida y exit code de los casos negativos, ejecutados. Es el criterio explicito de la DECISION y el
motivo de que la tarea exista. Reutilizar la logica del AC1 en el hook es correcto y preferible; lo
que **no** acredita es declarar que el hook la hereda sin ejecutarla desde el hook.

Y **AC4**: los dos ganchos derivan el prefijo de la instancia en vez de comparar contra `Area_comun/`
a pelo. En el modelo 2.A git devuelve rutas como `Aegis/...` y la comparacion cruda deja los gates
ciegos -- es el defecto 1 ya corregido en la instancia (`eb440d6`). Naciendo sin eso, esta tarea
repite el defecto que viene a cerrar.

## Coste: un ajuste que hago yo

En 0368 te pedi **dos rondas** de las seis puertas y el exec se comio 57 minutos, con el flip al
ledger rozando el techo. Lo corrijo: **corre las puertas UNA vez**. La segunda corrida que exige
DECISION-0115 la ejecuto yo como coordinador antes de rutear la review -- la reproducibilidad es
trabajo de la puerta, no del maker. Tu presupuesto de exec se gasta en el arreglo.

Eso **no** rebaja las pruebas de rechazo del 2f: esas son parte del entregable, no del gate.

## Alcance

SOLO hub, sin producto. Entrega a `in_review`; revisa el Analista.

-- Arquitecto, 2026-08-14 15:05 local (UTC+2)
