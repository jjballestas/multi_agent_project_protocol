---
id: TASK-0056
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
closed_by: Claude (ratificacion adversarial)
depends_on: [TASK-0054]
relates_to: [TASK-0049, TASK-0046]
phase: P2
spec_id: Area_comun/specs/SPEC-0042-fase5.2-tool-policy.md
linked_decisions: [DECISION-0015, DECISION-0018]
execution_pipeline: [anadir config tool_policy deny-by-default en protocol.config.json + .template (ausencia = comportamiento actual); crear runtime/tool_policy.py con is_tool_allowed(agent,tool,task_scope,registry,config) deny-by-default, classify_action(action)->read/local_write/local_exec/contract_change/external/sensitive, gate_for_action(tipo)->automatico+log/diff-obligatorio/DECISION+review+QA/human-approval (tabla SPEC-0038 sec.8.3); cablear aditivo en turn_validate.py (patron de 5.1: errores de seguridad->semanticos): tool fuera de allowlist => rechazado + registrado security.tool_denied; cambio de contrato sin decision_refs => falla; accion externa/sensible => gate humano (gate.human_required); crear examples/runtime_tool_policy_cases/ con los 6 casos del test plan + step de CI]
acceptance_criteria: [TP1 deny-by-default - una tool no listada en la allowlist del agente (por capacidad+scope) NO se ejecuta y queda registrada (security.tool_denied); TP2 - el tipo de accion determina el gate (sec.8.3): cambio de contrato sin decision_refs falla, accion sensible/externa exige aprobacion humana; TP3 - aditivo/reversible: sin tool_policy declarada o sin tools el comportamiento es BYTE-EQUIVALENTE al actual y el fallback N=2 se preserva; los golden y la suite runtime existentes siguen verdes; domain-neutral (tipos de accion genericos, sin terminos de negocio); sin red; sin secretos; neutralidad limpia]
test_plan: [examples/runtime_tool_policy_cases/ determinista (sin red/reloj/random): (1) agente sin permiso para tool X => NO ejecuta, registrado security.tool_denied; (2) cambio de contrato sin decision_refs => falla; (3) accion sensible => pausada human_required; (4) accion dentro de policy y tipo permitido => pasa; (5) sin tool_policy/sin tools => byte-equivalente, fallback N=2; (6) determinismo dos corridas mismo resultado; suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [config tool_policy deny-by-default (ausencia = comportamiento actual) en live + template; runtime/tool_policy.py aditivo (is_tool_allowed/classify_action/gate_for_action); cableado en turn_validate sin romper validaciones actuales; golden examples/runtime_tool_policy_cases/ verde con los 6 casos + suite runtime completa + gates py (validador/encoding/neutralidad); suite en CI; fallback N=2 byte-equivalente; neutralidad limpia; sin red/secretos; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0056 - Fase 5.2: tool-policy deny-by-default + clasificacion de acciones

> `implementation`/security -> SDD. Rebanada 2 de Fase 5 (SPEC-0040 sec.3). Aditiva, deny-by-default,
> config-gated, fallback N=2 intacto. Ver SPEC-0042. NO requiere DECISION nueva (autorizada por
> DECISION-0015 + OK operador).

## Contexto

5.1 (TASK-0054) fijo el invariante "ningun contenido controlado por el actor decide seguridad". Falta el
control de PERMISO DE HERRAMIENTA (allowlist por-herramienta atada a capacidad+scope, D-13) y de TIPO DE
ACCION (gates por read/local_write/local_exec/contract_change/external/sensitive, sec.8.3). A12: una
tool-policy deny-by-default minima es obligatoria ANTES de habilitar cualquier tool con efecto externo.

## Alcance

1. **Config `tool_policy` deny-by-default** (live + template); **ausencia = comportamiento actual**.
2. **`runtime/tool_policy.py`**: `is_tool_allowed`, `classify_action`, `gate_for_action`.
3. **Cableado aditivo en `turn_validate.py`** (patron 5.1): tool fuera de allowlist => rechazado +
   `security.tool_denied`; cambio de contrato sin `decision_refs` => falla; accion externa/sensible =>
   `gate.human_required`.
4. **Golden `examples/runtime_tool_policy_cases/`** (6 casos) + CI.

## Restricciones

- **Aditivo**; deny-by-default aplica solo a tools declaradas (no rompe turnos actuales sin tools);
  **fallback N=2 byte-equivalente**.
- **Domain-neutral** (tipos de accion genericos); sin red; sin secretos; neutralidad limpia.
- Fuera de alcance: 5.3 (firma del envelope), Fase B, Fase 6/7. Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

Rebanada 2 de 3 de Fase 5: 5.1 (done) -> **5.2 (esta)** -> 5.3 (firma del envelope, ya disenada, se encola
despues de cerrar esta). Codex autonomo (~100s): tomala cuando vuelvas (offline hasta ~1:45 por creditos).
