---
task_id: TASK-0230
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-03
artifacts:
  - D:/Agentes/Zeus/Zeus-protocol/scripts/new-instance.mjs
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - D:/Agentes/Zeus/NOVA/Aegis/instance.profile.json
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/TASK_TEMPLATE.md
  - D:/Agentes/Zeus/NOVA/Aegis/.agents/
commits:
  product: e7c6da4
  instance: ab2b6a2
---

# Handoff TASK-0230 - new_instance Aegis

Implemented in `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da4 feat(instance): add nova budget bootstrapper`.

Instance created at `D:/Agentes/Zeus/nova-budget` from protocol tag `v1.18.0`, then relocated to the DECISION-0085 final path `D:/Agentes/Zeus/NOVA/Aegis`.
Source tag commit: `c9a442354bb5002b4df3a21e581ef1e891029c58`.
Instance commit: `ab2b6a2335c5cdb973a77bc955010dfce2bd7dce chore(instance): relocate governance instance to Aegis`.
Final instance path confirmed: `D:/Agentes/Zeus/NOVA/Aegis`; `D:/Agentes/Zeus/NOVA` is a flat suite umbrella without `.git`.

Key implementation points:
- `scripts/new-instance.mjs` defaults to dry-run, requires explicit `--write`, pins source ref to `v1.18.0`, validates target path under `D:/Agentes/Zeus`, and uses temp staging plus final rename for atomic writes.
- `instance.profile.json` now declares the `aegis` instance under suite `NOVA`, path `D:/Agentes/Zeus/NOVA/Aegis`, arm `budget`, mode `governed-instance`, risk taxonomy, Git adapter, committed agent configs, no multi-IDE adapters, and `engramInstallAllowed: false`.
- `.agents/{Codex,Arquitecto,Analista}/config.json` files are committed in the instance repo and point at workspace root `D:/Agentes/Zeus/NOVA/Aegis`.
- Generated `Area_comun/protocol/TASK_TEMPLATE.md` extends intake v2 / DoR for `feature` and `product` with `target_user`, `functional_scope`, `assets_inputs`, `tech_constraints`, `risks_list`, `priority`, and anti-empty rules.
- Tests cover dry-run planning, DoR anti-empty validation, atomic write target protection, source tag pin, generated Git adapter config, and absence of the forbidden installer string from generated configs.

Gates run:
- `node --check scripts/new-instance.mjs` PASS.
- `node --check tests/staticContract.test.js` PASS.
- `node scripts/new-instance.mjs --dry-run --name nova-budget --source-ref v1.18.0 --protocol-repo D:/Agentes/multi_agent_project_protocol --zeus-root D:/Agentes/Zeus` PASS.
- `node scripts/new-instance.mjs --write --name nova-budget --source-ref v1.18.0 --protocol-repo D:/Agentes/multi_agent_project_protocol --zeus-root D:/Agentes/Zeus` PASS.
- `node --check public/app.js` PASS.
- `node --check src/server.js` PASS.
- `npm test` PASS: 112 tests, 90 pass, 22 skipped.
- `python scripts/validate_collaboration_state.py --root .` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `python scripts/scan_encoding.py` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `python scripts/scan_domain_neutrality.py` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `Get-ChildItem -Path D:/Agentes/Zeus/NOVA -Force -Recurse -Directory -Filter .git` returned only `D:\Agentes\Zeus\NOVA\Aegis\.git`.

task_id: TASK-0230
status: in_review
executive_summary: Re-delivered TASK-0230 under DECISION-0085: NOVA is now a flat suite umbrella and the governance instance repo lives at D:/Agentes/Zeus/NOVA/Aegis with route refs updated.
artifacts: D:/Agentes/Zeus/Zeus-protocol commit e7c6da4; D:/Agentes/Zeus/NOVA/Aegis commit ab2b6a2; scripts/new-instance.mjs; tests/staticContract.test.js; D:/Agentes/Zeus/NOVA/Aegis/instance.profile.json; D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/TASK_TEMPLATE.md; D:/Agentes/Zeus/NOVA/Aegis/.agents configs.
gates: node --check scripts/new-instance.mjs PASS; node --check tests/staticContract.test.js PASS; dry-run PASS; write PASS; node --check public/app.js PASS; node --check src/server.js PASS; npm test PASS 112 tests (90 pass, 22 skipped); Aegis validate PASS; Aegis encoding PASS; Aegis domain-neutrality PASS; NOVA .git probe PASS only Aegis/.git found.
next_recommended: Arquitecto route adversarial review to Analista, then ratify or request changes under maker!=checker.
risks: Historical source docs and event logs inside Aegis still mention older NOVA paths as historical evidence; current handoff, instance.profile.json, and agent configs point to D:/Agentes/Zeus/NOVA/Aegis.
