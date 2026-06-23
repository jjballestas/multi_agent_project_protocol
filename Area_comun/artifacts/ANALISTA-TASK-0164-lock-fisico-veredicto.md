# ANALISTA TASK-0164 lock fisico - veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO. El lock fisico serializa correctamente escritores concurrentes normales: con 8 procesos en
paralelo no obtuve fork, la cadena quedo lineal y drift 0. Pero el vector pedido de kill/torn-write no queda
cubierto: si queda una linea JSON parcial al final de `runtime/state/events.jsonl`, el siguiente
`submit_intent` puede devolver `applied: true` y un `event.seq` nuevo, mientras `read_jsonl_torn_safe` sigue
leyendo solo el prefijo sano, el evento nuevo queda pegado a la cola rota e invisible, y la hot state no cambia.
`validate_chain` y `protocol_state_drift` permanecen verdes sobre el prefijo, por lo que el fallo queda
enmascarado.

RECOMENDACION DE CIERRE: CAMBIO-REQUERIDO.

## Ancla canonica

- Protocolo implementacion revisada: `745a678` (`coord(TASK-0164): deliver claim row lock implementation`).
- Protocolo HEAD de instruccion: `346dd00`.
- Producto Zeus revisado: `4faacd1` (`fix(intake): row-scope front claims`).
- Clones limpios: `C:/tmp/analista-task0164-protocol` y `C:/tmp/analista-task0164-zeus`.
- Hash #4 `protocol.config.json`: `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`
  en `745a678`, `346dd00` y `HEAD`.

## Reproduccion

| Prueba | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` | cambios ajenos preexistentes en `.claude/settings.json`, `personal/Analista/MEMORY.md` y `personal/Arquitecto/...`; no stageados |
| `python scripts/validate_collaboration_state.py` en repo vivo, con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py` en clon limpio protocolo `745a678`, sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py --root .` | exit 0 |
| `python scripts/scan_encoding.py --root .` | exit 0 |
| `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` en clon limpio | exit 0, 8/8 |
| `python examples/intent_tx_cases/run_intent_tx_cases.py` en clon limpio | exit 0, 8/8 |
| `npm test` en clon limpio Zeus `4faacd1` | exit 0, 57/57 |
| Chain vivo antes del veredicto | `validate_chain.valid=true`, `agent_signatures.valid=true`, `anchor.valid=true`, drift 0, `up_to_seq=1435` |

## Tabla vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| AC-A claims por filas distintas | PASA | Golden `claims_distinct_rows_ok` exit 0; dos scopes `CLAIMS.json#A` y `CLAIMS.json#B` no solapan. |
| AC-A misma fila rechazada | PASA | Golden `claims_same_row_conflict` exit 0; dos scopes sobre el mismo selector se rechazan. |
| AC-B compat bare-vs-row | PASA | Golden `claims_bare_vs_row_conflict` exit 0; bare `CLAIMS.json` sigue cubriendo cualquier fila y bloquea el selector. |
| AC-C concurrencia normal N>2 | PASA | Payload propio con 8 procesos `submit_intent.py --intents` simultaneos sobre 8 tareas/claims distintos: returncodes 0/0/0/0/0/0/0/0, 17 eventos esperados y leidos, `validate_chain.valid=true`, enlaces `prev_hash` lineales, drift 0, todas las tareas `in_progress`. |
| AC-C intento de fork | PASA | En la prueba N=8 no aparece fork: cada evento leido cumple `current.prev_hash == compute_event_prev_hash(current, previous.prev_hash)`. |
| AC-C kill/torn-write | SLIPS | Inyecte una cola parcial `{\"seq\":999` al final de `events.jsonl` y luego ejecute `submit_intent` de `task_status`. Resultado: la llamada devolvio exito con `event_seq=2`, pero `read_jsonl_torn_safe` siguio leyendo solo 1 evento; el nuevo evento quedo no parseable detras de la cola rota, `TASK_INDEX` siguio `in_progress`, y `validate_chain.valid=true`/drift 0 quedaron verdes sobre el prefijo. |
| AC-D #4 byte-identica | PASA | `protocol.config.json` conserva hash `2e35f26e...` entre `745a678`, `346dd00` y `HEAD`; no toque genesis, registry ni keys. |
| Neutralidad de dominio | PASA | `scan_domain_neutrality.py --root .` exit 0. |

## Detalle del slip

Secuencia minima:

1. Partir de un fixture con genesis y hot state sin drift.
2. Anadir bytes parciales al final de `runtime/state/events.jsonl`: `{"seq":999`.
3. Ejecutar un `submit_intent` valido.

Observado:

```text
before_readable=1
submit_intent return=success
event_seq=2
after_readable=1
TASK_INDEX.status=in_progress
validate_chain.valid=true
protocol_state_drift.has_drift=false
```

Interpretacion: el lock evita interleaving entre procesos vivos, pero no recupera ni trunca una cola rota antes de
append. Como `atomic_append_jsonl` abre en append y escribe despues de la cola parcial, el evento siguiente queda
concatenado a una linea invalida. El lector tolerante corta antes de esa linea; los gates verifican el prefijo y no
detectan que una llamada reportada como aplicada no fue materializada.

## Residuales declarados

- No demostre un fork bajo concurrencia normal; el lock funciona para escritores vivos.
- El hallazgo es recuperacion ante muerte a media escritura o tail corrupto, no un bypass de claims por fila.
- La solucion deberia ser falsable: bajo lock, antes de calcular head, detectar/truncar cola JSON parcial o fallar
  duro antes de reportar `applied:true`; despues de eso, repetir el payload torn-write debe terminar en rechazo
  explicito o en append legible con drift 0 real.
