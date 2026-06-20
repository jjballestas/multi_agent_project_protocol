---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-fix-neutralidad-TASK-0138
task_id: TASK-0138
type: DECISION
from: Operador
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
one_line_summary: "NO cerrar TASK-0138 todavia. El Analista valido DECISION-0053: BOUNDING anti-impersonacion PASA (no se reabre la impersonacion), pero CAMBIO REQUERIDO en NEUTRALIDAD -- el core runtime/submit_intent.py (L337-338, verificado en canonico) HARDCODEA author:Operador/relayed_by:Arquitecto = identidades de instancia en el core generico, regresion SILENCIOSA (scan no la atrapa), viola regla 1. Fix: atribucion CALLER-DERIVED (grep de los literales = 0); acotar regex message_id; y extender el scan para atrapar literales de agente (regresion-proof). Nueva pasada del Analista (grep=0) antes de cerrar."
requested_action: "TASK-0138 sigue en in_review; NO cerrar hasta resolver el CAMBIO del Analista (artefacto: Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md). (1) NEUTRALIDAD (bloqueante): el core `runtime/submit_intent.py` L337-338 hardcodea `author:'Operador'` y `relayed_by:'Arquitecto'` -- identidades de ESTA instancia en el runtime generico (el resto del core usa ROLES). Fix: atribucion CALLER-PROVIDED (el front/Zeus provee author/relayed_by; el core no lleva literales de agente), consistente con como el intake ya lo hace. Falsable: `grep '\"Operador\"|\"Arquitecto\"' runtime/submit_intent.py` debe dar 0 tras el fix (hoy 2). Esto tambien cierra el #5 (un archive directo no-via-front no queda mis-atribuido). (2) Acotar la regex del message_id a [A-Za-z0-9._-] (hoy admite ':' = NTFS ADS en Windows). (3) RECOMENDADO (regresion-proof): extender scan_domain_neutrality para atrapar literales de identidad de agente en el core (asi esta clase de regresion deja de ser silenciosa, filosofia AC11/AC22); si es mucho para esta task, declaralo follow-up explicito. (4) FOLLOW-UP aparte: leaks analogos preexistentes (apply.py owner default 'Codex', context.py implementer->Codex). MANTENER verde lo que ya paso: bounding AC25, AC24 idempotente/honesto, hard-gate EXACTAMENTE {requirement-intake, mailbox-archive}, #4 byte-identica, validate con/sin secretos exit 0, drift 0, un archive deja el canonico verde, npm test. CONDICION DE CIERRE: grep de literales = 0 + NUEVA pasada del Analista confirmando neutralidad + bounding intacto. maker=Codex/checker=Arquitecto, reproduccion desde clon limpio. Reporta drafts/cierre en canonico."
question: "Reabres TASK-0138 (sigue in_review) para hacer la atribucion caller-derived (grep=0) + acotar regex + extender el scan de neutralidad, con nueva pasada del Analista antes de cerrar? El bounding ya paso; esto es solo neutralidad del core."
context_refs:
  - Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md
  - Area_comun/mailbox/open/MSG-20260620-Analista-to-Operador-DECISION-0053-veredicto.md
  - Area_comun/decisions/DECISION-0053-mailbox-archive-relay.md
  - runtime/submit_intent.py
deadline_or_blocking_level: blocking
---

# GO - TASK-0138 no cierra: fix de NEUTRALIDAD del core (Analista)

El Analista valido DECISION-0053 como pediste. Resultado: el **bounding anti-impersonacion PASA** (no pude
reabrir la impersonacion extendiendo el relay a una 2a accion -- doble capa, builder server-side, pruebas
negativas permanentes). Pero hay un **CAMBIO REQUERIDO en neutralidad** que verifique en canonico:

`runtime/submit_intent.py` L337-338 hardcodea `author:"Operador"` / `relayed_by:"Arquitecto"` -- identidades
de esta instancia en el **core generico**. `scan_domain_neutrality` no lo atrapa (solo busca dominio) ->
regresion SILENCIOSA, viola la regla 1.

## No cerrar hasta:
- **Atribucion CALLER-DERIVED:** el caller (front/Zeus) provee author/relayed_by; el core sin literales de
  agente. Falsable: `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` = 0 (hoy 2). Cierra tambien el
  #5 (archive directo no-via-front no se mis-atribuye).
- **Regex del message_id** acotada a [A-Za-z0-9._-] (sin ':' NTFS ADS).
- **(recomendado) extender scan_domain_neutrality** para atrapar literales de agente en el core -> regresion-
  proof; si no entra en esta task, follow-up explicito.
- **Follow-up aparte:** leaks analogos (apply.py "Codex", context.py).
- Mantener verde: bounding AC25, AC24, hard-gate exactamente {requirement-intake, mailbox-archive}, #4
  byte-identica, validate con/sin secretos exit 0, canonico verde.

**Cierre:** grep=0 + nueva pasada del Analista (neutralidad + bounding intacto). maker=Codex/checker=Arquitecto.
Verifico en canonico. Canal ASCII.
