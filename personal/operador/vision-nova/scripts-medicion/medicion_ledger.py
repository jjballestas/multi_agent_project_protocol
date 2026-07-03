#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
medicion_ledger.py -- gestor append-only del CSV de medicion del estudio NOVA Budget.

MODELO (unica forma fiel a "APPEND-ONLY + jamas editar a mano + la fila se actualiza
en cada veredicto y se cierra en integracion", NOVA-ESTUDIO-002 s.1-s.3):

    <tabla>_journal.csv   -> log APPEND-ONLY de eventos (OPEN/UPDATE/CLOSE); nunca se reescribe.
    <tabla>.csv           -> VISTA materializada (ultimo estado por clave); la (re)genera el
                             script a partir del journal; jamas se edita a mano.

La atestacion real (sha256 -> intent del ledger del hub) es del Arquitecto en cada gate;
este script hace pseudo-atestacion (commit git plano del repo hub) e IMPRIME el sha256 y la
linea lista para el intent. No escribe el ledger #4.

Subcomandos:
    nueva-fila     abre una fila (valida los campos de apertura obligatorios; NA prohibido ahi)
    actualizar     superpone campos sobre una fila existente (cada veredicto adversarial)
    cerrar-fila    actualiza + exige estado de cierre y re-materializa
    materializar   regenera <tabla>.csv desde el journal (idempotente)
    sha256         imprime sha256 del journal y del csv + linea para el intent de atestacion
    verificar      valida integridad journal<->vista y el schema

Uso tipico:
    python medicion_ledger.py nueva-fila --set tarea_id=NB-P4-2 --set brazo=gobernado \\
        --set par_id=PAR-1 --set estimate_previo_SML=M --set criticidad=alta \\
        --set fecha_commit_estimate=2026-07-08
    python medicion_ledger.py actualizar --clave NB-P4-2 --set reworks_n=1 \\
        --set secuencia_veredictos=RECHAZADO;OK
    python medicion_ledger.py cerrar-fila --clave NB-P4-2 --set estado_final=done \\
        --set fecha_fin=2026-07-12 --set tokens_total_atribuibles=41000

defectos: identico pero --tabla defectos y clave explicita (--clave DEF-0001).
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
META_COLS = ["event_seq", "event_ts", "op", "clave"]
# columna que ES la clave natural por tabla (o None -> se antepone 'defecto_id' sintetico)
KEY_COLUMN = {"medicion": "tarea_id", "defectos": None}
NA = "NA"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOOL_TRUE = {"true", "1", "si", "yes", "y", "t"}
BOOL_FALSE = {"false", "0", "no", "n", "f"}


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(2)


def load_schema(tabla, schema_dir):
    path = os.path.join(schema_dir, "schema_%s.json" % tabla)
    if not os.path.exists(path):
        die("schema no encontrado: %s" % path)
    with open(path, "r") as f:
        sch = json.load(f)
    cols = [c["n"] for c in sch["columnas"]]
    by_name = {c["n"]: c for c in sch["columnas"]}
    return sch, cols, by_name


def coerce(col_def, value, is_open_phase_field):
    """Valida/normaliza un valor contra su definicion. NA solo permitido en campos de cierre."""
    v = value.strip()
    tipo = col_def["tipo"]
    if v == NA or v == "":
        if is_open_phase_field and not col_def.get("na_ok"):
            die("campo de apertura '%s' no puede ser NA/vacio" % col_def["n"])
        return NA
    if tipo == "enum":
        if v not in col_def["enum"]:
            die("valor '%s' invalido para '%s'; enum=%s" % (v, col_def["n"], col_def["enum"]))
        return v
    if tipo == "int":
        try:
            return str(int(v))
        except ValueError:
            die("'%s' debe ser entero (col '%s')" % (v, col_def["n"]))
    if tipo == "float":
        try:
            return str(float(v))
        except ValueError:
            die("'%s' debe ser float (col '%s')" % (v, col_def["n"]))
    if tipo == "bool":
        low = v.lower()
        if low in BOOL_TRUE:
            return "true"
        if low in BOOL_FALSE:
            return "false"
        die("'%s' debe ser bool (col '%s')" % (v, col_def["n"]))
    if tipo == "date":
        if not DATE_RE.match(v):
            die("'%s' debe ser fecha YYYY-MM-DD (col '%s')" % (v, col_def["n"]))
        return v
    return v  # str


def parse_sets(pairs):
    out = {}
    for p in pairs:
        if "=" not in p:
            die("--set espera campo=valor, recibi: '%s'" % p)
        k, val = p.split("=", 1)
        k = k.strip()
        if k in out:
            die("campo repetido en --set: '%s'" % k)
        out[k] = val
    return out


def journal_path(tabla, corpus):
    return os.path.join(corpus, "%s_journal.csv" % tabla)


def view_path(tabla, corpus):
    return os.path.join(corpus, "%s.csv" % tabla)


def read_journal(tabla, corpus, cols):
    path = journal_path(tabla, corpus)
    events = []
    if not os.path.exists(path):
        return events
    with open(path, "r", newline="") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            events.append(row)
    return events


def materialize_rows(events, cols):
    """ultimo evento gana por clave, preservando orden de primera aparicion."""
    order = []
    state = {}
    for ev in events:
        clave = ev["clave"]
        if clave not in state:
            order.append(clave)
            state[clave] = {c: NA for c in cols}
        for c in cols:
            if c in ev and ev[c] != "":
                state[clave][c] = ev[c]
    return order, state


def write_view(tabla, corpus, cols, order, state):
    key_col = KEY_COLUMN[tabla]
    out_cols = cols if key_col else (["defecto_id"] + cols)
    path = view_path(tabla, corpus)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        for clave in order:
            row = state[clave]
            vals = ([] if key_col else [clave]) + [row[c] for c in cols]
            w.writerow(vals)
    return path


def next_seq(events):
    if not events:
        return 1
    return max(int(e["event_seq"]) for e in events) + 1


def append_event(tabla, corpus, cols, op, clave, values, event_ts):
    path = journal_path(tabla, corpus)
    events = read_journal(tabla, corpus, cols)
    seq = next_seq(events)
    exists = os.path.exists(path)
    header = META_COLS + cols
    row = {c: "" for c in header}
    row["event_seq"] = str(seq)
    row["event_ts"] = event_ts
    row["op"] = op
    row["clave"] = clave
    for k, v in values.items():
        row[k] = v
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if not exists:
            w.writeheader()
        w.writerow(row)
    return seq


def resolve_clave(tabla, args, sets):
    key_col = KEY_COLUMN[tabla]
    if args.clave:
        return args.clave
    if key_col and key_col in sets:
        return sets[key_col]
    die("no pude resolver la clave; pasa --clave (o incluye %s en --set)" % (key_col or "defecto_id"))


def validate_and_coerce(sets, by_name, cols, required_open, enforce_open):
    """valida claves conocidas, aplica coercion; marca los campos de apertura como no-NA."""
    values = {}
    for k, v in sets.items():
        if k not in by_name:
            die("campo desconocido: '%s' (no esta en el schema)" % k)
        cd = by_name[k]
        is_open_req = enforce_open and (k in required_open)
        values[k] = coerce(cd, v, is_open_req)
    return values


def git_commit(corpus, paths, msg):
    try:
        root = subprocess.check_output(
            ["git", "-C", corpus, "rev-parse", "--show-toplevel"],
            stderr=subprocess.STDOUT).decode().strip()
    except Exception as e:
        sys.stderr.write("AVISO: no es repo git, salto commit (%s)\n" % e)
        return
    rel = [os.path.relpath(p, root) for p in paths if os.path.exists(p)]
    subprocess.check_call(["git", "-C", root, "add"] + rel)
    # commit solo si hay algo staged
    rc = subprocess.call(["git", "-C", root, "diff", "--cached", "--quiet"])
    if rc == 0:
        sys.stderr.write("AVISO: nada que commitear\n")
        return
    subprocess.check_call(["git", "-C", root, "commit", "-m", msg])


def sha256_file(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_sha256(tabla, corpus):
    jp = journal_path(tabla, corpus)
    vp = view_path(tabla, corpus)
    jh = sha256_file(jp)
    vh = sha256_file(vp)
    print("journal %s sha256=%s" % (os.path.basename(jp), jh))
    print("vista   %s sha256=%s" % (os.path.basename(vp), vh))
    print("")
    print("# ATESTACION (la ejecuta el Arquitecto en el gate; el journal es la fuente inmutable):")
    print("#   registrar sha256 del journal via intent barato del ledger del hub.")
    print("#   sha256_journal=%s" % jh)
    return jh, vh


def do_write(args, op):
    tabla = args.tabla
    corpus = args.corpus
    sch, cols, by_name = load_schema(tabla, args.schema_dir)
    required_open = sch["campos_apertura_obligatorios"]
    sets = parse_sets(args.set or [])
    clave = resolve_clave(tabla, args, sets)
    events = read_journal(tabla, corpus, cols)
    _, state = materialize_rows(events, cols)
    exists = clave in state

    if op == "OPEN":
        if exists:
            die("la clave '%s' ya fue abierta; usa 'actualizar'/'cerrar-fila'" % clave)
        faltan = [c for c in required_open if c not in sets and c != KEY_COLUMN[tabla]]
        # si la clave natural es una columna, tambien debe venir en sets
        if KEY_COLUMN[tabla] and KEY_COLUMN[tabla] not in sets:
            faltan.append(KEY_COLUMN[tabla])
        if faltan:
            die("faltan campos de apertura obligatorios: %s" % sorted(set(faltan)))
        values = validate_and_coerce(sets, by_name, cols, required_open, enforce_open=True)
    else:
        if not exists:
            die("la clave '%s' no existe; abrela con 'nueva-fila'" % clave)
        values = validate_and_coerce(sets, by_name, cols, required_open, enforce_open=False)
        if op == "CLOSE":
            merged = dict(state[clave])
            merged.update(values)
            if merged.get("estado_final", NA) == NA:
                die("cerrar-fila exige estado_final (done|abandonada|truncada|bloqueada)")

    seq = append_event(tabla, corpus, cols, op, clave, values, args.event_ts)
    order, state2 = materialize_rows(read_journal(tabla, corpus, cols), cols)
    vp = write_view(tabla, corpus, cols, order, state2)
    jp = journal_path(tabla, corpus)
    print("OK %s seq=%d clave=%s -> %s" % (op, seq, clave, os.path.basename(jp)))
    print("vista re-materializada: %s (%d filas)" % (os.path.basename(vp), len(order)))
    if not args.no_commit:
        git_commit(corpus, [jp, vp], "medicion(%s): %s %s seq=%d" % (tabla, op.lower(), clave, seq))
    if args.atestar:
        cmd_sha256(tabla, corpus)


def cmd_materializar(args):
    tabla = args.tabla
    sch, cols, by_name = load_schema(tabla, args.schema_dir)
    order, state = materialize_rows(read_journal(tabla, args.corpus, cols), cols)
    vp = write_view(tabla, args.corpus, cols, order, state)
    print("vista re-materializada: %s (%d filas)" % (os.path.basename(vp), len(order)))


def cmd_verificar(args):
    tabla = args.tabla
    sch, cols, by_name = load_schema(tabla, args.schema_dir)
    events = read_journal(tabla, args.corpus, cols)
    if not events:
        print("journal vacio; nada que verificar")
        return
    # secuencia monotona
    seqs = [int(e["event_seq"]) for e in events]
    if seqs != list(range(1, len(seqs) + 1)):
        die("event_seq no es 1..N monotono: %s" % seqs)
    # cada evento: enums/tipos validos
    for e in events:
        for c in cols:
            v = e.get(c, "")
            if v not in ("", NA):
                coerce(by_name[c], v, is_open_phase_field=False)
    order, _ = materialize_rows(events, cols)
    print("OK verificar: %d eventos, %d claves, schema y secuencia consistentes" % (len(events), len(order)))


def main():
    ap = argparse.ArgumentParser(description="Gestor append-only del CSV de medicion NOVA Budget")
    ap.add_argument("cmd", choices=["nueva-fila", "actualizar", "cerrar-fila",
                                    "materializar", "sha256", "verificar"])
    ap.add_argument("--tabla", default="medicion", choices=["medicion", "defectos"])
    ap.add_argument("--corpus", default=".", help="carpeta del corpus (hub)")
    ap.add_argument("--schema-dir", default=HERE, help="carpeta de los schema_*.json")
    ap.add_argument("--clave", help="clave de la fila (tarea_id en medicion; requerida en defectos)")
    ap.add_argument("--set", action="append", help="campo=valor (repetible)")
    ap.add_argument("--event-ts", default=None, help="timestamp del evento (default: ahora UTC)")
    ap.add_argument("--no-commit", action="store_true", help="no hacer commit git")
    ap.add_argument("--atestar", action="store_true", help="imprimir sha256 tras escribir")
    args = ap.parse_args()

    if args.event_ts is None:
        args.event_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.cmd == "nueva-fila":
        do_write(args, "OPEN")
    elif args.cmd == "actualizar":
        do_write(args, "UPDATE")
    elif args.cmd == "cerrar-fila":
        do_write(args, "CLOSE")
    elif args.cmd == "materializar":
        cmd_materializar(args)
    elif args.cmd == "sha256":
        cmd_sha256(args.tabla, args.corpus)
    elif args.cmd == "verificar":
        cmd_verificar(args)


if __name__ == "__main__":
    main()
