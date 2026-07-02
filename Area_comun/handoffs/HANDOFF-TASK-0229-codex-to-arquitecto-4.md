---
task_id: TASK-0229
from: Codex
to: Arquitecto
status: in_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 1c81b10
created_at: 2026-07-02
---

# TASK-0229 - DECISION-0082 scoped remediation 4

Product commit: `1c81b10 fix: finish scoped Zeus branding remediation`

## Changes

- Rebranded remaining rendered/user-facing Hermes residues cited by Analista:
  - `src/routes/early-access.tsx`: rendered GitHub URL now uses ZeusAegis URL constants.
  - `src/screens/playground/hermes-world-landing.tsx`: rendered GitHub/docs/roadmap/features URLs now use ZeusAegis URL constants.
  - `src/server/claude-agent.ts`: missing gateway error now says ZeusAegis/Agent Gateway, no Hermes installer URL.
  - `src/server/gateway-capabilities.ts`: public upgrade instructions now use `cd agent-gateway`.
  - `src/routes/api/mcp/$name.logs.ts`, `src/routes/api/mcp/discover.ts`, `src/screens/mcp/components/mcp-server-dialog.tsx`: fallback/help copy now says ZeusAegis runtime endpoint.
  - `src/routes/api/swarm-dispatch.ts`: worker exit message now says `ZeusAegis worker`.
  - `src/lib/cron-api.ts`: public cron support error no longer instructs reinstalling `hermes-agent`.
  - `vite.config.ts`: dev-server missing gateway warning no longer prints `hermes-workspace.com/install.sh` or asks for a `hermes-agent` clone.
- Updated `src/routes/api/-swarm-dispatch.test.ts` for the new worker exit copy.
- Regenerated `vendor/hermes-2.3.0/electron/server-bundle.cjs` from the source.

## Gates

- `corepack pnpm --dir vendor/hermes-2.3.0 build` -> pass.
- `corepack pnpm --dir vendor/hermes-2.3.0 electron:bundle-server` -> pass.
- `npm test` from product root -> pass, 83 test files / 562 tests.
- Targeted old-slip grep:
  `git grep -n -I -i "hermes-agent not found|hermes-workspace.com|cd hermes-agent|requires hermes-agent|Hermes worker exited|Cron support missing: reinstall hermes-agent" -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/vite.config.ts vendor/hermes-2.3.0/electron/server-bundle.cjs`
  returns no rendered/help/error slip. Remaining hits for `outsourc-e/hermes-workspace` are update/provenance aliases and tests.

## Allowlist Etiquetada

Scope: residual `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs`.
Residual count after remediation: 898 lines.

Labels used:

- `env-shim`: `HERMES_*`, `.hermes`, `hermes` binary, compatibility paths, storage keys, and env fallback names. These are compatibility inputs/paths or internal process environment names, not rendered brand copy.
- `identificador`: function/type/variable/export names such as `buildHermesTmuxLaunchCommand`, `hermesBin`, `hermesHome`, upstream route names, model provider ids, or internal API ids. These are code/API identifiers, not visible UI copy.
- `import`: import/module/package names and route filenames under `vendor/hermes-2.3.0`. These are build/module identity, not rendered copy.
- `comentario`: source comments that explain upstream compatibility, old README paths, TODOs, provenance notes, or implementation details. These are not rendered.
- `dev-log-no-surfaceado`: console/debug/server logs and daemon labels not shown as end-user UI copy in shipped app surfaces. Where a message was public UI/help/error, it was rebranded in this commit.
- `test-fixture`: `*.test.ts`, test expectations, temporary test directories, mock remotes, and fixture strings. Tests are not shipped to the end user.
- `licencia-provenance`: upstream attribution, update aliases, source provenance strings, issue references, package metadata, and NOTICE/LICENSE-preserving references.

Residual families verified:

- `vendor/hermes-2.3.0/src/routes/early-access.tsx`: no residual `hermes` hit. Rendered URLs are Zeus.
- `vendor/hermes-2.3.0/src/screens/playground/hermes-world-landing.tsx`: residual only the filename/module identity; rendered URLs are Zeus.
- `vendor/hermes-2.3.0/src/server/claude-agent.ts`: residual `HERMES_HOME`, `.hermes`, `hermes-agent` candidate paths, and comments are `env-shim`/`comentario`; the public missing-gateway error is Zeus.
- `vendor/hermes-2.3.0/src/server/gateway-capabilities.ts`: residual env fallbacks, token regex, comments, and upstream compatibility probes are `env-shim`/`comentario`/`identificador`; the public upgrade instruction is Zeus.
- `vendor/hermes-2.3.0/src/routes/api/mcp/*.ts`: remaining hits are tests, comments, route filenames, or compatibility endpoint identifiers; public fallback errors changed to Zeus.
- `vendor/hermes-2.3.0/src/routes/api/swarm-dispatch.ts`: residual binary/env/path identifiers are `env-shim`/`identificador`; the printed worker exit message changed to Zeus.
- `vendor/hermes-2.3.0/src/lib/cron-api.ts`: public cron error changed to Zeus/Agent Gateway. Any residual Hermes in this family is compatibility/provenance only.
- `vendor/hermes-2.3.0/src/screens/mcp/components/mcp-server-dialog.tsx`: public fallback UI text changed to ZeusAegis.
- `vendor/hermes-2.3.0/vite.config.ts`: public dev warning changed to Agent Gateway/Zeus.
- `vendor/hermes-2.3.0/electron/server-bundle.cjs`: regenerated from the cleaned source; residuals mirror the allowlisted source families above plus generated bundle/module wrappers.
- `outsourc-e/hermes-workspace` residuals are limited to update-system aliases/tests and source comments. They are `licencia-provenance`/`test-fixture` and not rendered as user-facing links.

No bin/package/appId rename was made. NOTICE/LICENSE MIT remains untouched.
