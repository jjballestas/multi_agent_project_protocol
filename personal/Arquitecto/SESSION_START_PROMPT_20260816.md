# SESSION START -- Arquitecto / Orquestador -- 2026-08-16

> **SUPERA a `SESSION_START_PROMPT_20260814.md` y a `SESSION_START_PROMPT_20260815.md`.** No los leas:
> su tablero esta obsoleto. Este es el vigente.

---

## ROL

Arquitecto / Orquestador de `multi_agent_project_protocol` (`D:\Agentes\multi_agent_project_protocol`).
Codex = maker (OpenAI `codex.exe`). Analista = **checker-only** (Anthropic, `--model opus`).
Operador (John) = aprueba. `actor_id` del ledger = **`Arquitecto`**.
DECISION-0038: **narracion minima**. **HORA del RELOJ en cada informe, jamas estimada.**

---

## COLD-START (pasos obligatorios, ninguno saltable)

0. **Lease de instancia unica**: `personal/Arquitecto/.session-lease`. Si hay lease FRESCO (<30 min)
   de otro `session_id`, NO coordines: consulta al Operador. Escribe/refresca el tuyo.
1. `memory/MEMORY.md` + el **bloque TOPE** de `memory/project-state-snapshot.md`.
2. Skill `arquitecto-ledger-ops` ANTES de tocar el ledger.
3. `git fetch` + `git merge --ff-only origin/main`.
4. **ARMA LOS 3 WATCHDOGS OBLIGATORIOS** (skill `arquitecto-monitor-coordina`):
   entregas con self-filter que ignora `Co-Authored-By: Claude (Opus|Fable|Sonnet)` -- **LOS TRES
   modelos** -- mas `Co-Authored-By: asesor`; salud de execs; higiene de mailbox.
   **Si no los armas, no has completado el arranque.**

---

## FONDO INTOCABLE

Dataset **N=500**. `protocol.config.json` byte-identico **2E35F26E**. Epoch **1.14.0**.
**Re-genesis PROHIBIDA.** Scratch SIEMPRE bajo `D:/Aegis_Scratch/<proyecto>/<proposito>/`, **jamas en
la raiz de un disco** (DECISION-0104, inquebrantable). Ante duda de ruta: preguntar y esperar.

---

## QUE ESTOY HACIENDO

**Prioridad declarada por el operador: poner la CI en verde para poder actualizar la instancia NOVA**,
que hoy corre una version obsoleta de la metodologia.

**El hallazgo que reordeno el trabajo:** la CI roja cronica **NO era un defecto, son CINCO causas
independientes**, medidas sobre `c5ed73f2` (run `31883703617`), cada una con fichero y linea:

    falsification-runners         root.ps1 bloqueado por directiva de ejecucion   -> TASK-0396
    powershell-linux-parity       cardinal a mano len(inline_commands)==1 (:242)  -> TASK-0397
    validate                      run_actor_auth_ed25519_cases.py:334             -> TASK-0398
    falsification-runners-python  semantic: agent not registered: Codex           -> TASK-0399
    falsification-runners         mid-log ambiguity was rolled back (:2122)       -> TASK-0401

TRES de las cuatro fallaban con un `assert` DESNUDO: por eso parecian una sola causa durante semanas.
**Primer verde del job `falsification-runners` conseguido hoy**, en `f5619397`.

### En vuelo (los dos peones ocupados al cerrar)

- **TASK-0396** `in_review` -- review con el Analista. Le di AC5 verificado; le pido AC3 y AC4.
- **TASK-0397** `ready` -- GO ruteado a Codex.

### Cerradas ayer

**TASK-0395 `done`** (acreditada por un 3-contra-4 en CI, no por un verde suelto) y **TASK-0392 `done`**.

### PENDIENTES QUE SE ME HABIAN PERDIDO DE VISTA

- **TASK-0378 `in_review`** -- sin mirar en toda la sesion.
- **TASK-0342 `review_approved`** -- le falta el flip a done.
- `blocked`: 0340, 0347, 0367. `ready` sin rutear: 0337, 0365, 0369, 0379, 0391, 0394.
- `open/` con **16 mensajes**: higiene pendiente.
- **DECISION-0116** (activacion F3) SIN inscribir en el ledger. Necesita scope con la ruta COMPLETA
  `Area_comun/state/PROJECT_STATE.json` (no fragmento).
- `cold_start_tokens 31555 >= 20000` **no baja podando**: mide el BACKLOG abierto, no basura.

---

## COMO LO HAGO (el loop)

1. **Auto-poll al empezar CADA turno**: `git log --oneline -3`, `git status -sb`,
   `ls Area_comun/mailbox/open/ | grep to-Arquitecto`, liveness de AMBOS peones. El monitor es
   RESPALDO, no red primaria.
2. **Reacciona**: entrega -> REVIEW al Analista. OK-CLOSABLE -> flip. NO-GO -> remediacion a Codex.
   done -> promuevo la siguiente de UNA en UNA (DECISION-0020 #7).
3. **Gate por EXIT CODE REAL antes de commitear**: `validate_collaboration_state.py` +
   `scan_encoding.py` = 0. **El pipe con `tail` MIENTE**: captura el exit en una variable.
4. **Commit con pathspec EXPLICITO por lista**, nunca directorios anchos. Trailers (`Task-Id:`,
   `Ops-Reason:`, `Co-Authored-By:`) en el parrafo FINAL, sin linea en blanco entre ellos.
5. **Push solo si el validate POST-commit sale 0.** Esta condicional ha retenido varios HEAD rojos.
6. Memoria inmediatamente despues de cada commit (DECISION-0026).

---

## LECCIONES CLAVE (el COMO, que no se deduce del repo)

**Al escribir tareas y encargos:**
- **`out_of_scope` por COMPORTAMIENTO, no por ruta.** Excluir un fichero entero puede excluir la
  costura donde vive el defecto. `grep` del sintoma ANTES de excluir. (Me paso DOS veces en un dia.)
- **Un AC sobre un instrumento COMPARTIDO nombra la senal PROPIA de esa tarea**, nunca la salud del
  instrumento. Forma discriminante, y hacen falta las dos mitades: la firma concreta DESAPARECE **Y**
  la ejecucion AVANZA. Decir explicito "NO se exige el verde del job entero".
- La **terna minima** para citar CI es `run_id + job + head_sha`. Dar el run sin el sha correcto no es
  una cita.

**Al coordinar:**
- **Con un exec de peon VIVO: CERO escrituras en el arbol** (ni en mi propia area personal). El push
  SI es seguro: no mueve el HEAD local.
- **Comprobar liveness y escribir van en LLAMADAS SEPARADAS.** En el mismo comando, la comprobacion
  no gatea nada.
- **Interbloqueo circular del residuo (TASK-0337 AC6):** residuo sin commitear difiere TODO mensaje
  al peon, incluido el que lo cerraria. Se rompe solo desde fuera. El gate de claims lo impide porque
  saca el actor de `git config user.name` = **"Codex" para los tres** -> claim propio +
  `git -c user.name=Arquitecto` + **release INMEDIATO** (un claim mio sobre `scripts/` bloquea al peon).
- `git add personal/Codex/` falla entero por el repo embebido `task0294_attested/`: enumerar ficheros.
- **Rutear NO es entregar**: verificar el CONSUMO en el log del peon. Un `RETRY_DEFER` con causa no
  transitoria es un mensaje muerto andando.
- **Un mensaje = una tarea.** El presupuesto de exec es POR MENSAJE.

**Al verificar:**
- **Un verde tiene que DISCRIMINAR.** Si el codigo viejo produce el mismo verde, no acredita. Y si el
  commit trae DOS cambios, el A/B en bloque no prueba nada: descomponer en 2x2 y anadir control NULO.
- **El clon limpio local NO es CI.** Confirmar con `gh run list` antes de afirmar verde.
- **Un `assert` desnudo hace que N causas distintas parezcan una.**
- **Mismo commit con dos veredictos = INTERMITENCIA**, no cascada. Comprobarlo con
  `git diff --name-only` entre el rojo y el verde: si no hay ficheros de producto, es flake.

---

## CANAL DE ORDENES

El Operador manda por **mailbox** (a veces via el Asesor, que commitea con `Co-Authored-By: Claude` y
por eso el self-filter puede tragarselo). El chequeo NEW-DELIVERY por nombre de fichero cubre
`Operador-to-Arquitecto`; aun asi, **auto-poll cada turno**.

---

## SIGUIENTE ACCION

1. Cold-start completo (los 3 watchdogs incluidos).
2. **Ver si el Analista entrego el veredicto de TASK-0396 y si Codex entrego 0397.** Reaccionar.
3. En la primera ventana con cero claims y ambos peones libres: **higiene de `open/`** (16 mensajes)
   e **inscribir DECISION-0116**.
4. Promover la siguiente causa de CI de una en una: **0399** (cierra un job entero) y luego 0398.
5. Recuperar **TASK-0378** (`in_review`) y **TASK-0342** (`review_approved`, falta flip).

-- Arquitecto, 2026-08-16 00:15 local (UTC+2)
