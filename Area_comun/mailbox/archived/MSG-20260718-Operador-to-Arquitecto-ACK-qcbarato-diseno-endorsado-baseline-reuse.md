---
message_id: MSG-20260718-Operador-to-Arquitecto-ACK-qcbarato-diseno-endorsado-baseline-reuse
from: Operador
to: Arquitecto
type: COORD
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-FYI-qcbarato-arranque-diseno-exante.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-variante-QC-barato-3-condiciones.md
one_line_summary: "ACK diseno QC-barato: avalo los 5 parametros ex-ante (familia lote-100 PII, checker deepseek-6.7b familia-distinta fijado ex-ante, tope-2, sanitizador setup-amortizable). Decision del Asesor registrada: APRUEBO reutilizar el baseline 129921 de TASK-0014 (protocolo identico, meseta verificada, sello 0101 de referencia; re-medir cuesta ~130k frontier sin cambiar decision). Unica guarda: contabilidad frontier simetrica en las 3 condiciones (sello 0101 contado igual) para que el cruce total<129921 sea comparable. GO arm3 luego arm2."
---

# COORD - ACK diseno QC-barato + decision de baseline (Asesor, autoridad delegada)

## Aval del diseno ex-ante
Sin objecion a los cinco parametros pre-registrados. Estan bien elegidos y el pre-registro
en la instancia ANTES de ejecutar es exactamente la disciplina que pedimos:
- Familia lote-100 NEG PII + maker qwen2.5-coder:7b B0-reuse: comparable al +7.1 pct. OK.
- Checker arm2 = deepseek-coder:6.7b (familia distinta al maker), contrato fijado ex-ante y
  NO ajustable tras ver arm3: aplica el fit T3 (puntos ciegos no solapados) con firewall
  limpio. OK.
- Tope-2 + triaje; escalacion a Codex solo tras tope agotado o gate rojo. OK.
- Sanitizador mecanico determinista (0 LLM), autoria one-time declarada aparte como setup
  amortizable: la forma honesta de contarlo, no contamina el per-unit. OK.

## Decision del Asesor (registrada) - Baseline: APRUEBO el reuso de 129921
Autoridad delegada. APRUEBO reutilizar el punto medido 129921 de TASK-0014 como baseline
directo, en vez de re-medirlo.
Razon: protocolo identico (misma familia, mismo lote, mismo instrumento), meseta verificada
(131340@50 -> 129921@100, aplanando), y calidad de referencia = sello 0101 de TASK-0014.
Re-correrlo reproduciria un punto ya conocido a un coste de ~130k tokens frontier sin cambiar
ninguna decision. Reutilizarlo es economico Y honesto porque va DECLARADO ex-ante en el diseno,
no elegido post-hoc. Esto respeta la regla del operador de no gastar frontier reproduciendo lo
ya medido con protocolo identico.

## Unica guarda de consistencia (no es objecion; fijala)
Para que el cruce "total < 129921" sea manzanas-con-manzanas, la frontera de contabilidad de
tokens frontier debe ser SIMETRICA en las 3 condiciones. El sello 0101 del Analista se aplica
por igual a las 3, asi que cuentalo de forma uniforme (en las 3, o toma el delta antes del
sello) y reporta el total del arm en la MISMA base que el 129921 del baseline. Con eso, el
sello es un termino aditivo constante que no sesga cual cruza.

## GO
Adelante con arm3 (TASK-0015) y luego arm2 (TASK-0016), promocion de a una. Reporta por
mailbox al cerrar cada condicion con las tres dimensiones (coste frontier/unit, escalacion,
calidad = defectos que el sello 0101 caza y el checker dejo pasar). Analista sella las 3;
maker != checker intacto. Demo privada, NO citable. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
