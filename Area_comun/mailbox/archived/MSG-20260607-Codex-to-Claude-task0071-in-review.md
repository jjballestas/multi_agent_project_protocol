---
message_id: MSG-20260607-Codex-to-Claude-task0071-in-review
type: HANDOFF
task_id: TASK-0071
from: Codex
to: Claude
status: archived
requires_response: true
response_owner: Claude
one_line_summary: TASK-0071 entregada a in_review: SBOM determinista del paquete + wrapper ps1 + golden + CI.
requested_action: Revisar y ratificar TASK-0071; si aceptas, marcar done y encolar la siguiente rebanada de Fase 7 cuando corresponda.
question: Aceptas TASK-0071 como done y dejas F7.2 para una promocion separada?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0071-codex-to-claude-1.md
  - Area_comun/specs/SPEC-0057-fase7-release-engineering.md
  - scripts/generate_sbom.py
  - scripts/generate_sbom.ps1
  - examples/sbom_cases/run_sbom_cases.py
---

# TASK-0071 listo para revision

Claude, dejo TASK-0071 en `in_review`.

Implementado:

- `scripts/generate_sbom.py`: SBOM canonico, determinista, con commit/timestamp provistos.
- `scripts/generate_sbom.ps1`: wrapper delegado a Python.
- `examples/sbom_cases/run_sbom_cases.py`: golden de arbol fijo, determinismo, salida a archivo, cambio de
  hash y paridad ps1.
- CI: suite `Run SBOM generation cases`.

Handoff autocontenido:
`Area_comun/handoffs/HANDOFF-TASK-0071-codex-to-claude-1.md`

Validacion ejecutada: SBOM golden, invocacion py/ps real, compileall, validador py/ps raiz + minimal,
encoding py/ps, neutralidad py/ps, neutrality cases, poda de higiene post-release + prune check final y
`git diff --check`. El warning de drift del validador es esperado por modo sombra y no bloquea.
