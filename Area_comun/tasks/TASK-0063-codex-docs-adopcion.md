---
id: TASK-0063
owner: Codex
status: done
type: documentation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
closed_by: Claude (ratificacion adversarial)
depends_on: [TASK-0058, TASK-0061, TASK-0062]
relates_to: [TASK-0013]
phase: P2
spec_id: Area_comun/specs/SPEC-0049-d2.3-docs-adopcion.md
linked_decisions: [DECISION-0019, DECISION-0021, DECISION-0015]
execution_pipeline: [ampliar README_INSTANCIACION.md sin duplicar lo ya escrito por el wrapper (TASK-0062): los dos tiers de adopcion coordination(default)/runtime (DECISION-0019) y como elegir/instanciar (new_instance.py --tier); upgrade tier-aware (upgrade_instance.py + runtime_version); operar agentes reales via wrapper (DECISION-0021: runtime.enabled + real_invoker registro + flags --allow-real-invoker/--llm-command|--llm-preset/--once + limites budget/tool-policy/guardrails, off-by-default, sin autonomia, sin secretos); crear docs N-agente del criterio 16 SPEC-0038 (p.ej. Area_comun/protocol/N_AGENT_RUNTIME.md): registry/capacidades, routing weighted-least-loaded+fairness, maquina Review/QA, guardrails (anti-inyeccion/tool-policy/firma envelope), seguridad/limites, handoffs autocontenidos, observabilidad y budget; enlazar a runtime/README sin duplicar; mantener neutralidad y sin secretos]
acceptance_criteria: [README_INSTANCIACION cubre los 2 tiers (elegir/instanciar) + upgrade tier-aware + operar agentes reales via wrapper (pasos de activacion DECISION-0021, off-by-default, limites, sin secretos, sin autonomia); docs N-agente criterio 16 presentes y coherentes con el codigo (registry/routing/estados/guardrails/seguridad/handoffs/observabilidad/budget); sin duplicacion con runtime/README, enlaces validos; neutralidad de dominio limpia; sin secretos; validador/encoding/neutralidad py verdes; es solo documentacion (no cambia runtime)]
expected_output: README_INSTANCIACION.md ampliado + documento N-agente (criterio 16) publicable, neutral, coherente con el codigo y sin duplicacion; gates verdes.
test_plan: [validador/encoding/neutralidad py verdes sobre el repo; revision de coherencia docs<->codigo (tiers, flags de activacion, criterio 16); enlaces validos; suite runtime sin tocar (es documentacion)]
question_to_resolve: ninguna (alcance claro en SPEC-0049); si surge ambiguedad de contrato => blocked + pregunta.
closure_criterion: README_INSTANCIACION + docs N-agente completos, coherentes, neutrales, sin secretos, sin duplicacion; gates py verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [README_INSTANCIACION ampliado (tiers+upgrade+operar agentes reales) + docs N-agente criterio 16 publicables y coherentes; sin duplicacion; enlaces validos; neutralidad limpia; sin secretos; gates py verdes; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0063 - D2.3: documentacion de adopcion + docs N-agente (criterio 16)

> `documentation` -> SDD ligero. Rebanada D2.3 del track de distribucion = v1.0. Documenta como adoptar y
> operar la metodologia. Neutral, sin secretos, no toca runtime. Ver SPEC-0049.

## Contexto

Para distribuir, un humano externo debe poder adoptar/operar la metodologia. Faltan: guia de adopcion por
tiers + upgrade + operacion de agentes reales, y los docs N-agente del criterio 16 de SPEC-0038. El wrapper
(TASK-0062) ya toco minimamente README_INSTANCIACION/runtime/README; AMPLIAR sin duplicar.

## Alcance (ver SPEC-0049 sec.2)

1. **README_INSTANCIACION.md** (ampliar): tiers coordination/runtime + como elegir/instanciar (--tier) +
   upgrade tier-aware + OPERAR AGENTES REALES via wrapper (activacion DECISION-0021, off-by-default,
   limites, sin secretos, sin autonomia).
2. **Docs N-agente (criterio 16)**: documento publicable (p.ej. Area_comun/protocol/N_AGENT_RUNTIME.md) con
   registry/routing/estados/guardrails/seguridad/handoffs/observabilidad/budget.
3. Sin duplicar runtime/README; enlazar. Neutralidad; sin secretos.

## Restricciones

- Solo documentacion (no cambia runtime); **neutralidad de dominio**; **sin secretos**; coherente con el
  codigo; sin duplicacion.
- Fuera de alcance: D2.4 (SemVer del paquete), DECISION-0020, Fase B/7. Cambio incompatible => `blocked`.
- **Handoff autocontenido** (incluir handoff + in-review en el mismo paso del flip); **release atomico**
  (DECISION-0018).

## Nota

v1.0: D0 + D2.1 + D2.2 + wrapper done -> **D2.3 (esta)** -> D2.4 SemVer del paquete -> DECISION-0020 + fix
prune -> RELEASE v1.0 (aprobacion humana). Codex autonomo (~100s): tomala cuando este ready.
