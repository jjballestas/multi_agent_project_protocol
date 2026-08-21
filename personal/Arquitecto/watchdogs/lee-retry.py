# Lee un retry.json de peon y emite UNA linea por entrada MUERTA o casi-muerta.
# `defer_terminal` agota la entrada entera: `attempts=N` junto a `exhausted:true`
# lee al reves de lo que significa.
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception:
    sys.exit(0)
if not isinstance(d, dict):
    sys.exit(0)
for k, v in d.items():
    if not isinstance(v, dict):
        continue
    ex = str(v.get('exhausted', '')).lower() == 'true'
    out = str(v.get('outcome', ''))
    defs = v.get('defers', 0)
    if ex or out == 'defer_terminal' or (isinstance(defs, int) and defs >= 15):
        print("%s exhausted=%s outcome=%s defers=%s reason=%s"
              % (k, ex, out, defs, v.get('defer_reason', '')))
