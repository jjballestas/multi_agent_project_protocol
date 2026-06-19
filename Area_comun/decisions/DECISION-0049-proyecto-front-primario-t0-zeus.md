---
decision_id: DECISION-0049
title: Proyecto-front (UI single-operator) como proyecto PRIMARIO de tesis y T0; capa de aplicaciones Zeus, acoplamiento unidireccional, repo separado; supersede "DB de Budget = T0"
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0035, DECISION-0040, DECISION-0029, DECISION-0047, DECISION-0048, DECISION-0041]
phase: P2
---

# DECISION-0049 - Proyecto-front primario y T0; capa de aplicaciones Zeus

> ACCEPTED por el operador (GO lanzar proyecto-front, 2026-06-19). Lanza el primer PRODUCTO real
> desarrollado POR la metodologia, como proyecto primario de tesis y T0. SUPERSEDE el encuadre previo
> "handover de la DB de Budget = T0" (Budget pasa a proyecto posterior, sigue gateado por PII + DB).
> NO toca #4 (epoca 1.14.0, DECISION-0047).

## Contexto

La tesis necesita un caso real desarrollado bajo el protocolo cuyo dataset de coordinacion sea publicable.
La DB de Budget arrastra PII de terceros (gate DEF-PII, DECISION-0040) y depende de la DB terminada. El
operador elige como proyecto primario un **front single-operator para lanzar/operar/observar el propio
protocolo**: es **PII-free** -> su dataset de coordinacion se captura Y publica sin DEF-PII.

## Decision

1. **Proyecto-front = proyecto PRIMARIO de tesis y T0.** Su primera coordinacion gobernada bajo #4 es el
   inicio del dataset (T0), atestada en caliente. PII-free: dataset publicable sin DEF-PII. Budget pasa a
   proyecto POSTERIOR (gateado por PII + DB). Esto **supersede** "DB de Budget = T0".

2. **Capa de aplicaciones `Zeus`, repo SEPARADO, acoplamiento UNIDIRECCIONAL.** El protocolo/metodologia NO
   se mueve: vive en `D:\Agentes\multi_agent_project_protocol` y **GOBIERNA**. Las APLICACIONES de la
   metodologia viven bajo `D:\Agentes\Zeus\`. Repo destino del front = **`D:\Agentes\Zeus\Zeus-protocol`**
   (producto, separado del core). Acoplamiento unidireccional (espejo DECISION-0035): el protocolo gobierna
   y desarrolla el producto; el **core neutral NO se contamina** con codigo/dominio del producto, y el
   producto NO escribe el protocolo salvo por los canales gobernados (`submit_intent`).

3. **Separacion gobernanza vs producto (que vive donde):**
   - **PROTOCOLO (`Area_comun/`, atestado #4 = DATASET):** la coordinacion que desarrolla el front --
     decisiones de metodologia, SPEC de alcance, tasks, handoffs/GOs, ledger. T0 y el dataset se forman
     aqui.
   - **`Zeus-protocol/` (producto):** el codigo del front + su diseno interno de producto. Se desarrolla
     por SDD via la metodologia.
   *(Punto a confirmar con el operador: si quiere ademas la DECISION+SPEC de PRODUCTO dentro de
   `Zeus-protocol/` o solo el codigo; ver pregunta de coordinacion.)*

4. **Single-operator (DECISION-0029 intacto).** Launcher/UI de un solo operador. **Multi-tenant FUERA de
   alcance** (cambio de modelo de confianza: claves por-usuario, aislamiento) -> su propia DECISION futura.

5. **MVP (se convierte en SPEC):** UI local single-operator para **operar y observar** el protocolo:
   - **Ver (read-only):** mailbox (open/answered/archived), estado (PROJECT_STATE/TASK_INDEX/CLAIMS),
     decisiones/specs/tasks, handoffs, y el ledger atestado #4 / dataset (epoca, drift, version).
   - **Accionar (gobernado):** lanzar turno/run de agente, crear handoff/mensaje, emitir transiciones **via
     `submit_intent`** (escritor unico; SIN bypass de gates ni de #4), disparar validacion.
   - **Tech:** web (para habilitar multi-tenant futuro); detalle en la SPEC. Usa los connectors Git/CI del
     floor conforme aterricen.

6. **Compliance (duro):** todo write del front al estado/protocolo va por `submit_intent` (gates + #4 +
   drift); lectura por patron read-only. #4 intacto (epoca 1.14.0; capacidades nuevas fuera del config
   pinned, DECISION-0047). Neutralidad: cero producto en el core/`*.template.*`. Una cosa a la vez (coordina
   con el floor Git/CI/skills en curso; no combinar ventanas de riesgo). PII de terceros nunca al event log
   (ademas el proyecto es PII-free); DEF-PII (TASK-0118) sigue diferida (no la necesita este proyecto).

## Alcance / No-alcance

- **En alcance:** lanzar el proyecto-front como primario/T0; capa Zeus (repo separado, unidireccional);
  MVP single-operator (ver+accionar gobernado); SDD por la metodologia; dataset PII-free.
- **Fuera de alcance:** multi-tenant (DECISION futura); Budget/DB-live (proyecto posterior, PII+DB);
  bypass de gates/#4; mover/contaminar el core; Fase 4 / discovery.

## Consecuencias

- La tesis gana un caso real, PII-free, publicable, desarrollado bajo el protocolo, con T0 atestado bajo #4.
- Queda nombrada la capa de aplicaciones (Zeus) y el acoplamiento unidireccional; el core sigue neutral.

## Alternativas consideradas

- **DB de Budget = T0.** Superseded: PII de terceros (gate DEF-PII) + dependencia de la DB; dataset no
  publicable limpio. Budget = proyecto posterior.
- **Front dentro del repo del protocolo.** Descartada: contaminaria el core neutral; producto va en repo
  separado (Zeus), acoplamiento unidireccional (espejo DECISION-0035).
- **Multi-tenant ya.** Descartada: cambia el modelo de confianza (DECISION-0029); su propia DECISION.
