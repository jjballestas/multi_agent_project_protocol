---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0414-r5-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0414
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CERRABLE sobre 123fab06 -- SLIP-A cerrado en la PUERTA con control historico (la CLI de drift pasa de 0 a 1 con la misma mutacion en el mismo arbol), y el maker se declaro bien: 4/5 antes, 5/5 despues. Su sexta es ALCANZABLE y la cadena no la impide.
requested_action: Cierre TASK-0414 (in_review -> done) sobre 123fab06. Y al abrir r6, dos cosas son suyas - (1) abrala con la variante de COLA, no la de media cadena: quitar el ancla cuando es el ultimo evento deja la cadena VALIDA (medido sobre la cadena real) y ninguna puerta lo ve, mientras que a media cadena la caza el detector de huecos y r6 saldria verde por una propiedad temporal; (2) lleve a r6 el residuo R1 (ningun caso del runner ejercita las puertas extremo a extremo), no una sexta vuelta de esta tarea.
question: Al abrir r6, quiere que la trate como agujero de DISCRIMINANTE (lo que medi: validate_chain y el guardia del registro salen verdes con el ancla de cola quitada) o exige antes la reproduccion extremo a extremo, que obliga a revertir el arbol a seq 9763 y re-materializar el estado caliente -- la unica pieza que declaro no medida?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0414-r5-el-registro-ausente-que-ya-muerde-verdict.md
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r5.md
  - Area_comun/artifacts/Analista-TASK-0414-r4c-el-ancla-que-se-desvanece-verdict.md
  - runtime/eventlog.py
  - runtime/protocol_replay.py
deadline_or_blocking_level: high
---

# Veredicto TASK-0414 r5 -- OK-CERRABLE

Ancla: commit de producto `123fab06`, control historico `123fab06^` (`dbb9294f`), HEAD del protocolo
`3bb82158`. Cuatro clones limpios (`git clone -s -n`) en `D:/Aegis_Scratch/protocol/an0414r5/`. Nada
corrido en el arbol caliente. Cadena medida: 9162 eventos, cabeza seq 9833, un unico
`event_auth.registry_anchor` en seq 9764, cero eventos `chain.anchor`.

## Su pregunta, primero: es alcanzable, y la cadena no lo impide

**Si.** Con el ancla a media cadena (el log de hoy) borro el ancla, borro el registro y
re-sincronizo: el guardia devuelve `registry_absent / valid True` --el control apagado-- y
**`protocol_replay.py --check-drift` sale en EXIT 0 verdict=CLEAN teniendo delante un hueco de seq**.
`protocol_state_drift` no llama a `validate_chain` en ningun punto. Ahi hoy le salva el detector de
huecos de `validate_collaboration_state.py` (EXIT 1, `gap at seq 9765`).

**Pero el detector de huecos solo tiene algo que ver porque hoy hay 69 eventos detras del ancla.** En
el instante en que un ancla se escribe, el ancla ES la cola -- y lo fue durante todo r4c. Medido sobre
el prefijo genuino de la cadena real hasta seq 9764, cuyos `prev_hash` son los de produccion:

    validate_chain(prefijo)                  -> valid True  'chain valid'
    validate_chain(prefijo menos la cola)    -> valid True  'chain valid', 9091 eventos   <- SIN hueco
    guardia del registro, registro borrado   -> {'valid': True, 'reason': 'registry_absent'}

Quitar la cola no rompe ningun `prev_hash`: cada evento encadena hacia atras y nadie encadena hacia el
que ya no esta. El genesis pineado ata el PRINCIPIO de la cadena; no hay nada que ate el FINAL. Y no
hay pin externo que lo compense: cero eventos `chain.anchor`, luego `validate_eventlog_anchors` es hoy
una puerta vacua (`checked=0`).

No la meti en esta tarea, como pidio. Lo que no medi y r6 debe medir: la variante de cola **extremo a
extremo** (exige revertir el arbol a seq 9763 y re-materializar el estado caliente; es una mutacion
distinta de la que se ataca).

## Lo que acredita el arreglo

Su autodeclaracion es correcta, y la verifique por comportamiento con mis propias cargas, no con el
runner del maker: **OLD 4/5, NEW 5/5**, y el unico caso que cambia es `registry_deleted`
(`registry_absent` -> `registry_missing`). En 2x2 de runner: tests viejos x codigo viejo = 0, tests
nuevos x codigo viejo = **1, muriendo en la linea 237** (`assert missing_registry["valid"] is False`),
tests nuevos x codigo nuevo = 0 en dos corridas con stdout byte-identico.

Y en la PUERTA, con el vector de r4c (borrar el registro + `rebuild_snapshot`) sobre la cadena real,
misma mutacion en los dos arboles:

    --check-drift        123fab06^ -> EXIT 0 CLEAN        123fab06 -> EXIT 1 DRIFT path=EVENT_AUTH_KEY_REGISTRY.json

**Correccion que le importa antes de que la cite mal:** el validador canonico NO discrimina aqui. Sale
en 1 en las dos versiones, y en `123fab06^` sale en 1 por un motivo ajeno a este arreglo (`snapshot
mismatch: state hash differs`). Sobre la cadena de hoy `rebuild_snapshot` ya no re-sincroniza del todo,
asi que el escape de r4c --que en su dia daba 0 en las DOS puertas-- hoy solo se reproduce en la CLI de
drift. La discriminacion medida es real y esta en esa CLI.

## Residuos declarados (ninguno bloquea)

- **R1** El caso `registry_deleted_resynced_snapshot` **no re-sincroniza ningun snapshot**: hace
  `unlink()` y llama a la funcion pura. Ninguno de los cinco casos nuevos toca puerta alguna, y el
  escape de r4c era precisamente un verde extremo a extremo. El fin a fin lo medi yo y sale bien; la
  evidencia del repositorio no lo demuestra. Deberia viajar con r6.
- **R2** `if not actual: return registry_missing` (doce lineas mas abajo) quedo **inalcanzable**:
  imagen especular del defecto de r4c. Inofensivo, y trampa para el proximo lector.
- **R3** `seq` se devuelve en crudo (`None` posible; `int()` lanza con un seq no numerico).
  Preexistente y **falla cerrado**. Cosmetico.
- **R4** `--check-drift` no ejercita la cadena en absoluto. No es defecto de esta entrega; es el
  terreno de r6.

## Puertas, por exit code, en clon limpio de 123fab06

    validate_collaboration_state.py    0     OK: collaboration state is valid.
    protocol_replay --check-drift      0     verdict=CLEAN up_to_seq=9833
    scan_encoding.py                   0
    scan_domain_neutrality.py          0
    run_replay_secret_independent_cases.py   0 / 0   (dos corridas, stdout byte-identico)

Alcance de producto declarado respetado. No corri `npm test` ni el job entero.

Detalle completo, tablas y reproduccion:
`Area_comun/artifacts/Analista-TASK-0414-r5-el-registro-ausente-que-ya-muerde-verdict.md`.

-- Analista, 2026-08-18 00:56 local (UTC+2)
