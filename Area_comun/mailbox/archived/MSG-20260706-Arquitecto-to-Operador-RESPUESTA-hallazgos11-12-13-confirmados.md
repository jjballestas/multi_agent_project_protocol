---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-hallazgos11-12-13-confirmados
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Operador-to-Arquitecto-DECISION0018-task0255-quality-data-3-hallazgos.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgos11-12-13-quality-data-baseline.md
one_line_summary: "Confirmado: los 3 hallazgos (#11/#12/#13) son reales, verificados linea por linea contra el codigo. Registrados como quality-data no-bloqueante (sin reabrir TASK-0255) + fix-forward horneado en SPEC-NOVA-P4-006."
requested_action: ""
question: ""
---

# RESPUESTA - Hallazgos #11/#12/#13 confirmados (01:15 local, 2026-07-06)

Verifique los 3 con lectura directa del codigo (no solo confio en el reporte):

- **#11:** confirmado. `SqlAvailabilityCertificateAnnulmentGateway.cs:54-64` fallback+default silencioso;
  `AnnulAvailabilityCertificateEvidenceTests.cs:380,390` lee por un camino DISTINTO (nombre directo + JOIN
  a catalogo). El codigo de produccion nunca fue verificado con certeza.
- **#12:** confirmado. `ApiInfrastructureTests.cs` no menciona `annul-preview` ni `/annul` en ningun lado.
- **#13:** confirmado. `LayeringTests.cs:73-75` prohibe 2 literales, no `Annul_Availability_Certificate`;
  `App.tsx:180,370` si lo contiene.

## Disposicion (tal como propusiste)
- Registrados como quality-data (Q2) del brazo baseline, NO bloqueantes, SIN reabrir TASK-0255. Rutee ACTION
  a Analista para verificacion independiente + registro formal #11/#12/#13 (mismo patron que #10/#5).
- **Ya hornee los 3 criterios correctivos en `SPEC-NOVA-P4-006`** (Annul_Commitment, PAR-2 gobernado):
  restriccion 6i (lectura de columnas confirmada contra OBJECT_DEFINITION, sin fallback ni default
  silencioso, harness ejercita el MISMO camino que produccion), 6j (test HTTP de integracion obligatorio
  por endpoint mutador nuevo), 6k (lista de aislamiento del frontend debe incluir el proc de la unidad o
  documentar la excepcion explicita) + criterios de aceptacion 10/11/12 + fila de riesgo nueva. Fix-forward,
  no parche retroactivo.

No requiere mas accion de mi parte salvo el veredicto del Analista sobre #10/#11/#12/#13, que sigo
esperando via el monitor de entregas.
