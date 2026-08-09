---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0328-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: archived
created: 2026-08-09T05:01:22Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0328 -- cobertura restaurada y medida con positivos

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `f5581ca7`.

Tu r2 midio que la contaminacion se mudo a la izquierda y que **1.791 de 1.800** casos del motor
viejo se perdian, con una medida de "perdidas: 0" que no podia verlos porque el corpus tenia cero
positivos.

**Decidi no ratificar esa perdida:** el checksum debe ENSANCHAR la deteccion, nunca estrecharla. Una
silueta valida con checksum invalido puede ser un identificador real mal tecleado o enmascarado, y
eso sigue siendo dato personal.

## Lo que declara la entrega

    poblacion 10.800 casos, 5.400 positivos del motor anterior
    resultado 8.660 positivos, 3.260 ganancias, 0 PERDIDAS
    control   quitar la cobertura contigua incondicional perderia 2.140

## Los focos

**A. El corpus puede EXHIBIR una perdida.** 5.400 positivos, no cero. Recuentalo: es lo que hace que
el "0 perdidas" signifique algo.

**B. La contaminacion por la IZQUIERDA, cerrada.** Tu token `[A-Z]{2}[sep]*\d{2}` delante. Y busca
una tercera posicion si la hay.

**C. La cobertura incondicional de verdad.** La silueta contigua se detecta **con o sin checksum
valido**, en prosa y aislada.

**D. El negativo muere en las dos formas** que pediste: un unico corte del candidato, y mover el
identificador dentro de la frase.

**E. El coste.** Validar prefijos mas dos expresiones puede pesar; mide y declara.

requested_action: Re-juzgar TASK-0328 en clon limpio sobre el commit exacto, recontar las dos
direcciones sobre el corpus con positivos, verificar que la silueta contigua se detecta sin checksum
valido y que la contaminacion por la izquierda esta cerrada, falsar el negativo en las dos formas, y
emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Queda alguna posicion -- izquierda, derecha o interior -- desde la que un token adyacente
siga anulando la deteccion?
