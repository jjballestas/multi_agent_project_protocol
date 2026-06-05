# DISEÑO — Runtime M2 (autonomía: adapters reales + loop multi-agente + observabilidad)

> **Bajo DECISION-0009** (runtime adoptado, opt-in/off-by-default). M2 es **diseño-ahead**: las SPEC y
> TASK se derivan **cuando M1 aterrice** (TASK-0030/0031) y se libere el estado. Construye sobre la
> interfaz `AgentAdapter` y el loop `--run` fijados en M1 (SPEC-0030). Neutral (tooling).
> Última actualización: 2026-06-05 · Autor: Claude (arquitecto).

## 0. Resumen
M0 = plano de control read-only (`--plan`). M1 = primer escritor seguro (apply + gate + commit/revert)
con un **replay adapter** que cierra el loop de forma determinista. **M2 = autonomía real:** sustituir
el replay por **adapters que invocan agentes reales** (Claude/Codex vía SDK/CLI), encadenar turnos
**Claude↔Codex** sin humano (salvo gates), automatizar el mailbox como transiciones y añadir
**presupuesto + run-log + métricas de ROI**. El loop de M1 **no cambia**: M2 solo enchufa adapters
reales detrás de la misma interfaz y endurece la política de parada.

## 1. Alcance de M2
- `runtime/adapters/claude_adapter.py` y `runtime/adapters/codex_adapter.py` — implementan
  `AgentAdapter.run_turn` invocando el SDK/CLI real, con **sandbox de escritura** limitado a `root` y al
  scope del claim, y devolviendo un *turn report* conforme a `turn_schema.json`.
- `runtime/context.py` (extensión) — **context pack** de arranque en frío real (AGENTS §0 + tarea +
  specs/decisions enlazadas), con *prompt caching* del prefijo estable entre turnos.
- `runtime/loop.py` (o `orchestrator --run` extendido) — **loop multi-agente**: tras un turno que deja
  una tarea en `in_review`, el router enruta la **ratificación** al arquitecto (Claude) automáticamente;
  los handoffs Claude↔Codex se ejecutan sin humano salvo gate.
- `runtime/mailbox.py` — **mailbox automation**: `open→answered/archived` como transiciones derivadas
  del *turn report* (reusa las reglas de TASK-0021/SPEC-0021 y el frontmatter mínimo de TASK-0025).
- `runtime/budget.py` + `runtime/runlog.py` (extensión) — **techo de coste/iteraciones** y **métricas
  de ROI** (turnos/tarea, colisiones evitadas, reverts, % gates verdes, coste por tarea).
- **Gates humanos** endurecidos: `human_approval_points` (DECISION_REQUIRED / HUMAN_REQUIRED / release
  MAJOR) generan `HUMAN_REPORT` y **paran** el loop; nunca se auto-resuelven.

## 2. Adapters reales (sobre la interfaz de M1)
```python
class ClaudeAdapter(AgentAdapter):     # mismo Protocol que replay/manual de M1
    name = "Claude"
    def run_turn(self, *, context, root):
        # 1. construye prompt: contrato de turno (turn_schema) + AGENTS.md + protocolo + tarea
        # 2. invoca Claude (Agent SDK / API) con herramientas de fichero limitadas a `root`
        # 3. el agente escribe ficheros en `root` y DEVUELVE un turn report (JSON)
        # 4. retorna el report; el orquestador (M1) valida+aplica+gate+commit/revert
```
- **Vendor-neutral:** cambiar `ClaudeAdapter`→`CodexAdapter`→`<otro>` no toca el loop. "manual mode"
  (M1) sigue como adapter de respaldo. Esto **desacopla** el protocolo de Claude/Codex.
- **Seguridad del adapter:** herramientas de escritura **sandbox** a `root`; el adapter **no** puede
  tocar `.git/`, `Area_comun/decisions/`, `AGENTS.md`, `protocol.config*` (write-allowlist de M1 + el
  propio sandbox). El report declara `changed_paths`; el orquestador rechaza si exceden el claim.

## 3. Loop multi-agente autónomo
Política determinista (reusa el router de SPEC-0027, ahora con adapters habilitados por `owner`):
1. **Gate humano** presente ⇒ parar + `HUMAN_REPORT`.
2. **Mailbox** `requires_response:true` a un agente con adapter ⇒ responder (cierra el lazo).
3. **`in_review`** ⇒ ruta al **arquitecto** (Claude) para ratificar (acepta ⇒ `done`; pide cambios ⇒
   vuelve a `in_progress`/`blocked`).
4. **`ready`/`in_progress`** del owner con adapter, deps satisfechas, sin claim de otro ⇒ ejecutar.
5. Sin trabajo ⇒ fin de run. **Determinismo:** desempate por `(priority, id)`; el contenido lo produce
   el agente, las transiciones las decide el código.
- Una tarea recorre `ready → (Codex) in_progress → in_review → (Claude) done` **sin humano**, con 1
  commit por turno y gate por turno. El humano entra solo en los gates.

## 4. Observabilidad y control (ROI)
- **`runtime/runs/RUN-<id>.jsonl`**: una línea por turno (unidad, agente, outcome, transición, gate,
  commit, coste, duración). Fuente de las métricas que pide la monetización del protocolo.
- **Métricas derivadas:** turnos por tarea, % gates verdes, nº de reverts, colisiones evitadas (claims),
  coste (tokens) por tarea. Reporte de run al cerrar.
- **Budget/`--max-iter`:** techo duro; al alcanzarlo, para y reporta (no "se escapa").

## 5. Troceo (derivar a SPEC + TASK cuando M1 aterrice)
| Hito | Task (owner) | Spec a emitir | DoD |
|---|---|---|---|
| M2 | `claude_adapter` real (1 turno real → 1 commit) (Codex) | SPEC-00xx adapter-real | una tarea `ready→in_review` ejecutada por un agente real vía runtime |
| M2 | `codex_adapter` + loop multi-agente Claude↔Codex (Codex) | SPEC-00xx loop-autonomo | una tarea recorre el ciclo completo sin humano |
| M2 | mailbox automation como transiciones (Codex, reusa SPEC-0021/TASK-0025) | SPEC-00xx mailbox-auto | golden de mailbox pasan vía runtime |
| M3 | gates humanos + budget + run-log/métricas (Claude diseño, Codex impl) | SPEC-00xx observabilidad | DECISION_REQUIRED para el loop + reporte de métricas |
| Piloto | correr sobre `bot_spot_ai_strategy_pack` (humano + ambos) | — | evidencia de ROI real |

**Prerrequisito:** M1 (TASK-0030/0031) aceptado. **Aprobación humana** para **activar** (`enabled:true`):
poner el runtime a ejecutar agentes reales sobre el repo es un cambio de modo de operación; off-by-default
se mantiene y encenderlo es decisión del human owner (DECISION-0009 §gates).

## 6. Riesgos específicos de M2
| Riesgo | Mitigación |
|---|---|
| Agente real produce trabajo incorrecto y lo commitea | gate por turno + 1 commit/turno + `git revert` (M1) |
| Adapter escapa del sandbox / toca política | sandbox a `root` + write-allowlist de M1 + report `changed_paths` validado |
| Coste de tokens descontrolado en el loop | budget + `--max-iter` + prompt caching del context pack |
| Loop se cicla sin progreso | determinismo + anti-carrera (`from` casa) + parada por "sin trabajo"/max-iter |
| El runtime "se escapa" del humano | gates humanos como paradas duras; activar = decisión humana |
| Acoplamiento a un vendor | todo via `AgentAdapter`; manual mode como respaldo |

## 7. Qué NO incluye M2
- No elimina al humano de los gates (DECISION_REQUIRED/HUMAN_REQUIRED/MAJOR siguen parando el loop).
- No añade servidor/DB: el estado sigue en ficheros (dogfooding/auditoría).
- No auto-aprueba releases ni cambios de política. No define el dominio del piloto (vive en la instancia).
