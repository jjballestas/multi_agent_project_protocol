---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-remediacion-seguridad-relay
task_id: TASK-0134
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "NO ratifico el relay como esta. La pasada adversarial del Analista (canonico) destapo un DEFECTO DE SEGURIDAD CRITICO YA EN CANONICO (verificado por mi en server.js 42e7931): el endpoint local sin auth confia en payload.actorId y en payload.intents ARBITRARIOS para acciones no-intake -> un POST local (o pagina drive-by a 127.0.0.1) puede forjar decision/claim/task_status ATESTADO firmado como Arquitecto; el enforce #4 no lo para. TASK-0134 pasa a ser REMEDIACION DE SEGURIDAD: cierra #1 (impersonacion) y #3 (accountability) + cambios del Analista. NO cerrar sin la prueba negativa de impersonacion verde. Bloqueante."
requested_action: "Rehaz DECISION-0052/SPEC-0086-ext2/TASK-0134 como REMEDIACION (no solo 'agregar el relay'). Incorpora el veredicto del Analista (Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md). (1) #1 IMPERSONACION (CRITICO, bloqueante): hoy server.js (Zeus 42e7931) hace `actorId = action.actorId || payload.actorId || 'Arquitecto'` y para acciones no-intake toma `intents` ARBITRARIOS del payload (solo valida el kind). Endpoint 127.0.0.1 SIN auth. -> se puede forjar un evento atestado firmado como Arquitecto. FIX: nunca confiar en payload.actorId; cada accion = builder SERVER-SIDE con forma estricta (NO intents crudos del cliente); relay-como-Arquitecto SOLO para la forma exacta del requirement-intake; PRUEBA NEGATIVA PERMANENTE (intentar relayar cualquier otro intent/forma como Arquitecto -> RECHAZADO). Es la anomalia DECISION-0018 ya mergeada: remediarla, no solo 'no empeorarla'. (2) #3 ACCOUNTABILITY: la firma del relay = ORIGEN+TRANSPORTE, NO aval; DECISION-0052 lo declara explicito (el aval es la SPEC despues); test de que un relayado NO cuenta como autorado por el Arquitecto. (3) Cambios del Analista: test de RENDER (firmante=Arquitecto; ningun verde que diga 'Operador firmo'); asertar genesis/keys/version BYTE-IDENTICOS (no solo drift 0); AC15 happy-path = write REAL demostrado (no mock) + test de comportamiento permanente en CI; NO sobre-afirmar 'PII-free' (la redaccion es best-effort por patrones, no cero-PII garantizado; DEF-PII/TASK-0118 sigue el gate). (4) Considera (tu decision) endurecer el endpoint local con confirmacion/auth, ya que aun acotado al intake una pagina drive-by podria inyectar una semilla falsa (severidad menor; puede ser follow-on). CONDICION DE CIERRE: TASK-0134 NO cierra sin (a) la prueba negativa de impersonacion VERDE y (b) el happy-path con write REAL verde. maker=Codex/checker=Arquitecto, SDD, reproduccion desde clon limpio. Pasada del Analista de nuevo sobre el fix de #1 antes de cerrar. Drafts para mi ratificacion."
question: "Reabres TASK-0134 como remediacion de seguridad (cierras #1 impersonacion + #3 accountability + cambios), con la prueba negativa de impersonacion como condicion de cierre innegociable? Reporta drafts."
context_refs:
  - Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md
  - Area_comun/mailbox/open/MSG-20260620-Analista-to-Operador-relay-veredicto-adversarial.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0052-operator-intake-relay-signer.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext2-intake-happy-path.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0134-intake-happy-path-relay.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# GO - TASK-0134 = REMEDIACION DE SEGURIDAD (no ratifico el relay como esta)

La pasada adversarial del Analista (voz externa) destapo, y yo verifique en el codigo canonico
(Zeus 42e7931), un **defecto de seguridad critico que YA esta mergeado**:

```
actorId = action.actorId || payload.actorId || "Arquitecto"
intents (no-intake) = payload.intents   // arbitrarios del cliente, solo se valida el kind
endpoint 127.0.0.1 SIN auth
```

-> Un POST local (otro proceso, o una pagina drive-by a localhost) puede **forjar una decision/claim/
task_status ATESTADO firmado como Arquitecto**. El enforce #4 no lo para (Arquitecto es firmante). Esto
rompe la integridad de la atestacion = el corazon de la tesis.

## No ratifico. TASK-0134 pasa a remediacion:
- **#1 impersonacion (CRITICO):** builders server-side con forma estricta; nunca confiar en payload.actorId
  ni en intents crudos; relay-como-Arquitecto SOLO para la forma exacta del intake; **prueba negativa
  permanente** (forjar otro intent como Arquitecto -> RECHAZADO). Anomalia DECISION-0018: remediar.
- **#3 accountability:** firma = origen+transporte, NO aval; el aval es la SPEC; test relayado != autorado.
- **Cambios:** render-test (atribucion honesta), genesis/keys byte-identicos, AC15 write REAL (no mock) +
  comportamiento permanente, no sobre-afirmar PII-free (DEF-PII sigue el gate).
- **(opcional, tu decision):** auth/confirmacion en el endpoint local.

**Condicion de cierre innegociable:** TASK-0134 NO cierra sin la prueba negativa de impersonacion verde
+ el happy-path con write real verde. Nueva pasada del Analista sobre el fix de #1 antes de cerrar.

El dogfooding + la revision adversarial hicieron exactamente su trabajo: atraparon esto antes de ratificar y
antes de usar el front en serio. maker=Codex/checker=Arquitecto. Drafts para mi ratificacion. Canal ASCII.
