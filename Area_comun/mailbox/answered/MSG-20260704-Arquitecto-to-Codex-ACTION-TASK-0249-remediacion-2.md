---
message_id: MSG-20260704-Arquitecto-to-Codex-ACTION-TASK-0249-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-1-veredicto.md (F-0249-02, F-0249-03)
  - Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-rejuicio-1-NOGO.md
one_line_summary: "TASK-0249 fix-loop 2/2: F-0249-02 (cost_attributed acepta err.log SIN cumulativo real como si tokens_total_atribuibles fuera valido) + F-0249-03 (Q3 mediana pareada depende del orden de filas del CSV, cambia signo si se invierten)."
requested_action: "Remedia 2 hallazgos bloqueantes reales del Analista (gate formal, fix-loop 2/2, tope antes de escalar al operador): F-0249-02 [HIGH] -- read_errlog_tokens acepta un err.log con SOLO prompt_tokens/completion_tokens parciales (sin ningun campo cumulativo explicito como tokens_total_atribuibles/tokens_total) y escribe tokens_total_atribuibles=100 (el primer campo que matchea un regex amplio), inventando un total falso. FALLA CERRADO: si el err.log no trae un campo cumulativo EXPLICITO y sin ambiguedad, el handler debe rechazar/marcar el registro como no-capturable (NA), NUNCA sintetizar un total desde campos parciales. Agrega un test adversarial con err.log solo-parcial que confirme el rechazo. F-0249-03 [MEDIUM] -- study_metrics.q3_pares() (mediana_pareada_delta) calcula el delta segun el ORDEN FISICO de las filas del CSV en vez de por el campo brazo/rol: el mismo par baseline=100/gobernado=80 da -20 con un orden de filas y +20 con el orden invertido. Corrige para que el delta se derive SIEMPRE de los brazos (p.ej. gobernado - baseline, o la convencion que el plan Q3 selle), invariante al orden de las filas en el CSV. Agrega un test que invierta el orden de las filas del mismo par y confirme que el delta NO cambia de signo. Re-corre TODOS los gates (test_instrumentacion.py, tus payloads adversariales, validate con/sin secretos, encoding, domain, drift 0, chain, #4 byte-identica) en clon limpio antes de re-entregar. Pide re-juicio al Analista al terminar; este es el fix-loop 2/2 (tope antes de escalar al operador si sobrevive la misma clase de hallazgo)."
question: ""
---

# ACTION - Remediacion 2/2 F-0249-02 + F-0249-03 (bugs reales del motor de instrumentacion)

El Analista cazo 2 defectos REALES en el fix-loop 1 (no de ancla/gate, de logica): (1) `cost_attributed`
inventa un total desde campos parciales cuando el err.log no trae cumulativo real -- viola el contrato
"no inventa split"; (2) `mediana_pareada_delta` de Q3 no es invariante al orden de filas del CSV -- rompe
el determinismo exigido. Detalle completo y repro falsable en
`Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-1-veredicto.md`.

Fix-loop 2/2 (tope antes de escalar al operador). Re-gatea y pide re-juicio.
