# ANALISTA TASK-9304 jball reanchor verdict

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

La epoca 2 de Aegis para `jball:v1` pasa los gates nominales y los negativos F-9303-01 para boundary/config-history. El bloqueo es falsable: el AC de TASK-9304 pide que un tamper en `pre_t0` haga fallar `validate_chain`, pero un clon limpio con `pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl` modificado sigue con `validate_collaboration_state.py` exit 0 y `validate_chain.valid=true`.

## Ancla canonica

| Item | Valor |
|---|---|
| Hub REVIEW | `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9304-jball-reanchor.md` |
| Hub HEAD revisado | `b8393eec02635ecc458246efe933ae751f6f975a` |
| Aegis repo | `D:/Agentes/Zeus/NOVA/Aegis` |
| Aegis commit revisado | `00ccb55b9d02e676c9cf31218f4ae1edc25c3ee1` |
| Producto Nova-Budget | NOT_RUN por instruccion canonica: SIN producto Nova-Budget en alcance |

## Reproduccion por gates

| Gate | Repo/contexto | Exit | Resultado |
|---|---|---:|---|
| `python examples/chain_cases/run_tests.py` | Aegis clean clone `00ccb55b` | 0 | PASS 39/39 |
| `python scripts/validate_collaboration_state.py` | Aegis clean clone `00ccb55b` | 0 | PASS |
| `python scripts/scan_encoding.py` | Aegis clean clone `00ccb55b` | 0 | PASS |
| `python scripts/scan_domain_neutrality.py` | Aegis clean clone `00ccb55b` | 0 | PASS |
| `protocol_state_drift(Path('.'))` | Aegis clean clone `00ccb55b` | 0 | `has_drift=false`, `up_to_seq=3841` |
| `validate_chain(events_in_log_order, config)` | Aegis clean clone `00ccb55b` | 0 | `valid=true`, `checked_events=3169` |
| `python scripts/validate_collaboration_state.py` | Hub vivo con secretos | 0 | PASS |
| `python scripts/validate_collaboration_state.py` | Hub clean clone sin `secrets/` | 0 | PASS |
| `python scripts/scan_encoding.py` | Hub vivo | 0 | PASS |
| `python scripts/scan_domain_neutrality.py` | Hub vivo | 0 | PASS |
| `protocol_state_drift(Path('.'))` | Hub vivo | 0 | `has_drift=false`, `up_to_seq=4625` |
| `validate_chain(events_in_log_order, config)` | Hub vivo | 0 | `valid=true`, `checked_events=3953` |

Hub #4: `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, `protocol_version=1.14.0`.

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Epoca 1 preservada | PASA | Sello `[672,3807]`: 3136 lineas, sha256 `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`, match config. |
| Pre-T0 preservado byte-identico | PASA parcial | Archivo `pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl`: 671 lineas, sha256 `7e2452aef71352c863f467612a4b3742446574d342c100020619055ff186fbe3`, match config. |
| Epoca 2 sellada sin solape | PASA | Sello `[3809,3836]`: 28 lineas, sha256 `705469a433b21954ccb09378067efd656e2cdbfcceb2f751620ee4f02538e115`, boundary seq `3837`, sin solape con epoca 1. |
| F-9303-01 payload boundary epoca 2 | PASA | Tamper de `boundary_id`, `old_config_hash`, `sealed_segment.sha256`, `event_count`, `seq_range` en evento seq 3837 falla cerrado con `regenesis boundary config payload mismatch`. |
| F-9303-01 config history epoca 2 | PASA | Tamper de `boundary_id`, `old_config_hash`, `sealed_segment.sha256`, `event_count`, `seq_range` en `config_epoch_history[1]` falla cerrado. |
| Tamper evento/prev_hash epoca 1 | PASA | Mutar evento o `prev_hash` en seq 673 falla con `corruption at seq 673: hash mismatch`. |
| Tamper evento/prev_hash epoca 2 | PASA | Mutar evento o `prev_hash` en seq 3810 falla con `corruption at seq 3810: hash mismatch`. |
| Tamper evento/prev_hash post-epoca 2 | PASA | Mutar evento o `prev_hash` en seq 3838 falla con `corruption at seq 3838: hash mismatch`. |
| `jball:v1` registrado | PASA | `event_state.signature_config.public_keys["jball:v1"] = pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=` y `agent_registry.agents` contiene `id=jball`, `capabilities=["implementer"]`. |
| Hub intacto | PASA | Hub config mantiene `2E35F26E...` y `1.14.0`; hub chain/drift validos. |
| Tamper pre-T0 debe hacer fallar `validate_chain` | SLIPS - WARNING-real | En copia limpia de Aegis `00ccb55b`, tras `Add-Content pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl tamper`, `python scripts/validate_collaboration_state.py` devuelve exit 0 y `validate_chain` devuelve `{"valid": true, "reason": "chain valid"}`. Esto contradice AC5 de TASK-9304. |

## Hallazgo bloqueante

F-9304-01 / WARNING-real / D2-S2: la integridad de `pre_t0` no esta gateada por `validate_chain` ni por `validate_collaboration_state.py`.

Repro minimo:

```powershell
$tmp='C:/tmp/analista-aegis-pre-t0-tamper'
Copy-Item -Recurse 'C:/tmp/analista-aegis-task-9304' $tmp
Add-Content -Path "$tmp/pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl" -Value 'tamper'
cd $tmp
python scripts/validate_collaboration_state.py
python -c "from pathlib import Path; import json; from runtime.eventlog import events_in_log_order; from runtime.protocol_replay import validate_chain; cfg=json.load(open('protocol.config.json',encoding='utf-8-sig')); print(json.dumps(validate_chain(events_in_log_order(Path('.')), cfg, root=Path('.')), ensure_ascii=True))"
```

Observed: validator exit 0 and `validate_chain.valid=true`.

Expected under TASK-9304 AC5: tamper in `pre_t0` fails validation, or the AC is formally narrowed to state that `pre_t0` is only a byte-identical sealed export checked by explicit seal recomputation, not by `validate_chain`.

## Residuales

- `jball-live` intentionally remains deferred to John machine; not counted as a defect.
- Nova-Budget `npm test` intentionally NOT_RUN because the canonical REVIEW states SIN producto Nova-Budget en alcance.
- Actor `actor_auth.sig` on ordinary `intent.applied` events is chain-covered by event hash, but `validate_agent_signatures` has no live `agent.attestation` rows in this Aegis log (`checked=0`); I did not use that as a blocker because the TASK-9304 acceptance points the live-signature check to a deferred machine path.

## Fix-loop esperado

Codex/Arquitecto must either:

1. Remediate validation so `pre_t0_provenance.sealed_export` is recomputed and hard-fails on byte drift during the relevant gate, with a permanent negative for pre-T0 tamper; or
2. Record a canonical scope correction that AC5 does not require `validate_chain` to cover pre-T0 and that explicit seal recomputation is the only pre-T0 check.

After that, rerun Aegis chain cases, validate, encoding, domain, drift, hub gates with and without secrets, and request Analista re-juicio before closure. Maximum 2 iterations before operator escalation.

task_id: TASK-9304
status: change_required
executive_summary: CAMBIO-REQUERIDO. Aegis epoch 2 and F-9303-01 negatives pass, but pre-T0 tamper remains invisible to validate_chain/validate_collaboration_state despite TASK-9304 AC5 requiring tamper in any epoch including pre_t0 to fail.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-TASK-9304-jball-reanchor-veredicto.md
  - path_or_commit: Aegis commit 00ccb55b9d02e676c9cf31218f4ae1edc25c3ee1
gates:
  - command: python examples/chain_cases/run_tests.py
    result: PASS
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: pre_t0 tamper probe against validate_chain
    result: FAIL
next_recommended: Remediate or formally narrow the pre-T0 validation contract, then request Analista re-juicio before closure.
risks: Closing now would certify a broader tamper guarantee than the current validator actually enforces.
