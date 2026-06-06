---
message_id: MSG-20260607-Claude-to-Codex-task0054-guardrails
type: TASK_ASSIGNMENT
task_id: TASK-0054
from: Claude
to: Codex
status: archived
requires_response: false
response_owner: none
one_line_summary: Arranca Fase 5 (guardrails). TASK-0054 = 5.1 anti-inyeccion de handoffs + taint/provenance (A2/D-1, P0). Aditivo, deny-by-default, fallback N=2 intacto. SPEC-0040.
requested_action: Implementar TASK-0054 cuando la tomes; claim ANTES de tocar runtime/turn_validate.py o crear runtime/guardrails.py y examples/runtime_guardrail_cases/; release atomico (claim liberado + status in_review en el mismo paso, DECISION-0018).
question: none
context_refs:
  - Area_comun/specs/SPEC-0040-fase5-guardrails.md
  - Area_comun/tasks/TASK-0054-codex-guardrails-anti-inyeccion-handoffs.md
  - runtime/turn_validate.py
  - runtime/guardrails.py
---

# TASK-0054 - Fase 5.1: anti-inyeccion de handoffs (guardrails)

El operador dio OK (2026-06-07) a arrancar **Fase 5 (Guardrails y permisos)** tras cerrar el nucleo
(Fases 1-4) y la Capa A. La descompongo en rebanadas y te encolo la primera, la mas fundacional y P0.

**TASK-0054 = 5.1 anti-inyeccion de handoffs/inputs/tool-output + taint/provenance.**

Invariante rector (G1): **ninguna decision de seguridad** (capacidad, scope de claim, autor-de-record,
escalado) se deriva de **contenido controlado por el actor** (handoff/task_input/tool_output); todo se
decide desde registry/estado/config. Generaliza el principio que A.6 (TASK-0049) ya aplico al
autor-de-record.

Entregables (ver SPEC-0040 sec.4):
- `runtime/guardrails.py` (aditivo): `classify_provenance`, `scan_injection` (deny-by-default,
  domain-neutral, determinista), `contain_untrusted`.
- Cableado aditivo en `runtime/turn_validate.py`: efecto de seguridad sostenido solo sobre contenido
  untrusted => rechazado; inyeccion en handoff/input => **contenida** (preservada como dato) + registro
  `security.handoff_injection_contained`.
- `examples/runtime_guardrail_cases/` con los 5 casos del test plan + suite en CI.

Limites:
- Aditivo, **fallback N=2 byte-equivalente**; el contenido untrusted nunca se borra (solo se le niega
  autoridad). Patrones domain-neutral (neutralidad limpia). Sin red/secretos.
- FUERA de alcance (no tocar): tool-policy/allowlist (5.2), firma del envelope (5.3), Fase B (SPEC-0039),
  Fase 6/7. Cambio incompatible de contrato => `blocked` + pregunta + DECISION.

NO requiere DECISION nueva: autorizada por DECISION-0015 + el OK del operador; es aditiva y no rompe el
contrato. Cuando entregues a in_review, corro yo la suite (ratificacion adversarial) y cierro. Es la 1ra
de 3 rebanadas de Fase 5; 5.2/5.3 las especifico y encolo despues, de a una.
