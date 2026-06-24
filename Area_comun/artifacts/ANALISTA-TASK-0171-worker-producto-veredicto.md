# ANALISTA-TASK-0171-worker-producto-veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO.

El alta de worker de producto cumple las fronteras principales: no toca #4, no emite submit_intent, no registra firmantes, escribe solo el registro runtime de producto, rechaza type-confusion y no devuelve la privada al cliente. El bloqueo es puntual y falsable: la instruccion de review exige privada server-side gitignored con mode 0600, pero en Windows el archivo generado queda observable como mode 0666 via `fs.stat().mode & 0o777`. No cierro una AC de manejo de clave privada si la evidencia local contradice el modo declarado.

## Ancla canonica

| Elemento | Ancla |
|---|---|
| Producto | Zeus-protocol `f6dc8a56a801a50c6624517c835580d46d432199` |
| Protocolo citado por instruccion | `0c24550aebc39498d69a04e37e2a206bccf73ccd` |
| Protocolo con mensaje REVIEW materializado | `2d31a4b8d644a182452dbca83aa82bb748493399` |
| Repo producto probado | clon limpio en `%TEMP%`, checkout detached del commit citado |

## Reproduccion y gates

| Prueba | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout f6dc8a5` | exit 0, HEAD `f6dc8a56a801a50c6624517c835580d46d432199` |
| `npm test` en clon limpio producto | primera corrida local timeout exit 124 a 244s; rerun exit 0, 74/74 |
| `python scripts/validate_collaboration_state.py` repo vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` clon protocolo sin secretos `2d31a4b` | exit 0 |
| `python scripts/validate_collaboration_state.py` clon protocolo citado `0c24550` | exit 0 |
| `python scripts/scan_domain_neutrality.py` repo vivo | exit 0 |
| `python scripts/scan_encoding.py` repo vivo | exit 0 |
| drift vivo | exit 0, `has_drift:false`, `up_to_seq:1708` |
| #4 `protocol.config.json` | byte-identica, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores adversariales

| Vector / AC | Prueba propia por comportamiento | Veredicto |
|---|---|---|
| AC1 alta gobernada preview -> execute | `dry_run` devuelve 200 sin crear registro; `execute` con confirmacion crea `extractors.runtime.json` con worker, publicKeyPem y `enabled:false` | PASA |
| AC2 privada nunca al cliente | Respuesta execute y registry no contienen `PRIVATE KEY`, `BEGIN PRIVATE` ni `privateKeyPem`; logs del server tampoco | PASA |
| AC2 privada nunca a git | `.gitignore` cubre `extractors.runtime.json` y `.secrets/`; `git check-ignore -v` confirma ambas rutas | PASA |
| AC2 mode 0600 de privada | Archivo server-side creado bajo `PRODUCT_WORKER_SECRETS_ROOT`; `fs.stat(private).mode & 0o777` devuelve `666` en Windows, no `600` | SLIPS |
| AC3 off-by-default | Registry guarda `enabled:false`; respuesta declara `liveUseRequires:"file-ingestion gate"`; `loadAgentRoster` filtra workers `enabled:false` | PASA |
| AC4 no #4/genesis/firmantes | Antes/despues del execute: hashes de `protocol.config.json`, `runtime/state/events.jsonl` y `runtime/state/snapshot.json` identicos; `agent_registry` y `signature_config` no contienen el worker | PASA |
| AC4 no submit_intent | Ruta `/api/protocol/product-workers/register` llama `registerProductWorker`, no `runSubmitIntent`; respuesta `submitIntentEmitted:false` | PASA |
| AC5 no top-level injection | `actorId` extra -> 400, sin escribir | PASA |
| AC5 no worker extra keys | `privateKeyPem` extra -> 400, sin escribir | PASA |
| AC5 typeof string estricto | `id` array, `role` object, `provider` array, `defaultModel` number, `defaultEndpoint` object, `mode` array -> 400, sin escribir | PASA |
| AC5 id safe / no traversal | `../Bad`, `Bad\\Path`, `Bad Id` -> 400, sin escribir | PASA |
| AC5 provider allowlist | provider `openai` -> 400, sin escribir | PASA |
| AC5 endpoint loopback-only | `8.8.8.8`, decimal `2130706433`, userinfo `127.0.0.1@evil.com`, IPv4-mapped, HTTPS over `127.0.0.1` -> 400, sin escribir | PASA |
| AC5 duplicate id | second registration of same id -> 400, registry unchanged | PASA |
| AC5 confirm gate | execute without `REGISTER_PRODUCT_WORKER` -> 409, registry unchanged | PASA |

## Residuales declarados

- El modo POSIX no es una garantia portable en Windows. Si el proyecto quiere conservar "mode 0600" como AC, debe probarlo de forma compatible con la plataforma o implementar ACL/restriccion equivalente. Si no es un requisito real en Windows, la AC/review debe dejar de afirmarlo como gate.
- No encontre escape nuevo en #4, submit_intent, agent_registry, signature_config, type-confusion, path traversal, endpoint loopback, duplicate-id u off-by-default.

## Recomendacion

CAMBIO-REQUERIDO: no cerrar TASK-0171 hasta que Codex corrija o haga verificable la proteccion de permisos de la privada del worker en Windows, o hasta que Arquitecto modifique explicitamente el criterio para no exigir mode 0600 como gate. El resto de fronteras esta CERRABLE.
