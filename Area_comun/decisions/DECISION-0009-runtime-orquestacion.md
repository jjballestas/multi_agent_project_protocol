---
decision_id: DECISION-0009
title: Adoptar un runtime de orquestación automatizada (opt-in, off by default)
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0006, DECISION-0007, DECISION-0008, DECISION-0001, TASK-0026]
phase: P2
---

# DECISION-0009 — Runtime de orquestación automatizada

## Contexto
Hoy el protocolo **documenta** la coordinación (tasks, claims, mailbox, handoffs) pero un humano
ejecuta cada paso a mano (abrir sesión, copiar contexto, lanzar al otro agente, mover el mailbox,
actualizar estado). Propuesta del **operador humano** (entregada vía agente externo) con diseño
completo en [DISENO-runtime-orquestacion-automatizada.md](../artifacts/DISENO-runtime-orquestacion-automatizada.md):
añadir un **plano de control (`runtime/`)** que invoca agentes y aplica las transiciones de estado.

> **Nota de numeración:** el diseño reservaba "DECISION-0008", pero ese ID ya se publicó para
> **eficiencia de tokens**. Esta decisión toma **DECISION-0009**. Los dos tracks corren **en paralelo**.

## Decisión
Se **adopta** el runtime de orquestación tal como lo fija el diseño (§1 principios no negociables):

- **Capa `runtime/` opt-in y off-by-default** (`runtime` en `protocol.config(.template).json`,
  `enabled:false`). Una instancia sin el bloque se comporta **exactamente como hoy**.
- **Ficheros = fuente de verdad** (sin servidor ni base de datos): preserva dogfooding y auditabilidad.
- **1 turno = 1 commit** (trazabilidad total + rollback atómico).
- **Gate por turno**: validador + scan de neutralidad tras cada turno; si falla ⇒ `git revert` +
  `blocked` + escala al humano.
- **Gates humanos como paradas duras**: `human_approval_points` (`DECISION_REQUIRED`/`HUMAN_REQUIRED`/
  release MAJOR) detienen el loop; no son sugerencias.
- **Adapters vendor-neutral** (interfaz `AgentAdapter`): el protocolo deja de estar acoplado a
  Claude/Codex; son dos adapters de muchos. "Manual mode" como adapter de respaldo.
- **Determinismo donde se pueda**: router, transiciones y gates son código; solo el *contenido* lo
  produce el agente, encapsulado en un **contrato de turno** estricto (`turn_schema.json`).
- **Claim como lock previo a `adapter.run()`** (DECISION-0007): el `from` de cada transición debe casar.

## Aprobación humana
El operador humano **aprobó abrir este track en paralelo** (2026-06-05). Sigue requiriendo
aprobación humana explícita: **la primera corrida autónoma del piloto** y cualquier endurecimiento
(quitar dry-run / gate humano). Releases MAJOR mantienen la aprobación de DECISION-0001.

## Activación (2026-06-06)
El operador humano **aprobó activar `runtime.enabled:true` en esta instancia viva** (post-v0.8.0, con
runtime M0+M1 completos). Registro del acto y su alcance:

- **Cambio:** `protocol.config.json` (instancia viva) `runtime.enabled: false → true`. La
  **`protocol.config.template.json` permanece `false`**: las instancias nuevas siguen naciendo apagadas.
- **Qué habilita hoy:** `runtime/orchestrator.py --run` deja de abortar y **opera sobre el repo vivo**
  cuando se invoca explícitamente (`--run --replay-report …`), con **gate por turno + 1 commit/turno +
  paradas humanas duras**. Solo existe el **`replay` adapter** (determinista); no hay automation que lo
  dispare por sí solo.
- **Qué sigue gateado (sin cambio):** los **adapters LLM reales** (`claude_adapter`/`codex_adapter`) y el
  **loop autónomo del piloto** son **M2** y requieren su propia aprobación; **endurecer** (quitar
  dry-run/gate humano, escribir estado sin contrato de turno) sigue siendo **MAJOR**.
- **Reversible:** volver a `false` restaura el comportamiento previo (instancia sin bloque = como hoy).

## Versionado y neutralidad (DECISION-0001)
Por ser **aditivo y off-by-default** ⇒ **MINOR, target v0.8.0** (track separado del de eficiencia de
tokens v0.7.0). Endurecer (auto-aplicar sin gate humano, escribir estado sin contrato de turno) sería
**MAJOR**. `runtime/**` es **tooling neutral**: se añade a `scan_globs` de neutralidad (`.py/.ps1`).

## Backlog (del diseño §7; SDD activado, tareas de un solo owner)
- **TASK-0026** (Claude, analysis, M0): contrato de turno (`turn_schema.json`) + SPEC del router.
- M0+: `runtime/` skeleton con `--plan` dry-run (Codex); wrapper git + write-allowlist + gate por
  turno (Codex); `claude_adapter` un turno real (Codex); `codex_adapter` + loop + mailbox automation
  (Codex); gates humanos + budget + run-log (Claude diseño / Codex impl); **piloto** sobre una
  instancia real con métricas de ROI.

## Consecuencias
- **Positivas:** la coordinación deja de ser manual; trazabilidad por commit/turno; vendor-neutral;
  base para medir ROI real (turnos/tarea, colisiones, coste) — conecta con DECISION-0008 (tokens).
- **Costo:** una capa nueva (`runtime/`) a mantener; superficie de seguridad (write-allowlist, gates).
- **Seguimiento:** TASK-0026 (M0) y el backlog §7; la capa se publica como **v0.8.0** al madurar.

## Alternativas consideradas
- **Seguir 100% manual:** descartado — no escala; el operador ejecuta cada paso.
- **Servidor/cola/DB externos:** descartado — rompería el modelo file-based y la auditabilidad.
- **Acoplar al par Claude/Codex:** descartado — la interfaz de adapter mantiene la neutralidad de vendor.
