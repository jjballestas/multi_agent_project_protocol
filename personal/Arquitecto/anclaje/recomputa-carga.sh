#!/bin/bash
# Re-computo INDEPENDIENTE de la carga de anclaje de una unidad N=6.
# No consume los numeros declarados por NOVA: los recalcula y luego los compara.
# Todo sobre el COMMIT (git cat-file blob), nunca sobre el arbol de trabajo.
# NOTA: recomputa hashes sobre el COMMIT, identicos aqui o en un clon. NO sustituye al clon
# limpio: la ceremonia completa exige ademas correr el validate de NOVA sobre un clon fresco
# antes de escribir la entrada.
#   uso: recomputa-carga.sh <commit> <TASK-94xx> [ruta-repo-nova]
set -u
COMMIT="${1:?falta el commit de NOVA.git}"
TASK="${2:?falta el id de la unidad, p.ej. TASK-9402}"
NOVA="${3:-/d/Agentes/NOVA-Suite/NOVA}"
EV="Aegis/runtime/state/events.jsonl"
TMP=D:/Aegis_Scratch/protocol/anclaje
mkdir -p "$TMP" 2>/dev/null
CFG="Aegis/protocol.config.json"
MED="Aegis/Area_comun/artifacts/MEDICION-${TASK}.md"

cd "$NOVA" || { echo "ERROR: no existe el repo $NOVA"; exit 1; }
git cat-file -e "${COMMIT}^{commit}" 2>/dev/null || { echo "ERROR: commit $COMMIT no existe en $NOVA"; exit 1; }

echo "nova_commit            $(git rev-parse "$COMMIT")"

# --- events.jsonl: hash del BLOB, no del fichero del arbol
if ! git cat-file -e "${COMMIT}:${EV}" 2>/dev/null; then
  echo "ERROR: $EV AUSENTE en ese commit"; exit 1
fi
git cat-file blob "${COMMIT}:${EV}" > D:/Aegis_Scratch/protocol/anclaje/.anc-ev.jsonl 2>/dev/null
echo "sha256_events_jsonl    $(sha256sum D:/Aegis_Scratch/protocol/anclaje/.anc-ev.jsonl | cut -d' ' -f1)"

python - <<'PY'
import json
n = 0
last = None
for line in open('D:/Aegis_Scratch/protocol/anclaje/.anc-ev.jsonl', encoding='utf-8'):
    if line.strip():
        n += 1
        last = line
e = json.loads(last)
import hashlib
print("event_count            %d" % n)
print("head_seq               %s" % e.get('seq'))
print("head_prev_hash         %s" % (e.get('prev_hash') or e.get('prev') or 'NO-DECLARADO'))
# la linea de cabeza se hashea TAL CUAL viaja en el fichero, sin el salto final
# La convencion del salto final NO esta fijada entre las dos instancias: se emiten LAS DOS,
# para que una discrepancia solo por ese byte no se confunda con una anomalia real.
NL = chr(10)
sin = last[:-1] if last.endswith(NL) else last
# La convencion del salto final no esta fijada entre las dos instancias: se emiten LAS DOS,
# para que una discrepancia solo por ese byte no se confunda con una anomalia real.
print("sha256_head_line       %s   (sin salto final)" % hashlib.sha256(sin.encode("utf-8")).hexdigest())
print("sha256_head_line_nl    %s   (con salto final)" % hashlib.sha256(last.encode("utf-8")).hexdigest())
PY

# --- config epoch: sha8 del BLOB en LF
if git cat-file -e "${COMMIT}:${CFG}" 2>/dev/null; then
  git cat-file blob "${COMMIT}:${CFG}" > D:/Aegis_Scratch/protocol/anclaje/.anc-cfg.json
  SHA=$(sha256sum D:/Aegis_Scratch/protocol/anclaje/.anc-cfg.json | cut -d' ' -f1)
  echo "config_epoch_sha8      $(printf '%s' "${SHA:0:8}" | tr 'a-f' 'A-F')"
else
  echo "config_epoch_sha8      AUSENTE EN ESE COMMIT"
fi

# --- artefacto de medicion de la unidad: guarda de AUSENTE, igual que la suya
if git cat-file -e "${COMMIT}:${MED}" 2>/dev/null; then
  git cat-file blob "${COMMIT}:${MED}" > D:/Aegis_Scratch/protocol/anclaje/.anc-med.md
  echo "artefacto_medicion     ${MED}"
  echo "sha256_medicion        $(sha256sum D:/Aegis_Scratch/protocol/anclaje/.anc-med.md | cut -d' ' -f1)"
else
  echo "artefacto_medicion     AUSENTE EN ESE COMMIT  <-- carga INCOMPLETA, no anclar"
fi

# --- instrumentacion F3.3: cuenta los eventos que el sello exige (s.9 p.5)
python - <<'PY'
import json, collections
c = collections.Counter()
for line in open('D:/Aegis_Scratch/protocol/anclaje/.anc-ev.jsonl', encoding='utf-8'):
    if not line.strip():
        continue
    e = json.loads(line)
    p = e.get('payload', {})
    c[str(p.get('intent_type') or e.get('type'))] += 1
tres = ('cost.attributed', 'defect.reported', 'manual.intervention')
print("instrumentacion_F33    " + "  ".join("%s=%d" % (t, c.get(t, 0)) for t in tres))
if all(c.get(t, 0) == 0 for t in tres):
    print("                       AVISO: cero eventos de instrumentacion -- la medicion de esta")
    print("                       unidad NO sale del ledger. Sello s.9 p.5.")
PY
rm -f D:/Aegis_Scratch/protocol/anclaje/.anc-ev.jsonl D:/Aegis_Scratch/protocol/anclaje/.anc-cfg.json D:/Aegis_Scratch/protocol/anclaje/.anc-med.md
