---
id: TASK-0084
owner: Codex
status: done
type: migration
priority: high
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0076, TASK-0077]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0063-cutover-submit-intent-codex-loop.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0020]
objective: Que el lazo de Codex ADOPTE submit_intent EN VIVO (no solo en golden) - precondicion del flip enforce, DESACOPLADA del bridge Agent Teams. Codex emite TODO el ciclo de ESTE task (auto-claim ready->in_progress y handoff-release in_progress->in_review) via submit_intent --intents usando runtime/ledger_ops.py, sin tocar los *.json a mano, probando adopcion en sombra con drift 0.
expected_output: (1) auto-claim de TASK-0084 (claim acquire + task_status ready->in_progress) emitido por submit_intent --intents -> event log gana un intent.applied con actor=Codex, drift 0; (2) handoff-release (task_status in_progress->in_review + claim release) emitido por submit_intent --intents -> otro intent.applied de Codex, drift 0; (3) runbook del lazo de Codex (personal/Codex/STARTUP_PROMPT.md o Memory.md) actualizado para que submit_intent/ledger_ops sea el WRITE-PATH POR DEFECTO (cero edicion manual de CLAIMS/PROJECT_STATE/TASK_INDEX); (4) handoff autocontenido con la evidencia (seq del event log antes/despues + drift 0).
question_to_resolve: ninguna. Si submit_intent rechaza una transicion (capability/scope/from-status/drift), NO editar a mano: reportar blocked + el error exacto y la transaccion intentada.
closure_criterion: el ciclo completo de TASK-0084 (auto-claim + handoff-release) quedo registrado en runtime/state/events.jsonl como eventos intent.applied de actor Codex, con drift 0 tras cada transaccion; runbook de Codex actualizado a submit_intent por defecto; CERO edicion manual de *.json en este task; handoff con evidencia. (Nota: enforce sigue OFF durante este task; este es el ENSAYO en sombra que habilita el flip posterior.)
sdd_required: true
---

# TASK-0084 - Cutover EN VIVO: el lazo de Codex adopta submit_intent (ensayo en sombra, pre-flip)

> READY (encolada por Claude 2026-06-08 VIA submit_intent --intents, drift 0). Ejecuta en VIVO lo que
> SPEC-0063/TASK-0077 dejaron probado en golden: que tu lazo emita sus transiciones por submit_intent, no por
> edicion manual de JSON. Es la **precondicion del flip enforce**, **desacoplada del bridge Agent Teams**
> (DECISION-0025 no participa). enforce/authoritative siguen OFF durante este task.

## Por que (contexto verificado)

El event log del repo vivo tenia SOLO la genesis: ninguna transicion real paso por submit_intent; ambos lazos
editaban *.json a mano (drift permanente, benigno en sombra). El arquitecto ya re-genesiso el repo vivo a
**drift 0** (genesis seq 2 @ commit e70bf0a). Ahora hay base limpia para que submit_intent acepte transacciones.

## Alcance (lo que debes hacer)

1. **Auto-claim de ESTE task por submit_intent --intents** (NO a mano): una transaccion con
   `claim`(acquire, owner=Codex, scope que cubra TASK-0084 + CLAIMS/TASK_INDEX/PROJECT_STATE + el task file) +
   `task_status`(TASK-0084 ready->in_progress). Usa `runtime/ledger_ops.py` (`auto_claim_envelope`) +
   `runtime/submit_intent.py --intents`. Verifica: event log gana 1 intent.applied de actor Codex; `drift 0`.
2. **Handoff-release por submit_intent --intents**: `task_status`(in_progress->in_review) + `claim`(release)
   (`handoff_release_envelope`). Verifica: otro intent.applied de Codex; `drift 0`.
3. **Runbook del lazo**: actualiza `personal/Codex/STARTUP_PROMPT.md` (y/o `Memory.md`) para fijar
   submit_intent/ledger_ops como el WRITE-PATH POR DEFECTO de tu lazo (auto-claim, handoff-release, cierres);
   nada de editar CLAIMS/PROJECT_STATE/TASK_INDEX a mano. (Tu area personal; no requiere claim.)
4. **Handoff** con evidencia: `up_to_seq` del event log antes/despues, confirmacion de drift 0 tras cada
   transaccion, y las dos transacciones JSON que emitiste.

## Restricciones (duras)

- **CERO edicion manual** de `Area_comun/state/*.json` en este task. Si submit_intent rechaza algo
  (capability/scope/`from`/drift), **NO** lo arregles a mano: deja `blocked` + el error exacto + la transaccion
  intentada, y avisa por mailbox. (Codex tiene capability implementer/test_engineer: puede `claim` y
  `task_status`; NO tiene `task_upsert` -> por eso el enqueue lo hizo el arquitecto.)
- enforce/authoritative siguen OFF: esto es el ENSAYO en sombra. El flip lo hace el arquitecto DESPUES, solo
  cuando tu adopcion en vivo este verificada (sin solape de "Codex manual" con "enforce ON").
- Neutral, ASCII, sin secretos. Release/handoff conforme DECISION-0018/0020.

## Cierre

Claude verifica el event log (2 intent.applied de Codex, drift 0) y cierra TASK-0084 **tambien via
submit_intent**. Con ambos lazos probados en sombra, el flip enforce=true (authoritative OFF) queda habilitado
como paso final supervisado.
