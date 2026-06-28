# ANALISTA TASK-0208 re-pass waiver guard verdict

Firma: Analista

## Verdict

REFUTADO / CAMBIO-REQUERIDO. TASK-0208 is not closable on Zeus-Aegis `b47b707e142618231aa095c6cb82418df1b69c9f`.

The clean clone gate is green and the previous transitive vector is fixed, but the graph guard still has at least two falsable bypasses requested by the review prompt: case-variant first-party imports on Windows and query/suffix imports. A governance panel file can reach `src/lib/i18n` while `collectGovernanceWaiverViolations` returns no violation.

## Canonical anchor

| Item | Value |
| --- | --- |
| Protocol instruction HEAD | `62cea00933295b84deef5f40801134cfcff8ee63` |
| Review request | `Area_comun/mailbox/open/MSG-20260628-Arquitecto-to-Analista-REPASS-TASK-0208.md` |
| Product repo | `D:/Agentes/Zeus/Zeus-Aegis` |
| Product commit tested | `b47b707e142618231aa095c6cb82418df1b69c9f` |
| Clean clone | `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-d3df3cd6f1a74ac798975b8c55c7be28` |

## Reproduction

| Gate / probe | Command | Exit |
| --- | --- | ---: |
| Product clean clone full gate | `npm test` at Zeus-Aegis clean clone `b47b707e142618231aa095c6cb82418df1b69c9f` | 0 |
| F0 wrapper rerun | `node scripts/zeus-aegis-f0-test.mjs` under `vendor/hermes-2.3.0` | 0 |
| Excluded upstream 11 files | `corepack pnpm exec vitest run --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000 <11 files>` | 1 |
| Protocol validator | `python scripts/validate_collaboration_state.py` | 0 |
| Domain neutrality | `python scripts/scan_domain_neutrality.py` | 0 |
| Encoding | `python scripts/scan_encoding.py` | 0 |
| Drift | `protocol_state_drift(Path("."))` | `has_drift=False`, `up_to_seq=2413` |
| #4 config | `Get-FileHash protocol.config.json -Algorithm SHA256` | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

Full gate facts:

- `npm test` exited 0 in the clean clone.
- F0 wrapper rerun exited 0 with `82 passed` test files and `548 passed` tests.
- Running the 11 excluded files directly exited 1 with `24 failed | 44 passed (68)`, matching the waiver count and list.

## Vector table

| Vector / AC | Result | Evidence |
| --- | --- | --- |
| Full product gate at cited commit | PASA | Clean clone `npm test` exit 0. |
| Excluded count and list | PASA | Direct run of the 11 excluded files: exit 1, 24 failed, 44 passed, 68 total. |
| Previous transitive vector `governance.tsx -> intermediate -> ../lib/i18n` | PASA | Synthetic regression in `governance-waiver.test.ts` returns `src/routes/governance-waiver-transitive.ts reaches ../lib/i18n (src/lib/i18n)`. |
| Alias import `@/lib/i18n` | PASA | My extracted guard probe returns BLOCKED. |
| `src/` import `src/lib/i18n` | PASA | My extracted guard probe returns BLOCKED. |
| Dynamic import `import("../lib/i18n")` | PASA | My extracted guard probe returns BLOCKED. |
| `require("../lib/i18n")` | PASA | My extracted guard probe returns BLOCKED. |
| Re-export `export * from "../lib/i18n"` | PASA | My extracted guard probe returns BLOCKED. |
| Barrel/index indirection `governance.tsx -> ../lib -> ./i18n` | PASA | My extracted guard probe returns BLOCKED at `src/lib/index.ts`. |
| Extension-explicit import `../lib/i18n.ts` | PASA | My extracted guard probe returns BLOCKED. |
| Case-variant Windows import `../lib/I18N` | SLIPS | On this Windows clone `fs.existsSync("src/lib/I18N.ts")` is true, but the guard compares against lower-case `src/lib/i18n` and returns `[]`. |
| Query/suffix import `../lib/i18n?raw` | SLIPS | The guard resolves `src/lib/i18n?raw`; it is neither equal to `src/lib/i18n` nor under `src/lib/i18n/`, so it returns `[]`. |
| SEAMS served-surface honesty | PASA with residual | `chat-message-list`, `context-usage`, `swarm2-screen`, and `chat-composer-context-controls` are now labelled as served product or not F0-certified, not harmless test-rot. |
| SEAMS current evidence consistency | RISK DECLARED | `docs/SEAMS.md` still says latest F0 evidence is `79` files / `533` tests, while my cited F0 run at `b47b707` reports `82` files / `548` tests. Not the primary blocker, but stale closure evidence should be corrected if the task is touched again. |

## Falsable blocker

The guard normalizes slash direction and strips file extensions, but it does not canonicalize case or strip allowed bundler query/suffix markers before comparing a resolved first-party import against `waivedSurfaceModules`.

Exact extracted-guard probe output:

```text
direct-lower: BLOCKED ["src/routes/governance.tsx reaches ../lib/i18n (src/lib/i18n)"]
case-variant-windows: SLIP []
query-suffix: SLIP []
alias-lower: BLOCKED ["src/routes/governance.tsx reaches @/lib/i18n (src/lib/i18n)"]
src-lower: BLOCKED ["src/routes/governance.tsx reaches src/lib/i18n (src/lib/i18n)"]
dynamic-lower: BLOCKED ["src/routes/governance.tsx reaches ../lib/i18n (src/lib/i18n)"]
require-lower: BLOCKED ["src/routes/governance.tsx reaches ../lib/i18n (src/lib/i18n)"]
export-star-lower: BLOCKED ["src/routes/governance.tsx reaches ../lib/i18n (src/lib/i18n)"]
barrel-index: BLOCKED ["src/lib/index.ts reaches ./i18n (src/lib/i18n)"]
extension-explicit: BLOCKED ["src/routes/governance.tsx reaches ../lib/i18n.ts (src/lib/i18n)"]
```

Windows filesystem check:

```text
exists src/lib/i18n.ts true
exists src/lib/I18N.ts true
```

## Required change

Normalize resolved first-party module specifiers to the comparison domain before the waived-surface check:

- Strip query/hash suffixes such as `?raw`, `?worker`, `#...` before path comparison.
- Compare against waived modules using a case-normalized form at least on Windows, or fail closed on any import whose resolved path differs from the real source path only by case.
- Add permanent negative tests for `../lib/I18N` and `../lib/i18n?raw` (or reject query/suffix first-party imports in panel files if that is the intended policy).

## Recommendation

CAMBIO-REQUERIDO. Do not close TASK-0208 until the guard blocks the two slipping families above and SEAMS evidence is refreshed or explicitly scoped as historical.
