# ANALISTA - TASK-0239 re-gate actor remediation

Firma: Analista
Fecha: 2026-07-02

## Veredicto

OK -> CERRABLE.

La remediacion F-0239-01 queda cerrada: un intent `exception` con `payload.actor != actor_id` es rechazado antes de idempotency/event emission, tambien dentro de transacciones. No encontre escape nuevo en la familia revisada. La recomendacion es cerrar TASK-0239 tras el circuito normal de Arquitecto/Codex.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo instruccion REVIEW | `f2c972db70232b9e2e188aa503ad30fd4c1cf0c8` |
| Implementacion remediacion | `bc9cc8d84927f32837cdfc9ee5cdc301f6115aaa` |
| Producto control Zeus-protocol | `b2b2395da39090109db6de2dc50726dbaab1a11e` |
| Clean clone base | `C:/Users/johnb/AppData/Local/Temp/analista-0239-regate-4e5782fe3e0744f39477b13da4b70d2b` |
| #4 pin `protocol.config.json` | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `npm test` en clean clone Zeus-protocol `b2b2395...` | EXIT 0, 109 tests, 87 pass, 22 skipped |
| `python scripts/test_exception_recorded.py` en clean clone protocolo `f2c972...` | EXIT 0, 6 tests |
| `python scripts/test_intake_gate.py` en clean clone protocolo `f2c972...` | EXIT 0, 12 tests |
| `python -m py_compile runtime/submit_intent.py runtime/protocol_replay.py scripts/test_exception_recorded.py` | EXIT 0 |
| `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` | EXIT 0 |
| `python scripts/validate_collaboration_state.py` live y clean | EXIT 0 / EXIT 0 |
| `python scripts/scan_domain_neutrality.py` live y clean | EXIT 0 / EXIT 0 |
| `python scripts/scan_encoding.py` live y clean | EXIT 0 / EXIT 0 |
| `protocol_state_drift(Path('.'))` live y clean | `has_drift=false`, `up_to_seq=3315` |

## Vectores adversariales

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| F-0239-01: `actor=Arquitecto`, caller `implementer_agent`, single submit | PASA | Rechaza con `exception.actor must match caller actor_id`; eventos antes/despues 0/0. |
| F-0239-01 en transaccion `good+bad` | PASA | Rechaza con el mismo error; eventos antes/despues 0/0, sin append parcial del intent bueno. |
| Test permanente | PASA | `scripts/test_exception_recorded.py::test_rejects_actor_mismatch` cubre actor ajeno y la suite completa sale EXIT 0. |
| Actor shape confusion | PASA | `actor` list, dict, int, bool y string con NUL rechazan; whitespace externo en string exacto trimmea a caller y emite como `implementer_agent`. |
| Round-trip firmado/listable/drift 0 | PASA | Eventos `exception.recorded` propios quedan listables por task; drift del probe `has_drift=false`. |
| 4 rechazos base TASK-0239 | PASA | kind fuera de enum `free_text`, summary no-ASCII, duplicate id y task inexistente cubiertos por suite EXIT 0. |
| Enums cerrados | PASA | `kind` fuera de enum rechaza; valores documentados en `EXCEPTION_KINDS` son los aceptados. |
| U1-U3 y U2 publicable | PASA | `TASK_PROTOCOL.md` contiene U1/U2/U3 y lista publica por id/kind/task_id/actor/beneficiary/channel/impact/summary. |
| Puente R5 TASK-0238 | PASA | `python scripts/test_intake_gate.py` EXIT 0: exception_ref inexistente, kind incorrecto y task incorrecto rechazan; el positivo con evento real queda cubierto. |
| Pin #4 | PASA | SHA256 byte-identico `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Residuales

- `require_text` sigue normalizando algunos campos con `str(...).strip()`. Para `actor`, las formas no-string probadas no escapan porque el guard compara contra `actor_id`; el residual es de estilo/robustez, no bloqueante para F-0239-01.
- El clean clone de producto se uso como control por instruccion; TASK-0239 es cambio de runtime del protocolo y Zeus-protocol quedo sin tocar.

## Recomendacion

CERRABLE.
