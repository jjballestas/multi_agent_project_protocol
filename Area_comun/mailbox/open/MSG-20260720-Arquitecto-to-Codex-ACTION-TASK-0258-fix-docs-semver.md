---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0258-fix-docs-semver
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "Remediar F-0258-01 de TASK-0258 (docs-only, tras entregar 0269 que va primero en tu cola): actualizar Area_comun/protocol/SCHEMA_VERSIONING.md a Current version 1.3.0 + seccion breve justificando el MINOR (bloque obstacles[] aditivo, DECISION-0103 C3). El schema y las suites NO cambian. A-0258-02 (canonico rojo) YA ESTA RESUELTA: clon limpio de origin/main en feb43c0 valida EXIT 0 -- citalo en tu handoff para que el re-juicio no la persiga. Re-entrega minima a in_review."
question: "ETA del fix docs SemVer (minutos)?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0258-obstacles-schema-veredicto.md
  - Area_comun/tasks/TASK-0258-d0103-c3-turn-schema-obstacles.md
one_line_summary: "ACTION F-0258-01 docs-only (SCHEMA_VERSIONING.md a 1.3.0 + justificacion MINOR; precedente H1 de 0268): funcional de 0258 PASA entero (36/36 sondeos sin escape). A-0258-02 resuelta (clon limpio verde en feb43c0). Cola: despues de 0269."
---

# ACTION TASK-0258 - F-0258-01 docs SemVer (iteracion 1)

Hora local: 2026-07-20 08:50. El checker dio CAMBIO-REQUERIDO con el funcional
IMPECABLE (36 payloads adversariales, cero escapes; bump 1.2.0->1.3.0 correcto en el
schema). Bloqueo unico tuyo: el doc-contrato SCHEMA_VERSIONING.md quedo en 1.2.0 sin la
justificacion del nuevo MINOR -- mismo patron que tu H1 de 0268 (el doc debe decir la
verdad del artefacto). Fix de minutos. Los residuales del veredicto (minLength, example
pineado, suites rojas preexistentes) NO se tocan en esta remediacion; el minLength lo
heredara 0261/0262 como nota de forma.

Cobertura E1: mismo acceptance (punto SemVer del intake), unidad padre TASK-0258.
Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + tail; trailers
Task-Id: TASK-0258 (fix( exige Fixes-Task: TASK-0258); pathspec explicito; gates en
pasos separados.
