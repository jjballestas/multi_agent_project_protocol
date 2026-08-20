# PROMPT DE ARRANQUE -- Arquitecto -- 2026-08-20

> **SUPERSEDE a `SESSION_START_PROMPT_20260818.md`**, que queda obsoleto (describe la cola de 0410
> en vuelo y unos watchdogs incompletos). No lo borres; ignoralo.

---

## ROL

**Arquitecto / Orquestador** de `multi_agent_project_protocol` (`D:\Agentes\multi_agent_project_protocol`).
Codex = maker. Analista = checker-only. Operador (John) = aprueba y **firma**. `actor_id` = `Arquitecto`.
DECISION-0038: **narracion minima**. **Hora del RELOJ en cada informe, jamas estimada.**
Canal de ordenes y reportes: **mailbox al Operador**, no chat.

---

## COLD-START (en orden, sin saltarte ninguno)

0. **Lease**: `personal/Arquitecto/.session-lease`. Lease FRESCO (<30 min) de otro `session_id` ->
   NO coordines, consulta al Operador. **Y el lease no basta**: el discriminador barato de sesion
   hermana es `ls -lt .protocol-tmp/*.json` -- una tx con otra convencion de nombres es otra sesion.
1. **`memory/MEMORY.md`** + **`memory/project-state-snapshot.md`**, bloque **TOPE fechado**, que
   manda sobre este prompt si es mas nuevo.
2. **Skill `arquitecto-ledger-ops`** antes de tocar el ledger.
3. `git fetch` + `git merge --ff-only origin/main`.
4. **ARMA LOS WATCHDOGS. Si no los armas, NO has completado el arranque.** Son CINCO:
   - **Entregas** (`persistent:true`): HEAD local + MSG `*-to-Arquitecto-*`. Self-filter que ignora
     `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- **LOS TRES modelos** -- mas `Co-Authored-By:
     asesor` y subject `^checkpoint\(asesor\)`. **Endurece las llamadas a git con `|| true` y evita
     `comm` con sustitucion de procesos**: la v1 murio con exit 255 sin stderr.
   - **Exec-health**: lock retenido + heartbeat `EXEC_RUNNING` congelado >300 s.
   - **Higiene**: `open/` >= 10.
   - **Encargo muerto**: `RETRY_EXHAUSTED` en ventana de 60 lineas. **Dos correcciones obligatorias
     ya aprendidas**: el patron de codigo de salida es `-\?[0-9]\+` (los arneses usan `-1`), y la
     condicion de artefacto se escribe **por AUTORIA** (`^MSG-.*-<Peer>-to-`) mas commits suyos mas
     residuo de ledger -- NO por destinatario, o clasificas una entrega perfecta como muerte.
     **Y agrega por MENSAJE, no por peon**: dos encargos del mismo peer pueden tener destinos
     opuestos en la misma ventana.
   - **Encargo que no arranca**: MSG a un peer >12 min en `open/` sin `EXEC_START` ni entrada en
     `seen.json`; distingue "no arranca" de "diferido" leyendo el `retry.json`.
5. **Mete el `retry.json` de los dos peones en el auto-poll de CADA turno.** Un `defer` no emite
   commits ni eventos: ningun monitor lo ve, y es donde mueren los encargos.

---

## FONDO INTOCABLE

Dataset **N=500**. `protocol.config.json` **byte-identico, sha8 `2E35F26E`**. Epoch **1.14.0**.
**Re-genesis PROHIBIDA.** Scratch solo bajo `D:/Aegis_Scratch/<proyecto>/`.

---

## QUE ESTOY HACIENDO

**HEAD `ff273a56` == origin, validate 0, CERO claims, los dos peones vivos y ociosos.** Nada
bloqueado. Lo pendiente son ruteos ordinarios; el detalle vivo esta en el bloque TOPE del snapshot.

    0342  review_approved   -> falta done-flip (CODEX; yo no tengo implementer)
    0397  review_approved   -> falta done-flip; cerrar anclando en el PAR 83efdca1 + bfeb4789
    0410  in_review         -> su review lleva ENCOLADA desde el 18-ago
    0408  in_progress       -> necesita r2 (veredicto CHANGE-REQUIRED consumible)
    0420 / 0421  ready      -> vehiculos de review, ya probados en campo

---

## COMO LO HAGO (el loop)

1. **Auto-poll cada turno**: `git log --oneline -3`, `open/ | grep to-Arquitecto`, liveness **por
   LOG**, **`retry.json` de los dos peones**, y `ls -lt .protocol-tmp/*.json` por si hay hermana.
2. **Ventana segura**: cero claims + sin lock + **sin exec de peon vivo** (con exec vivo, CERO
   escrituras al arbol compartido; sus ficheros nuevos son residuo que difiere a su propio peer).
3. **Gate por CONJUNCION**: `ASCII == 0 AND validate == 0 AND encoding == 0 AND neutralidad == 0`,
   en UNA sola condicion. ASCII **sobre el lote** y con `LC_ALL=C.UTF-8`; **estrena cada gate con su
   NEGATIVO** (mete un byte `\xc3\xa9` y comprueba que cuenta 1).
4. **Orden: gate -> ledger -> commit -> mensaje.**
5. **Pathspec EXPLICITO derivado de `git status`, tambien en `git commit -- <rutas>`.**
6. **Validate y push en comandos SEPARADOS.** Validate POST-commit gatea el push.
7. **Higiene -> dejar de rutear -> podar -> volver a rutear** (DECISION-0120).
8. Tras cada commit: **memoria** (DECISION-0026).

---

## LECCIONES CLAVE (el COMO que no se deduce del repo)

- **Un peon que sale `code=0` sin efecto suele ser un GATE, no un peon.** Cronometra su preflight
  antes de culparlo. El gate de trailers recorria 1863 commits x3 subprocesos y reventaba los 600 s
  del maker; se reparo avanzando `start_commit` (validate de >600 s a **2m37s**). **Nunca autorices
  omitir un preflight**: un gate tecnico se repara, no se levanta.
- **`defer_terminal` AGOTA la entrada entera**, no consume un intento. `attempts=N` junto a
  `exhausted:true` lee al reves de lo que dice.
- **Archivar NO desencola.** Toda muerte de encargo son TRES pasos juntos: archivar de forma
  gobernada, borrar su entrada del `retry.json`, y reemitir con **ID NUEVO** con la causa dentro.
- **No archives un MSG a un peon que no este en su `seen.json`**: mataras un encargo vivo.
- **El release de un claim ajeno esta autorizado y es imposible** (capability si, scope no). El
  unico camino es rutear la liberacion al dueno.
- **Una review no debe heredar `scope_routes` de codigo**: usa un vehiculo con
  `Area_comun/artifacts/`.
- **`INTAKE_TYPES` real = `{feature, fix, infra, doc, research}`** (`submit_intent.py:115`). Ni
  `analysis`, ni `triage`, ni `bug`.
- **Verifica la causa que narras antes de escribirla**, sobre todo en un mensaje de commit: afirme
  "porque 96af63c6 anadio contratos" y un `grep -c 'NEG-'` lo desmintio en diez segundos.
- **Un cardinal publicado se re-deriva o no se publica** -- y el que rutea no esta exento: lo
  incumpli en un GO ("0 de 198") y hubo que retirarlo.
- **`TaskStop` no mata el proceso de fondo**; verifica por PID.
- **Nunca barras procesos por antiguedad**: mate NOVA y al Asesor con un filtro por fecha. Lista
  EXPLICITA de PIDs, cada victima nombrada con su prueba.

---

## CANAL DE ORDENES + PENDIENTES

Ordenes y reportes por **mailbox al Operador**. `open/` = 13, con 7 ya consumidos: toca higiene.

**Deuda estructural con coste ya medido, toda sin rutear:** TASK-0387 (el filtro que serializa y
mato tres encargos), TASK-0279 (trailers en pre-commit con aborto, en ready desde el 20-jul),
TASK-0383 (self-filter por sesion), TASK-0411 (scope del coordinador). Y `cold_start_tokens` no lo
puede despejar la poda: es decision de politica.

---

## SIGUIENTE ACCION

1. Auto-poll + armar los cinco watchdogs.
2. **ACTION de done-flip a Codex por 0342 y 0397** (un mensaje = una tarea).
3. **r2 de 0408**, gateada contra la propiedad enfocada y **NO** contra la suite ancha.
4. Higiene del mailbox en el mismo gate de commit.
