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
  instance: 518b2e5
---

# Handoff TASK-0230 - new_instance Aegis

Implemented in `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da4 feat(instance): add nova budget bootstrapper`.

Instance created as the canonical Aegis governance instance at `D:/Agentes/Zeus/NOVA/Aegis` from protocol tag `v1.18.0`. The earlier `nova-budget` name/path was a transitory bootstrap label superseded by DECISION-0085; it is not the final delivery identity.
Source tag commit: `c9a442354bb5002b4df3a21e581ef1e891029c58`.
Instance relocation commit: `ab2b6a2335c5cdb973a77bc955010dfce2bd7dce chore(instance): relocate governance instance to Aegis`.
Instance remediation commit: `518b2e58 fix(instance): align Aegis suite arm`.
Final instance path confirmed: `D:/Agentes/Zeus/NOVA/Aegis`; `D:/Agentes/Zeus/NOVA` is a flat suite umbrella without `.git`.

Key implementation points:
- `scripts/new-instance.mjs` defaults to dry-run, requires explicit `--write`, pins source ref to `v1.18.0`, validates target path under `D:/Agentes/Zeus`, and uses temp staging plus final rename for atomic writes.
- `instance.profile.json` now declares the `aegis` instance under suite `NOVA`, path `D:/Agentes/Zeus/NOVA/Aegis`, arm `nova-suite`, mode `governed-instance`, risk taxonomy, Git adapter, committed agent configs, no multi-IDE adapters, and `engramInstallAllowed: false`.
- `.agents/{Codex,Arquitecto,Analista}/config.json` files are committed in the instance repo and point at workspace root `D:/Agentes/Zeus/NOVA/Aegis`.
- Generated `Area_comun/protocol/TASK_TEMPLATE.md` extends intake v2 / DoR for `feature` and `product` with `target_user`, `functional_scope`, `assets_inputs`, `tech_constraints`, `risks_list`, `priority`, and anti-empty rules.
- Tests cover dry-run planning, DoR anti-empty validation, atomic write target protection, source tag pin, generated Git adapter config, and absence of the forbidden installer string from generated configs.

Gates run:
- `node --check scripts/new-instance.mjs` PASS.
- `node --check tests/staticContract.test.js` PASS.
- Historical bootstrap commands that used `--name nova-budget` are superseded by DECISION-0085 and are not the canonical delivery route. The final committed instance identity is `aegis` at `D:/Agentes/Zeus/NOVA/Aegis`.
- `node --check public/app.js` PASS.
- `node --check src/server.js` PASS.
- `npm test` PASS: 112 tests, 90 pass, 22 skipped.
- `python scripts/validate_collaboration_state.py --root .` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `python scripts/scan_encoding.py` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `python scripts/scan_domain_neutrality.py` in `D:/Agentes/Zeus/NOVA/Aegis` PASS.
- `Get-ChildItem -Path D:/Agentes/Zeus/NOVA -Force -Recurse -Directory -Filter .git` returned only `D:\Agentes\Zeus\NOVA\Aegis\.git`.

task_id: TASK-0230
status: in_review
executive_summary: Remediated TASK-0230 fix-loop 1/2: the handoff now names aegis@NOVA/Aegis as the canonical final identity, marks nova-budget as only a superseded bootstrap label, and the Aegis profile uses arm=nova-suite rather than a product arm.
artifacts: D:/Agentes/Zeus/Zeus-protocol commit e7c6da4; D:/Agentes/Zeus/NOVA/Aegis commit 518b2e5; scripts/new-instance.mjs; tests/staticContract.test.js; D:/Agentes/Zeus/NOVA/Aegis/instance.profile.json; D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/TASK_TEMPLATE.md; D:/Agentes/Zeus/NOVA/Aegis/.agents configs; Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md.
gates: node --check scripts/new-instance.mjs PASS; node --check tests/staticContract.test.js PASS; node --check public/app.js PASS; node --check src/server.js PASS; npm test PASS 112 tests (90 pass, 22 skipped); Aegis validate PASS; Aegis encoding PASS; Aegis domain-neutrality PASS; hub encoding/domain-neutrality/validate/drift PASS.
next_recommended: Arquitecto route TASK-0230 remediation re-gate to Analista for F-0230-AEGIS-01 and F-0230-AEGIS-02, then ratify or request changes under maker!=checker.
risks: Historical source docs and event logs inside Aegis may still mention older bootstrap labels as history; current handoff, instance.profile.json, and agent configs point to D:/Agentes/Zeus/NOVA/Aegis and identify the instance as aegis.
