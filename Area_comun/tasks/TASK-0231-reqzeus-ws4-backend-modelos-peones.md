---
task_id: TASK-0231
title: "[VISION-NOVA][F6.1] Fase peones bajo DECISION-0078 ajustada (peon -> gate -> critico -> firmante; sandbox piloto-peones intacto) [re-alcance: pivote Vision Nova, DECISION-0083]"
type: build
status: proposed
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-30
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0074, DECISION-0077, DECISION-0078, DECISION-0083]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0231-reqzeus-ws4-backend-modelos-peones.md
---

# TASK-0231 - [VISION-NOVA][F6.1] Fase peones (re-alcance DECISION-0083)

- **Owner build:** Codex - **Review:** Analista (seguridad/PII) - **Checker:** Arquitecto - Decision de backend: Operador.
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`. **Spike de peones en repo SANDBOX aparte** `D:/Agentes/Zeus/piloto-peones`. Dep: D3 (0074).

## Alcance
1. Backend por defecto (router empresa OpenAI-compat u Ollama local) que expone **modelos frontera** (firmantes) +
   **peon** (drafter boilerplate). Punto unico de claves/costo.
2. **Bloqueo PII (cero-egress):** prueba negativa de que datos reales NO salen a modelos externos.
3. **Spike de peones (opcional, en sandbox aparte):** experimento A/B/C de la guia (DECISION-0074); metrica que decide
   = tokens del firmante; peon = maker keyless fuera del ledger, firmante distinto firma (maker!=checker).

## DoD
- Chat de prueba responde; claves fuera del repo; **prueba negativa PII no sale**.
- Si se corre el spike: va en `D:/Agentes/Zeus/piloto-peones`, cero escritura al repo medido; reporte de medicion.
- Gate Analista (seguridad): GO. maker!=checker.

## Medicion del uso de peones y regla de aislamiento (directiva Operador 2026-07-03)
- **Medicion (descriptiva):** el diseno declara `orchestration_mode` POR TAREA (enum mono|peones|mixto|NA)
  y captura los 5 campos peon del schema de medicion (congela en sello Etapa 1, <=08-jul):
  `orchestration_mode`, `peones_n` (int), `peon_revivals_n` (int; los peones REVIVEN por memoria hibrida),
  `peon_modelos` (str; p.ej. qwen2.5-coder:7b, deepseek-coder:6.7b), `tokens_peones` (int).
  **Contabilidad dura:** `tokens_peones` es SUBSET ya contado en las cubetas dev/checker (informativo,
  EXCLUIDO de toda confirmatoria, mismo trato que tokens_cache_reads) -> NO se suma aparte, no doble-contar.
- **Regla de aislamiento (invariante del estudio):** los peones son una VARIABLE distinta del tratamiento
  aditivo (el tratamiento medido es la GOBERNANZA ATESTADA, no la orquestacion). En el contraste central
  (baseline mono vs gobernado mono) el brazo gobernado se mantiene MONO-orquestado; si aparece un peon se
  REGISTRA (descriptivo via `orchestration_mode`) pero NO convierte el brazo en 'tratamiento peones'. El
  EFECTO de los peones se mide SOLO en esta fase F6 (mono-vs-peones bajo gobierno completo -> Q1), aislado,
  con `orchestration_mode` declarado por tarea y pool PROPIO (no se solapa con las unidades del contraste
  central). Meter peones en el brazo gobernado del estudio central cambia DOS cosas a la vez (gobierno +
  orquestacion) y confunde Q1/Q4: prohibido.
- **DoD adicional:** el diseno de F6 declara `orchestration_mode` por tarea, captura los 5 campos peon, y
  respeta el aislamiento intra-estudio (pool propio, no solapa el contraste central). Modelos peon candidatos
  instalados en Ollama: qwen2.5-coder:3b/7b y deepseek-coder:6.7b.

## Handoff
Autocontenida. Ambiguedad -> blocked + 1 pregunta concreta.
