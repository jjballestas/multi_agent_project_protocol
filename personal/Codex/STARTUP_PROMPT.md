# Startup Prompt For Next Session

You are Codex in `d:\Agentes\multi_agent_project_protocol`.

Start by reading:

1. `AGENTS.md`
2. `personal/Codex/Memory.md`
3. `Area_comun/state/PROJECT_STATE.json`
4. `Area_comun/state/TASK_INDEX.json`
5. `Area_comun/state/CLAIMS.json`
6. `Area_comun/mailbox/open/`

Context:

- The human approved/froze N-agent Phase 0.
- `DECISION-0015` is accepted and `SPEC-0038` is frozen.
- `TASK-0043` Phase 1 is accepted/done.
- `TASK-0044` Phase 2 is accepted/done.
- `TASK-0045` Phase 3 is ready for Codex.
- Private area is `personal/Codex/`; do not create files under legacy `Codex/`.

Immediate next action:

1. Check `git status --short`.
2. Read `Area_comun/mailbox/open/MSG-20260606-Claude-to-Codex-task0045-fase3.md`.
3. Read `Area_comun/tasks/TASK-0045-codex-n-agent-fase3-router.md`.
4. If no active claim blocks it, claim TASK-0045 and implement N-agent Phase 3:
   router weighted-least-loaded deterministic + capability routing + author exclusion for review/QA +
   fairness gate + routing explanation.

Important constraints:

- Keep fallback N=2 byte-equivalent.
- Current router cases must remain green.
- Use `routing_weights` from config, not hardcoded constants.
- If no reviewer/QA distinct from author is eligible, escalate with reason and candidates; never self-review.
- Fairness must be over eligible assignments and include anti-starvation.
- Apply liveness + handoff-release.
- Run the runtime regression suite and protocol gates before final answer.
