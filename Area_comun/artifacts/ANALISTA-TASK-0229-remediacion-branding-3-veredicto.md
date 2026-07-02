# ANALISTA - TASK-0229 remediacion branding 3 - veredicto

Firma: Analista.

## Veredicto

CAMBIO-REQUERIDO / NO-GO. No recomiendo cierre.

El gate funcional principal pasa, pero el AC de la instruccion no pasa: el grep residual de `hermes` sobre
`vendor/hermes-2.3.0/src` y `vendor/hermes-2.3.0/electron/server-bundle.cjs` no queda limitado a compatibilidad,
licencia, provenance interna, env shim o interno no renderizado. Hay residuos user-facing en rutas de UI, mensajes
de error/ayuda y enlaces renderizados.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo REVIEW | `2e3900c80a2ce831b0c7c7dbdb19d9b59a447154` |
| Instruccion procesada | `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-remediacion-branding-3.md` |
| Producto revisado | `D:/Agentes/Zeus/Zeus-Aegis` |
| Commit producto | `1b047d3b4d601351090b95fe53641aa8946769dc` |
| Clean clone producto | `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem3-aegis-f661c42c78eb46b58cc655e1c0232f95` |
| Clean clone protocolo | `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem3-protocol2-bc9a0a24d8c4483fb08e945a7bc05886` |

Nota de alcance: la orden generica menciona `Zeus-protocol`, pero la tarea, el handoff y el commit canonico de
esta ronda citan `D:/Agentes/Zeus/Zeus-Aegis`; revise ese producto.

## Reproduccion

| Comando / gate | Exit | Resultado |
| --- | ---: | --- |
| `git clone D:/Agentes/Zeus/Zeus-Aegis <tmp>; git checkout 1b047d3` | 0 | Checkout limpio del commit citado. |
| `npm --prefix <tmp> test` | 0 | 83 files / 562 tests, pass. |
| `corepack pnpm --dir <tmp>/vendor/hermes-2.3.0 exec vitest run src/server/zeus-env-aliases.test.ts` | 0 | 3/3 pass. |
| `corepack pnpm --dir <tmp>/vendor/hermes-2.3.0 build` | 0 | Build pass. |
| `corepack pnpm --dir <tmp>/vendor/hermes-2.3.0 electron:bundle-server` | 0 | Bundle command pass; rerun in tmp dirties `server-bundle.cjs` because generated bundle embeds absolute build paths. |
| `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` | 0 | 954 residual hits. |
| Targeted old-slip grep (`Hermes Dashboard`, `Hermes Kanban`, `Hermes Workspace`, etc.) | 1 | Old exact examples are gone. |
| Diff package/appId/binarios probe | 0 | No package/electron-builder/bin rename diff found in `1b047d3^..1b047d3`. |
| MIT license probe | 0 | `vendor/hermes-2.3.0/LICENSE` starts `MIT License`; `package.json` keeps `"license": "MIT"`. |
| Protocolo vivo `validate_collaboration_state.py` | 0 | OK. |
| Protocolo vivo `scan_domain_neutrality.py` | 0 | OK. |
| Protocolo vivo `scan_encoding.py` | 0 | OK. |
| Protocolo vivo drift | 0 | `has_drift=false`, `up_to_seq=3140`. |
| Protocolo limpio `validate_collaboration_state.py --root <tmp>` | 0 | OK. |
| Protocolo limpio `scan_domain_neutrality.py --root <tmp>` | 0 | OK. |
| Protocolo limpio `scan_encoding.py --root <tmp>` | 0 | OK. |
| Protocolo limpio drift | 0 | `has_drift=false`, `up_to_seq=3140`. |
| `Get-FileHash protocol.config.json -Algorithm SHA256` | 0 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Vectores / AC

| Vector | Estado | Evidencia falsable |
| --- | --- | --- |
| Full `npm test` producto en clon limpio | PASA | `npm --prefix <tmp> test` exit 0, 83 files / 562 tests. |
| Alias env ZEUS con shim legacy | PASA | `zeus-env-aliases.test.ts` exit 0, 3/3. |
| Old examples bloqueados en rondas previas | PASA | Grep exacto de la familia previa (`Hermes Dashboard`, `Hermes Kanban`, `Hermes Workspace`, `Hermes config`, etc.) exit 1. |
| No rename de binarios/appId/package | PASA | Diff de `1b047d3^..1b047d3` no toca package/electron-builder/binarios. |
| MIT license | PASA | `vendor/hermes-2.3.0/LICENSE` y `vendor/hermes-2.3.0/package.json` conservan MIT. |
| Bundle regenerado | PASA con residual | El bundle existe en el commit y el comando de bundle sale 0. Rerun en clean clone modifica el bundle por rutas absolutas del tmp, asi que no lo uso como byte-identical gate. |
| Grep residual = solo allowlist valida | SLIPS | Comando residual devuelve 954 hits; varios son renderizados o errores publicos, no solo compat/provenance/interno. |
| Allowlist no clasifica user-facing como interno | SLIPS | La allowlist mete enlaces/provenance, storage keys y runtime endpoints, pero algunos aparecen en UI, errores o ayuda. |

## Slips bloqueantes

Estos ejemplos salen del commit `1b047d3` y son suficientes para bloquear el cierre:

```text
vendor/hermes-2.3.0/src/routes/early-access.tsx:4:const HERMES_REPO_URL = 'https://github.com/outsourc-e/hermes-workspace'
vendor/hermes-2.3.0/src/screens/playground/hermes-world-landing.tsx:3:const HERMES_REPO_URL = 'https://github.com/outsourc-e/hermes-workspace'
vendor/hermes-2.3.0/src/screens/playground/hermes-world-landing.tsx:4:const HERMES_ROADMAP_URL = 'https://github.com/outsourc-e/hermes-workspace/blob/main/docs/zeusworld/master-roadmap.md'
vendor/hermes-2.3.0/src/screens/playground/hermes-world-landing.tsx:5:const HERMES_DOCS_URL = 'https://github.com/outsourc-e/hermes-workspace/tree/main/docs/zeusworld'
vendor/hermes-2.3.0/src/screens/playground/hermes-world-landing.tsx:6:const HERMES_FEATURES_URL = 'https://github.com/outsourc-e/hermes-workspace/blob/main/FEATURES-INVENTORY.md'
vendor/hermes-2.3.0/src/server/claude-agent.ts:158:"hermes-agent not found. Run the installer: curl -fsSL https://hermes-workspace.com/install.sh | bash",
vendor/hermes-2.3.0/src/server/gateway-capabilities.ts:155:'For full features, install Agent Gateway from source (`git clone https://github.com/ZeusAegis/agent-gateway && cd hermes-agent && pip install -e .`), then start the gateway on :8642 (`zeus gateway run`). For the extended APIs (Sessions, Skills, Config, Jobs) also start the dashboard on :9119 (`zeus dashboard`).'
vendor/hermes-2.3.0/src/routes/api/mcp/$name.logs.ts:33:'Live test/discover requires hermes-agent /api/mcp runtime endpoint, not yet available on this dashboard.',
vendor/hermes-2.3.0/src/routes/api/mcp/discover.ts:48:'Live test/discover requires hermes-agent /api/mcp runtime endpoint, not yet available on this dashboard.',
vendor/hermes-2.3.0/src/routes/api/swarm-dispatch.ts:215:printf '\n[Hermes worker exited with status %s]\n' "$status"
```

Why these block:

- `early-access.tsx` and `hermes-world-landing.tsx` render external links. The instruction explicitly says
  user-facing URLs/links outside the allowlist are NO-GO. Calling these "provenance" is not enough when they are
  button/link targets in rendered screens.
- `claude-agent.ts`, `gateway-capabilities.ts`, `mcp/*.ts`, and `swarm-dispatch.ts` are public error/help/runtime
  messages. They are not merely internal identifiers.
- The bundle contains the same residues, for example `electron/server-bundle.cjs:137158-137161`,
  `260996`, `274304`, `281149`, `282140`, so the generated artifact still exposes them too.

Additional non-blocking residue families remain in localStorage/storage keys and compatibility endpoints
(`hermes-workspace-locale`, `hermes-workspace-agent-name`, `/api/hermes-tasks`, `HERMES_*`). I do not block on those
when they are truly compatibility state/API, but they must not be used to justify the rendered/error/help examples
above.

## Recomendacion

CAMBIO-REQUERIDO. Remediacion minima: either rebrand or remove the rendered/user-facing Hermes URLs and public
runtime/help/error messages above, regenerate `electron/server-bundle.cjs`, then rerun the same grep gate. Residual
Hermes hits should be limited to a narrower allowlist that distinguishes:

- user-visible link/error/help/copy: must be Zeus or absent;
- compatibility env/API/storage/binary identifiers: may remain;
- tests/fixtures and license/provenance comments/docs not rendered to the operator: may remain.

