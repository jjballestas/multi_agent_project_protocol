---
artifact_id: ANALISTA-TASK-0157-egress-pii-veredicto
task_id: TASK-0157
author: Analista
type: review_verdict
created_at: 2026-06-23
product_anchor: D:/Agentes/Zeus/Zeus-protocol@2afc944
protocol_anchor_cited: multi_agent_project_protocol@2e72cf9
protocol_head_reviewed: 7172e75
verdict: CERRABLE
---

# Veredicto Analista - TASK-0157

Firma: Analista.

## Veredicto

OK -> CERRABLE.

No halle un escape nuevo en el vector AC58 ni regresion en AC52/AC43/AC16. El auto commit+push no actua como
segundo escritor: se ejecuta despues de `runtime/submit_intent.py` y commitea/pushea los paths derivados del
resultado gobernado (`materialization.paths`, runtime state y task files escritos por el builder). Los runtime
overrides siguen fuera de version control y los configs versionados siguen `enabled:false`.

## Ancla canonica

- Producto revisado en clon limpio: `D:/Agentes/Zeus/Zeus-protocol@2afc944`.
- Protocolo citado por la instruccion: `2e72cf9`.
- Protocolo HEAD al emitir este veredicto: `7172e75` (solo corrige rr=false del mensaje de review).
- No use el working tree del producto como fuente de verdad.

## Reproduccion

| Prueba | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 2afc944` | exit 0 |
| `npm test` en clon limpio | primera corrida timeout local a 124s; segunda corrida exit 0, 50/50 pass |
| `node --test --test-name-pattern "auto commit push lands only exact submit_intent outputs\|auto commit push reports non-fast-forward\|candidate review stays outside the ledger\|local-vlm extractor is loopback-only\|AC55-AC57\|AC58\|file ingestion is gated"` | exit 0, 8/8 pass |
| Payloads propios sobre exports front (`buildFileRequirementPayload`, `buildCandidateApprovalPayload`, `redactRequirementText`) | exit 0 |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clone without secrets>` | exit 0 |
| Drift runtime | exit 0, `has_drift=false`, `up_to_seq=1233` |
| `python scripts/scan_domain_neutrality.py --root .` | exit 0 |
| `python scripts/scan_encoding.py --root .` | exit 0 |
| `git diff --exit-code -- protocol.config.json runtime/state/genesis.json runtime/state/agent_keys runtime/state/events.jsonl runtime/state/snapshot.json` | exit 0 (#4 byte-identica en rutas criticas) |

## Vectores revisados

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| AC58 no es segundo escritor | PASA | `runSubmitIntent` llama `runtime/submit_intent.py` antes de `commitAndPushSubmitIntentOutputs`. El commit usa `git add -- <paths>` y `git commit --only -- <paths>`. La suite prueba dirty y staged ajenos y confirma que no entran al commit. |
| AC58 no filtra secretos/PII por push | PASA | Los paths pusheados vienen del output gobernado y del seed markdown escrito por el builder. Raw uploads y candidate store viven en os temp, no en el repo. `.gitignore` cubre `commit-push.runtime.json`, `file-ingestion.runtime.json` y `.secrets/`. El payload publicable redacta PII estructural en los builders probados. |
| AC58 off-by-default | PASA | `commit-push.config.json` y `file-ingestion.config.json` versionados mantienen `enabled:false`; `resolveRuntimeConfigPath` prefiere `*.runtime.json` solo si existe y la env var mantiene precedencia por inicializacion. |
| Carry AC52 loopback extractor | PASA | `sanitizeLocalVlmConfig` usa host raw extraido del endpoint y `isLoopbackHost`; la suite cubre decimal, octal, hex, externos, sufijos, IPv4-mapped y leading-zero como rechazados, y acepta localhost/127.* / `[::1]`. El nuevo boton file-mode llama la ruta existente `/api/protocol/intake-extractions/run`, no abre otra ruta de red. |
| Carry AC43/AC16 tarjetas y PII | PASA | Las candidatas se renderizan fuera del ledger; `submitCandidateApproval` bloquea sin `piiReviewed`; el servidor revalida PII humano, firma del Extractor y provenance antes de construir el intake. Narrativa e intencion pasan por redaccion antes del seed gobernado. |

## Slips intentados

| Intento | Resultado |
| --- | --- |
| Working tree con archivo sucio y staged ajeno durante auto-push | PASA: no entra al commit; lo cubre el test de remote real. |
| Non-fast-forward del remote de prueba | PASA: 409 sin sobrescribir. |
| Hosts `2130706433`, `0177.0.0.1`, `0x7f000001`, `0.0.0.0`, externo, sufijo y IPv4-mapped | PASA: extractor queda disabled/rechazado. |
| Candidata sin PII humana, firma ausente/forjada, provenance mismatch, active content | PASA: rechazado antes de ledger. |
| PII estructural en payload de archivo y candidata | PASA: plano publicable redacta; raw upload queda fuera del repo y no se pushea. |

## Residuales

- El auto-push sigue siendo egress a `origin` cuando el operador activa el runtime override. No es fuga por defecto,
  pero depende de que el remote configurado sea el esperado por el operador.
- La redaccion PII sigue siendo best-effort estructural, no garantia "PII-free" universal. El gate humano sigue
  siendo obligatorio.
- El allowlist estatico de egress no es sandbox. El control fuerte observado aqui es que el flujo nuevo reutiliza
  la ruta local-vlm loopback ya gateada y no introduce otro fetch/CLI externo.

## Recomendacion

OK -> CERRABLE. Recomiendo que Arquitecto cierre TASK-0157 si sus propios gates siguen verdes.
