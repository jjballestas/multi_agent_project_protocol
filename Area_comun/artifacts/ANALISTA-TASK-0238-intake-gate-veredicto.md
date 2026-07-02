---
artifact_id: ANALISTA-TASK-0238-intake-gate-veredicto
task_id: TASK-0238
from: Analista
to: Arquitecto
type: REVIEW
status: final
created_at: 2026-07-02
canonical_protocol_head: 66b9401
implementation_commit: 0efe196
delivery_commit: 17c5973
product_anchor: b2b2395
recommendation: CAMBIO-REQUERIDO
---

# Veredicto TASK-0238 - Intake gate determinista

Firma: Analista.

## Ancla canonica

- Protocolo revisado en clon limpio: `66b9401` (`mailbox(REVIEW): Arquitecto -> Analista gate adversarial TASK-0238`).
- Implementacion citada: `0efe196`.
- Entrega citada: `17c5973`.
- Producto: la instruccion/handoff no cita commit de producto nuevo y declara Zeus-protocol untouched; use clon limpio de `D:/Agentes/Zeus/Zeus-protocol` en HEAD `b2b2395da39090109db6de2dc50726dbaab1a11e` como regression externo.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm test --prefix <clean Zeus clone>` en `b2b2395` | exit 0; 109 tests, 87 pass, 22 skipped |
| `python -m unittest scripts.test_intake_gate` en clon protocolo `66b9401` | exit 0; 11 tests |
| `python scripts/validate_collaboration_state.py --root <clean protocol clone>` | exit 0; warning de mailbox FYI stale |
| `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root <clean protocol clone>` | exit 0; warning de mailbox FYI stale |
| `python scripts/scan_encoding.py --root <clean protocol clone>` | exit 0 |
| `python scripts/scan_domain_neutrality.py --root <clean protocol clone>` | exit 0 |
| `python scripts/validate_collaboration_state.py` en repo vivo | exit 0; warning de mailbox FYI stale |
| `python scripts/scan_encoding.py` en repo vivo | exit 0 |
| `python scripts/scan_domain_neutrality.py` en repo vivo | exit 0 |
| Drift vivo via `runtime.protocol_replay.protocol_state_drift(Path("."))` | exit 0; `has_drift=false`, `up_to_seq=3268` |
| `protocol.config.json` sha256 en `0efe196^`, `0efe196`, `66b9401`, `HEAD` y worktree | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` byte-identico |

## Tabla vector por vector

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| R0 anti-retroactividad para ids `<= TASK-0238` | PASA | Payloads propios: `TASK-0238` sin intake valida en `ready`, `claimed`, `in_progress`, `in_review`, `done`, `review_approved`, `qa_pending`, `qa_failed`, `architect_review`. HEAD limpio valida verde. Conteo propio: 176 tareas pre-boundary en estados enforced sin bloque intake quedan exentas. |
| R1 aplica solo a ids posteriores a `TASK-0238` | PASA | Payloads propios: `TASK-0239` sin intake falla en todos los estados enforced anteriores con `Task TASK-0239 missing intake block`; `TASK-0239` en `proposed` sin intake valida. |
| N1-N4 basicos de intake incompleto / placeholder / enum | PASA | Tests propios y `scripts.test_intake_gate` cubren missing block, `goal: ''`, acceptance `TBD` y `risk: severe`; todos fallan en el validador. |
| N6 submit_intent proposed->ready con intake invalido | PASA para missing intake | Test suite y payload propio rechazan missing intake antes de cambiar `TASK_INDEX`; estado queda `proposed`. |
| R0 fuera de config pineado | PASA | `Area_comun/protocol/INTAKE_GATE.json` contiene `enabled:true`, `start_task_id:TASK-0238`; `protocol.config.json` permanece byte-identico con hash #4 esperado. |
| Neutralidad / encoding | PASA | Gated con scans exit 0 en clon limpio y repo vivo. |
| R5 `intake_exempt: true` exige `exception_ref` valido existente | SLIPS | Payload propio en Python validator: `TASK-0239 ready` con `intake_exempt: true` y `exception_ref: 999`, sin ningun evento `exception.recorded`, devuelve `errors=[]`. Payload propio en PowerShell validator sobre el mismo caso devuelve `OK: collaboration state is valid.` Runtime `submit_intent` con la misma tarea `proposed -> ready` acepta la transaccion (`applied=True`) y deja `TASK_INDEX` en `ready`. |

## Hallazgo bloqueante

**F-0238-01 - Escape de exencion sin evento registrado.**

El SPEC s.2 R5 exige que `intake_exempt: true` requiera `exception_ref` valido, es decir un evento existente `exception.recorded` con `kind=intake_exempt` y `task_id` coincidente. La implementacion no cumple la familia: un task post-boundary puede entrar a `ready` con solo:

```yaml
intake:
  intake_exempt: true
  exception_ref: 999
```

sin evento de excepcion real. El validator Python y el validator PowerShell quedan verdes, y `runtime/submit_intent.py` acepta `proposed -> ready`. Esto rompe la garantia de excepcion gobernada y convierte el escape en un string no verificable.

Raiz observable:

- En validators, el caso con `exception_ref: 999` sin eventos no reporta error de intake.
- En runtime, `validate_intake_for_ready` solo verifica que `exception_ref` sea no vacio; no valida existencia, tipo ni task_id del evento.
- El test positivo llamado `test_p3_ready_with_recorded_exception_validates` no materializa ningun evento `exception.recorded`, por lo que no prueba "recorded".

## Residuales

- No encontre escape nuevo en R0/R1 para familias de status enforced ni ruptura del pin #4.
- El producto Zeus no tiene commit ancla citado para TASK-0238; el regression externo en el HEAD local citado salio verde.
- El warning de mailbox FYI stale preexistente no afecta el gate de TASK-0238, pero sigue pendiente de higiene por el owner autorizado.

## Recomendacion

CAMBIO-REQUERIDO. No cerrable hasta que R5 sea hard-gate real en Python validator, PowerShell validator y `submit_intent`, con tests negativos permanentes para `exception_ref` inexistente, evento de otro kind y evento de otro `task_id`, mas un positivo con evento `exception.recorded` valido.
