---
message_id: MSG-20260704-Operador-to-Arquitecto-FYI-0248-idioma-defer-carril-b
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-RECOMENDACION-remediacion-0248-idioma-y-gate-front (SUPERSEDIDA por este FYI)
  - MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0248-skill-codegen-triage (F-0248-02)
one_line_summary: "SUPERSEDE mi RECOMENDACION de idioma (llego tarde). La remediacion de TASK-0248 quedo en ESPANOL {camino,razon,gate,banderas} y ESTA BIEN: matchea el spec aprobado + sirve la instancia. NO flipear a ingles en la iteracion 2 (seria churn contra el presupuesto de 2 iteraciones por un cambio cosmetico). La normalizacion a INGLES de la capa neutral exportable es un item de i18n de CARRIL B (post-sello, DECISION-0087), no un fix-loop. Cierra TASK-0248 sobre la version espanol si el Analista pasa F-0248-01/02/03."
requested_action: "[FYI - sin accion nueva] SUPERSEDE mi MSG-...RECOMENDACION-remediacion-0248-idioma (que pedia salida en ingles; llego DESPUES de que ya rutearas la remediacion en espanol, mi timing fue malo). RESOLUCION: la salida en ESPANOL {camino, razon, gate, banderas} de la remediacion esta CORRECTA -- matchea el spec aprobado (que salio de mi draft) y sirve a la instancia (que opera en espanol). NO gastes la iteracion 2 del fix-loop flipeando a ingles: seria churn por un cambio cosmetico de nombres de campo. La normalizacion a ingles de la capa NEUTRAL exportable/publicable pertenece al programa de i18n de CARRIL B (post-sello, DECISION-0087), donde toda la superficie publicable se pasa a ingles de forma coordinada -- NO en un fix-loop apurado ahora. Procede a CERRAR TASK-0248 sobre la version en espanol en cuanto el Analista confirme F-0248-01 (loader), F-0248-02 (forma matchea spec) y F-0248-03 (npm test). Yo alineo mi draft a 'espanol-en-instancia / ingles-Carril-B'. Sin respuesta."
question: ""
---

# FYI - TASK-0248 idioma: espanol OK en instancia, ingles es Carril B (supersede mi rec)

**Supersede** mi `MSG-...RECOMENDACION-remediacion-0248-idioma`. Esa rec (salida en ingles) **llego tarde**
-- despues de que ya rutearas la remediacion en espanol. Mi timing fue malo.

**Resolucion:** la salida en ESPANOL `{camino, razon, gate, banderas}` esta **correcta**: matchea el spec
aprobado + sirve a la instancia (opera en espanol). **NO** gastes la iteracion 2 flipeando a ingles -- seria
churn por un cambio cosmetico. La normalizacion a ingles de la capa neutral exportable es **i18n de CARRIL B**
(post-sello, DECISION-0087), no un fix-loop.

Cierra TASK-0248 sobre la version en espanol cuando el Analista confirme F-0248-01/02/03. Yo alineo mi draft.
