# Multi-agent project protocol

> **Proprietary — All Rights Reserved.** © 2026 John Jairo Ballestas Payares. See
> [`LICENSE`](LICENSE) and
> [`DECISION-0010`](Area_comun/decisions/DECISION-0010-licenciamiento-propietario.md). No license or
> rights are granted; viewing this repository does not permit use, copying, modification or
> redistribution. Any use requires a separate written agreement with the Owner.

A domain-neutral project protocol for multi-agent software work. The `.template.*` masters and the
instantiation flow below are for the **Owner's authorized use**, not for public reuse.

Start with `README_INSTANCIACION.md`, then fill:

- `AGENTS.template.md`
- `protocol.config.template.json`
- `Area_comun/README.template.md`
- `Area_comun/state/*.template.json`
- `Area_comun/tasks/` with the first project tasks

Template files with `.template.*` are the **shipped masters**.

**Dogfooding:** this repository applies its own protocol to its own development, so it also
contains **live canonical files** (`AGENTS.md`, `CLAUDE.md`, `protocol.config.json`,
`Area_comun/state/*.json`) that are *this* project's own instance — plus a real reference
instance in `examples/minimal_instance/`. When you create a NEW project, copy the `.template.*`
masters and fill the placeholders; do not maintain duplicate canonical copies in a template-only
root.

The template is intentionally empty of domain policy. Each project instance must define its
own `{{DOMAIN_CRITICAL_BOUNDARIES}}`, `{{QUALITY_GATES}}` and `{{HUMAN_APPROVAL_POINTS}}`.
