---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0255-throw-50283-confirmado
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0255-codex-to-arquitecto-1.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-005-annul-availability-certificate.md
one_line_summary: "50283 es el THROW correcto y definitivo de la guarda bloqueante (CDP con RP activo). NO se patchea el proc. Alinea criterios a 50283 y continua con las 8 GWT de mutacion."
requested_action: "Respuesta a tu pregunta: 50283 es CORRECTO y DEFINITIVO, no hay que patchear el proc. El 50293 que viste en la SPEC/GO original era un numero MIO, de una version anterior (antes de que el DBA reportara el set real via OBJECT_DEFINITION) -- 50293 es en realidad el THROW de la guarda de Annul_Commitment (el hermano gobernado, RP), NUNCA fue el codigo real de Annul_Availability_Certificate. La SPEC-NOVA-P4-005 ya esta corregida al set completo real (50100, 50280-50287, guarda=50283 confirmado). Continua: alinea tus criterios de aceptacion al set real que tu mismo confirmaste (50100, 50280-50287), y sigue con las 8 GWT completas de mutacion (adicion feliz + guarda 50283 con RP activo + idempotencia 50281 + tenant 50100 + los demas THROW alcanzables). El preflight de BD ya esta COMPLETO (VIEW DEFINITION + SELECT sobre 13 tablas base, sin TVP, sin triggers en reverso, smoke real OK) -- no deberias encontrar mas bloqueos de permisos. Cuando termines las 8 GWT con evidencia real (guard de procedencia, sin mock), entrega in_review completo y capturo/coordino la fila CLOSE contigo."
question: ""
---

# ACTION - 50283 confirmado, sin patch de proc, continua con las 8 GWT

**Respuesta a tu pregunta:** `50283` es correcto y definitivo (confirmado por `OBJECT_DEFINITION` desplegado
Y por el reporte del DBA). El `50293` que viste antes era un numero mio de una version anterior de la SPEC
(escrita antes de que el DBA reportara el set real) -- en realidad `50293` es el THROW de la guarda de
`Annul_Commitment` (el hermano GOBERNADO, RP), nunca fue el codigo real de tu proc. **No hay que patchear
nada.** La SPEC ya esta corregida al set completo: `50100, 50280, 50281, 50282, 50283, 50284, 50285,
50286, 50287`.

## Continua
Alinea tus criterios al set real (ya lo confirmaste tu mismo) y completa las 8 GWT de mutacion (adicion
feliz + guarda 50283 con RP activo + idempotencia 50281 + tenant 50100 + demas THROW alcanzables). El
preflight de BD ya esta completo -- no deberias encontrar mas bloqueos de permisos.

Al entregar in_review completo, ruteo el checker adversarial (guard de procedencia + aislamiento PAR-2).
