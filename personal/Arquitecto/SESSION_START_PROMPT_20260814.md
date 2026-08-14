# SESSION START PROMPT -- Arquitecto (2026-08-14)

> SUPERA a SESSION_START_PROMPT_20260812.md (no lo borres). Estado REAL verificado por medicion al
> cierre 2026-08-14 13:37 local (UTC+2).
>
> **Los crons quedaron VIVOS y sin marcador `.stop`.** Cero claims activos.

## ROL
Arquitecto / Orquestador de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Codex=maker/implementer, Analista=checker-only, operador(John)=aprueba. actor_id ledger="Arquitecto".
DECISION-0038 narracion minima. HORA local **leida del reloj, jamas estimada**, en cada informe.

## COLD-START (en orden; PASO 4 NO ES SALTABLE)
0. **Lease instancia-unica:** lee `personal/Arquitecto/.session-lease`; si hay lease FRESCO (<30min)
   de otro session_id -> NO coordinar, consultar al operador. Escribe/refresca el tuyo.
   **OJO (DECISION-0113 + TASK-0383):** el lease es DECLARATIVO. Una sesion hermana puede estar
   operando sin haberlo leido, y el self-filter de los monitores **no la distingue de ti** porque
   filtra por firma de MODELO. Si ves commits que no recuerdas, no asumas que son tuyos.
1. Lee `memory/MEMORY.md` + `memory/project-state-snapshot.md` (bloque TOPE).
2. Dispara la skill `arquitecto-ledger-ops` ANTES de cualquier escritura al ledger.
3. `git fetch` + `git merge --ff-only origin/main`. Verifica HEAD==origin.
4. **ARMA LOS 3 WATCHDOGS OBLIGATORIOS (skill `arquitecto-monitor-coordina`): (a) monitor de entregas
   HEAD-local con self-filter Opus|Fable|Sonnet + asesor; (b) watchdog exec-health **por HEARTBEAT
   `EXEC_RUNNING` del log del CRON**, nunca por mtime del `err.log` (en text-mode queda a 0 bytes y
   falso-positivea); (c) watchdog de higiene. SI NO LOS ARMAS, NO HAS COMPLETADO EL ARRANQUE.**
   Usa el monitor de entregas **persistente**: el de un disparo muere al notificar y el de 1h expira;
   con los dos huecos ciegos de esta semana (4h y 7h) eso no vuelve a pasar.
5. **Crons VIVOS al cerrar.** Verifica liveness real. Si murieron:
   `powershell -NoProfile -File personal/<Peer>/<peer>_mailbox_cron.ps1` (run_in_background), y **lee
   su log en la primera ronda** -- un `RETRY_DEFER` con causa no transitoria es un mensaje muerto
   andando. Si el Analista no resuelve su binario, arranca con `-AgentExe claude` (rodeo de runtime
   mientras TASK-0367 cierra).
6. **Runners propios** (DECISION-0112): `gh api repos/jjballestas/multi_agent_project_protocol/actions/runners`
   -> `protocol-win` y `protocol-linux` `online`. Si Linux falta, relanza `wsl -d Ubuntu -- sleep infinity`.

## FONDO INTOCABLE
`protocol.config.json` sha8 **2E35F26E** (verificado hoy), epoch **1.14.0** PINEADO, dataset **N=500**.
Re-genesis PROHIBIDO.

## QUE ESTOY HACIENDO

**Objetivo del operador: TERMINAR LA MEMORIA HIBRIDA.** F3 tiene **pre-aprobacion** para su DECISION
de activacion, que se emite cuando F2 este acreditada.

**1. TASK-0368 -- la PUERTA de F3. EL CHECKER AGOTO SU LAZO Y ESCALO AL OPERADOR (13:42).**
Su veredicto de r4: CHANGE-REQUIRED, pero con dos precisiones que cambian el cuadro.
- **Mi rojo era drift trivial** (arbol-contra-blob), como yo mismo declare que podia ser. Hice bien en
  no presentarlo como prueba.
- **r4 cierra bien lo que se le pidio.** Lo que queda es OTRA entrada: una decision con
  `superseded_by` **y sin `status`** se clasifica VIGENTE con las SEIS puertas verdes -- y eso lo
  **introdujo r2**, no r4.

**LA ELECCION ES DEL OPERADOR, no de la cadena de remediacion.** El checker agoto sus dos iteraciones
y yo la mia. Opciones, con su recomendacion tecnica en (a):
- **(a)** tercera iteracion acotada a UNA propiedad -- que `decision_policy_state` siga evaluando
  `superseded_by` cuando `status` es `None` -- con la prueba ya escrita en la seccion 3.2 de su
  veredicto.
- **(b)** cerrar TASK-0368 con el hallazgo enrutado como tarea propia y declarado en el cierre.

**NO ratifiques el done-flip sin esa decision del operador.**

**2. TASK-0378 (`ready`) es lo siguiente para Codex.** Acuerdo explicito del operador: *"espera a que
Codex termine y luego aplicas el nuevo requerimiento"*. Detras, 0379.

**3. TASK-0373 (F2, `ready`) sin rutear a proposito** -- no abrir un segundo frente con la puerta en
juicio. Es la mitad de la memoria hibrida que NO existe: `cold_packs`, `stubs` y `hot_cold_rules`
siguen a **cero** y no hay `Area_comun/archive/`.

**4. TASK-0367 (`in_progress`) es la deuda mas antigua**: su remediacion r2 lleva mas de un dia en
`open/` sin procesar.

## COMO LO HAGO (rieles, con lo aprendido esta semana)
- Ledger: TODA transicion por `submit_intent --actor-id Arquitecto`. Claim acquire ANIDADO con scope
  (incluida su fila `CLAIMS.json#<claim_id>`); release PLANO.
- **`idempotency_key` EXPLICITA por intent, siempre.** La derivada sale del CONTENIDO, asi que en un
  bucle de remediacion colisiona desde la 2a vuelta y el error habla de "partial transaction
  idempotency state" -- que suena a drift y no lo es (TASK-0382).
- **VALIDATE Y PUSH EN COMANDOS SEPARADOS.** Encadenarlos hace el validate decorativo: el push sale
  aunque de rojo. Me paso el 12-ago a las 22:37.
- **El pathspec se deriva de `git status`, no de lo que movio el ledger.** `git add` falla ENTERO si
  UNA ruta no existe; un fichero del peer archivado estando untracked no tiene ruta en `open/`.
- **Commit con pathspec por lista explicita**, nunca `git add -A`. Trailers en el parrafo FINAL sin
  linea en blanco. Subject `fix(`/`revert(`/`hotfix(` exige `Fixes-Task:`.
- **GATE REPRODUCIBLE (DECISION-0115):** un gate acredita si REPITE. Dos corridas sobre el mismo
  commit, o el arnes se declara no idempotente y se EXCLUYE. Al citar un verde, di cuantas corridas.
- **ASCII puro** en `Area_comun/`: barrido de bytes >127 antes de commitear (me mordio 2 veces hoy).
- **`scan_encoding` da FALSO ROJO transitorio** mientras `submit_intent` tiene el `.ledger.lock`.
- **No tocar historia con el exec del peer VIVO**: su `--amend` reescribe el HEAD de AHORA y puede
  comerse tu commit. Rescata el mensaje del reflog y repara con el arbol quieto.
- Mutaciones y clones de prueba: **bajo `D:/Aegis_Scratch/protocol/`**, y borrar al terminar.

## LECCIONES CLAVE (el COMO durable)
- **Una senal que no puede enrojecer ninguna puerta no es una senal, es una linea de log.** Es el hilo
  de las cuatro vueltas de 0368.
- **Un negativo puede ser una TAUTOLOGIA con forma de frontera**: comparar 16 elementos de una
  poblacion contra 21 de otra se cumple para cualquier implementacion.
- **Ante "sigue rojo pero es de TASK-XXXX": ABRE la XXXX.** Puede devolvertelo por nombre y entonces
  el rojo no es de nadie.
- **Un AC que pide el caso ENTERO verde mientras el `out_of_scope` excluye causas es CONTRADICTORIO.**
  Enmiendalo con fecha visible, jamas en silencio.
- **Neutralizar una FORMA sin comprobar que nombra la PROPIEDAD**: `claude` era un binario del PATH,
  no un participante. Y la ASIMETRIA (rompio a un peon y no al otro) lo hizo invisible.
- **Mecanismo probado != camino probado** (DECISION-0115): un doble admite el primero; solo el
  contrato real cierra el segundo.
- **Una verificacion que CONFIRMA lo que esperabas es donde hay que pedir la segunda fuente.**

## CANAL DE ORDENES + PENDIENTES

**Ratificado hoy por el operador:** DECISION-0113 (liveness), 0114 (proveedor vinculante) y 0115
(que significa "verificado"). Las tres nacen de mediciones de la instancia NOVA.

**Pendientes:**
1. El veredicto de 0368 r4 (arriba).
2. **Bonus del informe de NOVA sin plegar todavia**: que el runner del maker commitee su memoria antes
   de soltar el claim (va con TASK-0337), y que el `--health` distinga "se retiro ocioso" de "se
   retiro con trabajo encolado" (va con TASK-0380). No abri ids nuevos por no inflar la cola.
3. **28 tareas `proposed`**, incluidas 0370-0383. La cola de Codex manda el ritmo, no el backlog.

## SIGUIENTE ACCION (tras el cold-start)
1. Leer el veredicto de TASK-0368 r4 y actuar segun cierre o no.
2. Rutear TASK-0378 en cuanto Codex quede libre; 0379 detras.
3. Retomar TASK-0367, la deuda mas antigua del canal.
