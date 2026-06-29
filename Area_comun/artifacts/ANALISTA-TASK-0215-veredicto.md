---
task_id: TASK-0215
reviewed_task: TASK-0213
reviewer: Analista
type: adversarial_review
status: cambio-requerido
protocol_head_review_instruction: 3d7da2eeae13524150106f6fcd8120c3e119c3d3
protocol_commit_under_review: d2d19e26bb46498723f37265cc7de10c50153064
signature: Analista
---

# ANALISTA TASK-0215 - Veredicto adversarial TASK-0213

## Veredicto

CAMBIO-REQUERIDO. TASK-0213 no es cerrable.

El golden de la ceremonia pasa en clon limpio del protocolo, y V3/V4/V5 sostienen para los caminos honestos. Pero hay dos slips falsables:

1. V2 REFUTADO: un worker keyless puede escribir el ledger bajo `event_state.enforce=true` si el override local lo atribuye a la clave de un firmante. El evento queda como `actor: agent-worker` pero `actor_auth.keyid: agent-a:v1` y `event_auth.key_id: agent-a-hmac:v1`, y `submit_intent` devuelve exit 0 con escritura real. Falta un guard de binding actor->keyid, no solo verificacion criptografica de keyid.
2. V1 DEBIL: `scripts/keygen_agent.py --secret-dir <absolute-path>` escribe PEM/HMAC fuera de `protocol-secrets/` y lo declara en stdout JSON. Aunque el camino de `new_instance.py` usa el default seguro, el script standalone permite violar la garantia "privadas->protocol-secrets".

## Ancla canonica

- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260629-Arquitecto-to-Analista-GO-TASK-0215.md` en protocolo HEAD `3d7da2eeae13524150106f6fcd8120c3e119c3d3`.
- Commit bajo review: `d2d19e26bb46498723f37265cc7de10c50153064` (`feat(instancing): add attested ceremony`).
- Clon limpio protocolo: `C:/Users/johnb/AppData/Local/Temp/protocol-review-0215-235089e9f6a74572b7d829e9c3c6894b`, checkout `d2d19e2`.
- Clon obligatorio de producto: `C:/Users/johnb/AppData/Local/Temp/zeus-protocol-review-0215-f2b5d43960a44d8d8be5b43c7edb3947`; `git checkout d2d19e2` salio exit 1 porque ese commit no existe en `D:/Agentes/Zeus/Zeus-protocol`. No se pudo ejecutar `npm test` ahi por ausencia del commit citado. La tarea revisada es del repo protocolo, no del producto.

## Reproduccion y exit codes

| Gate / probe | Exit | Resultado |
|---|---:|---|
| `git clone D:/Agentes/multi_agent_project_protocol <tmp>; git checkout d2d19e2; python scripts/test_attested_instancing.py` | 0 | Golden oficial PASS. |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout d2d19e2` | 1 | Commit citado no existe en el repo producto; `npm test` no aplicable. |
| `new_instance.py --tier attested --roster <signer+worker>` en clon limpio protocolo | 0 | Instancia generada. |
| `validate_collaboration_state.py --root <instancia>` | 0 | Estado generado valido. |
| Clon sin `protocol-secrets/`: `validate_collaboration_state.py --root <clone>` | 0 | Verificacion portable por publicas sostiene. |
| Clon sin secretos, `actor_auth_enforce=true`, `submit_intent --actor-id agent-a` | 1 | Falla cerrado: `actor_auth private signing key missing for actor: agent-a`; no cambia `events.jsonl`. |
| Worker honesto, `actor_auth_enforce=true`, sin clave privada propia | 1 | Falla cerrado: `actor_auth private signing key missing for actor: agent-worker`; no cambia `events.jsonl`. |
| Worker con override cruzado a clave/HMAC de `agent-a`, `event_state.enforce=true` | 0 | REFUTADO: escribe evento aplicado como `agent-worker` firmado con `agent-a:v1`; `events.jsonl` cambia. |
| `keygen_agent.py --secret-dir <absolute external-secrets> --output -` | 0 | DEBIL: crea `escape-agent-ed25519-private.pem` y `escape-agent-eventauth.key` fuera de `protocol-secrets/` y publica esas rutas en stdout JSON. |
| Hashes pineados antes/despues de keygen+ceremonia (`runtime/eventlog.py`, validador, `protocol.config.json`) | 0 | Byte-identicos. |
| Drift de instancia generada | 0 | `has_drift=false`, `up_to_seq=1`, `enforced=false`, `authoritative=false`. |
| Repo vivo: `validate_collaboration_state.py`, `scan_encoding.py` | 0 | Verdes; validate mantiene solo warnings preexistentes. |
| Repo vivo: drift | 0 | `has_drift=false`, `up_to_seq=2512`. |
| Repo vivo: `protocol.config.json` sha256 | 0 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, sin diff. |

## Tabla vector por vector

| Vector | Veredicto | Evidencia falsable |
|---|---|---|
| V1 secretos no impresos/commiteados/filtrados | DEBIL | Camino honesto: `.gitignore` oculta `protocol-secrets/` y `git status --porcelain` no muestra PEM/HMAC. Slip: `keygen_agent.py --secret-dir C:/.../external-secrets --output -` sale 0, crea PEM/HMAC fuera de `protocol-secrets/` y devuelve rutas absolutas secret-bearing. Exigir que `--secret-dir` quede bajo `<root>/protocol-secrets` o documentar/cambiar el AC. |
| V2 worker keyless no escribe bajo enforce | REFUTADO | Con `event_state.enforce=true` y `actor_auth_enforce=true`, basta anadir en `event-state.runtime.json` `keyids.agent-worker=agent-a:v1`, `private_key_files.agent-worker=<agent-a pem>` y `event_auth.keys.agent-worker=<agent-a hmac>`. `submit_intent --actor-id agent-worker` sale 0 y materializa claim. El evento lleva `actor=agent-worker` con keyid/HMAC de `agent-a`; no hay binding estricto actor->keyid propio. |
| V3 clon sin secretos verifica pero no firma | PASA | Copia sin `protocol-secrets/` valida exit 0. Con `actor_auth_enforce=true`, firmante `agent-a` no puede escribir: exit 1 por clave privada ausente y `events.jsonl` byte-identico. |
| V4 guardrail TFM pineados del hub | PASA | En clon `d2d19e2`, hash antes/despues de keygen+ceremonia identico para `runtime/eventlog.py`, `scripts/validate_collaboration_state.py`, `protocol.config.json`. |
| V5 genesis/cadena/enforce-off | PASA | Instancia nueva valida exit 0; drift `has_drift=false`; `event_state.enforce=false`, `authoritative=false`; override final `actor_auth_enforce=false`. |
| V6 neutralidad | PASA con residual | No vi terminos de dominio/business en los archivos nuevos ni en la ceremonia. Residual no bloqueante: `scan_domain_neutrality.py --root <instancia>` hereda falsos positivos `operator` de scripts existentes copiados al runtime; el gate canonico del repo vivo es el relevante y debe estar verde. |

## Cambio requerido

1. Bloquear atribucion cruzada: durante firma y verificacion, exigir que el `keyid` usado para `actor_auth` pertenezca de forma inmutable al `actor` declarado y que el HMAC `key_id` sea el de ese actor. Si un worker no tiene keyid propio publicado, cualquier intento de mapearlo a un keyid de firmante debe fallar antes de escribir.
2. Endurecer `keygen_agent.py`: rechazar `--secret-dir` absoluto o relativo que resuelva fuera de `<root>/protocol-secrets/` (o eliminar la opcion para el camino atestado). Mantener solo rutas portables bajo `protocol-secrets/`.
3. Anadir regresiones permanentes: worker con `keyids.worker=signer:v1` + private/HMAC del signer debe salir exit 1 y dejar `events.jsonl` byte-identico; keygen con `--secret-dir` externo debe salir exit 1.

## Recomendacion de cierre

CAMBIO-REQUERIDO. No cerrar TASK-0213 hasta que V2 y V1 tengan controles negativos permanentes y una re-pasada adversarial salga verde.

Firmado: Analista
