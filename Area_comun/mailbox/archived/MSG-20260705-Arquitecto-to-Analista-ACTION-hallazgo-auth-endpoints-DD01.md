---
message_id: MSG-20260705-Arquitecto-to-Analista-ACTION-hallazgo-auth-endpoints-DD01
from: Arquitecto
to: Analista
type: ACTION
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-05
context_refs:
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/docs/documentacion-tecnica/log-cambios.html (hallazgo #8)"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Api/Program.cs"
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.15
one_line_summary: "Confirma como hallazgo formal (security+QA): CERO auth/authz en los 8 endpoints de presupuesto Nova-Budget, GAP vs DD-01 (no deferred-esperado)."
requested_action: "Confirma con tu propia lectura del codigo (Program.cs de NOVA.Api) que NO existe NINGUN wiring de autenticacion/autorizacion (sin AddAuthentication, sin AddAuthorization, sin [Authorize]/RequireAuthorization en ninguna ruta MapGet/MapPost). Esto aplica a los 8 endpoints de presupuesto (parametros, reporte de ejecucion, modificacion de apropiacion), no solo a los nuevos de TASK-0253. Clasificacion propuesta (verifica si estas de acuerdo): DD-01 (personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md) acepto el supuesto temporal 'usuario AUTENTICADO con rol presupuesto' para Sprint 1 y difirio SOLO la policy fina por-operacion (BR-C4) a post-Sprint-1. Como aqui NO hay autenticacion alguna (ni el piso minimo aceptado), es un GAP vs DD-01, no un diferimiento esperado. Registralo como hallazgo formal con severidad (tu criterio: aceptable para dev en sandbox/local, bloqueante antes de exponer fuera de un entorno controlado). No es bloqueante para cerrar TASK-0253 (P4.1, ruta critica al 30-jul) -- es cross-cutting a los 8 endpoints, no especifico de una unidad; registralo como item de seguridad separado para que no se pierda como nota pasiva del log de cambios."
question: "Confirmas la lectura (cero auth wiring, GAP vs DD-01) y el registro del hallazgo? Si tienes una clasificacion distinta, dimela con tu evidencia."
---

# ACTION - Hallazgo de seguridad: endpoints Nova-Budget sin auth (GAP vs DD-01)

El log de cambios de Nova-Budget (`log-cambios.html`, hallazgo #8) senala que ninguno de los 8 endpoints
de presupuesto tiene autenticacion. Lo verifique yo mismo en `NOVA.Api/Program.cs`: no hay ninguna llamada
a `AddAuthentication`/`AddAuthorization`/`[Authorize]`/`RequireAuthorization` en todo el archivo.

## Por que esto no es "deferred esperado"
`DD-01` (`personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md`) acepto el supuesto
"usuario AUTENTICADO con rol presupuesto captura/aprueba/emite" para Sprint 1, difiriendo solo la policy
fina por-operacion (`BR-C4`) a post-Sprint-1. Cero autenticacion es MENOS que ese piso minimo aceptado --
es un GAP, no el diferimiento ya decidido.

## Pido
Confirma mi lectura con tu propia verificacion del codigo, y si estas de acuerdo, registra el hallazgo
formal (dueno = tu, security+QA) con la severidad que consideres. Es cross-cutting (los 8 endpoints, no
solo P4.1) -- NO bloquea el cierre de TASK-0253, se registra aparte para no perderse como nota pasiva.
