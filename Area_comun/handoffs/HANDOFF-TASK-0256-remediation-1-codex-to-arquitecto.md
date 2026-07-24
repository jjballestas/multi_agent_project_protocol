# HANDOFF - TASK-0256 remediation iteration 1

## Delivery

- Implementation commit: `26995a6`.
- Changed policy route: `AGENTS.template.md` only.
- Selected fix: option B, one introductory clarification before the three roster rules.
- The clarification limits the policy to code-executing agent participants and states
  that it neither alters human-owner approval authority nor redefines the registry's
  `signer`/`worker` key-possession tiers.
- The three rules are unchanged. Runtime, validators, config, and live instances are unchanged.

## Generated attested-default evidence

Command: `python scripts/new_instance.py --source-template . --target <temp> --project-name task0256_probe --project-goal probe --project-description probe --architect ArchitectAgent --implementer MakerAgent --analyst CheckerAgent --human-owner HumanOwner --phase-id P0 --phase-name Probe --phase-goal probe --tier attested --scratch-root <temp-scratch>`

Result: exit 0.

Generated route:
`C:/Users/johnb/AppData/Local/Temp/task0256-remediation1-038abcab1d944be6b7daca682b49b12e/Aegis/AGENTS.md`

Matched generated content:

- Lines 64-65: the new human-owner authority and key-possession-tier clarification.
- Line 67: rule 1, worker agent subordinate to maker.
- Line 70: rule 2, strong-capability maker governs worker agents.
- Line 76: rule 3, strong-capability adversarial checker and `maker != checker`.

## Gates

- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python runtime/protocol_replay.py --check-drift --root .` -> exit 0, clean through seq 6320.
- `python scripts/test_attested_instancing.py` -> exit 0.
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> exit 0.
- Fresh attested-default generation and content match -> exit 0.

## Review boundary

Codex is the maker. Codex did not review or ratify the remediation. Independent checker:
Analista.
