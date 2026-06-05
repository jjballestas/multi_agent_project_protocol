# Dotnet Enterprise - professional profile

`dotnet_enterprise` packages professional .NET enterprise practices as an optional profile for
the multi-agent protocol. It is based on `D:\Agentes\entorno_open_cloude` and keeps every
stack-specific rule inside `profiles/dotnet_enterprise/`.

## What It Adds

- ADR and architecture baseline for .NET enterprise development.
- Branching, artifact model and template-versioning guidance.
- Secure AI usage rules, development secret handling and container-network security.
- Azure DevOps pipeline templates, including regulated pipeline checks.
- Dev Container, SQL Server development and database bootstrap templates.
- Onboarding and master prompt material for .NET development work.

## When To Use It

Use this profile when a project instance is a .NET enterprise application or platform that wants
repeatable development environments, SQL Server development governance, CI/CD templates and
stricter security rules around AI-assisted work.

Do not use it for generic protocol instances or non-.NET projects. The core protocol remains
domain-neutral without this profile.

## Core Compatibility

- Profile version: `0.1.0`
- Required protocol version: `>=0.2.0 <1.0.0`

An adopting instance must declare a compatible `protocol_version` in `protocol.config.json`.

## How To Adopt

1. Create a normal core instance with `scripts/new_instance.py`.
2. Copy `profiles/dotnet_enterprise/` into the instance, or reference a published version.
3. Add the profile boundaries, gates and approval points from `profile.manifest.json` to the
   instance `AGENTS.md` and `protocol.config.json` where applicable.
4. Register adoption in `Area_comun/state/PROJECT_STATE.json`:

   ```json
   "adopted_profiles": [
     {
       "profile_id": "dotnet_enterprise",
       "profile_version": "0.1.0",
       "adopted_at": "2026-06-05"
     }
   ]
   ```

5. Record a local decision in `Area_comun/decisions/` for traceability.
6. Run the collaboration state validator.

## Structure

```text
dotnet_enterprise/
|-- profile.manifest.json
|-- README.md
|-- docs/
|   |-- Guia_Metodologica.md
|   |-- ONBOARDING.md
|   |-- arquitectura/
|   |-- contenedores/
|   |-- decisiones/
|   |-- gobierno/
|   |-- pipelines/
|   `-- seguridad/
|-- templates/
|   |-- azure-pipelines/
|   |-- db-bootstrap-dotnet/
|   |-- devcontainer-dotnet/
|   |-- docker-sqlserver/
|   `-- repo-structure/
`-- prompts/
    `-- prompt-maestro-Desarrollo_DotNet.md
```

## Security Notes

No real secrets are included. `.env.example` uses placeholders only. Adopting projects must keep
real values in ignored local files, protected pipeline variables or an approved vault.

## Neutrality Boundary

This profile may mention .NET, SQL Server, Azure DevOps, Docker and Dev Containers because those
are its explicit scope. Those terms must not be copied into the protocol core, core templates or
generic validator contract.
