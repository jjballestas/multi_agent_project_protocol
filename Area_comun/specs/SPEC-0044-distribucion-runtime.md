---
spec_id: SPEC-0044-distribucion-runtime
task_id: TASK-0058
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0019, DECISION-0002, DECISION-0003, DECISION-0006, DECISION-0009]
relates_to: [SPEC-0038]
---

> SPEC de la distribucion del runtime via TIERS DE ADOPCION (consecuencia de DECISION-0019 = (c) tiers +
> (a) scaffolding completo como motor del tier runtime). Aditiva, off-by-default, neutral. Decompone D2 en
> rebanadas; D2.1 = TASK-0058.

# SPEC-0044 - Distribucion del runtime via tiers de adopcion

## 1. Problema

Tras DECISION-0019, la metodologia se distribuye en dos **tiers de adopcion**: `coordination` (ligero,
default) y `runtime` (completo, trae el motor). Hoy `new_instance.py` solo produce el equivalente al tier
coordination y no conoce tiers; no existe ejemplo del tier runtime; `upgrade_instance.py` no propaga
`runtime/`. Hay que implementar el eje de tiers manteniendo todo aditivo, off-by-default y neutral, y SIN
tocar la maquinaria de perfiles profesionales (eje ortogonal).

## 2. Eje `adoption_tier` (ortogonal a `adopted_profiles`)

- Campo `adoption_tier` en `protocol.config.json`/`.template`: `"coordination" | "runtime"`.
- **Ausencia => `coordination`** (backward-compatible; instancias actuales y `minimal_instance` no cambian).
- Ortogonal a `adopted_profiles` (DECISION-0002/0003, por stack). Combinaciones validas: coordination,
  runtime, coordination+<profile>, runtime+<profile>.
- El tier `runtime` trae el motor pero **OFF** (runtime/tool_policy/event_auth enabled=false): el tier dice
  "motor presente", no "motor activo" (activar = DECISION-0009 de la instancia).

## 3. Decomposicion (D2)

| # | Rebanada | Entregable | Estado |
|---|----------|-----------|--------|
| D2.1 | new_instance tier-aware: distribuye motor+gates+CI en tier runtime | new_instance.py --tier + adoption_tier + examples/full_runtime_instance verde + golden | **TASK-0058 (esta)** |
| D2.2 | upgrade_instance tier-aware + runtime_version | upgrade_instance.py (deltas runtime/** si tier=runtime) + runtime_version sellado | por encolar |
| D2.3 | Docs de adopcion + docs N-agente | README_INSTANCIACION (tiers, elegir, upgrade) + criterio 16 SPEC-0038 | por encolar |
| D2.4 | SemVer del paquete-metodologia + migracion | versionado/CHANGELOG + notas para adoptantes | por encolar |

## 4. D2.1 - Alcance (TASK-0058)

1. **`scripts/new_instance.py`**: anadir `--tier coordination|runtime` (**default coordination**).
   - `coordination`: comportamiento actual (capa de coordinacion).
   - `runtime`: ademas copia `runtime/` (EXCLUYENDO `runtime/state/`, `runtime/runs/`, `__pycache__/`) +
     `scripts/` de gates (validate_collaboration_state, scan_encoding, scan_domain_neutrality, prune_state;
     py y ps1) + `.github/workflows/validate.yml` template + templates de runtime (turn_schema + bloques
     `runtime`/`tool_policy`/`event_auth` OFF). Escribe `adoption_tier` en la config renderizada.
2. **`protocol.config.template.json` + `protocol.config.json`**: anadir `adoption_tier` (ausente=>coordination).
3. **`examples/full_runtime_instance`**: instancia de referencia generada con `--tier runtime`, que **valida
   verde** (motor presente pero OFF).
4. **`examples/minimal_instance`**: queda como tier coordination (anotar `adoption_tier:"coordination"` o
   dejar ausente=default); INTACTO.
5. **Validador tier-aware (aditivo, paridad py/.ps1):** si `adoption_tier=runtime` => espera `runtime/`
   presente; si `coordination`/ausente => comportamiento actual. No rompe instancias existentes.
6. **Golden de instanciacion** + CI: genera ambos tiers en tmp y verifica (4.x test plan).

## 5. Invariantes

- **DI1:** el tier runtime produce una instancia autocontenida (motor + gates + CI).
- **DI2:** off-by-default (motor OFF en la instancia nueva); fallback N=2 byte-equivalente; una instancia
  runtime que no activa el motor se comporta como una coordination.
- **DI3:** neutralidad; sin secretos; NO se copian `runtime/state`, `runtime/runs`, `__pycache__`.
- **DI4:** el tier coordination (default) y `examples/minimal_instance` quedan intactos (camino ligero).
- **DI5:** `adoption_tier` es ortogonal a `adopted_profiles` (no se mezclan).

## 6. Tests (deterministas)

1. `--tier coordination` (o sin flag) => instancia = coordination (sin runtime); validador verde.
2. `--tier runtime` => instancia con runtime/ + gates + CI + `adoption_tier:runtime`, motor OFF; validador/
   encoding/neutralidad verde sobre la instancia generada.
3. tier runtime NO copia runtime/state, runs, __pycache__.
4. `examples/minimal_instance` sigue verde (DI4).
5. determinismo: dos generaciones identicas por tier (sin reloj/random).

## 7. Fuera de alcance (D2.1)

- D2.2/D2.3/D2.4 (rebanadas siguientes). Activar el motor en una instancia (gateado, DECISION-0009).
- Cambio incompatible de contrato => blocked + DECISION.

## 8. SemVer

- MINOR (eje de tiers aditivo; el camino coordination preexistente se preserva).
