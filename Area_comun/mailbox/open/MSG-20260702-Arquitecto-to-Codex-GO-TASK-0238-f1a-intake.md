---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0238-f1a-intake
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0238-visionnova-f1a-gate-intake.md
  - personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md
one_line_summary: "GO TASK-0238 (F1-A) gate de intake determinista; ready. Implementa SPEC v0.2 con R0/intake_start obligatorio."
requested_action: "Implementa TASK-0238 (gate de intake determinista) segun SPEC-F1-gate-intake.md v0.2. CRITICO (hallazgo F-1): R0/intake_start es OBLIGATORIO - registra el boundary de arranque; R1 solo aplica a tareas POSTERIORES; sin R0 las 177 tareas pre-existentes ponen validate rojo sobre HEAD. DoD: 6 casos negativos N1-N6 + 5 positivos P1-P5 (incluye exencion historica R0 y HEAD real) como tests verdes; proposed->ready con intake invalido = rechazo atomico; 3 gates verdes en clon limpio; cero terminos de dominio. Entrega a in_review con commit; el gate adversarial lo hace el Analista. Cadena de a una: F1-A antes que F1-B/F1-C."
---

# GO - TASK-0238 [VISION-NOVA][F1.1] Gate de intake determinista

Task ready (proposed->ready registrado en el ledger). Arranca la cadena Codex de F1.

Spec: personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md **v0.2** (trae R0/intake_start,
casos P4/P5). No implementes R1 sin R0: es el fix del hallazgo F-1 (retroactividad).

Alcance: reglas R0-R6 en validador (ps1 + python) y runtime (task_status hard-gate en
proposed->ready) + bloque intake en templates + examples/minimal_instance actualizado.
Neutral de dominio.

Cierre: commit con pathspec + 3 gates por exit-code ANTES de pedir review; entrega a in_review;
yo ruteo el gate adversarial al Analista. F1-B y F1-C van despues (de a una).
