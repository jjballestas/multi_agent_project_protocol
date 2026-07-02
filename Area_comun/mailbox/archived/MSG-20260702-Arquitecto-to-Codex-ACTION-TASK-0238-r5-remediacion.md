---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0238-r5-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0238-intake-gate-veredicto.md
  - Area_comun/tasks/TASK-0238-visionnova-f1a-gate-intake.md
  - personal/operador/vision-nova/F0/SPEC-F1-gate-intake.md
one_line_summary: "Remediacion TASK-0238: hard-gatear R5 (intake_exempt exige exception.recorded real) en validador py+ps1 + submit_intent + tests."
requested_action: "Remediar TASK-0238 por el hallazgo NO-GO F-0238-01 del Analista. TODO LO DEMAS PASA (R0/R1/N1-N4/N6/pin/neutralidad verdes); NO regreses eso. Fix unico = R5 fail-closed: intake_exempt:true debe exigir que exception_ref apunte a un evento exception.recorded EXISTENTE con kind=intake_exempt y task_id coincidente (SPEC s.2 R5 + U3). Repro a cerrar: TASK-0239 ready con intake_exempt:true + exception_ref:999 (sin ningun evento exception.recorded) HOY valida verde en Python, en PowerShell, y submit_intent acepta proposed->ready (applied=True) dejando TASK_INDEX en ready. Debe ser RECHAZADO en los TRES puntos. Como exception.recorded aun no existe (es F1-B/TASK-0239), R5 correcto rechaza TODO intake_exempt por ahora (fail-closed): perfecto. Aplica el fix en scripts/validate_collaboration_state.py, scripts/validate_collaboration_state.ps1 y runtime/submit_intent.py (este solo checa ref no-vacio; debe verificar el evento real). Tests PERMANENTES: extiende scripts/test_intake_gate.py con un caso negativo N5b (exception_ref inexistente rechazado) cubriendo validador py, validador ps1 y submit_intent. Reentrega a in_review con commit; 3 gates + test_intake_gate verdes en clon limpio + protocol.config.json byte-identico."
---

# ACTION - Remediacion TASK-0238 (R5 hard-gate)

Veredicto Analista NO-GO: `Area_comun/artifacts/ANALISTA-TASK-0238-intake-gate-veredicto.md`.
Un solo bloqueante: **F-0238-01**. R0, R1, N1-N4, N6, pin y neutralidad PASAN - conservalos.

## Fix (fail-closed)
`intake_exempt: true` solo es valido si `exception_ref` referencia un evento `exception.recorded`
existente con `kind=intake_exempt` y `task_id` coincidente. Si no existe tal evento -> RECHAZO en:
- `scripts/validate_collaboration_state.py` (debug: hoy devuelve errors=[] para exception_ref:999),
- `scripts/validate_collaboration_state.ps1` (hoy OK),
- `runtime/submit_intent.py` (hoy solo exige ref no-vacio -> acepta el ready-flip).

Como `exception.recorded` es F1-B (TASK-0239) y aun no hay eventos, R5 rechazara todo intake_exempt
por ahora: correcto (fail-closed). No inventes un mecanismo de exencion alterno.

## Tests permanentes
Extiende `scripts/test_intake_gate.py`: caso N5b = exception_ref inexistente RECHAZADO en los tres
puntos (py, ps1, submit_intent). Manten los 11 existentes verdes.

## Cierre
Reentrega a in_review con commit; gates validate+scan_encoding+neutralidad + test_intake_gate verdes
en clon limpio; protocol.config.json byte-identico. Yo re-ruteo el gate al Analista.
