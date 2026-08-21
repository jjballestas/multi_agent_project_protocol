#!/bin/bash
# VIGIA 4 -- ENCARGO MUERTO. Agrega POR MENSAJE, nunca por peon: dos encargos del
# mismo peer pueden tener destinos opuestos en la misma ventana.
# Tres correcciones ya pagadas:
#  (a) el patron de codigo de salida es `-\?[0-9]\+` -- los arneses usan `-1`;
#  (b) la condicion de artefacto se escribe por AUTORIA (`^MSG-.*-<Peer>-to-`), no
#      por destinatario, o una entrega perfecta se clasifica como muerte;
#  (c) `defer_terminal` NO consume un intento: MATA la entrada entera, y no emite
#      commit ni evento -- por eso aqui se lee el retry.json, no solo el log.
. /d/Agentes/multi_agent_project_protocol/personal/Arquitecto/watchdogs/lib-comun.sh
cd "$ROOT" || exit 1
WD="$ROOT/personal/Arquitecto/watchdogs"
declare -A dicho
while true; do
  for p in codex analista; do
    if [ "$p" = "codex" ]; then P=Codex; else P=Analista; fi
    d="$ROOT/.protocol-tmp/${p}_mailbox_cron"
    logf="$d/${p}_mailbox_cron.log"
    if [ -f "$logf" ]; then
      tail -60 "$logf" 2>/dev/null | grep -E 'RETRY_EXHAUSTED|defer_terminal|exit_code=-\?[0-9]\+|code=-\?[0-9]\+' > /tmp/.wd4.$p 2>/dev/null || true
      while IFS= read -r linea; do
        [ -z "$linea" ] && continue
        msg=$(printf '%s' "$linea" | grep -oE 'MSG-[A-Za-z0-9._-]+' | head -1 || true)
        h=$(printf '%s' "$linea" | md5sum | cut -c1-8)
        k="log-$P-${msg:-sinid}-$h"
        [ -n "${dicho[$k]}" ] && continue
        dicho[$k]=1
        art=$(ls "$ROOT/Area_comun/mailbox/open/" 2>/dev/null | grep -cE "^MSG-.*-${P}-to-" || true)
        com=$(git log --oneline -8 --author="$P" 2>/dev/null | wc -l || true)
        echo "ALERTA encargo-muerto $P [${msg:-sin-id}]: $linea"
        echo "    artefacto por AUTORIA de $P: ${art:-0} MSG en open/, ${com:-0} commits recientes -- si >0, verifica COMPLETITUD antes de dar por muerto el encargo"
      done < /tmp/.wd4.$p
    fi
    rj="$d/${p}_mailbox_cron.retry.json"
    if [ -f "$rj" ]; then
      python "$WD/lee-retry.py" "$rj" > /tmp/.wd4rj.$p 2>/dev/null || true
      while IFS= read -r fila; do
        [ -z "$fila" ] && continue
        k="rj-$P-$fila"
        [ -n "${dicho[$k]}" ] && continue
        dicho[$k]=1
        echo "ALERTA encargo-muerto $P (retry.json, muerte SILENCIOSA que ningun monitor de eventos ve): $fila"
      done < /tmp/.wd4rj.$p
    fi
  done
  sleep "${ARQ_INTERVALO_EM:-180}"
done
