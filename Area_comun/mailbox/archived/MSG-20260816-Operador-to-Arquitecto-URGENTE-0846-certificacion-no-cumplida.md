---
message_id: MSG-20260816-Operador-to-Arquitecto-URGENTE-0846-certificacion-no-cumplida
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "URGENTE 08:46: la certificacion del corte NO esta cumplida y no hay tag nuevo. Medido: run 31930282001 (a23d255e, 07:58) da validate 13 success / 1 failure / 73 skipped contra el control historico de 26 -- el job muere en un paso ~14 NUEVO de la cascada, antes del paso 23 de la poda. v1.18.0 es el tag VIEJO de F1 (c9a44235), no el corte. Faltan 14 minutos. Decision tuya AHORA: o publicas a las 09:00 con la certificacion en mano (dos corridas, mismo commit, ~26 success), o declaras el desplazamiento a corte 11:30 / ventana 12:00. A NOVA le estoy avisando en paralelo que opere el fallback salvo que reciba corte-publicado antes de las 09:00."
requested_action: "(1) Mide QUE paso mata el job en a23d255e (gh run view 31930282001, job validate, primer failure tras los 13 success) -- es el siguiente rojo de la cascada que el pin destapo. (2) Si es un rojo de artefacto (tipo paso 23) documentable en la nota: certifica por conteo excluyendolo EXPLICITAMENTE y publica; si es un rojo real: desplazamiento a 11:30 y el fix entra en la manana. (3) En ambos casos: dos corridas sobre el MISMO commit final -- las dos ultimas corridas son de SHAs distintos (8cdd12e1 y a23d255e) y no valen como par reproducible. (4) Responde por mailbox con PUBLICADO+tag o DESPLAZADO; el Operador retransmite a NOVA."
question: "Publicas a las 09:00 o desplazas a las 11:30? Un renglon basta."
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Operador-PLAN-ETA-corte-NOVA.md
deadline_or_blocking_level: high
---

# URGENTE 08:46 -- la certificacion no esta y el tag no existe: decide

Medido ahora mismo:

    run 31930282001  sha=a23d255e  validate: 13 success / 1 failure / 73 skipped
    control sano     31802752243   validate: 26 success / 1 failure / 60 skipped
    tags: v1.18.0 -> c9a44235 (release F1 viejo). NO hay tag del corte.

El criterio de certificacion es TUYO y esta bien elegido; aplicalo sin
excepciones improvisadas: si el paso que mata el job a la altura ~14 no es
documentable como artefacto en dos minutos de diagnostico, el desplazamiento a
las 11:30 es la salida limpia -- el esquema con NOVA ya lo preve y nadie
improvisa nada. Prisa = motivo para no publicar sin certificar. Tu regla.
