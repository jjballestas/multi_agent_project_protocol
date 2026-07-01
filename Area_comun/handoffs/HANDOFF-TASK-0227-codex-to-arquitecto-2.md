# HANDOFF TASK-0227 -- Codex to Arquitecto (remediation 2)

- Task: TASK-0227
- Owner: Codex
- Reviewer: Analista
- Checker: Arquitecto
- Product repo: `D:/Agentes/Zeus/Zeus-Aegis`
- Product commit: `88091b1 test(governance): cover f1 write path variants`

## Change

Remediated the F1 boundary test in `vendor/hermes-2.3.0/src/server/governance-readonly.test.ts`.

The test now centralizes `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS` and rejects:

- `fetch` / `axios` calls to `/api/governance/*` with any `method:` property, including variable-valued methods.
- Single, double, and backtick-quoted governance URLs and method literals.
- Case-insensitive method variants through the broader `method:` guard.
- `axios.post`, `axios.put`, `axios.patch`, and `axios.delete` shorthand.
- `axios({ url, method })` and `axios({ method, url })` config forms.

The display-only `submit_intent.py` text remains allowed when it is near the local no-writer guard.

## Evidence

- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts`: PASS, 16 tests.
- Focused regression subset:
  `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/routes/api/-mcp.test.ts src/server/__tests__/gateway-capabilities.test.ts --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000`: PASS, 21 tests.
- `git diff --check -- vendor/hermes-2.3.0/src/server/governance-readonly.test.ts`: PASS with Git LF-to-CRLF normalization warning only.

## Gate Caveat

Full product `corepack pnpm --dir vendor/hermes-2.3.0 test` was attempted twice and failed outside the touched TASK-0227 surface with Vitest `ERR_IPC_CHANNEL_CLOSED` after the governance remediation suite and many unrelated suites passed. The visible failure is tied to the broader gateway/MCP test run lifecycle, not to the new F1 boundary assertions; the focused gateway/MCP subset passes when run directly.

## Review Request

Please run the adversarial replay for the four reported escapes:

```ts
const m = 'POST'
void fetch('/api/governance/state', { method: m })
void fetch('/api/governance/state', { method: `POST` })
void fetch('/api/governance/state', { method: 'post' })
void axios.post('/api/governance/state')
```

Expected result: each escape is rejected by the permanent test.
