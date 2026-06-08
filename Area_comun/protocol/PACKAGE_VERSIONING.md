# PACKAGE_VERSIONING.md - Versionado del paquete-metodologia

Este documento consolida como debe leer una instancia adoptante las versiones del paquete
`multi_agent_project_protocol`. No publica una release ni cambia ningun numero de version; solo
explica las reglas de adopcion y migracion.

Fuentes autoritativas:

- `protocol_version`: [DECISION-0001](../decisions/DECISION-0001-versionado.md) y
  [CHANGELOG.md](../../CHANGELOG.md).
- `runtime_version` y tiers: [DECISION-0019](../decisions/DECISION-0019-distribucion-runtime.md) y
  [README_INSTANCIACION.md](../../README_INSTANCIACION.md).
- `schema_version` del turno: [SCHEMA_VERSIONING.md](SCHEMA_VERSIONING.md) y
  [runtime/turn_schema.json](../../runtime/turn_schema.json).
- `profile_version`: [DECISION-0003](../decisions/DECISION-0003-adopted-profiles-contract.md) y
  [profiles/README.md](../../profiles/README.md).
- Operacion runtime N-agente y wrapper real: [N_AGENT_RUNTIME.md](N_AGENT_RUNTIME.md) y
  [DECISION-0021](../decisions/DECISION-0021-activacion-wrapper-llm.md).
- Cadena de release verificable: [RELEASE_ENGINEERING.md](RELEASE_ENGINEERING.md) y
  [DECISION-0023](../decisions/DECISION-0023-firma-release.md).

## Modelo

Una instancia adopta el protocolo como un conjunto de contratos versionados, no como una libreria
unica. El core de coordinacion, el motor runtime, el schema de turnos y los perfiles pueden avanzar
a ritmos distintos, aunque una release del repositorio pueda empaquetar cambios de varios ejes.

La instancia registra lo que adopta en sus propios archivos vivos y decide cuando migrar. El master
del protocolo no se propaga automaticamente.

## Cuatro ejes

| Eje | Donde se declara | Que gobierna | A quien aplica |
|---|---|---|---|
| `protocol_version` | `protocol.config.json` | Contrato de coordinacion: estructura, lifecycle, plantillas, estado, mailbox, handoffs y validadores. | Todos los tiers. |
| `runtime_version` | `protocol.config.json` | Motor local `runtime/`, gates, CI adoptable y comportamiento operativo del tier runtime. | Solo instancias `adoption_tier: runtime`. |
| `schema_version` | `runtime/turn_schema.json` | Contrato JSON de un reporte de turno y sus consumidores (`turn_validate`, `apply`, adapters y golden cases). | Instancias runtime y productores de turn reports. |
| `profile_version` | `profiles/<id>/profile.manifest.json` y `PROJECT_STATE.json#adopted_profiles` | Perfil profesional opcional y sus fronteras/gates/plantillas. | Solo instancias que adoptan ese perfil. |

Reglas de lectura:

- `protocol_version` es el eje base. Si cambia de MAJOR, la instancia debe migrar de forma explicita.
- `runtime_version` no tiene efecto practico en una instancia `coordination`; en `runtime` indica el
  nivel del motor que la instancia porta o compara.
- `schema_version` es independiente del release del repo. Un cambio puede ser compatible con el
  protocolo y aun asi requerir que productores/consumidores de turn reports entiendan campos nuevos.
- `profile_version` se fija por perfil adoptado. El perfil tambien declara `requires_protocol_version`.

## SemVer para el adoptante

Desde la perspectiva de una instancia, el impacto se clasifica por el contrato que la instancia debe
operar despues de adoptar el cambio.

| Incremento | Significado para la instancia | Ejemplos |
|---|---|---|
| `MAJOR` | Requiere migracion o aprobacion explicita porque una instancia valida podria dejar de validar u operar igual. | Cambiar lifecycle, exigir un campo nuevo, cambiar semantica de un estado, hacer obligatorio un runtime antes opcional, o subir un perfil con frontera nueva. |
| `MINOR` | Agrega capacidad compatible. La instancia existente sigue siendo valida si no adopta la nueva capacidad. | Nuevo documento de protocolo, campo opcional, nuevo perfil, nuevo tier/runtime off-by-default, nuevo campo opcional del turn schema. |
| `PATCH` | Corrige sin cambiar contrato. | Typos, aclaraciones, links, bugfix de validador que no cambia que se acepta o rechaza. |

Regla de desempate: si una migracion podria romper una instancia existente, tratarla como `MAJOR` y
pedir decision. Para releases `v1.0.0` o superiores, DECISION-0001 exige aprobacion humana antes del
tag aunque el contenido sea estabilizacion del contrato.

## Compatibilidad por tier

`adoption_tier` define cuanta maquinaria del protocolo porta la instancia:

| Tier | Versiones que debe mirar | Compatibilidad esperada |
|---|---|---|
| `coordination` | `protocol_version`; `profile_version` si adopta perfiles. | No porta `runtime/`. La ausencia de `adoption_tier` equivale a `coordination`. `upgrade_instance.py` no propone deltas de runtime para este tier. |
| `runtime` | `protocol_version`, `runtime_version`, `schema_version`; `profile_version` si adopta perfiles. | Porta motor, gates y CI, pero todo nace off-by-default. `runtime_version` se compara contra el master; `schema_version` rige los turn reports. |

Cambiar de `coordination` a `runtime` es una adopcion de capacidad, no una activacion automatica del
motor. Despues del cambio, `runtime.enabled`, `tool_policy`, `event_auth` y `runtime.real_invoker`
siguen controlados por la configuracion y por decisiones de la instancia.

## Release verificable

Al publicar una version del paquete-metodologia, el emisor puede generar una cadena verificable con
SBOM, manifiesto, provenance y firma. Esa cadena no cambia los ejes de version; los registra como datos del
artefacto para que el adoptante sepa exactamente que contrato esta verificando.

La guia operativa esta en [RELEASE_ENGINEERING.md](RELEASE_ENGINEERING.md). La regla de seguridad central es
DECISION-0023: el material real de firma pertenece al emisor o a su CI y nunca se commitea. Sin firma/material
publico, `verify_release` comprueba integridad de contenido; con firma y `--pubkey`, tambien comprueba
autenticidad para el backend declarado.

## Migracion

### Actualizar dentro del mismo tier

1. Leer [CHANGELOG.md](../../CHANGELOG.md) entre la version adoptada y la version objetivo.
2. Ejecutar `upgrade_instance.py` contra el master para obtener un reporte informativo de deltas.
3. Separar cambios de contrato (`protocol_version`) de cambios de motor (`runtime_version`), schema
   (`schema_version`) y perfiles (`profile_version`).
4. Registrar una decision de instancia cuando el cambio sea incompatible, toque fronteras, active
   runtime/agentes reales o actualice un perfil con impacto operativo.
5. Aplicar los deltas elegidos en la instancia y correr sus gates de validacion.

### Subir de coordination a runtime

Para una instancia nueva, crearla con:

```powershell
python scripts\new_instance.py ... --tier runtime
```

Para una instancia existente:

1. Registrar una decision de adopcion del tier runtime.
2. Cambiar `adoption_tier` a `runtime` y sellar `runtime_version`.
3. Adoptar los deltas que `upgrade_instance.py` reporte para `runtime/**`, scripts de gates y CI.
4. Confirmar que no se adoptan artefactos de ejecucion (`runtime/state/`, `runtime/runs/`,
   `__pycache__/`).
5. Mantener el motor apagado hasta que exista una decision separada para operarlo.
6. Validar la instancia completa.

### Activar agentes reales

El wrapper CLI real pertenece al tier runtime, pero se distribuye apagado. Activarlo exige decision
propia de la instancia, `runtime.enabled:true`, `runtime.real_invoker.enabled:true`, registro de
aprobacion, flags de ejecucion real y limites operativos. Ver
[DECISION-0021](../decisions/DECISION-0021-activacion-wrapper-llm.md) y
[README_INSTANCIACION.md](../../README_INSTANCIACION.md#operar-agentes-reales).

### Actualizar perfiles

Un perfil se adopta por `profile_id` + `profile_version`. Para subirlo:

1. Verificar que `requires_protocol_version` satisface el `protocol_version` de la instancia.
2. Actualizar `PROJECT_STATE.json#adopted_profiles`.
3. Registrar decision si es primera adopcion, MAJOR del perfil o cambio de frontera/gate.
4. Validar que el manifest local y el estado coinciden.

## Politica de cambios incompatibles

Un cambio incompatible no se aplica silenciosamente. Debe quedar registrado como decision de la
instancia adoptante y, cuando afecte boundaries, aprobacion humana. Si durante una tarea aparece
una incompatibilidad no prevista, la tarea pasa a `blocked` con una pregunta concreta.

El release `v1.0.0` del protocolo queda fuera de este documento: el bump de `protocol_version`, la
entrada de CHANGELOG, el reporte y el tag son un paso de release separado con aprobacion humana.
