#!/usr/bin/env bash
# Devuelve 0 si es seguro commitear (ningun peer en exec), 1 si hay que esperar.
# Uso:  bash personal/Arquitecto/guard-commit-si-peer-trabaja.sh || echo "ESPERA"
cd "$(dirname "$0")/../.." || exit 2
busy=""
for a in codex analista; do
  L=".protocol-tmp/${a}_mailbox_cron/${a}_mailbox_cron.log"
  [ -f "$L" ] || continue
  last=$(tail -1 "$L")
  case "$last" in
    *EXEC_RUNNING*|*EXEC_PROGRESSING*|*POST_DELIVERY_WINDOW_START*)
      el=$(printf '%s' "$last" | grep -oE 'elapsed=[0-9]+' | cut -d= -f2)
      busy="$busy $a(${el:-?}s)" ;;
  esac
done
if [ -n "$busy" ]; then
  echo "NO COMMITEAR -- peer en exec:$busy"
  exit 1
fi
echo "seguro: ningun peer en exec"
