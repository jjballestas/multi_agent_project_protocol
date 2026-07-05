---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-TASK-0246-in-review-flip
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-06
context_refs:
  - Area_comun/tasks/TASK-0246-nova-dev-revision-adversarial-specs-sprint1.md
  - Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md
one_line_summary: "TASK-0246 (docs) deliverables completos (informe adversarial + SPECs). Ejecuta el flip in_progress -> in_review (capability implementer, tarea type=docs no es owner-closeable por el Arquitecto)."
requested_action: "Acquire claim covering TASK_INDEX/PROJECT_STATE/task .md para TASK-0246, submit_intent task_status in_progress -> in_review, release claim, commit+push. Evidencia: informe adversarial commiteado (commit 8321277, Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md) confirma sin contradicciones con la arquitectura obligatoria + mapeo RES->SPEC completo del alcance sellado; SPECs gobernadas del Sprint 1 (pares + P3 + pool Q4 + BR-C4) todas commiteadas en Area_comun/specs/nova/ (incluye SPEC-NOVA-P4-006 nueva, commit 9bd3587). DoD cumplido: informe + SPECs + este ACTION funciona como el FYI al Operador (referenciado)."
question: ""
---

task_id: TASK-0246
status: in_progress
executive_summary: Ambas partes del alcance de TASK-0246 completas. (1) Informe adversarial del paquete NOVA-DEV (Ingenas): sin contradicciones con la arquitectura obligatoria; mapeo RES-000..012 -> SPEC-NOVA confirma cobertura completa del alcance sellado (pares gobernados + familia P3 + pool Q4 declarado + BR-C4); gaps de RES fuera del pool sellado (obligacion/pago-anulacion, cascada reversos, cierre de vigencia, PAC, reportes regulatorios) registrados como backlog futuro explicito, no defecto de esta entrega (el paquete mismo se auto-declara honesto sobre ellos). 3 mejoras de proceso propuestas al NOVA_PROMPT (guard de procedencia, F-NOVA-01/OBJECT_DEFINITION, checklist DoR) para que el Operador decida aplicarlas. (2) SPECs gobernadas commiteadas: verifique el inventario completo contra el pool Q4 declarado (10 unidades) + los pares -- todas ya existian salvo SPEC-NOVA-P4-006 (Annul_Commitment, PAR-2 gobernado), que escribi con diseno de autorizacion real (converge hallazgos #5/#7/#8).
artifacts: Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md; Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md; 12 SPECs totales en Area_comun/specs/nova/.
gates: validate_collaboration_state.py exit 0; scan_encoding.py exit 0; scan_domain_neutrality.py exit 0.
next_recommended: Ejecuta el flip in_progress->in_review (capability implementer). Tras eso ruteo REVIEW al Analista (checker-only) para el gate adversarial formal de esta tarea.
risks: Ninguno. El informe es de solo lectura sobre el paquete Ingenas (no lo edita); las SPECs nuevas no se construyen (linea roja pool Q4/gobernado hasta 30-jul).
