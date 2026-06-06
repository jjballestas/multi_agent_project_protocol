---
spec_id: SPEC-0042-fase5.2-tool-policy
task_id: TASK-0056
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0015, DECISION-0018]
relates_to: [SPEC-0038, SPEC-0040]
---

> Rebanada 2 de la Fase 5 (SPEC-0040 sec.3). SPEC-0038 sec.8.3/8.4, D-13, addenda A12. Aditiva,
> deny-by-default, config-gated, fallback N=2 byte-equivalente. NO requiere DECISION nueva (autorizada por
> DECISION-0015 + OK operador). Si fuerza un cambio incompatible de contrato => blocked + DECISION.

# SPEC-0042 - Fase 5.2: tool-policy deny-by-default + clasificacion de acciones

## 1. Problema

La rebanada 5.1 (guardrails, TASK-0054) fijo el invariante "ningun contenido controlado por el actor decide
seguridad". Falta el control de **permiso de herramienta** y de **tipo de accion**: hoy no hay allowlist
por-herramienta atada a capacidad + scope (SPEC-0038 sec.8.4, D-13), ni gates por tipo de accion
(lectura / escritura local / ejecucion local / cambio de contrato / accion externa / accion sensible,
sec.8.3). Addenda A12: una **tool-policy deny-by-default minima es obligatoria ANTES** de habilitar
cualquier tool con efecto externo real.

## 2. Alcance (TASK-0056)

1. **Config `tool_policy` (deny-by-default)** en `protocol.config.json` + `.template`: allowlist
   por-herramienta atada a capacidad + scope de tarea (no un enum grueso). **Ausencia de `tool_policy` =
   comportamiento actual** (no hay tools con efecto externo en replay => byte-equivalente).
2. **Modulo `runtime/tool_policy.py`** (aditivo):
   - `is_tool_allowed(agent, tool, task_scope, registry, config) -> bool` deny-by-default.
   - `classify_action(action) -> tipo` (`read` / `local_write` / `local_exec` / `contract_change` /
     `external` / `sensitive`).
   - `gate_for_action(tipo) -> gate` (automatico+log / diff-obligatorio / DECISION+review+QA /
     human-approval), segun la tabla de SPEC-0038 sec.8.3.
3. **Cableado aditivo en `runtime/turn_validate.py`** (reusar el patron de 5.1: errores de seguridad ->
   semanticos): un agente que usa una tool fuera de su allowlist => **rechazado y registrado** (p.ej.
   `security.tool_denied`); cambio de contrato sin `decision_refs` => falla; accion externa/sensible =>
   gate humano (`gate.human_required`).
4. **Golden `examples/runtime_tool_policy_cases/`** + step de CI.

## 3. Invariantes

- **TP1:** deny-by-default: una tool no listada en la allowlist del agente (por capacidad+scope) NO se
  ejecuta y queda registrada.
- **TP2:** el tipo de accion determina el gate (sec.8.3); cambio de contrato exige DECISION+review+QA;
  accion sensible/externa exige aprobacion humana.
- **TP3:** aditivo/reversible: sin `tool_policy` declarada (o sin tools) el comportamiento es
  byte-equivalente al actual; fallback N=2 intacto.

## 4. Tests (deterministas, sin red)

1. agente sin permiso para tool X => NO ejecuta, queda registrado (`security.tool_denied`).
2. cambio de contrato (schema/API) sin `decision_refs` => falla.
3. accion sensible (credenciales/produccion/borrado) => pausada (`human_required`).
4. accion dentro de policy y tipo permitido => pasa.
5. sin `tool_policy` / sin tools => byte-equivalente; fallback N=2 intacto.
6. determinismo (sin reloj/red/random).

## 5. Fuera de alcance

- 5.3 (firma del envelope, SPEC-0043), Fase B (SPEC-0039), Fase 6/7.
- Sandbox de side-effects real (se activa con superficie externa real).
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer

- MINOR (config + modulo aditivos; default = comportamiento actual).
