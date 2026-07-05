---
message_id: MSG-20260706-Operador-to-Arquitecto-DECISION0018-task0255-quality-data-3-hallazgos
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo10-50212-etiquetado-cruzado.md
  - "D:/Agentes/Zeus/NOVA/Nova-Budget (product HEAD edbc037be8ce8297fbf308f611eef8c84aeccbf0)"
one_line_summary: "Senal DECISION-0018: 3 huecos de calidad NO-bloqueantes en TASK-0255 baseline (ya cerrada) que el GO adversarial informal no marco. Registrar como quality-data del baseline SIN reabrir la unidad medida + hornear los criterios correctivos en SPEC-NOVA-P4-006 / patron gobernado."
requested_action: "(a) Registrar los 3 hallazgos como quality-data del brazo baseline (continuar la numeracion #10 -> #11/#12/#13; via Analista igual que #10 si aplica), SIN reabrir ni re-medir TASK-0255 (unidad baseline cerrada y medida; tocarla altera lo medido). (b) Hornear los criterios correctivos en SPEC-NOVA-P4-006 (hermano gobernado Annul_Commitment) y en el patron gobernado de Sprint 1, como PREP fix-forward, no parche retroactivo."
question: "Confirmas el registro como quality-data no-bloqueante (sin reabrir la unidad) y el horneado de los criterios en SPEC-NOVA-P4-006? Si tu lectura de severidad difiere, dimelo con evidencia."
---

# ACTION (DECISION-0018) - 3 huecos de calidad en TASK-0255 baseline no marcados por el GO informal

Ratificaste el GO de TASK-0255 (checker adversarial informal: "0 hallazgos bloqueantes"). Una pasada
transversal posterior (change-monitor + verificacion del Asesor contra el codigo real, product HEAD
edbc037) surfaceo 3 huecos que el GO no marco. Los tres son NO-BLOQUEANTES -- el GO dijo "0 BLOQUEANTES",
no "0 hallazgos", asi que esto NO lo contradice: lo complementa como serie honesta de calidad del brazo
baseline (es justo lo que Q2 contrasta). Los senalo por DECISION-0018 para el registro; NO reabrir la
unidad medida.

## Hallazgo #11 (media, roza correctness) -- lectura de result-set con columnas inciertas + default silencioso
`SqlAvailabilityCertificateAnnulmentGateway.cs:54-64`: el gateway de produccion adivina nombres de columna
con fallback encadenado -- `reversal_id` -> `availability_certificate_reversal_id`, y `document_state` ->
`availability_certificate_state` -> **default silencioso `"A"`**. El arnes de evidencia (que SI corre contra
SQL vivo) NO usa esos primeros nombres: lee `availability_certificate_reversal_id` directo sin fallback
(`AnnulAvailabilityCertificateEvidenceTests.cs:380`) y deriva el estado por un JOIN a `Core.Internal_Catalog`
(linea 390), no del result-set del proc. Es decir: el camino de lectura de produccion NO fue verificado con
certeza contra el proc desplegado. Si el result-set real no trae esas columnas, el API reporta `state="A"` y
`reversalId=null` en silencio. A diferencia de TASK-0254, esto no llego verificado. Criterio correctivo para
el patron gobernado: leer la columna confirmada contra `OBJECT_DEFINITION` del proc desplegado (sin
adivinanza + default silencioso), o cubrir el mapeo del result-set en la evidencia F-NOVA-01.

## Hallazgo #12 (baja-media) -- sin test de integracion HTTP con gateway falso para los 2 endpoints
`ApiInfrastructureTests.cs` usa `WebApplicationFactory` + gateways falsos pero solo ejercita
`/appropriation-modifications`, parametros y execution-report. **No hay** test HTTP que pegue a
`GET /api/budget/availability-certificates/annul-preview` ni `POST .../annul` con un
`IAvailabilityCertificateAnnulmentGateway` falso. La logica del servicio tiene unitarias; el wiring HTTP
(ruta -> endpoint -> mapeo de comando -> gateway) queda sin cubrir. Criterio correctivo: extender el patron
de integracion HTTP-con-gateway-falso a cada endpoint mutador nuevo del brazo gobernado.

## Hallazgo #13 (baja) -- el frontend contiene el proc mutador como literal y se omitio de la lista prohibida
`App.tsx:180,370` contiene el literal `'Budget.Annul_Availability_Certificate'` (etiqueta de la UI
"Anulacion de CDP"), y el arch-test del frontend `LayeringTests.cs:73-75` (`React_app_does_not_contain_sql
_or_procedure_calls`) prohibe `Apply_Budget_Modification` (0253) y `Apply_Availability_Adjustment` (0254)
pero **no** `Annul_Availability_Certificate` -- justo la omision que evita que el test cace el literal. Rompe
el patron de las 2 tareas previas. Matiz: es texto descriptivo, el frontend no LLAMA al proc (leak nulo),
pero es una inconsistencia del guard de aislamiento que el GO no senalo. Criterio correctivo: decidir en el
patron gobernado si el nombre del proc mutador puede exhibirse en la UI; si no, anadirlo a la lista prohibida
(y mover la etiqueta a un identificador neutral); si si, documentar la excepcion explicita.

## Encuadre de estudio
Los 3 son DATA de calidad del brazo baseline (Q2), fix-forward. NO reabrir TASK-0255 (misma disciplina que
#8/auth: gap declarado + fix-forward en el miembro gobernado, nunca alterar post-hoc lo medido). El fenomeno
mismo -- una capa mas adversarial caza lo que el GO informal por-unidad dejo pasar en el baseline -- es
evidencia de la tesis central (registrada en EVIDENCIA-VIVA A9).
