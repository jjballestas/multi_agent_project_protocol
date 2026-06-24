# ANALISTA - TASK-0166 runtime-control fix verdict

Firma: Analista
Fecha: 2026-06-24

## Veredicto

CAMBIO-REQUERIDO. Los 2 defectos reportados antes quedan parcialmente cerrados en `cab246cc48facb8b8dc6af52ca5a80ac4eddf766`, pero hay un escape nuevo falsable en AC2: `agentId` no string con array JSON de un solo elemento (`["Codex"]`) se coerciona con `String(value || "")` a `Codex`, pasa `sanitizeRuntimeControlAgentId`, matchea la allowlist y activa el runtime.

Esto rompe la garantia "agentId exacto server-side / no-exacto -> 400" de la instruccion de review. Recomendacion de cierre: CAMBIO-REQUERIDO, no cerrable.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Producto | `D:/Agentes/Zeus/Zeus-protocol` |
| Commit producto revisado | `cab246cc48facb8b8dc6af52ca5a80ac4eddf766` |
| Commit protocolo citado por la instruccion | `a2ed687` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0166-fix.md` |
| Tarea | `Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md` |
| Spec | `Area_comun/specs/SPEC-0089-panel-operar-agentes-q1-control-runtime.md` |

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout cab246c` | exit 0, HEAD `cab246cc48facb8b8dc6af52ca5a80ac4eddf766` |
| `npm test` en clon limpio producto | exit 0, 64/64 pass |
| Payload propio contra server temporal + protocolo clonado en `a2ed687` | exit 0 del script de prueba, slip reproducido |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clone-sin-secretos-a2ed687>` | exit 0 |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| Drift #4 vivo | `has_drift=false`, `up_to_seq=1591` |
| `protocol.config.json` vivo | byte-identico durante la pasada, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Matriz adversarial

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| AC1 heartbeat futuro +10 anos | PASA | `GET /api/protocol/agent-runtime` devuelve `Codex.status=dormant`. |
| AC1 heartbeat futuro dentro de tolerancia 0.5s | RIESGO DECLARADO no bloqueante | Devuelve `alive`. Lo trato como tolerancia explicita del fix (`>1000ms` falla cerrado), no como bypass nuevo. |
| AC1 heartbeat stale 10 min | PASA | Devuelve `dormant`. |
| AC2 `agentId="Codex"` exacto | PASA control positivo | `POST activate` devuelve 200, crea heartbeat, `status=alive`. |
| AC2 leading/trailing space | PASA | `" Codex"` y `"Codex "` devuelven 400, no crean heartbeat, `status=dormant`. |
| AC2 control chars | PASA | `Codex\\t`, `Codex\\u0000`, `Codex\\u007f`, `Codex\\n` devuelven 400, no crean heartbeat. |
| AC2 case/non-ASCII/ZWJ/internal-space | PASA | `codex`, `Code-x` con e aguda, `Codex\\u200d`, `Co dex` devuelven 400, no crean heartbeat. |
| AC2 no-string array single | SLIPS | JSON `{ "agentId": ["Codex"], "action": "activate" }` devuelve 200, crea `Codex.heartbeat`, y `status=alive`. |
| AC2 no-string array with spaces | PASA | `[" Codex "]` devuelve 400. |
| AC2 no-string array two elements | PASA | `["Codex","x"]` devuelve 400. |

## Hallazgo bloqueante

`src/server.js::sanitizeRuntimeControlAgentId` hace:

```js
const raw = String(value || "");
const normalized = ascii(stripControl(raw)).trim();
```

Con `value = ["Codex"]`, `String(value)` produce exactamente `Codex`. Ese valor no contiene controles, no cambia con `trim`, pasa el guard y se usa en `allowlist.get(agentId)`. Resultado observado: activacion real de Codex con un payload que no es el string exacto permitido por la API.

Contrato esperado: `agentId` debe ser un string ASCII exacto registrado. Cualquier otro tipo JSON debe devolver 400 antes del lookup y sin side effect.

## Residuales

- El mtime futuro dentro de 1s queda como tolerancia declarada del diseno actual; no lo uso como bloqueo.
- El body JSON invalido con null crudo puede devolver 500 por parser generico; no es bypass de activacion y no fue el escape bloqueante.

## Recomendacion

CAMBIO-REQUERIDO. Endurecer `sanitizeRuntimeControlAgentId` con type check estricto (`typeof value === "string"`) antes de cualquier coercion, y anadir behavior-test negativo permanente para `agentId: ["Codex"]` que asierte 400 y ausencia de heartbeat.
