---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-brc4-entregado-registrar-enmienda
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - personal/asesor/DRAFT-ENCARGO-DBA-BR-C4-hardening.md
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-brc4-operation-authorization.sql"
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-brc4-operation-authorization-evidence.txt"
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
one_line_summary: "BR-C4 (opcion b) ENTREGADO y verificado por el DBA en sandbox: 36/36 smoke de separacion, THROW 50320-50324, rollback 0 residuos, guard sandbox 51011. Registra la enmienda fechada del sello confirmando Q4 n=10 tras verificacion independiente; hornea Assert_Permission en las SPECs P3.x para Sprint 1."
requested_action: "(1) Verifica independiente la entrega del DBA contra lo DESPLEGADO (OBJECT_DEFINITION de los 6 procs con guarda BR-C4 como nova_budget_verifier; los sets THROW reales BR-C4=50320-50324; el smoke de separacion emitir/aprobar/anular). (2) Registra la ENMIENDA FECHADA del sello (formato s.24/s.25) confirmando BR-C4 cerrada -> P3.2/P3.3/P3.4 elegibles pool Q4 -> n=10 (la condicion sellada se cumplio antes del 29-jul). (3) Hornea en las SPECs P3.x el criterio de que los procs REALES de captura de borrador (que se construyen en Sprint 1) invoquen Security.Assert_Permission -- el DBA probo la guarda con shims Authorize_*_Draft_Capture porque los procs reales aun no existen; la guarda es real en aprobar/anular, shim en captura."
question: "Confirmas la verificacion independiente + registro de la enmienda (Q4 n=10) y el horneado de Assert_Permission en P3.x? Si tu verificacion contra BD difiere del reporte del DBA, dilo con la evidencia."
---

# ACTION - BR-C4 entregado (opcion b): verificar + registrar enmienda + hornear en P3.x

El DBA del Operador entrego BR-C4 (matriz de autorizacion por operacion) verificado en `DbsFinanciero_SANDBOX`
antes del 29-jul. La condicion sellada se CUMPLIO -> P3.2/P3.3/P3.4 preservan elegibilidad Q4 (n=10).

## Reporte del DBA (resumen; evidencia en los archivos referenciados)
- 9 permisos BR-C4 en `Security.Permission`; 9 roles por documento x operacion; 4 identidades smoke
  (capture-only/approve-only/annul-only/no-access); `Security.Assert_Permission` creado.
- Guardas BR-C4 inyectadas en 6 procs REALES: `Approve_{Availability_Certificate,Commitment,Obligation}_Draft`
  + `Annul_{Availability_Certificate,Commitment,Obligation}`.
- **Rango THROW: 50320-50324** (el sugerido 50300-50319 colisionaba con `Reset_Sandbox_Mutator_Baseline`
  50300-50303; el DBA lo verifico y ajusto -- correcto).
- Validacion: OBJECT_DEFINITION visible como `nova_budget_verifier`; **smoke de separacion 36/36 PASS**;
  anulaciones reales con rollback (CDP 30, RP 87, OBL 665), 0 residuos; guard sandbox aborto 51011 contra
  prod; sin secretos. VIEW DEFINITION sobre `Annul_Obligation` agregado. Grants ampliados para
  `budget_sandbox_verifier`.

## Lectura del Asesor (study-integrity)
Entrega SOLIDA, cumple los criterios del encargo. DOS notas para Sprint 1:
1. **Shims de captura:** los procs reales de captura de borrador P3 no existen aun (Sprint 1) -> el DBA uso
   shims falsables para probar la guarda de captura. La guarda es REAL en aprobar/anular. Los procs reales
   de captura DEBEN heredar `Assert_Permission` -> hornear en las SPECs P3.x (accion 3).
2. Es HARDENING simetrico, no toca lo medido; el dev no crea los procs (regla 8).

Falta la VERIFICACION INDEPENDIENTE (tu, contra lo desplegado, como hiciste con PAR-2) antes de registrar la
enmienda. El Asesor hace design/study-integrity, NO sustituye la verificacion empirica contra BD.

-- Operador
