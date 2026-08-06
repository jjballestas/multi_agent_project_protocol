---
name: cron-zombie-sweep
description: >-
  Caza y mata PROCESOS HUERFANOS (zombies) que dejan los execs de los crons de agente (Codex/Analista/
  Arquitecto) cuando se cuelgan y el harness los mata por deadline o el Arquitecto los mata a mano: el
  TREE_KILL no siempre limpia el arbol, y quedan procesos node/python/git (node --test,
  architect-runtime-launcher.mjs, architect-runtime-stub.mjs, frontserver/vite, submit_intent, validate)
  vivos horas, reteniendo puertos/locks/memoria y colgando los execs siguientes. USAR cuando: el watchdog
  exec-health dispara (lock retenido + err.log 0-byte congelado); un review/entrega/exec no avanza con
  CPU~0; ANTES y DESPUES de destrabar un exec colgado (taskkill); o periodicamente al notar node/python
  procs viejos. Es el CAZADOR compensatorio; el fix de RAIZ (que el harness TREE_KILL limpie el arbol +
  timeout de cross-atest) es una tarea aparte. Complementa arquitecto-cron-lifecycle (destrabar cron) y el
  watchdog exec-health de arquitecto-monitor-coordina. Trigger words: zombie, zombies, huerfano, orphaned,
  proceso colgado, node --test colgado, exec colgado, cazar zombies, matar huerfanos, taskkill, TREE_KILL,
  procesos node viejos, frontserver huerfano, sweep, barrido de procesos, err.log 0-byte, CPU 0.
---

# cron-zombie-sweep -- cazar y matar procesos huerfanos de execs de cron

> Autoridad: el Arquitecto tiene autorizacion del operador para taskkill (pedirla per-sesion si el
> clasificador la deniega). NO mata los CRONS persistentes (los loops *_mailbox_cron.ps1), solo los
> huerfanos de trabajo. Fix de raiz = TASK de harness (TREE_KILL completo + timeout de cross-atest).

## 1. El PATRON (por que aparecen)
1. Un exec de cron (Codex/Analista/Arquitecto) spawnea procesos hijo al trabajar: `node.exe`
   (`node --test`, `architect-runtime-launcher.mjs`, `architect-runtime-stub.mjs`, frontserver `src/server.js`,
   `vite`), `python.exe` (`submit_intent`, `validate_collaboration_state`), `git.exe` (clone/checkout).
2. El exec se CUELGA (fallo de proveedor -> err.log 0-byte + CPU~0; o cross-atest que cuelga) y el harness
   lo TREE_KILL por DEADLINE (1h) -- o el Arquitecto lo mata a mano para destrabar.
3. **El kill NO limpia el arbol completo** (permiso denegado en un nieto, o `taskkill` sin `/T`): los hijos
   quedan HUERFANOS (reparentados), vivos horas, reteniendo puertos (4173/4289 del frontserver), locks,
   memoria -> **cuelgan el siguiente exec** (conflicto de recurso) y el ciclo se repite.

Sintoma de cuelgue (distinguir de "lento-pero-vivo"): `Get-Process -Id <pid>` da **CPU ~0** y
**NI `runs/*.out.log` NI `runs/*.err.log`** han producido una sola linea pasado el margen real de la
tarea. Un exec vivo consume CPU.

> **RECALIBRADO 2026-08-06 tras un falso positivo en vivo.** La regla anterior era "`err.log` 0 bytes
> congelado **>13min**", y marca como colgado un exec perfectamente sano. Dos correcciones:
> 1. **Mira `out.log`, no solo `err.log`.** Con `-AgentProvider Anthropic` la salida normal va a
>    **stdout**, y un `err.log` a 0 bytes es el estado **SANO** (sin errores), no una senal de cuelgue.
> 2. **13 minutos es demasiado poco.** Las reviews del Analista tardan **12-37 min** y su salida
>    aparece **AL FINAL**, no de forma continua: durante casi todo el exec los dos logs estan a 0. Usa
>    un margen por encima del maximo observado (**45 min**) o derivalo del `-ExecTimeoutSeconds` de ese
>    peer, y **antes de matar comprueba CPU acumulada y tamano de proceso**: la regla es REVISAR, no
>    matar (ver [[feedback-timeout-revisar-no-matar]]).
>
> El coste de equivocarse aqui no es simetrico: un falso positivo mata trabajo bueno y ademas ensena
> al operador a ignorar la alarma.
>
> 3. **Mide la CPU del ARBOL, no del pid del log.** El pid que publica `*_mailbox_cron.log` es el
>    **envoltorio PowerShell**; el trabajo lo hace un hijo (`claude.exe` / `codex.exe`). Caso real
>    2026-08-06: el padre marcaba **0,31 s** de CPU mientras el hijo llevaba **25 s y 519 MB**.
>    Medir solo la raiz garantiza el falso positivo. Recorre los hijos recursivamente y suma; si el
>    arbol consume CPU, el exec esta VIVO aunque sus logs esten a cero.

## 2. CAZAR (detectar los huerfanos) -- comando probado
Un proceso node/python/git es ZOMBIE si (a) su proceso PADRE ya NO esta vivo (huerfano/reparentado) Y
(b) su linea de comando matchea una firma de trabajo de agente. Listar SIN matar:
```bash
powershell.exe -NoProfile -Command '
$live = (Get-Process).Id
Get-CimInstance Win32_Process -Filter "Name=''node.exe'' OR Name=''python.exe'' OR Name=''git.exe''" |
  Where-Object { ($_.ParentProcessId -notin $live) -and ($_.CommandLine -match "architect-runtime|--test|Zeus-protocol|submit_intent|validate_collaboration|vite|src.server") } |
  Select-Object ProcessId,ParentProcessId,CreationDate,@{n="Cmd";e={$_.CommandLine.Substring(0,[Math]::Min(80,$_.CommandLine.Length))}} | Format-Table -Auto
'
```
Ajusta la firma (`-match`) al producto: anade rutas/nombres del repo que se este observando. La edad
(CreationDate vieja, anterior al exec vivo actual) refuerza el diagnostico.

## 3. MATAR (destrabar + barrer)
1. **El exec colgado en si** (el powershell del EXEC, NO el cron loop): `taskkill //F //T //PID <exec_pid>`
   -- el `/T` mata el ARBOL (hijos + nietos). Si un nieto da "permiso denegado", igual mata lo que puede;
   sigue con el barrido. Identifica el exec por el `EXEC_START pid=<...>` del `*_mailbox_cron.log` o por el
   lock retenido.
2. **Barrido de huerfanos remanentes** (los que sobrevivieron al TREE_KILL):
```bash
powershell.exe -NoProfile -Command '
$live = (Get-Process).Id
$orphans = Get-CimInstance Win32_Process -Filter "Name=''node.exe'' OR Name=''python.exe''" |
  Where-Object { ($_.ParentProcessId -notin $live) -and ($_.CommandLine -match "architect-runtime|--test|Zeus-protocol|submit_intent|validate_collaboration|vite|src.server") }
foreach($p in $orphans){ Write-Host "kill orphan $($p.ProcessId): $($p.CommandLine.Substring(0,[Math]::Min(50,$p.CommandLine.Length)))"; Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue }
if(-not $orphans){ Write-Host "no orphans remaining" }
'
```
3. **Verifica limpio:** re-corre el cazador (s.2) -> vacio. `tasklist //FI "IMAGENAME eq node.exe"` sin
   procesos de trabajo. Los CRONS (`*_mailbox_cron.ps1`, pids persistentes) SIGUEN VIVOS.

## 4. Que NO matar (seguridad)
- Los **crons persistentes** (`codex/analista/arquitecto_mailbox_cron.ps1`, pids de larga vida): matarlos
  DETIENE al agente. Solo se matan los EXECS de trabajo y sus hijos huerfanos.
- Procesos node/python de una sesion VIVA (hijos de un exec actualmente corriendo, con err.log creciendo).
- El IDE / la sesion del Arquitecto / procesos del operador. La firma `-match` acota a trabajo de agente;
  revisa la lista del cazador ANTES de barrer si hay duda.

## 5. Despues de matar
- Si mataste un exec de review/entrega con veredicto/entrega YA ENTREGADO: el cron programa RETRY; para
  cortarlo, avanza el ESTADO de la tarea (p.ej. NO-GO flip in_review->changes_requested) para que el retry
  ABORTE (task ya no reclamable/revisable), o marca el MSG seen (skill arquitecto-cron-lifecycle s.5; ojo:
  editar seen.json puede requerir permiso del operador). NUNCA dejes un retry colgandose en bucle.
- Reporta el episodio como anomalia DECISION-0018 si es recurrente, y escala el FIX DE RAIZ (harness
  TREE_KILL completo + timeout de cross-atest) a una tarea gobernada.

## 6. Exportabilidad (DECISION-0061)
Este cazador es generico de la metodologia: portarlo a la capa neutral `skills/` (exportable via
new_instance) para que toda instancia lo tenga. Ajustar solo las firmas `-match` al stack del producto de
la instancia. Neutralidad: cero terminos de dominio; las firmas son nombres de herramientas/rutas, no negocio.

## Checklist de una linea
Watchdog dispara / exec CPU~0 + err.log 0-byte -> CAZA (s.2, listar) -> confirma huerfanos -> MATA el exec
(`taskkill /F /T`) + BARRE huerfanos (s.3) -> verifica limpio + crons vivos -> corta el retry (avanza estado)
-> anomalia + escala fix de raiz si recurrente.
