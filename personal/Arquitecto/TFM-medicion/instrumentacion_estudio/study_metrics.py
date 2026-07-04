#!/usr/bin/env python3
# -*- coding: ascii -*-
import argparse
import csv
import json
from statistics import median

NA = "NA"


def read_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_int(row, key):
    value = row.get(key, NA)
    return 0 if value in ("", None, NA) else int(value)


def q1_costo(medicion):
    product = [r for r in medicion if r.get("rol_en_par") != "overhead_fijo"]
    overhead = [r for r in medicion if r.get("rol_en_par") == "overhead_fijo"]
    by_arm = {}
    by_tag = {}
    for row in product:
        by_arm[row.get("brazo", NA)] = by_arm.get(row.get("brazo", NA), 0) + as_int(row, "tokens_total_atribuibles")
    for row in overhead:
        by_tag[row.get("tag_incidente_maquinaria", NA)] = by_tag.get(row.get("tag_incidente_maquinaria", NA), 0) + as_int(row, "tokens_total_atribuibles")
    return {"tokens_producto_por_brazo": by_arm, "tokens_producto_total": sum(by_arm.values()), "overhead_por_tag": by_tag, "tokens_con_overhead": sum(by_arm.values()) + sum(by_tag.values()), "degradacion_por_cubeta": "NA_si_sesion_no_separada"}


def q2_calidad(defectos):
    confirmatorio = [d for d in defectos if d.get("paridad_detector") == "true" and d.get("clase") == "b"]
    descriptivo = [d for d in defectos if d.get("paridad_detector") != "true"]
    by_tax = {}
    for row in confirmatorio:
        by_tax[row.get("taxonomia", NA)] = by_tax.get(row.get("taxonomia", NA), 0) + 1
    return {"confirmatorio_clase_b_paridad_true_n": len(confirmatorio), "confirmatorio_por_taxonomia": by_tax, "descriptivo_paridad_false_n": len(descriptivo), "plan_b_efecto_techo": len(confirmatorio) == 0}


def q3_pares(medicion):
    pairs = {}
    for row in medicion:
        par_id = row.get("par_id", NA)
        if par_id != NA and row.get("rol_en_par") != "overhead_fijo":
            pairs.setdefault(par_id, []).append(as_int(row, "tokens_total_atribuibles"))
    deltas = [v[1] - v[0] for v in pairs.values() if len(v) == 2]
    return {"dot_plot_points": pairs, "mediana_pareada_delta": median(deltas) if deltas else NA, "statistical_inference": "RECHAZADO_POR_DISENO", "forbidden_outputs": ["p_value", "intervalo_confianza", "regresion"]}


def q4_causal(medicion, expected_pairs=8):
    pairs = {r.get("par_id") for r in medicion if r.get("par_id", NA) != NA}
    return {"estado": "SUBPOTENCIADO" if len(pairs) < expected_pairs else "PRE_VENTANA_LISTO", "pares_observados": len(pairs), "pares_esperados": expected_pairs, "sorteo_diseno": "8/2", "emite_causalidad": False}


def q5_transfer(medicion):
    modes = {}
    for row in medicion:
        modes[row.get("orchestration_mode", NA)] = modes.get(row.get("orchestration_mode", NA), 0) + 1
    return {"descriptivo": True, "orchestration_mode_n": modes, "afirmacion_causal": False}


def build_report(medicion, defectos, now, window_start, window_end):
    return {"generated_at": now, "window": {"start": window_start, "end": window_end}, "q1": q1_costo(medicion), "q2": q2_calidad(defectos), "q3": q3_pares(medicion), "q4": q4_causal(medicion), "q5": q5_transfer(medicion)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--medicion", required=True)
    p.add_argument("--defectos", required=True)
    p.add_argument("--now", required=True)
    p.add_argument("--window-start", required=True)
    p.add_argument("--window-end", required=True)
    args = p.parse_args()
    print(json.dumps(build_report(read_rows(args.medicion), read_rows(args.defectos), args.now, args.window_start, args.window_end), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
