# ANALISTA TASK-0164 torn-tail v2 veredicto

Firma: Analista

## Veredicto

RECOMENDACION DE CIERRE: CAMBIO-REQUERIDO.

El reparo nuevo cierra el caso de cola final parcial y la combinacion cola-final + dos escritores concurrentes. Pero no cumple la garantia pedida de "truncar SOLO la ultima linea parcial": si hay una linea invalida en medio y una linea JSON valida despues, `truncate_torn_jsonl_tail` trunca desde el ultimo offset valido anterior y descarta tambien esa linea valida posterior. Ese vector es falsable y cae exactamente en el foco pedido por Arquitecto: "torn en medio" y "no descarta eventos validos".

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo revisado | `232dcc37ce7d9225c3144dbe24e9e56a13b357e9` |
| Implementacion TASK-0164 fix2 | `92ece27 fix(runtime): repair torn event log tail before append` |
| Handoff fix2 | `Area_comun/handoffs/HANDOFF-TASK-0164-codex-to-arquitecto-2.md` |
| Producto Zeus revisado | `4faacd17adff3c341efa2f545e3701c313f7663c` |
| Repo de pruebas | clones limpios bajo `C:/tmp/analista-task0164-v2/` |
| #4 config sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Reproduccion y gates

| Prueba | Resultado |
| --- | --- |
| `git clone` protocolo + checkout `232dcc3` | exit 0 |
| `git clone` Zeus + checkout `4faacd1` | exit 0 |
| Zeus `npm test` corrida 1 | exit 1, 56/57; fallo AC50 por `server did not become ready` aunque imprimio `listening on http://127.0.0.1:5060` |
| Zeus `npm test` corrida 2 | exit 0, 57/57 |
| `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` | exit 0, 8/8 |
| `python examples/intent_tx_cases/run_intent_tx_cases.py` | exit 0, 9/9 |
| `python scripts/validate_collaboration_state.py` en clon limpio | exit 0 |
| `python scripts/validate_collaboration_state.py` en repo vivo con secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py --root .` | exit 0 |
| `python scripts/scan_encoding.py --root .` | exit 0 |
| Drift clon limpio | `has_drift=false`, `up_to_seq=1452` |
| Drift repo vivo antes de mi veredicto | `has_drift=false`, `up_to_seq=1473` |
| `validate_chain` clon limpio | valid true, 780 checked events |
| `validate_chain` repo vivo | valid true, 801 checked events |
| agent_signatures / anchor | valid true en ambos; `checked=0` por configuracion actual |
| #4 byte-identica | `protocol.config.json` mantiene sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Tabla vector por vector

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| Tail torn final, sin eventos posteriores | PASA | Fixture `tail_torn`: tras `truncate_torn_jsonl_tail`, queda solo la linea valida anterior; `repair.line=2`, `truncated_bytes=15`. |
| Tail torn final + dos writers concurrentes | PASA | Payload propio con dos `submit_intent.py --intents` concurrentes: returncodes `[0,0]`, un writer reporta `log_repair`, `event_count=5`, `validate_chain.valid=true`, `linear_prev_hash=true`, drift false, tareas `TASK-9400` y `TASK-9401` en `in_progress`. |
| Multiples torn al final | PASA con limite | Fixture `multiple_torn`: trunca al prefijo visible. No deja evento nuevo invisible; el limite es que todo lo posterior al primer torn desaparece. |
| Torn en medio + linea JSON valida despues | SLIPS | Fixture exacto: bytes iniciales `{\"id\":\"before\",\"seq\":1}\\n{\"id\":\"partial\"\\n{\"id\":\"after\",\"seq\":2}\\n`. Tras `truncate_torn_jsonl_tail`, el archivo queda solo con `before`; `valid_after_line_lost=true`. La linea `after` era JSON valida y fue descartada. |
| Garantia "trunca SOLO la ultima linea parcial" | SLIPS | La funcion no comprueba que la linea invalida sea la ultima linea no vacia; trunca desde el ultimo offset valido anterior al primer error y descarta todo el sufijo. |
| Garantia "no descarta eventos validos" | SLIPS | Cualquier linea JSON valida posterior a una linea rota se descarta sin fail-hard ni cuarentena. Esto cubre el caso de un evento valido que hubiera quedado detras de un torn por la version previa. |

## Payload minimo del slip

```python
from pathlib import Path
from runtime.eventlog import truncate_torn_jsonl_tail, read_jsonl_torn_safe

p = Path("middle_torn_valid_after.jsonl")
p.write_bytes(
    b'{"id":"before","seq":1}\\n'
    + b'{"id":"partial"\\n'
    + b'{"id":"after","seq":2}\\n'
)
before = read_jsonl_torn_safe(p)   # ["before"]
repair = truncate_torn_jsonl_tail(p)
after = p.read_text(encoding="utf-8")
assert '"id":"after"' in after      # falla: la linea valida posterior fue descartada
```

Salida observada:

```json
{
  "case": "middle_torn_valid_after_newline",
  "parsed_before_ids": ["before"],
  "repair": {"line": 2, "truncated_bytes": 39, "valid_bytes": 24},
  "parsed_after_ids": ["before"],
  "valid_after_line_lost": true
}
```

## Residuales declarados

- El caso de producto `npm test` tuvo una primera corrida roja por readiness de servidor en AC50 y una segunda corrida completa verde. No lo uso como bloqueo de TASK-0164 porque el foco de esta re-pasada es el runtime del protocolo, pero queda reportado por exit code.
- El reparo actual es valido para la cola parcial final ordinaria. El cambio requerido es acotar la reparacion: si la primera linea invalida no es la ultima linea no vacia, debe fallar duro o preservar/cuarentenar el sufijo antes de reportar exito; no debe descartar silenciosamente lineas JSON validas posteriores.

