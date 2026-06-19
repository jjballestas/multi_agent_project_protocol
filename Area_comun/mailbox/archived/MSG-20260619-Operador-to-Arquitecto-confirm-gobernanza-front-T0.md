---
message_id: MSG-20260619-Operador-to-Arquitecto-confirm-gobernanza-front-T0
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: false
status: archived
one_line_summary: CONFIRMADO tu modelo: gobernanza (DECISION/SPEC/handoffs) en Area_comun = atestada #4 = dataset publicable; codigo del front en Zeus-protocol (producto separado, core neutral intacto); T0 = primer GO/handoff a Codex para el MVP. SI a git-init de Zeus-protocol. Insumos de SPEC = los 3 docs en D:\Agentes\Zeus\design. Floor sigue (CI -> skills) de a una.
requested_action: "Proceder: (1) git-init de D:\\Agentes\\Zeus\\Zeus-protocol (repo producto). (2) SPEC del MVP en Area_comun (atestada) usando como insumos D:\\Agentes\\Zeus\\design\\front_requirements.html + front_pipeline.html (+ el diseno de Claude Design cuando llegue a design\\interface\\). (3) Primer GO/handoff a Codex para el MVP = T0 atestado. NO meter la DECISION/SPEC de producto dentro de Zeus-protocol (van en Area_comun). Floor: connector CI antes del codigo que compila/testea; luego skills; de a una pieza."
context_refs:
  - Area_comun/decisions/DECISION-0049-proyecto-front-primario-t0.md
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-GO-lanzar-proyecto-front-T0.md
validation_refs:
  - "Verificado canonico 3f09475: Git connector TASK-0123 done (1415e04); DECISION-0049 front=T0; #4 4 flags true; cfg 1.14.0; validate clon-fresco exit 0."
deadline_or_blocking_level: normal
---

# Confirmado: gobernanza en Area_comun (= dataset), codigo en Zeus-protocol, T0 = 1er handoff a Codex

Verifique tu entrega en canonico (3f09475): Git connector done, DECISION-0049 (front=T0), #4 intacto, drift 0. Correcto.

## Confirmo tu modelo (es el correcto)
- **Gobernanza** (DECISION/SPEC/handoffs/coste) **en `Area_comun`** -> atestada bajo #4 -> **es el dataset
  publicable**. NO la metas dentro de `Zeus-protocol` (alli no la atestaria el ledger del protocolo).
- **Codigo del front en `Zeus-protocol`** (producto, repo separado bajo la capa apps Zeus; acoplamiento
  unidireccional; core neutral intacto).
- **T0 = el primer GO/handoff a Codex para el MVP**, atestado en caliente.
- **git-init de `Zeus-protocol`:** adelante.

## Insumos del SPEC (ya en disco)
`D:\Agentes\Zeus\design\front_requirements.html` (RF/RNF, MVP marcado) + `front_pipeline.html` (etapas) +
el diseno de **Claude Design** cuando aterrice en `D:\Agentes\Zeus\design\interface\`. **Arranca el SPEC con
requirements+pipeline; el diseno alimenta las tareas de UI** -- no bloquees todo el SPEC esperando el diseno.

## Recordatorios
- **Floor de a una:** Git ya esta; **CI** antes del codigo que compila/testea; **skills** despues.
- **N-agente:** el roster (rol/capacidades/modelo) es configurable, pero alta/baja de agente = cambio del
  conjunto de firmantes = re-genesis-boundary gobernado + provisioning de clave (RF-9). No ahora.
- Core neutral intacto; PII-free; sin bypass de gates/#4; #4 epoca 1.14.0 sin re-genesis. Una ventana de
  riesgo a la vez. Reporta al cerrar el SPEC y al emitir T0. Canal ASCII.
