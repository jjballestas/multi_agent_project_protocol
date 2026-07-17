---
message_id: MSG-20260717-Operador-to-Arquitecto-DECISION-adopta-memoria-hibrida-follow-through
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-f1-completa-demo-revive-exitosa.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "DECISION DE ADOPCION del operador: ADOPTA la memoria hibrida en la metodologia. Los 4 criterios de demostracion verdes + DEMO REVIVE conductual exitosa cross-atestada (Entrada 1) lo sostienen. Redacta la DECISION de adopcion PARA FIRMA. Follow-through: promocion al master hub via export 0096 = Fase 3+ AGENDADA post-ventana-medida (no toca el estudio ahora); re-juicio formal U3/U4 via (c); cierre del runbook; probe de coste del peon (diseno ya ruteado); F2 minimo NO."
requested_action: "[DIRECTIVA] Redacta la DECISION de ADOPCION de la memoria hibrida PARA FIRMA del operador (patron 0091/0099): metodologia adopta la capacidad; promocion al master hub (scripts/instance_assets via export 0096) AGENDADA a Fase 3+ POST-ventana-medida; U3/U4 re-juicio formal via (c); F2 minimo NO (nada lo pide). Me devuelves el draft para presentarlo a firma. No toques scripts/ del hub durante la ventana medida."
question: "Confirmas el alcance de la DECISION de adopcion (adopta + promocion agendada post-ventana + no F2) y me devuelves el draft para firma?"
---

# DIRECTIVA - Decision del operador: ADOPTA la memoria hibrida

## Decision
El operador **ADOPTA la memoria hibrida en la metodologia**. La sostiene la demostracion (criterio
del GO, por DEMOSTRACION no estadistica): **round-trip verde + drift 0 + cold-start recall + REVIVE
demostrable**, los 4 VERDES, con la **DEMO REVIVE conductual exitosa** (peon muerto -> worker de
contexto cero revivio SOLO con su pack atestado, verifico contra el ledger vivo, no repitio trabajo
ya hecho, claimo con llaves de instancia, entrego con gates 0/0/0 y drift 0; cross-atest Entrada 1).

## Follow-through (redactalo en la DECISION de adopcion)
1. **Promocion al master hub** (scripts/instance_assets, via export born-operational DECISION-0096):
   integracion Fase 3+ (gate canonico) **AGENDADA a POST-ventana-medida** (post-30-jul). NO se toca
   scripts/ del hub durante la ventana. La instancia deja el motor probado y esperando.
2. **Re-juicio formal de U3/U4** (checker_formal=0 declarado): se cierra con la migracion (c) del
   checker a otro proveedor. No bloquea la adopcion (decidida por demostracion).
3. **Runbook (TASK-0005):** cierra su ciclo (fallback informal si el classifier lo frena).
4. **Probe de coste del peon:** diseno ya ruteado; ejecuta tras cerrar F1.
5. **F2 minimo: NO** -- nada lo pide hoy; no expandir alcance.

## Firewall y guardrails
La adopcion es del OPERADOR por DEMOSTRACION; el probe NO es evidencia citable (anti-HARKing).
Fondo intocable (2E35F26E / epoch 1.14.0 / N=500); PII de nomina fuera del store; DECISION-0081
intacta; el estudio medido (Contabilidad) sigue gated post-30-jul, sin tocar.

Redacta la DECISION de adopcion y devuelvemela para la firma del operador.

-- Operador (via Asesor).
