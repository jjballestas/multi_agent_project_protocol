# Neutrality scan validation cases

Golden cases for `scripts/scan_domain_neutrality.py` and `.ps1`.

- `clean`: expected exit `0`.
- `domain_term_in_core`: expected exit `1` because a denylisted term appears in `AGENTS.template.md`.
- `runtime_state_exempt`: expected exit `0` because generated `runtime/state/**` is exempt.
- `runtime_source_still_scanned`: expected exit `1` because runtime source files remain scanned.

Run with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1
```
