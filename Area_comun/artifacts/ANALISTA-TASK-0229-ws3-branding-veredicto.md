---
artifact_id: ANALISTA-TASK-0229-ws3-branding-veredicto
task_id: TASK-0229
author: Analista
created_at: 2026-07-02
verdict: CAMBIO-REQUERIDO
canonical_protocol_head: ab120827f36cc5fd6d5fbc9975318b19e0f6fd3a
canonical_product_repo: D:/Agentes/Zeus/Zeus-Aegis
canonical_product_commit: ea3f52ce30abefe266b81661189d6d7864d69cb3
review_message: Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0229-ws3-branding.md
signature: Analista
---

# Veredicto TASK-0229 WS3 Branding

RECOMENDACION DE CIERRE: CAMBIO-REQUERIDO. No cerrable.

El gate sustantivo falla por AC1: aun quedan cadenas Hermes visibles al usuario en codigo fuente de UI y en el bundle Electron versionado. Esto contradice el DoD "0 cadenas hermes VISIBLES al usuario". Los alias ZEUS_* con shim HERMES_* pasan en los probes propios, y los gates de build/test salen verdes, pero el cierre no es defendible mientras esas superficies sigan exponiendo Hermes.

## Anclas canonicas

| Superficie | Ancla |
|---|---|
| Protocolo que contiene la instruccion REVIEW | `ab120827f36cc5fd6d5fbc9975318b19e0f6fd3a` |
| Producto bajo review | `D:/Agentes/Zeus/Zeus-Aegis` |
| Commit producto probado en clon limpio | `ea3f52ce30abefe266b81661189d6d7864d69cb3` |
| Commit funcional de branding dentro de ese HEAD | `980445cd7a3d0662040da72181fb285a4c003cb6` |
| Clon limpio producto | `C:/Users/johnb/AppData/Local/Temp/analista-0229-ws3-6feea6e1392a4806840fdf1817f905e0/zeus-aegis` |

## Reproduccion

| Gate | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-Aegis ... ; git checkout ea3f52ce30abefe266b81661189d6d7864d69cb3` | EXIT 0 |
| `npm test` en clon limpio producto | EXIT 0, wrapper total 376.1 s, Vitest 83 files / 562 tests en el tramo vendor |
| `corepack pnpm --dir vendor/hermes-2.3.0 build` | EXIT 0 |
| Probe propio Vitest alias HERMES URL/dashboard/password sin ZEUS | EXIT 0, 2/2 |
| `python scripts/validate_collaboration_state.py` protocolo vivo | EXIT 0 |
| `python scripts/validate_collaboration_state.py --root <clean-protocol>` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` vivo y clean-protocol | EXIT 0 |
| `python scripts/scan_encoding.py` vivo y clean-protocol | EXIT 0 |
| Drift protocolo vivo y clean-protocol | `has_drift=false`, `up_to_seq=3104` |
| `protocol.config.json` sha256 vivo y clean-protocol | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| AC1: cero cadenas Hermes visibles al usuario en UI/strings/i18n/onboarding | SLIPS | `git grep -n -I "Hermes Agent\\|Hermes Workspace\\|HERMES_API_URL\\|hermes setup\\|hermes gateway run" -- vendor/hermes-2.3.0/src` devuelve multiples superficies visibles. Ejemplos: `src/components/connection-startup-screen.tsx:28` muestra `Set HERMES_API_URL...`; `:361` y `:366` muestran `HERMES_API_URL`; `src/components/onboarding/setup-step-content.tsx:135` muestra `Or point HERMES_API_URL`; `src/components/mobile-hamburger-menu.tsx:226` muestra `Hermes Agent`; `src/screens/mcp/mcp-screen.tsx:62` muestra `Hermes Workspace - MCP`; `src/screens/skills/skills-screen.tsx:465` muestra `Hermes Workspace Marketplace`. |
| AC2: alias ZEUS_API_URL / ZEUS_API_TOKEN con shim HERMES_* funcionando | PASA con residual de copy | Test existente cubre preferencia ZEUS. Probe propio agrego familia HERMES fallback: sin ZEUS, `HERMES_API_URL` gana a `CLAUDE_API_URL`; `HERMES_DASHBOARD_URL` gana a `CLAUDE_DASHBOARD_URL`; `HERMES_PASSWORD` gana a `CLAUDE_PASSWORD`. Probe EXIT 0. Residual: algunos textos de ayuda siguen pidiendo `HERMES_API_URL` como variable visible, que bloquea AC1 aunque el shim funcione. |
| AC3: pantalla "Preparando tu entorno Zeus" reemplaza setup manual | SLIPS | Existe copy Zeus en `src/screens/chat/components/connection-status-message.tsx`, pero `src/components/connection-startup-screen.tsx` sigue renderizando setup manual con `Set HERMES_API_URL`, `hermes setup`, `hermes gateway run`, y hint `HERMES_API_URL=http://your-server:8642 pnpm dev`. |
| AC4: no renombrar binarios internos/appId/paquetes | PASA | Diff de la entrega no cambia `appId` ni identidad interna; mantiene `hermes`/`hermes-agent` como comandos internos. Este punto no bloquea. |
| AC5: NOTICE/LICENSE MIT permanece | PASA | `vendor/hermes-2.3.0/LICENSE` conserva MIT copyright upstream. No encontre perdida de licencia por el commit bajo review. |
| AC6: render/build y `npm test` verdes por EXIT en clon limpio | PASA | `npm test` EXIT 0; `corepack pnpm --dir vendor/hermes-2.3.0 build` EXIT 0. |
| Bundle Electron versionado no debe exponer marca vieja si es distribuible | SLIPS | `vendor/hermes-2.3.0/electron/server-bundle.cjs` versionado contiene textos visibles como `Hermes Workspace Marketplace`, `Welcome to Hermes Workspace`, `Hermes Agent not connected`, y `HERMES_API_URL`. Si ese bundle entra en distribucion Electron, la marca vieja queda visible incluso tras compilar fuente. |

## Bloqueo falsable

Minimo para destrabar: limpiar o justificar con allowlist estricta todas las ocurrencias visibles de `Hermes Agent`, `Hermes Workspace`, `HERMES_API_URL`, `hermes setup` y `hermes gateway run` en `vendor/hermes-2.3.0/src/**` y en cualquier bundle versionado/distribuible. Las ocurrencias aceptables deben quedar limitadas a comandos internos, compatibilidad, licencia/provenance o rutas internas, no a labels, instrucciones, placeholders, errores ni onboarding visible.

## Residuales

- No bloqueo por assets `hermesworld`/NousResearch: DECISION-0076 los deja como gate de release aparte.
- No bloqueo por nombres internos `hermes`, `hermes-agent`, rutas `~/.hermes`, headers y API names: DECISION-0076 preserva mergeabilidad y compatibilidad.
- La suite esta verde, pero no cubre exhaustivamente la promesa de marca visible; el grep sobre fuente y bundle si demuestra escapes nuevos.

Firma: Analista.
