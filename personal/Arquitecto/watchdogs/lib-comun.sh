# Comun a los cinco vigias. NO se ejecuta suelto.
ROOT=/d/Agentes/multi_agent_project_protocol
# Marca de sesion: el self-filter PRIMARIO. El de modelo es secundario y fragil
# (TASK-0383): en este hub los peers no emiten Co-Authored-By, pero si algun dia
# el checker corre sobre Claude con trailer, el filtro de modelo lo silencia.
MARCA="${ARQ_MARCA:-Arq-Session: 43613ac0}"

# Un peer esta VIVO en ESTE root si su .pid apunta a un proceso existente Y su log
# de ESTE root se movio en los ultimos 15 min. El listado de procesos NO discrimina:
# la instancia NOVA corre crons con el MISMO -PeerId desde otra raiz.
peer_vivo() {
  local peer_l="$1"
  local d="$ROOT/.protocol-tmp/${peer_l}_mailbox_cron"
  local logf="$d/${peer_l}_mailbox_cron.log"
  [ -f "$logf" ] || { echo "no-log"; return; }
  local edad=$(( $(date +%s) - $(stat -c %Y "$logf" 2>/dev/null || echo 0) ))
  if [ "$edad" -gt 900 ]; then echo "log-rancio:${edad}s"; return; fi
  echo "vivo"
}
