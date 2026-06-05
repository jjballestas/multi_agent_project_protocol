# DISEÑO — Runtime de orquestación automatizada (invocación de agentes + mailbox autónomo)

> **Origen:** propuesta del **human owner** (entregada vía agente externo) para abrir la fase de
> automatización. **No es todavía una decisión adoptada.** Antes de implementar, un agente debe:
> (1) registrar `DECISION-0008` con aprobación humana (cambia el *modelo operativo*: hoy la
> coordinación es manual sobre ficheros; esto la vuelve autónoma), (2) crear un claim sobre las
> rutas afectadas (DECISION-0007), (3) derivar las SPEC y TASK de la §7.
>
> **Neutralidad:** todo lo aquí descrito es **tooling** (capa `runtime/`, como `scripts/`), no
> política de dominio. El core sigue siendo domain-neutral. La capa es **opt-in** y **off by
> default**. Última actualización: 2026-06-05.

## 0. Resumen ejecutivo

Hoy el protocolo **documenta** la coordinación (tasks, claims, mailbox, handoffs) pero un humano
ejecuta cada paso a mano: abre una sesión de Claude, copia contexto, lanza Codex, mueve mensajes del
mailbox de `open/` a `answered/`, actualiza el estado. El protocolo es el "qué"; falta el "quién lo
ejecuta solo".

Este diseño añade un **plano de control (runtime)** que:

1. Lee el estado canónico (`PROJECT_STATE`, `TASK_INDEX`, `CLAIMS`, `mailbox/open/`).
2. Decide **qué unidad de trabajo toca y a qué agente** (router determinista).
3. **Invoca al agente** programáticamente con un *context pack* construido según `AGENTS.md §0`.
4. Recibe un **turn report estructurado** (contrato JSON) y **aplica las transiciones de estado**:
   mueve el mailbox, actualiza `TASK_INDEX`, libera/crea claims, escribe handoffs.
5. **Valida tras cada turno** (validador + scan de neutralidad) y, si algo falla, **revierte** (git)
   y escala al humano.
6. Para en los **gates humanos** (`DECISION_REQUIRED` / `HUMAN_REQUIRED` / release MAJOR).

La fuente de verdad sigue siendo el sistema de ficheros (auditable, dogfoodeable, sin servidor). El
runtime es un orquestador *sobre* esos ficheros, no un sustituto.

## 1. Principios de diseño (no negociables)

- **Aditivo y opt-in.** Bloque `runtime` en `protocol.config(.template).json` con `enabled:false`
  por defecto. Una instancia sin el bloque se comporta exactamente como hoy.
- **Ficheros = fuente de verdad.** El runtime no introduce una base de datos ni un servidor. Todo
  estado vive donde ya vive. Esto preserva el dogfooding y la auditabilidad.
- **Un turno = un commit.** Cada invocación de agente que muta el repo produce **un commit git**.
  Da trazabilidad total y *rollback* atómico.
- **Vendor-neutral por contrato.** Los agentes se conectan por un **adapter** con interfaz fija. El
  protocolo deja de estar acoplado a "Claude/Codex": son dos adapters de muchos posibles.
- **Determinista donde se pueda.** El router, las transiciones de estado y los gates son código
  determinista. Solo el *contenido* del trabajo lo produce el agente (no determinista), y se
  encapsula en un contrato de salida estricto.
- **Humano en el lazo por diseño.** Los `human_approval_points` del config se respetan como paradas
  duras del loop, no como sugerencias.
- **Reusa lo que ya existe.** Validador, scan de neutralidad, harnesses y plantillas se invocan tal
  cual; el runtime los orquesta, no los reescribe.

## 2. Arquitectura

```text
                      ┌─────────────────────────── runtime/orchestrator.py ──────────────────────────┐
  protocol.config ───▶│  tick():                                                                      │
  Area_comun/state ──▶│   1. load_state()      ── lee PROJECT_STATE/TASK_INDEX/CLAIMS/mailbox         │
  Area_comun/mailbox ▶│   2. gate_validate()   ── validate_collaboration_state.py (rechaza si rojo)   │
  Area_comun/tasks ──▶│   3. select_unit()     ── router: ¿qué tarea/mensaje y qué agente?            │
                      │   4. acquire_claim()   ── escribe CLAIMS.json (lock de rutas)                 │
                      │   5. build_context()   ── context pack (AGENTS.md §0 + task + specs/decisions)│
                      │   6. adapter.run() ───────────────┐                                           │
                      │   7. apply_turn(report)           │     ┌── adapters/claude_adapter.py        │
                      │   8. gate_post()  ── validador +  │────▶│   adapters/codex_adapter.py          │
                      │      neutralidad; si rojo ⇒ git    │     │   adapters/<vendor>_adapter.py       │
                      │      revert + blocked + escalate  │     └── (interfaz AgentAdapter común)      │
                      │   9. commit_turn() ── 1 turno = 1 commit                                       │
                      │  10. stop? (sin trabajo / HUMAN_REQUIRED / budget / max_iter)                 │
                      └───────────────────────────────────────────────────────────────────────────────┘
                                   │ run-log
                                   ▼
                      runtime/runs/RUN-<ts>.jsonl  (auditoría + métricas + coste)
```

### 2.1 Componentes

| Componente | Ruta propuesta | Responsabilidad |
|---|---|---|
| Orquestador | `runtime/orchestrator.py` | Loop de control, transiciones, gates, commits, rollback |
| Router | `runtime/router.py` | Selección determinista de la próxima unidad y su owner |
| Interfaz de adapter | `runtime/adapters/base.py` | Contrato `AgentAdapter` (vendor-neutral) |
| Adapters concretos | `runtime/adapters/claude_adapter.py`, `codex_adapter.py` | Invocan al agente real |
| Context builder | `runtime/context.py` | Arma el *context pack* de arranque en frío |
| Contrato de turno | `runtime/turn_schema.json` | Esquema JSON del *turn report* del agente |
| Wrapper git | `runtime/vcs.py` | commit/revert por turno; *write-allowlist* |
| Mailbox automation | `runtime/mailbox.py` | open→answered/archived según reglas |
| Run-log / métricas | `runtime/runlog.py` | JSONL por run + resumen de métricas |

## 3. Router — selección determinista de la próxima jugada

`select_unit()` aplica, en orden, una política explícita (configurable en `protocol.config`):

1. **Gates humanos primero.** Si hay `mailbox/open/` con `requires_response:true` dirigido al humano
   o `PROJECT_STATE.status != active` ⇒ **parar** y escalar (no se auto-resuelve).
2. **Mensajes de mailbox `open` dirigidos a un agente automatable** con `requires_response:true` →
   responder antes de tomar tareas nuevas (cierra el lazo de comunicación).
3. **Tareas accionables**: estado en `{ready, claimed, in_progress}`, `owner` con adapter
   habilitado, sin claim activo de **otro** owner sobre sus rutas, dependencias satisfechas.
   - Prioridad: `in_progress` (continuar) > `in_review` (revisión cruzada por el arquitecto) >
     `ready` (empezar). Desempate por id ascendente.
4. **Tareas `blocked`** no se tocan salvo que su `question` esté respondida en `mailbox/answered/`.
5. Si no hay nada accionable ⇒ **fin del run** (exit limpio).

La política es **datos, no código**: un bloque `runtime.routing` permite ajustar orden y filtros sin
tocar el orquestador.

## 4. Contrato de turno (`turn_schema.json`) — la pieza clave

El agente **no** escribe estado libremente: produce un **turn report** estructurado que el runtime
valida y aplica. Esto convierte la salida no-determinista del modelo en transiciones deterministas.

```json
{
  "task_id": "TASK-0042",
  "agent": "Codex",
  "outcome": "DONE | REVIEW | CHANGES | BLOCKED | DECISION_REQUIRED | HUMAN_REQUIRED | FYI | ACK",
  "status_transition": { "from": "in_progress", "to": "in_review" },
  "files_touched": ["scripts/foo.py", "examples/.../bar.json"],
  "handoff": { "create": true, "path": "Area_comun/handoffs/HANDOFF-TASK-0042-codex-to-claude-1.md" },
  "mailbox": [
    { "action": "answer", "ref": "MSG-...-open.md", "code": "OK", "context_refs": ["TASK-0042"] }
  ],
  "claim": { "action": "release", "scope": ["scripts/foo.py"] },
  "blocking_question": null,
  "summary": "Una línea, compacta (DECISION-0005).",
  "cost": { "input_tokens": 0, "output_tokens": 0 }
}
```

Reglas que el runtime **impone** sobre el report (si no se cumplen ⇒ turno inválido, revert):

- `status_transition.from` debe coincidir con el `TASK_INDEX` actual (detección de carreras).
- `files_touched` debe estar cubierto por un claim activo del agente (DECISION-0007).
- `outcome=BLOCKED` exige `blocking_question` no nulo (TASK_PROTOCOL).
- `outcome=DECISION_REQUIRED|HUMAN_REQUIRED` ⇒ el runtime **para** y genera HUMAN_REPORT.
- `outcome=DONE` exige handoff si la salida la usa otro agente (DoD de `AGENTS.md §9`).

## 5. Adapters — interfaz vendor-neutral

```python
class AgentAdapter(Protocol):
    name: str
    def run(self, *, context_pack: ContextPack, task: Task, workdir: Path,
            budget: Budget) -> TurnReport: ...
```

- **`claude_adapter`**: vía **Claude Agent SDK / Anthropic API**, con herramientas de fichero
  limitadas a `workdir` y *prompt caching* del context pack (gran parte es estable entre turnos).
- **`codex_adapter`**: vía Codex CLI/API equivalente.
- **Cualquier vendor** (otro LLM, un humano "manual mode") implementa la misma interfaz. Esto
  **desacopla** el protocolo de Claude/Codex — corrige la crítica de "neutral salvo en los roles".
- El adapter recibe un *system prompt* que incluye: el contrato de turno (debe responder con el
  JSON), `AGENTS.md`, el protocolo y la tarea. Devuelve el `TurnReport` + los ficheros ya escritos en
  `workdir`.

## 6. Seguridad, auditoría y observabilidad

- **Dry-run (`--plan`)**: imprime las 1..N jugadas que haría sin invocar agentes. Primer entregable.
- **1 turno = 1 commit** con mensaje `runtime(turn): TASK-XXXX <outcome>`; rollback = `git revert`.
- **Write-allowlist**: los adapters no pueden tocar `.git/`, `Area_comun/decisions/`,
  `protocol.config.json` ni `AGENTS.md` salvo flag explícito (cambios de política = humano).
- **Gate por turno**: validador + scan de neutralidad antes de `commit_turn()`. Rojo ⇒ revert.
- **Budget**: techo de tokens/coste y `--max-iter`; al alcanzarlo, para y reporta.
- **Run-log** `runtime/runs/RUN-<ts>.jsonl`: una línea por turno (unidad, agente, outcome,
  transición, coste, duración, resultado del gate). De aquí salen las **métricas de ROI** que pide la
  monetización: turnos por tarea, colisiones evitadas, reverts, % gates verdes, coste por tarea.

## 7. Plan de entrega (derivar a DECISION + SPEC + TASK)

> Pensado para trocearse en tareas pequeñas de un solo owner, con SDD activado.

**DECISION-0008 — Adoptar runtime de orquestación automatizada (requiere aprobación humana).**
Fija: capa `runtime/` opt-in y off-by-default; ficheros como fuente de verdad; 1 turno = 1 commit;
gates humanos como paradas duras; interfaz de adapter vendor-neutral. Por cambiar el modelo
operativo, se trata como **MAJOR** candidato (o MINOR si se acepta que, al estar off-by-default, es
aditivo) — **decisión del human owner en la propia DECISION-0008**.

| Hito | Tarea (owner) | Entregable | DoD |
|---|---|---|---|
| **M0** | Diseño contrato de turno + router (Claude, `analysis`) | `turn_schema.json`, SPEC del router | Esquema validado; golden de reports válidos/ inválidos |
| **M0** | `runtime/` skeleton + `--plan` dry-run (Codex, `implementation`) | orquestador que **planifica sin invocar** | `--plan` lista jugadas correctas sobre el dogfood |
| **M1** | Wrapper git + write-allowlist + gate por turno (Codex) | `vcs.py`, rollback | turno que falla el gate se revierte sin tocar estado |
| **M1** | `claude_adapter` (un solo turno real) (Codex) | invocación 1 tarea → 1 commit | una tarea `ready`→`in_review` ejecutada por runtime |
| **M2** | `codex_adapter` + loop multi-agente + mailbox automation (Codex) | handoff Claude↔Codex autónomo | una tarea recorre el ciclo completo sin humano |
| **M2** | Mailbox hygiene como transiciones (Codex, reusa TASK-0021) | open→answered/archived auto | casos golden de mailbox pasan vía runtime |
| **M3** | Gates humanos + budget + run-log/métricas (Claude diseño, Codex impl.) | HUMAN_REPORT auto, métricas | `DECISION_REQUIRED` para el loop y reporta |
| **Piloto** | Correr el runtime sobre `bot_spot_ai_strategy_pack` (humano + ambos) | reporte con métricas reales | evidencia de ROI: turnos/tarea, colisiones, coste |

**Orden recomendado:** M0 (planner) → M1 (un turno real con rollback) → M2 (loop de dos agentes +
mailbox) → M3 (gates + observabilidad) → piloto con métricas.

## 8. Versionado y neutralidad

- Si se publica **off-by-default**, es aditivo ⇒ candidato **v0.7.0 (MINOR)**, pero por cambiar el
  modo de operar se **recomienda aprobación humana** igualmente (DECISION-0008).
- Endurecer (auto-aplicar sin gate humano, quitar dry-run, escribir estado sin contrato de turno)
  sería **MAJOR**.
- Ningún fichero de `runtime/` puede introducir términos de dominio en la superficie neutral (§1.1
  de `DISENO-robustez-operacional.md`): se añade `runtime/**` a `scan_globs` para los `.py/.ps1`.

## 9. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Agente produce trabajo incorrecto y lo commitea | Gate por turno + 1 commit/turno + revert automático |
| Carreras entre dos agentes sobre las mismas rutas | Claim como lock previo a `adapter.run()`; `from` de la transición debe casar |
| Coste descontrolado de tokens | Budget + `--max-iter` + prompt caching del context pack |
| El runtime "se escapa" del humano | Gates humanos como paradas duras; write-allowlist sobre decisions/policy |
| Acoplamiento a un vendor | Interfaz `AgentAdapter`; "manual mode" como adapter de respaldo |
| Romper el dogfooding | Ficheros siguen siendo la verdad; el runtime no añade servidor ni DB |

## 10. Qué NO incluye este diseño (límites)

- No hay servidor, cola de mensajes externa ni base de datos: a propósito, para no romper el modelo
  file-based ni la auditabilidad.
- No hay auto-aplicación de upgrades ni cambios de política sin humano.
- No define el dominio del piloto: eso vive en la instancia, no en `runtime/`.
