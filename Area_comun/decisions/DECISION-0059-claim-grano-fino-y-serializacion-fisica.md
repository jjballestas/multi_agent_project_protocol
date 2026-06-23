# DECISION-0059 - Claims de grano fino (por-fila) + serializacion fisica del event-log

- **Estado:** accepted (ratificada por el operador 2026-06-23; cambia comportamiento del nucleo bajo #4, lock fisico).
- **Fecha:** 2026-06-23
- **Autor:** Arquitecto. **Maker propuesto:** Codex. **Checker:** Arquitecto + pasada Analista (foco concurrencia/#4).
- **Relacionada:** DECISION-0020 (anti-colision), DECISION-0022 (runtime-authoritative), AC72/SPEC-0086 (mensaje canal-ocupado).

## Problema

El front (operador) y los agentes (Codex/Analista) son ambos escritores del ledger. Todo `claim acquire` reserva el
ARCHIVO ENTERO `Area_comun/state/CLAIMS.json` (y muchos claims tambien listan `runtime/state/events.jsonl` /
`snapshot.json`). Como el chequeo de solape (`validate_scope_authority`, submit_intent.py ~610) rechaza dos claims
activos que solapen una ruta, **mientras un agente tiene un claim activo (a veces 15 min, mid-implementacion) el
operador no puede escribir** (aprobar una candidata, enviar un requisito): "claim acquire overlaps active claim ...
CLAIMS.json / CLAIMS.json". `TASK_INDEX`/`PROJECT_STATE` YA son por-fila (`ROW_SCOPED_LEDGER_PATHS`), por eso tareas
distintas no chocan; el cuello es CLAIMS.json (archivo entero) y los paths fisicos del runtime listados en scope.

## Decision

1. **Claims por-fila (logico).** Agregar `Area_comun/state/CLAIMS.json` a `ROW_SCOPED_LEDGER_PATHS`. Un `claim
   acquire` reserva su PROPIA fila `Area_comun/state/CLAIMS.json#<claim-id>` (no el archivo entero). Dos claims con
   claim-id distinto NO solapan (la logica de selector de `scope_covers` ya lo soporta: ~123-127). El
   `required_scopes` del kind claim (submit_intent.py ~565) pasa de `["CLAIMS.json"]` a
   `["CLAIMS.json#<claim-id>"]`. Los demas recursos siguen por-fila (`TASK_INDEX.json#<task>`,
   `PROJECT_STATE.json#active_tasks/<task>`) + ficheros concretos (task .md, SPEC, MSG mailbox file-scoped).
2. **Quitar los paths FISICOS del runtime de los claim-scopes.** Los claims NO listan `runtime/state/events.jsonl`
   ni `runtime/state/snapshot.json` (no son recursos logicos addressables; son materializacion del runtime). La
   serializacion de esos archivos la garantiza el lock fisico (punto 3), no el claim.
3. **Serializacion FISICA del append al event-log (clave para #4).** Al hacer los claims finos se elimina la
   serializacion logica de-archivo-entero que hoy impide appends concurrentes. Para no bifurcar la cadena #4
   (dos escritores con el mismo `prev_hash`), `submit_intent` toma un LOCK de archivo (OS, p.ej. en
   `runtime/state/.ledger.lock`) alrededor de la seccion critica (leer-head -> validar -> append -> materializar);
   tras adquirir el lock RE-LEE el head actual (por si otro escritor avanzo). Asi escritores concurrentes se
   serializan FISICAMENTE por milisegundos (no por los minutos del claim logico) y la cadena/firmas/anclaje #4
   quedan intactos. (Alternativa equivalente: CAS optimista sobre el head con reintento; el lock es mas simple.)

## Garantias / limites

- **DECISION-0020 preservada en espiritu:** la anti-colision sigue (no hay dos escritores corrompiendo el MISMO
  recurso). Solo se afina el grano: contencion LOGICA por-recurso (claim-id/tarea) + serializacion FISICA por lock,
  en vez de bloqueo de-archivo-entero. El operador deja de bloquearse por un agente que trabaja en OTRA cosa.
- **#4 byte-identica:** NO se toca `protocol.config.json` (la lista esta en codigo, no en config), ni el genesis, ni
  el agent_registry/keys. La semantica de la cadena (prev_hash, firmas, anclaje) no cambia; el lock solo ORDENA los
  appends concurrentes. Sin re-genesis.
- **Compatibilidad hacia atras:** un scope de-archivo-entero sin selector sigue cubriendo todo (no rompe claims
  viejos; solo sobre-reservan). Los claims nuevos usan el selector.
- **Neutralidad de dominio:** cambio 100% en el nucleo neutral (submit_intent.py + un lock); cero terminos de dominio.
- **Mensaje canal-ocupado (AC72) se mantiene:** en la ventana fisica (lock) o si aun hay contencion logica real, el
  front sigue mostrando "Canal ocupado, intente mas tarde"; con grano fino esa ventana se vuelve rara y breve.

## Riesgo y verificacion

- Riesgo central: CONCURRENCIA bajo #4. Mitigacion: el lock fisico + re-lectura de head garantiza un solo append a
  la vez (cadena consistente). PASADA ADVERSARIAL DEL ANALISTA obligatoria con prueba de DOS escritores concurrentes
  (front + agente) -> ambos progresan, cadena #4 valida (validate_chain/firmas/anclaje verdes), drift 0, sin fork.
- Gates: `validate` con/sin secretos exit 0 en clon limpio; neutralidad+encoding 0; #4 byte-identica; sin regresion
  de los goldens de submit_intent/claims.

## Plan

SPEC + TASK (maker=Codex / checker=Arquitecto + Analista). Off-by-default no aplica (es comportamiento del nucleo);
se entrega con la prueba de concurrencia verde antes de cerrar. Tras esto, el operador opera el front sin bloquearse
por los agentes de fondo.
