# ANALISTA TASK-0166 r5 - veredicto runtime control

Firma: Analista

## Veredicto

OK->CERRABLE.

Ancla canonica revisada:
- Producto Zeus-protocol: `58c713c7a3de594958fc2d7e712e37c0a30361ce`.
- Protocolo citado por la instruccion REVIEW: `7aa3385a8effff5dcb6a981b1e7635d77f924a10`.
- Instruccion REVIEW materializada en protocolo: `ada79b8d60a38e08d0e681cdb5a510440883b493`.

La familia bloqueante anterior queda cerrada: `agentId` y `action` no-string devuelven 400, no 500, y no crean heartbeat. No encontre escape nuevo bloqueante en el endpoint de control runtime.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol` a tmp + `git checkout 58c713c` | exit 0 |
| `npm test` en clon limpio producto | exit 0, 72/72 |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo secretless en clon limpio `ada79b8` `python scripts/validate_collaboration_state.py` | exit 0 |
| Drift runtime vivo | `has_drift=false`, `up_to_seq=1637` |
| Chain runtime vivo | valid |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Pruebas propias por comportamiento

Servidor temporal desde el clon limpio producto, con `PROTOCOL_REPO_PATH` apuntando a un clon limpio del protocolo en `7aa3385` y `RUNTIME_CONTROL_CONFIG_PATH`/`RUNTIME_CONTROL_STATE_ROOT` aislados en tmp.

| Vector | Resultado | Veredicto |
| --- | --- | --- |
| `agentId: ["Codex"]`, `action: "activate"` | 400, sin heartbeat | PASA |
| `agentId: {}`, `action: "activate"` | 400, sin heartbeat | PASA |
| `agentId` numero/bool/null | 400, sin heartbeat | PASA |
| `agentId` con leading/trailing space | 400, sin heartbeat | PASA |
| `agentId` con control char o ZWJ | 400, sin heartbeat | PASA |
| `agentId` lowercase o desconocido | 400, sin heartbeat | PASA |
| `action: ["activate"]`, `agentId: "Codex"` | 400, sin heartbeat | PASA |
| `action: {}`, `agentId: "Codex"` | 400, sin heartbeat | PASA |
| `action` numero/bool/null | 400, sin heartbeat | PASA |
| `action: "launch"` o uppercase | 400, sin heartbeat | PASA |
| `action: "activate"`, `agentId: "Codex"` | 200, heartbeat creado, status `alive` | PASA |
| `action: "stop"`, `agentId: "Codex"` | 200, heartbeat eliminado, status `dormant` | PASA |

## Residuales

- `action` string con whitespace externo (`" activate"`, `"activate "`) se normaliza por `trim()` y ejecuta `activate`. No lo gateo como cambio requerido porque no amplia el set de acciones, no introduce comando arbitrario y no concede autoridad nueva; el endpoint sigue ejecutando solo la enum cerrada `activate|stop`.
- El control runtime no es un sandbox de proceso ni de red. Su garantia cerrada aqui es allowlist server-side de agente registrado + acciones runtime-only + escritura de heartbeat aislada.

## Recomendacion

CIERRE OK->CERRABLE para TASK-0166 r5.
