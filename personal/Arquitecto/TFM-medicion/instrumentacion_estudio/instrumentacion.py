#!/usr/bin/env python3
# -*- coding: ascii -*-
import csv
import hashlib
import json
import os
import re

NA = "NA"
TOKEN_RE = re.compile(r"\b(?:tokens_total_atribuibles|tokens_total|cumulative_tokens|total_tokens_cumulative)\b[^0-9]*(\d+)", re.I)


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path, fields, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in data:
            w.writerow({k: row.get(k, NA) for k in fields})


def load_schema(schema_dir, name):
    with open(os.path.join(schema_dir, "schema_%s.json" % name), "r", encoding="utf-8") as f:
        schema = json.load(f)
    cols = [c["n"] for c in schema["columnas"]]
    return cols, {c["n"]: c for c in schema["columnas"]}, schema["campos_apertura_obligatorios"]


def validate(col, value):
    if value in ("", None, NA):
        return NA
    value = str(value)
    tipo = col["tipo"]
    if tipo == "enum" and value not in col["enum"]:
        raise ValueError("invalid enum for %s: %s" % (col["n"], value))
    if tipo == "int":
        return str(int(value))
    if tipo == "float":
        return str(float(value))
    if tipo == "bool":
        low = value.lower()
        if low in ("true", "1", "si", "yes"):
            return "true"
        if low in ("false", "0", "no"):
            return "false"
        raise ValueError("invalid bool for %s: %s" % (col["n"], value))
    if tipo == "date" and not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        raise ValueError("invalid date for %s: %s" % (col["n"], value))
    return value


def read_errlog_tokens(path):
    found = None
    matches = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            match = TOKEN_RE.search(line)
            if match:
                found = int(match.group(1))
                matches.append(match.group(0))
    if found is None:
        raise ValueError("no explicit cumulative token count found in err.log")
    return found


def idempotency_key(tarea_id, sesion_ids):
    raw = tarea_id + "|" + "|".join(sorted(str(s) for s in sesion_ids))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def cost_attributed(medicion_csv, schema_dir, tarea_id, sesion_ids, errlog_path, extra):
    cols, by_name, required = load_schema(schema_dir, "medicion")
    data = rows(medicion_csv)
    current = next((dict(r) for r in data if r.get("tarea_id") == tarea_id), {c: NA for c in cols})
    current.update(extra or {})
    current.update({
        "tarea_id": tarea_id,
        "sesiones_ids": ";".join(sesion_ids),
        "fuente_tokens": "err.log",
        "tokens_total_atribuibles": str(read_errlog_tokens(errlog_path)),
        "tokens_dev": NA,
        "tokens_adversarial_informal": NA,
        "tokens_checker_formal": NA,
        "tokens_coordinacion_gobierno": NA,
    })
    missing = [c for c in required if current.get(c, NA) == NA and c != "par_id"]
    if missing:
        raise ValueError("missing opening fields: " + ",".join(missing))
    current = {c: validate(by_name[c], current.get(c, NA)) for c in cols}
    current["cost_idempotency_key"] = idempotency_key(tarea_id, sesion_ids)
    data = [r for r in data if r.get("tarea_id") != tarea_id] + [current]
    write_rows(medicion_csv, cols + ["cost_idempotency_key"], data)
    return current


def defect_reported(defects_csv, schema_dir, defecto_id, values):
    cols, by_name, required = load_schema(schema_dir, "defectos")
    try:
        missing = [c for c in required if values.get(c, NA) in ("", None, NA)]
        if missing:
            raise ValueError("missing opening fields: " + ",".join(missing))
        row = {c: validate(by_name[c], values.get(c, NA)) for c in cols}
    except Exception as exc:
        return "rejected", {"defecto_id": defecto_id, "reason": str(exc)}
    data = rows(defects_csv)
    if not any(r.get("defecto_id") == defecto_id for r in data):
        write_rows(defects_csv, ["defecto_id"] + cols, data + [dict({"defecto_id": defecto_id}, **row)])
    return "accepted", row


def manual_intervention(medicion_csv, schema_dir, incidente_id, fecha, tokens, tag_incidente_maquinaria):
    cols, by_name, _ = load_schema(schema_dir, "medicion")
    row = {c: NA for c in cols}
    row.update({
        "tarea_id": "OVERHEAD-FIJO-" + incidente_id,
        "brazo": "gobernado",
        "par_id": NA,
        "rol_en_par": "overhead_fijo",
        "estimate_previo_SML": "S",
        "criticidad": "overhead",
        "fecha_commit_estimate": fecha,
        "tokens_total_atribuibles": str(int(tokens)),
        "tag_incidente_maquinaria": tag_incidente_maquinaria,
    })
    row = {c: validate(by_name[c], row.get(c, NA)) for c in cols}
    data = [r for r in rows(medicion_csv) if r.get("tarea_id") != row["tarea_id"]] + [row]
    write_rows(medicion_csv, cols, data)
    return row


def product_task_tokens(data):
    return sum(int(r.get("tokens_total_atribuibles", 0)) for r in data if r.get("rol_en_par") != "overhead_fijo" and r.get("tokens_total_atribuibles") not in ("", NA, None))
