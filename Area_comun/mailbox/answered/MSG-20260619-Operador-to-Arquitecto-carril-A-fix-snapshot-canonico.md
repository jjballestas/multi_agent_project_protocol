---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-fix-snapshot-canonico
type: CHANGES
task_id: TASK-0117
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: Verificacion post-push: #4 ON y SANO (chain/firmas/anclaje validos, drift 0, provenance/sello correctos, TASK-0117 done) - NO rollback. PERO el commit canonico 7a43439 NO pasa su propio validate_collaboration_state desde CLON LIMPIO: assert_snapshot_matches falla porque el snapshot del head (snapshots/215806be....json) NO esta commiteado (existe en tu working tree, no en canonico). Fix-forward: commitear el snapshot faltante + revalidar desde clon fresco.
requested_action: "Fix-forward (no rollback): (1) commitear el snapshot del head faltante runtime/state/snapshots/215806be... .json (o re-materializar + refrescar snapshot.json) y push; (2) VERIFICAR validate_collaboration_state.py --root . = exit 0 desde un CLON FRESCO (no tu working tree); (3) reportar el nuevo HEAD canonico. No reactivar Carril B hasta que esto este verde + mi confirmacion. #4 sigue ON."
question: "Confirmas el fix-forward (commitear el snapshot del head + revalidar desde clon limpio exit 0) y reportas el nuevo HEAD? #4 se queda ON (no rollback)."
context_refs:
  - Area_comun/decisions/DECISION-0045-boundary-t0-sello-pre-t0.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
validation_refs:
  - "Verificado por el asistente sobre 7a43439 (clon fresco /tmp, blobs crudos byte-identicos): chain valid (validate_chain, 8 ev), agent signatures valid, anchors valid, protocol_state_drift has_drift=False (drift 0), genesis prev_hash==canonical_hash(config), sha256 sello==pre_t0_provenance (7e2452ae), TASK-0117 done, 4 flags true, cfg=ps=1.14.0. FALLO unico: validate_collaboration_state --root . exit 1 'snapshot mismatch: state hash differs' (assert_snapshot_matches); snapshot.json.canonical_hash=215806bea5c6453fdb34baef... NO esta entre los 11 snapshots committeados en runtime/state/snapshots/."
deadline_or_blocking_level: blocking
---

# #4 ON y sano, pero canonico no se auto-valida en clon limpio - fix-forward

Hice de "clon fresco / CI" sobre 7a43439 (blobs crudos, byte-identicos).

## Verde (coincide con tu reporte) - #4 ON y SOLIDO, sin rollback
- 4 flags true, cfg=ps=1.14.0, TASK-0117 done.
- `validate_chain` valid (8 ev) + firmas validas + anclas validas.
- `protocol_state_drift` **has_drift=False** (drift 0 real: replay reproduce el estado vivo).
- genesis `prev_hash == canonical_hash(config)`; sha256 del sello == `pre_t0_provenance` (7e2452ae);
  `chain_manifest` presente. El boundary T0 es solido.

## Defecto (incompletitud del commit, no corrupcion)
`validate_collaboration_state.py --root .` desde **clon limpio** da **exit 1: "snapshot mismatch: state
hash differs"** (`assert_snapshot_matches`). Causa: `snapshot.json` apunta a `canonical_hash =
215806be...`, pero `runtime/state/snapshots/215806be...json` **NO esta commiteado** (hay 11 snapshots,
ese no). Existe en tu working tree -> tu `validate` dio verde; un **clon fresco de canonico no lo tiene**
-> CI / cualquier clon nuevo (incluido el patron "copia limpia" que usamos) falla el gate.

## Fix-forward (rapido, no rollback - #4 se queda ON)
1. Commitea el snapshot del head faltante `runtime/state/snapshots/215806be...json` (o re-materializa +
   refresca `snapshot.json`) y push.
2. **Revalida desde un CLON FRESCO** (no tu working tree): `validate_collaboration_state --root .` = exit 0.
3. Reporta el nuevo HEAD canonico.

## Leccion de proceso
El "drift 0 / verde" se valido en tu working tree (tenia el archivo). **Validar siempre desde clon limpio**
(misma clase que la divergencia vista-vs-canonico anterior). Eso fue lo que cazo esto.

Carril B sigue en PAUSA hasta que el clon-fresco pase verde + mi confirmacion. #4 ON. Canal ASCII.
