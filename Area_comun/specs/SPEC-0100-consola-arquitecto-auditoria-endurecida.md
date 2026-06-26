---
spec_id: SPEC-0100
task_id: TASK-0187
type: security
status: accepted
linked_decisions:
  - DECISION-0062
  - DECISION-0040
  - DECISION-0050
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0100 - Consola del Arquitecto pieza 3: auditoria endurecida (store controlado + guarda PII)

## Context

DECISION-0062 (accepted) + piezas 1 (proceso-puente, TASK-0185) y 2 (UI, TASK-0186) cerradas. La pieza 1 ya deja
un `audit.jsonl` minimo redactado (sin PII, fuera del #4). **Pieza 3 = endurecer esa auditoria**: store controlado,
estructurado, acotado, con redaccion PII robusta, NUNCA al dataset atestado. maker=Codex / checker=Arquitecto.
Repo = Zeus-protocol.

## Scope

- **Store de auditoria controlado** (bajo `.runtime/architect-bridge/`, gitignored, fuera del dataset atestado):
  registra por sesion los eventos de ciclo (open/stop), cada mensaje del operador y cada salida del Arquitecto,
  con `sessionId` + timestamp + tipo.
- **Redaccion PII robusta:** reusar el screening/redaccion del producto (familias enumerables: email, telefono,
  documento, direccion, NIT, cuenta) sobre TODO lo que se persista (no solo un patron).
- **Acotado/retencion:** el store no crece sin limite (rotacion o tope de tamano/entradas por sesion), documentado.
- **NUNCA al #4:** la auditoria no toca `runtime/state/events.jsonl` ni el ledger; el modulo no importa escritores.

## Acceptance Criteria

- **AC1 (store estructurado por sesion):** el audit registra ciclo (open/stop) + mensajes del operador + salidas del
  Arquitecto con `sessionId`/timestamp/tipo, en `.runtime/architect-bridge/` (gitignored). Behavior-test.
- **AC2 (redaccion PII robusta, prueba negativa PERMANENTE):** enviar un mensaje con PII de varias familias
  (email/telefono/documento/direccion/NIT/cuenta) -> NINGUN literal aparece en el store de auditoria. Extiende la
  prueba minima de pieza 1 a las familias enumerables.
- **AC3 (nunca al #4 / no concede autoridad):** el modulo de auditoria NO importa escritores del ledger/event-log
  y NO escribe `Area_comun/state/*` ni `runtime/state/events.jsonl`. Test de imports + byte-identidad del ledger.
- **AC4 (acotado/retencion):** el store esta acotado (rotacion o tope por sesion); un volumen alto de eventos no lo
  hace crecer sin limite. Behavior-test del bound; documentar la politica.
- **AC5 (gated por el puente / off-by-default):** la auditoria solo opera cuando el puente esta activo; con el
  puente disabled no se crea store. Consistente con off-by-default.
- **AC6 (gates):** `npm test` (rapido) verde + casos en el tier CI (`npm run test:ci` en VENTANA QUIETA: 98/...
  100% pass); protocolo `validate_collaboration_state.py` exit 0 (con/sin secretos), drift 0,
  scan_encoding/neutrality exit 0; `protocol.config.json`/genesis intactos; Co-Authored-By Codex.

## Out of scope

- UI de revision del audit (si se quiere, tarea posterior); el store es para auditoria/forense, no panel.
- Consolas para otros agentes; NOVA; multi-tenant; alta/baja de agente (RF-9).
- Cualquier persistencia de audit en el dataset atestado o en el #4 (prohibida).

## Notes

- La auditoria es evidencia controlada de coordinacion, NO parte del dataset atestado (DECISION-0038/0040): por eso
  gitignored + redactada + acotada. Endurece lo que pieza 1 dejo minimo.
- Repo producto Zeus-protocol; clon en Windows: `git -c core.longpaths=true`. Checker corre test:ci en ventana
  quieta (sin peers mid-exec; el full-suite flakea bajo carga, deuda TASK-0182).
