# Arquitectura del protocolo — core / profiles / examples

> Entregable de **TASK-0005** (Claude). Materializa
> [DECISION-0002](../decisions/DECISION-0002-core-perfiles-profesionales.md) y se apoya en el
> versionado de [DECISION-0001](../decisions/DECISION-0001-versionado.md).

## 1. Las tres capas

```text
┌──────────────────────────────────────────────────────────────────────┐
│ (a) CORE neutral de dominio                          [se versiona vX.Y.Z]
│     AGENTS.md · Area_comun/protocol/* · *.template.* · validador        │
│     ciclo de vida · claims · mailbox · handoffs · decisiones · reports  │
│     → NEUTRAL: sin .NET/SQL/Azure DevOps/Docker/trading/negocio.        │
│     → Es lo único que define el contrato y la compatibilidad (SemVer).  │
└───────────────▲───────────────────────────────────────▲────────────────┘
                │ requires_protocol_version              │ instancia
                │ (rango SemVer del core)                │
┌───────────────┴────────────────┐         ┌─────────────┴────────────────┐
│ (b) PROFILES (opcionales)       │ compone │ (c) EXAMPLES / instancias     │
│     profiles/<id>/              │────────▶│     examples/* y repos reales │
│     manifest + docs/templates/  │         │     core  ó  core + perfiles  │
│     prompts + fronteras extra   │         │     (declaran adopted_profiles)│
│     → AQUÍ vive todo lo de stack │         └───────────────────────────────┘
└──────────────────────────────────┘
```

- **(a) Core** — neutral, reutilizable, versionado. Único dueño del contrato (estructura, ciclo de
  vida, campos obligatorios, validador, `*.template.*`). Cambiarlo de forma incompatible es MAJOR
  y requiere aprobación humana.
- **(b) Profiles** — extensiones opcionales por stack/tipo de proyecto bajo `profiles/<id>/`. Cada
  uno con su `profile.manifest.json`. Son **aditivos**: añaden, nunca relajan. Publicar un perfil o
  el mecanismo de perfiles es MINOR.
- **(c) Examples / instancias** — proyectos que aplican el core, o core + N perfiles. Declaran qué
  perfiles adoptan (`adopted_profiles` y/o decisión propia). `examples/minimal_instance/` es el
  ejemplo solo-core.

## 2. Reglas de composición

1. Una instancia **siempre** parte del core. Los perfiles son opcionales y acumulables.
2. Un perfil solo es aplicable si el `protocol_version` de la instancia satisface su
   `requires_protocol_version` (compatibilidad por MAJOR, DECISION-0001).
3. Los perfiles pueden **endurecer** fronteras/gates/aprobaciones; **no** pueden relajarlas ni
   tocar el contrato del core.
4. Conflicto entre dos perfiles (gates incompatibles) → se resuelve con una **decisión de la
   instancia**; el core no arbitra políticas de dominio.
5. La frontera de neutralidad es la invariante dura: el barrido de neutralidad sobre el núcleo y
   los `*.template.*` del core debe quedar **limpio**; lo específico vive solo en `profiles/<id>/`.

## 3. Contrato del manifiesto (resumen)

Definido y documentado en [`../../profiles/README.md`](../../profiles/README.md) §3 y en
[`../../profiles/PROFILE_TEMPLATE/profile.manifest.template.json`](../../profiles/PROFILE_TEMPLATE/profile.manifest.template.json).
Claves: `profile_id`, `profile_version` (SemVer del perfil), `requires_protocol_version` (rango del
core), `stack`, `provides` (docs/templates/prompts), `adds_boundaries`, `adds_quality_gates`,
`adds_human_approval_points`, `depends_on_profiles`, `neutrality_note`.

## 4. Cómo una instancia registra la adopción

- **Recomendado (máquina-legible):** `adopted_profiles` en `PROJECT_STATE.json` con
  `{ profile_id, profile_version, adopted_at }` por cada perfil.
- **Y/o decisión de instancia:** `DECISION-XXXX-*.md` en el repo del proyecto.
- El **validador** ganará conciencia de `adopted_profiles` en **TASK-0007**, de forma aditiva:
  sin perfiles declarados, el comportamiento es idéntico al actual.

## 5. Mapa de directorios objetivo

```text
multi_agent_project_protocol/
├── AGENTS.md · CLAUDE.md · CHANGELOG.md            (core)
├── *.template.* · protocol.config.json             (core)
├── Area_comun/                                      (core: protocolo + estado vivo)
├── scripts/                                         (core: validador)
├── profiles/                                        (capa b)
│   ├── README.md
│   ├── PROFILE_TEMPLATE/
│   └── dotnet_enterprise/        ← TASK-0006 (primer perfil)
└── examples/                                        (capa c)
    └── minimal_instance/         (solo-core, valida verde)
```

## 6. Trabajo derivado

- **TASK-0006 (Codex):** construir `profiles/dotnet_enterprise/` desde `entorno_open_cloude`
  (ADRs, branching, seguridad, pipelines Azure DevOps, Dev Containers, SQL Server) respetando este
  contrato y la frontera de neutralidad.
- **TASK-0007 (Codex):** `adopted_profiles` en la plantilla de estado + soporte en validador
  (paridad `.py` ↔ `.ps1`), todo aditivo.

## 7. Decisión abierta (no bloqueante)

`adopted_profiles` ¿solo en `PROJECT_STATE.json`, solo decisión, o ambos? **Recomendación:** ambos
la primera adopción (campo para máquina + decisión para trazabilidad humana); se cierra junto a
TASK-0007.
