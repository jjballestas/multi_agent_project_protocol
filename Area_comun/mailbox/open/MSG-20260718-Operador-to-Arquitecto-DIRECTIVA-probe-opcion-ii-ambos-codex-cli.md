---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-probe-opcion-ii-ambos-codex-cli
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-smoke-peon-qwen7b-verde.md
  - personal/Arquitecto/DISENO-probe-coste-peon-local.md
one_line_summary: "El operador CONFIRMA opcion (ii): instrumento del probe = Codex CLI en AMBOS brazos (absolutos comparables con el maker real de produccion). Re-corre el brazo A en el Codex CLI (descarta el brazo A revivido en curso, que apenas arranco). Brazo B tambien por el Codex CLI. Mismo instrumento en los dos -> delta valido + absolutos aplicables al setup real. Reporta la tabla A-vs-B."
requested_action: "[DIRECTIVA] Opcion (ii): usa el Codex CLI como instrumento en AMBOS brazos del probe. RE-CORRE el brazo A por el cron Codex (descarta el brazo A revivido que acaba de empezar). Corre el brazo B por el cron Codex (spec del maker CLI -> peon qwen2.5-coder:7b via HTTP local -> revision/integracion del maker CLI). Reporta la tabla A-vs-B (tokens frontier del maker, wall-clock, iteraciones de correccion del peon, veredicto del checker) + lectura cualitativa."
question: "Confirmas ambos brazos por el Codex CLI y el descarte del brazo A revivido en curso?"
---

# DIRECTIVA - Probe opcion (ii): ambos brazos en Codex CLI

El operador CONFIRMA la recomendacion: **instrumento del probe = Codex CLI en AMBOS brazos**, para
que los absolutos de tokens frontier sean comparables con su maker real de produccion (Codex), que
es lo que responde su decision de coste.

## Que hacer
- **Descarta el brazo A revivido** en curso (apenas arranco, coste minimo).
- **Brazo A por el Codex CLI:** el maker CLI hace la mitad-A directo. Registra tokens frontier del CLI.
- **Brazo B por el Codex CLI:** el maker CLI escribe la spec detallada -> peon `qwen2.5-coder:7b`
  (via API HTTP local localhost:11434 para conteo limpio) ejecuta la mitad-B -> el maker CLI
  revisa/corrige/integra. Registra tokens frontier del ciclo B + wall-clock/iteraciones del peon.
- **Mismo instrumento (Codex CLI) en los dos brazos** -> el delta A-vs-B es internamente valido Y
  los absolutos aplican al setup real. Umbral pre-declarado: B gana si ahorra >=25% de tokens
  frontier CON la suite verde en ambos. Empate/perdida = resultado util.

## Guardrails
Demo NO citable (anti-HARKing); PII de nomina fuera del probe; fondo intocable (2E35F26E / 1.14.0 /
N=500); DECISION-0099 (spec del maker al peon como artefacto = evidencia de peon subordinado);
checker fuerte revisa la unidad completa. Reporta la tabla A-vs-B + lectura cualitativa al cerrar.

-- Operador (via Asesor).
