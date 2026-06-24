# ANALISTA TASK-0171 - veredicto fix private-key ACL

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica revisada:
- Producto Zeus-protocol: `cb7ce0a` (`fix(worker): restrict private key ACL`).
- Protocolo citado por la instruccion REVIEW: `1e3a4e7`.
- Instruccion REVIEW materializada en protocolo: `62bd09d`; gates finales corridos sobre el vivo en `01586e8`.

No encontre escape nuevo bloqueante. La privada queda protegida de forma verificable en Windows real: la ACL del
fichero generado contiene solo `JBALL_PC\johnb:(F)` para el usuario actual y no contiene Everyone, BUILTIN\Users ni
NT AUTHORITY\Authenticated Users. La ruta de la privada sigue derivada por servidor bajo `.secrets/workers`, el id del
worker sigue validado, y `icacls` se invoca via `execFile` con argv fijo, sin shell.

## Reproduccion

| Prueba | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout cb7ce0a` | exit 0 |
| `npm test` en clon limpio producto | primera corrida timeout local exit 124 a 304s; rerun exit 0, 74/74 |
| Clon protocolo anclado `1e3a4e7`; `python scripts/validate_collaboration_state.py --root <clone>` | exit 0 |
| Protocolo vivo; `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo vivo; `python scripts/scan_domain_neutrality.py` | exit 0 |
| Protocolo vivo; `python scripts/scan_encoding.py` | exit 0 |
| Drift protocolo vivo | `has_drift=false`, `up_to_seq=1743` |
| #4 `protocol.config.json` | byte-identica, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Dry run no escribe secretos ni ledger | PASA | `dry_run` propio devolvio 200; no se creo runtime config antes de execute. |
| Execute no expone privada | PASA | `execute` propio devolvio 200; respuesta y `extractors.runtime.json` no contienen `BEGIN PRIVATE KEY`; el fichero privado si existe en `.secrets/workers`. |
| ACL Windows restringida | PASA | `icacls` del fichero: solo `JBALL_PC\johnb:(F)` mas linea de exito; no aparecen Everyone, BUILTIN\Users ni Authenticated Users. |
| POSIX 0600 | PASA por lectura de codigo | Rama no-Windows hace `writeFile(..., mode: 0o600)` y luego `chmod(privateKeyPath, 0o600)`. No ejecutable en esta plataforma Windows. |
| `icacls` acotado | PASA | Unico uso nuevo es `execFileAsync("icacls", [privateKeyPath, "/inheritance:r", "/grant:r", "<user>:F", "/remove:g", SID...])`; sin shell. El guard `allowedCliBinaries` permite solo `git`, `python`, `icacls`. |
| Fallo de proteccion fail-closed | PASA | Con `PATH=""`, `icacls` falla: endpoint 500, `code=PRIVATE_KEY_PROTECTION_FAILED`, privada borrada, registry no creado. |
| Ruta privada server-controlled | PASA | `worker.id` traversal/space y type confusion devuelven 400; `assertPathUnderRoot` valida `PRODUCT_WORKER_SECRETS_ROOT`. |
| Endpoint/provider no local o no permitido | PASA | Payloads propios `2130706433`, `8.8.8.8`, IPv4-mapped externo y provider no `local-vlm` devuelven 400. |
| Duplicate y confirmacion | PASA | Missing confirm devuelve 409; duplicate tras execute devuelve 400. |
| Fronteras del protocolo | PASA | Hashes de `protocol.config.json`, `runtime/state/events.jsonl` y `runtime/state/snapshot.json` del protocolo clonado se mantuvieron iguales tras execute. |

## Residuales

- La prueba POSIX queda por lectura porque esta pasada corrio en Windows real.
- El control de `icacls` depende de que el proceso no este corriendo bajo una cuenta o entorno comprometido. No es un sandbox; es una proteccion de fichero para la clave generada por el servidor.

## Recomendacion

CERRABLE. Procede cerrar TASK-0171 si el Arquitecto no requiere otra voz.
