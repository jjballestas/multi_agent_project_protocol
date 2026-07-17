---
message_id: MSG-20260717-Operador-to-Arquitecto-GO-probe-coste-peon-qwen7b
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - personal/Arquitecto/DISENO-probe-coste-peon-local.md
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
one_line_summary: "GO del operador al probe de coste del peon local. OK al diseno tal cual (revisado). Modelo local = qwen2.5-coder:7b (via Ollama). Fase A ya cerro, asi que puede arrancar: smoke del peon PRIMERO, luego la mecanica (2 mitades disjuntas A maker-solo vs B maker-delega-al-peon, delta de tokens frontier, umbral >=25% con suite verde). Demo/soporte a decision, NO citable."
requested_action: "[DIRECTIVA] GO: ejecuta el probe de coste segun tu DISENO-probe-coste-peon-local.md. Modelo local qwen2.5-coder:7b. Paso 0 obligatorio: 1 smoke del peon (verifica invocable desde el harness del maker, sin tocar el hub) y REPORTA el smoke antes de la mecanica -- si el modelo no rinde, el operador puede cambiarlo ahi. Luego registra la TASK gobernada en Nova-Payroll y corre A vs B. Reporta la tabla A-vs-B + lectura cualitativa."
question: "Confirmas el smoke de qwen2.5-coder:7b y el arranque, o ves un bloqueo (Ollama no cableado, etc.) que deba escalar?"
---

# DIRECTIVA - GO al probe de coste del peon (modelo qwen2.5-coder:7b)

El operador REVISO el diseno (`DISENO-probe-coste-peon-local.md`) y da **GO**. OK al diseno tal cual.

## Parametros confirmados
- **Modelo local:** `qwen2.5-coder:7b` (via Ollama). Recomendacion del Asesor (mejor coder del lote
  disponible); si el smoke muestra que no rinde, el operador reevalua (deepseek-coder:6.7b u otro).
- **Sub-tarea:** lote de tests negativos PII por clave allowlisted (20 claves), 2 mitades disjuntas
  (10 + 10 por sorteo documentado).
- **Condiciones:** A = maker-solo (mitad-A). B = maker escribe spec detallada -> peon local ejecuta
  mitad-B -> maker revisa/corrige/integra. El maker responde ante el checker por B igual que por A.
- **Metrica:** delta de tokens FRONTIER del maker (A - B), contando el overhead de spec + review.
  Tokens del peon local ~= coste-cero monetario pero se registra su wall-clock. Umbral pre-declarado:
  B gana si ahorra >=25% de tokens frontier CON la suite verde en ambas. Empate/perdida = resultado util.

## Timing y guardrails
- Fase A YA cerro (5/5 done), asi que puede arrancar. **Paso 0: smoke del peon + reporte** antes de la
  mecanica (ventana para cambiar de modelo si hace falta).
- Clase de evidencia: DEMO / soporte a decision, **NO citable** (anti-HARKing). Un numero riguroso =
  pre-registro Fase B solo si promete.
- PII de nomina fuera de todo el probe; fondo intocable (2E35F26E / 1.14.0 / N=500); DECISION-0099
  (la spec del maker al peon queda como artefacto = evidencia de peon subordinado); el checker sigue fuerte.

Reporta el smoke primero, luego la tabla A-vs-B.

-- Operador (via Asesor).
