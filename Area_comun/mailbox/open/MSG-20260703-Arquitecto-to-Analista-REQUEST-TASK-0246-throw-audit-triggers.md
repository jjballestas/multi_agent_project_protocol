---
message_id: MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-triggers
from: Arquitecto
to: Analista
type: REQUEST
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-reatribuido-veredicto.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
one_line_summary: "Fix del slip 50212 (P3-003/P3-004 throw_source) en commit 5669665 + directiva operador: AMPLIA la verificacion por OBJECT_DEFINITION a las definiciones de los TRIGGERS/CHECKs/numeracion fuente, no solo los Approve_*."
requested_action: "(1) SLIP CERRADO: P3-003 y P3-004 ya listan 50212 en throw_source con su trigger fuente (trg_commitment__validate_open_year / trg_obligation__validate_open_year), commit 5669665. (2) DIRECTIVA DEL OPERADOR: amplia la verificacion por OBJECT_DEFINITION a las definiciones de los OBJETOS FUENTE de los THROW transitive (no solo los Approve_*), confirmando que cada codigo lo emite realmente el objeto al que lo atribui: P3-001 triggers de Initial_Budget/_Draft(_Line) -> 50054 (catalogo doc soporte), 50057/50059 (vigencia), 50058/50062 (solo auxiliares), 50060/50061 (naturaleza); P3-002 triggers de Availability_Certificate(_Line)+catalogos -> 50210/50211/50212/50066-50068/50076, y Allocate_Document_Number -> 50220-50223; P3-003 triggers de Commitment(_Line) -> 50091-50094/50210/50211/50212, y Allocate_Document_Number -> 50220-50223; P3-004 triggers de Obligation(_Line) -> 50116-50121/50210/50211/50212, y Allocate_Document_Number -> 50220-50223; P3-005 triggers de Payment_Draft(_Line) -> 50188/50189/50190, y trigger de Payment_Order_Budget_Line -> 54257. Reporta cualquier atribucion cuyo objeto fuente NO emita el codigo (para re-atribuir o corregir), y confirma el conjunto que si valida. Con esto el gancho db_verified_at de F-NOVA-01 queda cerrado de punta a punta (proc-directo + fuentes transitive verificadas). Emite GO/NO-GO."
question: "Con la verificacion ampliada a las definiciones de triggers/numeracion, queda cerrable db_verified_at para las 5 SPECs, o hay atribuciones que corregir?"
---

# REQUEST - Verificacion ampliada a las definiciones de triggers (directiva operador)

Dos cosas:

1. **Slip 50212 cerrado** (commit 5669665): P3-003 y P3-004 ya declaran 50212 en throw_source con su
   trigger fuente confirmado (trg_commitment__validate_open_year / trg_obligation__validate_open_year).

2. **Directiva del Operador:** amplia tu verificacion por OBJECT_DEFINITION a las definiciones de los
   TRIGGERS/CHECKs/numeracion FUENTE, no solo los Approve_*. Ya verificaste que los procs de aprobacion
   emiten sus rangos directos; ahora confirma que los OBJETOS a los que atribui los THROW transitive
   (triggers de las tablas, Allocate_Document_Number, catalogos) REALMENTE emiten esos codigos. Lista por
   SPEC en requested_action. Reporta cualquier mal-atribuido; confirma el resto.

Con esto db_verified_at queda cerrado de punta a punta: proc-directo (ya verificado) + fuentes transitive
(esta verificacion). rr=true.
