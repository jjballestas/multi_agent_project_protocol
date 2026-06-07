---
id: TASK-0061
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0058]
relates_to: [TASK-0019]
phase: P2
spec_id: Area_comun/specs/SPEC-0047-d2.2-upgrade-tier-aware.md
linked_decisions: [DECISION-0019, DECISION-0006, DECISION-0001]
execution_pipeline: [anadir sello runtime_version en protocol.config.json + .template (master lo fija; instancia tier runtime lo porta); extender scripts/upgrade_instance.py (+ paridad .ps1) para incluir runtime/** y .github/workflows/validate.yml en los globs adoptables PERO proponiendo deltas de runtime/** SOLO si la instancia tiene adoption_tier=runtime (si coordination/ausente, comportamiento actual sin runtime); excluir runtime/state/ runtime/runs/ __pycache__/; el reporte markdown muestra el delta de runtime y runtime_version master vs instancia solo para instancias runtime; crear examples/runtime_upgrade_cases con los casos del test plan + CI]
acceptance_criteria: [U1 instancia adoption_tier=runtime recibe propuestas de delta de runtime/** (nuevo/cambiado/eliminado) + salto de runtime_version; U2 instancia coordination/sin tier NO recibe propuestas de runtime/** (comportamiento actual); U3 inform-only (la adopcion sigue siendo decision de la instancia, DECISION-0006), aditivo, paridad py/.ps1, no se proponen runtime/state ni runtime/runs ni __pycache__; golden y suite existentes verdes; neutralidad limpia; sin secretos]
test_plan: [examples/runtime_upgrade_cases determinista: (1) instancia runtime-tier con motor desactualizado => upgrade propone deltas runtime/** + runtime_version; (2) instancia coordination-tier => upgrade NO propone runtime/** (solo coordinacion/scripts como hoy); (3) no se proponen runtime/state, runtime/runs, __pycache__; (4) inform-only: no muta la instancia; paridad py/.ps1; validador/encoding/neutralidad py verdes]
closure_criteria: [runtime_version en config live+template; upgrade_instance.py (+ paridad .ps1) tier-aware (runtime/** + CI en globs, propuesto solo si adoption_tier=runtime; excluye state/runs/pycache); reporte muestra delta runtime + runtime_version solo para runtime-tier; golden runtime_upgrade_cases verde con los 4 casos + suite + gates py; suite en CI; inform-only y aditivo (DECISION-0006); paridad py/.ps1; neutralidad limpia; sin secretos; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0061 - D2.2: upgrade_instance tier-aware + runtime_version

> `implementation` -> SDD. Rebanada D2.2 del track de distribucion (DECISION-0019). Mitiga el drift del
> tier runtime: hace que upgrade_instance propague deltas del motor a instancias runtime. Aditiva, paridad
> py/.ps1, inform-only. Ver SPEC-0047. NO requiere DECISION nueva.

## Contexto

`upgrade_instance.py` hoy NO propaga `runtime/**` => una instancia del tier runtime no recibe propuestas de
delta del motor (drift, la contra de DECISION-0019(a)). Esta tarea lo hace tier-aware.

## Alcance (ver SPEC-0047 sec.2)

1. **`runtime_version`** en config live+template (master lo fija; instancia runtime lo porta).
2. **upgrade tier-aware** (py + .ps1): `runtime/**` + CI en los globs adoptables, propuesto **solo si
   `adoption_tier=runtime`**; coordination/ausente => como hoy. Excluir state/runs/pycache.
3. **Reporte** muestra delta runtime + runtime_version (master vs instancia) solo para runtime-tier.
4. **Golden** `examples/runtime_upgrade_cases/` (4 casos) + CI.

## Restricciones

- **Inform-only** (adopcion = decision de la instancia, DECISION-0006); **aditivo**; **paridad py/.ps1**.
- NO proponer artefactos de ejecucion (`runtime/state/`, `runtime/runs/`, `__pycache__/`).
- **Neutralidad**; sin secretos.
- Fuera de alcance: aplicar/mergear automaticamente; wrapper LLM real; D2.3 docs; D2.4 SemVer; Fase B/7.
  Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

Track de distribucion: D2.1 done -> **D2.2 (esta)** -> [wrapper LLM real] -> D2.3 docs -> D2.4 SemVer ->
release v1.0. D0 (motor) ya cerrado. Codex autonomo (~100s): tomala cuando este ready.
