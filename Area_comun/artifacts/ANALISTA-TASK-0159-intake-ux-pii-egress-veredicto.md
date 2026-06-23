# ANALISTA - Veredicto TASK-0159

Firma: Analista
Fecha: 2026-06-23
Tarea: TASK-0159
Producto canonico revisado: `Zeus-protocol` commit `bc8346db385d53d68ce0e92d89307e1e6796bb5b`
Protocolo canonico de instruccion: `036114c24913b34a57f89c9d9adba16729fe09f7`
Protocolo citado por el handoff/checker: `2359251`

## Veredicto

OK/CERRABLE.

No encontre escape nuevo en los tres focos pedidos: extractor loopback-only + candidatas no-ledger + gate humano PII; estados nuevos sin fuga de secreto/PII por el flujo probado; y sin segundo escritor fuera de `runtime/submit_intent.py`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Clon limpio producto checkout `bc8346d`; `npm test` | PASS 52/52, exit 0 |
| Payloads propios servidor producto contra clon protocolo desechable `2359251` | PASS, exit 0 |
| Payloads propios UI extraidos de `public/app.js` | PASS, exit 0 |
| `python scripts/validate_collaboration_state.py` con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py` sin secretos en clon limpio | exit 0 |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| Drift #4 | `has_drift=false`, `up_to_seq=1304`, exit 0 |
| #4 byte-identica antes del veredicto | `protocol.config.json` hash `81cf406eb6e200deea001d3b48d5cf12f33d3f10`; `runtime/state/events.jsonl` hash `e3fb9aa231466239f08df70c97eeffb1a8e0a95c`; `runtime/state/snapshot.json` hash `8852e17399be9397738178b725541e963efc3a9d` |

## Payloads Adversariales Propios

Use un servidor producto temporal desde el clon limpio, con `PROTOCOL_REPO_PATH` apuntando a un clon desechable del protocolo y stores fuera del repo.

| Vector | Prueba | Resultado |
| --- | --- | --- |
| AC52 loopback-only | `127.0.0.1` y `https://localhost` | PASA: config habilitada |
| AC52 decimal loopback | `http://2130706433:11434/api/chat` | PASA: config deshabilitada |
| AC52 octal/hex | `0177.0.0.1`, `0x7f000001` | PASA: config deshabilitada |
| AC52 externo/sufijo/userinfo | `8.8.8.8`, `127.0.0.1.evil.com`, `127.0.0.1@evil.com` | PASA: config deshabilitada |
| AC52 IPv4-mapped / HTTPS a IP | `[::ffff:127.0.0.1]`, `https://127.0.0.1` | PASA: config deshabilitada |
| AC43 candidatas no-ledger | Extraccion deterministic-local de `.md` con dos historias | PASA: 2 candidatas en store `os_tmp_outside_attested_dataset`; `TASK_INDEX.json` sin `CAND-*`, `type=candidate` ni `status=candidate` |
| AC43 gate humano PII | Aprobacion de candidata con `piiReviewed=false` | PASA: 409 |
| AC16 redaccion | Aprobacion con `NIT 900.123.456 SELECT * FROM dbo.secretos` y `piiReviewed=true` | PASA: task generado no contiene `900.123.456`, `dbo.secretos` ni `SELECT`; contiene marcadores `REDACTED` |
| AC17 anti-bypass | Payloads con `actorId`, `intents`, `route=Area_comun/state/TASK_INDEX.json` | PASA: no devuelven 200 |
| AC17 execute cerrado | `actionId=sdd-task-upsert`, `mode=execute` | PASA: no devuelve 200 |
| AC62 nota real | `fileIngestionSummary` con `.md/.pdf/.png` | PASA: muestra extensiones reales y bytes reales |
| AC62 estados rojos | `completed-empty` y `failed` en panel de candidatas | PASA: `empty-state error-text` y razon visible |
| UI injection | Candidata con titulo `<b>x</b>` | PASA: HTML escapado como `&lt;b&gt;x&lt;/b&gt;` |

## Residuales

- La garantia PII sigue siendo best-effort estructural, no cero-PII semantico. No bloquea porque el flujo mantiene gate humano duro antes del intake y redaccion estructural al construir el task.
- `local-vlm` loopback-only es un guard de configuracion/host, no un sandbox de red general. No bloquea porque los payloads de canonicalizacion pedidos quedan cerrados y el provider off-by-default sigue intacto.
- El estado de error visible renderiza la razon que entrega el servidor. En el flujo probado, las razones son acotadas/generadas por servidor y los fallos no exponen secreto; si en el futuro se propaga stderr externo crudo, debe revisarse otra vez.

## Recomendacion

CERRABLE.
