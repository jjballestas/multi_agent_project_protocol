#!/bin/bash
# VIGIA 1 -- ENTREGAS. Tres senales: MSG nuevo a-Arquitecto en open/, commit nuevo
# en HEAD LOCAL (los peers commitean sin pushear), y avance de origin/main.
# Self-filter: marca de sesion PROPIA (primaria) + trailer de modelo de los TRES
# modelos + asesor (secundaria). Todas las llamadas a git van con `|| true` y NO se
# usa `comm` con sustitucion de procesos: la v1 murio con exit 255 sin stderr.
. /d/Agentes/multi_agent_project_protocol/personal/Arquitecto/watchdogs/lib-comun.sh
cd "$ROOT" || exit 1
COP="$ROOT/personal/Arquitecto/watchdogs/mail-copias"
mkdir -p "$COP" 2>/dev/null
base=$(git rev-parse HEAD 2>/dev/null || true)
obase=$(git rev-parse origin/main 2>/dev/null || true)
vistos=$(ls "$ROOT/Area_comun/mailbox/open/" 2>/dev/null | grep '^MSG-' | sort || true)
anunciados=""
ciclo=0
propio() {  # 0 = es mio (callar), 1 = ajeno (anunciar)
  local c="$1" cuerpo subj
  cuerpo=$(git log -1 --format='%B' "$c" 2>/dev/null || true)
  subj=$(git log -1 --format='%s' "$c" 2>/dev/null || true)
  printf '%s' "$cuerpo" | grep -qF "$MARCA" && return 0
  printf '%s' "$cuerpo" | grep -qE 'Co-Authored-By: Claude[^<]*(Opus|Fable|Sonnet)' && return 0
  printf '%s' "$cuerpo" | grep -qiE 'Co-Authored-By: *asesor' && return 0
  printf '%s' "$subj" | grep -qE '^checkpoint\(asesor\)' && return 0
  return 1
}
while true; do
  ahora=$(ls "$ROOT/Area_comun/mailbox/open/" 2>/dev/null | grep '^MSG-' | sort || true)
  while IFS= read -r m; do
    [ -z "$m" ] && continue
    printf '%s\n' "$vistos" | grep -qxF "$m" && continue
    # La copia se hace SIEMPRE (tambien de los mios): un archivado o un rollback
    # se lleva el fichero en segundos.
    cp -f "$ROOT/Area_comun/mailbox/open/$m" "$COP/$m" 2>/dev/null || true
    # Solo se ANUNCIA lo ajeno. El emisor es el campo 3 del nombre; se extrae por
    # campo, nunca con un comodin que se trague el nombre del emisor.
    [ "$(printf '%s' "$m" | cut -d- -f3)" = "Arquitecto" ] && continue
    echo "ENTREGA MSG: $m (copia en mail-copias)"
  done <<< "$ahora"
  vistos="$ahora"

  cur=$(git rev-parse HEAD 2>/dev/null || true)
  if [ -n "$cur" ] && [ "$cur" != "$base" ]; then
    for c in $(git rev-list --reverse "${base}..${cur}" 2>/dev/null || true); do
      propio "$c" && continue
      case " $anunciados " in *" $c "*) continue ;; esac
      anunciados="$anunciados $c"
      echo "ENTREGA COMMIT: $(git log -1 --oneline "$c" 2>/dev/null || true)"
    done
    base=$cur
  fi

  ciclo=$((ciclo+1))
  if [ $((ciclo % 4)) -eq 0 ]; then
    git fetch -q origin 2>/dev/null || true
    ocur=$(git rev-parse origin/main 2>/dev/null || true)
    if [ -n "$ocur" ] && [ "$ocur" != "$obase" ]; then
      # Self-filter TAMBIEN aqui y por RANGO, no por la punta: un push ajeno puede
      # aterrizar por debajo del mio.
      for c in $(git rev-list --reverse "${obase}..${ocur}" 2>/dev/null || true); do
        propio "$c" && continue
        case " $anunciados " in *" $c "*) continue ;; esac
        anunciados="$anunciados $c"
        echo "ORIGIN/MAIN avanzo: $(git log -1 --oneline "$c" 2>/dev/null || true)"
      done
      obase=$ocur
    fi
  fi
  sleep "${ARQ_INTERVALO:-30}"
done
