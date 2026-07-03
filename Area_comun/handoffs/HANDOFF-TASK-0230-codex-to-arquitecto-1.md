---
task_id: TASK-0230
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-03
artifacts:
  - D:/Agentes/Zeus/Zeus-protocol/scripts/new-instance.mjs
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - D:/Agentes/Zeus/NOVA/instance.profile.json
  - D:/Agentes/Zeus/NOVA/Area_comun/protocol/TASK_TEMPLATE.md
  - D:/Agentes/Zeus/NOVA/.agents/
commits:
  product: e7c6da4
  instance: 172edcb
---

# Handoff TASK-0230 - new_instance nova-budget

Implemented in `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da4 feat(instance): add nova budget bootstrapper`.

Instance created at `D:/Agentes/Zeus/nova-budget` from protocol tag `v1.18.0`, then relocated to the operator-directed final path `D:/Agentes/Zeus/NOVA`.
Source tag commit: `c9a442354bb5002b4df3a21e581ef1e891029c58`.
Instance commit: `172edcb53d18ac6568a61c42b10f644cf9fb9ed9 chore(instance): configure nova-budget`.
Final instance path confirmed: `D:/Agentes/Zeus/NOVA`.

Key implementation points:
- `scripts/new-instance.mjs` defaults to dry-run, requires explicit `--write`, pins source ref to `v1.18.0`, validates target path under `D:/Agentes/Zeus`, and uses temp staging plus final rename for atomic writes.
- Generated `instance.profile.json` declares arm `budget`, mode `governed-instance`, risk taxonomy, Git adapter, committed agent configs, no multi-IDE adapters, and `engramInstallAllowed: false`.
- Generated `.agents/{Codex,Arquitecto,Analista}/config.json` files are committed in the instance repo.
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

task_id: TASK-0230
status: in_review
executive_summary: Built and executed the nova-budget new_instance flow from pinned tag v1.18.0, with committed Git-adapter agent configs and instance DoR v2 template extension.
artifacts: D:/Agentes/Zeus/Zeus-protocol commit e7c6da4; D:/Agentes/Zeus/NOVA commit 172edcb; scripts/new-instance.mjs; tests/staticContract.test.js; instance.profile.json; Area_comun/protocol/TASK_TEMPLATE.md; .agents configs.
gates: node --check scripts/new-instance.mjs PASS; node --check tests/staticContract.test.js PASS; dry-run PASS; write PASS; node --check public/app.js PASS; node --check src/server.js PASS; npm test PASS 112 tests (90 pass, 22 skipped).
next_recommended: Arquitecto route adversarial review to Analista, then ratify or request changes under maker!=checker.
risks: Existing v1.18.0 source history contains governance references that mention the forbidden installer as a prohibition; generated instance configs do not contain or enable it, and the script does not execute it.
