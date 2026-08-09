#!/usr/bin/env bash
# Devuelve 0 si es seguro commitear, 1 si hay que esperar.
#
#   bash personal/Arquitecto/guard-commit-si-peer-trabaja.sh          # comprueba una vez
#   bash personal/Arquitecto/guard-commit-si-peer-trabaja.sh --wait   # espera hasta que sea seguro
#   bash personal/Arquitecto/guard-commit-si-peer-trabaja.sh --deliver # ignora "correo pendiente"
#
# --deliver es para EL commit que entrega el mensaje: si bloqueara por correo pendiente, el commit
# que crea el mensaje no podria hacerse nunca. Sigue bloqueando por exec vivo y por reintento.
#
# POR QUE MIRA MAS QUE EL EXEC (2026-08-10, carrera real):
# la version anterior solo miraba si habia un exec CORRIENDO. Comprobe "ningun peer en exec",
# arranco un reintento en los segundos siguientes, y mi commit lo mato con head_changed.
# Un exec no empieza porque si: empieza cuando el peer TIENE TRABAJO. Asi que el predicado no es
# "hay un exec" sino "puede haberlo antes de que yo termine": exec vivo, reintento pendiente, o
# mensaje suyo sin consumir en open/. Mismo principio que le exijo a los contratos: no mirar el
# sintoma (una linea de log) sino la condicion que lo causa.
cd "$(dirname "$0")/../.." || exit 2

check() {
  reasons=""
  for a in codex analista; do
    peer=$(printf '%s' "$a" | sed 's/^./\U&/')
    L=".protocol-tmp/${a}_mailbox_cron/${a}_mailbox_cron.log"
    R=".protocol-tmp/${a}_mailbox_cron/${a}_mailbox_cron.retry.json"

    # 1. exec vivo
    if [ -f "$L" ]; then
      last=$(tail -1 "$L")
      case "$last" in
        *EXEC_RUNNING*|*EXEC_PROGRESSING*|*EXEC_START*|*POST_DELIVERY_WINDOW_START*)
          el=$(printf '%s' "$last" | grep -oE 'elapsed=[0-9]+' | cut -d= -f2)
          reasons="$reasons ${a}:exec(${el:-0}s)" ;;
      esac
    fi

    # 2. reintento pendiente (arranca solo en el siguiente ciclo)
    if [ -f "$R" ]; then
      n=$(python -c "
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: d={}
# Solo cuenta reintentos de execs que YA CORRIERON y fallaron (attempts>0).
# Una entrada 'deferred' con attempts==0 es un pre-exec defer: el exec NO arranco, asi que
# commitear no puede matarlo -- y muchas veces el defer lo causa justo mi arbol sucio, con lo
# que bloquear ahi es un abrazo mortal. (Medido el 2026-08-10.)
print(sum(1 for v in d.values() if isinstance(v,dict) and not v.get('exhausted') and int(v.get('attempts') or 0) > 0))
" "$R" 2>/dev/null)
      [ "${n:-0}" -gt 0 ] 2>/dev/null && reasons="$reasons ${a}:reintento($n)"
    fi

    # 3. correo suyo sin consumir: es lo que DISPARA el exec
    if [ "$DELIVER" != "1" ]; then
      m=$(grep -lE "^to: ${peer}$" Area_comun/mailbox/open/MSG-*.md 2>/dev/null | wc -l | tr -d ' ')
      [ "${m:-0}" -gt 0 ] 2>/dev/null && reasons="$reasons ${a}:correo($m)"
    fi
  done
  [ -z "$reasons" ]
}

DELIVER=0
[ "$1" = "--deliver" ] && DELIVER=1
[ "$2" = "--deliver" ] && DELIVER=1

if [ "$1" = "--wait" ]; then
  for _ in $(seq 1 240); do
    if check; then echo "seguro: peers sin trabajo pendiente"; exit 0; fi
    sleep 15
  done
  echo "TIMEOUT esperando ventana:$reasons"; exit 1
fi

if check; then echo "seguro: peers sin trabajo pendiente"; exit 0; fi
echo "NO COMMITEAR --$reasons"
exit 1
