---
message_id: MSG-20260711-Operador-to-Arquitecto-GO-regenesis-A2-julian-y-speckit-contabilidad
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Arquitecto-to-Operador-FYI-hito-contabilidad-base-solida-ws1-fix.md
  - Area_comun/artifacts/PREP-CONTABILIDAD-esqueleto-spec-patron.md
  - dictionary/accounting_ws1_base_solida.html (design-source, D:/Agentes/Ingenas, fuera del hub)
  - dictionary/accounting_module_requirements.html (SDD design-source, fuera del hub)
one_line_summary: "GO a la re-genesis A2 de Aegis (Julian ya acepto la invitacion + pubkey recibida) + DIRECTIVA PREP: con el WS1 y el SDD de Contabilidad instancia el kit de SPECs SPEC-CONT-* siguiendo el patron Presupuesto (escribir, NO construir). Ninguna de las dos abre el build gobernado."
requested_action: "(1) EJECUTA la re-genesis A2 del config de AEGIS (candado de la instancia, NUNCA el hub): registra la pubkey jheredia:v1 + alta en agent_registry + gate e2e de 2 clones; Julian ya acepto la invitacion y su pubkey esta persistida. (2) Con el WS1 (accounting_ws1_base_solida.html) y el SDD (accounting_module_requirements.html) como design-source, INSTANCIA el kit de SPECs SPEC-CONT-* por unidad/slice (R1-R8) en formato NOVA-SPEC-T-001, reutilizando el patron de las SPECs de Presupuesto (superficie sobre procs, gates dotnet/arch/F-NOVA-01 con los THROW reales de la seccion D, aislamiento intra-par, preflight por unidad). Es PREP: escribir, NO construir; NO promuevas tareas de build; el build sigue gated por (base promovida al hub/instancia + Sprint 1 post-30-jul)."
question: "Confirmas ejecutada la re-genesis A2 (o blocker con pregunta) y arrancas el kit SPEC-CONT-* como PREP? Reporta cuando el gate e2e de 2 clones quede verde (desbloquea a Julian) y a medida que entregues las SPEC-CONT por slice."
---

# ACTION - GO re-genesis A2 (Julian) + kit SPEC-CONT de Contabilidad (PREP)

Recibido tu FYI del hito design-source (base solida + WS1 + THROW reales + fix de integridad). Dos ordenes.

## 1. GO re-genesis A2 de Aegis (onboarding de Julian)
Julian ACEPTO la invitacion a NOVA-Aegis en git y su pubkey ed25519 (jheredia:v1) ya esta persistida.
GO a ejecutar la re-genesis A2 del config de AEGIS (candado de la INSTANCIA, NUNCA el hub):
- registra la pubkey jheredia:v1,
- alta en agent_registry,
- gate e2e de 2 clones -> reporta cuando quede verde.
Autorizo que reactive agentes. Es PREP valido: NO abre el build gobernado (sigue gated por base promovida
+ Sprint 1 post-30-jul) y NO toca baseline/core pineado (2E35F26E, epoch 1.14.0, dataset N=500).

## 2. Kit SPEC-CONT-* de Contabilidad (PREP, escribir no construir)
Con el design-source ya atestado -- WS1 (accounting_ws1_base_solida.html) + SDD
(accounting_module_requirements.html), en D:/Agentes/Ingenas fuera del hub -- instancia el kit de SPECs de
Contabilidad:
- una SPEC por unidad/slice siguiendo R1-R8 del SDD: Slice 1 reportes RO, Slice 2 comprobante manual
  borrador->publicacion->reverso, Slice 3 cierre/apertura mensual P03-P07, Slice 4 saldos iniciales de
  vigencia, Slice 5 CHIP contingencia, 6A informe trimestral CGN/CHIP, 6B cierre anual, 6C causacion de
  ingresos/CxC (marca 6C como frontera del modulo fuente donde aplique);
- formato NOVA-SPEC-T-001, reutilizando el patron congelado de las SPECs de Presupuesto (superficie C# sobre
  procs, gates dotnet/arch, F-NOVA-01 con los THROW REALES de la seccion D del WS1, aislamiento intra-par,
  preflight por unidad del PREP);
- respeta la escotilla SESSION_CONTEXT('accounting_annual_close') y el fix de integridad del periodo cerrado
  tal como quedaron en el WS1 -- no lo relajes en las SPECs; hornea el follow-up de s.4 (fijar
  source_module_code='accounting' en la captura manual) como hardening declarado, no como bypass.

Es PREP: ESCRIBIR, no construir. NO promuevas tareas de build ni actives SESSION_CONTEXT desde la API. El
BUILD gobernado sigue gated por (base promovida al hub/instancia + calendario Sprint 1 post-30-jul). La
colocacion gobernada (hub Area_comun/specs/nova/ como Presupuesto, o el ledger de la instancia) queda a tu
criterio de frontera; solo deja claro donde viven.

-- Operador
