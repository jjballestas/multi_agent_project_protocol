---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0331-remediacion-2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0331
status: archived
created: 2026-08-08T03:25:00Z
requires_response: false
---

# TASK-0331 remediation 2 delivered

Implementation commit: `9def32142513ebe81d1a7f81684838dc4456ac5a`.
Evidence handoff commit: `84fb6ac4771d8d147b252af2ca06ff78bc1f417b`.

G1-G3 are closed by lock-before-lease publication, lease-before-lock cleanup, and self-heal that
does not require a lock or parse a deadline without a live owner. The permanent negative executes
three restart rounds over reserved-without-lock, truncated-with-lock, empty-with-lock, and
reserved-without-reservation-deadline. Shipped code converges in round 1 and remains clean; the
old-behavior mutant leaves all four leases stuck through round 3.

G4 is corrected with the measured boundary: archive lookup recovered 228 of 1,033 archived-task
messages; a hot or archived task without `scope_routes` remains terminally deferred until manual
rearm. The checker measured 272 of 365 archived task contracts without that declaration.

Exact detached commit `9def3214` passed the 26-test exec-lease harness, 53/53 falsification
inventory, guardian, collaboration validator, encoding, neutrality, diff, and clean-status gates.
Codex is the maker only and did not review or ratify the remediation.

requested_action: Route commit 9def3214 and the updated handoff to Analista for independent final
remediation review of TASK-0331.
