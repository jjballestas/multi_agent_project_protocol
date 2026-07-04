# ANALISTA - TASK-0249 F3.3 instrumentacion re-juicio 2/2

Firma: Analista
Fecha: 2026-07-04

## Veredicto

OK/CERRABLE.

Ancla canonica revisada:

- Protocolo REVIEW HEAD: `7be5cf1af5c96c44e3e94693ef789ebe39ef67d5`
- Implementacion/handoff remediado: `fc412b86037a17cc7ddda36da29d67a309d8c21e`
- Producto Nova-Budget: N/A por instruccion canonica ("Producto commit citable: NINGUNO"; alcance 100% hub/instancia)

## Reproduccion

Clon limpio del protocolo: `C:\Users\johnb\AppData\Local\Temp\analista-task0249-20260704145801`, checkout `7be5cf1`.

| Gate | Resultado |
| --- | --- |
| `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` | PASS exit 0, 7 tests |
| `python -m py_compile personal/Arquitecto/TFM-medicion/instrumentacion_estudio/instrumentacion.py personal/Arquitecto/TFM-medicion/instrumentacion_estudio/study_metrics.py personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` | PASS exit 0 |
| Payloads adversariales propios contra `instrumentacion.py` y `study_metrics.py` | PASS exit 0 |
| `python scripts/validate_collaboration_state.py` en clon limpio | PASS exit 0 |
| `python scripts/scan_encoding.py` en clon limpio | PASS exit 0 |
| `python scripts/scan_domain_neutrality.py` en clon limpio | PASS exit 0 |
| Drift/chain en clon limpio | PASS exit 0, `has_drift=false`, `up_to_seq=3865`, `checked_events=3193` |
| `git diff --exit-code fc412b8 -- protocol.config.json` en clon limpio | PASS exit 0 |
| `python scripts/validate_collaboration_state.py` en repo vivo | PASS exit 0 |
| `python scripts/scan_encoding.py` en repo vivo | PASS exit 0 |
| `python scripts/scan_domain_neutrality.py` en repo vivo | PASS exit 0 |
| `git diff --exit-code fc412b8 -- protocol.config.json` en repo vivo | PASS exit 0 |
| Producto `npm test` | NOT_RUN: instruccion canonica declara producto NINGUNO y ordena no ejecutar producto |

`protocol.config.json` permanece byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Matriz vector por vector

| Vector / AC | Juicio | Evidencia falsable |
| --- | --- | --- |
| F-0249-02: `err.log` solo-parcial no debe inventar `tokens_total_atribuibles` | PASA | Payloads `prompt_tokens=100 completion_tokens=50`, JSON OpenAI-like, lineas separadas y `total prompt tokens: 150` fueron rechazados con `ValueError` y no crearon CSV. |
| F-0249-02: cumulativos explicitos validos siguen aceptados | PASA | `tokens_total_atribuibles=321`, `tokens_total: 322`, `cumulative_tokens 323`, `total_tokens_cumulative 324` materializaron exactamente 321/322/323/324. |
| F-0249-03: Q3 no depende del orden fisico CSV | PASA | Dos pares con deltas -20 y +30 dieron `mediana_pareada_delta=5.0`; al invertir filas, el valor siguio siendo 5.0 y los puntos fueron equivalentes. |
| Determinismo del reporte | PASA | Dos llamadas a `build_report` con el mismo `now` parametrizado produjeron JSON ordenado identico. |
| `defect.reported` rechaza enums invalidos y acepta fila valida | PASA | `taxonomia=D9` -> `rejected`; `taxonomia=D1` con campos de apertura -> `accepted`. |
| `manual.intervention` solo overhead fijo | PASA | Fila `OVERHEAD-FIJO-*` con `rol_en_par=overhead_fijo`; `product_task_tokens` devuelve 0 para el incidente. |
| Q4/Q5 no emiten causalidad | PASA | `q4.emite_causalidad=false` y `q5.afirmacion_causal=false` en payload propio. |
| Eventos applied:false / off-by-default no tocan event log | PASA | Test canonico `test_event_log_off_by_default_unchanged` PASS; suite completa 7/7. |
| Gates del hub y drift | PASA | Validate/encoding/domain PASS; drift `has_drift=false`, `up_to_seq=3865`; chain valid `checked_events=3193`. |
| #4 / epoch pin | PASA | `protocol.config.json` byte-identico contra `fc412b8`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Residuales

- El parser acepta solo los aliases cumulativos explicitos listados en el contrato; no intenta sumar parciales ni inferir totales desde formatos no declarados.
- Producto Nova-Budget queda fuera de este cierre por instruccion canonica. Si el operador quiere convertir producto en gate de F3.3, hace falta una instruccion con commit citable.

## Recomendacion

CERRABLE. No detecte un escape nuevo en F-0249-02/F-0249-03 ni regresion en los vectores del re-juicio 1.

task_id: TASK-0249
status: done
executive_summary: OK/CERRABLE; F-0249-02 y F-0249-03 quedan cerrados por comportamiento en clon limpio, y los vectores previos de TASK-0249 siguen verdes.
artifacts:
  - Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-2-veredicto.md
  - Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-rejuicio-2-OK.md
gates:
  - command: python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py
    result: PASS exit 0
  - command: payloads adversariales propios contra instrumentacion.py y study_metrics.py
    result: PASS exit 0
  - command: python scripts/validate_collaboration_state.py
    result: PASS exit 0 clean clone and live
  - command: python scripts/scan_encoding.py
    result: PASS exit 0 clean clone and live
  - command: python scripts/scan_domain_neutrality.py
    result: PASS exit 0 clean clone and live
  - command: drift/chain probe
    result: PASS exit 0, has_drift=false, up_to_seq=3865, checked_events=3193
next_recommended: Arquitecto puede cerrar TASK-0249 si sus propios gates de cierre permanecen verdes.
risks: Producto Nova-Budget no fue ejecutado porque la instruccion canonica declara producto NINGUNO.
