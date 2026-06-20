---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0134
task_id: TASK-0134
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0134 (ready, maker=Codex): REMEDIACION DE SEGURIDAD del intake RF-14. Anti-impersonacion (builders SERVER-SIDE estrictos; eliminar trust de payload.actorId/intents; relay-como-Arquitecto SOLO para la forma exacta requirement-intake; prueba negativa permanente) + accountability (endorsement:none) + camino feliz WRITE REAL + render honesto + #4 byte-identico. Ratificado DECISION-0052 + ext2 SPEC-0086 (AC15/AC18/AC19/AC20). Codigo en Zeus-protocol; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0052-operator-intake-relay-acotado-anti-impersonacion.md
  - Area_comun/tasks/TASK-0134-codex-intake-remediacion-seguridad.md
  - Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# GO - TASK-0134 remediacion de seguridad del intake (RF-14)

Ratificado por el operador (DECISION-0052 + ext2 SPEC-0086). Es REMEDIACION de un defecto CRITICO ya mergeado
(Zeus 42e7931): server.js confia en payload.actorId (linea 384) + payload.intents crudos (linea 371) en
endpoint sin auth -> POST local forja evento atestado firmado como Arquitecto. maker=Codex / checker=Arquitecto.

## Lo esencial
- **#1 ANTI-IMPERSONACION (AC19, CRITICO):** eliminar `payload.actorId` y `payload.intents` crudos. Cada
  accion = builder SERVER-SIDE estricto (el server construye el intent desde campos validados). `actorId`
  server-side. Relay-como-Arquitecto SOLO para la forma exacta `requirement-intake`. **Prueba negativa
  PERMANENTE en CI:** forjar actorId/intents/forma != intake como Arquitecto -> RECHAZADO.
- **#3 ACCOUNTABILITY (AC20):** `endorsement:none`; firma=origen+transporte, no aval; test relayado != autorado.
- **CAMINO FELIZ (AC15) WRITE REAL (no mock):** execute+confirm -> escritura real (requirement en estado,
  seq, drift 0, author=Operador/relayed_by=Arquitecto). Test de comportamiento permanente.
- **RENDER (AC18):** firmante=Arquitecto + author=Operador; ningun verde "Operador firmo".
- **#4 byte-identico:** config/genesis/keys/version byte-identicos (no solo drift 0).
- **PII (AC16):** redaccion best-effort por patrones; NO sobre-afirmar PII-free. **UX:** project-first +
  tipografia del selector destacada (rework components/intake/).

## Cierre INNEGOCIABLE
NO cierra sin (a) AC19 anti-impersonacion VERDE y (b) AC15 write-real VERDE. **Nueva pasada del Analista sobre
el fix de #1 ANTES de cerrar.** Gates: node --test/CI verde, validate exit 0 con/sin secretos, drift 0, #4
epoca 1.14.0 byte-identica, neutralidad. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega via submit_intent (in_review) cuando este verde; yo reproduzco como checker (incluyendo impersonacion
+ write real) y, con la pasada del Analista, cierro.
