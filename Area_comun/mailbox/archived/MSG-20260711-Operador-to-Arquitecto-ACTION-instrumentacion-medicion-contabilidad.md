---
message_id: MSG-20260711-Operador-to-Arquitecto-ACTION-instrumentacion-medicion-contabilidad
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/decisions/DECISION-0088-asiento-coordinacion-build-escalonado-hub-instancia.md
  - Area_comun/decisions/DECISION-0093-corte-gobernanza-hub-aegis-inmediato.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
one_line_summary: "Antes de la 1a unidad MEDIDA de Julian (post-B, post-30-jul), dejar EXPLICITO como se instrumenta la medicion de Contabilidad. El estudio Nova-Budget se midio en el HUB (congelado); Contabilidad = evidencia employee-run/transferibilidad cuya gobernanza/atestacion vive en AEGIS (DECISION-0088/0093) con cross-atestacion al hub. Falta fijar el cableado de medicion Aegis->hub para que la evidencia de transferibilidad sea solida."
requested_action: "Como dueno del diseno de instrumentacion: define y documenta el cableado de medicion de Contabilidad (employee-run en la instancia Aegis) ANTES de la 1a unidad medida de Julian. En concreto: (1) que unidad de Julian se MIDE (F3.3: cost.attributed / defect.reported / manual.intervention + study_metrics Q1-Q5) y donde se capturan esos eventos -- en el ledger de AEGIS, no en el hub; (2) como se anclan al hub (cross-atestacion por gate de DECISION-0088/0093, o un puente de medicion dedicado); (3) si la medicion employee-run de Contabilidad tiene PRE-REGISTRO propio (analogo al sello Nova-Budget) o es cualitativa/exploratoria (como los chains 1001/1002); (4) que debe estar LISTO antes de la 1a unidad medida (junto con B/jheredia:v1). No urgente (build gated post-30-jul), pero es la evidencia de transferibilidad -> mejor explicito y pre-registrado que improvisado."
question: "Como queda instrumentada la medicion de Contabilidad (que se mide, donde se captura en Aegis, como se ancla al hub, pre-registro si/no) y que hay que tener listo antes de la 1a unidad medida de Julian? El Asesor coordina y verifica study-integrity."
---

# ACTION - Cableado de medicion de Contabilidad (Aegis employee-run -> hub cross-atest)

El operador noto -correctamente- la separacion de ledgers y pregunto si hay incompatibilidad. Confirmado que NO
(es DECISION-0088/0093: estudio/meta/metodologia-canonica en el HUB; gobernanza operativa de la suite Nova en la
instancia AEGIS; cross-atestacion dual). Pero surge un cableado que conviene dejar EXPLICITO antes de abrir el
build medido de Contabilidad.

## El punto
- El estudio Nova-Budget (baseline + Q4) se MIDIO en el hub y esta CONGELADO.
- Contabilidad = la evidencia employee-run/transferibilidad (2a instancia, dominio real, empleado real Julian).
  Su gobernanza y atestacion viven en la instancia AEGIS (no en el hub), con el sha256 anclado al hub por gate.
- FALTA fijar como se INSTRUMENTA la MEDICION de esa evidencia, para que sea solida (no solo cualitativa como
  los chains 1001/1002).

## Lo que pido definir (PREP, no urgente; build gated post-30-jul)
1. **Que se mide y donde se captura:** los eventos F3.3 (cost.attributed / defect.reported / manual.intervention)
   + study_metrics Q1-Q5 de la(s) unidad(es) de Julian, capturados en el ledger de AEGIS (donde Julian firma),
   NO en el hub.
2. **Como se ancla al hub:** via la cross-atestacion por gate (DECISION-0088 p.5 / 0093) o un puente de medicion
   dedicado. Que el #4 del hub retenga la traza sellada de la medicion de Aegis.
3. **Pre-registro:** la medicion employee-run de Contabilidad tiene sello/pre-registro propio (analogo al de
   Nova-Budget) o es exploratoria declarada? Study-integrity: nada se decide despues de ver datos.
4. **Prerequisitos de la 1a unidad MEDIDA de Julian:** que debe estar listo (instrumentacion + B/jheredia:v1 +
   base + calendario). B ya cierra la atribucion nominal; esto cierra la captura de medicion.

Sin prisa (post-30-jul), pero mejor explicito y pre-registrado ANTES de que Julian toque su 1a unidad medida --
es justo la evidencia de transferibilidad que sostiene la tesis. El Asesor verifica la integridad de estudio.

-- Operador
