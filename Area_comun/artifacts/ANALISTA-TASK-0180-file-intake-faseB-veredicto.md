---
artifact_id: ANALISTA-TASK-0180-file-intake-faseB-veredicto
task_id: TASK-0180
type: review_verdict
from: Analista
created_at: 2026-06-25
product_commit: 0b8593ae5044a16764a665dc291dd1e0eed22e1c
protocol_anchor: 5a9fe5f
recommendation: "OK->CERRABLE"
---

# Veredicto Analista - TASK-0180

Veredicto: OK->CERRABLE.

Ancla canonica revisada: producto `0b8593ae5044a16764a665dc291dd1e0eed22e1c` (`feat(intake): add deterministic file candidate review`) y protocolo `5a9fe5f` (`coord(TASK-0180): pasada del Analista (gate PII + no-egress) + memoria`), que contiene la instruccion REVIEW abierta.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Producto clon limpio `npm test` en `C:\Users\johnb\AppData\Local\Temp\zeus-0180-review-2c09141a4f9f4ff983f9dd30d7b5156a` | exit 0, 90/90 |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo sin secretos, clon `5a9fe5f`, `python scripts/validate_collaboration_state.py --root <tmp>` | exit 0 |
| Drift protocolo vivo | `has_drift=false`, `up_to_seq=1964` |
| Drift protocolo tmp con candidatas/store externo presentes tras flujo real | `has_drift=false`, `up_to_seq=1970` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` vivo | byte-identico en git, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Prueba por comportamiento

Prueba propia sobre servidor temporal de producto `0b8593a`, protocolo tmp `5a9fe5f`, `FILE_INGESTION_CONFIG_PATH` temporal con `enabled=true`, `extractor.provider=deterministic-local`, store temporal externo, clave Ed25519 temporal para firmar candidatas, y preload que hace fallar cualquier `globalThis.fetch` usado dentro del proceso servidor.

Resultado propio:

```json
{
  "uploadStatus": 200,
  "taskId": "TASK-EXTRACT-664D6D2E98",
  "extractionStatus": 200,
  "egress": {
    "boundary": "none_deterministic_no_llm",
    "provider": "deterministic-local",
    "networkEgress": false,
    "consent": "DETERMINISTIC_FILE_CONSUMER"
  },
  "candidateCount": 1,
  "withoutPii": {
    "status": 409,
    "error": "candidate approval requires human PII review acknowledgement"
  },
  "activeEdit": {
    "status": 400,
    "error": "requirement-intake narrative contains active content"
  },
  "piiEdit": {
    "status": 200,
    "reqId": "REQ-E61698065B",
    "candidateUpdates": 1
  },
  "reqTextChecks": {
    "hasEmail": false,
    "hasPhone": false,
    "hasAddr": false,
    "hasDoc": false,
    "hasEmailToken": true,
    "hasPhoneToken": true,
    "hasAddrToken": true,
    "hasDocToken": true,
    "hasProvenanceHashes": true
  },
  "rawBefore": true,
  "rawAfterApprove": false,
  "approvedCandidateStatus": "approved"
}
```

## Vectores

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| AC43 aprobar sin declarar PII | PASA | Payload `candidate.piiReviewed=false` contra `/api/protocol/actions/submit` devuelve HTTP 409 antes de aprobar: `candidate approval requires human PII review acknowledgement`. |
| AC43 re-screen del texto editado candidate->intake | PASA | Payload editado con email, telefono, direccion y documento aprueba con `piiReviewed=true`; el seed generado no contiene literales y si contiene `[EMAIL-REDACTED]`, `[PHONE-REDACTED]`, `[ADDR-REDACTED]`, `[DOC-REDACTED]`. |
| AC43 contenido activo editado | PASA | Payload editado con `<script>` y `piiReviewed=true` devuelve HTTP 400 `requirement-intake narrative contains active content`; no se aprueba. |
| No-egress de modelo en consumidor determinista | PASA | Con `globalThis.fetch` pre-cargado para fallar, la extraccion determinista completa HTTP 200, `candidateCount=1`, `provider=deterministic-local`, `boundary=none_deterministic_no_llm`, `networkEgress=false`. La ruta que llama modelo queda restringida al provider `local-vlm`. |
| Browser sin referencia a modelo | PASA | En `public/app.js` no aparecen `localVlm`, `qwen3-vl` ni `/api/chat`; los `fetch` del browser son rutas propias (`/api/protocol/...`, `/api/help/manual`). |
| Store fuera del dataset / no-ledger | PASA | Candidatas expuestas con `storeKind=os_tmp_outside_attested_dataset` y `storeLocator=.runtime/file-candidates`; `.runtime/` esta gitignored; drift 0 con candidato aprobado presente en store externo. |
| Clon limpio sin store externo valida | PASA | Clon secreto-less de protocolo `5a9fe5f` sin carpeta runtime externa valida exit 0. |
| OFF-by-default | PASA | `file-ingestion.config.json` versionado mantiene `fileIngestion.enabled=false` y `extractor.enabled=false`; la prueba solo uso config temporal. |
| Purga del raw al terminal | PASA | El raw existe tras upload (`rawBefore=true`) y desaparece tras aprobar candidata (`rawAfterApprove=false`); status externo queda `approved`. |
| #4 byte-identica | PASA | `protocol.config.json` sin diff; sha256 vivo `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Residuales

- La prueba propia verifica egress determinista con `fetch` bloqueado. No bloquea `http.request` por monkeypatch, pero el diff muestra que la rama determinista usa `extractCandidateDrafts(...)`; `http.request`/`net.connect` no aparecen en la rama de producto y la llamada de modelo esta confinada a `local-vlm`.
- La purga fue probada en aprobacion. `discarded` usa el mismo `markCandidateStatus` y `purgeRawUpload`; no encontre divergencia funcional.

## Recomendacion

OK->CERRABLE. No encontre escape nuevo para el gate PII humano, no-egress de modelo de la Fase B, store fuera del dataset, OFF-by-default ni purga del raw.

Firma: Analista.
