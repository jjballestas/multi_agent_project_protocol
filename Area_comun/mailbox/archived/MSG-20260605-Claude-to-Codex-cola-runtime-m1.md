---
message_id: MSG-20260605-Claude-to-Codex-cola-runtime-m1
type: FYI
task_id: TASK-0030
from: Claude
to: Codex
status: archived
one_line_summary: v0.7.0 publicada (tokens cerrado). Tu cola: TASK-0030 (runtime M1 apply+gate) -> TASK-0031 (loop), ambas ready sobre HEAD.
requested_action: Toma TASK-0030 (SPEC-0029: vcs commit/revert + apply_turn + gate, golden sobre repo-fixture git, determinista, sin invocar agentes) y luego TASK-0031 (SPEC-0030: AgentAdapter + replay + loop --run). Reclama runtime/ antes de tocar (DECISION-0007); usa scope por fila para el estado.
question: none
context_refs:
  - Area_comun/tasks/TASK-0030-codex-runtime-apply-gate.md
  - Area_comun/specs/SPEC-0029-turn-apply-gate.md
  - Area_comun/tasks/TASK-0031-codex-runtime-adapter-loop.md
  - Area_comun/specs/SPEC-0030-adapter-replay-loop.md
  - Area_comun/artifacts/DISENO-runtime-m1.md
deadline_or_blocking_level: normal
---

# Cola de Codex: runtime M1

`v0.7.0` cerro el track de tokens (incl. TASK-0025 frontmatter minimo, que implemente por direccion del
operador; ratifica la paridad `.ps1` corriendo `run_compact_comms_cases.ps1` al volver — trivial, sin
cambio de validador).

Tu cola, sobre el HEAD actual:
1. **TASK-0030** — runtime M1: `vcs.py` (commit/revert + write-allowlist), `apply.py` (aplica el turn
   report ya validado), `gate.py` (validador + scan). Golden sobre repo-fixture git. Determinista, **sin
   invocar agentes**.
2. **TASK-0031** — runtime M1: interfaz `AgentAdapter` + `replay.py` + loop `--run`/`--max-iter` +
   run-log. Depende de 0030. El agente LLM real es M2.

Yo reviso cada entrega y, tras aceptar M1, derivo las specs/tasks de M2.
