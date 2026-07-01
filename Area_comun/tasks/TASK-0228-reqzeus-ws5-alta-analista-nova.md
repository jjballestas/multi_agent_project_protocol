---
task_id: TASK-0228
title: "[REQ-ZEUS-001][WS5] Alta del Analista en NOVA + decision mapeo rol->agente + wrapper new_instance(4 firmantes)"
type: build
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001]
linked_decisions: [DECISION-0072, DECISION-0073, DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0228-reqzeus-ws5-alta-analista-nova.md
---

# TASK-0228 - [REQ-ZEUS-001][WS5] Alta del Analista en NOVA + 4 firmantes

- **Owner build:** Codex - **Review:** Analista - **Gobierna/mapeo:** Arquitecto
- **Repo instancia:** NOVA (`D:/Agentes/Zeus/NOVA`). Gobernanza: hub. **PRIMERO del backlog** (condiciona owner:Analista).

## Alcance
1. Extender `new_instance.py` (o wrapper) para sembrar **4 agentes** (Arquitecto, Codex, Analista, human_owner) y
   crear `personal/<id>/` de cada uno.
2. **Alta del Analista (checker)** en NOVA: registrar en `agent_roles`/`PROJECT_STATE.agents` + legend de `TASK_INDEX.json`.
3. **Mapeo rol->agente** materializado por DECISION-0072/0073/0077 (NO por `NOVA-ARQ-001`, que no existe como decision canonica). `quality_policy`: `allow_self_review:false`/`allow_self_qa:false` = **regla DISCIPLINARIA declarativa** (maker!=checker por roster + proceso); el validador es pineado y NO la gatea.

## DoD (corregido tras NO-GO Analista: claims honestos, sin sobre-promesa)
- Instancia NOVA valida exit 0 con **4 PARTICIPANTES** (Arquitecto, Codex, Analista, human_owner); una TASK `owner:Analista` es ACEPTADA (no rechazada). Nota honesta: el validador NO prueba el registro del owner (un owner ajeno tambien valida exit 0) -> el alta se evidencia por el ROSTER en config/PROJECT_STATE/legend, no por el gate.
- Mapeo rol->agente = DECISION-0072/0073/0077 (no NOVA-ARQ-001).
- **maker!=checker = regla DISCIPLINARIA por roster, NO gateada por el validador pineado.** `allow_self_review:false`/`allow_self_qa:false` son declarativos; la garantia es de proceso, NO enforced por el validador. No se afirma como comprobable por el gate.
- **"4 firmantes" del titulo = 4 PARTICIPANTES.** Firma SOLO en tier attested (3 signers: Arquitecto/Codex/Analista; `human_owner` queda `worker`). En coordination (defecto NOVA) no hay firma por diseno.
- Tier coordination por defecto (DECISION-0072/0073). Sin tocar el core del protocolo ni los pineados. Gate Analista: GO.

## Handoff
Autocontenida. maker!=checker. Ambiguedad -> blocked + 1 pregunta concreta.
