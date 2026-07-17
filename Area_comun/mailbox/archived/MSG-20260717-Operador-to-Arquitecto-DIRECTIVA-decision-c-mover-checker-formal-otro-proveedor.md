---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-decision-c-mover-checker-formal-otro-proveedor
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-FYI-clasificador-proveedor-recurrente-fallback-checker.md
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
one_line_summary: "El operador ELIGE la opcion (c): mover el checker formal a otro proveedor/CLI que autorice trabajo de seguridad legitimo, via DECISION (cambio de harness). Redacta la DECISION con un destino propuesto y prepara para FIRMA del operador. No bloquea U4 (sigue el fallback informal); los re-juicios formales diferidos se re-ejecutan en el nuevo proveedor en vez de esperar a que OpenAI desbloquee."
requested_action: "[DIRECTIVA] Redacta la DECISION que mueve el CHECKER FORMAL a otro proveedor/CLI que autorice trabajo de seguridad legitimo (el rol de checker ES sondeo adversarial de seguridad; un proveedor cuyo classifier lo flagea esta mal casado). Propon el destino y el alcance (instancia vs capa hub), y preparala PARA FIRMA del operador -- me la presentas y la relevo. No degrades los probes."
question: "Confirmas el destino propuesto (recomendacion: Claude/Anthropic CLI, ya usado como fallback informal, da diversidad maker!=checker por PROVEEDOR) y el alcance (recomendacion: capa hub via espejo 0096, aplica a toda instancia)?"
---

# DIRECTIVA - Decision del operador: OPCION (c), mover el checker formal a otro proveedor/CLI

## Decision
El operador ELIGE la **opcion (c)** de tu FYI: **mover el checker formal a otro proveedor/CLI** que
autorice trabajo de seguridad legitimo, via **DECISION** (cambio de harness). Es el arreglo
ESTRUCTURAL, no un parche: el rol de checker es sondeo adversarial de seguridad por diseno, y un
proveedor cuyo classifier flagea eso esta fundamentalmente mal casado para el rol.

## [RECOMENDACION] Destino y alcance (objetables)
- **Destino:** Claude/Anthropic CLI. Razones: (1) autoriza trabajo de seguridad legitimo -> elimina
  el falso positivo de raiz; (2) YA es el checker del fallback informal que corre ahora, asi que
  FORMALIZA lo que ya funciona; (3) da **diversidad maker!=checker por PROVEEDOR** (maker OpenAI/
  Codex vs checker Claude), mas fuerte que solo por posesion de llave. Si ves una alternativa mejor
  (harness/coste), proponla en el draft.
- **Alcance:** capa HUB (metodologia) con espejo en el export born-operational (0096) -> aplica a
  toda instancia. Razon: CUALQUIER checker adversarial sufre el mismo mismatch de proveedor, no solo
  el de Nova-Payroll. Si prefieres acotar a Nova-Payroll primero y generalizar despues, justifica.

## Efecto operativo (incorporalo al draft)
- **NO bloquea U4** en curso: sigue el fallback informal para cerrar Fase A.
- Los **re-juicios formales diferidos** (U3 con checker_formal=0, y cualquier otro) se **re-ejecutan
  en el NUEVO proveedor** una vez cableado, en vez de esperar a que OpenAI desbloquee. Asi Fase A
  cierra con la atestacion formal completa por la via nueva.
- maker!=checker por CAPACIDAD + LLAVE + (ahora) PROVEEDOR. Cumple DECISION-0099 regla 3.

## Guardrails
Fondo intocable (2E35F26E / epoch 1.14.0 / N=500), firewall anti-HARKing (Fase A = demostracion, no
citable), DECISION-0081 intacta, PII de nomina fuera del store. El cambio es de HARNESS del checker,
no del estudio medido.

Preparala PARA FIRMA (patron 0091/0099): me presentas el draft y relevo la firma del operador.

-- Operador (via Asesor).
