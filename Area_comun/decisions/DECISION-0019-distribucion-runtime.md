---
decision_id: DECISION-0019
title: Modelo de distribucion = tiers de adopcion (coordination/runtime) + scaffolding completo como motor del tier runtime
status: accepted
date: 2026-06-07
ratified_at: 2026-06-07
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0002, DECISION-0003, DECISION-0006, DECISION-0009, DECISION-0015, DECISION-0001]
phase: P2
---

# DECISION-0019 - Distribucion del runtime via tiers de adopcion (c + a)

> Estado: ACCEPTED (2026-06-07, elegida y aprobada por el operador). Cambio de boundary/contrato (AGENTS.md
> sec.4): la unidad distribuible se ofrece en **dos tiers de adopcion**; el tier runtime incluye el motor
> completo (scaffolding completo). Todo aditivo y off-by-default. SemVer MINOR (DECISION-0001). Neutral.

## Contexto

La meta del operador es que la metodologia sea **distribuible a otros proyectos**. Hoy
`scripts/new_instance.py` distribuye SOLO la capa de coordinacion (AGENTS.md, protocol.config, state JSONs
via `*.template.*`); NO distribuye el motor `runtime/` ni los `scripts/` de gates ni CI; `examples/
minimal_instance` no tiene runtime. Un adoptante recibe el contrato pero no el motor.

Para un producto distribuible, la **adopcion ligera es una ventaja estrategica**: baja la barrera de
entrada (adoptar la disciplina de coordinacion sin cargar el motor) y ofrece camino de upgrade.

## Decision

Se adopta el modelo **(c) tiers de adopcion + (a) scaffolding completo como motor del tier runtime**:

1. **Eje nuevo `adoption_tier`** en `protocol.config`, con dos valores:
   - **`coordination` (ligero, DEFAULT):** solo la capa de coordinacion (lo que se distribuye hoy =
     `examples/minimal_instance`).
   - **`runtime` (completo):** coordinacion + motor `runtime/` + `scripts/` de gates + workflow de CI +
     templates de runtime, todo **OFF-BY-DEFAULT** (runtime/tool_policy/event_auth enabled=false). El tier
     solo significa "el motor esta presente"; activarlo es decision aparte de la instancia (DECISION-0009).
2. **`new_instance.py --tier coordination|runtime`**, con **default `coordination`**. El tier runtime
   copia el motor + gates + CI + templates de runtime (excluyendo artefactos de ejecucion: `runtime/state/`,
   `runtime/runs/`, `__pycache__/`).
3. **Eje ORTOGONAL a los perfiles profesionales** (DECISION-0002/0003, que son por stack/dominio:
   dotnet_enterprise, etc.). `adoption_tier` decide que **maquinaria del protocolo** se opera;
   `adopted_profiles` decide sobre que **stack** se construye. Una instancia puede ser coordination+dotnet,
   runtime+dotnet, etc.
4. **Camino de upgrade lite -> runtime:** una instancia coordination puede subir a runtime adoptando los
   deltas del motor via `upgrade_instance.py` (tier-aware) + sellando `runtime_version`.

Opciones descartadas/diferidas: (b) paquete versionado (introduce packaging/publicacion que el repo
-Markdown+JSON+py sin build- hoy no tiene; prematuro); usar la maquinaria de perfiles profesionales para el
tier (es un eje distinto; se confundirian stack vs maquinaria).

## Invariantes / restricciones

- **Aditivo / backward-compatible:** ausencia de `adoption_tier` => `coordination` (instancias actuales no
  cambian). `examples/minimal_instance` (coordination) queda intacto.
- **Off-by-default:** el tier runtime trae el motor OFF; fallback N=2 byte-equivalente.
- **Neutralidad de dominio** en todo lo distribuido (runtime y gates). Sin secretos (claves event_auth solo
  de bootstrap/prueba).
- **Versionado:** `protocol_version` + `runtime_version`; upgrades via `upgrade_instance.py`.

## Consecuencias

Desbloquea SPEC-0044 y su backlog:
- **D2.1 (TASK-0058):** `new_instance.py --tier` + campo `adoption_tier`; el tier runtime distribuye motor +
  gates + CI + templates; `examples/full_runtime_instance` valida verde (motor off); `examples/
  minimal_instance` = coordination intacto; golden de instanciacion (ambos tiers); validador tier-aware aditivo.
- **D2.2:** `upgrade_instance.py` tier-aware (deltas de `runtime/**` solo si `adoption_tier=runtime`) +
  `runtime_version`.
- **D2.3:** docs de adopcion (tiers, como elegir, upgrade lite->full) + docs N-agente (criterio 16 SPEC-0038).
- **D2.4:** SemVer del paquete-metodologia + notas de migracion para adoptantes.

Camino futuro: si el drift entre instancias duele, evaluar (b) paquete versionado para el motor del tier
runtime (sin cambiar el modelo de tiers).

## Aprobacion humana

Requerida por ser cambio de boundary (AGENTS.md sec.4). Otorgada por el operador el 2026-06-07.
