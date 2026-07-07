---
message_id: MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgos11-12-13-quality-data-baseline
from: Arquitecto
to: Analista
type: ACTION
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/src/NOVA.Infrastructure/Budget/AvailabilityCertificateAnnulments/SqlAvailabilityCertificateAnnulmentGateway.cs"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/AnnulAvailabilityCertificateEvidenceTests.cs"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/ApiInfrastructureTests.cs"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.ArchitectureTests/LayeringTests.cs"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/apps/nova-web/src/App.tsx"
  - Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md
one_line_summary: "DECISION-0018 (via Operador): 3 huecos de calidad NO-bloqueantes en TASK-0255 baseline (ya cerrada) que el GO informal no marco. Registra #11/#12/#13, sin reabrir TASK-0255; ya horneados fix-forward en SPEC-NOVA-P4-006."
requested_action: "Verifica independientemente (clon limpio, product HEAD edbc037be8ce8297fbf308f611eef8c84aeccbf0) y registra como hallazgos formales #11/#12/#13 (continuan la numeracion 1-10 ya usada), quality-data del brazo baseline (Q2), NO bloqueantes, SIN reabrir ni re-medir TASK-0255 (unidad cerrada; tocarla altera lo medido -- misma disciplina que #8/auth). (#11, media, roza correctness) SqlAvailabilityCertificateAnnulmentGateway.cs:54-64 lee reversal_id/document_state con fallback encadenado de nombres de columna + DEFAULT SILENCIOSO 'A' si no encuentra la columna; el harness de evidencia (AnnulAvailabilityCertificateEvidenceTests.cs:380,390) NO ejercita ese mismo camino -- lee availability_certificate_reversal_id directo sin fallback y deriva el estado por JOIN a Core.Internal_Catalog, no del result-set del proc. El camino de lectura de PRODUCCION nunca fue verificado con certeza contra el proc desplegado. (#12, baja-media) ApiInfrastructureTests.cs no tiene ningun test HTTP (WebApplicationFactory + gateway falso) para GET .../annul-preview ni POST .../annul -- el wiring HTTP completo de los 2 endpoints queda sin cubrir, solo hay unitarias de la capa Application. (#13, baja) LayeringTests.cs:73-75 (React_app_does_not_contain_sql_or_procedure_calls) prohibe los literales Apply_Budget_Modification y Apply_Availability_Adjustment pero NO Annul_Availability_Certificate; App.tsx:180,370 SI contiene ese literal (etiqueta de UI 'guardSource'). Es texto descriptivo (el frontend no llama al proc), pero rompe el patron de aislamiento que las 2 tareas previas si cumplieron -- omision, no verificado por el guard mecanico. Los 3 ya los verifique yo mismo linea por linea contra el codigo; coinciden exactamente con lo reportado. YA HORNEE los criterios correctivos como fix-forward en SPEC-NOVA-P4-006 (restricciones 6i/6j/6k + criterios de aceptacion 10/11/12 + fila de riesgo nueva) para que el miembro gobernado (Annul_Commitment, Sprint 1) no repita estos gaps -- verifica que el horneado es adecuado si tienes oportunidad al revisar la SPEC en su gate futuro."
question: "Confirmas el registro de #11/#12/#13 como quality-data no-bloqueante del brazo baseline (sin reabrir TASK-0255) y que el fix-forward en SPEC-NOVA-P4-006 es la disciplina correcta (vs. parche retroactivo)? Si tu clasificacion de severidad difiere, dimelo con tu evidencia."
---

# ACTION (DECISION-0018) - Registro de hallazgos #11/#12/#13 (quality-data baseline, TASK-0255)

El Operador senalo (verificado por mi con lectura directa del codigo) 3 huecos de calidad en TASK-0255
(PAR-2 baseline, ya `done`) que el checker adversarial informal no marco como bloqueantes -- y no lo son;
son data de calidad complementaria (Q2), no una contradiccion del GO.

## #11 (media, roza correctness): lectura de result-set por adivinanza + default silencioso
Gateway de produccion adivina nombres de columna con fallback + cae en `state="A"` sin verificar si la
columna existe. El harness de evidencia SQL real NO ejercita ese mismo camino de lectura (usa nombres y
mecanismo distintos) -- el codigo de produccion nunca fue verificado con certeza contra el proc real.

## #12 (baja-media): sin test HTTP de integracion para los 2 endpoints nuevos
`ApiInfrastructureTests.cs` no cubre `annul-preview`/`annul` con `WebApplicationFactory` + gateway falso.

## #13 (baja): omision del proc en la lista de aislamiento del frontend
El arch-test de aislamiento del frontend prohibe 2 procs anteriores pero no `Annul_Availability_Certificate`,
que SI aparece como literal descriptivo en `App.tsx`.

## Disposicion
Registrar como quality-data del baseline (Q2), NO reabrir TASK-0255. Ya horneados los 3 criterios
correctivos como fix-forward en `SPEC-NOVA-P4-006` (miembro gobernado, Annul_Commitment) para que Sprint 1
no repita el patron.
