# ANALISTA TASK-0172 final verdict

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO. No cierro TASK-0172.

Ancla canonica revisada:
- Producto Zeus-protocol: `967f5cbfb396e808df674850f965c386ddd5b9a3`.
- Protocolo HEAD de la instruccion REVIEW final: `e4858714575e834924cefcc7978782e7a564986d`.

Resultado sustantivo: el leak de PII que halle en la pasada anterior queda cerrado por comportamiento en el modelo publico de candidatas, y no encontre una nueva ruta de escritura, bypass del gate de PII ni activacion implicita del extractor tras las rondas de layout. Sin embargo, el gate obligatorio de producto no queda verde: `npm test` en clon limpio no alcanzo exit 0 en mis corridas. Por la regla de gatear por EXIT, la recomendacion de cierre es CAMBIO-REQUERIDO hasta tener una corrida limpia de `npm test` en el commit final o endurecer el harness que abre puertos aleatorios.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 967f5cb; npm test` | exit 124 por timeout local a 304s |
| `npm test` en el mismo clon limpio, rerun 1 | exit 1, 84/85 pass; fallo `candidate review stays outside the ledger...`, `listen EACCES 127.0.0.1:5040` |
| `npm test` en el mismo clon limpio, rerun 2 | exit 1, 84/85 pass; fallo `runtime control derives live state...`, servidor imprimio listening en `127.0.0.1:5060` pero `/healthz` no quedo listo |
| `npm test -- --test-name-pattern "TASK-0172|candidate review"` | exit 0, 13/13 pass |
| Payload propio PII contra `/api/protocol/actions` y `/api/protocol/intake-candidates` | exit 0; literales PII ausentes |
| Payload propio aprobacion sin `piiReviewed` | HTTP 409 |
| Payload propio extractor con config enabled pero `extractor.enabled=false` | HTTP 403 |
| `python scripts/validate_collaboration_state.py` repo vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` clon protocolo `e485871` sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py` repo vivo y clon sin secretos | exit 0 |
| `python scripts/scan_encoding.py` repo vivo y clon sin secretos | exit 0 |
| Drift runtime repo vivo y clon sin secretos | `has_drift=false`, `up_to_seq=1800` |
| `protocol.config.json` | sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, byte-identica |

Payload PII propio sembrado en store externo de candidatas:

```text
title = Contacto maria@example.com
narrative = Tel +1 (415) 555-2671 y direccion Calle 10 No 20-30 Piso 3
acceptance_intent = Debe ocultar documento AB12345 y cedula 123456789
```

Salida observada en el modelo publico:

```text
maria@example.com=false
+1 (415) 555-2671=false
Calle 10 No 20-30=false
documento AB12345=false
cedula 123456789=false
tokens presentes: [EMAIL-REDACTED], [PHONE-REDACTED], [ADDR-REDACTED]
```

## Vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| Fix del leak PII en modelo publico | PASA | `normalizeStoredCandidate` usa `publicModel = options.publicModel !== false`; `title`, `narrative` y `acceptance_intent` pasan por `redactPublicText` por defecto. Payload propio contra ambos endpoints publicos no devolvio email, telefono, direccion ni documento literal. |
| Path de aprobacion usa raw | PASA | `readStoredCandidate` llama `normalizeStoredCandidate(..., { publicModel: false })`; el builder de aprobacion compara provenance contra el stored raw y construye intake desde el draft aprobado. |
| Gate humano PII en aprobacion de candidata | PASA | Payload propio con `piiReviewed:false` devolvio HTTP 409 antes de aprobar; suite dirigida `candidate review` tambien cubre no-gate y aprobacion gobernada. |
| No-bypass / nueva ruta de escritura | PASA | Commit final `967f5cb` toca solo `public/styles.css` y `tests/staticContract.test.js` frente a su padre; la redaccion previa esta en `src/server.js`. No aparece nuevo emisor de `submit_intent` ni escritura directa a `Area_comun/state`. |
| Extractor off-by-default | PASA | Con file ingestion habilitado para review pero `extractor.enabled=false`, `/api/protocol/intake-extractions/run` devolvio HTTP 403. |
| Layout round 3: uploader solo modal, sin bloque de accion en aprobadas, textareas altas | PASA | Suite dirigida `TASK-0172|candidate review` exit 0; contratos `round3` pasan. |
| Layout round 4: campos full-width | PASA | Suite dirigida `TASK-0172|candidate review` exit 0; contrato CSS `candidate-card fields use the full card width` pasa. |
| Gate producto completo | SLIPS | `npm test` en clon limpio no dio exit 0 en dos reruns tras un timeout inicial; por instruccion, el cierre se gatea por EXIT, no por inferencia de que el fallo sea flake local. |

## Residuales

No encontre nuevo escape de PII en el plano publico de candidatas ni bypass nuevo de aprobacion. El residual bloqueante no es funcional del fix PII sino de cierre: la suite completa del producto no quedo verde en clon limpio durante esta pasada.

Recomendacion: CAMBIO-REQUERIDO.
