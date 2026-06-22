---
artifact_id: ANALISTA-TASK-0154-ux-behavior-tests-veredicto
task_id: TASK-0154
type: review_verdict
from: Analista
created_at: 2026-06-22
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: da5825d8405f3b2140e42821c6183c90bba49ec9
protocol_head: 5b04324
---

# Veredicto Analista - TASK-0154

Recomendacion: OK -> CERRABLE.

Ancla canonica revisada: producto Zeus-protocol `da5825d8405f3b2140e42821c6183c90bba49ec9` y protocolo `5b04324`. Alcance: revisar si los behavior-tests AC48/AC49/AC50 son falsables y no fake-green. No promuevo, no cierro, no ratifico estado.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Producto clean clone checkout `da5825d8405f3b2140e42821c6183c90bba49ec9` | OK |
| `npm test` en clean clone producto | exit 0, 47/47 pass |
| Mutacion AC48: quitar `governed-button` del boton compose | exit 1, falla test AC48 por ausencia de clase gobernada |
| Mutacion AC49: resetear tambien en `mode === "compose"` | exit 1, falla test AC49 (`true !== false`) |
| Mutacion AC50: cachear `loadProtocolSnapshot` por modulo | exit 1, falla test AC50 (`1.0.0 !== 1.0.1`) |
| Protocolo `python scripts/validate_collaboration_state.py` con secretos | exit 0 |
| Protocolo `python scripts/validate_collaboration_state.py` sin secretos, en clone sin `secrets/` | exit 0 |
| Drift #4 | exit 0 equivalente, `has_drift:false`, `up_to_seq:1176` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| #4 byte-identica durante la pasada | OK: `protocol.config.json`, `runtime/state/snapshot.json`, `runtime/state/events.jsonl`, `chain_manifest.json` conservaron hash SHA-256 |

Hashes #4 observados:

| Archivo | SHA-256 |
| --- | --- |
| `protocol.config.json` | `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354` |
| `runtime/state/snapshot.json` | `c67b690cbc4314043419c279024846fa229d7fd0d3d03b31e8d26d2f35e87417` |
| `runtime/state/events.jsonl` | `c5522cb2f0ce1c05379e1e237e46e1681d32cfeaec589f2c572a38f45b0a32b4` |
| `chain_manifest.json` | `030f2fa6f717b6bee780e5be71b339a9a0a0930b43c6bdf92d3093723c0b9def` |

## Vector por vector

| Vector | Veredicto | Evidencia falsable |
| --- | --- | --- |
| AC48 boton gobernado | PASA | El test localiza el boton `data-intake-step="compose"` y exige `class` con `governed-button`, ademas de `.governed-button` en CSS. Al quitar la clase del boton, el test falla con input `<button type="button" data-intake-step="compose">Nueva historia/requisito</button>`. |
| AC49 no-reset de Nueva historia | PASA | El test ejercita `deriveIntakeOutcome` con compose, preview, error y success. La familia prometida queda cubierta: solo success resetea; compose/preview/error conservan el draft. Al mutar compose para resetear, el test falla en `shouldReset false`. |
| AC50 canonico fresco sin reiniciar | PASA | El test arranca server contra repo protocolo fixture, lee `/api/protocol/snapshot`, commitea `protocol_version` 1.0.1 en el mismo repo y vuelve a leer sin reiniciar. Al introducir cache de modulo en `loadProtocolSnapshot`, el test falla porque la segunda lectura conserva `1.0.0`. |
| Suite producto | PASA | `npm test` en clone limpio del producto: 47/47 pass, exit 0. |
| Gates protocolo | PASA | validate con y sin secretos exit 0; drift 0; neutrality/encoding exit 0; #4 byte-identica. |

## Residuales

Residuales no bloqueantes:

- AC48 es una prueba de contrato de clase/CSS, no una prueba visual de layout. Es suficiente para esta tarea porque el AC pide bloquear el regreso a estilo ad-hoc, no validar pixeles.
- AC49 prueba la funcion pura `deriveIntakeOutcome` y un guard estatico del bloque compose. No simula click DOM completo, pero cubre la regla de negocio que gobierna el reset.
- AC50 cubre frescura del snapshot server-side por request. El refetch del front al navegar ya pertenece a AC29; aqui el vector pedido era que el server no cachee el canonico.

No encontre escape nuevo que haga pasar los tres tests con la regresion especificada por AC48/AC49/AC50.

Firma: Analista.
