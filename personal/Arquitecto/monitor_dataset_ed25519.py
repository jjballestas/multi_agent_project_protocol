import json, os, time, sys
P="runtime/state/events.jsonl"
THRESH_EVENTS=500
THRESH_AGENTS=2
def count():
    ed=0; per={}
    if not os.path.exists(P): return 0,per
    for l in open(P,encoding="utf-8"):
        l=l.strip()
        if not l: continue
        try: e=json.loads(l)
        except: continue
        if (e.get("actor_auth") or {}).get("method")=="ed25519":
            ed+=1; a=e.get("actor","?"); per[a]=per.get(a,0)+1
    return ed,per
while True:
    ed,per=count()
    # cross-signing (>=2 agentes) YA logrado 2026-06-27 (Arquitecto+Codex). Disparar solo por VOLUMEN.
    if ed>=THRESH_EVENTS and len(per)>=THRESH_AGENTS:
        print(f"THRESHOLD MET: {ed} ed25519 events across {len(per)} agents {per}")
        sys.exit(0)
    time.sleep(300)
