---
handoff_id: HANDOFF-TASK-0155-AC52-codex-to-arquitecto-2
task_id: TASK-0155
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-22T15:10:00Z
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 6369b5c
---

# TASK-0155 AC52 rework - strict loopback canonicalization

## Change
- Product commit: `6369b5c fix(intake): enforce strict loopback host syntax`.
- `src/server.js` now validates the raw endpoint host before `URL` canonicalization.
- Accepted local-vlm hosts are only:
  - `localhost`
  - dotted-decimal IPv4 in `127.0.0.0/8` without ambiguous leading-zero/octal/hex/integer notation
  - `::1` / `[::1]`
- Rejected family now covered by behavior test:
  - `2130706433`
  - `0177.0.0.1`
  - `0x7f.0.0.1`
  - `0x7f000001`
  - `0.0.0.0`
  - `8.8.8.8`
  - `evil.com`
  - `127.0.0.1.evil.com`
  - `[::ffff:8.8.8.8]`
  - `127.000.000.001`
- Positive control now covers `localhost`, `127.0.0.1`, `127.0.0.5`, and `[::1]`.

## Evidence
- Product `node --check src/server.js`: PASS.
- Product `node --check tests/staticContract.test.js`: PASS.
- Product `node --check public/app.js`: PASS.
- Product `git diff --check`: PASS.
- Product `npm test`: PASS, 48/48.
- Clean-clone product `npm test`: PASS, 48/48.
- Protocol `python scripts/scan_encoding.py --root .`: PASS.
- Protocol `python scripts/scan_domain_neutrality.py --root .`: PASS.
- Protocol drift: `has_drift=false`, `up_to_seq=1193` before delivery claim, hot/replay hashes equal.
- Protocol `python scripts/validate_collaboration_state.py --root .`: PASS with unrelated warning for `MSG-20260622-Arquitecto-to-Operador-ESTADO-cola-vacia.md`.
- `validate_collaboration_state.py --with-secrets` is not supported by the current script interface.

## Notes
- No live local-vlm use was enabled.
- The original AC51/AC53 behavior remains covered by the existing local-vlm extractor test.
- Existing unrelated protocol dirty files were not touched: `.claude/settings.json`, `personal/Arquitecto/carril_A/CEREMONIA-extractor-runbook.md`, and `personal/operador/infografia_ux_intake_zeus_protocol.pdf`.
