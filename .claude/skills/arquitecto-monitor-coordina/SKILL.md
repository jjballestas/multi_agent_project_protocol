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
- **Auto-ruido:** sin el self-filter, el monitor se dispara con tus propios commits. El filtro `Co-Authored-By:
  Claude Opus` los descarta (verificado: tus commits lo llevan, los de Codex/Analista no).
- **2+ timeouts seguidos con crons vivos** = cron atascado (lock/proceso huerfano). NO es "nada que hacer": diagnostica
  y destraba -> skill `arquitecto-cron-lifecycle`.
- **Arbol compartido:** peers commitean aqui; `git merge --ff-only` cada wake; `git pull --rebase --autostash` si el
  push sale non-ff. Vi gates en rojo TRANSITORIO por un peer a mitad de escritura -> re-correr hasta verde.
- **Trigger diferido:** si el operador pide "promover X luego de que Codex termine su cola", vigila via el monitor
  hasta que Codex quede sin pendientes y recien ahi promueve X.

## Checklist de una linea
Arma monitor self-filter -> wake con peer -> fetch+ff -> reacciona (GO=ratifico+done-flip / NO-GO=remediacion /
entrega=REVIEW / done=promuevo siguiente / rr=respondo) -> gate exit-code -> commit+push -> re-arma monitor.
Complementa: arquitecto-ledger-ops (recetas submit_intent), arquitecto-cron-lifecycle (cron atascado), mailbox-hygiene.
