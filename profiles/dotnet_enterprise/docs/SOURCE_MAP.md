# Source Map

This profile is derived from `D:\Agentes\entorno_open_cloude`.

| Profile path | Source path |
|--------------|-------------|
| `docs/Guia_Metodologica.md` | `Guia_Metodologica.md` |
| `docs/ONBOARDING.md` | `ONBOARDING.md` |
| `docs/arquitectura/arquitectura-general.md` | `docs/arquitectura/arquitectura-general.md` |
| `docs/contenedores/estrategia-docker-desarrollo.md` | `docs/contenedores/estrategia-docker-desarrollo.md` |
| `docs/decisiones/adr-001-diseno-base-entorno.md` | `docs/decisiones/adr-001-diseno-base-entorno.md` |
| `docs/gobierno/estrategia-branching.md` | `docs/gobierno/estrategia-branching.md` |
| `docs/gobierno/modelo-artefactos.md` | `docs/gobierno/modelo-artefactos.md` |
| `docs/gobierno/sql-server-gobernanza.md` | `docs/gobierno/sql-server-gobernanza.md` |
| `docs/gobierno/versionado-plantillas.md` | `docs/gobierno/versionado-plantillas.md` |
| `docs/pipelines/pipeline-base.md` | `docs/pipelines/pipeline-base.md` |
| `docs/seguridad/gestion-secretos-desarrollo.md` | `docs/seguridad/gestion-secretos-desarrollo.md` |
| `docs/seguridad/reglas-uso-ia.md` | `docs/seguridad/reglas-uso-ia.md` |
| `docs/seguridad/seguridad-red-contenedores.md` | `docs/seguridad/seguridad-red-contenedores.md` |
| `templates/azure-pipelines/` | `templates/azure-pipelines/` |
| `templates/db-bootstrap-dotnet/` | `templates/db-bootstrap-dotnet/` |
| `templates/devcontainer-dotnet/` | `templates/devcontainer-dotnet/` |
| `templates/docker-sqlserver/` | `templates/docker-sqlserver/` |
| `templates/repo-structure/` | `templates/repo-structure/` |
| `prompts/prompt-maestro-Desarrollo_DotNet.md` | `prompts/prompt-maestro-Desarrollo_DotNet.md` |

Sanitization applied:

- `templates/docker-sqlserver/.env.example` uses `<CAMBIAR_POR_PASSWORD_LOCAL_SEGURA>` instead of
  the source value.
- Onboarding and template README password examples use placeholders only.
- `.git/`, `Analisis/`, source examples and source repo metadata were not copied into the profile.
