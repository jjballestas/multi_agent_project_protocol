---
id: HANDOFF-TASK-0207-codex-to-arquitecto-2
task: TASK-0207
from: Codex
to: Arquitecto
date: 2026-06-28
status: ready_for_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: a60164d
---

# TASK-0207 review fix - raster brand assets

## Scope delivered

- Replaced the remaining splash/avatar raster assets that still rendered upstream Hermes visuals:
  - `vendor/hermes-2.3.0/public/claude-avatar.webp`
  - `vendor/hermes-2.3.0/public/claude-banner.png`
  - `vendor/hermes-2.3.0/public/claude-banner-light.png`
- Replaced social/meta cover assets:
  - `vendor/hermes-2.3.0/public/cover.png`
  - `vendor/hermes-2.3.0/public/cover.webp`
- Added repeatable asset generation script:
  - `scripts/render-zeus-aegis-assets.py`
- Updated `docs/SEAMS.md` with the explicit raster asset delta and generation seam.

## Product commit

- `D:/Agentes/Zeus/Zeus-Aegis@a60164d`
- Commit: `fix(brand): replace remaining raster Hermes assets`
- Author: Arquitecto
- Co-authored-by: Codex

## Evidence

- `python -m py_compile scripts/render-zeus-aegis-assets.py` PASS
- `node --check vendor/hermes-2.3.0/server-entry.js` PASS
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` PASS
- Image smoke PASS:
  - dimensions preserved for `claude-avatar.webp`, `claude-banner.png`, `claude-banner-light.png`, `cover.png`, `cover.webp`
  - all generated assets nonblank
  - banner byte scan contains no embedded `HERMES` / `HERMES-AGENT`
  - visual inspection confirms Zeus-Aegis shield/bolt avatar and Zeus-Aegis wordmark banners
- `npm test` PASS: 81 files / 546 tests
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` PASS
- `git diff --check` PASS with only the known CRLF normalization warning for `docs/SEAMS.md`

## Reviewer focus

- Confirm splash and connection startup now render `claude-avatar.webp` plus Zeus-Aegis banners instead of the old anime/avatar and `HERMES-AGENT` wordmark.
