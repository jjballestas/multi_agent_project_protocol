---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0336-remediacion-4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0336
status: archived
created: 2026-08-08T15:33:00Z
requires_response: false
---

# TASK-0336 remediation 4 delivered for independent review

Implementation commit: `90477ff7ac8dc7f838e4debb7c53e5ff7a2bfb83`.

The fail-closed whitelist remains intact. Bash blocks now derive command boundaries from the
effective Bash shell (LF only) and trim only horizontal layout whitespace. The test derives every
Unicode scalar that Python treats as a line separator but Bash does not, then rejects both command
coordinates through explicit Bash, implicit Unix Bash, job defaults, and workflow defaults. A bare
runner is accepted only after resolving a known effective shell family; unknown shells and dynamic
runner labels fail closed.

The AC5 contract mutates the live certification text to `FALSIFICATION_EXECUTION guaranteed=yes`
with `scope=full_execution_guarantee`; the bounded-static assertion rejects that output. Canonical
inventory is 8/8 runners, 59/59 contracts, and 37 wiring boundaries.

Declared debts: safe forms with arguments and dynamic/self-hosted labels remain outside the
whitelist; only 23 of the prior 31 boundaries discriminated in the reviewer's finite mutation
matrix; the line-continuation guard and whitelist overlap; TASK-0338 has the same splitlines-versus-
consumer root and is not absorbed here.

Exact commit passed the task suite, inventory, collaboration, encoding, neutrality, drift, compile,
and diff gates in a detached clean clone with empty Git status. `.github/workflows/validate.yml`
was not touched. Codex is maker only and did not review or ratify the remediation.

requested_action: Route implementation commit 90477ff7 to Analista for independent TASK-0336 r5
review before any closure.
