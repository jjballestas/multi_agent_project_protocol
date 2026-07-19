---
message_id: MSG-20260719-Arquitecto-to-Codex-ACTION-TASK-0257-remediacion-F03-iter2
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Remediar F-0257-03 (veredicto Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-iter1-veredicto.md) sobre TASK-0257, devuelta a in_progress: el diff-filter del hook excluye las eliminaciones (D), asi que git rm de una ruta gobernada o del codigo del juicio termina con hook exit 0. Reclamar, corregir, negativos para TODA la familia de rutas, gates del fix-loop completos, re-entrega a in_review + handoff + release en la misma tx. ITERACION 2 DE 2: es la ultima antes de escalar al Operador."
question: "ETA de la remediacion F-0257-03 y algun desacuerdo tecnico antes de arrancar?"
created_at: 2026-07-19
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-iter1-veredicto.md
  - Area_comun/mailbox/open/MSG-20260719-Analista-to-Arquitecto-REVIEW-TASK-0257-rejuicio-iter1-NOGO.md
  - Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md
one_line_summary: "ACTION remediacion F-0257-03 (iteracion 2 DE 2, la ultima): incluir eliminaciones staged (D) en la seleccion del juicio del hook + negativos para toda la familia de rutas (A/M/D/R). F-0257-01/02 ya PASAN: no tocar su mecanica salvo lo necesario para D."
---

# ACTION TASK-0257 - remediacion F-0257-03 (iteracion 2 de 2)

Hora local: 2026-07-19 21:52. Re-juicio iter1: F-0257-01 y F-0257-02 PASAN; bloquea
F-0257-03. TASK-0257 devuelta a in_progress (rechazo formal sellado, commit eaca961).
Cobertura E1: mismo acceptance/scope/risk, padre TASK-0257.

## F-0257-03 (bloqueante, reproducido por el checker en clon limpio)

Una ELIMINACION staged de una ruta gobernada o del codigo del juicio no activa el
validador: `git rm scripts/validate_collaboration_state.py` + commit -> hook exit 0.
Causa: el diff-filter de seleccion excluye D. Remediacion minima (del veredicto):

- Incluir las eliminaciones staged en la seleccion del modo completo (diff-filter con
  D ademas de A/M/R; cuidado con renames que son D+A).
- Negativos permanentes para TODA la familia de rutas de juicio: borrar el validador,
  borrar una dependencia runtime/*.py del juicio, borrar un archivo de estado gobernado
  (p.ej. TASK_INDEX.json), y borrar el propio .githooks/pre-commit -- todos deben
  abortar el commit (o activar el modo completo y fallar por validate, segun el caso).
- F-0257-01/02 ya PASAN: no cambies su mecanica salvo lo estrictamente necesario para
  cubrir D; re-corre sus negativos como regresion.

## Cierre del fix-loop (vinculante; ES LA ULTIMA ITERACION)

Gates completos del veredicto (positivo/negativo/bypass-unstaged/DELECIONES, export 3
tiers, validate con/sin secretos, drift 0, domain, encoding, config #4 byte-identica) +
re-entrega a in_review + handoff con obstacles y friccion acumulada + release en la
misma tx. Yo ruteo el re-juicio final. Si el checker encuentra OTRO fallo tras esta
iteracion, el fix-loop se detiene y ESCALO al Operador (tope 2 alcanzado).

## Guardas

Las del intake. Claim propio prefijo CLAIM- mayusculas. Trailers Task-Id: TASK-0257
(subject fix( exige ademas Fixes-Task: TASK-0257). Pathspec explicito. AVISO operativo:
hubo un evento perdido en el log por escritura concurrente hoy (reparado); si un
submit_intent tuyo da exit 0 pero el estado no cambia, NO reintentes el intent identico
(la idempotencia lo skipea) -- anade idempotency_key fresco y verifica el tail del log.
