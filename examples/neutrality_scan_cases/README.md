# Neutrality scan validation cases

Golden cases for `scripts/scan_domain_neutrality.py` and `.ps1`.

- `clean`: expected exit `0`.
- `domain_term_in_core`: expected exit `1` because a denylisted term appears in `AGENTS.template.md`.

Run with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1
```
