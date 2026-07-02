# ANALISTA VEREDICTO - TASK-0229 remediacion branding #2

Firma: Analista
Fecha: 2026-07-02
Recomendacion: CAMBIO-REQUERIDO / NO CERRABLE

## Ancla canonica

- Protocolo REVIEW HEAD: `735e9a45aa8ad02bf5fd56514823239211ae85af`
- Entrega protocolo: `5809c30 coord(TASK-0229): deliver branding remediation`
- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-remediacion-branding-2.md`
- Producto citado por handoff: `D:/Agentes/Zeus/Zeus-Aegis`
- Producto bajo review: `c9eb971480fa5eecc9c50cf0329e6676921007bb` (`Remediate Zeus-Aegis branding residues`)
- Clon limpio producto usado: `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem2-aegis-171993b6308741fd873bc6b10215f1f2/zeus-aegis`

Nota de ancla: la orden operativa generica menciona `D:/Agentes/Zeus/Zeus-protocol`, pero el commit `c9eb971` no materializa arbol legible al clonar desde ese repo (`fatal: unable to read tree`). La instruccion REVIEW y la tarea canonica citan `Zeus-Aegis`; el re-gate se hizo ahi.

## Reproduccion y gates

| Gate | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-Aegis ...; git checkout c9eb971480fa5eecc9c50cf0329e6676921007bb` | EXIT 0 |
| `npm test` en clon limpio producto | EXIT 0, 83 files / 562 tests |
| `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/zeus-env-aliases.test.ts` | EXIT 0, 3/3 |
| `corepack pnpm --dir vendor/hermes-2.3.0 build` | EXIT 0 |
| Diff `package.json` / `electron-builder.config.cjs` raiz y vendor para appId/binarios | EXIT 0, sin diff |
| `python scripts/validate_collaboration_state.py` protocolo vivo | EXIT 0 |
| `python scripts/validate_collaboration_state.py --root <clean protocol 735e9a4>` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` vivo y clean | EXIT 0 |
| `python scripts/scan_encoding.py` vivo y clean | EXIT 0 |
| Drift protocolo vivo | `has_drift=false`, `up_to_seq=3124` antes de mi claim |
| Drift protocolo clean 735e9a4 | `has_drift=false`, `up_to_seq=3124` |
| `protocol.config.json` sha256 vivo y clean | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Estado | Evidencia falsable |
|---|---|---|
| Strings exactas de mi NO-GO anterior: `Hermes updated`, `Hermes Dashboard`, `Hermes Kanban`, `HermesWorld`, `hermes gateway restart`, `hermes --gateway`, `~/.hermes`, `NousResearch/hermes-agent` en `vendor/hermes-2.3.0/src/**` y bundle | PASA parcial | Probe exacto no encontro esas cadenas fuera de compat esperada. |
| Shim `ZEUS_*` con fallback `HERMES_*` | PASA | Test `zeus-env-aliases.test.ts` EXIT 0, 3/3. |
| Build / bundle regenerable | PASA | `corepack pnpm --dir vendor/hermes-2.3.0 build` EXIT 0. |
| `npm test` en clon limpio | PASA | EXIT 0, 83 files / 562 tests. |
| No renombrar binarios/appId/paquetes | PASA | Diff contra parent en `package.json` / `electron-builder.config.cjs` raiz y vendor vacio. |
| NOTICE/LICENSE MIT intacto | PASA | `vendor/hermes-2.3.0/LICENSE` conserva `MIT License`; no cambio bloqueante detectado. |
| `grep -ri hermes` sobre `vendor/hermes-2.3.0/src` + `vendor/hermes-2.3.0/electron/server-bundle.cjs` deja solo allowlist compat/licencia/provenance | SLIPS | Persisten cadenas visibles no allowlist en src y bundle. Ejemplos: `src/screens/swarm2/swarm2-screen.tsx:864` contiene `Spawning a Hermes swarm worker`; `src/screens/swarm2/swarm2-screen.tsx:1498` contiene `Detected Hermes profiles`; `src/screens/swarm2/swarm2-screen.tsx:1724` contiene `Hermes config`; `src/screens/jobs/create-job-dialog.tsx:152` contiene `Build a scheduled Hermes task`; `src/screens/playground/components/map-panel.tsx:38` contiene `Hermes Realm`; `src/screens/playground/components/inventory-panel.tsx:29` contiene `Hermes Sigil`; `src/routes/settings/index.tsx:1147` contiene `Could not load Hermes configuration`; el bundle reproduce estas mismas cadenas en `electron/server-bundle.cjs` lines 143812, 144345, 144573, 147651, 152563, 154154, 221294, 226097, 227477. |
| Bundle no arrastra strings viejos desde src | SLIPS | El bundle incluye residuos no allowlist que existen en src. Por ejemplo `Spawning a Hermes swarm worker` y `Hermes Realm` aparecen tanto en src como en `electron/server-bundle.cjs`. |

## Probe adversarial

Probe exacto sobre las cadenas de la instruccion produjo `hitCount=14`, pero todos los hits son `HERMES_API_URL` compat o `Hermes Workspace` en `src/server/pty-helper.py`. Eso no cierra el AC completo porque la misma instruccion exige que un `grep -ri hermes` sobre src+bundle deje solo allowlist.

El `git grep -n -I -i "hermes" -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` devuelve muchas cadenas no allowlist y user-facing. Las mas graves estan en pantallas de Swarm, Jobs, Settings, MCP fallback y Playground, y el bundle versionado las contiene tambien.

## Residuales declarados

- No bloqueo por `HERMES_*` usado como shim de compatibilidad.
- No bloqueo por licencia MIT ni por menciones de provenance estrictamente legales.
- Si el alcance de TASK-0229 pretende limitarse solo a la lista exacta anterior, entonces el DoD y el requested_action deben cambiar. Con el texto canonico actual, "0 cadenas hermes VISIBLES al usuario" y "grep -ri hermes ... SOLO allowlist" no estan cumplidos.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0229. Codex debe purgar o allowlistear explicitamente los residuos visibles restantes en `vendor/hermes-2.3.0/src/**` y regenerar `vendor/hermes-2.3.0/electron/server-bundle.cjs` desde ese src limpio. El siguiente re-gate debe incluir un probe que falle si `git grep -n -I -i "hermes"` en src+bundle contiene textos user-facing fuera de allowlist.
