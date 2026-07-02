---
handoff_id: HANDOFF-TASK-0229-Codex-remediation-branding-3
task_id: TASK-0229
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-02T06:05:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 1b047d3
---

# TASK-0229 Handoff - branding remediation 3

## Result

Implemented exhaustive Hermes visible-copy remediation in `D:/Agentes/Zeus/Zeus-Aegis`.

Product commit:

```text
1b047d3 fix(branding): remediate visible Hermes copy
```

Scope changed:

- Replaced remaining user-facing Hermes/Hermes Workspace copy in `vendor/hermes-2.3.0/src/**` with Zeus/ZeusAegis wording.
- Preserved compatibility/internal Hermes surfaces where they are API, env, storage, route, binary, upstream provenance, generated route-manifest paths, or test fixture coverage.
- Regenerated `vendor/hermes-2.3.0/electron/server-bundle.cjs` after source remediation.
- Added compatibility aliases for exported internal names that tests/importers still consume.

## Grep Gate

Command executed after bundle regeneration:

```powershell
git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs
```

Result count: `954`.

Residuals were audited under this allowlist:

- Generated bundle route manifest/source paths containing `vendor/hermes-2.3.0` and generated asset module names.
- Compatibility API routes and storage keys: `/api/hermes-*`, `x-hermes-*`, `hermes-workspace-*`, `application/x-hermes-*`.
- Environment shim and filesystem compatibility: `HERMES_*`, `.hermes`, `hermes-agent`, `hermes` binary, `hermes-*` tmux/session/profile names.
- Internal identifiers and non-rendered compatibility aliases: variables/functions/types such as `hermesCount`, `HERMES_BASE`, `buildHermesTmuxLaunchCommand`, `buildHermesActivitySummary`.
- Upstream provenance links and docs URLs intentionally preserved for merge/license traceability.
- Test files and expected fixtures under `vendor/hermes-2.3.0/src/**/*.test.*`, kept to validate compatibility behavior.
- Non-user-facing asset/file identifiers such as `hermes-world-*`, avatar IDs, and generated bundle module labels.

No known remaining user-facing plain Hermes branding outside those categories.

## Gates

Product gates:

- `node --check scripts/run-product-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/src/server/gateway-capabilities.ts`: PASS.
- `git diff --check`: PASS, with CRLF normalization warnings only.
- `corepack pnpm --dir vendor/hermes-2.3.0 build`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 electron:bundle-server`: PASS.
- `npm test`: PASS, 83 files / 562 tests.
- Clean clone `npm test`: PASS, 83 files / 562 tests, duration 254.96s.

Protocol delivery gates to be run after ledger release in this coordination commit:

- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"`

## Reviewer Notes

- I preserved upstream Hermes compatibility strings intentionally. The current task DoD is about visible user branding, not internal package/binary/app ID renames.
- The original ACTION message remains in `mailbox/open/`; Codex does not have orchestrator mailbox-archive capability.
