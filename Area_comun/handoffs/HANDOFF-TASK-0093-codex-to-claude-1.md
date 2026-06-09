---
handoff_id: HANDOFF-TASK-0093-codex-to-claude-1
task_id: TASK-0093
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-09
claim_id: CLAIM-20260609-task0093-codex
---

# HANDOFF TASK-0093 - claim acquire del orquestador

## Resumen

TASK-0093 queda listo para ratificacion adversarial de Claude. El cambio cierra el gap-8 off-pilot:
el paso `claim` del orquestador ya no es NO-OP; antes de invocar el adapter intenta adquirir el claim
del owner ruteado via `submit_intent` con `actor_id == owner`.

No se rearmo SA.4 y no se corrio piloto.

## Cambios principales

- `runtime/orchestrator.py`
  - Agrega `acquire_routed_claim` en el tramo `trace.append("claim")`.
  - Reusa claim activo owner+task si ya existe.
  - Adquiere por `submit_intent` si falta claim.
  - Rechaza el turno antes del adapter si `submit_intent` falla por conflicto de scope u otra regla.
  - Recarga estado y baseline dirty tras adquirir claim para que el commit del turno no mezcle la adquisicion.
- `runtime/adapters/llm_adapter.py`
  - El prompt deja claro que el orquestador ya adquirio el claim y que el LLM no debe reportar `transitions.claims`.
- `runtime/apply.py`
  - Inyecta release automatico del claim activo cuando el outcome/transition es terminal (`in_review`, `done`, `blocked` o `outcome=blocked`) y el report no lo trae.
  - Incluye rutas derivadas de transiciones en el set de paths a commitear.
- `examples/runtime_loop_cases/run_runtime_loop_cases.py`
  - Golden sin pre-claim: el orquestador adquiere claim, el turno aplica y el claim queda released tras outcome terminal.
  - Golden con pre-claim: no emite adquisicion nueva.
  - Golden con claim ajeno/conflictivo: rechaza antes del adapter y no commitea.

## Evidencia corrida por Codex

- `python -m py_compile runtime\orchestrator.py runtime\apply.py runtime\adapters\llm_adapter.py examples\runtime_loop_cases\run_runtime_loop_cases.py`
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> 11 casos OK
- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> 9 casos OK
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> 4 casos OK
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> 6 casos OK
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> 11 casos OK
- `python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py` -> 10 casos OK
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warnings de FYI archivables
- `python scripts\scan_domain_neutrality.py --root .` -> OK
- `python scripts\scan_encoding.py --root .` -> OK
- Drift check: `has_drift=false` antes de preparar este handoff.

Nota: los comandos no aprobados en esta sesion siguen afectados por `windows sandbox: spawn setup refresh`;
las gates anteriores se ejecutaron con elevacion cuando fue necesario. El operador pidio priorizar este
checkpoint antes de recuperar el sandbox.

## Puntos para ratificacion de Claude

- Confirmar que el scope derivado por `task_claim_scope` cubre el contrato esperado de SPEC-0070 sin
  sobre-extender mas de lo necesario.
- Confirmar que la reconciliacion elegida (prompt no reporta claims + `apply` release terminal automatico)
  evita doble-acquire y claim huerfano.
- Confirmar que el rechazo por claim ajeno ocurre antes del adapter y conserva cero commit.
- Confirmar que SA.4 sigue de-armado y que el smoke real end-to-end queda como paso posterior bajo GO
  separado del operador.

