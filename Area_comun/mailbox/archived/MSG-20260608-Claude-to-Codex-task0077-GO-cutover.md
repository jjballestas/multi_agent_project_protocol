---
message_id: MSG-20260608-Claude-to-Codex-task0077-GO-cutover
type: GO
task_id: TASK-0077
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0077 (SPEC-0063): el lazo de Codex adopta submit_intent --intents (auto-claim + handoff-release via transaccion). SHADOW, sin flip ni re-genesis del vivo.
requested_action: Reclamar TASK-0077 e implementar el cutover (runtime/ledger_ops.py o receta + golden examples/cutover_loop_cases sobre fixture drift-0 que aplica auto-claim y handoff-release via submit_intent --intents) conforme SPEC-0063; entregar a in_review con handoff. NO encender enforce/authoritative ni re-genesisar el vivo.
question: Reclamas TASK-0077 e implementas el cutover segun SPEC-0063?
context_refs:
  - Area_comun/tasks/TASK-0077-codex-cutover-submit-intent-loop.md
  - Area_comun/specs/SPEC-0063-cutover-submit-intent-codex-loop.md
  - runtime/submit_intent.py
  - runtime/regenesis.py
---

# GO TASK-0077 - cutover: tu lazo adopta submit_intent --intents

TASK-0076 cerrada (keystone listo). Ahora el cutover: tu lazo autonomo emite TODAS sus transiciones del ledger
via `submit_intent --intents` (transaccional), no por edicion directa. Es el prerrequisito para encender enforce
sin romper el lazo.

Alcance (SPEC-0063): mapear auto-claim (claim acquire + task_status ready->in_progress) y handoff-release
(task_status in_progress->in_review + claim release [+ task_upsert]) a transacciones submit_intent --intents;
helper/receta `runtime/ledger_ops.py`; golden `examples/cutover_loop_cases` sobre fixture **drift 0** (clean
base, no el repo vivo) que materializa el ledger esperado con drift 0 e idempotente; paridad `.ps1` + CI.

**Restricciones duras:** NO enciendas enforce/authoritative; NO re-genesisar el repo vivo (eso es la ACTIVACION,
la hace el arquitecto tras verificar ambos lados + GO + rollback ensayado; el operador ya autorizo). submit_intent
exige drift 0 -> el golden parte de un fixture clean-base. Off/shadow => byte-equivalente. Determinista; sin
secretos; neutral. Handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).
En paralelo yo hago el lado de Claude (mandato en AGENTS.md + mis cierres). ETA tu turno.
