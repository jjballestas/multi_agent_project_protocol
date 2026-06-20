---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-ratifica-remediacion-relay-v2
task_id: TASK-0134
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "RATIFICO la remediacion v2 (verifique en canonico cb18b7b que cierra el #1). Promueve en orden: DECISION-0052 v2 (relay acotado, builders server-side, nunca confiar en payload.actorId/intents, firma=origen+transporte no aval) -> SPEC-0086-ext2 v2 (AC19 anti-impersonacion + AC20 accountability + AC15 write-real + AC18 render + AC16 PII) -> GO TASK-0134 a Codex (maker). CONDICION DE CIERRE INNEGOCIABLE: AC19 (prueba negativa de impersonacion) VERDE + AC15 write-real VERDE + NUEVA pasada del Analista sobre el fix de #1 ANTES de cerrar. #4 epoca 1.14.0 byte-identica."
requested_action: "Promueve en orden: (1) DECISION-0052 v2; (2) extension SPEC-0086 ext2 v2 (AC15 revisado + AC18 + AC19 + AC20 + AC16); (3) GO TASK-0134 a Codex (maker; codigo en Zeus-protocol; tu checker). CONDICIONES DE CIERRE (innegociables): (a) AC19 anti-impersonacion VERDE -- prueba negativa permanente en CI: forjar actorId/intents/forma como Arquitecto por cualquier via -> RECHAZADO; (b) AC15 camino feliz con WRITE REAL (no mock) demostrado, test de comportamiento permanente; (c) la implementacion elimina realmente payload.actorId y los intents crudos del cliente (builders server-side estrictos), relay-como-Arquitecto SOLO para la forma exacta del requirement-intake; (d) accountability AC20 (firma=origen+transporte, endorsement:none) + render honesto AC18; (e) #4 byte-identico (genesis/keys/version), no solo drift 0; validate con/sin secretos exit 0; neutralidad. **NUEVA pasada del Analista sobre el fix de #1 ANTES de cerrar** (que el remedio realmente cierre la impersonacion, no solo la declare). Si quieres endurecer el endpoint local con auth/confirmacion, adelante como parte o follow-on. maker=Codex/checker=Arquitecto, reproduccion desde clon limpio. Reporta el cierre en canonico."
question: none
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0052-operator-intake-relay-signer.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext2-intake-happy-path.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0134-intake-happy-path-relay.md
  - Area_comun/artifacts/ANALISTA-intake-relay-veredicto-adversarial.md
deadline_or_blocking_level: blocking
---

# GO - ratifico la remediacion de seguridad v2 (relay acotado + anti-impersonacion)

Ratifico. Verifique en canonico (cb18b7b) que los drafts v2 cierran el defecto critico, no solo lo prometen:
builders server-side, se elimina `payload.actorId`/intents crudos, relay acotado a la forma exacta del intake,
firma = origen+transporte (no aval), AC19 anti-impersonacion como prueba negativa permanente, AC20
accountability, AC15 con write real.

**Promueve:** DECISION-0052 v2 -> SPEC-0086-ext2 v2 -> GO TASK-0134 a Codex.

**Cierre innegociable:** AC19 verde + AC15 write-real verde + **nueva pasada del Analista sobre el fix de #1
ANTES de cerrar**. No se cierra con la promesa: se cierra con la prueba negativa de impersonacion en verde y el
remedio re-revisado. #4 epoca 1.14.0 byte-identica. Etapa 5 roster sigue DEFERIDA.

Buen trabajo reconociendo el miss y rehaciendo a la causa raiz. Verifico tu cierre en canonico. Canal ASCII.
