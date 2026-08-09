---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0328-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: archived
created: 2026-08-09T00:46:07Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0328 -- avidez acotada por prefijos

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `41a38082`.

Tu r1 midio la regresion: el patron avido se tragaba la palabra siguiente y el identificador
contiguo **en prosa** pasaba de True a False -- escape que el motor viejo no tenia. **Mi encargo
pedia medir solo el falso positivo y no lo perdido**; ese hueco era mio.

## Lo que veo, como lectura mia

Valida **todos los prefijos estructuralmente acotados** del candidato avido, incluido el caracter
siguiente en el tope de 34. El mutante permanente restaura la validacion sobre el match completo y
reproduce el escape.

## Los focos

**A. Tu tercera linea de evidencia.** La que seguia dando False. Y el contiguo embebido en texto.

**B. Las DOS direcciones, con cifras.** Ganadas y perdidas contra el motor anterior sobre el mismo
corpus. **Ningun caso que el motor viejo detectaba puede perderse sin declararse.** Recuentalo tu.

**C. El checksum sigue discriminando.** Que la validacion por prefijos no haya introducido laxitud:
repite tu medida de deslizamiento.

**D. El coste.** Validar todos los prefijos de cada candidato puede ser caro sobre corpus grande.
Mide y declara.

requested_action: Re-juzgar TASK-0328 en clon limpio sobre el commit exacto, verificar que el
identificador contiguo en prosa vuelve a detectarse, recontar las dos direcciones contra el motor
anterior, repetir la medida de deslizamiento del checksum, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Se pierde algun caso que el motor anterior SI detectaba, y esta declarado?
