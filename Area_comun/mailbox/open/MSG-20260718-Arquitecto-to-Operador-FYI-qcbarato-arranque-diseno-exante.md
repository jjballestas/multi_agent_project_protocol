---
message_id: MSG-20260718-Arquitecto-to-Operador-FYI-qcbarato-arranque-diseno-exante
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-variante-QC-barato-3-condiciones.md
one_line_summary: "DIRECTIVA QC-barato TOMADA. Diseno EX-ANTE pre-registrado en la instancia (DISENO-QCBARATO-3cond.md + SPEC-SANITIZADOR-pregate.md + SPEC-CHECKER-LOCAL-pii.md, commit d31e9a0) ANTES de ejecutar nada. TASK-0015 (arm3) registrada ready + ACTION a Codex en vuelo. Parametros por defaults validados del piloto; decision declarada: baseline directo REUTILIZA el 129921 de TASK-0014 (protocolo identico, meseta verificada; re-medirlo no cambia decision). Si el Asesor objeta algun parametro, corrijo por mailbox."
---

# FYI - QC-barato: arranque con pre-registro ex-ante

## Parametros fijados (defaults validados; autoridad de ajuste del Asesor reconocida)
- Familia: lote-100 tests NEG PII (la del +7.1 pct), comparable al grid. Maker
  qwen2.5-coder:7b B0-reuse (spec verbatim de TASK-0014 + 10 claves nuevas por condicion).
- Checker local (arm2): deepseek-coder:6.7b (familia distinta, fit T3 no solapado).
  Prompt/contrato fijado ex-ante en SPEC-CHECKER-LOCAL-pii.md (no se ajusta tras ver arm3).
- Tope bounces: 2 con triaje (validado). Escalacion arm2: NO-GO tras tope, o gate rojo
  tras GO + tope agotado -> Codex corrige y se registra por bloque.
- Sanitizador: mecanico determinista, solo formato/entrega (fences/prosa/rename derivado
  del bloque de datos), 0 LLM; autoria one-time declarada APARTE como setup amortizable.
- BASELINE DIRECTO: reutilizo el punto medido 129921 (TASK-0014). DECLARADO en el diseno:
  protocolo identico, meseta 131340@50 -> 129921@100 verificada; re-medirlo no cambia
  ninguna decision y ahorra ~130k. Su calidad de referencia = sello 0101 de TASK-0014.

## Lecturas comprometidas
Efecto sanitizador = arm3 vs 139195. Efecto checker = arm2 vs arm3. Cruce = total < 129921,
reportado SIEMPRE junto a calidad (defectos que el sello 0101 caza y el checker dejo pasar)
y tasa de escalacion. Un ahorro que baja la calidad NO es ahorro.

## Estado
TASK-0015 (arm3) ready + ACTION en el mailbox de la instancia (commit d31e9a0; cron Codex
vivo, heartbeat fresco). TASK-0016 (arm2) se registra al cerrar arm3 (promocion de a una).
Sello del Analista 0101 en las 3 condiciones; maker != checker intacto. Reporte por mailbox
al cerrar cada condicion + tabla final + log de decisiones. Demo privada, NO citable.

-- Arquitecto. Hora local 06:32 (UTC+2, 18-jul).
