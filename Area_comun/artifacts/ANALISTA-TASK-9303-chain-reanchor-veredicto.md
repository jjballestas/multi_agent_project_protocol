# Veredicto Analista - TASK-9303 chain reanchor

Firma: Analista
Ancla canonica hub: `634d841` instruccion `MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9303-chain-reanchor.md`; HEAD observado del hub `3d2d97a`.
Ancla canonica Aegis: commit `95717820b9390f4a73cb8072ac4fb570fcd7a68d`; repo limpio clonado desde `D:/Agentes/Zeus/NOVA/Aegis` en `%TEMP%/aegis-review-9303-d5e3e7c9ddad41d9a89754859545570f`.

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

El mecanismo base pasa los gates nominales y preserva el segmento viejo por sello byte-identico. El bloqueo es falsable: `validate_chain` acepta mutaciones del payload del evento `chain.regenesis_boundary` y de `config_epoch_history` que alteran el sello declarado de historia sin invalidar la cadena. Esto contradice el criterio 4 en su forma fuerte: "tamper en cualquier segmento/evento debe fallar". El escape no requiere reescribir historia ni romper `prev_hash`; basta alterar metadatos de frontera/sello que el validador usa como registro de epoca.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/NOVA/Aegis <tmp>; git checkout 95717820` | EXIT 0 |
| `python examples/chain_cases/run_tests.py` | EXIT 0, 14/14 |
| `python scripts/validate_collaboration_state.py` en clon limpio Aegis | EXIT 0 |
| `python scripts/scan_encoding.py` en clon limpio Aegis | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en clon limpio Aegis | EXIT 0 |
| `validate_chain(all_events, protocol.config)` en clon limpio Aegis | valid true, checked_events 3142 |
| Drift Aegis por `protocol_state_drift` | has_drift false, up_to_seq 3814 |
| Sello segmento 672..3807 recomputado con `runtime.regenesis.event_segment_lines` | `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`, match true |
| Hub `python scripts/validate_collaboration_state.py` con secretos | EXIT 0 |
| Hub secretless clean clone `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Hub `python scripts/scan_encoding.py` con/sin secretos | EXIT 0 / EXIT 0 |
| Hub `python scripts/scan_domain_neutrality.py` con/sin secretos | EXIT 0 / EXIT 0 |
| Hub drift | has_drift false, up_to_seq 4576 |
| Hub `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Nova-Budget `npm test` | N/A por instruccion canonica: SIN producto en alcance |

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| crit.1 validate + drift tras reanchor | PASA | Aegis validate EXIT 0; drift false up_to_seq 3814 |
| crit.2 historia vieja preservada | PASA | Segmento 672..3807 recomputa sha256 `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`; event_count 3136 |
| crit.3 nuevo segmento contra config actual | PASA | `validate_chain` valid true sobre eventos hasta 3814; evento post-frontera encadena desde hash nuevo |
| crit.4 tamper payload en evento viejo seq 1000 | PASA | `validate_chain` falla: `corruption at seq 1000: hash mismatch` |
| crit.4 tamper actor_auth sig en evento viejo seq 1000 | PASA | `validate_chain` falla: `corruption at seq 1000: hash mismatch` |
| crit.4 tamper prev_hash en evento viejo seq 1000 | PASA | `validate_chain` falla: `corruption at seq 1000: hash mismatch` |
| crit.4 tamper payload en evento nuevo seq 3813 | PASA | `validate_chain` falla: `corruption at seq 3813: hash mismatch` |
| crit.4 tamper actor_auth sig en evento nuevo seq 3813 | PASA | `validate_chain` falla: `corruption at seq 3813: hash mismatch` |
| crit.4 tamper prev_hash en evento nuevo seq 3813 | PASA | `validate_chain` falla: `corruption at seq 3813: hash mismatch` |
| crit.4 tamper `chain.regenesis_boundary.payload.boundary_id` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `chain.regenesis_boundary.payload.old_config_hash` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `chain.regenesis_boundary.payload.sealed_segment.sha256` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `chain.regenesis_boundary.payload.sealed_segment.event_count` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `chain.regenesis_boundary.payload.sealed_segment.seq_range` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `config_epoch_history[0].sealed_segment.sha256` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `config_epoch_history[0].sealed_segment.event_count` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.4 tamper `config_epoch_history[0].boundary_seq` | SLIPS | `validate_chain` devuelve valid true / `chain valid` |
| crit.5 idempotencia | PASA nominal | `examples/chain_cases/run_tests.py` cubre 14 casos y no duplica frontera en el caso existente; no encontre duplicacion nueva |
| crit.6 hub intacto | PASA | Hub config sha256 sigue `2E35F26E...`; drift hub 0; no cambio de config/genesis del hub |
| crit.7a signer throwaway real | PASA | Harness importa `cryptography.hazmat.primitives.asymmetric.ed25519`, genera keypair raw, firma payload, valida firma buena y rechaza firma corrupta |
| crit.7b jheredia-live | DIFERIDO | Correctamente fuera de alcance por instruccion canonica |

## Hallazgo bloqueante

F-9303-01 [CRITICAL] La frontera de epoca no esta protegida como evento completo.

Repro minimo en el clon limpio:

```python
from copy import deepcopy
from pathlib import Path
from runtime.eventlog import all_events, read_protocol_config
from runtime.protocol_replay import validate_chain

root = Path(".")
config = read_protocol_config(root)
events = all_events(root)
idx = next(i for i, e in enumerate(events) if e.get("type") == "chain.regenesis_boundary")

mutated = deepcopy(events)
mutated[idx]["payload"]["sealed_segment"]["sha256"] = "0" * 64
print(validate_chain(mutated, config, root=root))
```

Salida observada:

```text
{'valid': True, 'reason': 'chain valid', 'checked_events': 3142, 'head': '66d314fc5538e4aa0e705c37f4139aad6668ac158fdd366ade9f11e2fa7d4bf8'}
```

El mismo patron ocurre con `payload.boundary_id`, `payload.old_config_hash`, `payload.sealed_segment.event_count`, `payload.sealed_segment.seq_range` y con los campos homonimos en `protocol.config.json/config_epoch_history`. En el evento de frontera, `validate_chain` compara solo `prev_hash` contra `new_config_hash`; no vuelve a hashear el payload de frontera ni exige equivalencia completa evento<->config para el sello. Por eso un tamper del registro que declara que historia quedo sellada no muerde.

## Residuales

- `event_auth.signature` mutada in-memory no hace fallar `validate_chain` porque ese campo no participa en el hash de cadena. No lo marco como bloqueo independiente si el contrato considera "firma" = `actor_auth` ed25519, pero queda declarado: la deteccion de HMAC depende de otro gate con secretos, no de `validate_chain`.
- No ejecute Nova-Budget `npm test`: la instruccion canonica de review declara SIN producto en alcance.

## Fix-loop esperado

Remediacion: hacer que `validate_chain` falle cerrado si el evento `chain.regenesis_boundary` no coincide byte/semanticamente con la entrada `config_epoch_history` y si el sello declarado no verifica contra las lineas 672..N. Agregar negativos permanentes para tamper de `boundary_id`, `old_config_hash`, `sealed_segment.sha256`, `event_count` y `seq_range`, tanto en payload de frontera como en config. Re-gatear chain_cases, validate, scan_encoding, scan_domain_neutrality, drift 0 y re-juicio Analista antes del cierre. Maximo 2 iteraciones antes de escalar al operador si sobrevive la misma clase de slip.

## Envelope

task_id: TASK-9303
status: CAMBIO-REQUERIDO
executive_summary: validate_chain pasa gates nominales, pero acepta mutaciones del payload de chain.regenesis_boundary y del sello config_epoch_history; por tanto el re-anclaje no es cerrable.
artifacts: Area_comun/artifacts/ANALISTA-TASK-9303-chain-reanchor-veredicto.md
gates: Aegis chain_cases EXIT 0 14/14; Aegis validate EXIT 0; Aegis encoding EXIT 0; Aegis neutrality EXIT 0; Aegis drift false up_to_seq 3814; hub validate con/sin secretos EXIT 0; hub encoding/domain EXIT 0; hub drift false up_to_seq 4576.
next_recommended: Codex debe endurecer validate_chain para proteger frontera/sello y pedir re-juicio Analista; cierre no recomendado.
risks: Si se cierra asi, el registro de que segmento historico quedo sellado puede ser alterado sin que validate_chain falle.
