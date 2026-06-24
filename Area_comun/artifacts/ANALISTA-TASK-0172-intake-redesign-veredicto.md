# ANALISTA TASK-0172 intake redesign verdict

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO. No cierro TASK-0172.

Ancla canonica revisada:
- Producto Zeus-protocol: `a4e0b50492a91ecbbc60c4e1e75085e5e05550da`.
- Protocolo citado por la instruccion: `009efe1250c522b7d200bf1a83f000e2e015b618`.
- REVIEW materializado en protocolo: `db368d46e9229b1ab7f3c2270473a46a400501b5`.

El rediseno es client-side y la suite completa pasa en clon limpio, pero la frontera RC-04/PII no queda refutada: el endpoint que alimenta el modal de revision entrega texto libre de candidatas sin redaccion. En una candidata sembrada con email, telefono, direccion y documento, `GET /api/protocol/actions` devolvio esos literales en `safeguards.candidateReview.candidates`. Como el modal prellena desde ese modelo, el prellenado puede filtrar PII al cliente.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout a4e0b50; npm test` | exit 0, 81/81 pass |
| Payload propio PII en candidate store + `GET /api/protocol/actions` | exit 0, leak confirmado |
| `python scripts/validate_collaboration_state.py` repo vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` clon protocolo `009efe1` sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py` repo vivo | exit 0 |
| `python scripts/scan_encoding.py` repo vivo | exit 0 |
| Drift runtime | `has_drift=false`, `up_to_seq=1767` |
| `protocol.config.json` | sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identica durante la pasada |

Payload propio usado contra servidor temporal en clon limpio de producto:

```text
candidate.title = Contacto persona@example.com
candidate.narrative = Tel +1 (415) 555-2671 y direccion Calle 10 No 20-30 Piso 3
candidate.acceptance_intent = Debe ocultar cedula 123456789
```

Salida observada en `safeguards.candidateReview.candidates`:

```text
persona@example.com=True
+1 (415) 555-2671=True
Calle 10 No 20-30=True
cedula 123456789=True
```

## Vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| RC-01 header unificado | PASA | Test `TASK-0172 AC1` pasa; cambios en `public/app.js` exponen `intake-control-bar`, radios Manual/Archivo contiguos, Nueva historia y Refresh. |
| RC-02 dashboard carpetas | PASA | Test `TASK-0172 AC2` pasa; `deriveIntakeFolders` deriva Pendientes/Aprobados desde candidatas y Preview desde estados fallidos/vacios. |
| RC-03 modal Manual gobernado | PASA | Test `TASK-0172 AC3` pasa; `submitIntake` sigue enviando a `/api/protocol/actions/submit` con `confirm: SUBMIT_INTENT` en execute. |
| RC-04 gate PII para aprobar candidata | PASA parcial | `submitCandidateApproval` exige checkbox local y `src/server.js::buildCandidateRequirementIntake` rechaza `piiReviewed !== true` con 409. |
| RC-04 prellenado PII-free | SLIPS | `loadCandidateReviewModel -> listStoredCandidates -> normalizeStoredCandidate` devuelve `title`, `narrative` y `acceptance_intent` con `ascii(stripControl(...))`, no `redactPublicText`/`redactRequirementText`; el payload propio confirma literales PII en el JSON del cliente. |
| RC-05 modal archivo uploader-only / accept OK | PASA | Test `TASK-0172 AC5` pasa; `deriveFileUploadModalState` habilita Aceptar solo con `status=ok` y `candidateCount>0`. |
| RC-06 standalone sin radios/lista inline | PASA | Test `TASK-0172 AC6` pasa; contrato `deriveExtractionStandaloneContract` devuelve `hasModeRadios=false`, `hasInlineCandidateList=false`. |
| No-bypass / nueva ruta de escritura | PASA | Commit toca solo `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`; `src/server.js` no cambia. Fetches de Intake siguen a `/api/protocol/actions/submit` y `/api/protocol/intake-extractions/run`; no aparece escritura directa a `Area_comun/state`. |
| Extractor off-by-default | PASA | Config versionada mantiene `fileIngestion.enabled=false`; UI muestra `Carga por archivo OFF. Activacion solo por runtime.` cuando el flag esta apagado. |

## Cambio requerido

Antes de cerrar, el modelo publico de candidatas que alimenta el front debe ser PII-free por construccion. Una forma falsable de cerrar el hueco:

- Redactar `title`, `narrative` y `acceptance_intent` en la respuesta publica (`/api/protocol/actions` y `/api/protocol/intake-candidates`) antes de que lleguen al cliente.
- Mantener hashes/provenance/ids intactos.
- Anadir test negativo permanente con email, telefono con parentesis, direccion y documento en una candidata almacenada; el JSON del cliente y el prellenado del modal no deben contener los literales.
- Conservar el gate humano `piiReviewed` en aprobacion.

## Residuales

No encontre nueva ruta de escritura ni activacion implicita del extractor en este commit. El residual bloqueante es especifico: confidencialidad del texto libre de candidata en el plano cliente antes de la revision humana.

Recomendacion: CAMBIO-REQUERIDO.
