# PROMPT DE ARRANQUE -- Arquitecto -- 2026-08-18

> **SUPERSEDE a `SESSION_START_PROMPT_20260817.md`**, que queda obsoleto (describe la saga 0414 en
> vuelo y una cola que ya no existe). No lo borres; ignoralo.

---

## ROL

**Arquitecto / Orquestador** de `multi_agent_project_protocol` (`D:\Agentes\multi_agent_project_protocol`).
Codex = maker. Analista = checker-only. Operador (John) = aprueba y **firma**. `actor_id` = `Arquitecto`.
DECISION-0038: **narracion minima**. **Hora del RELOJ en cada informe, jamas estimada.**
Canal de ordenes y reportes: **mailbox al Operador**, no chat.

---

## COLD-START (en orden, sin saltarte ninguno)

0. **Lease**: `personal/Arquitecto/.session-lease`. Lease FRESCO (<30 min) de otro `session_id` ->
   NO coordines, consulta al Operador.
1. **`memory/MEMORY.md`** + **`memory/project-state-snapshot.md`**, bloque **TOPE fechado**, que
   manda sobre este prompt si es mas nuevo.
2. **Skill `arquitecto-ledger-ops`** antes de tocar el ledger.
3. `git fetch` + `git merge --ff-only origin/main`.
4. **ARMA LOS WATCHDOGS. Si no los armas, NO has completado el arranque.**
   - **Entregas** (`persistent:true`): HEAD local + MSG `*-to-Arquitecto-*`. Self-filter por
     `%an != Arquitecto` **e** ignorando `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- **LOS TRES
     modelos** -- mas `Co-Authored-By: asesor` y subject `^checkpoint\(asesor\)`.
     **Commitea SIEMPRE con `git -c user.name=Arquitecto -c user.email=arquitecto@local.invalid`**:
     el `user.name` del repo es `Codex` y lo comparten los tres.
   - **Exec-health**: lock retenido + heartbeat `EXEC_RUNNING` congelado >300 s.
   - **Higiene**: `open/` >= 10.
   - **Encargo muerto**: `RETRY_EXHAUSTED` en **ventana de 60 lineas** (no la historia entera).
     **Y con la segunda condicion nueva: si existe el artefacto de entrega (commit del maker o
     handoff), NO es un encargo muerto** -- ver LECCIONES.
   - **Encargo que no arranca**: MSG a un peer >12 min en `open/` sin `EXEC_START` ni entrada en
     `seen.json`.

---

## FONDO INTOCABLE

Dataset **N=500**. `protocol.config.json` **byte-identico, sha8 `2E35F26E`**. Epoch **1.14.0**.
**Re-genesis PROHIBIDA.** Scratch solo bajo `D:/Aegis_Scratch/<proyecto>/`.

**Y esta medido, no supuesto:** el genesis real es `seq 672`, `prev_hash 649d99e6...`, y coincide
exactamente con `canonical_hash(config)`. **Cualquier** clave nueva en el config produce
`genesis mismatch` sobre la cadena entera. Lo verifique tres veces esta sesion.

---

## QUE ESTOY HACIENDO

**v1.19.1 PUBLICADA** (tag `27acf137`) **y NOVA DESBLOQUEADA**, adoptando. La saga **TASK-0414
cerrada** tras cinco rondas. **0378 y 0394 tambien `done`.**

### LO PRIMERO: dos decisiones FIRMADAS y SIN INSCRIBIR

El operador firmo en persona **DECISION-0120** y **DECISION-0121**. Los `.md` estan en
`Area_comun/decisions/` con `status: accepted`, y el cambio normativo de la 0120 ya esta aplicado.
**Falta el intent `decision` en el ledger.** Fallo con:

    ERROR: claim acquire overlaps active claim CLAIM-20260818-Codex-TASK-0410:
      Area_comun/state/PROJECT_STATE.json / PROJECT_STATE.json#active_tasks/TASK-0410

El intent `decision` **exige `PROJECT_STATE.json` ruta COMPLETA**, y eso solapa con cualquier
fragmento de un peon. **Reintenta `.protocol-tmp/tx-dec.json`** en cuanto Codex suelte el claim.
`validate` esta en 0 con los `.md` presentes, asi que no urge -- pero no esta cerrado.

**Sin commitear (mio):** `TASK_PROTOCOL.md`, las dos decisiones, 3 skills.
**NO commitees el estado de Codex** (CLAIMS/TASK_INDEX/PROJECT_STATE): esta en 0410.

### En vuelo

    0397  in_progress  r2 ruteada -- SOLO el AC4 (censo 76/353/12 -> 75/351/12)
    0408  in_progress  r1 entregada, falta veredicto INDEPENDIENTE registrado
    0410  in_progress  GO con DOS ampliaciones dentro (E6 y RES-3)
    0342  review_approved -- solo el flip, lo ejecuta CODEX
    nuevas 0415 0416 0417 0418 0419

---

## COMO LO HAGO (el loop)

1. **Auto-poll cada turno**: `git log --oneline -3`, `open/ | grep to-Arquitecto`, liveness **por
   LOG, no por proceso**, y **`retry.json` de los dos peones** -- un `defer` no emite commits ni
   eventos, asi que los monitores ven el mismo silencio que "no hay trabajo".
2. **Ventana segura**: cero locks + cero claims. Con exec de peon vivo, **cero escrituras al arbol**.
3. **Gate por CONJUNCION**: `ASCII == 0 AND validate == 0 AND encoding == 0 AND neutralidad == 0`.
   El ASCII se mide **sobre el lote que vas a commitear** y **con `LC_ALL=C.UTF-8`** (ver LECCIONES).
4. **Orden: gate largo -> ledger -> commit -> mensaje.** Nunca dejes un MSG en `open/` esperando un
   gate de 4 minutos: el cron lo toma del disco y su exec te limpia el indice.
5. **Pathspec EXPLICITO derivado de `git status`, y va TAMBIEN en `git commit -- <rutas>`.** Verifica
   el residuo **despues** de commitear; `COMMIT=0` no garantiza que entrara todo.
6. **Validate y push en comandos SEPARADOS.**
7. **Higiene -> dejar de rutear -> podar -> volver a rutear** (ya es normativo, DECISION-0120).
8. Tras cada commit: **memoria** (DECISION-0026).

---

## LECCIONES CLAVE (el COMO que no se deduce del repo)

- **Un gate nuevo se estrena con su NEGATIVO.** Mi chequeo ASCII dio verde toda una noche porque con
  `LC_ALL=C` el `grep -P` **falla** y yo contaba el fallo como cero. **No silencies el stderr de un
  instrumento de medida**, y distingue "no encontro nada" de "no pudo buscar".
- **`TaskStop` NO mata el proceso de fondo.** Devuelve "Successfully stopped" y sigue vivo; verifica
  por PID y mata el ARBOL. Ojo: un filtro `-like "*script*"` **se cuenta a si mismo**.
- **`RETRY_EXHAUSTED` no significa encargo muerto.** Puede ser un encargo **cumplido y no marcado**:
  los reintentos encuentran el trabajo hecho y salen `transient`. Antes de reenviar, **busca el
  artefacto de entrega**. Me costo tres execs de peer.
- **El encargo que se esta MURIENDO no lo ve ningun monitor**: un `defer` no emite nada. Solo se ve
  leyendo `retry.json`. Dos colisiones en un dia, ambas cazadas por el canal antes que por mis vigias.
- **Desbloquearse de un claim ajeno: scope MINIMO Y EXACTO.** Quita de tu scope lo que no escribes de
  verdad, empezando por `CLAIMS.json`. **Pero incluye SIEMPRE tu propia fila
  `CLAIMS.json#<self>`** o el claim no admite release y queda vencido-y-activo (me paso seis veces).
- **El intent `decision` exige `PROJECT_STATE.json` ENTERO**, asi que choca con cualquier fragmento
  de un peon. Es TASK-0411 en su forma mas pura.
- **Un cardinal publicado se re-deriva o no se publica.** Y si mides en el arbol caliente, el numero
  no es re-derivable desde la entrega: eso hundio el AC4 de 0397, y **la causa fue un commit mio**.
- **Revision adversarial: lentes repartidas y el autor EXCLUIDO.** Tumbo mi propuesta, la del canal
  y mi propia enmienda en la misma ronda. Exige comando+salida por hallazgo.
- **No cambies el criterio despues del juicio.** Retener un cierre por documentacion cuando el efecto
  esta acreditado por mutacion es mover la frontera a toro pasado.

---

## CANAL DE ORDENES + PENDIENTES

Ordenes y reportes por **mailbox al Operador**. `open/` = 3.

**Defecto recurrente del canal, censado:** 7 de 19 mensajes del Operador llevan
`requires_response: true` **sin** `requested_action`. Cada uno pone el canonico ROJO; uno **puso CI
en rojo** y enmascaro el baseline. Pedido: que la plantilla lo incluya siempre.

**Cola del maker acordada:** `0410 (con E6 como AC) -> 0412 -> 0413 -> 0416 -> 0418`, y **0417
despues**. Olas por criterio declarado, no en masa.

**Prediccion falsable pendiente:** el proximo run completo de `validate` vuelve a **26/1/60 en el
paso 23**. Si no, hay rojo nuevo.

**Tablero derivado:** `D:/Aegis_Scratch/protocol/tablero/gen.py --backlog` ->
`https://claude.ai/code/artifact/a1c5f824-43c0-43fb-bed7-f34ce5a09343`. Se DERIVA del ledger; no se
tacha a mano. El operador quiere que sea **propiedad exportable** de la metodologia (sin registrar).

---

## SIGUIENTE ACCION

1. **Inscribir DECISION-0120 y 0121** en cuanto Codex suelte el claim de 0410
   (`.protocol-tmp/tx-dec.json`, idempotente).
2. **Commitear lo mio** con pathspec explicito: `TASK_PROTOCOL.md`, las dos decisiones, las skills.
   **Sin tocar el estado de Codex.**
3. Vigilar 0397 r2, 0408 (falta veredicto independiente) y 0410.
4. **El flip de 0342** sigue pendiente y lo ejecuta Codex.
