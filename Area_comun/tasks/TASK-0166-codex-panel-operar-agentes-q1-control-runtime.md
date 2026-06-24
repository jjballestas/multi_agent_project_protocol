---
task_id: TASK-0166
title: "Proyecto-front: Panel Operar-Agentes Q1 -- control de runtime (indicador vivo/dormido + activar/detener por agente, allowlist) + 'Enviar al Arquitecto' desde el Intake (SPEC-0089, AC1-AC6)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0089
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-885632826E, REQ-9442785DD6]
linked_decisions: [DECISION-0057, DECISION-0050]
file: Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md
---

# TASK-0166 - Panel Operar-Agentes Q1: control de runtime (SPEC-0089)

> Segunda pieza del panel "Operar Agentes". Aprobada por el operador (REQ-885632826E + REQ-9442785DD6, mismo
> extraction TASK-EXTRACT-1F5C13A7B5). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (allowlist / no-bypass /
> no-autoridad / vivo-dormido derivado real). #4 byte-id; ASCII-only. Repo producto Zeus-protocol.

## Alcance (SPEC-0089 AC1-AC6)
- **AC1** Indicador vivo/dormido + ultimo latido por agente del agent_registry, DERIVADO del estado real del runtime
  (heartbeat/proceso), nunca estatico; fail-safe a "dormido/desconocido" (nunca falso-vivo).
- **AC2** Boton activar/detener runtime por agente: accion gobernada server-side, SOLO agente REGISTRADO (ALLOWLIST
  agent_id -> runtime conocido server-side, sin comando arbitrario / sin shell injection); runtime-only (DECISION-0057,
  no reconfigura identidad/keys/registry, no concede capabilities). agent_id no registrado/arbitrario -> 400, no ejecuta.
- **AC3** "Enviar al Arquitecto" en el Intake (REQ-885): registra el requisito por requirement-intake gobernado (ya
  existe) + notifica al Arquitecto por mailbox + despierta su runtime si dormido (AC2) + el front indica "tomado".
  Sin push manual del operador.
- **AC4** No-bypass / no-autoridad (carry AC17): activar no concede autoridad de riesgo ni crea ruta de escritura de
  estado fuera de lo gobernado; el agente sigue bajo sus capabilities; #4 sin tocar.
- **AC5** Estado claro + error AMABLE (carry AC72): "activando/deteniendo" + exito o mensaje amable (runtime no
  disponible / canal ocupado), no traceback crudo.
- **AC6** Off-by-default / sin riesgo nuevo; #4 byte-identica.

## DoD
- AC1-AC6 verdes con behavior-tests deterministas; carry AC16/AC17/AC58/AC72. node --test clon limpio exit 0;
  validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica.
- La ALLOWLIST es la barrera central: el server mapea agent_id->runtime conocido; NUNCA compone un comando del cliente.
  Behavior-test negativo: agent_id arbitrario -> rechazo, sin ejecucion.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA (allowlist sin comando
  arbitrario; activar no concede autoridad; vivo/dormido derivado real sin falso-vivo; no-bypass).
- REPRO: ver vivo/dormido por agente; activar un agente dormido -> vivo; en el Intake "Enviar al Arquitecto" -> requisito
  al canonico + MSG al Arquitecto + (si dormido) activado + "tomado".

## Notas
- "Vivo/dormido" se deriva de senal real (p.ej. mtime del heartbeat/cron log del agente, o proceso); definir la fuente
  canonica de heartbeat por agente; fail-safe a "dormido".
- DECISION-0057 ya autoriza al Arquitecto a activar/detener runtimes; el front expone ESA capacidad con rails (allowlist,
  runtime-only, honra stop). El despertar-al-destino que Q2 difirio se implementa aqui (AC3).
- NUNCA pilotar contra el log vivo: clon desechable para los repros de escritura gobernada.
