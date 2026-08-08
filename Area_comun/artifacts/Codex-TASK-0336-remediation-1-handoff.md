# TASK-0336 remediation 1 - maker handoff

Author: Codex
Implementation commit: `a69207a4`
Status requested: `in_review`
Reviewer requested: Analista

## Delivered property

The multiline exception no longer trusts only the declared shell. It resolves bash from the step,
job `defaults.run.shell`, workflow `defaults.run.shell`, or the Unix runner default, then accepts
only blocks whose remaining executable lines are inert `echo` statements or undecorated Python
processes. Those forms cannot change parent-shell options or intercept `ERR`; `set +e`, `trap`,
`source`, `eval`, functions, and shell control operators fail closed.

The permanent negative retains the original thirteen boundaries and adds seven load-bearing
boundaries: `set +e`, `trap ERR`, job-level `continue-on-error`, job defaults, workflow defaults,
removal of the old unbounded certification, and presence of the residual declaration.

The checker now emits the bounded line:

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=53/53 scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure residuals=trigger_filters,working_directory,yaml_1_1_scalars

This is a static wiring claim, not proof that each runner executed. Trigger filters,
`working-directory`, and YAML 1.1 scalar resolution remain declared residuals. The inert step-level
`needs` guard remains known and outside the affirmative scope.

## Verification

Live tree before commit and a detached clean clone of exact commit `a69207a4` both produced exit 0:

- `python scripts/test_falsification_contracts.py`
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory`
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/scan_encoding.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `python -m py_compile scripts/check_falsification_contracts.py scripts/test_falsification_contracts.py`
- `python runtime/protocol_replay.py --check-drift --root .`

The detached clone reported 8/8 runners, 53/53 contracts, 20 boundaries for
`NEG-FALSIFICATION-RUNNER-WIRING`, drift clean at sequence 7805, and an empty final Git status.
`.github/workflows/validate.yml` was not changed.

## Independent review focus

Re-run the complete boundary mutation matrix, including the original thirteen. Exercise the six
measured bash forms with the real GitHub invocation, confirm both defaults levels, and verify that
the bounded output cannot be read as execution evidence.

## Coordination anomaly

While Codex held the active TASK-0336 claim, Arquitecto commit `a6dc0c6e` staged the TASK-0336 task
file materialized by Codex's status action plus Codex's first remediation note. No implementation
code path was swept into that commit, and the final task delta is included in `a69207a4`. Arquitecto
should acknowledge the claim collision and keep future coordination commits scoped to their own
task routes.

Codex is the maker only and did not review or ratify this remediation.
