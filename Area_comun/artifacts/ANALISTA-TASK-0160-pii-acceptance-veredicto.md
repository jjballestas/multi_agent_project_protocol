---
artifact_id: ANALISTA-TASK-0160-pii-acceptance-veredicto
task_id: TASK-0160
author: Analista
created_at: 2026-06-23
product_commit: a3c5f26
protocol_commit: d8892f8b8c0b5ae8d60f37e802b8ca55430f7a68
verdict: CERRABLE
---

# Veredicto Analista - TASK-0160

Recomendacion: OK -> CERRABLE.

Ancla canonica: producto `Zeus-protocol` en `a3c5f26` y protocolo en
`d8892f8b8c0b5ae8d60f37e802b8ca55430f7a68`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Clon limpio producto `a3c5f26`, `npm test` | exit 0, 52/52 pass |
| Targeted behavior `node --test --test-concurrency=1 --test-name-pattern "file ingestion is gated\|local-vlm extractor\|candidate approval\|AC64\|AC65" tests/staticContract.test.js` | exit 0, 2/2 pass |
| Payloads propios contra servidor temporal y protocolo clonado | exit 0 |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| Validador sin secretos en clon limpio del protocolo | exit 0 |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| Drift runtime | exit 0, `has_drift=false`, `up_to_seq=1324` |
| #4 byte-identica | `protocol.config.json` SHA256 antes del veredicto `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| AC64: extraer archivo con `acceptanceIntent` vacio | PASA | Payload propio `mode=execute`, archivo valido, `acceptanceIntent=""`, `piiAcknowledged=true` devolvio 200 y creo `TASK-EXTRACT-*` tipo `triage`/`ready`, no candidata en `TASK_INDEX`. |
| AC43 carry: ack PII sigue obligatorio para extraer | PASA | Mismo payload con `piiAcknowledged=false` devolvio 409 `requirement-intake execute requires PII acknowledgement`. |
| Consentimiento extractor separado | PASA | `/api/protocol/intake-extractions/run` sin `consent` devolvio 409; con `FILE_EXTRACTION_AGENT` devolvio 200. |
| Candidatas no entran al ledger | PASA | Antes y despues de ejecutar el extractor, `TASK_INDEX` no contiene tareas con `status=="candidate"` ni `type=="candidate"`. |
| Aprobacion de candidata exige PII review | PASA | Payload propio de aprobacion con `piiReviewed=false` devolvio 409 `candidate approval requires human PII review acknowledgement`. |
| Aprobacion de candidata sigue exigiendo `acceptanceIntent` | PASA | Targeted behavior test del repo, sobre candidato firmado/sembrado, verifica aprobacion sin `acceptanceIntent` -> 400 `acceptanceIntent is required`. No depende solo de lectura de codigo. |
| Loopback-only local VLM | PASA | Targeted behavior test cubre familia decimal, octal, hex, `0.0.0.0`, externos, sufijos, IPv4-mapped y leading-zero como rechazados; positivos `localhost`, `127.0.0.1`, `127.0.0.5`, `[::1]`. |
| AC17 / segundo escritor | PASA | La extraccion escribe candidatas solo en store externo; el intake gobernado sigue pasando por `runtime/submit_intent.py` al aprobar. No observe escritura directa a `TASK_INDEX` desde el extractor. |
| AC65 label PII alineado sin quitar condicion | PASA | El cambio de UI queda cubierto por test estatico; el gate real se comprobo por payloads de servidor: el texto cambio, la condicion no. |

## Residuales declarados

- El custom payload con extractor deterministic-local devolvio `extraction.status="failed"` y cero candidatas, pero aun asi probo la parte relevante de seguridad: consentimiento requerido, respuesta controlada y no-ledger. La aprobacion de candidata con firma/semilla real queda cubierta por el targeted behavior test existente.
- PII sigue siendo best-effort estructural; no es garantia de cero PII.
- El guard loopback no es sandbox de red para procesos externos; es validacion de endpoint/configuracion de esta ruta.

Firma: Analista.
