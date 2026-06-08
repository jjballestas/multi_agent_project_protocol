---
spec_id: SPEC-0065-team-bridge-capas-AB
task_id: TASK-0083
type: design
status: ready
created_at: 2026-06-08
author: Claude (arquitecto)
linked_decisions: [DECISION-0025, DECISION-0022, DECISION-0018, DECISION-0017, DECISION-0009]
relates_to: [TASK-0038]
---

> PROMOVIDA por Claude (2026-06-08). Diseno tecnico del bridge Agent Teams -> protocolo, **solo
> Capas A+B** (DECISION-0025 ACCEPTED, alcance A+B). Capa C DIFERIDA a precondiciones DECISION-0022.

# Diseno - Bridge Agent Teams <-> protocolo ledger (Capas A+B)

## 1. Objetivo

Componer los hooks de Agent Teams (`TaskCreated`/`TaskCompleted`/`TeammateIdle`) con los mecanismos
existentes del protocolo, **sin** convertir al motor en vivo en escritor del ledger. Alcance:
- **Capa A (gate enforcement):** correr los gates existentes al cierre de tarea / idle de teammate y
  **bloquear** (`exit 2`) si fallan.
- **Capa B (audit append-only):** anexar cada evento a un journal durable sin mutar estado canonico.

Off-by-default, opt-in por registro, neutral de dominio, reversible. Conforme a DECISION-0025.

## 2. Estado actual (punto de partida real, ya en el repo)

Ya existen y se REUSAN (no se reconstruyen): `scripts/validate_collaboration_state.py`,
`scripts/scan_domain_neutrality.py`, `runtime/turn_validate.py`, `runtime/submit_intent.py` (gate
B.3, no usado por A+B), event log/snapshots (DECISION-0017), `scan_globs` de neutralidad. El bridge
solo orquesta estos componentes ante eventos de hook; no duplica logica.

## 3. Componentes nuevos

| # | Componente | Donde | Comportamiento |
|---|-----------|-------|----------------|
| C1 | Registro de activacion | `protocol.config.json` / `protocol.config.template.json`: `runtime.team_bridge {enabled:false, layers:[], activation_decision:"", approved_by:"", approved_at:""}` | Sin registro valido (o `enabled:false`) => `team_bridge.py` es no-op de estado: NO corre gates ni escribe audit, sale 0 (byte-equivalente al repo actual). Funcion `team_bridge_activation_error(config)` analoga a las existentes. |
| C2 | Entrypoint del bridge | `runtime/team_bridge.py --event <TaskCreated\|TaskCompleted\|TeammateIdle>` | Lee el payload del evento como JSON por **stdin**. Despacha a Capa A y/o B segun `layers`. |
| C3 | Capa A - gates | `team_bridge.py` -> subprocess de validador + neutralidad [+ `turn_validate` si configurado] | En `TaskCompleted`/`TeammateIdle`, si "gate" en `layers`: corre los gates; si alguno falla, imprime el detalle a **stderr** y retorna **2** (Agent Teams bloquea el cierre / mantiene al teammate). Si pasan, retorna 0. |
| C4 | Capa B - audit | `Area_comun/state/team_audit.jsonl` (append-only) | Si "audit" en `layers`: anexa una linea JSON `{observed_at, hook, ...payload}` por evento, sin mutar `state/*.json`. `ensure_ascii=True`. Crea el archivo/dir si falta. |
| C5 | Fail-closed / no-revienta | `team_bridge.py` | Error inesperado en Capa B no debe romper el team: se captura y (si audit activo) se intenta registrar; nunca propaga excepcion no controlada. Capa A es el unico camino que retorna 2 (intencional). |

**Capa C explicitamente FUERA de alcance:** `team_bridge.py` NO llama `submit_intent` ni mapea
estado en esta tarea. Si un evento trae `[TASK-XXXX]`, en A+B solo se audita (Capa B). El gancho de
C se deja documentado pero inerte/diferido (DECISION-0025 sec.3).

## 4. Contrato de configuracion (off-by-default)

`protocol.config.template.json` (master) y `protocol.config.json` (instancia viva) ganan:
```json
{ "runtime": { "team_bridge": {
    "enabled": false, "layers": [],
    "activation_decision": "", "approved_by": "", "approved_at": "" } } }
```
Activar A+B en la instancia viva (paso separado, registrado) seria:
`{"enabled":true,"layers":["gate","audit"],"activation_decision":"DECISION-0025",...}`.
La tarea entrega el bloque **off** (`enabled:false, layers:[]`): NO enciende nada.

## 5. Neutralidad y secretos

- `runtime/team_bridge.py` se anade a `scan_globs` del scan de neutralidad.
- Sin terminos de dominio, sin secretos. `team_audit.jsonl` no se versiona con contenido de runs
  reales (vacio/ausente por defecto; .gitignore si aplica, o solo se crea al activar).

## 6. Tests (recorded fixtures, deterministas)

- `examples/team_bridge_cases/` (o equivalente): payloads grabados de los 3 hooks.
- Golden:
  1. **off-sin-flag** => no-op, sale 0, no crea audit, no corre gates (byte-equivalente).
  2. **audit-only** (`layers:["audit"]`) => anexa linea correcta al jsonl; no corre gates.
  3. **gate-pass** (`layers:["gate"]`, estado verde) => corre gates, sale 0.
  4. **gate-fail** (estado intencionalmente roto en fixture aislado) => sale 2 + mensaje a stderr.
  5. **A+B** (`layers:["gate","audit"]`) => audita y aplica gate.
  6. **evento con [TASK-XXXX]** => en A+B solo audita (no toca ledger; Capa C inerte).
- Regresiones existentes (validador/neutralidad/runtime) verdes. Reloj/IDs deterministas via fixture.

## 7. Definicion de hecho (DoD)

- `runtime/team_bridge.py` (Capas A+B) + bloque `runtime.team_bridge` off-by-default en template e
  instancia + alta en `scan_globs` + golden `team_bridge_cases` verdes + regresiones verdes.
- Off => byte-equivalente al repo actual. Neutral, sin secretos.
- Capa C ausente (diferida). Handoff autocontenido a Claude para ratificacion adversarial.

## 8. Fuera de alcance

- Activar el bridge en la instancia viva (paso separado, registrado).
- Capa C (mapeo autoritativo via `submit_intent`): diferida a precondiciones DECISION-0022.
- Cualquier cambio a `.claude/settings.json` vivo (los hooks se cablean al activar, no aqui).
