#!/bin/bash
# VIGIA 5 -- ENCARGO QUE NO ARRANCA. Un MSG dirigido a un peer que lleva >12 min en
# open/ sin EXEC_START y sin entrada en su seen.json. Distingue "no arranca" de
# "diferido" leyendo el retry.json: un diferido SI fue visto y tiene motivo; el que
# no arranca es invisible para el arnes y muere sin dejar rastro.
. /d/Agentes/multi_agent_project_protocol/personal/Arquitecto/watchdogs/lib-comun.sh
cd "$ROOT" || exit 1
declare -A dicho
while true; do
  now=$(date +%s)
  for p in codex analista; do
    if [ "$p" = "codex" ]; then P=Codex; else P=Analista; fi
    d="$ROOT/.protocol-tmp/${p}_mailbox_cron"
    seenf="$d/${p}_mailbox_cron.seen.json"
    rj="$d/${p}_mailbox_cron.retry.json"
    logf="$d/${p}_mailbox_cron.log"
    for f in "$ROOT"/Area_comun/mailbox/open/MSG-*-to-${P}-*.md; do
      [ -f "$f" ] || continue
      m=$(basename "$f")
      mt=$(stat -c %Y "$f" 2>/dev/null || echo "$now")
      edad=$(( (now - mt) / 60 ))
      [ "$edad" -lt 12 ] && continue
      visto=no; difer=no; arranco=no
      [ -f "$seenf" ] && grep -qF "$m" "$seenf" 2>/dev/null && visto=si
      [ -f "$rj" ] && grep -qF "$m" "$rj" 2>/dev/null && difer=si
      [ -f "$logf" ] && grep -qF "$m" "$logf" 2>/dev/null && arranco=si
      [ "$visto" = "si" ] && [ "$arranco" = "si" ] && continue
      k="na-$m-$edad"
      kk="na-$m"
      [ -n "${dicho[$kk]}" ] && continue
      dicho[$kk]=1
      if [ "$difer" = "si" ]; then
        echo "AVISO no-arranca $P [$m]: ${edad} min en open/, DIFERIDO (aparece en retry.json) -- no es invisible, tiene motivo; lee su defer_reason"
      else
        est=$(peer_vivo "$p")
        echo "ALERTA no-arranca $P [$m]: ${edad} min en open/, sin EXEC_START, sin entrada en seen.json y SIN diferimiento -- el arnes no lo ve (cron: $est). Revisa task_id TASK-NNNN real, su fila en el indice y el bloque scope_routes"
      fi
    done
  done
  sleep "${ARQ_INTERVALO_NA:-240}"
done
