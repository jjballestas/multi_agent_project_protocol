---
decision_id: DECISION-0050
title: Convencion de repos y operacion - gobernanza/atestacion en el protocolo (hub permanente), codigo de producto en su repo bajo Zeus (acoplamiento unidireccional); el front es el panel del operador (VS Code opcional)
status: accepted
ratified_at: 2026-06-20
date: 2026-06-20
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amended_by: [DECISION-0095]
relates_to: [DECISION-0049, DECISION-0035, DECISION-0047, DECISION-0095]
phase: P2
---

# DECISION-0050 - Convencion de repos y operacion

> ENMENDADA por DECISION-0095 (2026-07-13): el punto 1 se REFINA -- lo que debe vivir SIEMPRE en el hub es
> el ANCLA de cross-atestacion; los EVENTOS de gobierno de un producto SI pueden vivir dentro del repo de
> producto, encapsulados en la carpeta constante `Aegis/` (modelo 2.A, un-repo), cross-atestados al hub.
> El resto de esta decision sigue vigente.

> ACCEPTED por el operador (2026-06-20). Convencion de METODOLOGIA, neutral (cero dominio). Patron repetible
> para todos los proyectos-producto. NO toca el config pinned (#4 epoca 1.14.0; AGENTS.md no esta pinned por
> el genesis). Se registra en AGENTS.md (s.8 Repository Map) + runbook.

## Decision (convencion)

1. **Gobernanza / coordinacion / atestacion -> SIEMPRE en el protocolo** (`multi_agent_project_protocol`):
   DECISION/SPEC/tasks/handoffs/mailbox + `submit_intent` + ledger #4. **Es el dataset** (atestado,
   publicable). Nunca dentro de un repo de producto (alli no se atestaria).
2. **Codigo de producto -> SIEMPRE en su repo bajo `D:\Agentes\Zeus\`** (acoplamiento unidireccional, espejo
   DECISION-0035/0049; el core neutral del protocolo NO se toca). Hoy: `Zeus-protocol`.
3. **El runtime de cada agente accede a AMBOS por RUTA** (ya configurado): un agente commitea codigo en su
   repo de producto y atesta gobernanza en el protocolo, sin necesitar un workspace multi-root de VS Code.
4. **El FRONT (`Zeus-protocol`) es el PANEL del operador** para operar/observar la metodologia (mailbox/
   estado/ledger/atestacion, GOs, lanzar agentes, multi-proyecto). **VS Code = OPCIONAL** (solo codigo
   crudo); el "multi-root" era andamio temporal, no requisito.
5. **Patron repetible:** cada proyecto futuro (Budget, etc.) tiene su propio repo bajo `D:\Agentes\Zeus\`;
   la gobernanza de TODOS vive en el unico protocolo (hub permanente). Los repos de producto rotan; el
   protocolo es constante.

## Alcance / No-alcance

- **En alcance:** fijar la convencion + registrarla en AGENTS.md (s.8) y el runbook; neutral, metodologica.
- **Fuera de alcance:** tocar #4/config pinned; mover/contaminar el core; cambiar el modelo single-operator
  (multi-tenant = DECISION futura).

## Consecuencias

- Nadie vuelve a asumir "VS Code multi-root" como requisito; el front es el panel.
- El protocolo queda como hub permanente de gobernanza/dataset; los productos son repos rotables bajo Zeus.
