#!/bin/bash
# VIGIA 2 -- EXEC-HEALTH. Muerde cuando un exec de peon esta retenido: lock tomado
# y heartbeat EXEC_RUNNING congelado > 300 s. La liveness se mide por el LOG DE ESTE
# ROOT, no por el listado de procesos: la instancia NOVA corre crons con el MISMO
# -PeerId desde otra raiz y un detector por nombre de proceso NO discrimina.
. /d/Agentes/multi_agent_project_protocol/personal/Arquitecto/watchdogs/lib-comun.sh
cd "$ROOT" || exit 1
declare -A dicho
while true; do
  for p in codex analista; do
    d="$ROOT/.protocol-tmp/${p}_mailbox_cron"
    logf="$d/${p}_mailbox_cron.log"
    [ -f "$logf" ] || continue
    est=$(peer_vivo "$p")
    now=$(date +%s)
    lmt=$(stat -c %Y "$logf" 2>/dev/null || echo "$now")
    edad=$(( now - lmt ))
    # Ultimo latido de exec en la cola del log (ventana de 200 lineas).
    hb=$(tail -200 "$logf" 2>/dev/null | grep -E 'EXEC_RUNNING|EXEC_START' | tail -1 || true)
    fin=$(tail -200 "$logf" 2>/dev/null | grep -E 'EXEC_DONE|OUTCOME:|TREE_KILL|Heartbeat processable' | tail -1 || true)
    if [ -n "$hb" ] && [ -z "$fin" ] && [ "$edad" -gt 300 ]; then
      k="hb-$p-$hb"
      if [ -z "${dicho[$k]}" ]; then
        dicho[$k]=1
        echo "ALERTA exec-health $p: heartbeat congelado ${edad}s -- ultimo: $hb"
      fi
    fi
    # Lease/lock retenido con el cron no-vivo = exec huerfano.
    lease=$(ls "$d"/*.lease* "$d"/*lock* 2>/dev/null | head -1 || true)
    if [ -n "$lease" ] && [ "$est" != "vivo" ]; then
      k="lock-$p-$(stat -c %Y "$lease" 2>/dev/null || echo 0)"
      if [ -z "${dicho[$k]}" ]; then
        dicho[$k]=1
        echo "ALERTA exec-health $p: lock/lease retenido y su cron NO esta vivo ($est) -- $lease"
      fi
    fi
    # Encargos esperando con el cron muerto: nadie los va a tomar.
    n=$(ls "$ROOT/Area_comun/mailbox/open/" 2>/dev/null | grep -icE "^MSG-.*-to-${p}-" || true)
    if [ "${n:-0}" -gt 0 ] && [ "$est" != "vivo" ]; then
      k="cola-$p-$n"
      if [ -z "${dicho[$k]}" ]; then
        dicho[$k]=1
        echo "ALERTA exec-health $p: $n encargo(s) en open/ y su cron NO esta vivo ($est) -- nadie los va a tomar"
      fi
    fi
  done
  sleep "${ARQ_INTERVALO_EH:-180}"
done
