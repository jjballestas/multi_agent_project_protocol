# Veredicto Analista - Hallazgos #11/#12/#13 quality-data baseline

Firma: Analista
Fecha: 2026-07-07

## Veredicto

CONFIRMADO. Los tres hallazgos #11/#12/#13 existen en el commit de producto citado y son quality-data Q2 no bloqueante del baseline TASK-0255 ya cerrado. No recomiendo reabrir ni re-medir TASK-0255; la disciplina correcta es registrar el dato y mantener el fix-forward en SPEC-NOVA-P4-006.

Clasificacion:
- #11: WARNING-real, media, roza correctness. El gateway de produccion usa fallback encadenado de columnas y default silencioso `"A"`; el harness de evidencia no ejercita ese mismo camino.
- #12: WARNING-real, baja-media. No hay test HTTP WebApplicationFactory para la familia annul-preview/annul.
- #13: WARNING-real, baja. El arch-test de React omite el literal del proc de anulacion, aunque el frontend lo contiene como texto descriptivo.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Protocolo HEAD revisado | d0435bfb58d300613febe348d11bed4a2e827e70 |
| Producto Nova-Budget revisado | edbc037be8ce8297fbf308f611eef8c84aeccbf0 |
| Instruccion REVIEW/ACTION | Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgos11-12-13-quality-data-baseline.md |
| Clon limpio producto | C:/Users/johnb/AppData/Local/Temp/nova-budget-review-9ba99b959799470592e267c26a271cb5 |
| Clon limpio protocolo sin secretos | C:/Users/johnb/AppData/Local/Temp/protocol-clean-14a55e60722a462c8f7d1ab0585327e0 |

## Reproduccion

| Gate/probe | Exit | Resultado |
|---|---:|---|
| `git fetch origin` + `git status --short` | 0 | HEAD local = origin/main; working tree con cambios ajenos no tocados. |
| `python scripts/validate_collaboration_state.py` | 0 | OK canonico con secretos. |
| `npm test` en clon limpio de producto raiz | -4058 | FAIL reproducible por ausencia de `package.json` en raiz. Residual transversal ya conocido; no refuta los hallazgos. |
| `dotnet test NOVA.sln --no-restore` en clon limpio de producto | 0 | Suite .NET verde en commit citado. |
| Probe propio de los 8 predicados #11/#12/#13 | 0 | Todos los predicados observados en el commit citado. |
| `python scripts/validate_collaboration_state.py` en clon protocolo sin `secrets/` | 0 | OK sin secretos. |
| `python scripts/scan_domain_neutrality.py` | 0 | OK. |
| `python scripts/scan_encoding.py` | 0 | OK antes de emitir este artefacto. |
| Drift runtime via `runtime.protocol_replay.protocol_state_drift` | 0 | `has_drift=false`, `up_to_seq=4395`. |
| Chain via `runtime.protocol_replay.validate_chain` | 0 | valid, `checked_events=3723`. |
| `protocol.config.json` sha256 | 0 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identico respecto al ancla. |

## Tabla vector por vector

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| #11 gateway usa fallback para `reversal_id` | PASA hallazgo | `SqlAvailabilityCertificateAnnulmentGateway.cs` llama `TryGetInt64(reader, "reversal_id") ?? TryGetInt64(reader, "availability_certificate_reversal_id")`. |
| #11 gateway usa fallback/default para estado | PASA hallazgo | `TryGetString(reader, "document_state") ?? TryGetString(reader, "availability_certificate_state") ?? "A"`. |
| #11 missing columns quedan silenciadas | PASA hallazgo | `TryGetInt64` y `TryGetString` capturan `IndexOutOfRangeException` y devuelven `null`; eso activa el fallback/default. |
| #11 harness no prueba el mismo camino | PASA hallazgo | `AnnulAvailabilityCertificateEvidenceTests.cs` lee `GetOrdinal("availability_certificate_reversal_id")` y deriva `DocumentState` por `JOIN Core.Internal_Catalog`, no desde el result-set del proc por el mismo mapper del gateway. |
| #12 familia HTTP annul-preview/annul sin test | PASA hallazgo | `ApiInfrastructureTests.cs` contiene WebApplicationFactory para health, OpenAPI, ProblemDetails, parameters, execution-report y appropriation-modifications; no contiene `annul-preview`, `annul`, `IAvailabilityCertificateAnnulmentGateway` ni `AvailabilityCertificateAnnulment`. |
| #13 guard mecanico omite proc | PASA hallazgo | `LayeringTests.cs` prohibe `Apply_Budget_Modification` y `Apply_Availability_Adjustment`; no prohibe `Annul_Availability_Certificate`. |
| #13 frontend contiene literal omitido | PASA hallazgo | `apps/nova-web/src/App.tsx` contiene `Budget.Annul_Availability_Certificate` en `guardSource` y en fallback visible. |
| Fix-forward SPEC P4-006 cubre #11/#12/#13 | PASA disciplina | SPEC-NOVA-P4-006 incluye restricciones 6i/6j/6k, criterios 10/11/12 y riesgo explicito para no repetir estos gaps en el miembro gobernado. |

## Residuales

- `npm test` en raiz del producto sale -4058 por ausencia de `package.json`. Lo declaro como gate transversal fallido/residual conocido, no como evidencia contra #11/#12/#13.
- No ejecuto SQL real ni BD sandbox en esta pasada; el alcance pedido es verificar el registro quality-data baseline y el horneado fix-forward, no re-medir TASK-0255.
- El hallazgo #11 no prueba que el proc desplegado devuelva columnas incompatibles; prueba que el codigo de produccion tolera silenciosamente incompatibilidad y que el harness no cubre ese camino.

## Recomendacion

OK -> CERRABLE para el registro de #11/#12/#13 como quality-data no bloqueante del baseline. No reabrir TASK-0255. Mantener la remediacion como fix-forward en SPEC-NOVA-P4-006 y exigir re-juicio formal cuando esa SPEC entre a construccion del brazo gobernado.

task_id: OPS-HALLAZGOS-QUALITY-DATA
status: done
executive_summary: Confirmo #11/#12/#13 como quality-data Q2 no bloqueante del baseline TASK-0255. No recomiendo reabrir ni re-medir TASK-0255; el fix-forward en SPEC-NOVA-P4-006 es adecuado.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-OPS-hallazgos11-12-13-quality-data-baseline-veredicto.md
  - path_or_commit: Area_comun/mailbox/open/MSG-20260707-Analista-to-Arquitecto-REVIEW-hallazgos11-12-13-quality-data-baseline-CONFIRMADO.md
gates:
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: npm test
    result: FAIL - product root has no package.json, exit -4058
  - command: dotnet test NOVA.sln --no-restore
    result: PASS
  - command: python scripts/scan_domain_neutrality.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: runtime.protocol_replay.protocol_state_drift + validate_chain
    result: PASS
next_recommended: Arquitecto registra #11/#12/#13 como quality-data no bloqueante y conserva SPEC-NOVA-P4-006 como fix-forward.
risks: Root npm gate sigue fallando por ausencia de package.json; #11 requiere SQL/result-set real en la futura construccion gobernada para cerrar la incertidumbre de compatibilidad.
