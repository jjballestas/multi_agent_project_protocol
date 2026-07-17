---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-politica-roster-peones-solo-codigo-nunca-checker
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0097-gate1-activacion-memoria-hibrida-nova-payroll.md
one_line_summary: "POLITICA DE ROSTER del operador: los peones (agentes trabajadores, en especial los de modelo LOCAL pequeno) son SOLO para desarrollo de codigo, con ordenes MUY EXPLICITAS (intake DoR completo, contrato sin ambiguedad). NUNCA como checker. El rol de checker (revision adversarial, Analista) permanece en modelo FUERTE. Gobiernala como veas (politica de roster o DECISION). No bloquea el build actual."
requested_action: "[DIRECTIVA] Adopta y gobierna la politica: peon = maker-only con intake explicito; el checker NUNCA es un peon debil, se mantiene en modelo fuerte. Propon como codificarla (nota de roster en el AGENTS de la instancia o DECISION nueva) y confirma. No cambia el trio actual de Nova-Payroll (Codex frontier + Analista fuerte ya cumplen)."
question: "La codificas como politica de roster en el AGENTS/config de la instancia, o prefieres una DECISION del hub (capa metodologia) para que aplique a toda instancia futura?"
---

# DIRECTIVA - Politica de roster: peones = SOLO codigo, con ordenes explicitas, NUNCA checker

## La politica (operador, 2026-07-17)
1. **Los peones son SOLO para desarrollar codigo.** Un peon (agente trabajador; aplica en especial
   a los de MODELO LOCAL pequeno tipo 3B-8B que el operador tiene disponibles) se usa como MAKER,
   nunca para otro rol.
2. **Se le dan ordenes MUY CLARAS y explicitas.** El intake al peon debe ir con DoR completo y
   contrato sin ambiguedad: cuanto mas debil el modelo, mas carga la spec y menos decide el peon
   (ethos SDD / anti-vibecoding). Nada de tareas abiertas o subespecificadas a un peon.
3. **NUNCA como checker.** El rol de revision adversarial (Analista) NO lo ocupa un peon debil. El
   checker permanece en modelo FUERTE.

## Por que (la razon epistemica)
El valor entero de la metodologia es que el checker CAZA bugs reales (hoy mismo su refutacion
tumbo el default 'extracted' fail-open y la colision de PK del patron diferido). Un modelo debil
como checker haria rubber-stamp: preservaria `maker!=checker` por POSESION DE LLAVE pero lo
vaciaria por CAPACIDAD -> el gate se vuelve teatro y contamina la evidencia. Esa pieza no se toca.

## Alcance y timing
- Aplica a Fase A y adelante. **NO bloquea el build actual** de Nova-Payroll: Codex (frontier) como
  maker + Analista (fuerte) como checker YA cumplen la politica. Es guardrail para cuando entren
  peones de modelo local al roster.
- Guardrails intactos: PII de nomina fuera del store, fondo intocable (2E35F26E/1.14.0/N=500),
  firewall anti-HARKing, DECISION-0081 intacta.

Confirma como la gobiernas (nota de roster en la instancia o DECISION del hub).

-- Operador (via Asesor).
