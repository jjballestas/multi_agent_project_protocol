---
task_id: TASK-0229
artifact_type: review_verdict
reviewer: Analista
status: final
created_at: 2026-07-02
canonical_protocol_commit: fd7c10f
canonical_product_repo: D:/Agentes/Zeus/Zeus-Aegis
canonical_product_commit: 1c81b109c533eaaf266c337bdb3bae5f0bf8f6ef
recommendation: CAMBIO-REQUERIDO
---

# ANALISTA - TASK-0229 remediacion branding 4 scope

Veredicto: **CAMBIO-REQUERIDO / NO-GO**. Bajo DECISION-0082, el gate ya no es cero-grep, pero todavia hay strings `hermes` que se renderizan o se navegan en superficies user-facing y estan tratados como internos por la allowlist.

## Ancla canonica

- Protocolo bajo review: `fd7c10f` (`coord(TASK-0229): re-REVIEW acotado al Analista...`).
- Handoff canonico: `Area_comun/handoffs/HANDOFF-TASK-0229-codex-to-arquitecto-4.md`.
- Producto citado por la instruccion canonica: `D:/Agentes/Zeus/Zeus-Aegis`.
- Producto commit: `1c81b109c533eaaf266c337bdb3bae5f0bf8f6ef`.
- Nota de ancla: `1c81b10` no existe en `D:/Agentes/Zeus/Zeus-protocol` (`git rev-parse` exit 1); si existe en `Zeus-Aegis` (`git rev-parse` exit 0). Use el repo de producto citado por TASK-0229 y por el handoff 4.
- Clean clone producto: `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem4-aegis-a6b482ee17a74db38f8bac3aca1436fe`.

## Reproduccion

| Gate | Resultado |
|---|---|
| `npm test` en clean clone producto | EXIT 0; 83 files / 562 tests |
| `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/zeus-env-aliases.test.ts` | EXIT 0; 3/3 |
| `corepack pnpm --dir vendor/hermes-2.3.0 build` | EXIT 0 |
| `corepack pnpm --dir vendor/hermes-2.3.0 electron:bundle-server` | EXIT 0 |
| `git diff --exit-code -- vendor/hermes-2.3.0/electron/server-bundle.cjs` tras bundle | EXIT 0; bundle regenerado coincide |
| Diff no-rename sobre `package.json`, `electron-builder.config.cjs`, `NOTICE`, `LICENSE*` | EXIT 0 / vacio para rutas relevantes |
| Protocolo vivo `validate`, `scan_domain_neutrality`, `scan_encoding` | EXIT 0 |
| Protocolo clean clone `fd7c10f` mismos gates | EXIT 0 |
| Drift vivo y clean | `has_drift=false`, `up_to_seq=3149` |
| `protocol.config.json` SHA256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| AC no cero-grep bajo DECISION-0082 | PASA | No bloqueo por identificadores, imports, comentarios, fixtures, env shim, storage keys o provenance no renderizados. |
| Slips citados en ronda 3: `early-access.tsx`, `hermes-world-landing.tsx`, errores/help de gateway/MCP/swarm | PASA en los ejemplos citados | Grep dirigido por `hermes-agent not found`, `hermes-workspace.com`, `cd hermes-agent`, `requires hermes-agent`, `Hermes worker exited`, `Cron support missing: reinstall hermes-agent` sobre `src`, `vite.config.ts` y bundle: EXIT 1 (sin matches). |
| Shim ZEUS/HERMES | PASA | `zeus-env-aliases.test.ts` EXIT 0 (3/3). |
| Bundle regenerado desde src | PASA | `build` EXIT 0, `electron:bundle-server` EXIT 0, `git diff --exit-code -- electron/server-bundle.cjs` EXIT 0. |
| Binarios/appId/paquete y NOTICE MIT | PASA | Diff dirigido sobre package/electron-builder/NOTICE/LICENSE no muestra cambios relevantes. |
| Allowlist etiquetada: `env-shim`/compat binary no renderizado | SLIP | `vendor/hermes-2.3.0/src/screens/settings/components/provider-wizard.tsx:657` renderiza en UI de setup: `<code className="font-mono">hermes</code>` dentro de "Run ... in terminal to verify". Esto es texto de setup mostrado al usuario; DECISION-0082 punto 1 cubre onboarding/setup y ayuda/uso. No es un env shim oculto. |
| Allowlist etiquetada: URL/path no user-facing | SLIP | `vendor/hermes-2.3.0/src/screens/playground/hermes-world-embed.tsx:12` navega el iframe a `source=hermes-workspace`. DECISION-0082 punto 1 incluye URLs/enlaces/paths user-facing mostrados o navegados. Aunque el texto visible dice ZeusWorld, la URL navegada conserva marca Hermes. |
| Allowlist etiquetada: provenance/update internals | SLIP | `vendor/hermes-2.3.0/src/routes/api/claude-update.ts:34` expone `expectedRepo: 'hermes-workspace'` para `ZeusAegis Workspace`; `:87` construye error publico `Remote URL does not match expected ${input.expectedRepo} repo.`. Ese JSON alimenta el update center; ante remoto distinto, el usuario ve "expected hermes-workspace repo". |

## Prueba adversarial propia

Probe propio sobre el clean clone:

```text
provider-wizard rendered terminal instruction: SLIP (src/screens/settings/components/provider-wizard.tsx)
zeusworld iframe navigated source query: SLIP (src/screens/playground/hermes-world-embed.tsx)
update API public expected repo value: SLIP (src/routes/api/claude-update.ts)
update API public error template: SLIP (src/routes/api/claude-update.ts)
EXIT 1
```

## Residuales

- No exijo cero-grep: los identificadores `HERMES_*`, imports, rutas internas, storage keys, tests, comentarios y provenance que no se muestran al usuario quedan fuera del bloqueo.
- El mismatch `Zeus-protocol` vs `Zeus-Aegis` queda declarado: el commit citado por el handoff no existe en `Zeus-protocol`, pero si en `Zeus-Aegis`, que es el repo declarado por TASK-0229.

## Recomendacion

**CAMBIO-REQUERIDO.** Rebrandear o justificar de forma falsable los tres slips user-facing anteriores. Con esos corregidos, los gates mecanicos ya estan verdes.

Firma: Analista.
