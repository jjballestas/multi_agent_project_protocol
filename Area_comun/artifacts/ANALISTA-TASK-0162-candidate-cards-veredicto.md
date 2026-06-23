# ANALISTA TASK-0162 - Veredicto candidate cards UX

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica revisada:
- Producto Zeus-protocol: `1b97c6bb39e54de8e28301f5885f8347385c8813`.
- Protocolo: `b3f8b7c4fc241cc9665a2b9a578840b990b454cb`.

No encontre bypass nuevo en AC69-AC71 ni relajacion del gate humano PII AC43. El marcado `approved` /
`discarded` queda en el store no-ledger; el requisito gobernado aparece solo por `submit_intent`.

## Reproduccion

| Prueba | Resultado |
| --- | --- |
| `git fetch origin; git status --short` en protocolo | exit 0; hay cambios/untracked ajenos solo en rutas personales y `.claude/settings.json`; no tocados |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| Parse de `Area_comun/state/*.json` con `utf-8-sig` | exit 0 |
| Clon limpio producto `C:/tmp/analista-task-0162-zeus`, checkout `1b97c6b`, `npm test` | exit 0; 55/55 pass |
| Producto targeted `node --test --test-name-pattern "candidate review stays outside the ledger|AC69-AC71" tests/staticContract.test.js` | exit 0; 2/2 pass |
| Payloads propios black-box contra servidor temporal + protocolo clonado | exit 0; PII gate 409, approve 200, discard 200, no candidate in ledger, PII redacted, drift false |
| Protocolo `python scripts/validate_collaboration_state.py` con secretos | exit 0 |
| Protocolo sin secretos en clon limpio | exit 0 |
| Drift replay | exit 0; `has_drift=false`, `up_to_seq=1374` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| #4 byte-identica | sin diff en `protocol.config.json` / chain / runtime state antes de este veredicto |

## Vector por vector

| Vector / AC | Estado | Evidencia adversarial |
| --- | --- | --- |
| AC69: aprobar sin PII revisada no procede y muestra error visible en tarjeta | PASA | Suite targeted pasa; diffs anclados agregan `data-candidate-error` + `.candidate-card-error`; payload propio al servidor con `piiReviewed:false` devuelve 409 antes de crear requisito. |
| AC43 carry: aprobar con PII revisada procede por camino gobernado | PASA | Payload propio con `piiReviewed:true` devuelve 200, `result.applied=true`, y el `task_upsert` produce `REQ-BD4BBD5021` en el protocolo clonado. |
| AC71: `approved` vive en store no-ledger y no crea candidato en `TASK_INDEX` | PASA | Tras approve, el JSON de candidato en el store temporal pasa a `status=approved` con `approved_requirement_id`; `TASK_INDEX` solo contiene el requisito `type=requirement/status=proposed`, no tareas `candidate` ni ids `CAND-*`. |
| AC71: discard vive en store no-ledger | PASA | POST `/api/protocol/intake-candidates/discard` devuelve 200 y `status=discarded`; `TASK_INDEX` no recibe el id de la candidata descartada. |
| AC17: no segundo escritor | PASA | En el flujo de approve, el unico aterrizaje ledger observado es el `task_upsert` dentro de `submit_intent`; `candidateUpdates` se aplica despues en el store externo. No hay ruta que inserte la candidata en estado canonico. |
| PII en planos publicables | PASA | Payload propio con NIT y SQL genera requisito redacted; no aparecen `900.123.456`, `dbo.saldos` ni `SELECT` en el requisito publicado; aparece marcador `REDACTED`. |
| AC70: Usar tarjeta sincroniza modo typed/manual sin escritura | PASA | Suite targeted pasa; el cambio es client-side: `syncIntakeInputMode("typed")` marca el radio y llama `applyIntakeInputMode`; no toca rutas `/api/protocol/actions/submit` ni endpoints de escritura. |
| Refresh tras approve/discard | PASA | Suite targeted pasa; ambos caminos exitosos llaman `refreshController.refreshView("intake", "...")` y despues sincronizan el modo esperado. |

## Residuales

- PII sigue siendo best-effort estructural; no es garantia de cero PII semantica.
- AC69/AC70 no son pruebas pixel-perfect; validan comportamiento DOM/contrato y ruta server, no layout visual exacto.
- El store no-ledger sigue siendo externo al ledger por diseno; su integridad depende de firma/provenance ya cubierta en tareas previas.

## Recomendacion

RECOMENDACION DE CIERRE: OK -> CERRABLE.
