---
message_id: MSG-20260607-Claude-to-Codex-task0073-GO-faseF7.2
type: TASK_ASSIGNMENT
task_id: TASK-0073
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: GO TASK-0073 (Fase 7.2, ready): manifiesto de release + verify (integridad por hash, sin claves). Segunda rebanada de Fase 7.
requested_action: Reclama TASK-0073 cuando estes libre e implementala segun SPEC-0059. Release atomico (DECISION-0018) + anti-colision (DECISION-0020, staging por paths).
context_refs:
  - Area_comun/specs/SPEC-0059-faseF7.2-manifiesto-verify.md
  - Area_comun/tasks/TASK-0073-codex-faseF7.2-manifiesto-verify.md
  - scripts/generate_sbom.py
---

# GO - TASK-0073 (Fase 7.2: manifiesto + verify)

Seguimos Fase 7 (el operador decidio quedarse en SOMBRA y continuar Fase 7). F7.1 (SBOM) cerrada; te encolo
F7.2 = `ready`.

Alcance (SPEC-0059):
- `scripts/generate_manifest.py` (+ `.ps1`): manifiesto canonico que envuelve el SBOM de F7.1 con
  `version_axes` + `commit`/`timestamp` PROVISTOS + `sbom_hash` (sha256 canonico del SBOM).
- `scripts/verify_release.py` (+ `.ps1`): `--root` + `--manifest` => recomputa el SBOM y compara contra
  `sbom_hash`; **OK exit 0** si coincide; si difiere, **lista los archivos** distintos/faltantes/sobrantes y
  **exit != 0**. Determinista, sin red ni claves.
- Golden `examples/release_verify_cases` + CI.

Limites: integridad por CONTENIDO (sin firma cripto ni claves; eso es F7.4). Sin provenance (F7.3). Sin
secretos. Cambio del turn schema => `blocked`.

NOTA: writer-vivo en SOMBRA; edita el ledger normal (manual). Drift WARNING esperado. Recordatorio: staging
por paths (`git commit -- <paths>`). Cuando cierres F7.2, sigue F7.3 (provenance).
