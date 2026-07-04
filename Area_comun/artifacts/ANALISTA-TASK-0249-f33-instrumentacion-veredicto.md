# ANALISTA - TASK-0249 F3.3 instrumentacion - veredicto

Firma: Analista

Veredicto: CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica revisada:
- Protocolo REVIEW HEAD: 2c6e847908416dbf41d7a14faa521df902fa8c1c
- Implementacion citada: a32ee61 (por handoff y ancestro del REVIEW)
- Producto Nova-Budget: ninguno citado; el REVIEW canonico declara alcance 100% hub/instancia y ordena no ejecutar clone/npm-test de producto.

Hallazgo bloqueante:
- F-0249-01 [CRITICAL]: el gate propio de la instrumentacion no es reproducible en clon limpio. `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` sale 1 porque intenta cargar `personal/Arquitecto/TFM-medicion/corpus/medicion/schema_medicion.json`, ruta que no esta commiteada en el commit canonico revisado. Por tanto no queda probado en canonico el handler `cost.attributed`, ni la validacion de `defect.reported`, ni `manual.intervention`, ni el test de event-log off-by-default.

Reproduccion con exit codes:

| Gate | Resultado |
|---|---|
| `git clone https://github.com/jjballestas/multi_agent_project_protocol.git <tmp>; git checkout 2c6e847908416dbf41d7a14faa521df902fa8c1c` | EXIT 0 |
| `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` | EXIT 1: `FileNotFoundError ... personal/Arquitecto/TFM-medicion/corpus/medicion/schema_medicion.json` |
| `python -m py_compile personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` | EXIT 0 |
| `python scripts/validate_collaboration_state.py` | EXIT 0 |
| `python scripts/scan_encoding.py` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| `python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), ensure_ascii=True, sort_keys=True))"` | EXIT 0; `has_drift=false`, `up_to_seq=3859` |
| `git diff --exit-code a32ee61 -- protocol.config.json` | EXIT 0 |
| Nova-Budget clone + `npm test` | NOT_RUN: no product commit cited and REVIEW canonico explicitly excludes product scope |

Vector por vector:

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| Determinismo `study_metrics.py` misma entrada -> misma salida | NO PROBADO | El test suite canonico aborta antes de completar la familia por fixture faltante. |
| `cost.attributed` lee cumulativo real del err.log, idempotente, cubetas NA | SLIPS | La primera prueba falla antes de ejercer la funcion por `schema_medicion.json` ausente. |
| Err.log con formato distinto no inventa split | NO PROBADO | No pude ejecutar payload adversarial contra el handler canonico porque el schema requerido no existe en clean clone. |
| `defect.reported` valida schema v1.0 y rechaza malformados sin fila invalida | NO PROBADO | La suite depende del mismo corpus no commiteado; el schema v1.0 no queda disponible en canonico. |
| `paridad_detector` particiona confirmatorio/descriptivo | NO PROBADO | La parte de metricas existe, pero el contrato completo con schema/evento no queda gateado por el fallo temprano. |
| `manual.intervention` produce OVERHEAD-FIJO y no carga tokens a tarea de producto | NO PROBADO | El handler requiere `schema_medicion.json`; el test canonico no llega a cerrarlo en clean clone. |
| Q3 guard duro sin p-value/IC/regresion | PARCIAL | Codigo contiene salida fija `RECHAZADO_POR_DISENO` y lista de prohibidos, pero la suite formal no termina. |
| Eventos applied:false no tocan `submit_intent` / event log byte-equivalente | NO PROBADO | El test de event log usa una ruta de corpus local no commiteada; no hay prueba byte-equivalente reproducible. |
| Gates hub validate/encoding/domain/drift/#4 | PASA | Exit 0 en clean clone, drift false, `protocol.config.json` byte-identico contra a32ee61. |

Residuales:
- No hay juicio de producto: el propio REVIEW canonico declara producto commit `NINGUNO` y fuera de alcance.
- El fallo es de reproducibilidad canonica, no de estilo. Puede estar verde en la maquina del maker por archivos ignorados/locales, pero eso no cierra el contrato del estudio.

Fix-loop esperado:
- Remediar en canonico los fixtures/rutas requeridos por `test_instrumentacion.py`, o cambiar el test para consumir solo fixtures commiteados dentro del alcance.
- Re-ejecutar en clon limpio: test de instrumentacion, py_compile, validate con/sin secretos si aplica, encoding, domain, drift 0 y #4 byte-identica.
- Re-juicio Analista antes del commit de cierre. Maximo 2 iteraciones antes de escalar al operador si sobrevive la misma clase de hallazgo.

task_id: TASK-0249
status: change_required
executive_summary: CAMBIO-REQUERIDO. TASK-0249 no es cerrable porque el gate propio de instrumentacion falla en clon limpio por fixtures/corpus no commiteados, asi que los handlers y el off-by-default no quedan probados canonicamente.
artifacts:
  - Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-veredicto.md
  - Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-NOGO.md
gates:
  - command: python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py
    result: FAIL exit 1
  - command: python scripts/validate_collaboration_state.py
    result: PASS exit 0
  - command: python scripts/scan_encoding.py
    result: PASS exit 0
  - command: python scripts/scan_domain_neutrality.py
    result: PASS exit 0
  - command: protocol_state_drift(Path('.'))
    result: PASS has_drift=false
next_recommended: Codex remedia fixtures/rutas reproducibles y solicita re-juicio formal de Analista.
risks: Si se cierra asi, F3.3 queda dependiente de archivos locales no atestados y el estudio podria medir con una herramienta no reproducible.
