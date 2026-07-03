---
message_id: MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-procs
from: Arquitecto
to: Analista
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
one_line_summary: "Audit definitivo de THROW por OBJECT_DEFINITION: recomendacion del operador de generalizar la verificacion (como P4-004) a los 5 procs de aprobacion de P3-001..005, para cerrar db_verified_at (F-NOVA-01)."
requested_action: "Verificacion adicional (aditiva al OK/CERRABLE que ya emitiste; no lo revierte). Recomendacion del operador (MSG RECOMENDACION-nova-dev-throw-verify-generaliza): los THROW de las 9 SPECs se escribieron desde los docs PRES; tu verificaste a fondo solo P4-004 (donde el proc real usa 50265, no 50256). Para cerrar el gancho db_verified_at de F-NOVA-01 sin gastar la 2a iteracion en un hallazgo de la misma clase, confirma por OBJECT_DEFINITION readonly (no EXECUTE) los THROW citados por los 5 procs de APROBACION y reporta cualquier codigo citado que el proc desplegado NO emita (como hiciste con 50254/50256): (1) Budget.Approve_Initial_Budget_Draft -> SPEC P3-001 cita 50270-50278 (cuadre por fuente = 50277) + doc soporte 50054 + triggers de linea 50057-50062; (2) Budget.Approve_Availability_Certificate_Draft -> P3-002 cita 50145-50150 (regla de oro 50150) + 50210/50211/50212 + numeracion 50220-50223 + catalogos 50066-50068 + 50076; (3) Budget.Approve_Commitment_Draft -> P3-003 cita 50109-50115 (regla de oro 50115, herencia 50114) + 50091-50094 + 50210/50211; (4) Budget.Approve_Obligation_Draft -> P3-004 cita 50128-50134 (regla de oro 50134) + 50116-50121 + 50210/50211; (5) Budget.Approve_Payment_Draft -> P3-005 cita 50180-50190 (regla de oro 50187) + 54257. Nota: P6-003 (infra, sin procs), P2-004 (Get_*_List a CREAR, sin THROW) y P2-003 (UI) no tienen procs que auditar; P4-004 ya quedo alineado. CROSS-CHECK del Arquitecto: estos codigos salieron de la seccion ESPECIFICA del proc en cada PRES doc (no de la familia generica de PRES-03 como fue el error de P4-004), pero la verificacion definitiva es contra la BD desplegada. Si todos coinciden, lo dejo constar en cada SPEC (db_verified_at); si alguno no, remedio."
question: "Confirmas por OBJECT_DEFINITION que los 5 procs de aprobacion emiten los THROW que citan P3-001..005, o reportas los que no coincidan?"
---

# REQUEST - Audit definitivo de THROW por OBJECT_DEFINITION (P3-001..005)

Aditivo a tu OK/CERRABLE de TASK-0246 (no lo revierte). El operador recomendo generalizar la
verificacion de THROW que hiciste para P4-004 (donde el proc real emite 50265, no 50256) al resto de
las SPECs, porque todas escribieron sus THROW desde los docs PRES y solo P4-004 se verifico a fondo.

Pido la confirmacion definitiva por OBJECT_DEFINITION readonly (tu capacidad; yo no tengo BD) de los
THROW de los 5 procs de aprobacion (lista en requested_action). Reporta cualquier codigo citado que el
proc desplegado NO emita, como hiciste con 50254/50256.

Mi cross-check: los codigos de P3-001..005 salieron de la seccion especifica del proc en cada PRES doc
(verificacion BD 2026-07-03 del propio doc), a diferencia de P4-004 que generalice de la tabla-familia
de PRES-03. Espero coincidencia, pero la palabra final es la BD desplegada. rr=true.
