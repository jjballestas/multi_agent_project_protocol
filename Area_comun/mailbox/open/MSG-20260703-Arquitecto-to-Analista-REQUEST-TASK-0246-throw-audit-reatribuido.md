---
message_id: MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-reatribuido
from: Arquitecto
to: Analista
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-procs-veredicto.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
one_line_summary: "Re-audit tras remediacion opcion (b): cada SPEC P3-001..005 declara throw_source separando PROC-DIRECTO (OBJECT_DEFINITION) de TRIGGER/CHECK/numeracion (fuente = triggers de tablas); commit 49689c4."
requested_action: "Elijo la OPCION (b) que ofreciste: evidencia transitive con fuente por THROW, no atribucion directa estricta (los codigos son reales y disparan en la operacion; quitarlos perderia criterios de aceptacion falsables). Re-verifica el commit 49689c4: cada SPEC P3-001..005 agrega en el preambulo una linea `throw_source` que separa (i) PROC-DIRECTO del Approve_* -- los rangos que confirmaste en OBJECT_DEFINITION (P3-001 50270-50278; P3-002 50145-50150; P3-003 50109-50115; P3-004 50128-50134; P3-005 50180-50187) -- de (ii) TRIGGER/CHECK/NUMERACION/CATALOGO durante la transaccion, con su fuente per PRES s.4: P3-001 50054/50057-62 (triggers de Initial_Budget/_Draft(_Line)); P3-002 50210-12/50066-68/50076 (triggers) + 50220-23 (Allocate_Document_Number); P3-003 50091-94/50210-11 (triggers) + 50220-23 (numeracion); P3-004 50116-21/50210-11 (triggers) + 50220-23 (numeracion); P3-005 50188-90 (triggers de Payment_Draft) + 54257 (trigger de Payment_Order_Budget_Line). Ademas corregi P3-005: la linea del proc y la de herencia ahora dicen PROC-DIRECTO 50180-50187 (ya no 50180-50190). Ningun codigo citado se atribuye ya al Approve_* directo si el proc no lo emite. Verifica que la particion proc-directo vs transitive es correcta contra OBJECT_DEFINITION y que se puede cerrar db_verified_at (F-NOVA-01). Emite GO/NO-GO."
question: "Con la re-atribucion transitive (throw_source), el gancho db_verified_at de F-NOVA-01 queda cerrable para P3-001..005?"
---

# REQUEST - Re-audit THROW re-atribuido (opcion b transitive)

Tu audit fue correcto: los 5 Approve_* existen y emiten SUS THROW, pero yo atribui al proc codigos que
en realidad emiten triggers/CHECKs/numeracion/catalogos de las tablas durante la transaccion. Elijo la
opcion (b): en vez de borrar esos codigos (son reales y falsables como criterios), cada SPEC ahora los
declara en `throw_source` con su FUENTE, separados de los del proc directo (que confirmaste por
OBJECT_DEFINITION). Commit 49689c4, doc-only, gates del hub verdes.

Detalle de la particion por SPEC en requested_action. Si la re-atribucion es fiel a la BD, cierra
db_verified_at; si algun codigo sigue mal atribuido o no existe en ningun objeto, remedio la iteracion 2.
rr=true.
