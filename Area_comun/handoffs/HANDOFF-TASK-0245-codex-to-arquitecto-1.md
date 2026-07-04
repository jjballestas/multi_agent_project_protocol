---
handoff_id: HANDOFF-TASK-0245-codex-to-arquitecto-1
task_id: TASK-0245
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-04
artifacts:
  - skills/session-watchdogs.skill.md
  - skills/skills.config.json
  - scripts/new_instance.py
  - examples/skills_loader_cases/run_skills_loader_cases.py
---

task_id: TASK-0245
status: in_review
executive_summary: Implemented an exportable neutral `session-watchdogs` skill, registered it off-by-default, taught `scripts/new_instance.py` to carry `skills/`, and added a loader golden that proves the skill is registered, neutral, parameterized, and loadable.
artifacts: `skills/session-watchdogs.skill.md`; `skills/skills.config.json`; `scripts/new_instance.py`; `examples/skills_loader_cases/run_skills_loader_cases.py`
gates: `python examples/skills_loader_cases/run_skills_loader_cases.py` PASS; `python scripts/test_skills_loader.py` PASS; `python scripts/new_instance.py --source-template . --target <temp> ... --force` plus loader enable probe PASS; `python scripts/scan_encoding.py --root .` PASS; `python scripts/scan_domain_neutrality.py --root .` PASS; `python scripts/validate_collaboration_state.py --root .` PASS; drift check PASS `has_drift=false up_to_seq=3788`; Nova-Budget `npm test` PASS; Nova-Budget `dotnet test NOVA.sln` PASS with known NU1903 Microsoft.OpenApi warning.
next_recommended: Analista adversarial review for TASK-0245, then Arquitecto checker ratification if accepted.
risks: No runtime hooks were wired by design; the skill is documentation plus read-only loader coverage only. The exported placeholder syntax uses `<...>` to avoid `new_instance` template interpolation.
