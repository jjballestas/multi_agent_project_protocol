# HANDOFF TASK-0100 - Codex to Claude

Date: 2026-06-14
Owner: Codex
Status: in_review

## Summary

Implemented the DECISION-0037 rescope for TASK-0100. The release LF guarantee is now forward-looking
(`v1.2.0+`), while `v1.1.0` remains signed and unchanged as a documented historical release with integrity
debt.

## Changed

- Added root `.gitattributes` with `* text=auto eol=lf` and explicit binary patterns.
- Added `dist/v1.1.0/KNOWN_LIMITATIONS.md` documenting the v1.1.0 limitations without euphemism:
  616 LF / 127 CRLF / 14 non-EOL mismatches, dirty-tree manifest generation, `runtime/protocol_replay.py`
  irreproducible from refs, and `verify.integrity.json ok:true` as emitter-local verification only.
- Added a DECISION-0037 amendment note to `SPEC-0075`, correcting the false v1.1.0 premise and scoping the
  spec to future releases.
- Updated `scripts/verify_release.py` to emit a `release_scope` note for pre-LF-normalization protocol
  release `1.1.0`. This does not change `ok`, does not hide diffs, and does not touch the signed manifest.
- Extended `examples/release_verify_cases/run_release_verify_cases.py` with a future-release smoke: a temp
  git repo with `.gitattributes`, `core.autocrlf=true`, forced checkout, LF byte assertion, and
  `verify_release ok:true`.

## Evidence

- Clean HEAD renormalize guard in temp clone with only `.gitattributes`: staged paths = `.gitattributes`
  only.
- `python examples\release_verify_cases\run_release_verify_cases.py` -> OK, 7 cases.
- `python scripts\verify_release.py --root . --manifest dist\v1.1.0\manifest.json` -> exit 1 as expected
  for current tree vs v1.1.0; payload includes `release_scope` and still reports full diff.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- Runtime drift check -> `has_drift:false`.

## Notes for review

- I did not regenerate, re-sign, or edit `dist/v1.1.0/manifest.json`, `signature.json`,
  `cosign.bundle.json`, `provenance.json`, `sbom.json`, `verify.integrity.json`, or
  `verify.provenance.json`.
- The `verify_release` pin is informational and structural: it makes the v1.1.0 exclusion visible in the
  verifier output while preserving failure semantics.
- PATCH bump and CHANGELOG are intentionally left for the architect close, per the GO.
