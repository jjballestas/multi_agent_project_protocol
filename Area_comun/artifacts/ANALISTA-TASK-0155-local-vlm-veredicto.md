---
artifact_id: ANALISTA-TASK-0155-local-vlm-veredicto
task_id: TASK-0155
type: review_verdict
from: Analista
to: Arquitecto
status: final
created_at: 2026-06-22
product_commit: 79be511
protocol_commit: 90de6fa
recommendation: CAMBIO-REQUERIDO
---

# Veredicto Analista - TASK-0155 local-vlm

Firma: Analista.

Veredicto: CAMBIO-REQUERIDO. No cierro TASK-0155.

Motivo gateante: AC52 no queda regresion-proof y, en prueba de comportamiento contra el servidor real, el endpoint
`http://2130706433:11434/api/chat` queda aceptado como `local-vlm` habilitado. El requerimiento de review pidio
refutar ese truco explicitamente. Si se decide aceptar notaciones numericas equivalentes a loopback, debe quedar
registrado como excepcion deliberada; con el texto actual de AC52 ("unicamente ese host:puerto local" y config con
host != loopback rechazada) lo trato como escape de canonicalizacion.

## Ancla canonica

- Producto: `D:/Agentes/Zeus/Zeus-protocol` commit `79be511` (`feat(intake): add local vlm extractor provider`).
- Protocolo: `D:/Agentes/multi_agent_project_protocol` commit `90de6fa`.
- Mensaje de review: `Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0155.md`.

## Reproduccion

| Check | Resultado |
| --- | --- |
| Clon limpio producto, checkout `79be511`, `npm test` | PASS 48/48, exit 0 |
| Prueba propia AC52 hosts contra `/api/protocol/actions` | exit 1 por escape `2130706433` |
| Prueba propia AC46 guard estatico: fetch externo, import `ky`, dynamic import `undici`, `http.get`, local-vlm permitido | PASS, exit 0 |
| Protocolo vivo `python scripts/validate_collaboration_state.py` con secretos presentes | exit 0 |
| Protocolo clon limpio sin `secrets/`, checkout `90de6fa`, `python scripts/validate_collaboration_state.py` | exit 0 |
| Drift runtime #4 | `has_drift=false`, `up_to_seq=1191`, hot_hash == replay_hash |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| #4 byte-identica | sin diff en `protocol.config.json`, `runtime/`, `agent_registry`, `Area_comun/state/` antes de esta entrega |

Nota: el flag `--with-secrets` no existe en `validate_collaboration_state.py`; verifique la variante con secretos
en el repo vivo (secret files presentes) y la variante sin secretos en clon limpio (secret files ausentes).

## Vectores

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| AC52 rechazo no-loopback: `0.0.0.0` | PASA | Config queda deshabilitada: `fileIngestion.enabled=false`, provider `disabled`. |
| AC52 rechazo no-loopback: `8.8.8.8` | PASA | Config queda deshabilitada. |
| AC52 rechazo no-loopback: `evil.com` | PASA | Config queda deshabilitada. |
| AC52 rechazo IPv6 no-loopback: `[2001:4860:4860::8888]` | PASA | Config queda deshabilitada. |
| AC52 truco host: `127.0.0.1.evil.com` | PASA | Config queda deshabilitada. |
| AC52 truco IPv6 mapped: `[::ffff:8.8.8.8]` | PASA | Config queda deshabilitada. |
| AC52 truco decimal: `2130706433` | SLIP | Config queda habilitada como `local-vlm`. Repro: endpoint `http://2130706433:11434/api/chat` en `localVlm.endpoint`; GET `/api/protocol/actions` devuelve `fileIngestion.enabled=true`. |
| AC52 test permanente de rechazo | SLIP | La suite solo cubre un no-loopback (`192.168.1.10`) y no cubre la familia de trucos pedida. El escape decimal no queda atrapado. |
| AC46 guard allowlist | PASA con residual ya conocido | Mis payloads propios marcaron `fetch("http://8.8.8.8...")`, `import ky`, `await import("undici")`, `http.get(...)`; `fetch(localVlm.endpoint)` dentro del wrapper permitido queda sin violacion. |
| AC51 troceado y dedupe | PASA | Suite limpia verifica mas de una llamada, `num_ctx===1024` en todas y dedupe a una candidata. Codigo fija `options.num_ctx=localVlm.numCtx` y trocea por `maxPayloadBytes`/`TEXT_EXTRACTION_CHUNK_BYTES`. |
| AC53 robustez + no-ledger + PII carry | PASA | Suite limpia verifica respuesta con texto+JSON+basura, candidata invalida descartada, candidata `pending`, no task `candidate`, drift 0; AC43 rechaza aprobacion sin `piiReviewed` y re-screen redacted antes de intake. |
| OFF-by-default | PASA | `file-ingestion.config.json` default `enabled=false`; provider live requiere config `enabled=true`, extractor enabled, `provider=local-vlm` y consentimiento `FILE_EXTRACTION_AGENT`. |

## Cambio requerido

1. Agregar test negativo permanente para la familia AC52 completa, al menos:
   `0.0.0.0`, `8.8.8.8`, `evil.com`, IPv6 no-loopback, `127.0.0.1.evil.com`, `2130706433`,
   `[::ffff:8.8.8.8]`.
2. Endurecer `sanitizeLocalVlmConfig` para validar el host canonico de entrada, no solo el hostname normalizado
   por `URL`, o registrar una decision explicita si se acepta la notacion decimal de loopback como equivalente
   permitida. Sin esa decision, el host debe ser literalmente `localhost`, `127.0.0.1` o `[::1]`/`::1`.

## Residuales

- AC46 sigue siendo un guard estatico, no sandbox. No bloquea este cierre si AC52 queda cubierto por test de
  comportamiento y canonicalizacion.
- La integracion real con Ollama/Qwen queda fuera de este cierre por decision de alcance; el provider sigue
  off-by-default.
