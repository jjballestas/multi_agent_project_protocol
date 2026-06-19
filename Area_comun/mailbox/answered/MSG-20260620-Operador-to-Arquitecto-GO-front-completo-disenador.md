---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-front-completo-disenador
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: GO a COMPLETAR el front a "totalmente funcional" (sera mi herramienta de trabajo): etapa 5 roster RF-9 + etapa 6 multi-proyecto + RF-10 kickoff, de a una por SDD. Y ONBOARD del agente DISENADOR (operador APROBO) via la etapa 5 roster + re-genesis-boundary GOBERNADO (ventana propia, yo presente, copia limpia). Badge honesto sigue como AC duro. #4 epoca 1.14.0.
requested_action: "(1) Completar el front a totalmente funcional, de a una pieza (SDD, maker!=checker, badge-honesto AC duro): etapa 5 (roster RF-9: gestionar agentes/roles/modelos desde la UI, alta/baja via flujo de re-genesis-boundary), etapa 6 (multi-proyecto + RF-10 kickoff). (2) Onboard del agente DISENADOR (operador aprobo): preferible como PRIMER uso de la etapa 5 roster (el front onboardea al agente = dogfooding). Es ceremonia #4: re-genesis-boundary GOBERNADO en COPIA LIMPIA, operador PRESENTE, provisioning de su keypair (publica al registry pinned, privada wrapper-side). El operador confirma el MODELO/backend del Disenador. NO combinar la re-genesis con otra ventana de riesgo. (3) Cuando el front este completo, dejarlo ejecutable (npm start / server) para uso del operador."
question: "Confirmas: completar front (etapa 5 roster -> etapa 6/kickoff) de a una, y onboardear al Disenador via etapa 5 + re-genesis-boundary gobernado (ventana propia, yo presente)? Que datos necesitas de mi para el Disenador (modelo/backend, capacidades)?"
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0045-boundary-t0-sello-pre-t0.md
  - Area_comun/decisions/DECISION-0047-versionado-epoca-bajo-4.md
  - personal/operador/sintesis_hoja_de_ruta.html
deadline_or_blocking_level: normal
---

# GO: completar el front (totalmente funcional) + onboard del agente Disenador

El operador quiere el **front COMPLETAMENTE FUNCIONAL** -- es la herramienta con la que trabajara en
adelante. Completa el MVP, **de a una pieza**, SDD completo (maker=Codex / checker=Arquitecto), con el
**AC duro del badge honesto** vigente (derivar de validacion real, nunca verde hardcodeado).

## (1) Completar el front
- **Etapa 5 - roster (RF-9):** gestionar **agentes / roles / modelos** desde la UI. Alta/baja de agente =
  cambio del conjunto de firmantes -> **flujo de re-genesis-boundary gobernado** (presentado en la UI como
  ceremonia, no toggle; provisioning de clave A2). El registry sigue **pinned por el genesis** (propiedad de
  seguridad).
- **Etapa 6 - multi-proyecto + kickoff (RF-10):** selector de proyectos bajo `D:\Agentes\Zeus\` + lanzar un
  proyecto nuevo desde la UI (su primer handoff = T0 del nuevo proyecto).
- Al cerrar: dejar el front **ejecutable** (npm start / server) para uso diario del operador.

## (2) Onboard del agente DISENADOR (operador APROBO)
- Preferible como **PRIMER uso real de la etapa 5 roster** -> el front onboardea al agente (dogfooding del
  proprio mecanismo).
- Es **ceremonia #4**: **re-genesis-boundary GOBERNADO**, en **copia limpia** (leccion DECISION-0045: nunca
  contra el log vivo), **operador PRESENTE**, provisioning de su keypair (publica al registry; privada
  wrapper-side, fuera del repo). **Su propia ventana** -- no combinar con otra ventana de riesgo.
- **Datos que necesito confirmarte:** modelo/backend del Disenador (p.ej. claude) + capacidades
  (`tool_policy`: leer SPECs/requisitos, escribir artefactos de diseno en `Zeus-protocol/design/`, NO escribir
  codigo ni ledger directo; entrega a Codex). Dime que falta y lo confirmo.
- Su rol en el flujo: Arquitecto le entrega tarea de diseno -> Disenador produce diseno -> handoff a Codex
  (va ANTES de implementar). Su trabajo queda **atestado** = parte del dataset.

## Compliance
#4 epoca 1.14.0; el config pinned solo cambia en la re-genesis del onboard (batcheado/gobernado). Una
ventana de riesgo a la vez. Codigo en Zeus-protocol; gobernanza en Area_comun (dataset). Reproduccion del
checker desde clon limpio. PII-free. Canal ASCII. Reporta al cerrar cada pieza.
