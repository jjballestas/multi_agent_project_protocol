---
handoff_id: HANDOFF-TASK-0080-codex-to-claude-1
task_id: TASK-0080
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0080 - SA.3 checkpoint humano

## Entrega

Implementado SPEC-0064 SA.3 en shadow, sin tocar el invoker real y sin encender autonomia:

- `protocol.config.json` y template mantienen `runtime.supervised_autonomy.enabled=false`, ahora con
  `caps.human_checkpoint_every_k=2`.
- `runtime/supervised_autonomy.py` valida `caps.human_checkpoint_every_k` como entero >= 1 solo bajo
  activacion supervisada registrada.
- El payload normalizado y el runreport incluyen `human_checkpoint_every_k`.
- `runtime/orchestrator.py` corta con `outcome=human_checkpoint` y `human_required=True` tras K turnos
  supervisados cuando queda trabajo por procesar; no hay auto-resume dentro de la misma invocacion.
- Los fix-cycles escalan a checkpoint humano al alcanzar `quality_policy.max_review_cycles` o
  `quality_policy.max_qa_cycles`, leyendo `review_attempts` / `qa_attempts` del estado ya aplicado.
- `examples/supervised_autonomy_cases` queda ampliado a 8 golden cases: max_turns, checkpoint por K turnos,
  checkpoint por fix-cycles, pausa, reloj, rechazo sin registro, off sin flag y cerrojo real intacto.

## Archivos tocados

- `protocol.config.json`
- `protocol.config.template.json`
- `runtime/orchestrator.py`
- `runtime/supervised_autonomy.py`
- `examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py`
- `Area_comun/tasks/TASK-0080-codex-autonomia-SA3-checkpoint-humano.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0079-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0080-GO-autonomia-SA3.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0080-in-review.md`
- `Area_comun/handoffs/HANDOFF-TASK-0080-codex-to-claude-1.md`

## Validacion ejecutada

- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK, 8 casos.
- `python -m py_compile runtime\orchestrator.py runtime\supervised_autonomy.py examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> OK.
- Suite funcional de CI ejecutada localmente -> OK: encoding, handoff-release, mailbox, prune, SDD, compact comms,
  neutrality cases, release/SBOM/provenance/sign, router, N-agent, property, concurrency, guardrails, tool policy,
  eventlog, protocol replay/materialize/enforce/genesis, intent flow/tx, cutover, auth, instantiation, upgrade,
  Review/QA, agent registry, turn schema/semantic, apply, loop, observability, budget, LLM adapter y real adapter.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift runtime.
- `powershell -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift runtime.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- `powershell -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> exit 0.
- `python scripts\prune_state.py --root . --apply` -> OK, `claims_archived=2`, `tasks_archived=1`,
  `next_actions_condensed=3`, `after_tokens=12700`.
- `python scripts\prune_state.py --root . --check` -> OK antes de liberar claim; tras liberar, prune se aplico como
  parte del cierre.
- `powershell -ExecutionPolicy Bypass -File scripts\prune_state.ps1 -Root . -Check` -> OK antes de liberar claim.

## Notas de revision

- El invoker real sigue rechazando subprocess multi-turno sin `--once`.
- Autonomia supervisada sigue off-by-default en config viva y template.
- El checkpoint por K turnos se emite despues de un turno verde y solo cuando quedan reportes dentro del limite
  supervisado; si el limite de `max_turns` se alcanza antes, gana `max_turns_reached`.
- Para fix-cycles no se agregan campos fuera del schema al turn report; se usa el estado aplicado.
- SA.4 (invoker real multi-turno bajo el sobre) queda gateada: no iniciar sin GO del operador y ensayo de rollback.
