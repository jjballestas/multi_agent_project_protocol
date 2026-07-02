# ANALISTA - TASK-0229 remediacion branding - veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO-GO. La remediacion no es cerrable.

Ancla canonica:
- Protocolo REVIEW HEAD: `a99a2b5aeccf697810b7fec5f280ea5f79520569`.
- Producto bajo review: `D:/Agentes/Zeus/Zeus-Aegis` commit `bcb2715b39df895de0ce6bb209cdb0eb3a363a5a`.
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem-branding-75b26ccc78bb49d687ce99891074b581/zeus-aegis`.
- Clean clone protocolo: `C:/Users/johnb/AppData/Local/Temp/analista-0229-protocol-clean`, checkout `a99a2b5aeccf697810b7fec5f280ea5f79520569`.

## Reproduccion

| Gate / probe | Exit | Resultado |
|---|---:|---|
| `npm test` en clon limpio de producto | 0 | Verde, wrapper completo. Vendor reporto 83 files / 562 tests. |
| `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/zeus-env-aliases.test.ts` | 0 | Verde, 3/3. Shim ZEUS/HERMES sigue cubierto. |
| `corepack pnpm --dir vendor/hermes-2.3.0 build` | 0 | Verde. |
| `git diff --exit-code ea3f52c bcb2715 -- vendor/hermes-2.3.0/package.json vendor/hermes-2.3.0/electron-builder.config.cjs` | 0 | Sin renombre de package/appId/config de empaquetado entre base y remediacion. |
| Protocolo live `validate_collaboration_state.py` | 0 | Verde. |
| Protocolo live `scan_domain_neutrality.py` | 0 | Verde. |
| Protocolo live `scan_encoding.py` | 0 | Verde. |
| Protocolo live drift via `protocol_state_drift(Path("."))` | 0 | `has_drift=False`, `up_to_seq=3117` tras claim. |
| Protocolo clean `validate_collaboration_state.py` | 0 | Verde. |
| Protocolo clean `scan_domain_neutrality.py` | 0 | Verde. |
| Protocolo clean `scan_encoding.py` | 0 | Verde. |
| Protocolo clean drift via `protocol_state_drift(Path("."))` | 0 | `has_drift=False`, `up_to_seq=3116`. |
| `Get-FileHash protocol.config.json -Algorithm SHA256` live/clean | 0 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identica. |

## Vector por vector

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| AC1/AC3: cero cadenas Hermes visibles en `vendor/hermes-2.3.0/src/**` salvo allowlist compat/licencia/provenance | SLIPS | Hay textos visibles fuera de allowlist: `src/components/update-center-notifier.tsx:470` muestra `Hermes updated`; `src/screens/swarm2/swarm2-kanban-board.tsx:82/84/88` muestra `Synced with Hermes Dashboard` y `Hermes Dashboard kanban plugin detected`; `src/screens/swarm2/swarm2-kanban-board.tsx:69/105` muestra `Hermes Kanban`; `src/components/settings-dialog/settings-dialog.tsx:599` muestra `hermes gateway restart`; `src/components/onboarding/setup-step-content.tsx:119/130` muestra `~/.hermes/.env` y `cd hermes-agent && hermes --gateway`; `src/routes/early-access.tsx:13/24/27/41` y `src/routes/reserve.tsx:109/115/156` exponen `HermesWorld`. |
| AC1/AC3: cero cadenas Hermes visibles en `vendor/hermes-2.3.0/electron/server-bundle.cjs` salvo allowlist compat/licencia/provenance | SLIPS | El bundle distribuible sigue conteniendo los mismos textos visibles: `electron/server-bundle.cjs:253824` contiene `Hermes updated`; `226769` contiene `Hermes gateway`; `228992` contiene `hermes gateway restart`; `274304` contiene instrucciones con `github.com/NousResearch/hermes-agent`, `hermes-agent`, `zeus gateway run` y `hermes dashboard`; `273774/273775/282330+` conservan ruta/componente `HermesWorld`; `275339/275343/275351` contienen `Hermes Kanban`. |
| Familias buscadas, no solo ejemplos previos | SLIPS | Conteo en `src/**` + bundle: `HermesWorld: 359`, `Hermes Dashboard: 27`, `Hermes Kanban: 22`, `~/.hermes: 64`, `HERMES_HOME: 143`, `HERMES_API_URL: 13`, `HERMES_API_TOKEN: 13`. No todo esto es bloqueante por si solo; el bloqueo son las cadenas user-facing no incluidas en la allowlist. |
| Shim `ZEUS_*` con fallback `HERMES_*` | PASA | Test dirigido `zeus-env-aliases.test.ts` exit 0, 3/3. |
| `npm test` en clon limpio | PASA | Exit 0, wrapper completo. |
| Build vendor | PASA | `corepack pnpm --dir vendor/hermes-2.3.0 build` exit 0. |
| No renombrar binarios/appId/paquetes | PASA | `package.json` y `electron-builder.config.cjs` no cambian frente a `ea3f52c`; `appId` sigue `com.hermesworkspace.app`, `productName` sigue `hermes-workspace`. Esto es coherente con el AC de merge upstream, aunque esos nombres no pueden usarse para cerrar el AC de copy visible. |
| NOTICE / MIT intacto | PASA con alcance | `vendor/hermes-2.3.0/package.json` conserva `license: MIT`; no halle renombre de package/config. No lo uso como bloqueo. |

## Bloqueo falsable

Ejecutar en el clon limpio:

```powershell
$paths = @('vendor/hermes-2.3.0/src','vendor/hermes-2.3.0/electron/server-bundle.cjs')
Get-ChildItem -Path $paths -Recurse -File |
  Select-String -Pattern 'Hermes updated|Hermes Dashboard|Hermes Kanban|HermesWorld|hermes gateway restart|hermes --gateway|~/.hermes|NousResearch/hermes-agent' -CaseSensitive:$false
```

Si ese comando sigue devolviendo las lineas citadas arriba, AC1/AC3 siguen abiertos. La allowlist de la instruccion cubre compat/licencia/provenance, pero no copy visible de UI, onboarding, settings, update center, routes de producto o bundle distribuible.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0229 hasta que el source servido/mostrado y el bundle Electron no contengan cadenas Hermes visibles fuera de una allowlist explicita y verificable de compatibilidad/licencia/provenance.

Residuales declarados:
- Acepte `HERMES_*` como compatibilidad solo cuando aparece en shims/config/env; no acepto textos de UI o instrucciones operativas que presenten Hermes al usuario.
- Acepte que package/appId/productName sigan sin renombrarse por el AC de merge upstream; ese residual no convierte en aceptables las cadenas visibles de UI/bundle.
