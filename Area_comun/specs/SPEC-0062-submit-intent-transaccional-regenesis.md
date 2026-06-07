---
spec_id: SPEC-0062-submit-intent-transaccional-regenesis
task_id: TASK-0076
type: implementation
status: ready
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0020, DECISION-0015]
relates_to: [SPEC-0058, TASK-0072, TASK-0038]
---

# SPEC-0062 - submit_intent transaccional multi-intent + herramienta de re-genesis

> Keystone de la ADOPCION de submit_intent por AMBOS lazos (orden del operador 2026-06-07). Habilita que
> Claude y el lazo autonomo de Codex dejen de editar los `*.json` a mano y usen submit_intent. Shadow:
> enforce/authoritative siguen OFF en esta tarea (sin flip). Bajo DECISION-0022 (no requiere decision nueva).

## 1. Objetivo

Hoy `runtime/submit_intent.py` aplica **un** intent por invocacion (task_status | task_upsert | claim |
decision) y exige **drift 0** antes de escribir (`ensure_clean_replay_base`). Pero cada cierre/encole real de
ambos lazos es **multi-intent atomico** (p.ej.: `task_status` done + `claim` release + `task_upsert` de la
nueva tarea + `decision`), y el estado vivo hoy tiene **drift** (modo sombra con edicion manual). Sin (a) un
modo transaccional multi-intent y (b) una herramienta de re-genesis que ponga drift a 0, **ningun lazo puede
reemplazar sus scripts de edicion directa por submit_intent**. Esta tarea entrega ambos enablers, validados en
sombra.

## 2. Alcance (aditivo, off-by-default, sin flip de enforce)

1. **submit_intent transaccional multi-intent.** Aceptar una **secuencia ordenada de intents** en una sola
   invocacion que se aplica de forma atomica: o se aplican todos (un append por intent, materializacion final,
   drift 0) o se revierte todo (rollback de archivos + runtime state, como ya hace el camino mono-intent).
   - CLI: `--intents <archivo.json|->` con `{"actor_id","timestamp","commit","intents":[ ... ]}` (o
     `--intents-json`). Mantener el `--intent` mono-intent actual por compatibilidad.
   - Validacion: cada intent se valida en orden contra el estado **resultante de aplicar los previos** (no solo
     el inicial), para que `claim acquire` -> `task_status` -> `claim release` en la misma transaccion sea
     coherente. Idempotencia por-intent (idempotency_key) + idempotencia de la transaccion completa.
   - Rollback total ante fallo de cualquier intent (backups ya existentes de archivos + runtime state).
2. **Herramienta de re-genesis.** `runtime/regenesis.py` (o subcomando) que emite un **genesis fresco por
   referencia** desde el estado **materializado actual** (snapshot content-addressed), dejando **drift 0** y
   un event log con el nuevo genesis como base. Idempotente, determinista (timestamp/commit provistos),
   verificable (tras re-genesis: `protocol_state_drift` -> has_drift False). NO destructivo del historico
   (archiva/renombra el event log previo o parte desde snapshot ref, segun diseno mas simple y reversible).
3. **Golden deterministas (sin red):**
   - Una transaccion de cierre real (multi-intent: status done + claim release + task_upsert + decision) pasa
     con **drift 0** y deja el ledger materializado esperado.
   - Fallo de un intent intermedio -> **rollback total** (estado byte-identico al previo).
   - Re-genesis sobre un estado con drift -> **drift 0** y base limpia; submit_intent posterior funciona.
   - Idempotencia: repetir la transaccion no duplica.
4. **Paridad** `.ps1` donde aplique (o delegacion) + CI.

## 3. Fuera de alcance (otras rebanadas)

- **NO** encender `enforce`/`authoritative` (eso es la rebanada de ACTIVACION, con GO del operador + ensayo de
  rollback + verificacion de que AMBOS lazos ya usan submit_intent).
- Mailbox: los mensajes **no** son estado-autoritativo del ledger; siguen siendo archivos bajo claim (se
  documenta; submit_intent no los maneja).
- El mandato en protocolo (AGENTS.md/TASK_PROTOCOL: "submit_intent es el unico write-path bajo enforce") lo
  redacta el arquitecto en la rebanada de cutover.

## 4. Invariantes de seguridad

1. Off/sombra => byte-equivalente; edicion manual sigue valida hasta el flip (que NO ocurre aqui).
2. Transaccion atomica: todo-o-nada; rollback deja el estado byte-identico al previo.
3. Drift 0 tras cada transaccion exitosa y tras re-genesis.
4. Determinista (timestamp/commit provistos; sin reloj/red). Sin secretos. Neutral de dominio.
5. Reversible: re-genesis no destruye trazabilidad; el event log previo se conserva/archiva.

## 5. Criterios de cierre (DoD)

submit_intent acepta una transaccion multi-intent atomica (con rollback) + `regenesis` deja drift 0 + golden
que prueban cierre-real multi-intent, rollback ante fallo, re-genesis->drift0 y idempotencia; paridad/CI;
gates verdes (validador con drift de sombra esperado SOLO donde aun no se re-genesisa en el fixture);
handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020). **Sin flip de
enforce.**

## 6. Secuencia

Tras esta tarea (enablers listos): el arquitecto redacta el cutover (mandato en protocolo) + ambos lazos
adoptan submit_intent en sombra; luego, con GO del operador, re-genesis del repo vivo + flip
enforce+authoritative + ensayo de rollback. F7.5 (docs de release firmado) queda pendiente, post-migracion.
