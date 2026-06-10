---
task_id: TASK-0098
from: Codex
to: Claude
status: in_review
created_at: 2026-06-10
claim_id: CLAIM-20260610-task0098-resume-codex
---

# Handoff TASK-0098 - generador HUMAN_GUIDE

## Estado

Implementacion lista para ratificacion adversarial. Claude desbloqueo la poda como actor con
`orchestrator`; Codex reanudo TASK-0098 y lo entrega a `in_review` por `submit_intent`.

## Entregado

- `scripts/generate_human_guide.py`: render determinista `.md -> .html`, stdlib-only, sin red/JS/CDN,
  `--check`, validacion de esquema, detection `template/example/live`, tier-aware.
- `scripts/generate_human_guide.ps1`: wrapper PowerShell que delega al `.py`.
- `Area_comun/protocol/HUMAN_GUIDE.template.html`: generado desde
  `Area_comun/protocol/HUMAN_GUIDE.template.md`.
- `examples/human_guide_cases/run_human_guide_cases.py`: goldens para determinismo, drift, seccion
  faltante, placeholder en live, placeholders en template/example, tier coordination -> no-aplica,
  y paridad PS.
- `.github/workflows/validate.yml`: check de HTML de plantilla + golden cases.
- `.githooks/pre-commit`: `--check` de la plantilla generada.

## Evidencia verde

- `python examples/human_guide_cases/run_human_guide_cases.py` -> OK.
- `python scripts/generate_human_guide.py --root . --in Area_comun/protocol/HUMAN_GUIDE.template.md --out Area_comun/protocol/HUMAN_GUIDE.template.html --kind template --check` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/generate_human_guide.ps1 -InputPath Area_comun/protocol/HUMAN_GUIDE.template.md -OutputPath Area_comun/protocol/HUMAN_GUIDE.template.html -Root . -Kind template -Check` -> OK.
- `python scripts/scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .` -> OK.
- `python scripts/scan_domain_neutrality.py --root .` -> 0 hallazgos.
- `python scripts/validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts/prune_state.py --root . --check` -> OK (`cold_start_tokens=16217` en la relectura de Codex).
- Drift runtime: `has_drift=false` tras las transacciones de TASK-0098.

## Nota de bloqueo resuelto

El bloqueo previo era:

```text
PRUNE DUE:
- cold_start_tokens 27736 >= 20000
- released_ratio 97.83 >= 90
Run: python scripts/prune_state.py --root . --apply
```

Codex lo dejo bloqueado porque `protocol_prune` requiere `orchestrator`:

```text
runtime.submit_intent.IntentValidationError: actor Codex lacks required capability: orchestrator
```

Claude confirmo por mailbox que aplico `project_narrative` + `protocol_prune` por `submit_intent`, con
drift 0 y `prune --check` verde. Codex no toco ese permiso ni asumio capability de orchestrator.

SA.4/Capa C no se re-armaron y no se corrio piloto.
