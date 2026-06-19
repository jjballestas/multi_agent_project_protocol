# HANDOFF TASK-0117 - Codex to Arquitecto - Fase 1 encendido #4

## Estado

TASK-0117 queda listo para revision maker!=checker de Fase 1. Codex ejecuto provisioning temporal,
piloto acotado y rollback. El flip permanente NO fue realizado por Codex.

## Provisioning usado

- Ed25519 public key Codex: `u7iYTw28SJ0zsJrBIhwycMG8S9cXMw9mjCXeOUYIhks=`
- Private key fuera del repo: `D:\Agentes\_protocol_private_runtime\TASK-0117\codex_ed25519_private.raw`
- HMAC secrets fuera del repo:
  - `D:\Agentes\_protocol_private_runtime\TASK-0117\codex_event_auth_hmac.txt`
  - `D:\Agentes\_protocol_private_runtime\TASK-0117\runtime_event_auth_hmac.txt`
- Anchor target real usado: `D:\Agentes\_protocol_anchor_audit\TASK-0117-phase1`
- Anchor evidence: `HEAD` + `anchors.log` generados en el target externo.

## Piloto vivo

- Runtime event seq window: 590-630.
- AC2 N=20:
  - denominator: 20 (`event_log.agent.attestation`)
  - numerator: 20
  - health_rate: 1.0
  - anchors: 20
  - chain_valid: true
  - signatures_valid: true
  - anchors_valid: true
  - event_auth_valid: true
- Nota AC2: esta metrica es salud del instrumento, no afirmacion de seguridad.

## AC3 negativo

`python examples\attestation_negative_cases\run_attestation_negative_cases.py`

- AC3-1-payload-alteration: pass, A2
- AC3-2-event-deletion: pass, A1
- AC3-3-event-insertion: pass, A1
- AC3-4-event-reordering: pass, A1
- AC3-5-unregistered-key: pass, A2
- AC3-6-cross-attribution: pass, A2

## AC5 rollback

- `protocol.config.json` fue restaurado byte-equivalent tras la ventana temporal.
- Drift: `has_drift=false`, replay hash == hot hash, `up_to_seq=630`.
- Flags finales:
  - `event_auth.enabled=false`
  - `event_state.chain_enabled=false`
  - `event_state.agent_signatures_enabled=false`
  - `event_state.anchor_enabled=false`
- `event_auth.keys` no queda en `protocol.config.json`.

## Gates ejecutados

- `python examples\attestation_health_cases\run_attestation_health_cases.py` - OK
- `python examples\attestation_negative_cases\run_attestation_negative_cases.py` - OK
- `python examples\readonly_enforcement_cases\run_readonly_enforcement_cases.py` - OK
- `python examples\chain_cases\run_tests.py` - OK
- `python examples\agent_signature_cases\run_agent_signature_cases.py` - OK
- `python examples\anchor_cases\run_anchor_cases.py` - OK
- `python examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py` - OK
- `python scripts\scan_encoding.py --root .` - OK
- `python scripts\scan_domain_neutrality.py --root .` - OK
- `python scripts\validate_collaboration_state.py --root .` - OK, mailbox hygiene warnings only
- Runtime HMAC secret scan contra repo - OK

## Riesgo / decision para el flip permanente

El piloto demuestra que el backend actual puede anclar en un target local externo real. Para el flip
permanente, Arquitecto debe decidir si ese target local externo es suficiente para esta ventana o si exige
un remoto git independiente con credenciales fuera del repo. Codex recomienda el target local externo para
esta fase controlada y migrar a remoto independiente antes de uso distribuido.
