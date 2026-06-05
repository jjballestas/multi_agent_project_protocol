# {{PROFILE_TITLE}} — perfil profesional

> Master neutral para crear un perfil. Copia `PROFILE_TEMPLATE/` a `profiles/<profile_id>/`,
> rellena todos los `{{...}}` y borra esta nota.

## Qué aporta este perfil
{{PROFILE_DESCRIPTION}}

- **Stack:** {{STACK_ITEM}}
- **Requiere core:** `{{REQUIRES_PROTOCOL_VERSION}}`
- **Versión del perfil:** `{{PROFILE_VERSION}}`

## Cuándo aplicarlo
Describe el tipo de proyecto/contexto para el que este perfil es adecuado.

## Cómo se instancia sobre el core
1. Copia `profiles/{{PROFILE_ID}}/` al repo de la instancia.
2. Verifica que el `protocol_version` de la instancia satisface `{{REQUIRES_PROTOCOL_VERSION}}`.
3. Aplica los artefactos de `provides` (docs/, templates/, prompts/).
4. Incorpora `adds_boundaries`, `adds_quality_gates` y `adds_human_approval_points` a `AGENTS.md`
   y `protocol.config.json` de la instancia.
5. Registra la adopción en `PROJECT_STATE.json` (`adopted_profiles`) y/o en una decisión.
6. Ejecuta el validador → verde.

## Estructura
```text
{{PROFILE_ID}}/
├── profile.manifest.json
├── README.md
├── docs/         ← documentación específica del stack
├── templates/    ← plantillas reutilizables del stack
└── prompts/      ← prompts maestros específicos (opcional)
```

## Frontera de neutralidad
Todo lo específico del stack vive dentro de este perfil. **Nada** de aquí debe filtrarse al core
del protocolo ni a sus `*.template.*`.
