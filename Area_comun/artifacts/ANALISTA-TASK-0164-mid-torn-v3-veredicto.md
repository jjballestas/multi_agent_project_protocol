# ANALISTA TASK-0164 mid-torn v3 veredicto

Firma: Analista

## Veredicto

RECOMENDACION DE CIERRE: OK->CERRABLE.

El fix v3 cumple la garantia que bloqueo v2: cuando aparece una linea JSONL invalida en medio y existe un evento valido despues, `submit_intent` falla cerrado, no trunca, no descarta la linea valida posterior, no reporta `applied:true` y no agrega eventos invisibles. La reparacion de tail-torn final sigue aplicando y los writers concurrentes quedan lineales bajo lock.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo citado por la instruccion/checker | `90958cff21b70f1320001c22812f341d21625550` |
| Implementacion TASK-0164 fix3 | `434b2e9 fix(runtime): fail closed on mid-log torn records` |
| Handoff fix3 | `Area_comun/handoffs/HANDOFF-TASK-0164-codex-to-arquitecto-3.md` |
| Producto Zeus revisado | `4faacd17adff3c341efa2f545e3701c313f7663c` |
| Repo de pruebas | clones limpios bajo `C:/tmp/analista-task0164-v3/` |
| #4 config sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Reproduccion y gates

| Prueba | Resultado |
| --- | --- |
| `git clone` protocolo + checkout `90958cf` | exit 0 |
| `git clone` Zeus + checkout `4faacd1` | exit 0 |
| Zeus `npm test` en clon limpio | exit 0, 57/57 |
| `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` | exit 0, 8/8 |
| `python examples/intent_tx_cases/run_intent_tx_cases.py` | exit 0, 10/10 |
| `python scripts/validate_collaboration_state.py` en clon limpio sin secretos | exit 0 |
| `python scripts/validate_collaboration_state.py` en repo vivo con secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py --root .` | exit 0 |
| `python scripts/scan_encoding.py --root .` | exit 0 |
| Drift clon limpio | `has_drift=false`, `up_to_seq=1478` |
| Drift repo vivo antes de este veredicto | `has_drift=false`, `up_to_seq=1486` |
| `validate_chain` clon limpio | valid true, 806 checked events |
| `validate_chain` repo vivo | valid true, 814 checked events |
| agent_signatures / anchor | valid true en ambos; `checked=0` por configuracion actual |
| #4 byte-identica | `protocol.config.json` mantiene sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Tabla vector por vector

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Middle torn `[valid, torn-json, valid-after]` | PASA | Payload propio: `submit_intent` return/falla por integridad; bytes intactos; `valid-after` preservado en bytes; evento nuevo ausente; visibles por lector torn-safe siguen en 1. |
| Middle non-object `[valid, [], valid-after]` | PASA | Payload propio: misma falla cerrada; bytes intactos; `valid-after` preservado. Cubre JSON parseable pero no evento objeto. |
| Garantia "no descartar valid-after" | PASA | En ambos middle cases el log queda byte-identico al corrupto original y conserva la linea valida posterior. |
| Garantia "no applied:true en mid-file torn" | PASA | El submit lanza error antes de aplicar; el idempotency key nuevo no aparece en el log. |
| Tail torn final | PASA | Payload propio: `applied=true`, `log_repair` presente, evento nuevo visible, `validate_chain.valid=true`, drift false. |
| Tail torn final + cuatro writers concurrentes | PASA | Returncodes `[0,0,0,0]`, un solo reporte de `log_repair`, 10 eventos visibles, `prev_hash` lineal, `validate_chain.valid=true`, drift false. |
| Middle torn + dos writers concurrentes | PASA | Returncodes `[1,1]`, ambos con error de integridad, bytes intactos, `valid-after` preservado, ningun `CLAIM-mid-conc-*` agregado. |
| Claims por-fila / compat / lock normal | PASA | Goldens oficiales `row_scoped_claim_cases` 8/8 e `intent_tx_cases` 10/10 exit 0. |

## Residuales declarados

- El producto Zeus no cita commit nuevo en la instruccion v3; use `4faacd1`, el ultimo commit de producto anclado en las pasadas de TASK-0164, para cumplir el gate de clon limpio `npm test`.
- `read_jsonl_torn_safe` sigue leyendo solo el prefijo ante corrupcion media. Eso ya no es cierre falso porque el camino escritor (`submit_intent`) falla cerrado bajo lock y no trunca ni aplica cuando hay evento valido posterior.
- Los checks de agent_signatures/anchor devuelven valid true con `checked=0` en la configuracion actual; lo reporto como evidencia del validador, no como firma material nueva.

