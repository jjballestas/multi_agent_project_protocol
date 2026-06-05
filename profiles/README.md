# profiles/ — Perfiles profesionales del protocolo

Esta carpeta contiene **perfiles profesionales**: extensiones **opcionales y componibles** del
protocolo, por stack o tipo de proyecto. Formaliza la capa (b) de
[DECISION-0002](../Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md).

> **Regla de oro.** El **core** del protocolo permanece **neutral de dominio**. Todo lo específico
> de un stack o negocio (lenguajes, motores de BD, plataformas DevOps, contenedores, ADRs de un
> ecosistema, etc.) vive **aquí**, en un perfil — **nunca** en los archivos del núcleo ni en los
> `*.template.*` del core.

## 1. ¿Qué es un perfil?

Un perfil es un paquete autocontenido bajo `profiles/<profile_id>/` que aporta documentación,
plantillas, prompts y **fronteras adicionales** para un contexto concreto (p.ej. `dotnet_enterprise`).
Cada perfil declara su contrato en un `profile.manifest.json`.

```text
profiles/
├── README.md                     ← este archivo
├── PROFILE_TEMPLATE/             ← master neutral para crear perfiles nuevos
│   ├── profile.manifest.template.json
│   ├── README.md
│   ├── docs/
│   ├── templates/
│   └── prompts/
└── <profile_id>/                 ← un perfil concreto (p.ej. dotnet_enterprise)
    ├── profile.manifest.json
    ├── README.md
    ├── docs/
    ├── templates/
    └── prompts/
```

## 2. Qué puede y qué no puede hacer un perfil

| Un perfil **PUEDE** | Un perfil **NO PUEDE** |
|---------------------|------------------------|
| Añadir docs, plantillas y prompts específicos de un stack. | Introducir términos de stack/negocio en el core o en los `*.template.*` del núcleo. |
| Añadir **fronteras y gates más estrictos** (seguridad, pipelines, aprobaciones). | **Relajar** o reescribir las fronteras o el ciclo de vida del core. |
| Declarar el stack y las herramientas que asume. | Cambiar el contrato del core (eso sería MAJOR y está prohibido). |
| Requerir un rango de versión del core (`requires_protocol_version`). | Depender de otro perfil de forma oculta (las dependencias se declaran). |

## 3. El contrato `profile.manifest`

Cada perfil declara un `profile.manifest.json`. Campos (ver
[`PROFILE_TEMPLATE/profile.manifest.template.json`](PROFILE_TEMPLATE/profile.manifest.template.json)):

| Campo | Tipo | Significado |
|-------|------|-------------|
| `schema_version` | string | Versión del esquema del manifiesto (hoy `"1.0"`). |
| `profile_id` | string | Identificador estable, `kebab_case` (= nombre de carpeta). |
| `profile_version` | string SemVer | Versión **del perfil** (independiente de la del core). |
| `title` / `description` | string | Nombre legible y resumen. |
| `requires_protocol_version` | string (rango SemVer) | Versión del **core** que necesita, p.ej. `">=0.2.0 <1.0.0"`. Compatibilidad por MAJOR (ver [DECISION-0001](../Area_comun/decisions/DECISION-0001-versionado.md)). |
| `stack` | string[] | Tecnologías/plataformas que asume el perfil. |
| `provides` | object | Artefactos que aporta: `docs[]`, `templates[]`, `prompts[]` (rutas relativas al perfil). |
| `adds_boundaries` | string[] | Fronteras duras adicionales que el perfil impone (solo más estrictas). |
| `adds_quality_gates` | string[] | Gates de calidad que el perfil añade. |
| `adds_human_approval_points` | string[] | Puntos de aprobación humana que el perfil añade. |
| `depends_on_profiles` | string[] | Otros `profile_id` requeridos (normalmente vacío). |
| `maintainer` | string | Responsable del perfil. |
| `neutrality_note` | string | Confirmación explícita de que nada del perfil se filtra al core. |

El **versionado del perfil** sigue SemVer aplicado al propio perfil: MAJOR si rompe a quienes ya lo
adoptaron, MINOR si añade artefactos/fronteras compatibles, PATCH para correcciones.

## 4. Cómo instancia un proyecto: core o core + perfiles

1. **Solo core (neutral).** Sigue [`../README_INSTANCIACION.md`](../README_INSTANCIACION.md): copia
   los `*.template.*`, rellena placeholders (incluido `protocol_version`) y valida. No se adopta
   ningún perfil.
2. **Core + uno o varios perfiles.** Además de lo anterior:
   1. Copia `profiles/<profile_id>/` al repo de la instancia (o referencia la versión publicada).
   2. Comprueba que `protocol_version` de tu instancia satisface el `requires_protocol_version` del
      perfil.
   3. Aplica los artefactos del perfil (`provides`) e incorpora sus `adds_boundaries` /
      `adds_quality_gates` / `adds_human_approval_points` a tu `AGENTS.md` y `protocol.config.json`.
   4. **Registra la adopción** (sección 5).
   5. Valida en verde.

Los perfiles son **aditivos**: una instancia que adopta un perfil sigue siendo una instancia válida
del core; el perfil solo añade.

## 5. Registro de adopción de un perfil

Cada adopción debe quedar registrada en la instancia, por al menos uno de estos medios (recomendado
**ambos** la primera vez):

- **Máquina-legible:** campo `adopted_profiles` en `Area_comun/state/PROJECT_STATE.json`, p.ej.:

  ```json
  "adopted_profiles": [
    { "profile_id": "dotnet_enterprise", "profile_version": "0.1.0", "adopted_at": "YYYY-MM-DD" }
  ]
  ```

- **Decisión de la instancia:** un `Area_comun/decisions/DECISION-XXXX-*.md` en el repo del
  proyecto que justifique la adopción y sus consecuencias.

> El soporte de `adopted_profiles` en la plantilla de estado y en el validador lo añade **TASK-0007**
> (de forma aditiva: las instancias sin perfiles validan igual que hoy).

## 6. Crear un perfil nuevo

1. Copia `PROFILE_TEMPLATE/` a `profiles/<tu_profile_id>/`.
2. Rellena `profile.manifest.json` (todos los `{{...}}`).
3. Coloca docs/plantillas/prompts en sus carpetas y enlázalos en `provides`.
4. Mantén la **neutralidad del core**: nada de tu stack debe acabar fuera de `profiles/<tu_profile_id>/`.

El primer perfil de referencia es **`dotnet_enterprise`** (TASK-0006), basado en buenas prácticas
de entorno empresarial .NET. Es el ejemplo canónico de cómo se empaqueta un stack como perfil sin
tocar el núcleo.
