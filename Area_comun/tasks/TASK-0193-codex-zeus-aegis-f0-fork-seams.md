---
task_id: TASK-0193
title: "Zeus-Aegis F0 - fork & seams & inventario (DECISION-0064): importar Hermes v2.3.0, correr vanilla, documentar seams + inventario de reuso (informe, sin UI todavia)"
type: discovery
status: changes_requested
owner: Codex
phase: P2
priority: high
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0050, DECISION-0022, DECISION-0020]
file: Area_comun/tasks/TASK-0193-codex-zeus-aegis-f0-fork-seams.md
---

# TASK-0193 - Zeus-Aegis F0: fork & seams & inventario

> maker=Codex / checker=Arquitecto. Repo de PRODUCTO = `D:/Agentes/Zeus/Zeus-Aegis` (ya creado, privado,
> `github.com/jjballestas/Zeus-Aegis`, scaffold commit 90cd5c8). **NO toca el core neutral ni el mecanismo #4.**
> Fase 0 de DECISION-0064: entrega un **INFORME + el fork corriendo vanilla**, todavia SIN vistas de gobernanza.
> Plan fuente: `personal/operador/Hermes/PLAN_INTEGRACION.md` (seccion Fase 0) y `PROMPT_CLAUDE_CODE_ARQUITECTO.md`.

## Objetivo

Asentar el fork de Hermes Workspace como base de Zeus-Aegis y documentar las costuras (seams) reales, sin
construir todavia el panel. Dejar el terreno listo y verificado para F1 (read-only), que queda GATEADA.

## Alcance (F0.1-F0.6)

- **F0.1** Importar el codigo de Hermes **v2.3.0** (NO `main`) al repo Zeus-Aegis como snapshot vendor en branch
  `vendor/hermes-2.3.0` (pin). Conservar `LICENSE` MIT + avisos de copyright de Hermes (ver `NOTICE.md`).
- **F0.2** Correr **vanilla** y verificar: gateway `:8642` + dashboard `:9119` + UI `:3000`; chat responde;
  `GET http://127.0.0.1:3000/api/sessions` -> 200. Ejecutar desde el **entorno real** (no sandbox stale).
- **F0.3** **Documento de seams** (en `Zeus-Aegis/docs/SEAMS.md`): rutas `/api/*` reales del front, `HERMES_API_URL`,
  `HERMES_API_TOKEN`, dashboard API (:9119), conductor (`/api/conductor-spawn|stop`), variables `.env`. Marcar lo
  verificado vs lo asumido.
- **F0.4** **Stack real confirmado** (corrige el material original): NO Next.js -> TanStack Start + Vite 7 + React 19
  + Electron 40; identificar y documentar como **aislar/retirar** el subsistema de juego 3D
  (`three`/`@react-three/fiber`/rapier) y el empaquetado Electron que un panel no usa.
- **F0.5** **Rebranding inicial** (nombre/colores Zeus-Aegis) **sin alterar** `LICENSE` ni avisos de copyright.
- **F0.6** **Inventario de reuso desde `D:/Agentes/Zeus/Zeus-protocol`** (en `Zeus-Aegis/docs/REUSE-INVENTORY.md`):
  que componentes de gobernanza (Intake RF-14, Mailbox, Backlog, Artifacts, consola agente-a-agente, Operate) son
  portables, su stack, y recomendacion (quedarse con lo que Hermes NO hace; descartar lo que Hermes ya hace mejor).

## DoD (= GATE 0)

1. Branch `vendor/hermes-2.3.0` con Hermes v2.3.0 importado; `LICENSE`/`NOTICE.md` MIT intactos; `scan` sin secretos.
2. Fork **corre vanilla en verde** (gateway/dashboard/UI arriba; chat OK; `/api/sessions` 200) — evidencia (logs/salidas).
3. `docs/SEAMS.md` entregado (rutas reales vs asumidas) + `docs/REUSE-INVENTORY.md` entregado.
4. Rebranding inicial aplicado sin tocar `LICENSE`/copyright; plan de aislamiento de juego 3D + Electron documentado.
5. Handoff autocontenido a Arquitecto (checker) en `Area_comun/handoffs/`; `TASK_INDEX` via intent.
6. **NO arrancar F1+** (read-only/write-through) -- GATEADO en DECISION-0064 (F2 = post-TFM).

## Restricciones

- Pin a v2.3.0; NO seguir `main` upstream (churn). Backend propietario separado (no mezclar core con archivos MIT).
- NO tocar el core neutral del protocolo, `protocol.config.json`, ni el mecanismo #4. Todo el trabajo en el repo
  de producto Zeus-Aegis.
- Minimal narration (DECISION-0038). Commit como Arquitecto con Codex via `Co-Authored-By` (committer nunca forja).
- Ambiguedad -> `blocked` + una pregunta concreta.
