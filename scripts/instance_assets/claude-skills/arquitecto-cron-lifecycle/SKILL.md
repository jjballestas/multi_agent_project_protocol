---
name: arquitecto-cron-lifecycle
description: >-
  Autoridad y recetas del Arquitecto para gestionar el ciclo de vida de los crons de los peers
  (Codex/Analista) cuando coordina: DIAGNOSTICAR un cron atascado y DESTRABARLO. USAR cuando: el
  monitor de origin/main da 2+ timeouts seguidos pero los crons estan vivos; el log del cron muestra
  `LOCKED skip` de toda la cola o `LOOP_ERROR`; una entrega no avanza aunque el peer este vivo. El
  Arquitecto (coordinador) tiene autoridad del operador sobre los crons de los peers: matar un cron
  atascado SI lo puede hacer (taskkill esta permitido); el relanzamiento tiene un gate de permisos.
  Trigger words: cron atascado, jammed, LOCKED skip, LOOP_ERROR, lock huerfano, zombie, taskkill,
  relanzar cron, destrabar Codex, destrabar Analista, monitor timeout, cola parada, prompt en uso.
---

# Arquitecto -- ciclo de vida de los crons de los peers

> **METODOLOGIA -- FRONTERA DE INSTANCIA (plantilla de instancia).** Skill de la metodologia: la usa el Arquitecto de
> CUALQUIER instancia. Opera SIEMPRE el ledger de TU instancia desde su raiz de gobernanza `Aegis/` (tu
> `<clon>/Aegis`, p.ej. `<governance-root>`), **NUNCA el hub ni otra instancia**. Las rutas/valores
> concretos son de referencia -- ajusta a tu clon. Los incidentes/tasks citados (F-*, TASK-XXXX) son lecciones
> ILUSTRATIVAS de origen hub, no estado de esta instancia.


> El Arquitecto coordina a Codex/Analista y tiene autoridad del operador sobre sus crons cuando se atascan.
> No lo delegues por reflejo: **matar un cron atascado SI lo puedes hacer** (taskkill esta permitido). Patron
> recurrente: un exec deja un lock o un proceso huerfano y el cron hace `LOCKED skip` de TODA la cola durante horas.
> Detectalo y destrabalo; el relanzamiento tiene un gate (seccion 4).

## 1. Sintomas de un cron atascado
- El **monitor de origin/main da 2+ timeouts seguidos** sin commits, pero los crons estan vivos (pid alive).
- `tail .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.log` muestra, cada ciclo:
  - `LOCKED skip <MSG>` de TODOS los mensajes (lock retenido), o
  - `LOOP_ERROR ... "no puede obtener acceso al archivo '..._mailbox_cron.prompt.v3.txt' porque esta siendo
    utilizado en otro proceso"` (un proceso viejo retiene el prompt file).
- Una tarea ya entregada (su commit `deliver` existe) pero su GO sigue en `mailbox/open/` y NO esta en `.seen.json`
  -> el cron la re-dispara y se vuelve a atascar.

### 1b. Caso MAS COMUN (visto 3x el 2026-07-01): exec de REVIEW muerto -> lock huerfano pre-deadline
El exec de review del Analista (OpenAI Codex CLI) **muere ~10min** en reviews de producto pesados (clone+npm test);
NO es deadline (ExecTimeoutSeconds=3600) sino muerte real del proceso (crash/recursos). Deja el `.lock`/`.lease`
huerfano. **El self-heal actual solo limpia si el lease VENCIO (deadline pasado), NO si el PID murio antes** -> el
lock bloquea la cola hasta 1h. Sintoma: lock mtime de hace >10min, EXEC_START sin EXEC_EXIT, `tasklist //FI "PID eq
<pid>"` = 0 (muerto). **DESTRABE MANUAL (mi autoridad):** confirma PID muerto y `rm -f
.protocol-tmp/<peer>_mailbox_cron/*.lock` (+ lease si aplica); el mensaje NO suele quedar `seen` (murio antes) -> el
cron lo re-EXEC solo; el reintento suele completar. Esto es exactamente lo que **TASK-0235** debe cerrar
estructuralmente (self-heal por PID-muerto-pre-deadline). Para no volar el evento en silencio: arma un watcher del
lock (emite si mtime >13min) ademas del monitor de entregas.

### 1c. STOP_JOB: token de parada por IGUALDAD EXACTA (desplegado 2026-07-02 con TASK-0236)
Los harnesses se detienen SOLO si `requested_action.Trim()` (o `one_line_summary`) es EXACTAMENTE `STOP_JOB`
(`-ceq "STOP_JOB"`, igualdad, NO contains). **Ya NO hay footgun: puedes MENCIONAR "STOP_JOB"/stop/parada/para en
el cuerpo o campos sin detener el cron.** Solo un mensaje cuyo requested_action SEA la orden literal detiene al agente.
Evolucion: (1) regex viejo `(detener|deten|parar|para|stop)`+peer -> se auto-disparaba con "para" preposicion;
(2) fix v1 (affe347) `-cmatch "\bSTOP_JOB\b"` (contains) -> AUN tumbaba el cron al solo MENCIONAR STOP_JOB (footgun-2,
tumbo el cron de Codex el 2026-07-02); (3) fix v2 (TASK-0236, desplegado) `-ceq` igualdad exacta -> footgun muerto.
Si un cron corre un harness pre-0236, vuelve a aplicar la cautela vieja hasta redesplegar.

### 1d. AUTO-EXIT por limite de rondas sin respuesta (MUERTE GRACEFUL, no es jam) -- y la regla de oro de liveness
El cron se AUTO-TERMINA solo tras `max_no_arquitecto_rounds` (=7) ciclos sin un mensaje nuevo del Arquitecto:
`No Arquitecto response limit reached; exiting.` en su `*.log`. Es apagado GRACEFUL por diseno (ahorro), NO un
cuelgue: pid muerto, SIN lock, log limpio. Visto 2x el 2026-07-02 (Codex ~03:17, Analista ~03:43).
- **CONSECUENCIA CRITICA (leccion 2026-07-02, el operador la cazo dos veces):** si le RUTEAS un mensaje a un peer
  cuyo cron YA se auto-termino, **no pasa NADA** -- el mensaje queda en `open/` sin procesar y tu crees que el peer
  esta trabajando. Peor: el monitor de entregas calla (no hay entrega) y el watchdog viejo NO lo veia (solo cazaba
  execs colgados = lock + log congelado; un cron gracefully-exited no tiene lock -> punto ciego total).
- **REGLA DE ORO -- verifica LIVENESS antes y despues de rutear:** ANTES de soltar un GO/REVIEW/ACTION a un peer,
  confirma que su cron esta vivo (`tasklist //FI "PID eq $(cat .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.pid)" //NH | grep -ci powershell`
  = 1, y el `*.log` con heartbeat reciente, NO `limit reached; exiting`). Si esta muerto, **relanza PRIMERO** y luego
  routea (o routea y relanza acto seguido). Incluye la liveness de AMBOS peers en el auto-poll de cada turno.
- **El WATCHDOG debe cazar el cron-MUERTO-con-pendientes, no solo el exec colgado:** por cada peer, si el pid NO
  esta vivo Y hay >=1 mensaje `Arquitecto-to-<Peer>` en `open/` fuera de su `*.seen.json` -> ALERTA "DEAD-CRON,
  relanzar". (Version desplegada en `arquitecto-monitor-coordina` s.1b.) Un cron idle que se auto-termino SIN
  pendientes no es alarma (relanzalo cuando tengas trabajo para el).
- Relanzar: `powershell -NoProfile -File personal/<Peer>/<peer>_mailbox_cron.ps1` (run_in_background). Al arrancar
  procesa la cola de `open/` que no este en su `seen.json`.

## 2. Diagnostico (read-only)
```
tail -12 .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.log      # LOCKED skip / LOOP_ERROR?
cat  .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.lock         # que MSG + timestamp retiene el lock
stat -c '%y' .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.lock # mtime viejo = huerfano
ls -lat .protocol-tmp/<peer>_mailbox_cron/runs/ | head                  # run-log en silencio (mtime viejo) = exec muerto/colgado
PID=$(cat .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.pid); tasklist //FI "PID eq $PID" //NH | grep -ci powershell
```
- **Ojo:** el exec pudo COMPLETAR (entrego la tarea, gates verdes) y aun asi no liberar el lock ni soltar el handle
  del prompt file. "Completo" != "limpio". Revisa el `.out.log`/`.err.log` del run.
- Verifica que no haya **claim huerfano** del peer en CLAIMS.json (normalmente el exec libera su claim; si quedo uno
  activo de un exec muerto, es otra anomalia a resolver).

## 3. Matar el cron atascado (permitido)
`taskkill` esta permitido. Mata el loop del cron **y sus hijos** (incluido el exec zombie que retiene el prompt file):
```
taskkill //PID <cron_pid> //T //F
tasklist //FI "PID eq <cron_pid>" //NH | grep -ci powershell        # 0 = muerto
python -c "open('.protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.prompt.v3.txt','a').close(); print('prompt libre')"
```
Solo borrar el archivo `.lock` NO alcanza si el proceso viejo sigue vivo reteniendo el prompt file: hay que matar el proceso.

### 3b. Pinpoint del holder cuando el zombie esta HUERFANO (no bajo el arbol del cron)
Si `taskkill //PID <cron_pid> //T` NO destraba (el zombie colgaba de otro padre muerto) y no hay `handle.exe`/`openfiles`,
y hay muchos procesos huerfanos (no matar a ciegas: romperia el panel/otros peers), usa el **Windows Restart Manager**
(`rstrtmgr.dll` via python: RmStartSession/RmRegisterResources/RmGetList) para pinpoint EXACTO los PIDs que retienen
el `prompt.v3.txt`/`.lock`, e itera `taskkill //PID <holder> //T //F` hasta `HOLDERS: none`, respetando el cron vivo y
el cron del checker. Script forense: `personal/Arquitecto/who_locks.py` (o equivalente en scratchpad).

### 3c. NO automatizar el barrido (gate Analista NO-GO)
El barrido de zombies es **intervencion manual-forense de emergencia con confirmacion**, NO politica automatica.
Motivo (veredicto Analista `ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto`): Restart Manager prueba POSESION de handle,
NO que el proceso sea zombie -> automatizarlo puede **matar trabajo vivo, incluido el del checker**. El barrido seguro
requiere primero el **contrato exec-lease** (heartbeat/deadline + kill solo por lease VENCIDO + exclusiones + dry-run +
deny-kill de submit_intent/git/npm + post-kill validate) -> **TASK-0235**. Hasta que 0235 este cerrada: solo manual, con
exclusion de la propia sesion y del exec del checker.

## 4. Relanzar el cron
- Comando estandar (params default, Interval 300), con `run_in_background: true`:
  - Codex:    `powershell -NoProfile -File personal/Codex/codex_mailbox_cron.ps1`
  - Analista: `powershell -NoProfile -File personal/Analista/analista_mailbox_cron.ps1`
- El relanzamiento puede estar **gateado por permisos del harness** en algunas sesiones. Si se permite, corre el
  comando y verifica el nuevo pid + primer ciclo en el log. Si el harness lo deniega, **handoff limpio: pasa al
  operador la linea exacta** para que la corra (o ajuste su configuracion de permisos). No intentes rodear el deny.
- El **cron del Arquitecto** (`personal/Arquitecto/arquitecto_cron.ps1`) NO se lanza desde una sesion interactiva del
  Arquitecto: activarlo obliga a stand-down (un escritor a la vez).

### 4b. REDESPLIEGUE completo del harness (deploy de una version nueva del .ps1)
Cuando el `.ps1` en HEAD es una version nueva (p.ej. 0235/0236 mergeados) pero los loops VIVOS corren el codigo
viejo, hay que **teardown + relanzar** (el codigo se carga al arrancar):
1. **Teardown de TODOS los loops** (puede haber DUPLICADOS: verlo es la mitad del bug): `taskkill //PID <p> //T //F`
   a cada loop, mata sus exec trees, y `rm` los `*.lock` + `*.exec-lease.json` stale de ambos peers.
2. **Verifica que quedaron abajo por el LOG** (mtime congelado = down), NO por una query de procesos.
3. **Relanza UNA sola instancia por peer** (s.4). En modo-auto el launch se deniega -> handoff al operador.
4. Confirma en el log el `mailbox cron started` + heartbeat, y que el harness nuevo esta activo (STOP_JOB, self-heal).

### 4c. Gotchas del destrabe/redespliegue (aprendidos 2026-07-02)
- **KILL de ARBOL, no de un pid:** un exec colgado tiene hijos (esbuild/node/cmd/powershell). `taskkill //PID <p> //T //F`
  (arbol) por CADA holder; un `Stop-Process` de un solo pid deja el arbol vivo reteniendo handles.
- **who_locks.py se auto-matchea:** tu propio powershell que corre la query contiene `mailbox_cron.ps1` en su
  command-line -> aparece como "holder"/"loop" (falso positivo, pid cambia cada vez). Fuente de verdad = el LOG
  del cron (frozen=down), no la query de procesos.
- **Prompt compartido:** con el harness previo a 0236, un exec colgado retiene `prompt.v3.txt` COMPARTIDO -> el loop
  no puede lanzar otro exec (LOOP_ERROR). Por eso hay que matar el arbol, no solo `rm` el lock. (0236 lo arregla con
  prompt por-exec.)
- **Diferir un GO** (que el cron lo skipee sin borrarlo): la firma seen es `Name|Length|LastWriteTimeUtc.Ticks`;
  igualala EXACTA (computala con powershell: `$f.Name+'|'+$f.Length+'|'+$f.LastWriteTimeUtc.Ticks`). Un valor custom
  NO sirve (el cron lo ve como "cambio" y re-procesa).

## 5. Post-destrabe (higiene que evita el re-cuelgue)
- **Archiva el GO consumido** que re-disparaba el cuelgue: Codex no puede (`mailbox_archive` exige capability
  `orchestrator`); lo hace el Arquitecto via `submit_intent mailbox_archive` (claim file-scoped open+archived). Ver
  skill `arquitecto-ledger-ops`.
- Gates verdes + drift 0, commitea, push.
- **Re-arma el monitor** (Monitor sobre origin/main) recien cuando el cron este sano; no antes.

## Checklist de una linea
2 timeouts + crons vivos? -> revisa lock / LOOP_ERROR / run-log -> `taskkill //T //F` (permitido) -> prompt libre? ->
relanza `-NoProfile -File personal/<peer>/...ps1` (si el harness deniega: handoff al operador) -> archiva el GO consumido
-> gates+push -> re-arma monitor.
