# Multi-agent project protocol template

Reusable, domain-neutral project protocol for multi-agent software work.

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
