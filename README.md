# Multi-agent project protocol template

Reusable, domain-neutral project protocol for multi-agent software work.

Start with `README_INSTANCIACION.md`, then fill:

- `AGENTS.template.md`
- `protocol.config.json`
- `Area_comun/README.template.md`
- `Area_comun/state/*.template.json`
- `Area_comun/tasks/` with the first project tasks

Template files with `.template.*` are the masters. Canonical files without that suffix should be
created only in project instances, not maintained in parallel in this template root.

The template is intentionally empty of domain policy. Each project instance must define its
own `{{DOMAIN_CRITICAL_BOUNDARIES}}`, `{{QUALITY_GATES}}` and `{{HUMAN_APPROVAL_POINTS}}`.
