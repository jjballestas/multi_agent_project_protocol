---
handoff_id: HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2
task_id: TASK-0153
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-22
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 5cb8910
---

# TASK-0153 External CLI Rework - Handoff Codex to Arquitecto

## Result
- Product commit: `5cb8910 test(intake): allowlist spawned egress commands`.
- `external-cli` now uses an explicit spawned-binary allowlist: `git`, `python`.
- The guard flags any literal first argument outside that allowlist for `execFile`, `execFileAsync`,
  `execFileSync`, `spawn`, and `spawnSync`.
- Positive controls cover `powershell`, `sh`, `bash`, `cmd`, `curl`, `wget`; allowed controls cover
  `git` and `python`.
- Real `src/**` remains clean.

## Evidence
- `node --check tests/staticContract.test.js`: PASS.
- Product `git diff --check`: PASS.
- Product `npm test`: PASS 44/44.
- Clean clone product `npm test`: PASS 44/44.

## Notes
- Change is scoped to `D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js`.
- No live extractor use was enabled. Off-by-default remains intact.
- `protocol.config.json`, `chain_manifest.json`, genesis, registry, keys and secrets were not touched.
