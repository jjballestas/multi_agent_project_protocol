---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-promueve-hallazgos-5-1-seguridad-DD01
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/NOVA_SPEC_Plantilla_Requisitos.md (rubric 12 puntos, punto 7 Estados y permisos)"
  - personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md (DD-01 supuesto temporal de autorizacion)
one_line_summary: "El log de cambios registro 9 hallazgos como 'Informacion pendiente'. DIRECTIVA: promueve #5 (endpoints nuevos SIN auth/authz -- marcado como RIESGO DE SEGURIDAD) y #1 (ReadOnlySqlOptions ahora escribe, nombre enganoso) de nota pasiva a HALLAZGO GOBERNADO CON DUENO. #5 dueno = Analista (security+QA). VERIFICA #5 contra DD-01: DD-01 acepto el supuesto temporal (usuario autenticado con rol presupuesto) para Sprint 1 y difirio BR-C4 (policy por operacion) a post-Sprint-1 -> determina si #5 es 'sin auth alguna' (GAP vs DD-01, hay que arreglar el minimo autenticado+rol) o 'autenticado+rol presente, policy por-operacion diferida' (esperado, documentar deferred-con-fecha). ADEMAS: el adversarial de 12 puntos cubre autorizacion de DOMINIO (punto 7 Estados y permisos) pero NO explicita la seguridad de capa API/endpoint (autenticacion + scope JWT budget:*) -> confirma/clarifica que el punto 7 (o un checkpoint nuevo) OBLIGUE a verificar auth de endpoint, para que no sea punto ciego del gate. Study-integrity: dejar un riesgo de seguridad como 'pendiente' pasivo ES la fuga de observaciones que mide Q2 (emitidas vs registradas-con-dueno)."
requested_action: "[DIRECTIVA] El log de cambios registro 9 hallazgos como 'Informacion pendiente' (bien: es la conducta que Q2 mide). PERO 2 de ellos NO pueden quedar como nota pasiva -- promuevelos a HALLAZGO GOBERNADO CON DUENO: (1) #5 ENDPOINTS NUEVOS SIN AUTH/AUTHZ (marcado como RIESGO DE SEGURIDAD, no solo observacion): dueno = Analista (security+QA checker). En Nova = API que muta presupuesto publico -> jamas a produccion sin auth. VERIFICALO CONTRA DD-01 antes de clasificar: DD-01 (DECISIONES-DOMINIO-PENDIENTES-nova.md) ACEPTO el supuesto temporal 'usuario autenticado con rol presupuesto captura/aprueba/emite' para Sprint 1, y CONFIRMO BR-C4 (policy por operacion) para post-Sprint-1. Entonces: si los endpoints no tienen NINGUNA auth (ni autenticado+rol) -> es un GAP vs DD-01 (falta el minimo aceptado), hay que arreglarlo o registrarlo como deferred-con-fecha explicito; si tienen autenticado+rol pero les falta solo la policy fina por-operacion (BR-C4) -> es el diferimiento ESPERADO, documentar como deferred-con-fecha, no como 'sin auth' a secas. (2) #1 ReadOnlySqlOptions AHORA ESCRIBE (nombre enganoso): dueno = maker (Codex) para renombrar + confirmar que no rompe la garantia readonly (toca la frontera readonly del estudio: readonly_s9=existencia vs verifier=paridad; un 'ReadOnly' que escribe es footgun). (3) RUBRIC DEL ADVERSARIAL: el operador pregunta si el adversarial de 12 puntos incluye seguridad. HALLAZGO: el punto 7 'Estados y permisos' (NOVA_SPEC_Plantilla_Requisitos.md) cubre autorizacion de DOMINIO (aprobar sin permiso / estado invalido), pero NO explicita la seguridad de capa API/ENDPOINT (que el endpoint exija usuario autenticado + scope JWT budget:read/write/approve). CONFIRMA/CLARIFICA que el punto 7 (o un checkpoint explicito) OBLIGUE a verificar auth de endpoint, para que la auth de API no sea punto ciego del gate informal. Es refinamiento de rubric (tu lo gobiernas); si cambias el rubric derivado, registralo. STUDY-INTEGRITY: un riesgo de seguridad dejado como 'pendiente' pasivo ES la fuga que mide Q2 (observaciones_emitidas_n vs observaciones_registradas_con_dueno_n) -> promoverlo con dueno es la conducta correcta y ademas dato limpio para Q2. Los otros 4 listados (carpeta huerfana ExecutionReports, carpetas vacias sin rastrear, salto RN-07/08/09 sin explicar, README desactualizado) SI pueden vivir como deuda registrada/higiene. Faltan 3 hallazgos de los 9 no detallados -> triarlos igual. RESPONDE con: (a) #5 promovido con dueno Analista + su clasificacion vs DD-01 (gap o deferred-con-fecha); (b) #1 promovido con dueno; (c) el punto 7 del rubric cubre o no la auth de endpoint, y si lo clarificaste; (d) cuales son los otros 3 hallazgos."
question: ""
---

# DIRECTIVA - Promueve #5 (seguridad) y #1 a hallazgos con dueno + verifica #5 vs DD-01

El log registro 9 hallazgos como "Informacion pendiente" (bien -- es lo que mide Q2). Pero **2 no pueden
quedar como nota pasiva**:

## (1) #5 -- Endpoints sin auth/authz (RIESGO DE SEGURIDAD)
- **Promueve a hallazgo gobernado, dueno = Analista** (security+QA). API que muta presupuesto publico -> nunca a prod sin auth.
- **Verifica contra DD-01 ANTES de clasificar:** DD-01 acepto el supuesto temporal *usuario autenticado con rol presupuesto* (Sprint 1) y difirio BR-C4 (policy por operacion) a post-Sprint-1.
  - Sin auth alguna (ni autenticado+rol) -> **GAP vs DD-01** (falta el minimo) -> arreglar o deferred-con-fecha explicito.
  - Autenticado+rol OK pero falta policy fina por-operacion -> **diferimiento esperado** -> documentar deferred-con-fecha, no "sin auth".

## (2) #1 -- ReadOnlySqlOptions ahora escribe (nombre enganoso)
- **Promueve a hallazgo, dueno = maker (Codex):** renombrar + confirmar que no rompe la garantia readonly (frontera del estudio; un "ReadOnly" que escribe es footgun).

## (3) Rubric del adversarial (la duda del operador)
- El **punto 7 "Estados y permisos"** cubre autorizacion de **DOMINIO** (aprobar sin permiso / estado invalido), pero **NO explicita** la seguridad de **capa API/endpoint** (autenticado + scope JWT `budget:*`).
- **Confirma/clarifica** que el punto 7 (o un checkpoint explicito) OBLIGUE a verificar auth de endpoint -> que la auth de API no sea punto ciego. Registralo si cambias el rubric derivado.

## Study-integrity
Un riesgo de seguridad como "pendiente" pasivo **es** la fuga que mide Q2 (emitidas vs registradas-con-dueno). Promoverlo con dueno = conducta correcta + dato limpio. Los otros 4 (ExecutionReports huerfana, carpetas vacias, salto RN-07/08/09, README) pueden vivir como higiene. Faltan 3 de los 9 -> trialos.

## Responde
(a) #5 con dueno Analista + clasificacion vs DD-01; (b) #1 con dueno; (c) el punto 7 cubre auth de endpoint?; (d) los otros 3 hallazgos.
