---
message_id: MSG-20260620-Arquitecto-to-Operador-confirma-front-completo-disenador
type: RESPONSE
task_id: none
from: Arquitecto
to: Operador
requires_response: true
response_owner: Operador
status: open
one_line_summary: CONFIRMO completar el front de a una pieza (etapa5 roster RF-9 -> etapa6 multi-proyecto/kickoff RF-10), maker=Codex/checker=Arquitecto, badge-honesto AC duro. Onboard del Disenador via etapa5 roster = ceremonia #4 re-genesis-boundary gobernada (copia limpia, tu presente, ventana propia). Te pido datos concretos del Disenador (abajo) + propongo hacer ANTES un endurecimiento pequeno (test de comportamiento del badge, recomendacion del Analista) por ser el AC duro de aqui en mas.
requested_action: "Confirmar (a) el Disenador propuesto (id=Disenador / modelo-backend a definir / capacidades minimo-privilegio / keypair) o ajustarlo, indicando el modelo/backend concreto; y (b) la secuencia: primero el endurecimiento badge-honesto (test de comportamiento, pieza chica) y luego etapa5 roster -> onboard Disenador -> etapa6, o saltar directo a etapa5. Con eso autoro el SDD de etapa5 + el plan de ceremonia del onboard."
question: "Confirmas (a) el Disenador propuesto (id/modelo/capacidades/keypair) o que ajusto; y (b) la secuencia: primero el endurecimiento badge-honesto (test de comportamiento, ~1 pieza chica) y luego etapa5 roster -> onboard Disenador -> etapa6? O prefieres saltar directo a etapa5?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260620-Operador-to-Arquitecto-GO-front-completo-disenador.md
  - Area_comun/mailbox/open/MSG-20260620-Analista-to-Arquitecto-TASK-0128-recomendacion.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
deadline_or_blocking_level: normal
---

# Confirmo: completar el front + onboard del Disenador

## (1) CONFIRMADO el plan
- Completar el front a totalmente funcional, **de a una pieza**, SDD completo (maker=Codex / checker=Arquitecto),
  con el **AC duro badge-honesto** vigente (derivar de validacion real, nunca verde hardcodeado), reproduccion
  del checker desde clon limpio, PII-free, gobernanza en Area_comun (dataset) / codigo en Zeus-protocol.
- Secuencia: **etapa 5 roster (RF-9)** -> **etapa 6 multi-proyecto + kickoff (RF-10)**. Al cerrar, front
  ejecutable (npm start) para tu uso diario.
- **Onboard del Disenador = PRIMER uso real de la etapa 5 roster** (dogfooding del mecanismo): ceremonia #4
  **re-genesis-boundary GOBERNADO**, en **copia limpia** (DECISION-0045: nunca contra el log vivo), **tu
  presente**, **su propia ventana** (no combinada con otra ventana de riesgo), provisioning de su keypair
  (publica al registry pinned por el genesis; privada wrapper-side fuera del repo). Registry sigue pinned.

## (2) Datos que necesito del Disenador -- propongo defaults, confirma o ajusta
- **id de agente:** `Disenador` (ASCII).
- **modelo/backend:** CONFIRMA cual (p.ej. claude-opus-4-8 u otro). Lo necesito para el agent_registry.
- **capacidades (tool_policy), minimo privilegio:**
  - LEE: `Area_comun/` (SPECs, tasks, requisitos) + `Zeus-protocol/design/`.
  - ESCRIBE: SOLO `Zeus-protocol/design/` (artefactos de diseno).
  - NO escribe codigo (ningun otro path de Zeus-protocol) ni ledger directo (no submit_intent de
    code/state). Su entrega va por **handoff a Codex** (diseno ANTES de implementar).
- **atestacion de su trabajo:** como NO escribe ledger directo, su handoff de diseno lo **atesta el flujo
  gobernado** (yo registro el handoff via submit_intent citando el artefacto por hash) -> queda en el dataset.
  Su keypair entra al registry igual (firmante futuro / propiedad del roster), aunque hoy su tool_policy le
  veda escribir el ledger. CONFIRMA si quieres que firme sus propios handoffs (le abro esa capacidad) o que
  los atieste yo (default).
- **rol en el flujo:** Arquitecto -> tarea de diseno -> Disenador produce diseno -> handoff a Codex -> Codex
  implementa -> Arquitecto checker. Su diseno = parte del dataset atestado.

## (3) Recomendacion de secuencia (Analista) -- mi sugerencia
El Analista recomienda (no bloqueante) endurecer la **honestidad de estado** con un **test de comportamiento**
(inyectar una verificacion-runtime que FALLA y asegurar badge **no-verde**; y todo-valido -> verde), porque el
test actual es string-match (prueba presencia, no comportamiento; un refactor podria repintar verde y pasar).
Como el badge-honesto es ahora **AC duro de todo el front**, **recomiendo hacerlo YA como pieza chica** (las
funciones ya son inyectables; coste bajo) **antes de la etapa 5**, y dejar "test de comportamiento del badge"
como **AC permanente** de etapa 5/6. Asi la propiedad-tesis queda regresion-proof antes de agregar mas UI.
Si prefieres velocidad, lo pliego como primer sub-AC de etapa 5. **Tu decides (b) arriba.**

## Proximo paso mio
En cuanto confirmes (a) y (b), autoro el SDD: SPEC refinada + task de la **etapa 5 roster** para Codex (con
badge-honesto + test de comportamiento como AC) y el **plan de ceremonia** del onboard del Disenador (copia
limpia, re-genesis-boundary, tu presente, rollback armado). El mecanismo del roster puedo empezar a disenarlo
sin esperar tus datos del Disenador (esos solo hacen falta para la ceremonia de onboard, que es el primer uso).

Compliance: #4 epoca 1.14.0 pinned (solo cambia en la re-genesis del onboard, batcheada/gobernada). Una
ventana de riesgo a la vez. Canal ASCII.
