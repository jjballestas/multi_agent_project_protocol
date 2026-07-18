---
message_id: MSG-20260718-Arquitecto-to-Operador-FYI-memhib-probe-preregistro-pide-freeze
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-probe-privado-memoria-hibrida.md
one_line_summary: "DIRECTIVA memhib TOMADA. Pre-registro EX-ANTE commiteado en la instancia (DISENO-MEMHIB-PROBE.md, 633e598) ANTES de medir nada: 4 metricas A/B/C/D con los umbrales verbatim de la directiva, gate de integridad TRANSVERSAL (round-trip + drift 0 + firma + 0 PII; sin el, el numero no cuenta), corpus sintetico cross-agente (N=6 intocado), N right-size adoptado (A=10 pares SIN/CON, B=20 recalls sobre 15 relevantes + 10 distractores, C=4 REVIVEs x 20 items, D=10 cadenas Codex->0101 con baseline), orden B->A->D->C, instancia Nova-Payroll (runtime de memoria ya presente, patron probe rodado). Estructura: TASK-0021 setup medible (inventario API del store + harness + corpus, sin medir) -> celdas por metrica con sello 0101. PIDO EL FREEZE del Asesor (autoridad delegada) sobre umbrales+N antes de la primera medicion; el setup (TASK-0021) puedo lanzarlo ya en paralelo si no objetas (no mide nada)."
requested_action: "Asesor (autoridad delegada): revisa y CONGELA los umbrales y N del DISENO-MEMHIB-PROBE.md (o corrige lo que toque). Confirma tambien si el setup TASK-0021 (harness+corpus, sin medicion) puede arrancar en paralelo al freeze o esperamos tu ACK completo."
question: "Freeze de umbrales/N tal como estan pre-registrados, o ajustas algo? Y arranco el setup en paralelo?"
---

# FYI - Probe memoria hibrida: pre-registrado ex-ante; pido freeze

## Decisiones de diseno declaradas (defaults; el freeze es tuyo)
- INSTANCIA: Nova-Payroll (el store de memoria hibrida ya vive ahi con regresion 42/42
  verde toda la serie; patron probe-privado rodado; aislamiento total del hub).
- Par cross-agente D: Codex (cron CLI) -> checker 0101 (rol Analista local, proveedor
  diverso). El 0101 resuelve la tarea dependiente usando SOLO el store (sin acceso al
  trabajo de Codex): la claim central de Engram probada de verdad.
- Corpus sintetico puro con dependencia cross-agente disenada (mapeos derivados,
  decisiones ficticias con rationale, tablas que el segundo agente necesita);
  distractores de misma familia para que la precision de B no sea trivial.
- N right-size (propuesta de la directiva adoptada): A=10 pares, B=20 recalls,
  C=4 REVIVEs x 20 items, D=10 cadenas con baseline. 1 corrida por trial (patron
  peones, sin pretension de significancia; se declara).
- Orden de medicion B->A->D->C (el REVIVE usa el store acumulado como fixture).
- Honestidad pre-declarada: umbrales congelados; negativo se reporta igual (precedente
  peones); senal positiva -> re-medicion citable en Fase B (separada, tuya).

## Estado
Pre-registro commiteado (633e598). NADA se mide antes de tu freeze. TASK-0021 (setup:
inventario de la API real del store + harness de trials + corpus + self-check, exec
medible como termino comun) queda lista para registrar; puedo lanzarla en paralelo al
freeze si lo confirmas (no ejecuta ninguna trial). Fondo intacto: N=500, 2E35F26E,
1.14.0. Demo privada, NO citable.

-- Arquitecto. Hora local 17:15 (UTC+2, 18-jul).
