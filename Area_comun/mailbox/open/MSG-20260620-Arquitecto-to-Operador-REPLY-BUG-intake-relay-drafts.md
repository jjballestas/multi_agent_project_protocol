---
message_id: MSG-20260620-Arquitecto-to-Operador-REPLY-BUG-intake-relay-drafts
task_id: TASK-0133
type: DECISION
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
in_reply_to: MSG-20260620-Operador-to-Arquitecto-BUG-intake-execute-actor-no-registrado
one_line_summary: "Acepto el hallazgo y reconozco mi MISS de checker (cerre 0133 sin probar el camino feliz real, solo dry_run+409). Mecanismo elegido = (b) RELAY: el intake lo firma el Arquitecto (firmante pinned) EN NOMBRE del Operador (author=Operador en el payload); #4 epoca 1.14.0 INTACTA, sin re-genesis. Probado: actor=Operador rechazado, actor=Arquitecto pasa. 3 drafts: DECISION-0052 (amends 0051) + ext2 SPEC-0086 (AC15 camino-feliz + AC18 atribucion) + TASK-0134 (fix+test+UX project-first). Espera ratificacion."
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0052-operator-intake-relay-signer.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext2-intake-happy-path.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0134-intake-happy-path-relay.md
deadline_or_blocking_level: blocking
---

# REPLY - BUG intake (camino feliz roto): mecanismo RELAY + reconocimiento del miss

## Reconozco el miss de checker (sin excusas)
Cerre TASK-0133 probando dry_run + el 409 negativo, pero **NUNCA ejecute el camino feliz real**
(execute+confirm -> escritura). Se fue verde-pero-incompleto. Es la misma leccion AC11: hay que probar el
COMPORTAMIENTO real, no solo la prueba negativa. Lo corrijo abajo y lo vuelvo AC permanente.

## Causa (confirmada y probada)
Bajo #4 enforce el runtime exige que el actor de cada evento este registrado Y firme. `Operador` no esta en
`agent_registry` ni en `protocol.config.json:event_auth.keys` -> rechazo. **Probado:** actor=Operador ->
"actor not registered/enabled"; actor=Arquitecto -> pasa el registro. El conjunto de firmantes vive en el
config, cuyo hash es el `prev_hash` del genesis -> **agregar al Operador como firmante = editar el config =
re-genesis = toca la epoca 1.14.0 PINNED.** Por eso `actorId:Operador` (lo que fijo 0051) era inviable.

## Mecanismo elegido -> (b) RELAY / co-firma por firmante pinned
El intake lo escribe **el Arquitecto** (firmante ya anclado al genesis) **EN NOMBRE del Operador**:
- front emite EXECUTE con `actorId:"Arquitecto"` -> firma con clave pinned -> **cadena #4 intacta, sin
  re-genesis, epoca 1.14.0 PINNED**.
- payload requirement con autoria honesta: `author:"Operador"`, `origin:"front-intake"`,
  `relayed_by:"Arquitecto"`. El dataset NO afirma que el Operador firmo; afirma que el Arquitecto RELAYO un
  requisito ORIGINADO por el operador. La UI lo declara (AC18, lente Analista: nada de verde/atribucion falsa).

Descarto (a) actor no-firmante (el runtime firma POR el actor; no hay actor sin secreto sin cambiar el modelo
de firma) y (c) re-genesis (lo mas pesado; pertenece a la ceremonia RF-9 roster DIFERIDA; queda como camino
futuro si quieres tu propia firma criptografica).

## Drafts (en personal/Arquitecto/carril_A/, sin promover)
- **DRAFT-DECISION-0052** (amends 0051): mecanismo RELAY; #4 intacto.
- **DRAFT-SPEC-0086-ext2**: AC15 revisado (negativo **y** CAMINO FELIZ = write real demostrado) + AC18
  (atribucion honesta del relay); RF-14 modelo de escritura actualizado.
- **DRAFT-TASK-0134** (maker=Codex/checker=Arquitecto): relay-signer + test del camino feliz + UX
  project-first + tipografia del selector (insumo Claude Design). NO se cierra sin ejecutar el write real.

## UX (lo paso a Claude Design)
project-first (selector de proyecto primero; demas campos habilitados tras elegir) + tipografia del selector
destacada. No bloqueante; entra en el rework.

Espera tu ratificacion para promover (DECISION-0052 -> ext2 SPEC-0086 -> GO TASK-0134 a Codex). #4 epoca
1.14.0 intacta en todo el camino. Etapa 5 roster sigue DEFERIDA.
