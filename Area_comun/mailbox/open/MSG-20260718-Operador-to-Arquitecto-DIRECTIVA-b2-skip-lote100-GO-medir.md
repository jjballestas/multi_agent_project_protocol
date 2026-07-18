---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-b2-skip-lote100-GO-medir
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-t4-grid-completo-techo-de-entrega.md
one_line_summary: "Dos decisiones del operador sobre el grid completo 17/17. (1) B2: SKIP DECLARADO confirmado -- grid cierra en 17 celdas + bounce-cap. (2) Lote-100 confirmatorio: NO se parquea -- GO MEDIRLO, porque el estudio esta siendo revelador (T4 refuto el techo-de-logica, fit modelo-familia, techo-de-entrega). Corre comparable a la curva 10/50 para confirmar/refutar el ~99. Demo NO citable."
---

# DIRECTIVA - B2 skip declarado + GO al lote-100 (medir, no parquear)

## Decision 1 - B2 (triage): SKIP DECLARADO confirmado
De acuerdo: B2 mediria lo que el rubric v0.2 + el si-entonces del manual ya operacionalizan.
Skip DECLARADO (no silencioso), registrado. El grid queda cerrado con 17 celdas + el chequeo
bounce-cap (TASK-0013).

## Decision 2 - Lote-100 confirmatorio: GO, MEDIRLO (no parqueado)
Cambio mi lectura previa: el estudio esta siendo REVELADOR (T4 refuto la prediccion de
techo-de-logica; el techo real es de entrega y es saneable ~0; el fit modelo-familia; el
break-even). Eso activa la Via 2 (medir lo que es distinto del prior art). Por tanto el
break-even ~99u deja de ser solo indicativo: quiero el punto medido, no la extrapolacion de 2
puntos.
- Corre lote 100 en AMBOS brazos (directo vs delegado-7b-B0reuse + QC-bounce), COMPARABLE a la
  curva de lote 10/50 (MISMO protocolo que esos puntos) para que confirme o refute limpiamente
  el ~99. La comparabilidad manda: no cambies el protocolo dentro del punto confirmatorio.
- Reporta: per-unit medido a lote 100, si el marginal delegado sigue por debajo del directo, y
  el break-even N ya con 3 puntos (10/50/100) en vez de 2.
- OPCIONAL (a tu criterio de diseno, NO dentro del confirmatorio): un punto extra CON el
  sanitizador mecanico pre-gate para mostrar la curva operativa mejorada. Si lo corres, va
  como celda aparte y claramente etiquetada, para no contaminar la comparabilidad del ~99.

## Continua (ya en marcha, sin cambios)
Bounce-cap 2-vs-3 (TASK-0013) en exec -> veredicto en tu proximo reporte; el dato T4 (bounce
oscilante en formato) hace plausible que el tope-3 recupere celdas de formato. Gate=scorer
VERIFICADO; aplica el fix de asserts de conformidad derivados del bloque de datos. Sanitizador
mecanico de salida al protocolo del manual NOVA (sube el techo real del peon).

## Marco
Demo PRIVADA, NO citable (el punto confirmatorio firma el numero para NUESTRA decision y para
la Via 2; si algun dia hay sellado, se re-mide con rigor estadistico multi-maquina). Instrumento
Codex CLI. Fondo intocable N=500 / 2E35F26E / epoch 1.14.0. Cierra el manual NOVA con el
veredicto del bounce-cap + el lote-100 y entregamelo como artefacto.

-- Operador (via Asesor). 18-jul.
