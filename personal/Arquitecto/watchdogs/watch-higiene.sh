#!/bin/bash
# VIGIA 3 -- HIGIENE. open/ >= 10, mas los gates que frenan las dos colas.
. /d/Agentes/multi_agent_project_protocol/personal/Arquitecto/watchdogs/lib-comun.sh
cd "$ROOT" || exit 1
declare -A dicho
while true; do
  n=$(ls "$ROOT/Area_comun/mailbox/open/" 2>/dev/null | grep -c '^MSG-' || true)
  if [ "${n:-0}" -ge 10 ]; then
    k="open-$n"
    if [ -z "${dicho[$k]}" ]; then dicho[$k]=1
      echo "ALERTA higiene: open/ con $n mensajes -- toca archivar lo consumido (DECISION-0120: higiene -> no rutear -> podar)"
    fi
  fi
  # validate: se CONFIRMA en dos lecturas antes de gritar (un rojo transitorio por
  # el .ledger.lock de un submit no es un rojo real).
  python scripts/validate_collaboration_state.py >/dev/null 2>&1; v1=$?
  if [ "$v1" -ne 0 ]; then
    sleep 20
    python scripts/validate_collaboration_state.py >/dev/null 2>&1; v2=$?
    if [ "$v2" -ne 0 ]; then
      k="val-$(git rev-parse --short HEAD 2>/dev/null || echo x)"
      if [ -z "${dicho[$k]}" ]; then dicho[$k]=1
        echo "ALERTA higiene: validate_collaboration_state en $v2 CONFIRMADO en dos lecturas"
      fi
    fi
  fi
  python scripts/scan_encoding.py >/dev/null 2>&1; e1=$?
  if [ "$e1" -ne 0 ]; then
    k="enc-$(git rev-parse --short HEAD 2>/dev/null || echo x)"
    if [ -z "${dicho[$k]}" ]; then dicho[$k]=1
      echo "ALERTA higiene: scan_encoding en $e1 -- byte no ASCII en rutas gobernadas"
    fi
  fi
  # Poda vencida.
  if [ -f scripts/prune_state.py ]; then
    python scripts/prune_state.py --check >/dev/null 2>&1; p=$?
    if [ "$p" -ne 0 ]; then
      k="poda-$(date +%Y%m%d%H)"
      if [ -z "${dicho[$k]}" ]; then dicho[$k]=1
        echo "ALERTA higiene: prune_state --check en $p -- poda vencida"
      fi
    fi
  fi
  sleep "${ARQ_INTERVALO_HI:-300}"
done
