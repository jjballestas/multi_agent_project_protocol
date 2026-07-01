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
