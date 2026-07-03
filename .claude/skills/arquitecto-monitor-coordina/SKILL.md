---
name: arquitecto-monitor-coordina
description: >-
  Loop reactivo del Arquitecto para coordinar a los peers (Codex/Analista) en semi-automatico desde una
  sesion interactiva: arma un MONITOR sobre origin/main que despierta con las entregas/veredictos de los
  peers, y reacciona (ratificar GO, rutear remediacion/review, promover la siguiente tarea). USAR cuando el
  operador pide "arma un monitor y coordina", o para mantener el pipeline moviendose sin polling manual. Incluye
  el comando exacto del watcher con SELF-FILTER (ignora los propios commits del Arquitecto) para evitar el
  auto-ruido. Trigger words: monitor, coordinar, coordinacion, watcher, origin/main, peers, Codex, Analista,
  veredicto, entrega, ratificar, rutear, promover, semi-auto, self-filter, auto-ruido, re-armar monitor, pipeline.
---

# Arquitecto -- monitor + coordinacion reactiva de peers

> El Arquitecto no puede lanzar crons PowerShell (deny del harness), asi que coordina desde la sesion via un
> MONITOR. **CRITICO (leccion 2026-07-01): vigila el HEAD LOCAL, NO `origin/main`.** Los crons de Codex/Analista
> corren y COMMITEAN al arbol COMPARTIDO pero **muchas veces NO pushean** -- sus entregas quedan como commits
> locales que un watcher de origin NUNCA ve. Un monitor sobre origin te da FALSA cobertura: solo caza pushes, y
> aca el push es la excepcion. Vigilar el HEAD local (mas los MSG `*-to-Arquitecto-*` nuevos en el mailbox) dispara
> en el instante en que el peer entrega, sin depender del push. Tu tambien pusheas sus commits locales al reaccionar.

## 1. El monitor (comando exacto: HEAD LOCAL + entregas, con SELF-FILTER)
`Monitor` tool, `persistent:false`, `timeout_ms:3600000` (1h; menos re-arms en vacio). Vigila el **HEAD local** y las
entregas nuevas; emite SOLO actividad de peers -- **ignora los propios** commits (los del Arquitecto llevan
`Co-Authored-By: Claude Opus` en el cuerpo; los de Codex/Analista NO). Asi re-armar NO se auto-dispara con tus commits:
```bash
cd /d/Agentes/multi_agent_project_protocol
base=$(git rev-parse HEAD)
seen=$(ls Area_comun/mailbox/open/ 2>/dev/null | grep -E "(Codex|Analista)-to-Arquitecto" | sort)
while true; do
  cur=$(git rev-parse HEAD 2>/dev/null)
  msg=""
  if [ "$cur" != "$base" ]; then
    for c in $(git rev-list --reverse ${base}..${cur} 2>/dev/null); do
      if ! git log -1 "$c" --format='%b' 2>/dev/null | grep -q "Co-Authored-By: Claude Opus"; then
        msg="${msg}COMMIT $(git log -1 "$c" --oneline 2>/dev/null)
"
      fi
    done
    base=$cur
  fi
  now=$(ls Area_comun/mailbox/open/ 2>/dev/null | grep -E "(Codex|Analista)-to-Arquitecto" | sort)
  newf=$(comm -13 <(printf '%s\n' "$seen") <(printf '%s\n' "$now") 2>/dev/null)
  if [ -n "$newf" ]; then msg="${msg}NEW-DELIVERY:
${newf}
"; fi
  seen="$now"
  if [ -n "$msg" ]; then echo "=== PEER ACTIVITY (local tree) ==="; printf '%s' "$msg"; break; fi
  sleep 30
done
```
Al recibir el evento: `git fetch` + coordina + **pushea el commit local del peer** (si no lo pusheo) + **re-arma** el
monitor. Con el self-filter, re-armar tras tus commits es seguro. Un watcher de `origin/main` es el ERROR historico:
te hace depender de que el operador te diga "revisa" porque no ves las entregas locales sin pushear.

## 1b. SEGUNDO monitor OBLIGATORIO: watchdog de salud de execs (falla silenciosa)
El monitor de entregas SOLO dispara cuando hay salida (commit/MSG). **Un exec colgado o muerto NO produce nada ->
el monitor calla -> no te enteras salvo que el operador lo note.** Arma SIEMPRE un segundo monitor `persistent:true`
que detecta el cuelgue por **lock retenido + run-log CONGELADO** (un exec vivo escribe a su `runs/*.err.log`; uno
colgado lo congela -- senal de vida robusta que distingue "colgado" de "lento-pero-vivo", no mata trabajo bueno):
```bash
cd /d/Agentes/multi_agent_project_protocol
declare -A alerted
while true; do
  for peer in codex analista; do
    dir=".protocol-tmp/${peer}_mailbox_cron"; lock="$dir/${peer}_mailbox_cron.lock"
    if [ -f "$lock" ]; then
      newest=$(ls -t "$dir"/runs/*.err.log 2>/dev/null | head -1)
      if [ -n "$newest" ]; then
        age=$(( $(date +%s) - $(stat -c %Y "$newest") ))
        if [ "$age" -gt 480 ]; then
          if [ "${alerted[$peer]}" != "1" ]; then
            echo "=== HUNG-EXEC $(date '+%H:%M:%S') ==="; echo "$peer: lock retenido + run-log CONGELADO ${age}s -> exec colgado/muerto; who_locks + destrabar."; alerted[$peer]=1
          fi
        else alerted[$peer]=0; fi
      fi
    else alerted[$peer]=0; fi
  done
  sleep 60
done
```
Emite una vez por episodio (flag `alerted`) y se resetea cuando el lock se va o el log vuelve fresco. Junto con el de
entregas cubre los DOS desenlaces de un exec: entrega (commit/MSG) o cuelgue (silencioso). El fix PERMANENTE del
cuelgue es TASK-0236/0237 (harness + hang-proof del npm test); el watchdog es el control compensatorio mientras tanto.

## 1c. TERCER monitor OBLIGATORIO: watchdog de higiene de mailbox (enforcer del cada-5)
La regla de higiene cada-5 es DISCIPLINA DE MODELO y se cae bajo carga alta (F2 2026-07-03: cascadas rapidas +
peers en exec -> el auto-poll por turno degenera a "vigilar el bloqueo actual" y suelta el conteo de consumidos;
open/ acumulo 19 sin higiene y el operador lo noto). El fix durable es un ENFORCER MECANICO: un watchdog persistente
que alerta cuando `open/` cruza un umbral, para clasificar consumidos + archivar en la proxima ventana idle:
```bash
cd /d/Agentes/multi_agent_project_protocol
alerted=0
while true; do
  n=$(ls Area_comun/mailbox/open/ 2>/dev/null | grep -c "MSG-")
  if [ "$n" -ge 10 ]; then
    if [ "$alerted" != "1" ]; then
      echo "=== MAILBOX-ACUMULADO $(date '+%H:%M:%S') ==="; echo "open/ tiene $n mensajes (umbral 10). Clasifica consumidos vs vivos y corre higiene (mailbox_archive) en la proxima ventana idle (peers sin lock)."; alerted=1
    fi
  else alerted=0; fi
  sleep 120
done
```
No archives desde el watchdog (semantica: "consumido" la decides tu); solo ALERTA. Al dispararse, clasifica y corre
`mailbox_archive` (skill mailbox-hygiene) en ventana idle (peers sin lock + tree sin half-write peer). Umbral 10 es
proxy mecanico del cada-5-consumidos.

## 1d. ARMAR LOS 3 MONITORES AL INICIAR SESION (directiva operador 2026-07-03)
Al arrancar como Arquitecto, arma SIEMPRE los tres como parte del cold-start: (1) monitor de entregas (s.1),
(2) watchdog 15-min/salud-execs (s.1b, ampliado a stall silencioso), (3) watchdog de higiene de mailbox (s.1c).
Los watchdogs son el ENFORCER; el auto-poll por turno es red primaria pero se cae bajo carga -> los monitores
mecanicos lo respaldan. **Exportabilidad:** estos watchdogs deben poder EXPORTARSE al instanciar la metodologia
(un Aegis/instancia recien creada arma los mismos en el arranque de sus agentes) -> item de diseno: portarlos a la
capa neutral `skills/` (DECISION-0061, exportable via new_instance) o al agent-runbook del TASK_TEMPLATE de instancia.
Ver [[watchdogs-al-iniciar-sesion]].

## 2. Reglas de reaccion (que hacer con cada senal de peer)
En cada wake: `git fetch` + `git merge --ff-only origin/main` (los peers commitean al arbol compartido; tu HEAD
local puede ir detras de origin). Luego, segun la senal:

| Senal del peer | Accion |
|---|---|
| **Analista GO / GO-CERRABLE** sobre X | Ratifico de checker: `task_status X in_review -> review_approved` (submit_intent); ACTION a Codex para el done-flip |
| **Analista NO-GO / CAMBIO-REQUERIDO** sobre X | Ruteo remediacion a Codex (ACTION) con el hallazgo concreto del veredicto |
| **Codex entrega** X a in_review (commit `deliver`/`redeliver`/`fix`) | Ruteo REVIEW al Analista (gate adversarial) |
| **Tarea -> done** (Codex done-flip) | Promuevo la SIGUIENTE del backlog de a una: `proposed -> ready` + GO |
| **Mensaje con `requires_response: true` a Arquitecto** | Respondo (cierra el loop) |
| **Directiva del operador** | La atiendo/escalo |

## 3. Rieles en cada ciclo (invariantes)
- Gate por EXIT-CODE antes de commit: `validate_collaboration_state.py` + `scan_encoding.py` + neutralidad = 0.
- **Commitea el saneamiento ANTES de pedir review** (el peer clona HEAD; si tus cambios estan solo en el working
  tree, HEAD sale rojo y el peer bloquea).
- **Ventana segura para el ledger** (submit_intent): 0 claims activos de peer + sin `index.lock`.
- Mensajes ASCII + footgun-safe (ver arquitecto-ledger-ops: nada de palabra-stop junto a cron/peer).
- Promocion de a UNA (DECISION-0020 #7). Push directo a main cuando verde. Narracion minima (DECISION-0038).
- Tras cada commit: actualiza memoria (DECISION-0026).

## 4. Gotchas aprendidos
- **EL MONITOR ASYNC NO BASTA SOLO -- AUTO-POLL al inicio de CADA turno (leccion 2026-07-02):** un monitor armado y
  vivo puede NO despertar la sesion cuando la entrega del peer cae en la ventana en que la sesion esta IDLE esperando
  input del usuario (el bash en background no se agenda / la notificacion no fuerza un turno). Sintoma real: entrega
  del Analista 03:17, monitor armado ~03:10 aun corriendo con 0 output, no desperto; el operador tuvo que preguntar
  "como va". La logica del monitor estaba bien (verificada a mano: base->ve los commits peer, pasan self-filter).
  FIX durable: **red PRIMARIA = auto-poll barato al empezar cada turno** (`git log --oneline -3`, `git status -sb`,
  `ls Area_comun/mailbox/open/`, estado de la tarea en vuelo); el monitor es RESPALDO. Cuando la sesion tiene
  actividad el monitor SI dispara (verificado con el done-flip 0237 y la entrega 0229); el hueco es solo la ventana
  idle. Nunca reportes "en curso" sin antes auto-pollear el HEAD real.
- **VERIFICA LIVENESS DEL PEER ANTES Y DESPUES DE RUTEAR (leccion 2026-07-02, el operador la cazo):** rutear un
  GO/REVIEW/ACTION a un peer cuyo cron YA se auto-termino (7 rondas sin respuesta, ver arquitecto-cron-lifecycle
  s.1d) NO hace NADA: el mensaje queda en `open/` sin procesar y tu crees que el peer trabaja. Sintoma real: rutee
  REVIEW-0229 + REQUEST-cierres al Analista 04:08 pero su cron habia muerto 03:43 -> nada avanzo hasta que el
  operador pregunto 04:34. FIX: antes de soltar un mensaje a un peer, `tasklist //FI "PID eq $(cat
  .protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.pid)" //NH | grep -ci powershell` = 1 y `*.log` con
  heartbeat reciente (no `limit reached; exiting`); si esta muerto, RELANZA primero. El auto-poll de cada turno
  incluye liveness de AMBOS peers, no solo git/open.
- **El WATCHDOG (s.1b) caza AMBOS: exec colgado (lock + log congelado) Y cron-MUERTO-con-pendientes** (pid no vivo +
  >=1 `Arquitecto-to-<Peer>` en open/ fuera de su seen.json). Un cron gracefully-exited NO tiene lock -> el watchdog
  viejo (solo lock) era CIEGO a la muerte graceful; la v2 chequea pid-liveness + pendientes. Idle-sin-pendientes no
  alarma.
- **Auto-ruido:** sin el self-filter, el monitor se dispara con tus propios commits. El filtro `Co-Authored-By:
  Claude Opus` los descarta (verificado: tus commits lo llevan, los de Codex/Analista no).
- **2+ timeouts seguidos con crons vivos** = cron atascado (lock/proceso huerfano). NO es "nada que hacer": diagnostica
  y destraba -> skill `arquitecto-cron-lifecycle`.
- **SILENT-REFUSAL (leccion 2026-07-03):** una tarea que queda en `in_review` con tu ACTION/GO marcada *seen* en el
  `<peer>_mailbox_cron.seen.json` pero SIN reentrega (status no avanza, no hay commit de fix) NO significa "peer
  trabajando". El heartbeat (`processable=0`) y el pid-vivo MIENTEN aqui: el peer YA ejecuto y se NEGO. Revisa
  `.protocol-tmp/<peer>_mailbox_cron/runs/*.err.log` (el ultimo por mtime) -> ahi esta el motivo. Caso real: Codex
  se nego a remediar TASK-0240 ~1h porque el Analista dejo un claim con scope wildcard `["*"]`
  (`CLAIM-...-wild-release`) que bloqueaba toda edicion compartida; salio sin commit y el monitor de entregas nunca
  disparo (no hubo salida). FIX: (1) resuelve el bloqueo real (aqui el claim wildcard se libero solo despues;
  si no, es anomalia DECISION-0018 a senalar/resolver); (2) **des-seen** la ACTION en el `seen.json` del peer
  (skill `arquitecto-cron-lifecycle` s.5) para que el cron la reprocese. Regla: si el monitor timea sobre una
  remediacion en vuelo, mira el err.log del peer ANTES de asumir que sigue trabajando.
- **DUAL-SESION ARQUITECTO (leccion 2026-07-03, directiva Operador resolucion-dual-sesion):** dos sesiones
  interactivas del Arquitecto pueden quedar vivas a la vez (la vieja con monitores armados sigue reaccionando
  cuando el operador ya arranco la nueva). Son INVISIBLES entre si: ambas firman actor_id Arquitecto y sus
  commits llevan Co-Authored-By: Claude, asi que el SELF-FILTER de ambos monitores descarta los commits de la
  otra -> colision silenciosa (higiene/promociones/GOs duplicados). GUARD OBLIGATORIO: al arrancar, verificar
  `personal/Arquitecto/.session-lease` (si hay lease FRESCO <30min de otro session_id -> NO coordinar, consultar
  al Operador); escribir/refrescar el lease propio en cada turno como parte del auto-poll; borrarlo al cerrar.
  Mitigacion si la dualidad ya ocurrio: particion de carriles via CLAIMS del ledger (unico mutex efectivo entre
  sesiones con la misma firma) + FYI al Operador para que ordene el stand-down de una (discriminador por
  session_start_ts). NO re-emitir GOs/higiene que la otra ya emitio: verificar CLAIMS.json + git log ANTES de
  cada escritura compartida.
- **REGLA 15-MIN por tarea demorada (directiva operador 2026-07-03):** BASELINE = una tarea normal del loop
  demora 6-9 min en promedio; una tarea/peticion ruteada que lleve >15 min sin entrega ni respuesta es ANOMALIA
  -> revision de analisis OBLIGATORIA, no espera pasiva. Es un disparador POR TAREA (evento), NO un polling
  periodico. Deteccion (watchdog v3.1, 3 formas de la demora): (a) peticion Arquitecto-to-peer >900s sin entrar
  al seen.json; (b) peticion *seen* >900s SIN respuesta NI commit del peer (silent-refusal); (c) claim activo
  retenido >900s sin exec corriendo. Analisis al disparar: tail del ultimo `runs/*.err.log` del peer (su
  ENVELOPE FINAL suele decir que espera o por que se nego -- leerlo PRIMERO: asi se cazo la espera-cruzada de
  claims 0241/0242), seen.json, CLAIMS.json activos, status de la tarea; remedio tipico = destrabar el bloqueo
  (claim/lock) + des-seen para re-disparar.
- **Arbol compartido:** peers commitean aqui; `git merge --ff-only` cada wake; `git pull --rebase --autostash` si el
  push sale non-ff. Vi gates en rojo TRANSITORIO por un peer a mitad de escritura -> re-correr hasta verde.
- **Trigger diferido:** si el operador pide "promover X luego de que Codex termine su cola", vigila via el monitor
  hasta que Codex quede sin pendientes y recien ahi promueve X.

## Checklist de una linea
Arma monitor self-filter -> wake con peer -> fetch+ff -> reacciona (GO=ratifico+done-flip / NO-GO=remediacion /
entrega=REVIEW / done=promuevo siguiente / rr=respondo) -> gate exit-code -> commit+push -> re-arma monitor.
Complementa: arquitecto-ledger-ops (recetas submit_intent), arquitecto-cron-lifecycle (cron atascado), mailbox-hygiene.
