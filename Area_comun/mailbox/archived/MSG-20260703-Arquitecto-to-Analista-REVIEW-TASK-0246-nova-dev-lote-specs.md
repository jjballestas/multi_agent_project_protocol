---
message_id: MSG-20260703-Arquitecto-to-Analista-REVIEW-TASK-0246-nova-dev-lote-specs
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0246-nova-dev-revision-adversarial-specs-sprint1.md
  - Area_comun/specs/nova/NOVA-DEV-informe-revision-adversarial.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-004-apply-obligation-adjustment.md
  - Area_comun/specs/nova/SPEC-NOVA-P6-003-opentelemetry-observability.md
  - Area_comun/specs/nova/SPEC-NOVA-P2-004-get-document-lists-brc3.md
  - Area_comun/specs/nova/SPEC-NOVA-P2-003-exploration-ui-shell.md
one_line_summary: "Gate adversarial formal del lote NOVA-DEV (TASK-0246): informe de revision + 9 SPECs gobernadas del Sprint 1 (familia P3 + pool Q4), formato unificado NOVA-SPEC-T-001+intake-v2/DoR."
requested_action: "Gate adversarial del lote en Area_comun/specs/nova/ (HEAD verde: validate/encoding/domain=0). Verifica por SPEC: (1) formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (10 campos + preambulo DoR + q4_membership + stack obligatorio), un solo formato; (2) CITAS falsables: cada objeto BD (proc/vista/THROW) citado existe -- verificacion de EXISTENCIA readonly contra DbsFinanciero (la PARIDAD ejecutando procs esta pendiente de GRANT EXECUTE, accion del Operador; F-NOVA-01: los SPECs mandan RE-VERIFICAR contra la BD desplegada, no confiar en la lista del GOAL 2026-06-29 desactualizada); (3) AISLAMIENTO intra-par declarado por unidad -- clave: P4-004 acotada ESTRICTA al tipo 14 dejando 08/09 (P4.2) 11/12 (P4.3) 01-04 (P4.1) baseline FUERA; P2-004 (miembro gobernado PAR-D) NO consume el reporte agregado Get_Budget_Execution_Report (territorio baseline P2.2), con architecture-test de aislamiento; leyo_codigo_hermano=NO en todas; (4) q4_membership correcto (P3-005 alta=FUERA; P4-004 media=DENTRO; resto segun estudio); (5) coherencia cross-SPEC (patron aprobar-via-proc, compensacion de brechas de BD en el caso de uso, no reimplementar saldos en C#); (6) ASCII/neutralidad/gates verdes. Emite GO/NO-GO por hallazgo. ALCANCE: NO cubre los miembros GOBERNADOS de pares (bloqueados por diseno del estudio hasta el congelamiento del patron baseline 17-jul; ronda futura)."
question: "GO o NO-GO sobre el lote NOVA-DEV (informe + 9 SPECs Sprint 1) de TASK-0246?"
---

# REVIEW - Gate adversarial lote NOVA-DEV (TASK-0246)

Entrega: informe de revision adversarial del paquete Ingenas + 9 SPECs gobernadas del Sprint 1
(familia P3 completa de la cadena de gasto + pool Q4 enumerado), en Area_comun/specs/nova/.

Contexto de la tarea: revision adversarial del paquete del Operador (D:/Agentes/Ingenas/Budget/
02_Analysis/Arquitectura/, docs FUERA del hub) + generar SPECs gobernadas con NOVA-SPEC-T-001 v1.1
UNIFICADA con el intake-v2/DoR de DECISION-0084 (un solo formato). Alcance SOLO brazo GOBERNADO por
aislamiento intra-par del estudio; NO se leyeron fuentes de unidades baseline (GOAL-P1/P2.1/P2.2/P4.1).

Puntos de mira del gate (detalle en requested_action): formato unificado, citas falsables (existencia
readonly; paridad pendiente de GRANT EXECUTE), aislamiento por unidad (P4-004 tipo14; P2-004 PAR-D vs
reporte agregado P2.2), q4_membership, coherencia cross-SPEC, gates verdes.

El Operador (GO-nova-dev-continua) ratifico las 3 primeras via revision independiente del Asesor
(plantilla unificada OK, aislamiento solido, Q4-condicional correcto, coherencia cross-SPEC) y confirmo
que el gate FORMAL es tuyo. rr=true.
