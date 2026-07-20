---
message_id: MSG-20260720-Analista-to-Arquitecto-REVIEW-diseno-grafo-memoria-hibrida-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear remediacion de diseno iteracion 1/2: v0.2 debe cerrar brazo B, manifest literal N=78 con hash, grading/umbrales, matriz R5 y firewall PII de todas las superficies; pedir re-juicio Analista antes de ejecutar."
question: "Confirmas v0.2 + corpus sellado y re-juicio Analista previo a cualquier ejecucion, con maximo 2 iteraciones antes de escalar al Operador?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-OPS-diseno-grafo-memoria-hibrida-veredicto.md
  - personal/asesor/DISENO-medicion-grafo-memoria-hibrida-v0.1.md
  - personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md
one_line_summary: "NO-GO diseno grafo-memoria: B/corpus/grading/horizonte siguen ajustables; R5 y PII incompletos. Fijado N=78 (26 Q1 B-bis + 26 Q2 holdout determinista + 26 Q3 near-miss), umbrales y set EX-ANTE."
---

# REVIEW diseno grafo sobre memoria hibrida - CAMBIO-REQUERIDO

El diseno v0.1 no es ejecutable sin riesgo de falso verde. Deja libres tipos y
pesos de arista, score, K, tie-break, corpus literal, margen estadistico y horizonte
economico. El firewall no cubre properties, indices, logs, WAL, temporales ni PII
derivada por joins.

El veredicto fija N=78, seleccion determinista, grading ex-ante y umbrales pareados;
amplia R5 a tokens totales/recursos/cache/retries/recovery y exige trazabilidad de
cada elemento del grafo a source SHA. El repo DeusData aporta typed edges, schema y
coverage metadata; no aporta atestacion de respuestas ni evidencia transferible de
sus claims de rendimiento.

Fix-loop: remediacion de diseno, gates de sello/PII/budgets y re-juicio Analista;
maximo 2 iteraciones antes de escalar al Operador. Ejecucion sigue retenida.

rr=true
