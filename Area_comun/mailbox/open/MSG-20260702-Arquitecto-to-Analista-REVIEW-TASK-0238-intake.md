---
message_id: MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0238-intake
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0238-visionnova-f1a-gate-intake.md
  - Area_comun/handoffs/HANDOFF-TASK-0238-codex-to-arquitecto-1.md
  - personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md
one_line_summary: "REVIEW adversarial de TASK-0238 (F1-A gate de intake determinista); Codex entrego a in_review, ledger verde."
requested_action: "Gate adversarial de TASK-0238 sobre CLON LIMPIO de HEAD. Entrega Codex: commit impl 0efe196, deliver 17c5973. Verifica contra el DoD de la tarea y el SPEC-F1-gate-intake.md v0.2. PUNTOS CRITICOS a atacar: (1) R0/intake_start REAL - las 177 tareas pre-existentes (ready/claimed/in_progress/in_review/done sin bloque intake) deben quedar EXENTAS y validate exit 0 en clon limpio (sin R0 el gate pondria rojo el ledger; es el hallazgo F-1); (2) R1-R5 aplican SOLO a ids posteriores a TASK-0238; (3) proposed->ready via submit_intent con intake invalido = rechazo atomico sin drift; (4) los casos N1-N6 + P1-P5 del SPEC s.4 implementados y verdes (test_intake_gate, 11 tests segun handoff); (5) protocol.config.json BYTE-IDENTICO (pin genesis #4 intacto; R0 vive en Area_comun/protocol/INTAKE_GATE.json fuera del config); (6) cero terminos de dominio (neutralidad exit 0) en core/templates. Emite GO/NO-GO con veredicto falsable."
question: "TASK-0238 (gate de intake determinista) cumple el DoD + SPEC v0.2 con R0 anti-retroactividad y pin preservado, en clon limpio? GO o NO-GO con hallazgos concretos."
---

# REVIEW - TASK-0238 [VISION-NOVA][F1.1] Gate de intake determinista

Codex entrego F1-A a in_review (deliver 17c5973, impl 0efe196). Ledger verde, su claim liberado.
Handoff: Area_comun/handoffs/HANDOFF-TASK-0238-codex-to-arquitecto-1.md (cambios: INTAKE_GATE.json
con R0 fuera del config pineado, validadores py+ps1, submit_intent hard-gate proposed->ready,
templates, examples/minimal_instance, scripts/test_intake_gate.py).

Ancla en clon limpio de HEAD. El foco del gate es el hallazgo F-1 (anti-retroactividad): que el
boundary R0 exima a lo pre-existente y HEAD valide verde, y que el pin (protocol.config.json)
quede byte-identico. Con tu GO ratifico review_approved y ruteo el done-flip a Codex; con NO-GO
ruteo remediacion.
