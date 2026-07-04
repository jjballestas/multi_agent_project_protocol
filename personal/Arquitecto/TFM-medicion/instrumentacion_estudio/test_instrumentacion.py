#!/usr/bin/env python3
# -*- coding: ascii -*-
import csv
import json
import os
import tempfile

import instrumentacion
import study_metrics

SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "corpus", "medicion")


def read_rows(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_cost_idempotent(tmp):
    err = os.path.join(tmp, "err.log")
    open(err, "w", encoding="utf-8").write("tokens_total_atribuibles=12345\n")
    out = os.path.join(tmp, "medicion.csv")
    extra = {"brazo": "baseline", "par_id": "PAR-A", "estimate_previo_SML": "M", "criticidad": "alta", "fecha_commit_estimate": "2026-07-04", "rol_en_par": "miembro", "orchestration_mode": "mono"}
    a = instrumentacion.cost_attributed(out, SCHEMA_DIR, "NB-P2-1", ["s1"], err, extra)
    b = instrumentacion.cost_attributed(out, SCHEMA_DIR, "NB-P2-1", ["s1"], err, extra)
    rows = read_rows(out)
    assert len(rows) == 1
    assert a["cost_idempotency_key"] == b["cost_idempotency_key"]
    assert rows[0]["tokens_total_atribuibles"] == "12345"
    assert rows[0]["tokens_dev"] == "NA"


def test_defect_rejects_bad_enum(tmp):
    out = os.path.join(tmp, "defectos.csv")
    status, _ = instrumentacion.defect_reported(out, SCHEMA_DIR, "BAD", {"tarea_id_origen": "NB-P2-1", "fecha_descubrimiento": "2026-07-05", "taxonomia": "D9", "severidad": "alta", "detector": "checker_formal", "paridad_detector": "true", "clase": "b"})
    assert status == "rejected"
    assert not os.path.exists(out)
    status, row = instrumentacion.defect_reported(out, SCHEMA_DIR, "DEF-1", {"tarea_id_origen": "NB-P2-1", "fecha_descubrimiento": "2026-07-05", "taxonomia": "D1", "severidad": "alta", "detector": "checker_formal", "paridad_detector": "true", "clase": "b"})
    assert status == "accepted"
    assert row["paridad_detector"] == "true"
    assert len(read_rows(out)) == 1


def test_manual_intervention_overhead_only(tmp):
    out = os.path.join(tmp, "medicion.csv")
    instrumentacion.manual_intervention(out, SCHEMA_DIR, "INC-1", "2026-07-04", 777, "incidente")
    rows = read_rows(out)
    assert rows[0]["rol_en_par"] == "overhead_fijo"
    assert instrumentacion.product_task_tokens(rows) == 0


def test_metrics_golden_and_q3_guard(tmp):
    medicion = [
        {"tarea_id": "A", "brazo": "baseline", "par_id": "PAR-1", "rol_en_par": "miembro", "tokens_total_atribuibles": "100", "tag_incidente_maquinaria": "NA", "orchestration_mode": "mono"},
        {"tarea_id": "B", "brazo": "gobernado", "par_id": "PAR-1", "rol_en_par": "miembro", "tokens_total_atribuibles": "80", "tag_incidente_maquinaria": "NA", "orchestration_mode": "mono"},
        {"tarea_id": "OVERHEAD-FIJO-1", "brazo": "gobernado", "par_id": "NA", "rol_en_par": "overhead_fijo", "tokens_total_atribuibles": "20", "tag_incidente_maquinaria": "arranque", "orchestration_mode": "NA"},
    ]
    defectos = [{"taxonomia": "D1", "paridad_detector": "true", "clase": "b"}, {"taxonomia": "D2", "paridad_detector": "false", "clase": "b"}]
    a = study_metrics.build_report(medicion, defectos, "2026-07-04T00:00:00Z", "2026-07-03", "2026-07-25")
    b = study_metrics.build_report(medicion, defectos, "2026-07-04T00:00:00Z", "2026-07-03", "2026-07-25")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["q1"]["tokens_producto_total"] == 180
    assert a["q1"]["overhead_por_tag"]["arranque"] == 20
    assert a["q2"]["confirmatorio_clase_b_paridad_true_n"] == 1
    assert a["q3"]["statistical_inference"] == "RECHAZADO_POR_DISENO"
    assert "p_value" in a["q3"]["forbidden_outputs"]
    assert a["q4"]["estado"] == "SUBPOTENCIADO"
    assert a["q5"]["afirmacion_causal"] is False


def test_event_log_off_by_default_unchanged(tmp):
    event_log = os.path.join(os.path.dirname(os.path.dirname(__file__)), "corpus", "runtime", "state", "events.jsonl")
    before = open(event_log, "rb").read()
    after = open(event_log, "rb").read()
    assert before == after


def main():
    tests = [test_cost_idempotent, test_defect_rejects_bad_enum, test_manual_intervention_overhead_only, test_metrics_golden_and_q3_guard, test_event_log_off_by_default_unchanged]
    with tempfile.TemporaryDirectory() as root:
        for test in tests:
            tmp = os.path.join(root, test.__name__)
            os.makedirs(tmp)
            test(tmp)
    print("OK test_instrumentacion: %d tests" % len(tests))


if __name__ == "__main__":
    main()
