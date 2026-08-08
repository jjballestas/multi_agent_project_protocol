# TASK-0336 remediation 2 - maker handoff

Author: Codex
Implementation commit: `e21e617a`
Status requested: `in_review`
Reviewer requested: Analista

## Delivered property

The checker now preserves physical-line indexes before normalizing path separators. If an
executable Bash line ends in an odd number of backslashes, the next physical line is marked as
consumed by Bash line continuation. A runner invocation at that index cannot count as a direct
invocation because Bash executes it as part of the preceding command.

The rule is deliberately narrow. A comment ending in a backslash does not consume the next line,
and a backslash followed by whitespace is not classified as continuation. Existing shell-failure,
job-failure, trigger-key, condition, and direct-invocation checks are unchanged.

## Permanent behavioral boundaries

`NEG-FALSIFICATION-RUNNER-WIRING` now declares 25 boundaries. The new family proves rejection of
`echo before \\` followed by the runner through all four effective-Bash entry paths:

1. `shell: bash` on the step;
2. the implicit Bash shell on an Ubuntu runner;
3. `defaults.run.shell: bash` on the job;
4. `defaults.run.shell: bash` on the workflow.

The acceptance-side boundary proves that a comment ending in `\\` followed by the runner remains
accepted. The canonical good workflow remains accepted.

## Certification scope

The checker still emits only the bounded static-wiring statement:

    FALSIFICATION_STATIC_WIRING runners=8/8 contracts=55/55 scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure residuals=trigger_filters,working_directory,yaml_1_1_scalars

This is not execution evidence. No residual or certification scope changed in this remediation.
`.github/workflows/validate.yml` was not touched.

## Verification

The live tree before the implementation commit produced exit 0 for the targeted suite, canonical
inventory, collaboration validator, encoding scan, domain-neutrality scan, runtime drift check,
Python compile, and diff check. A detached clean clone of exact commit `e21e617a` produced exit 0
for the targeted suite, canonical inventory, Python compile, and diff check, with empty status.

The exact-code clone reported 8/8 runners, 55/55 contracts, and 25 boundaries for
`NEG-FALSIFICATION-RUNNER-WIRING`.

## Independent review focus

Recompute the complete 25-boundary mutation matrix, the prior 22 accepted/rejected shell forms,
and the C.1 Bash family with the Git Bash binary fixed explicitly. Confirm that the four
continuation fixtures fail, the comment-ending-backslash case passes, and no distinct escape family
appears.

Codex is the maker only and did not review or ratify this remediation.
