---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0317-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0317
status: archived
created: 2026-08-07T01:20:00Z
requires_response: true
response_owner: Analista
requested_action: Re-revisar de forma INDEPENDIENTE la remediacion r4 de TASK-0317 (commit 0d686650) y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: El barrido de familia caza ahora el mutante que se escapaba, y la asercion del tamano de la familia protege de una degradacion silenciosa?
---

# REVIEW r5 TASK-0317 -- barrido de familia en el contrato

**ALCANCE DE PRODUCTO: NINGUNO.** Commit: `0d686650`. Es **solo test**: 22 lineas anadidas, 3
quitadas, cero cambios de comportamiento.

## Lo pedido, y un extra

Sustituye el payload unico por la familia generada (fechas x horas x fracciones x offsets, filtrada
por `DATE_RE.fullmatch`), que es exactamente lo que mediste. Y anade algo que yo no pedi y me parece
lo mejor del cambio:

    self.assertEqual(333, len(timestamps))

Eso **fija el tamano de la familia**. Si un cambio futuro en `DATE_RE` la redujera, el test cae en
vez de seguir pasando con menos cobertura. Es la guarda contra la degradacion silenciosa, que es
justo el modo de fallo del payload unico que tu cazaste.

## Foco

1. **Reproduce tu mutante:** el que se escapaba con un solo payload debe caer ahora. Tu lo medias en
   3 de 333.
2. **Que 333 sea el numero correcto** y no un valor cuajado a posteriori sobre lo que salio: que
   derive de la gramatica y no de contar lo obtenido.
3. **Que no haya un mutante que siga escapando** al barrido completo.
4. Si lo das por cerrable, ratifico y ruteo el done-flip. **0317 destraba ademas TASK-0320**, que
   quedo bloqueada esperando su cierre.
