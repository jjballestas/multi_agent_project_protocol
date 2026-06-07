---
id: TASK-0058
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
closed_by: Claude (ratificacion adversarial)
depends_on: []
relates_to: [TASK-0019]
phase: P2
spec_id: Area_comun/specs/SPEC-0044-distribucion-runtime.md
linked_decisions: [DECISION-0019, DECISION-0009, DECISION-0002, DECISION-0006]
execution_pipeline: [anadir campo adoption_tier (coordination|runtime; ausente=>coordination) a protocol.config.json + .template; anadir flag --tier coordination|runtime a scripts/new_instance.py con DEFAULT coordination; en tier coordination comportamiento actual; en tier runtime copiar ademas runtime/ EXCLUYENDO runtime/state/ runtime/runs/ y __pycache__/, los scripts/ de gates (validate_collaboration_state scan_encoding scan_domain_neutrality prune_state, py y ps1), un .github/workflows/validate.yml template, y templates de runtime (turn_schema + bloques runtime/tool_policy/event_auth OFF), y escribir adoption_tier:runtime en la config renderizada; crear examples/full_runtime_instance generada con --tier runtime que valida verde (motor presente pero OFF); dejar examples/minimal_instance como tier coordination INTACTO; hacer el validador tier-aware aditivo en py y ps1 (si adoption_tier=runtime espera runtime/ presente; si coordination/ausente comportamiento actual); crear golden de instanciacion que genere ambos tiers en tmp y verifique el test plan; registrar la suite en CI]
acceptance_criteria: [DI1 el tier runtime produce instancia autocontenida (motor runtime/ + scripts de gates + CI + turn_schema); DI2 off-by-default - runtime/tool_policy/event_auth OFF en la instancia runtime nueva, fallback N=2 byte-equivalente; DI3 neutralidad, sin secretos, NO se copian runtime/state ni runtime/runs ni __pycache__; DI4 el tier coordination (default) y examples/minimal_instance quedan INTACTOS (camino ligero); DI5 adoption_tier es ortogonal a adopted_profiles (no se mezclan); el validador/encoding/neutralidad corren VERDE sobre ambas instancias generadas; determinismo en el copiado; suite runtime existente sin regresion; paridad py/.ps1 del validador tier-aware]
test_plan: [golden de instanciacion determinista: (1) --tier coordination (o sin flag) => instancia coordination sin runtime, validador verde; (2) --tier runtime => instancia con runtime/ + scripts de gates + CI + adoption_tier:runtime y los 3 bloques OFF, validador/encoding/neutralidad verde sobre la instancia; (3) tier runtime NO copia runtime/state, runs, __pycache__; (4) examples/minimal_instance sigue verde (DI4); (5) dos generaciones identicas por tier (determinista); suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [adoption_tier en config live+template (ausente=>coordination); new_instance.py --tier coordination|runtime (default coordination) que en runtime copia motor+gates+CI+templates excluyendo state/runs/pycache y escribe adoption_tier:runtime; examples/full_runtime_instance valida verde (motor off); examples/minimal_instance intacto (DI4); validador tier-aware aditivo con paridad py/.ps1; golden de instanciacion verde con los 5 casos (ambos tiers); suite runtime completa + gates py verdes; suite en CI; off-by-default y fallback N=2; ortogonalidad con adopted_profiles (DI5); neutralidad limpia; sin secretos; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0058 - D2.1: new_instance tier-aware (distribuye el motor en el tier runtime)

> `implementation` -> SDD. Primera rebanada de la distribucion (DECISION-0019 = (c) tiers + (a) scaffolding
> completo como motor del tier runtime; aprobada por el operador). Aditiva, off-by-default, neutral. Ver
> SPEC-0044. NO requiere DECISION nueva (DECISION-0019 cubre el boundary).

## Contexto

DECISION-0019 distribuye la metodologia en dos **tiers de adopcion**: `coordination` (ligero, DEFAULT) y
`runtime` (completo, trae el motor). Hoy new_instance.py no conoce tiers y solo produce coordination; no
existe ejemplo del tier runtime. El tier es un eje ORTOGONAL a los perfiles profesionales (stack).

## Alcance (ver SPEC-0044 sec.4)

1. **`adoption_tier`** en config live+template (ausente => coordination).
2. **`new_instance.py --tier coordination|runtime`** (DEFAULT coordination):
   - coordination: comportamiento actual.
   - runtime: copia ademas `runtime/` (EXCLUYE state/runs/pycache) + `scripts/` de gates (py+ps1) +
     `.github/workflows/validate.yml` + templates de runtime (turn_schema + bloques runtime/tool_policy/
     event_auth OFF); escribe `adoption_tier:runtime`.
3. **`examples/full_runtime_instance`** (generada con --tier runtime) valida verde (motor OFF).
4. **`examples/minimal_instance`** = tier coordination, INTACTO (DI4).
5. **Validador tier-aware aditivo** (paridad py/.ps1): runtime => espera runtime/ presente; coordination/
   ausente => como hoy.
6. **Golden de instanciacion** (ambos tiers) + CI.

## Restricciones

- **Aditivo / off-by-default** (DI2); **fallback N=2 byte-equivalente**; **minimal_instance intacto** (DI4).
- **NO copiar** `runtime/state/`, `runtime/runs/`, `__pycache__/` (DI3).
- **adoption_tier ortogonal a adopted_profiles** (DI5) - no tocar la maquinaria de perfiles profesionales.
- **Neutralidad**; **sin secretos**; determinismo; **paridad py/.ps1** del validador.
- Fuera de alcance: D2.2 (upgrade tier-aware + runtime_version), D2.3 (docs), D2.4 (versionado); activar el
  motor (gateado, DECISION-0009). Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

Primera de 4 rebanadas (SPEC-0044 sec.3): D2.1 (esta) -> D2.2 (upgrade tier-aware) -> D2.3 (docs) -> D2.4
(SemVer del paquete). Se encolan de a una. Codex autonomo (~100s): tomala cuando este ready.
