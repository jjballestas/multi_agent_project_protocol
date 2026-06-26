---
task_id: TASK-0187
title: "Consola del Arquitecto pieza 3: auditoria endurecida (store controlado + guarda PII, acotado, nunca al #4) (SPEC-0100, DECISION-0062)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0100
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: TASK-0178 / DECISION-0062 (consola del Arquitecto; pieza 3)
reuses: [TASK-0185, TASK-0186]
linked_decisions: [DECISION-0062, DECISION-0040, DECISION-0050]
file: Area_comun/tasks/TASK-0187-codex-consola-arquitecto-auditoria-pieza3.md
---

# TASK-0187 - Consola del Arquitecto, pieza 3 (auditoria endurecida)

> maker=Codex / checker=Arquitecto. Repo = Zeus-protocol. Endurece el audit minimo de pieza 1 (TASK-0185). NO
> toca #4/config. Off-by-default (gated por el puente).

## Alcance (SPEC-0100 AC1-AC6)
- **Store de auditoria controlado** en `.runtime/architect-bridge/` (gitignored, fuera del dataset): por sesion,
  ciclo (open/stop) + mensajes del operador + salidas del Arquitecto, con sessionId/timestamp/tipo.
- **Redaccion PII robusta** (familias enumerables: email/telefono/documento/direccion/NIT/cuenta) sobre todo lo
  persistido.
- **Acotado/retencion** (rotacion o tope por sesion), documentado.
- **Nunca al #4:** no importa escritores del ledger/event-log; no escribe Area_comun/state ni events.jsonl.

## DoD (= SPEC-0100 AC1-AC6)
- AC1 store estructurado por sesion (ciclo + mensajes + salidas; sessionId/timestamp/tipo; gitignored).
- AC2 redaccion PII robusta (prueba negativa PERMANENTE): PII de varias familias -> ningun literal en el audit.
- AC3 nunca al #4 / no concede autoridad (test de imports + byte-identidad del ledger).
- AC4 acotado/retencion (bound por sesion; volumen alto no crece sin limite).
- AC5 gated por el puente / off-by-default (disabled -> no se crea store).
- AC6 gates: npm test rapido verde + test:ci en VENTANA QUIETA 100% pass; protocolo validate exit 0 (con/sin
  secretos), drift 0, encoding/neutralidad exit 0; config/genesis intactos; Co-Authored-By Codex.

## Fuera de alcance
- UI de revision del audit (tarea posterior); consolas para otros agentes; NOVA; multi-tenant; RF-9.
- Persistencia de audit en el dataset atestado o en el #4 (prohibida).

## Notas
- Auditoria = evidencia controlada de coordinacion, NO dataset atestado (gitignored + redactada + acotada).
  Reusa el screening/redaccion del producto. Checker corre test:ci en ventana quieta (sin peers mid-exec).
