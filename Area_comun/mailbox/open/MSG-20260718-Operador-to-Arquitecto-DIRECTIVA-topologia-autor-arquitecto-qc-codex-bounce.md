---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-topologia-autor-arquitecto-qc-codex-bounce
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-tramo-t1-b0reuse-cerrado.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-b0reuse-quita-b1literal-sigue-grid.md
one_line_summary: "GO a la topologia de delegacion aplanada: el Arquitecto autora la spec peon-ready y enruta; el peon ejecuta; Codex hace QC con bounce (tope + triaje desliz-vs-techo a tu criterio); entrega al Analista para el check formal independiente que sella. Instrumenta bounces + QC-tokens en el grid. maker!=checker (0101) intacto. Demo NO citable."
---

# DIRECTIVA - Topologia de delegacion aplanada (autor-Arquitecto + QC-Codex-bounce + check Analista)

## Motivacion (del hallazgo del probe)
El tramo T1 mostro que la spec calibrada ES el valor y que la re-especificacion por Codex era
la ceremonia cara. Aplanamos: quien mejor conoce la tarea (el Arquitecto, frontier) autora la
spec YA peon-ready, se enruta por tier, y se elimina que Codex tenga que rehacer la spec.

## El loop operativo (adoptar)
1. ARQUITECTO: autora la spec peon-ready (calibrada para el modelo destino, no solo
   "detallada") Y ENRUTA por tier: mecanica peon-apta -> peon; dura/abierta -> Codex directo.
2. PEON: ejecuta codigo bajo esa spec (subordinado al maker, DECISION-0099).
3. CODEX: hace QC del output del peon y BOUNCE si no pasa (devuelve al peon con feedback).
   - TOPE de bounces y CRITERIO de triaje desliz-vs-techo: A TU CRITERIO de diseno. Guia:
     devolver solo deslices corregibles (formato, caso omitido); si es techo de capacidad,
     no repetir en el tier barato -- subir a Codex directo. El tope evita quemar ciclos
     baratos infinitos en una tarea que excede al peon (leccion B1).
4. ANALISTA: recibe el trabajo que paso el QC de Codex y hace el CHECK FORMAL INDEPENDIENTE
   que SELLA (Claude/Anthropic por DECISION-0101, proveedor diverso).

## Guardarrail no negociable (maker != checker, DECISION-0101)
El QC de Codex es control de calidad del LADO MAKER; NO es el check de gobernanza. Codex estuvo
en la cadena maker (autoria via Arquitecto + supervision + integracion) y por tanto NUNCA sella.
El sello es SIEMPRE del Analista independiente, de proveedor distinto. No fundir ambas
validaciones.

## Instrumentacion en el grid (nuevas metricas)
Anade al grid en curso dos metricas para que el N de break-even incluya el coste de calidad,
no solo el de spec:
- Numero de BOUNCES por celda (cuantas devoluciones al peon hasta pasar el QC).
- Tokens de QC de Codex por celda (el coste frontier de revisar el output del peon).
Ademas, mide added-spec-tokens del lado ARQUITECTO (autoria peon-ready) vs autoria-Codex: es el
numero que confirma si el aplanamiento ahorra de verdad (~0 marginal = tesis confirmada).

## Marco
Demo PRIVADA, NO citable (firewall anti-HARKing: el piloto informa la decision de correr un
confirmatorio, no su diseno). Instrumento Codex CLI. Baseline de maquina por celda. Fondo
intocable N=500 / 2E35F26E / epoch 1.14.0. Esto es topologia operativa del carril; si en algun
momento la quieres como norma permanente del roster, la formalizamos como decision gobernada
(hoy es adopcion de carril, no sello). Reporta por mailbox al cerrar cada tramo.

-- Operador (via Asesor). 18-jul.
