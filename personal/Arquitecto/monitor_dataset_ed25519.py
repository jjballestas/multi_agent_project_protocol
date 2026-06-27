import json, os, time, sys
# Monitor del dataset TFM -- SOLO cuenta eventos ELEGIBLES (no observa H1-H3; evita peeking, V4).
# Ventana elegible (baseline canonico unico): turnos gobernados cruzado-firmados Ed25519 con seq >= DATASET_START_SEQ.
P="runtime/state/events.jsonl"
DATASET_START_SEQ=2221   # atestado: primer evento elegible tras el baseline (seq 2220 = construccion del aparato)
THRESH_EVENTS=500        # N (stop-rule: primeros 500 elegibles desde DATASET_START_SEQ)
THRESH_AGENTS=2
def count():
    ed=0; per={}
    if not os.path.exists(P): return 0,per
    for l in open(P,encoding="utf-8"):
        l=l.strip()
        if not l: continue
        try: e=json.loads(l)
        except: continue
        if e.get("seq",0) < DATASET_START_SEQ: continue   # EXCLUSION pre-baseline
        if (e.get("actor_auth") or {}).get("method")=="ed25519":
            ed+=1; a=e.get("actor","?"); per[a]=per.get(a,0)+1
    return ed,per
while True:
    ed,per=count()
    if ed>=THRESH_EVENTS and len(per)>=THRESH_AGENTS:
        print(f"STOP-RULE: {ed} eventos elegibles (>= {THRESH_EVENTS}) desde seq {DATASET_START_SEQ}, {len(per)} agentes {per}. CERRAR VENTANA (no mirar H1-H3 antes).")
        sys.exit(0)
    time.sleep(300)
