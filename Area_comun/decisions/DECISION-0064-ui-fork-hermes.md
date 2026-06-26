---
decision_id: DECISION-0064
title: UI del operador como fork de Hermes Workspace (MIT) = cliente del single-writer; contrato /api/governance/*; GATEADO a post-TFM
status: proposed
ratified_at: null
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0050, DECISION-0022, DECISION-0028, DECISION-0020, DECISION-0040, DECISION-0062]
phase: P2
---

# DECISION-0064 - UI del operador sobre un fork de Hermes (cliente del single-writer)

> PROPUESTA, **parqueada para la Fase B (post-TFM)**. El operador investigo montar la UI del panel sobre un fork
> de **Hermes Workspace** (`outsourc-e/hermes-workspace`, MIT) en vez de construir el chrome desde cero. Plan
> detallado del operador en `personal/operador/Hermes/` (README + PLAN_INTEGRACION + PROMPT + control.html).
> **No se activa hasta que la medicion del TFM este congelada/capturada** (no cambiar el core bajo medicion).

## Contexto

DECISION-0050 fijo el front como panel del operador (codigo en repo producto bajo `D:\Agentes\Zeus\`). En vez de
seguir construyendo el chrome (shell/chat/terminal/skills/memoria/layout/movil), se forkea Hermes (MIT, ya provee
ese chrome) y se monta ENCIMA la gobernanza especifica de la metodologia. La direccion sana es **"su UI sobre tu
metodologia"**: el runtime es la fuente de verdad / single-writer; la UI **lee** slim views y **escribe solo** via
`submit_intent`.

## Decision

1. **La UI es CLIENTE del single-writer (DECISION-0022/0028).** Toda mutacion de estado pasa por
   `runtime/submit_intent.py` (transaccion atomica); el hard-gate B.3 rechaza ediciones manuales del ledger como
   drift. **Ningun camino UI/Node escribe `Area_comun/state/*.json`.** La inversa romperia `enforce/authoritative`.
2. **Contrato `/api/governance/*`:** lectura (health/state/backlog/mailbox/decisions/handoffs/ledger) sobre slim
   views (read-only, cold-start barato); escritura `POST /api/governance/intent` -> `submit_intent --intents`
   (kinds `task_status`/`task_upsert`/`claim`/`decision`). Anti-colision DECISION-0020 + manejo legible de B.3.
3. **Reuso de zeus-protocol:** se portan las **vistas/logica de gobernanza** (Intake RF-14, Mailbox, Backlog,
   Artifacts, consola agente-a-agente, Operate); se **descarta el chrome** que Hermes ya hace mejor.
4. **Licencia:** conservar `LICENSE` MIT + avisos de copyright de Hermes; renombrar el fork (copyright != marca);
   anadir copyright propio a archivos nuevos; mantener el protocolo propietario como **backend separado** (no
   mezclar core propietario con archivos MIT). *No es asesoria legal.*
5. **Fases con gates** (del plan del operador): F0 fork+seams+inventario -> F1 read-only -> F2 write-through ->
   F3 chat/multiproyecto -> F4 hardening. SDD por fase, maker=Codex / checker=Arquitecto.
6. **GATE de orden (clave):** **NO arrancar las fases de build (F1+) hasta que la medicion del TFM (H1-H3) este
   congelada/capturada.** Razon: un build grande sobre el core durante la ventana de medicion contamina el
   experimento (cambia el sistema, el dataset, el sobrecoste) y anade un writer-path nuevo que el modelo de
   amenaza A2 tendria que re-contemplar. La **F0** (fork privado + pin + seams + inventario, todo fuera del core)
   es segura de hacer en cualquier momento.

## Alcance / No-alcance

- **En alcance:** la UI del operador como cliente del single-writer sobre un fork de Hermes; el contrato
  `/api/governance/*`; reuso de la gobernanza de zeus; estrategia de licencia.
- **Fuera de alcance:** cambiar el core neutral; tocar el mecanismo #4; medir el TFM (eso es el pre-registro +
  GATE-DATASET); cualquier escritura directa al ledger desde la UI.

## Consecuencias

- El operador obtiene un panel ergonomico sin reinventar shell/chat/terminal, sobre un protocolo ya probado.
- El trabajo de gobernanza de zeus-protocol se reusa (no se pierde); el chrome (incl. parte de la consola del
  Arquitecto) se sustituye por lo nativo de Hermes.
- Riesgos (del plan): romper single-writer (mitiga guard F2.2), churn del API de Hermes (pin F0.2), sandbox stale
  (ejecutar desde entorno real), contaminacion de licencia (backend separado), sobre-alcance (respetar gates).

## Alternativas consideradas

- **Seguir construyendo el chrome en zeus-protocol:** mas trabajo, peor ergonomia; descartado salvo como fuente
  de componentes de gobernanza a portar.
- **UI como escritor del estado:** rompe single-writer/enforce; descartado (la UI es cliente, nunca escritor).
