---
handoff_id: HANDOFF-TASK-0191-codex-to-arquitecto-1
task_id: TASK-0191
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-27
implementation_commit: 5f2d246
memory_commit: aac23c6
---

# HANDOFF TASK-0191 - Harness H1-H3

## Entregado

- `research/experiment_h1h3/harness.py`: runner reproducible con seed/K, fixtures desechables root-local, guard de
  byte-identidad para rutas vivas, inyeccion A1/A2/A3, medicion TPR/FPR/salud AC2, sobrecoste con-#4 vs sin-#4 y
  verificador externo solo-publicas.
- `research/experiment_h1h3/README.md`: uso y salidas.
- `examples/experiment_h1h3_cases/run_experiment_h1h3_cases.py`: golden AC1-AC6, incluyendo root vivo byte-identico
  y reproducibilidad misma seed/K.
- `.github/workflows/validate.yml`: agrega el golden del harness a CI.

## Evidencia

- `python -m py_compile research\experiment_h1h3\harness.py examples\experiment_h1h3_cases\run_experiment_h1h3_cases.py` PASS.
- `python examples\experiment_h1h3_cases\run_experiment_h1h3_cases.py` PASS 2/2.
- `python examples\attestation_negative_cases\run_attestation_negative_cases.py` PASS 6/6.
- `python examples\actor_auth_ed25519_cases\run_actor_auth_ed25519_cases.py` PASS 5/5.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .` PASS.
- Drift/#4 byte-identica antes de entrega: `has_drift=false`, `up_to_seq=2149`.

## Notas de revision

- El harness no ejecuta la medicion sobre dataset real; solo construye el aparato y sus goldens sobre fixtures/copias.
- Las metricas de latencia son estimaciones deterministicas derivadas del tamano serializado para preservar
  reproducibilidad exacta en CI. El tamano por evento se mide sobre eventos realmente escritos en copia desechable.
- `pwsh` no esta instalado en esta maquina; el gate PowerShell se ejecuto con `powershell`.
