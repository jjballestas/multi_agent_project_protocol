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
`Co-Authored-By: Claude <modelo>` en el cuerpo; los de Codex/Analista NO). **IGNORA TODOS los modelos Claude
(Opus AND Fable AND Sonnet), no solo Opus** -- leccion dual-sesion 2026-07-03: la OTRA sesion Arquitecto puede
correr en otro modelo (Fable 5) y su firma es `Claude Fable`; un self-filter solo-Opus reacciona a esa sesion.
Ampliado 2026-07-04: una sesion en Sonnet 5 firma `Claude Sonnet 5`, y el filtro viejo (solo Opus|Fable) SI
disparaba con los propios commits de esa sesion (falso positivo verificado). **IGNORA
TAMBIEN al ASESOR** (leccion 2026-07-04): sus commits llevan `Co-Authored-By: asesor <asesor@nova.local>` (NO el
trailer Claude) y/o subject `checkpoint(asesor)` -> sin filtrarlo, sus checkpoints frecuentes disparan ruido. El
filtro cubre `Co-Authored-By: Claude (Opus|Fable|Sonnet)` OR `Co-Authored-By: asesor` OR subject `^checkpoint\(asesor\)`
(por eso el grep lee `%s%n%b` = subject+body, no solo `%b`). Asi re-armar NO se auto-dispara con tus commits, ni
con los de una sesion Arquitecto hermana, ni con los del asesor:
```bash
cd /d/Agentes/multi_agent_project_protocol
base=$(git rev-parse HEAD)
seen=$(ls Area_comun/mailbox/open/ 2>/dev/null | grep -E "(Codex|Analista|Operador)-to-Arquitecto" | sort)
while true; do
  cur=$(git rev-parse HEAD 2>/dev/null)
  msg=""
  if [ "$cur" != "$base" ]; then
    for c in $(git rev-list --reverse ${base}..${cur} 2>/dev/null); do
      body=$(git log -1 "$c" --format='%s%n%b' 2>/dev/null)
      if ! echo "$body" | grep -qE "Co-Authored-By: Claude (Opus|Fable|Sonnet)|Co-Authored-By: asesor|^checkpoint\(asesor\)"; then
        msg="${msg}COMMIT $(git log -1 "$c" --oneline 2>/dev/null)
"
      fi
    done
    base=$cur
  fi
  now=$(ls Area_comun/mailbox/open/ 2>/dev/null | grep -E "(Codex|Analista|Operador)-to-Arquitecto" | sort)
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

**ARMALO `persistent:true` (correccion 2026-08-13).** El de un disparo muere al notificar y el de 1h
expira; esta semana costo DOS huecos ciegos de 4h y 7h, en uno de los cuales el peon vacio su cola y
se auto-retiro sin que yo me enterara. Persistente = no vuelve a pasar. (El parrafo de abajo describe
por que el single-shot era peligroso; se conserva como diagnostico historico.)

**EL SELF-FILTER POR MODELO NO DISTINGUE A UNA SESION HERMANA (2026-08-14, medido en campo por la
instancia NOVA y confirmado contra esta skill).** El patron
`Co-Authored-By: Claude (Opus|Fable|Sonnet)` es una firma de MODELO: otra sesion de Arquitecto firma
IGUAL, asi que cada monitor descarta los commits de la hermana creyendolos propios. Dos Arquitectos
operaron una instancia durante horas siendo invisibles el uno para el otro POR CONSTRUCCION, y el
coste fue real -- una entrega verificada como incompleta se ruteo al checker sin esa evidencia. El
arreglo de codigo es TASK-0383 (filtrar por SESION, no por modelo). **Mientras no aterrice: si ves
commits que no recuerdas haber hecho, NO asumas que son tuyos** -- mira el reflog y el lease antes de
concluir nada.

**CRITICO (leccion 2026-07-05): este monitor es SINGLE-SHOT -- se dispara UNA vez y muere.** A diferencia
de los watchdogs 1b/1c (`persistent:true`), este NO sigue vivo tras notificar. Si procesas la notificacion
(lees el mensaje, actuas, commiteas) pero NO vuelves a invocar `Monitor` con el mismo comando ANTES de
pasar a esperar de nuevo, quedas ciego a la SIGUIENTE entrega hasta que el operador pregunte manualmente.
El operador lo detecto 2 veces en una sola sesion. Regla dura: la ULTIMA accion de cada ciclo de reaccion
(despues de commitear+pushear) es SIEMPRE re-armar este mismo monitor -- no lo dejes para "cuando tenga
algo mas que hacer". Ademas, el filtro de nombres de archivo debe cubrir TAMBIEN `Operador-to-Arquitecto`
(no solo Codex/Analista) -- una DIRECTIVA nueva del operador via Asesor/mailbox tambien debe despertarte,
y el patron viejo (solo peers) era ciego a eso.

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

**USA EL HEARTBEAT `EXEC_RUNNING` DEL LOG DEL CRON, NO EL mtime DEL `err.log` (correccion 2026-08-12).**
La version de arriba falso-positivea en CADA review: en text-mode el `err.log` queda a **0 bytes** y su
mtime nunca se refresca, asi que a los 480 s canta cuelgue con el exec perfectamente vivo (medido: disparo
a los 511 s mientras el hijo `claude.exe` tenia WS de 450 MB y el heartbeat latia). El arnes emite
`EXEC_RUNNING pid=... elapsed=Ns` cada 60 s (TASK-0302): esa SI es senal de vida. Version corregida --
alerta solo si el LOG DEL CRON lleva >300 s sin latir y el ultimo evento no es `EXEC_EXIT`:
```bash
cd /d/Agentes/multi_agent_project_protocol
declare -A alerted
while true; do
  for peer in codex analista; do
    dir=".protocol-tmp/${peer}_mailbox_cron"; lock="$dir/${peer}_mailbox_cron.lock"; log="$dir/${peer}_mailbox_cron.log"
    if [ -f "$lock" ] && [ -f "$log" ]; then
      hb=$(grep -n "EXEC_RUNNING\|EXEC_START\|EXEC_EXIT" "$log" 2>/dev/null | tail -1)
      logage=$(( $(date +%s) - $(stat -c %Y "$log") ))
      case "$hb" in
        *EXEC_EXIT*) alerted[$peer]=0 ;;
        *) if [ "$logage" -gt 300 ]; then
             if [ "${alerted[$peer]}" != "1" ]; then
               echo "=== HUNG-EXEC $(date '+%H:%M:%S') ==="
               echo "$peer: lock retenido y el HEARTBEAT lleva ${logage}s sin latir (ultimo: ${hb})."
               alerted[$peer]=1
             fi
           else alerted[$peer]=0; fi ;;
      esac
    else alerted[$peer]=0; fi
  done
  sleep 60
done
```

**FALSO POSITIVO EN TEXT-MODE -- NO MATES SIN VERIFICAR LIVENESS REAL (leccion 2026-07/08, aplicada ~5x):** con
`claude --output-format text` el exec BUFEA stdout hasta el final y deja `runs/*.err.log` en **0 bytes**, asi que su
mtime NUNCA se refresca -> este watchdog lo ve "CONGELADO" y falso-positivea en CADA review (las reviews del Analista
tardan 12-37min). El err.log 0-byte NO prueba cuelgue. Cuando dispare, **REVISA LIVENESS REAL antes de tocar nada**
(directiva del operador "revisar, no matar a ciegas", ver [[feedback-timeout-revisar-no-matar]]): (1) el hijo
`claude.exe` del exec (`Get-CimInstance Win32_Process -Filter ParentProcessId=<execpid>`) con **CPU>0 + ws~450-480MB**
= trabajando; (2) el clon de review bajo `D:/Aegis_Scratch/protocol/` con actividad reciente; (3) la edad del exec
(EXEC_START del cron log) dentro de la ventana 12-37min; (4) `submit_intent` colgado en fase commit? Solo si el hijo
claude esta MUERTO o el exec supera con mucho la ventana Y sin progreso, es cuelgue real. Antes de ratificar/escribir
el ledger tras una entrega, verifica ademas que el peer no este a mitad de commit (verdict/HANDOFF untracked + exec
vivo -> espera su EXEC_EXIT). El TASK-0302 (heartbeat EXEC_RUNNING) da al watchdog una senal de vida fiable en el
cron log; usala en vez del err.log cuando este disponible.

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
mecanicos lo respaldan. **Y arma tambien el CUARTO (s.1g, encargo muerto)**: los tres obligatorios cubren
entrega y cuelgue, pero un exec que MUERE sin colgarse se ve exactamente igual que un peon sin trabajo, y ese
punto ciego costo cinco horas el 17-ago. **Exportabilidad:** estos watchdogs deben poder EXPORTARSE al instanciar la metodologia
(un Aegis/instancia recien creada arma los mismos en el arranque de sus agentes) -> item de diseno: portarlos a la
capa neutral `skills/` (DECISION-0061, exportable via new_instance) o al agent-runbook del TASK_TEMPLATE de instancia.
Ver [[watchdogs-al-iniciar-sesion]].

## 1e. PUNTO CIEGO del self-filter: mensajes del Operador commiteados por el ASESOR (leccion 2026-07-14)
El Asesor rutea GOs/DIRECTIVAs del Operador commiteando el MSG al arbol -- y sus commits pueden llevar
`Co-Authored-By: Claude <modelo>` (la sesion asesor corre en Claude). El SELF-FILTER del monitor de commits
los descarta como "propios", y aunque el chequeo NEW-DELIVERY por nombre de archivo los cubre, la
notificacion puede quedar detras de turnos largos. Caso real: un GO rr (respuesta a 3 inputs) estuvo ~1h en
el arbol sin procesarse; se descubrio por una via lateral. REGLA DURA: el **auto-poll al inicio de CADA
turno** (`git log --oneline -3` + `ls Area_comun/mailbox/open/ | grep to-Arquitecto`) se ejecuta SIEMPRE,
aunque el mensaje del operador parezca puro debate/consulta/Notion -- la respuesta que esperas puede estar
YA en el arbol.

## 1f. Watch read-only de OTRA instancia (dos-trios, DECISION-0095)
Cuando hay trabajo de otra instancia en vuelo que el hub debe cosechar (un gate por cerrar, un encargo con
deadline), arma un monitor persistente ADICIONAL read-only sobre SU `origin/main`. NO reemplaza a los 3
obligatorios del hub; es el ojo dos-trios: no operas su ledger, pero te enteras en <2min de cada avance
(registro, entrega del maker, veredicto del checker, done-flip) y cosechas (cross-atest, enmiendas) sin
pedir reportes:
```bash
cd /d/Agentes/<ruta-instancia>
base=$(git rev-parse origin/main 2>/dev/null)
while true; do
  git fetch origin --quiet 2>/dev/null || true
  cur=$(git rev-parse origin/main 2>/dev/null)
  if [ "$cur" != "$base" ]; then
    echo "=== <INSTANCIA> origin/main AVANZO $(date '+%H:%M:%S') ==="
    git log --oneline ${base}..${cur} 2>/dev/null
    base=$cur
  fi
  sleep 120
done
```

## 1g. EL CUARTO DESENLACE que los 3 watchdogs NO cubren: el ENCARGO MUERTO (2026-08-17, 5 horas ciegas)
Los 3 obligatorios cubren dos desenlaces de un exec: **entrega** (s.1) y **cuelgue** (s.1b). Hay un TERCERO
que ninguno ve: el exec **muere sin colgarse**. El arnes lo reintenta, agota los intentos
(`RETRY_EXHAUSTED attempts=3`, causa tipica: el CLI del proveedor revienta con un error de su router), marca
el mensaje y **vuelve a idle**. Desde fuera el cuadro es **IDENTICO al de "no hay trabajo"**: cron vivo,
heartbeat puntual, `processable_messages=0`, sin lock, sin claims, sin commit. El monitor de entregas calla
(no hubo salida), el de salud calla (no hay lock retenido), el de higiene calla. **Caso real: 03:18 -> 07:56,
cinco horas creyendo que el peon trabajaba.**

**El discriminador NO es la liveness del cron.** Es una **obligacion de trabajo pendiente, no reconocida y
DURADERA**: hay una tarea `in_progress` cuyo dueno no ha producido nada en N minutos y cuyo mensaje ya no
esta pendiente en `open/`. Cuarto watchdog, barato y directo a la causa:
```bash
cd /d/Agentes/multi_agent_project_protocol
declare -A alerted
while true; do
  for peer in codex analista; do
    r=".protocol-tmp/${peer}_mailbox_cron/${peer}_mailbox_cron.retry.json"
    log=".protocol-tmp/${peer}_mailbox_cron/${peer}_mailbox_cron.log"
    dead=$(grep -o "RETRY_EXHAUSTED[^\"]*" "$log" 2>/dev/null | tail -1)
    ex=$(grep -o "EXEC_EXIT code=[0-9]*" "$log" 2>/dev/null | tail -1)
    if [ -n "$dead" ] || [ "$ex" != "EXEC_EXIT code=0" -a -n "$ex" ]; then
      if [ "${alerted[$peer]}" != "$dead$ex" ]; then
        echo "=== ENCARGO MUERTO $(date '+%H:%M:%S') ==="
        echo "$peer: $dead / $ex -- el cron sigue vivo y ocioso. Reenvia con ID NUEVO o ESCALA."
        alerted[$peer]="$dead$ex"
      fi
    fi
  done
  sleep 120
done
```
**SEGUNDA CONDICION OBLIGATORIA (2026-08-18, falso positivo caro):** `RETRY_EXHAUSTED` **no
distingue** un encargo MUERTO de un encargo **CUMPLIDO y no marcado consumido**. Caso medido: r2 de
TASK-0394 se entrego (commit del maker) y se ruteo (mensaje al checker) ANTES del primer reintento;
los tres execs siguientes encontraron el trabajo hecho, salieron `transient` y agotaron los intentos.
Aplicar dos-vidas ahi habria duplicado trabajo cerrado. **Antes de reenviar, busca el ARTEFACTO DE
ENTREGA** (commit del maker o mensaje de handoff): si existe, NO esta muerto -- esta sin marcar, y lo
que toca es archivar el mensaje y desencolar su entrada del `retry.json`. Coste del falso positivo:
tres execs de peer.

**Y el punto ciego que NINGUN monitor cubre: el encargo que se esta MURIENDO.** Un `RETRY_DEFER` no
emite commits ni eventos, asi que los vigias ven el mismo silencio que "no hay trabajo". Solo se ve
leyendo el `retry.json` del peer y comparando su `defer_started_at + 7200s` contra los `expires_at`
de los claims que lo bloquean. **Metelo en el auto-poll de cada turno**: dos colisiones en un solo
dia se cazaron asi, con 66 y 27 minutos de margen.

**Politica del operador (17-ago): DOS VIDAS POR ORDEN.** Un reenvio automatico con **id NUEVO** y nota de la
causa; si el reenvio tambien muere, **ESCALADA al operador**. Nunca una tercera a ciegas. Y no atribuyas la
muerte a un incidente de proveedor sin mirar QUE CLI la emitio: el error de un proveedor no explica la caida
del exec del otro (me paso: culpe a un incidente ya resuelto y perdi el diagnostico real).

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

## 1h. Correcciones de campo a los watchdogs (2026-08-19, las tres costaron un diagnostico falso)

**(a) El monitor de entregas murio con `exit 255` sin stderr.** Endurecelo: `set +e` al inicio,
toda llamada a git tolerante (`cur=$(git rev-parse HEAD 2>/dev/null); [ -z "$cur" ] && cur="$base"`),
y **sustituye `comm -13 <(...) <(...)` por comparacion en shell puro** (`echo "$seen" | grep -qxF
"$f"`). La sustitucion de procesos es la sospechosa. Un monitor caido no avisa de que se cayo.

**(b) El patron del codigo de salida DEBE aceptar negativos:** `EXEC_EXIT code=-\?[0-9]\+`. Los
arneses usan **`code=-1`** para "lo mate yo", y `code=[0-9]*` casa la cadena VACIA -> el alerta sale
con `code=` a secas y la comparacion contra `"EXEC_EXIT code=0"` dispara siempre.

**(c) La condicion de artefacto se escribe por AUTORIA y se agrega por MENSAJE.** Buscar
`<peer>-to-Arquitecto` clasifico como MUERTA una entrega perfecta cuyo maker habia ruteado su review
**directo al checker**. Correcto: `^MSG-.*-<Peer>-to-` sobre todo `open/`, MAS commits suyos de las
ultimas 2 h, MAS el residuo sin commitear de `Area_comun/state/` y `runtime/state/` -- que es la
senal mas informativa de las tres, porque distingue "no hizo nada" de "hizo y no publico". Y
**agrega por MENSAJE, no por peon**: en la misma ventana un peer puede tener un encargo entregado y
otro muerto, y agregar por peon mezcla los dos destinos.

**Regla general: un vigia nuevo se estrena contra el caso que YA ocurrio**, no contra el que
imaginas. El v2 se valido re-clasificando correctamente el mismo evento que el v1 fallo.

## 1i. Cuando el checker se muere de hambre: el VEHICULO de review

Sintoma: el checker acumula `RETRY_DEFER ... reason=active_external_claim` y **nunca ejecuta**,
mientras el maker trabaja legitimamente. Causa: el arnes resuelve las rutas del encargo desde el
`.md` de **su** `task_id`, asi que una review que cita la tarea auditada hereda su `scope_routes` de
CODIGO (`scripts/`) y choca con el claim del maker. Y **el defer (7200 s) muere antes que cualquier
claim de exec largo**, asi que esperar no lo arregla: el 18-ago murieron TRES encargos asi, con 21
diferimientos y cero ejecuciones.

Remedio operativo, probado en campo: **registra una tarea-vehiculo** (`type: research`, owner del
checker, intake completo) cuyo `scope_routes` sea **lo que la review ESCRIBE** --
`Area_comun/artifacts/` -- y rutea la review citando ESE `task_id`. El juicio y su exigencia siguen
siendo los de la tarea auditada, y se dice dentro del mensaje junto con la causa de la muerte
anterior y la cuenta de vidas. **No uses `Area_comun/mailbox/open/` como ruta** si algun peer tiene
claim file-scoped sobre un MSG: un directorio solapa con un fichero suyo. Acreditado por EFECTO --
el checker arranco con los dos claims del maker ACTIVOS. El fix de RAIZ es TASK-0387; declara el
vehiculo como rodeo en su `out_of_scope`.
