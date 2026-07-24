# FAILURE_MODES.md - Named failure modes and their guardrails

> Source of truth: `AGENTS.md`. This catalog is part of the shipped, **domain-neutral** protocol.
>
> **What this is.** A named catalog of multi-agent failure modes mapped to the operational incidents
> this protocol has already mitigated and the guardrail that contains each one. It uses the **MAST**
> taxonomy (*Multi-Agent System failure Taxonomy*; Cemri et al., 2025, "Why Do Multi-Agent LLM Systems
> Fail?") as a shared **vocabulary** for naming the 14 failure modes.
>
> **What this is NOT (honesty boundary).** This is **MAST applied to this protocol's operational
> incidents**, not a claim of 1:1 equivalence with the MAST-Data dataset, and not an empirical study of
> the project history (that is a separate, deferred work item — "#1 / protocol_research" — which needs
> its own decision). Where a MAST mode has **no real incident** in this repository, the row says so
> plainly; we do not invent incidents to fill the table. The `Incident?` column states only whether a
> concrete incident is **cited** for that row or the guardrail is preventive-only; it is **not** a tally
> of incidents and carries no count, frequency or severity. Quantifying those is the deferred empirical
> work item (#1).
>
> **MAST is the vocabulary, not the whole surface.** This protocol also guards failure modes that are
> **outside MAST** and are not cataloged here: e.g. ASCII/encoding discipline for the mailbox/state
> channel (DECISION-0012), the domain-neutrality boundary, and secret-leak prevention (`AGENTS.md` §4).
> MAST names *multi-agent coordination* failures; these other modes are infrastructure/policy guards.
> This catalog is therefore **not an exhaustive failure surface** for the protocol.

## How to use this catalog

- **When something breaks:** find the row whose *symptom* matches, read the *guardrail*, and follow the
  referenced decision/mechanism. If no row matches, you may have found a new mode — open a `discovery`
  task and propose an addition by decision.
- **When designing new automation:** before building a loop/scanner, also run the loop governor
  ("Does it deserve a loop?") in [`TASK_PROTOCOL.md`](TASK_PROTOCOL.md).
- **Scope of "guardrail":** a guardrail here is a protocol rule and/or a runtime mechanism that
  *prevents, detects, or contains* the mode. Many are off-by-default capabilities; the catalog names the
  guardrail regardless of whether this live instance has it enabled.

## Reference key

References point to the canonical artifact that defines the guardrail:
`DECISION-00xx` = `Area_comun/decisions/`; `TASK_PROTOCOL` / `AGENTS` = the contracts;
`runtime/*` = the runtime mechanism; `quality_policy` / `event_state` / `budget` = config blocks.

---

## 1. Specification and system-design failures

| MAST mode | Symptom in this protocol | Incident? | Guardrail (reference) |
|-----------|--------------------------|-----------|------------------------|
| **FM-1.1 Disobey task specification** | An agent emits output that does not satisfy the declared task contract (malformed turn, missing required SDD fields, deliverable that ignores `acceptance_criteria`). | **Guardrail, no own incident** (preventive) | Turn schema validation (`runtime/turn_schema.json` + `runtime/turn_validate.py`); SDD required fields and the review check against `spec_id`/`acceptance_criteria`/`test_plan`/`closure_criteria` (`TASK_PROTOCOL`). |
| **FM-1.2 Disobey role specification** | An agent acts outside its role: writing the shared ledger directly when only the runtime may (drift), or using a capability it does not hold. | **Incident cited**: pre-`enforce` manual-edit drift required a re-genesis to drift 0, which motivated the single-writer cutover. | Single-writer **mechanism**: `enforce` B.3 hard-gate rejects manual ledger edits as drift; all transitions go through `runtime/submit_intent.py` (DECISION-0017 drift, DECISION-0022/0028; `runtime/regenesis.py`). Capability/role separation: `agents[].capabilities` (architect != implementer), `runtime/tool_policy.py`. |
| **FM-1.3 Step repetition** | Redundant re-execution of an already-done step: duplicate turns, `run_log` accumulation, a `run_id` that collides across runs. | **Incident cited (once)**: `run_id` collision with the smoke run in the re-pilot. | Idempotency on ledger writes (`idempotency_key` in `submit_intent`, stable `subject_hash`). Observed in the re-pilot (`run_id` collision with the smoke run); the structural fix is tracked as **TASK-0096** (`run_id` unique per orchestrator run), still `proposed`. |
| **FM-1.4 Loss of conversation history** | Context lost across a cold start or a peer's prior work overwritten, so an agent re-derives or contradicts established state. | **Guardrail, no own incident** (preventive/by-design) | Self-contained handoffs (`AGENTS` §0/§7); slim views + cold-start reading order (DECISION-0030); golden post-commit memory so the next cold start reflects the just-committed reality (DECISION-0026). |
| **FM-1.5 Unaware of termination conditions** | An agent runs without a bound, or stalls silently while holding work, with no notion of when to stop or to yield. | **Incident cited**: silent-stall risk observed in semi-auto/overlapping windows motivated the liveness-signal rule. | Liveness rule — every work turn on an active claim must leave a verifiable signal (DECISION-0013, `TASK_PROTOCOL` handoff-release & liveness); preventive arm: budget/deadline caps (`runtime/budget.py`: soft/hard `cost_tokens`, `max_cost_tokens`, deadline). |

## 2. Inter-agent misalignment

| MAST mode | Symptom in this protocol | Incident? | Guardrail (reference) |
|-----------|--------------------------|-----------|------------------------|
| **FM-2.1 Conversation reset** | A multi-step exchange restarts and loses accumulated alignment, repeating earlier negotiation. | **No own incident** | Not observed as a distinct incident in this repo. Partially pre-empted by self-contained handoffs and the fixed cold-start reading order (`AGENTS` §0): an agent re-entering cold reconstructs state from artifacts rather than from chat history. |
| **FM-2.2 Fail to ask for clarification** | An agent proceeds on an ambiguous/inconsistent requirement instead of asking, inventing scope or acceptance criteria. | **Guardrail, no own incident** (preventive) | "Clarity before execution": ambiguity becomes `blocked` + **one concrete question** (DECISION-0005, `TASK_PROTOCOL`); escalation ladder `escalate_to_architect_before_human` (`quality_policy`). |
| **FM-2.3 Task derailment** | Work drifts off the agreed scope (scope creep beyond the claimed routes / pipeline). | **Guardrail, no own incident** (preventive) | Work only inside the claimed `scope` and the task `execution_pipeline`; one owner per task; review checks the result against `acceptance_criteria` (`TASK_PROTOCOL`). |
| **FM-2.4 Information withholding** | An agent detects an anomaly/inconsistency in shared state or a peer's work and does not surface it. | **Incident cited**: observed handoff/state anomalies motivated the mandatory-notification rule. | Mandatory anomaly notification: detector must notify the owner via `mailbox/open/` with one concrete, actionable message and record it; must not silently fix nor leave it unsignaled (DECISION-0018). |
| **FM-2.5 Ignored other agent's input** | An agent overwrites or ignores a peer's claim/work (e.g. clobbering a peer's ledger write in an overlapping window). | **Incident cited**: three observed concurrent-write failures (HALLAZGOS) across Phase 5.2/5.3, 6.x and D2.x. | Do not edit routes under another owner's active claim; anti-collision rule for concurrent ledger writes — prepare out of band, write only in a safe window, atomic ledger write, explicit-path staging (DECISION-0020). |
| **FM-2.6 Reasoning-action mismatch** | An agent's stated reasoning and its actual action diverge (claims to do X, does Y). | **No own incident** | Not observed as a distinct incident here. Partially mitigated by structure: minimal-narration addendum makes the **deliverable/handoff authoritative over narration** (DECISION-0005 addendum 2026-06-13), and structured turns/intents constrain action to declared scope. |

## 3. Task verification and termination

| MAST mode | Symptom in this protocol | Incident? | Guardrail (reference) |
|-----------|--------------------------|-----------|------------------------|
| **FM-3.1 Premature termination** | A task is closed before it is actually complete: e.g. the "done/in_review" message is written but the state transition (status flip + claim release) did not land. | **Incident cited**: incomplete handoff-release (message written, state not transitioned) observed and codified as an anomaly. | Handoff-release atomicity — the message and the state transition must land together; an in_review/done task must not retain an active claim (DECISION-0018, `TASK_PROTOCOL`); `closure_criteria` required before close. |
| **FM-3.2 No or incomplete verification** | Output committed without adequate checking: an undeclared dirty tree, a half-written snapshot, or skipped gates. | **Incident cited**: orchestrator turn left the task `.md` dirty in the re-pilot (TASK-0091/TASK-0095). | Green gates before commit; explicit-path staging and a consistent snapshot, never broad `add -A` (DECISION-0020 #5); validator must be green; `test_plan` required by SDD. |
| **FM-3.3 Incorrect verification** | Verification happens but is unsound — most often an agent verifying its own work (maker == checker). | **Guardrail, no own incident** (preventive) | Maker != checker enforced: `allow_self_review:false`, `allow_self_qa:false` (`quality_policy`); two-part close (implementer `in_progress -> in_review`, architect `in_review -> done`); adversarial review voices (DECISION-0031), architect closes analysis tasks (DECISION-0032). |

---

## Coverage summary (honest)

- **14 / 14 MAST modes named**, each with a guardrail (preventive and/or detective).
- Each row's `Incident?` cell states only whether a **concrete incident is cited** for that mode or the
  guardrail is **preventive-only**. This is deliberately **not** a count: no tally, frequency or
  severity is asserted. FM-1.3 is cited as a single observed occurrence (structural fix `proposed` in
  TASK-0096); FM-2.1 and FM-2.6 have **no own incident** and are only partially pre-empted by structure.
- Quantifying frequency/severity across the project history is the deferred empirical work item
  (#1 / protocol_research) and requires its own decision. This catalog is qualitative.
- MAST is the vocabulary, not the whole failure surface: non-MAST guards (encoding/DECISION-0012,
  domain-neutrality, secrets) live in their own contracts and are out of scope here.

## Maintenance

This file ships with the protocol and is versioned with it. Adding, removing or re-mapping a row is a
protocol change and requires an append-only decision in `Area_comun/decisions/`.
