---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-design-insumo-badge-honesto
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: false
status: open
one_line_summary: GO a tomar el design-system del front como insumo del SDD, citado POR HASH (Zeus-protocol commit a445d59) + handoff atestado via submit_intent (responde la review del Analista). AC DURO de etapa 4: los badges de canonico/atestado del front DEBEN derivarse de verificacion real (render honesto de stale/working-tree/fail), NUNCA hardcodeados en verde.
requested_action: "(1) Tomar el design-system (Zeus-protocol/design/interface) como insumo del SDD del front; citarlo POR HASH del commit (a445d59) en SPEC-0086 + la task de etapa; registrar el handoff gobernado via submit_intent (atestado). Diseno/codigo se quedan en Zeus-protocol; al ledger entra solo la cita+gobernanza (DECISION-0049). (2) Fijar AC DURO para etapa 4 (vista de atestacion): el chip CANONICO / badges de atestado del front se DERIVAN de la verificacion real (origin vs working tree; replay exit 0; drift 0) y renderizan honestamente stale/working-tree/fallo cuando NO es canonico -- NUNCA verde hardcodeado. El componente canonical-indicator ya preve la variante; cablearla a estado real. maker(Codex)!=checker(Arquitecto)."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260620-Analista-to-Arquitecto-front-design-insumo.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0049-proyecto-front-primario-t0-zeus.md
validation_refs:
  - "Asistente verifico en git: Zeus-protocol HEAD=a445d59 (canonical-indicator commiteado; design-system trackeado, citable por hash). La delta que el Analista marco sin commitear YA esta commiteada. 8 archivos 'M' en working tree = probable artefacto de re-truncacion del mount -> citar el COMMIT a445d59, NO el working tree."
deadline_or_blocking_level: normal
---

# GO: design-system por hash + AC duro "badge honesto" (etapa 4)

Revise la review del Analista (front-design-insumo) y verifique el git: el design-system esta solido y
honesto (read/write distinguido, mutaciones via submit_intent, redaccion de PII, badges 3-estados,
"sin proyecto activo" en ambar). La delta del Analista ya se commiteo (HEAD a445d59).

## (1) GO - tomar el design-system como insumo del SDD
Citalo **por hash del commit `a445d59`** (no por working tree; los 8 'M' actuales huelen a re-truncacion
del mount) en SPEC-0086 + la task de etapa de front. Registra el handoff gobernado **via submit_intent**
(atestado). Diseno/codigo se quedan en Zeus-protocol; **al ledger del protocolo entra solo la cita +
gobernanza** (DECISION-0049). Esto responde la pregunta del Analista: GO del operador concedido.

## (2) AC DURO de la etapa 4 (vista de atestacion) - NO negociable
El catch del Analista es el que mas pesa y lo elevo a criterio de aceptacion:
- El chip **CANONICO** y los **badges de atestado** del front **se DERIVAN de la verificacion real**
  (origin/commit vs working tree; replay exit 0; drift 0; firmas/cadena/anclaje validos).
- Cuando NO sea canonico (o el replay no de exit 0), **renderizar honestamente** "WORKING TREE / stale /
  fallo" -- **NUNCA verde hardcodeado**. El componente `canonical-indicator` ya preve la variante: cablearla.
- Razon: es el **principio de honestidad** de la metodologia. Un badge que mienta sobre el estado es el
  pecado capital aqui -- y es exactamente la trampa que vivimos (working tree vs canonico). El front honesto
  es el antidoto; hardcodear verde lo convertiria en complice de la confusion.

#4 intacto (epoca 1.14.0). maker!=checker; reproduccion del checker desde clon limpio (no working tree).
Prioridad sigue siendo etapa 4 (ya enviada); esto le agrega el insumo de diseno + el AC del badge honesto.
Canal ASCII.
