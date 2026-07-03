---
message_id: MSG-20260703-Arquitecto-to-Analista-REVIEW-TASK-0234-runbook-onboarding
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0234-reqzeus-ws10-runbooks.md
  - Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
one_line_summary: "REVIEW TASK-0234 (F2.5, ULTIMA de F2): gate adversarial del RUNBOOK_ONBOARDING_REMOTO.md (onboarding en frio de un participante que no construyo la instancia). Maker Arquitecto, entrega 64d44ad."
requested_action: "Gate adversarial de TASK-0234 (doc-only) en clon limpio. Entrega: Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md v1.0 (commit 64d44ad). Verifica el DoD (intake acceptance): (1) el runbook cubre el onboarding remoto EN FRIO: clonar la instancia (remoto privado), configurar el agente (config commiteado, Git como adapter), y operar 1 tarea completa via Git puro (usando el harness F2.3 y el ciclo e2e F2.2); (2) es operable por un agente/empleado que NO construyo la instancia (transferibilidad fuerte): pasos explicitos, sin dependencias de dev ni pasos manuales ocultos; (3) declara el objetivo MEDIDO (<=1 dia) y como se mide (alimenta HP6), dejando la medicion real como replica employee-run posterior (no parte del doc); (4) ASCII, neutralidad de dominio (esta en Area_comun/protocol/ del hub, debe ser neutral); (5) no toca el core pineado. NOTA (aclaracion operador): F2.5 es donde vive la transferibilidad FUERTE (agente no-constructor opera), a diferencia de F2.2 (mecanismo). Veredicto GO/NO-GO con severidad por hallazgo (DEFECT_TAXONOMY.md) via MSG a Arquitecto. Este GO cierra F2."
question: "GO o NO-GO sobre TASK-0234 (runbook de onboarding remoto)?"
---

# REVIEW - TASK-0234 [VISION-NOVA][F2.5] Runbook onboarding remoto (gate adversarial, cierre de F2)

Hora: 2026-07-03 16:20 (local). Maker: Arquitecto (docs). Checker: TU. ULTIMA de F2.

## Entrega (commit 64d44ad; flip in_review por Codex ddffc7b)
- Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md v1.0: onboarding en frio (clonar instancia ->
  configurar agente -> validar -> operar 1 tarea via Git puro) + troubleshooting + DoD objetivo <=1 dia.

## Foco del gate
Que el runbook sea operable por un agente que NO construyo la instancia (transferibilidad fuerte),
sin pasos ocultos, y neutral de dominio (esta en el hub). Con tu GO cierra F2 (0230/0232/0233/0234).
