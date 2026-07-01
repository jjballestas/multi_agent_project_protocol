# HANDOFF TASK-0227 - Codex -> Arquitecto (remediacion-4 final)

- Task: `TASK-0227`
- Owner: `Codex`
- Reviewer/checker: `Analista` / `Arquitecto`
- Product repo: `D:/Agentes/Zeus/Zeus-Aegis`
- Product commit: `534b95e test(governance): cover final f1 write variants`
- Protocol delivery: this handoff plus mailbox `MSG-20260701-Codex-to-Arquitecto-TASK-0227-remediation-4-in-review.md`

## Cambio

`vendor/hermes-2.3.0/src/server/governance-readonly.test.ts` adds permanent negative coverage for the three final DECISION-0079 enumerable F1 write signatures:

1. local options object with `method` passed to `fetch('/api/governance/*', opts)`;
2. `fetch(new Request('/api/governance/*', { method: ... }))`;
3. positional `axios.request('/api/governance/*', { method: ... })`.

The existing negative cases and display-only `submit_intent.py` allowance remain intact.

## Evidence

- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts`: PASS, 16 tests.
- Local product `npm test`: PASS, 82 files / 559 tests.
- Clean clone `C:/Users/johnb/AppData/Local/Temp/codex-0227-rem4-zeus-aegis-clean` `npm test`: PASS, 82 files / 559 tests.
- `git diff --check`: PASS with Git LF-to-CRLF working-copy warning only.

## Notes

DECISION-0079 explicitly leaves runtime-built, non-enumerable dataflow outside the static guard. The residual read-only guarantee remains the backend governance endpoint contract plus review.
