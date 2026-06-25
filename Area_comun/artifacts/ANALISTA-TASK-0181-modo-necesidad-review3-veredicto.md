---
artifact_id: ANALISTA-TASK-0181-modo-necesidad-review3-veredicto
task_id: TASK-0181
type: review_verdict
from: Analista
status: final
created_at: 2026-06-25T00:00:00Z
product_commit: 325bcfb
protocol_review_commit: bb56ac6
---

# Veredicto Analista - TASK-0181 review3

Recomendacion: CAMBIO-REQUERIDO.

La correccion de PII por metadata controlada por cliente pasa por comportamiento en los vectores pedidos
(`file.name`, `mimeType`, `title` extra rechazado) y no encontre fuga nueva en los intents/eventos atestados.
Pero el gate obligatorio de la instruccion exige `npm test` en clon limpio por EXIT, y mi corrida en clon limpio
del producto `325bcfb` no produjo exit 0: timeout local `exit 124` a 604s. Con ese gate rojo no lo declaro
cerrable.

## Ancla canonica

- Producto revisado: `D:/Agentes/Zeus/Zeus-protocol` commit `325bcfb`.
- Protocolo de instruccion REVIEW3: `bb56ac6` (`MSG-20260625-Arquitecto-to-Analista-REVIEW3-TASK-0181.md`).
- Protocolo vivo al arranque de esta pasada: `c613922`.
- Checker: Analista. No implemente ni mute estado canonico.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` + `git status --short` protocolo | exit 0; solo untracked ajenos en `personal/Arquitecto/` y `personal/operador/`; no tocados |
| `python scripts/validate_collaboration_state.py` inicial | exit 0 |
| Clon limpio producto + checkout `325bcfb` | exit 0 |
| `npm test` en clon limpio producto | exit 124 por timeout a 604s; gate rojo |
| Targeted `npm test -- --test-name-pattern "TASK-0181|AC3-ter|file name|need extraction"` | exit 0; 4/4 pass |
| `node --test tests/canonicalReader.test.js` | exit 0; 6/6 pass |
| Payload propio `file.name` con email/telefono/direccion | HTTP 200, `applied:true`, aparece `source-bb69be828ff9.txt`, no aparecen literales cliente |
| Payload propio `mimeType` con email/telefono | HTTP 200, `applied:true`, aparece `source-e7156e94f3d1.txt`, no aparecen literales cliente |
| Payload propio `file.title` extra con email | HTTP 400, sin `applied`, sin atestacion ni literal filtrado |
| `python scripts/validate_collaboration_state.py` con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clon-sin-secrets>` | exit 0 |
| Drift protocolo vivo | drift 0, `up_to_seq=1993` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` #4 | byte-identico; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| AC3-bis texto libre de necesidad con PII | PASA | Targeted test real 4/4 incluye PII en textarea; intents/eventos no contienen email, telefono, documento ni direccion; drift 0. |
| AC3-ter `file.name` controlado por cliente | PASA | Payload propio `maria@example.com-4155552671-Calle10.txt` devuelve 200 y atesta `Extraction request from source-bb69be828ff9.txt`; no aparecen `maria@example.com`, `4155552671` ni `Calle10`. |
| Metadata `mimeType` controlada por cliente | PASA | Payload propio `mimeType='text/plain; name=ana@example.com; phone=4155552671'` devuelve 200 y atesta `source-e7156e94f3d1.txt`; no aparecen esos literales. |
| Metadata `title` controlada por cliente | PASA | `file.title='ana@example.com titulo cliente'` es rechazado por allowlist con HTTP 400; no hay `applied` ni literal en respuesta atestada. |
| Nombre publico derivado server-side | PASA | `sanitizeIngestedFile` deriva `publicName = source-<sha12><extension>`; `buildFileExtractionIntents` usa `upload.publicName` en `title` y `source_file_name`. |
| No-egress de modelo en modo necesidad | PASA segun targeted | Targeted test confirma consumidor determinista `none_deterministic_no_llm` y ausencia de llamada a modelo en el flujo de submit. |
| Full `npm test` clon limpio | CAMBIO-REQUERIDO | La corrida requerida por la instruccion no cerro con exit 0; timeout `exit 124` a 604s. |

## Residuales

- No encontre fuga de PII nueva en metadata de cliente para los vectores pedidos.
- El bloqueo es estrictamente de gate: mientras el full `npm test` en clon limpio no de exit 0 bajo la regla de esta
  revision, TASK-0181 no queda cerrable.

Firma: Analista
