# ANALISTA - Veredicto TASK-9304 F-9304-01 re-juicio

Firma: Analista

## Veredicto

OK/CERRABLE para F-9304-01. El hallazgo original queda cerrado: en clon limpio de Aegis, mutar el export
`pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl` ya hace fallar `validate_collaboration_state.py`
con exit 1 y `validate_chain` devuelve `valid=false` con razon `pre_t0 sealed export hash mismatch`.

Ancla canonica revisada:

- Hub/protocolo REVIEW HEAD: `77a2583acc6aaedc5ca6aa5f9b1bb271d5506ea9`
- Instruccion: `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9304-F9304-01-rejuicio.md`
- Aegis clean clone: `8159716cfaa0b3720de889841b14b82844730799`
- Fix citado: `7f80e481` (`runtime/protocol_replay.py`)
- Aegis `protocol.config.json` sha256: `77242D63090144C8818426927CC8AF149F4FE36C7637AE1B84387674D4BDD283`

## Reproduccion y gates

| Gate / prueba | Resultado |
|---|---|
| `python examples/chain_cases/run_tests.py` en Aegis clean clone | EXIT 0, 40/40 |
| `python scripts/validate_collaboration_state.py` en Aegis clean clone | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en Aegis clean clone | EXIT 0 |
| `python scripts/scan_encoding.py` en Aegis clean clone | EXIT 0 |
| `validate_chain` directo en Aegis clean clone | `valid=true`, `checked_events=3184` |
| Drift Aegis clean clone | `has_drift=false`, `up_to_seq=3856` |
| Hub `python scripts/validate_collaboration_state.py` con secretos | EXIT 0 |
| Hub clean clone sin `secrets/`, `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Hub `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Hub `python scripts/scan_encoding.py` | EXIT 0 |
| Hub drift | `has_drift=false`, `up_to_seq=4627` |
| Hub chain | `valid=true`, `checked_events=3955` |
| Hub `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Nova-Budget root `npm test` en clean clone | EXIT `-4058`, sin `package.json`; fuera del alcance canonico de este REVIEW |

## Vectores revisados

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| F-9304-01: tamper del export `pre_t0` debe fallar cerrado | PASA | Append de `tamper` al export pre-T0: validator EXIT 1 con `Runtime event log chain invalid: pre_t0 sealed export hash mismatch`; `validate_chain` directo: `valid=false`, `seq=pre_t0`. |
| Negativo permanente y real | PASA | `GC-40-pre-t0-export-tamper` existe en `examples/chain_cases/run_tests.py`, escribe un export pre-T0 real, lo muta con `tamper`, y exige `pre_t0 sealed export hash mismatch`; suite 40/40 EXIT 0. |
| Re-verificacion del sello, no confianza ciega en el export | PASA | `validate_pre_t0_seal` lee bytes del path declarado, recompone sha256, cuenta lineas no vacias y verifica `seq_range` primera/ultima linea. |
| No regresion F-9303-01: frontera/config de epocas | PASA | Probe propio: mutar `config_epoch_history[1].boundary_id` devuelve `valid=false`; mutar `payload.sealed_segment.event_count` del boundary seq 3837 devuelve `valid=false`. |
| Epocas 1/pre_t0 byte-identicas | PASA | `protocol.config.json` byte-identico entre `00ccb55b9d02e676c9cf31218f4ae1edc25c3ee1`, `7f80e481` y `8159716c`: sha256 `77242D63090144C8818426927CC8AF149F4FE36C7637AE1B84387674D4BDD283`. |

## Residuales declarados

- `jball-live` queda diferido a la maquina de John por diseno de la instruccion; no lo uso como faltante.
- Un ataque coordinado que muta el export pre-T0 y tambien reescribe `protocol.config.json` para declarar el nuevo
  sha/count/range valida verde en mi probe aislado. No bloquea este cierre porque el contrato operativo exigido aqui
  incluye #4 byte-identica de `protocol.config.json`; sin esa comparacion externa, el sello declarado no es una raiz
  de confianza suficiente.
- `npm test` en la raiz de `Nova-Budget` limpio devuelve `-4058` por ausencia de `package.json`. Lo registro porque
  el prompt operativo generico lo pidio, pero el REVIEW canonico de TASK-9304 declara `SIN producto Nova-Budget en
  alcance`; no lo trato como gate de cierre de Aegis.

## Recomendacion de cierre

OK -> CERRABLE para TASK-9304 F-9304-01. No pido segunda remediacion.

task_id: TASK-9304
status: OK/CERRABLE
executive_summary: F-9304-01 esta cerrado; el tamper pre_t0 que antes validaba verde ahora falla cerrado por validator y validate_chain.
artifacts: Area_comun/artifacts/ANALISTA-TASK-9304-F9304-01-rejuicio-veredicto.md
gates: Aegis chain_cases 40/40 EXIT 0; Aegis validate/domain/encoding EXIT 0; hub validate con y sin secretos EXIT 0; hub domain/encoding EXIT 0; drift 0; #4 byte-identica.
next_recommended: Arquitecto puede ratificar el re-juicio y rutear el cierre correspondiente; no ejecutar jball-live hasta la ventana de John.
risks: Validacion pre_t0 depende de que protocol.config.json siga byte-identico/anclado; Nova-Budget root npm test falla fuera de alcance canonico.
