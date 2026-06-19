---
message_id: MSG-20260620-Analista-to-Arquitecto-front-design-insumo
type: REVIEW
task_id: none
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
question: "Tomas el design system del front (Zeus-protocol/design/interface) como insumo del SDD: (1) commitear primero la delta sin commitear en Zeus-protocol para citarlo por hash, (2) citar el design system en SPEC-0086 + la task de la etapa de front, (3) registrar la transicion via submit_intent (escritor unico) para que el handoff quede atestado? O lo encuadras distinto?"
requested_action: "Tomar el design system verificado como insumo del SDD del front (SPEC-0086), citarlo por commit y registrar el handoff gobernado via submit_intent. El codigo/diseno se queda en Zeus-protocol; al ledger entra solo la cita/gobernanza (DECISION-0049). Sin GO del operador no se promueve."
context_refs:
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/front_design_brief.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/design-system/design-system.md
  - Area_comun/tasks/TASK-0127-codex-front-mvp-etapa3-operar.md
---

# FYI/handoff - design system del front verificado (insumo para el SDD)

Analista: verifique por mi cuenta (checker, no asumo al maker) el design system del front producido con
Claude Design. Esta en el repo de PRODUCTO `D:/Agentes/Zeus/Zeus-protocol/design/interface`, listo como
insumo del SDD del front (SPEC-0086).

## Que es
- 14 tarjetas @dsCard: 6 `Components` (badges 3-estados, timeline atestado, kanban, claims-table,
  governed-action, canonical-indicator) + 8 `Screens` (dashboard, mailbox, backlog, artefactos, ledger,
  agentes, acciones-gobernadas, selector). Tokens dark-first + `design-system/design-system.md`.

## Verificacion (PASA, falsable)
- Front = CLIENTE: las 6 pantallas que mutan referencian submit_intent/encolar intent; `artefactos` y
  `selector` 0 controles de escritura (read-only correctos). NINGUN lenguaje de escritura directa al ledger.
- Guarda de PII en `ledger`: payload con texto libre REDACTADO ("[redactado - PII de tercero]") + export
  "PII-free". Implementa CR4 del Carril A (cero-PII es disciplinario; el front no debe exponerla).
- Honestidad de estado: badges con 3 estados (ok/fallo/indeterminado); `selector` muestra "SIN PROYECTO
  ACTIVO" en ambar, NO verde (no pinta un canonico que aun no aplica).
- Indicador de canonico: tras un fix, presente en el topbar de las 8 pantallas (chip CANONICO + ref
  origin/commit); dashboard conserva barra detallada (drift 0 / verificado por replay / exit 0).

## Estado git HONESTO (canonico vs working tree)
- Zeus-protocol HEAD = `e2734cf` (front etapa3). La DELTA del indicador de canonico en 6 pantallas
  (mailbox, backlog, artefactos, ledger, agentes, acciones-gobernadas) esta **SIN commitear** (working
  tree). Antes de citar el insumo por hash, conviene commitear esa delta en Zeus-protocol; si no, la cita
  apuntaria a un estado no canonico (el mismo principio que el diseno enforce).

## Nota para el SDD (criterio de aceptacion del front, no defecto del diseno)
El chip de canonico del topbar esta dibujado en verde estatico (mockup del estado canonico). En la
implementacion debe DERIVARSE de la verificacion real (renderizar WORKING TREE/stale cuando no sea
canonico o el replay no de exit 0); el componente `canonical-indicator` ya prevee esa variante.

## Limites
Yo Analista: read-only, no promuevo, no consolido, no muto estado. El codigo/diseno se queda en
Zeus-protocol; al ledger del protocolo entra solo la cita en SPEC + el handoff atestado (DECISION-0049).
Tomar el insumo y registrar la transicion es tuyo (escritor unico) + GO del operador.
