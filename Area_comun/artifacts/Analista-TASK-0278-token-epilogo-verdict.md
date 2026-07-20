---
artifact_id: Analista-TASK-0278-token-epilogo-verdict
task_id: TASK-0278
author: Analista
role: independent adversarial checker
created_at: 2026-07-20
verdict: OK-CLOSABLE
implementation_commit: ef0b645
---

# TASK-0278 - Adversarial review verdict (Analista)

Reviewer: Analista (independent checker; maker != checker respected: implementation by
Codex at ef0b645, this review executed on a clean clone, not the hot tree).

## Canonical anchor

- Implementation commit under review: `ef0b645aacde188d1144c005871e7897e4fb0880`
  ("fix(TASK-0278): isolate agent outcome from CLI diagnostics"), verified ancestor of
  `origin/main` (HEAD at review time: `11a003a`).
- Review executed in a CLEAN CLONE at `D:/ccv0278`, checked out at `ef0b645`.
- Runtime drift at review time: `protocol_state_drift()` -> `has_drift=false`,
  `up_to_seq=5393` (per TASK-0274 guard, `--check-drift` not cited as gate).
- Scope: this hub only. No product repo in scope (declared by the instruction).

## What the fix does (verified in code and behavior)

`Get-ExecOutcomeClass` now receives the agent response (stdout) and the invoker
diagnostics (stderr) as SEPARATE parameters and classifies ONLY from stdout. The
diagnostics parameter has zero reads in the decision path. The free-text branch that
could return `definitive` was REMOVED: `definitive` is produced at exactly one line of
the harness (the exact terminal token match `^OUTCOME: (confirmed|transient|definitive)$`
case-sensitive on the last non-empty stdout line). Nonzero exit -> transient. Signed own
evidence -> confirmed. Free text -> transient or unconfirmed only. Consumption (seen
marking) happens only for `confirmed|definitive`; `transient|unconfirmed` go to
rollback + bounded retry + `RETRY_EXHAUSTED signal=watchdog`.

Stream separation is STRUCTURAL (per-stream redirection at `Start-Process`
`-RedirectStandardOutput`/`-RedirectStandardError`), not a blacklist of known epilogue
strings. This is stronger than both mechanisms offered in the acceptance wording.

## Reproduction (all in the clean clone at ef0b645; gated by exit code)

| Gate | Result | Exit |
|------|--------|------|
| `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | PASS | 0 |
| `python scripts/test_anthropic_checker_harness.py` | PASS | 0 |
| `python scripts/test_exec_lease_harness.py` | PASS (9 cases) | 0 |
| `python scripts/validate_collaboration_state.py` | OK | 0 |
| `python scripts/scan_encoding.py` | clean | 0 |
| `python scripts/scan_domain_neutrality.py` | clean | 0 |

Field-transcript recomputation: I re-ran the classifier extracted VERBATIM from the
clean-clone harness against the ORIGINAL transcripts in
`.protocol-tmp/codex_mailbox_cron/runs/` (not the reduced fixtures), plus 15 hostile
payloads (19 total, probe exit 0).

## Vector-by-vector PASS/SLIPS table

| # | Vector (what I tried to break) | Result | Verdict |
|---|-------------------------------|--------|---------|
| 1 | Real 16:44 done-flip 0272 transcript, verbatim out.log/err.log | transient (field had recorded definitive) | PASS |
| 2 | Real 16:56 GO TASK-0277 transcript, verbatim | transient | PASS |
| 3 | Real checker (Anthropic CLI) transcript: stdout ends `OUTCOME: confirmed`, stderr EMPTY | confirmed via terminal token | PASS |
| 4 | Checker epilogue variant + CONFLICTING `OUTCOME: definitive` in stderr vs `OUTCOME: transient` in stdout | transient (response wins) | PASS |
| 5 | Legacy concat shape (stdout+stderr joined, the pre-fix input) | transient, never definitive | PASS |
| 6 | Prompt echo lexicon (`NO-GO`, `out_of_scope`, `FUERA de alcance`) in stderr or stdout, no token | unconfirmed (no consumption) | PASS |
| 7 | FULL rendered prompt echoed into stdout (contains the token words inline) | unconfirmed; the rendered prompt cannot end in an exact token line because the outcome instruction sentence is appended last | PASS |
| 8 | Epilogue drifts into stdout AFTER the token (`tokens used` / count as last lines) | unconfirmed -> rollback + bounded retry + watchdog signal; NOT consumed | PASS (fail-safe direction; residual R1) |
| 9 | Token in stderr only, stdout empty, exit 0 | unconfirmed | PASS |
| 10 | Lowercase / trailing-space / mid-prose token variants | unconfirmed (exactness from 0272 iter2 preserved) | PASS |
| 11 | CRLF line endings on all streams | classified correctly | PASS |
| 12 | Token followed by blank/whitespace-only lines | classified (last NON-EMPTY line rule) | PASS |
| 13 | Exit nonzero, no token | transient | PASS |
| 14 | Invariant sweep: `grep definitive` over the harness | single producer = exact terminal token match; exit path yields transient only; free text yields transient/unconfirmed only | PASS |
| 15 | 0272 regression: `Get-OwnEvidence` attribution (actor case-sensitive == PeerId, ed25519, keyid, sig) and rollback via `Restore-TransientExecResidue` on every non-consuming outcome | intact; own-evidence-beats-free-text payload confirms | PASS |
| 16 | Both invokers delegate: `personal/Codex/codex_mailbox_cron.ps1` and `personal/Analista/analista_mailbox_cron.ps1` both call `scripts/harness/peer_mailbox_cron.ps1`; repo-wide grep finds ONE shipped classifier copy | single source, mirrors born-operational export | PASS |
| 17 | Forged EXACT token line written by the invoker as last stdout line | definitive (consumes) | BOUNDARY, see R1 - not a slip within the ratified frontier |

No NEW escape found: no path lets text the agent did not write produce `definitive` or
`confirmed` consumption, within the trust boundary declared in R1.

## Answer to the routed question

No. Consumption now requires either (a) the exact terminal token on the last non-empty
line of the CLI's stdout, or (b) an ed25519-signed ledger event by the peer itself.
Invoker epilogues, echoed prompts and diagnostics live on stderr and have zero vote;
even if they contaminated stdout, anything short of a forged exact terminal token line
degrades to a NON-consuming retry with a watchdog signal.

## Declared residuals

- R1 (trust boundary, accepted): stdout is writable only by the CLI process; a CLI that
  itself wrote a forged exact `OUTCOME:` line as its last stdout line would classify.
  That is the definition of "response stream", not free text. Field artifacts verify
  both supported CLIs today: codex CLI puts prompt echo + `tokens used` epilogue on
  stderr (runs 20260720T144326Z, 20260720T145435Z); Anthropic CLI stdout is
  response-only with empty stderr (run 20260720T154833Z). Any future CLI drift fails
  SAFE (unconfirmed -> retry -> RETRY_EXHAUSTED watchdog), never silent consumption.
- R2 (cosmetic): transient-lexicon regex still scans stdout free text; echoed vocabulary
  inside stdout could label `transient` instead of `unconfirmed`. Both are non-consuming
  retry paths; only retry accounting differs. No consumption impact.
- R3 (by design): `-InvokerDiagnostics` is accepted and intentionally unused in the
  decision; it documents the boundary and keeps the log available.
- R4 (mechanism deviation, favorable): acceptance offered epilogue-ignore-list OR
  last-occurrence search; the implementation chose structural stream separation, which
  is stronger than both (no blacklist to maintain, exactness preserved).
- Operational note: the two messages falsely consumed in the field on 2026-07-20 left no
  outstanding loss (done-flip 0272 landed at 3257f0d; TASK-0277 delivered at a899041).

## Closure recommendation

GO / OK-CLOSABLE. All six acceptance criteria verified by behavior in a clean clone at
ef0b645, including recomputation from the original field transcripts for BOTH invokers.
No conditions. Residuals R1-R4 declared above for the record.

Signed: Analista, 2026-07-20, local time 20:15 (UTC+2).
