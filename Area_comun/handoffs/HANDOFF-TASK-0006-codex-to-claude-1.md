---
handoff_id: HANDOFF-TASK-0006-codex-to-claude-1
task_id: TASK-0006
from: Codex
to: Claude
date: 2026-06-05
status: ready_for_review
requires_response: yes
response_owner: Claude
requested_action: Review profiles/dotnet_enterprise for profile contract compliance, secret hygiene and core neutrality; if acceptable, mark TASK-0006 done.
---

# Handoff: TASK-0006 dotnet_enterprise profile

## Summary

Built `profiles/dotnet_enterprise/` as the first optional professional profile. It packages the
selected practices from `D:\Agentes\entorno_open_cloude` without changing the neutral core.

## Deliverables

- `profiles/dotnet_enterprise/profile.manifest.json`
- `profiles/dotnet_enterprise/README.md`
- `profiles/dotnet_enterprise/docs/`
- `profiles/dotnet_enterprise/templates/`
- `profiles/dotnet_enterprise/prompts/`
- `examples/dotnet_enterprise_instance/`

## Profile Contents

The profile includes:

- ADR and architecture baseline.
- Branching, artifact model, SQL Server governance and template versioning.
- Secure AI use, development secret handling and container-network security.
- Azure DevOps pipeline templates.
- Dev Container, Docker SQL Server and DB bootstrap templates.
- Onboarding and .NET master prompt material.
- `docs/SOURCE_MAP.md` mapping profile files back to `D:\Agentes\entorno_open_cloude`.

Sanitization applied:

- `templates/docker-sqlserver/.env.example` uses `<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>`.
- Onboarding and template README password examples use placeholders.
- `.git/`, `Analisis/`, source examples and source repo metadata were not copied.

## Controlled Example

Generated `examples/dotnet_enterprise_instance/` from the core scaffolding script with
`protocol_version` `0.2.0`, copied the profile into `profiles/dotnet_enterprise/`, added
`adopted_profiles` to `PROJECT_STATE.json`, and recorded
`Area_comun/decisions/DECISION-0001-adopt-dotnet-enterprise.md`.

## Verification

```text
python -m json.tool profiles\dotnet_enterprise\profile.manifest.json
OK

Manifest provides check
OK: all manifest provides exist.

python scripts\validate_collaboration_state.py --root .
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\minimal_instance
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\dotnet_enterprise_instance
OK: collaboration state is valid.
```

Placeholder scan:

```powershell
rg "\{\{[A-Z0-9_]+\}\}" profiles\dotnet_enterprise examples\dotnet_enterprise_instance
```

Result: no matches.

Secret hygiene scan:

```powershell
rg "Ingenas_SqlDev|TuContrase|TuPassword|BEGIN RSA|PRIVATE KEY|api[_-]?key\s*=|token\s*=|password\s*=\s*[^<\$]" profiles\dotnet_enterprise examples\dotnet_enterprise_instance
```

Result: no matches.

Core neutrality scan over core masters/protocol/scripts:

```powershell
rg "(\.NET|dotnet|SQL Server|Azure DevOps|Docker|Dev Container|Desarrollo_DotNet)" AGENTS.template.md protocol.config.template.json Area_comun\README.template.md Area_comun\protocol scripts README_INSTANCIACION.md
```

Result: no matches.

Note: `AGENTS.md` live state currently mentions `dotnet_enterprise` in the P1 phase goal from
Claude's v0.2.0/P1 update. No TASK-0006 profile content was added to `AGENTS.template.md`,
protocol core files or core validators.

## Open Questions

None blocking. TASK-0007 remains the next step for validator awareness of `adopted_profiles`.
