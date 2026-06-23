# ANALISTA TASK-0163 - veredicto ledger-busy

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica revisada:
- Producto Zeus-protocol: `d1de0c1` (`fix(intake): sanitize ledger busy errors`).
- Protocolo: `e668cd0` (`review(TASK-0163): handoff al Analista -- ledger-busy saneado, sin fuga argv, sin bypass`).

La entrega cumple AC72: la contencion del ledger se serializa igual que antes, pero el cliente recibe un error
tipado y saneado. No encontre bypass nuevo ni fuga de `argv`, comando, `--intents-json` o traceback en la
superficie publica probada.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol` a tmp + `git checkout d1de0c1` | exit 0 |
| `npm test` en clon limpio de producto | exit 0, 57/57 |
| `node --test --test-name-pattern "AC72\|no-bypass\|candidate review stays outside\|intake endpoint rejects impersonation\|file ingestion is gated"` | exit 0, 6/6 |
| Payloads propios contra funciones extraidas de `src/server.js` + `public/app.js` | exit 0, 6 busy + 3 tecnicos |
| `python scripts/validate_collaboration_state.py` con secretos en repo vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` sin secretos en clon limpio del protocolo `e668cd0` | exit 0 |
| `python scripts/scan_domain_neutrality.py` vivo y clon limpio | exit 0 |
| `python scripts/scan_encoding.py` vivo y clon limpio | exit 0 |
| Drift runtime | `has_drift=false`, `up_to_seq=1388` |
| `protocol.config.json` | sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`; byte-identico antes del veredicto |

## Vectores adversariales

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Contencion `claim acquire overlaps active claim` con traceback, comando y `--intents-json` en stderr/message | PASA | `submitIntentClientError` devuelve solo `{ error: "ledger-busy", code: "ledger-busy", retryable: true }`; regex negativa no encuentra comando, argv, claim id ni traceback. |
| Familia de contencion: `overlaps active claim`, `active claim`, `ledger busy`, `concurrent ledger`, `contention` | PASA | 6 payloads propios dieron HTTP logico 409 y body saneado; `friendlyGovernedError` mapea a `Canal ocupado, intente mas tarde`. |
| Otros errores tecnicos con traceback/comando/secret/path en stderr | PASA | 3 payloads propios dieron `{ error: "submit_intent failed" }`, status logico 502, sin fuga de comando, `--intents-json`, traceback, secret ni path. |
| Front requirement-intake, escritura previa de file extraction y aprobacion de candidata | PASA | `public/app.js` usa `friendlyGovernedError` en los tres flujos; targeted suite cubre AC72 + candidate/file/intake. |
| No-bypass / anti-impersonacion | PASA | Targeted `intake endpoint rejects impersonation...` y `negative no-bypass...` exit 0; el servidor sigue construyendo actor/intents server-side. |
| Candidatas fuera del ledger + PII gate duro | PASA | Targeted `candidate review stays outside the ledger...` exit 0. |
| Serializacion del ledger | PASA | El cambio envuelve el error de `runtime/submit_intent.py`; no cambia claims, scopes, `submit_intent`, ni grano de escritura. |
| #4 / config de protocolo | PASA | `protocol.config.json` byte-identico antes del veredicto; drift 0. |

## Slips buscados

No encontre escape bloqueante.

Residual no bloqueante: el detector `isLedgerBusySubmitIntentError` es deliberadamente amplio; una cadena tecnica
que contenga "active claim" aunque no sea una contencion real se clasificaria como `ledger-busy`. Lo probe con
`inactive claimant record mentions active claim in docs only` y dio 409. Esto no filtra datos ni abre bypass; el
riesgo es de diagnostico demasiado amable, no de seguridad ni gobierno.

## Recomendacion

RECOMENDACION DE CIERRE OK -> CERRABLE para TASK-0163.
