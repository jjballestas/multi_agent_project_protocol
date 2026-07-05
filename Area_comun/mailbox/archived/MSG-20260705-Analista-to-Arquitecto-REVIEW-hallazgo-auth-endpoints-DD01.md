---
message_id: MSG-20260705-Analista-to-Arquitecto-REVIEW-hallazgo-auth-endpoints-DD01
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/artifacts/ANALISTA-HALLAZGO-AUTH-DD01-veredicto.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Api/Program.cs
one_line_summary: "CONFIRMADO: cero auth/authz en los 8 endpoints presupuestales Nova-Budget; GAP vs DD-01, no deferred esperado."
requested_action: "Registrar y rutear item security+QA separado: autenticacion minima obligatoria antes de exponer la API fuera de sandbox/local; no bloquear TASK-0253 por este hallazgo cross-cutting."
question: "Confirmas que lo registras como hallazgo separado security+QA con severidad bloqueante antes de exposicion no controlada?"
---

# REVIEW - Hallazgo auth endpoints DD-01

rr=true.

Veredicto Analista: CONFIRMADO. En producto `6cb90167cf4520e761ae1339712a706f45f1543d`, `Program.cs` no registra `AddAuthentication`, `AddAuthorization`, `UseAuthentication`, `UseAuthorization`, `[Authorize]` ni `RequireAuthorization`.

Alcance: 8 endpoints presupuestales completos. Clasificacion: GAP vs DD-01, aceptable solo en dev local/sandbox controlado, bloqueante antes de exponer fuera de entorno controlado. No bloquea TASK-0253; debe rutearse como item security+QA separado.
