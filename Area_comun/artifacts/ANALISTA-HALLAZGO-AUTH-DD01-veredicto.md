---
artifact_id: ANALISTA-HALLAZGO-AUTH-DD01-veredicto
from: Analista
type: review_verdict
created_at: 2026-07-05
product_repo: D:/Agentes/Zeus/NOVA/Nova-Budget
product_commit: 6cb90167cf4520e761ae1339712a706f45f1543d
protocol_head: d76b4b290461587eeb99d6e1ec65f509f9eb5f83
status: hallazgo-confirmado
---

# Veredicto Analista - Hallazgo auth endpoints DD-01

## Veredicto

CONFIRMADO. En el commit de producto `6cb90167cf4520e761ae1339712a706f45f1543d`, la API Nova-Budget no tiene wiring de autenticacion/autorizacion en `src/NOVA.Api/Program.cs`: no hay `AddAuthentication`, `AddAuthorization`, `UseAuthentication`, `UseAuthorization`, `[Authorize]` ni `RequireAuthorization`.

El alcance es transversal a los 8 endpoints presupuestales existentes, no solo a P4.1. Esto es GAP vs DD-01: DD-01 acepto para Sprint 1 el supuesto minimo de usuario autenticado con rol presupuesto y difirio la policy fina por operacion post-Sprint-1. Cero autenticacion queda por debajo de ese piso minimo; no es el diferimiento esperado.

Clasificacion: aceptable solo para dev local/sandbox controlado; bloqueante antes de exponer la API fuera de un entorno controlado.

## Ancla canonica y reproducibilidad

| Item | Valor |
|---|---|
| Protocolo HEAD revisado | `d76b4b290461587eeb99d6e1ec65f509f9eb5f83` |
| Producto revisado | `D:/Agentes/Zeus/NOVA/Nova-Budget` |
| Producto commit limpio | `6cb90167cf4520e761ae1339712a706f45f1543d` |
| Archivo fuente | `src/NOVA.Api/Program.cs` |
| Nota de canon | La instruccion ACTION recibida estaba presente en working tree pero no en `origin/main`; este veredicto deja el hallazgo formal en canonico. |

## Gates y comandos

| Gate | Resultado |
|---|---|
| `git fetch origin` + `git status --short` | HEAD local = `origin/main` (`d76b4b2`); existen cambios/untracked ajenos no tocados. |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| Lectura `Area_comun/state/*.json` con `utf-8-sig` | exit 0 |
| Clon limpio producto + checkout `6cb90167cf4520e761ae1339712a706f45f1543d` | exit 0 |
| `npm test --prefix <clon-producto>` | exit 1: no existe `package.json` en raiz del producto. |
| `npm install --prefix <clon-producto>/apps/nova-web` | exit 0 |
| `npm test --prefix <clon-producto>/apps/nova-web` | exit 0: 1 test passed. |
| `python scripts/validate_collaboration_state.py` vivo con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clon-secretless>` | exit 0 |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| drift vivo | exit 0; `has_drift=false`, `up_to_seq=4046` |
| `protocol.config.json` byte-identico contra HEAD | true; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Prueba por comportamiento

Busqueda estatica sobre `Program.cs` en clon limpio:

| Vector / garantia | Evidencia | Veredicto |
|---|---|---|
| Servicio de autenticacion registrado | `AddAuthentication=false` | SLIPS |
| Servicio de autorizacion registrado | `AddAuthorization=false` | SLIPS |
| Middleware de autenticacion en pipeline | `UseAuthentication=false` | SLIPS |
| Middleware de autorizacion en pipeline | `UseAuthorization=false` | SLIPS |
| Metadata de autorizacion por endpoint | `[Authorize]=false`, `RequireAuthorization=false` | SLIPS |
| Endpoint `/api/budget/parameters/accounts` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/parameters/funding-sources` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/parameters/account-funding-sources` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/parameters/investment-projects` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/parameters/document-series` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/execution-report` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/appropriation-modifications/validate` | sin metadata auth | SLIPS |
| Endpoint `/api/budget/appropriation-modifications/` | sin metadata auth | SLIPS |

La familia prometida queda cubierta completa: 5 endpoints de parametros + 1 reporte de ejecucion + 2 endpoints de modificacion de apropiacion = 8 endpoints presupuestales sin auth.

## Residuales

- No probe trafico HTTP en servidor vivo porque la garantia se refuta por ausencia total de wiring y metadata en el unico `Program.cs` que registra rutas.
- El `npm test` obligatorio en raiz no es reproducible por falta de `package.json`; el gate web bajo `apps/nova-web` si pasa tras instalar dependencias.
- La instruccion ACTION no estaba canonica antes de este commit; el hallazgo queda canonizado por este artefacto y el MSG asociado.

## Recomendacion

CERRABLE como registro de hallazgo formal separado. No debe bloquear el cierre de TASK-0253 por ser cross-cutting a los 8 endpoints, pero debe quedar como item security+QA obligatorio antes de exposicion fuera de entorno controlado.

task_id: HALLAZGO-AUTH-DD01
status: CERRABLE
executive_summary: CONFIRMADO cero auth/authz en los 8 endpoints presupuestales de Nova-Budget; GAP vs DD-01, no diferimiento esperado.
artifacts: Area_comun/artifacts/ANALISTA-HALLAZGO-AUTH-DD01-veredicto.md; Area_comun/mailbox/open/MSG-20260705-Analista-to-Arquitecto-REVIEW-hallazgo-auth-endpoints-DD01.md
gates: validate vivo exit 0; validate secretless exit 0; domain exit 0; encoding exit 0; drift 0 up_to_seq=4046; product root npm test exit 1 por package.json ausente; apps/nova-web npm test exit 0.
next_recommended: Registrar item security+QA separado y exigir autenticacion minima antes de exponer la API fuera de sandbox/local.
risks: API expuesta sin control de identidad ni rol; aceptable solo en dev local/sandbox controlado.
