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
El exec de review del Analista (OpenAI Codex CLI) **muere ~10min** en reviews Zeus-Aegis pesados (clone+npm test);
NO es deadline (ExecTimeoutSeconds=3600) sino muerte real del proceso (crash/recursos). Deja el `.lock`/`.lease`
huerfano. **El self-heal actual solo limpia si el lease VENCIO (deadline pasado), NO si el PID murio antes** -> el
lock bloquea la cola hasta 1h. Sintoma: lock mtime de hace >10min, EXEC_START sin EXEC_EXIT, `tasklist //FI "PID eq
<pid>"` = 0 (muerto). **DESTRABE MANUAL (mi autoridad):** confirma PID muerto y `rm -f
.protocol-tmp/<peer>_mailbox_cron/*.lock` (+ lease si aplica); el mensaje NO suele quedar `seen` (murio antes) -> el
cron lo re-EXEC solo; el reintento suele completar. Esto es exactamente lo que **TASK-0235** debe cerrar
estructuralmente (self-heal por PID-muerto-pre-deadline). Para no volar el evento en silencio: arma un watcher del
lock (emite si mtime >13min) ademas del monitor de entregas.

### 1c. STOP_JOB (directiva operador 2026-07-01): el token de parada ya NO es ambiguo
Los harnesses ahora se detienen SOLO con el token exacto `STOP_JOB` (`-cmatch "\bSTOP_JOB\b"` en summary/
requested_action). El regex viejo (`detener|deten|parar|para|stop|standdown` + peer) quedo retirado -- se
auto-disparaba con "para" preposicion y con la tarea 0235 (contiene "stop marker"). **Se activa al RELANZAR el cron
con el harness nuevo** (committeado en affe347); hasta entonces el cron vivo usa el harness viejo -> sigue el footgun
en tus mensajes al peer hasta el redespliegue.

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
