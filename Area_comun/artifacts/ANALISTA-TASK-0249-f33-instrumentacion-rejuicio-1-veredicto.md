# ANALISTA - TASK-0249 F3.3 instrumentacion - rejuicio 1

Firma: Analista

Veredicto: CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica revisada:
- Protocolo REVIEW HEAD: 5bf2e70 (mensaje REVIEW del Arquitecto).
- Producto Nova-Budget: N/A. La instruccion canonica cita "Producto commit citable: NINGUNO" y ordena no ejecutar clone/npm-test de producto porque TASK-0249 no toca producto.
- Implementacion bajo juicio: `personal/Arquitecto/TFM-medicion/instrumentacion_estudio/` en el commit canonico anterior.

Hallazgos bloqueantes:

- F-0249-02 [HIGH]: `cost_attributed` acepta un err.log sin cumulativo y registra un total falso. Payload: `prompt_tokens=100 completion_tokens=50 no cumulative field`. Resultado observado: fila aceptada con `tokens_total_atribuibles=100`. Esto no es "cumulativo leido"; es el primer campo parcial que calza con el regex amplio `(tokens|total)`. Riesgo falsable: un log con desglose parcial pero sin total acumulado queda materializado como medicion valida.
- F-0249-03 [MEDIUM]: Q3 `mediana_pareada_delta` depende del orden fisico de filas, no de los brazos del par. Con el mismo par baseline=100/gobernado=80, el orden `[baseline,gobernado]` da `-20` y el orden `[gobernado,baseline]` da `20`. La mediana pareada no puede depender del orden accidental del CSV.

Reproduccion con exit codes:

| Gate | Resultado |
|---|---|
| `git clone . <tmp>; git checkout 5bf2e70` | EXIT 0 |
| `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py` | EXIT 0; 5 tests |
| Payload adversarial propio sobre handlers/metrics | EXIT 0; 7 vectores ejecutados; slips: `cost malformed err.log`, `q3 row-order invariant` |
| `python scripts/validate_collaboration_state.py` en clon limpio sin secretos | EXIT 0 |
| `python scripts/scan_encoding.py` en clon limpio | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en clon limpio | EXIT 0 |
| `protocol_state_drift(Path('.'))` en clon limpio | EXIT 0; `has_drift=false`, `up_to_seq=3861` |
| `validate_chain(events_in_log_order(root), config, root=root)` en clon limpio | EXIT 0; `valid=true`, `checked_events=3189` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; byte-identico contra `5bf2e70` |
| `python scripts/validate_collaboration_state.py` en repo vivo con secretos | EXIT 0 |
| `python scripts/scan_encoding.py` en repo vivo | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en repo vivo | EXIT 0 |
| Drift vivo | EXIT 0; `has_drift=false`, `up_to_seq=3861` |
| Chain vivo | EXIT 0; `valid=true`, `checked_events=3189` |
| Nova-Budget clean clone + `npm test` | NOT_RUN: no commit de producto citado; REVIEW canonico excluye producto |

Vector por vector:

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| Determinismo `study_metrics.py` misma entrada -> misma salida | PASA | Suite canonica exit 0; payload propio repite `build_report` con mismo `now` y salida estable. |
| `cost.attributed` cumulativo real, idempotente, cubetas NA | SLIPS | Caso positivo pasa con `tokens_total_atribuibles: 43210`, idempotente y cubetas NA; caso negativo acepta `prompt_tokens=100 completion_tokens=50` como total 100 aunque no hay cumulativo. |
| Err.log con formato distinto no inventa split | PARCIAL | No inventa cubetas por rol; pero si inventa `tokens_total_atribuibles` desde un campo parcial. |
| `defect.reported` schema v1.0 y rechazo sin fila invalida | PASA | Malformado por campo obligatorio faltante y enum fuera de rango -> `rejected`; archivo invalido no queda escrito; valido se acepta. |
| `paridad_detector` particiona confirmatorio/descriptivo | PASA | Defecto valido `paridad_detector=true`, `clase=b` entra en Q2 confirmatorio; rejected no contamina CSV. |
| `manual.intervention` OVERHEAD-FIJO sin cargar tarea de producto | PASA | Fila `OVERHEAD-FIJO-INC-X`, `rol_en_par=overhead_fijo`, `product_task_tokens(rows)==0`. |
| Q3 guard duro sin p-value/IC/regresion | PARCIAL | No calcula inferencia y devuelve `RECHAZADO_POR_DISENO`; residual: expone los nombres prohibidos en `forbidden_outputs`, no valores numericos. |
| Q3 mediana pareada coherente | SLIPS | Misma pareja con filas invertidas cambia delta `-20` -> `20`; debe derivar el signo por `brazo`, no por orden CSV. |
| Q4/Q5 skeleton descriptivo/subpotenciado | PASA | Q4 emite `SUBPOTENCIADO` con n menor que esperado; Q5 no afirma causalidad. |
| Eventos `applied:false` no tocan `submit_intent` / event log | PASA | No hay llamadas a `submit_intent`; hash de `runtime/state/events.jsonl` igual antes/despues de invocar handlers. |
| Gates hub validate/encoding/domain/drift/#4 | PASA | Exit 0 con y sin secretos, drift 0, chain valid, #4 byte-identica. |

Residuales declarados:
- Producto no probado por diseno de la instruccion canonica: no hay commit de producto citado y el alcance declara NINGUN cambio en Nova-Budget.
- `forbidden_outputs` nombra `p_value`, `intervalo_confianza` y `regresion`; no lo bloqueo porque no emite estadisticos, pero conviene renombrarlo a una negativa textual si se quiere evitar ambiguedad en consumidores.

Fix-loop esperado:
- Endurecer `read_errlog_tokens`: aceptar solo un campo cumulativo explicito (`tokens_total_atribuibles` o `tokens_total` con semantica clara) y fallar cerrado si el err.log solo trae parciales como `prompt_tokens`/`completion_tokens`.
- Calcular Q3 por brazos (`gobernado - baseline`, o la direccion que el plan selle) y no por orden de filas; agregar test con filas invertidas.
- Re-gatear test de instrumentacion, payloads adversariales, validate con/sin secretos, encoding, domain, drift 0, chain y #4 byte-identica. Re-juicio Analista antes del cierre; maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0249
status: change_required
executive_summary: CAMBIO-REQUERIDO. TASK-0249 no es cerrable: el fix hace reproducible la suite, pero `cost_attributed` acepta err.logs sin cumulativo como medicion valida y Q3 cambia la mediana pareada al invertir filas del mismo par.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-1-veredicto.md; Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-rejuicio-1-NOGO.md
gates: clean clone test_instrumentacion exit 0; adversarial payloads exit 0 with 2 slips; validate clean/vivo exit 0; encoding clean/vivo exit 0; domain clean/vivo exit 0; drift clean/vivo 0 up_to_seq=3861; chain valid checked_events=3189; #4 sha256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354
next_recommended: Devolver a Codex para fix-loop 2/2 sobre parser cumulativo de err.log y Q3 order-invariance; re-juicio formal previo a cierre.
risks: Si se cierra asi, la medicion del estudio puede registrar tokens falsos desde logs parciales y puede cambiar signo de Q3 por orden accidental de CSV.
