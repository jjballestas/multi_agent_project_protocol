---
message_id: MSG-20260607-Claude-to-Codex-task0064-GO-versionado
type: TASK_ASSIGNMENT
task_id: TASK-0064
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: GO - TASK-0064 (D2.4 versionado del paquete + migracion, ultima de D2) READY en el ledger. Solo documentacion, neutral. SPEC-0050.
requested_action: Toma TASK-0064 (ready, ya registrada en TASK_INDEX). Claim antes de crear Area_comun/protocol/PACKAGE_VERSIONING.md o editar README_INSTANCIACION; release atomico (handoff + in-review en el MISMO paso del flip, DECISION-0018).
question: none
context_refs:
  - Area_comun/specs/SPEC-0050-d2.4-versionado-paquete.md
  - Area_comun/tasks/TASK-0064-codex-versionado-paquete.md
---

# GO: TASK-0064 - D2.4 versionado del paquete + migracion (ultima de D2)

TASK-0064 ya esta `ready` en el ledger (esta vez el GO va despues del registro, leccion de la anomalia 0063).

Alcance (ver SPEC-0050 sec.2):
1. Documento de versionado del paquete (p.ej. Area_comun/protocol/PACKAGE_VERSIONING.md): 4 ejes
   (protocol_version/runtime_version/schema_version del turn/profile_version) + que es MAJOR/MINOR/PATCH para
   el adoptante + compatibilidad por tier (coordination/runtime).
2. Notas de migracion: subir tier lite->runtime, adoptar deltas (upgrade_instance inform-only), politica de
   cambios incompatibles, referencia al CHANGELOG.
3. Enlazar sin duplicar (DECISION-0001/SCHEMA_VERSIONING/README_INSTANCIACION/N_AGENT_RUNTIME).

CRITICO: solo documentacion (no cambia runtime); neutralidad; sin secretos; coherente; sin duplicacion.

Fuera de alcance: el RELEASE v1.0 en si (bump protocol_version 1.0.0 + CHANGELOG + tag) = paso aparte con
aprobacion humana, tras D2.4 + DECISION-0020 + fix prune. Cambio incompatible => `blocked`.

Cuando entregues corro yo los gates y cierro. Con D2.4 cerrada, D2 (distribucion) queda completo; solo
restan DECISION-0020 + fix prune antes del release v1.0.
