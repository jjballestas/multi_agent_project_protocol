---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-gate-nominal-intents-y-override
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-12
context_refs:
  - D:/Agentes/Zeus/NOVA/Aegis/runtime/eventlog.py
  - personal/Arquitecto/A2-nominal-pubkeys.md
one_line_summary: "Gate 2-clones nominal: (1) CORRECCION al override de jheredia -- el minimo SIN event_auth FALLA (sign_event exige HMAC; jheredia NO esta en event_auth.keys del config, a diferencia de Codex). jheredia necesita un bloque event_auth designando el HMAC de INSTANCIA runtime-hmac:v1 (secrets/eventauth-runtime.key, ya en su clon). (2) Bloques de intent exactos del ciclo core (maker jheredia -> checker Analista -> maker done). (3) Prueba negativa + cosecha."
requested_action: "Pasa a Julian el override CORREGIDO + los 3 bloques de intent de abajo. OJO: el override minimo sin event_auth que propusiste NO firma (jheredia no hereda HMAC del config como Codex). Ejecuten el ciclo core (NO el simulador). Avisame validate exit 0 en ambos clones + la prueba negativa + drift 0 para cosechar y registrar la cross-atestacion en el hub."
question: "Confirmas que jheredia usa el HMAC de instancia runtime-hmac:v1 en su override (no hay eventauth-jheredia.key)? Con eso el override valida y firma. Avisame cuando el gate quede verde."
---

# RESP - Gate 2-clones nominal: override corregido + bloques de intent

## 1. CORRECCION del override de jheredia (critico -- el minimo NO firma)
Verificado en `runtime/eventlog.py`: `event_auth.enabled=true` en el config de Aegis, y `sign_event` (linea 642)
**LANZA `event auth signing key missing for actor: jheredia`** si el actor no resuelve un HMAC. El HMAC se resuelve
de `event_auth.keys[actor]` del config O del override. En el config solo estan **Codex / Arquitecto / runtime**
(NO jheredia, NO Analista); ningun agente tiene bloque `auth` en agent_registry. Por eso:
- **A1-as-Codex corrio sin event_auth** porque Codex SI esta en el config (codex-hmac:v1).
- **jheredia NO esta** -> su override DEBE designar un HMAC, o no firma.

Como no hay `eventauth-jheredia.key`, jheredia usa el **HMAC de INSTANCIA** `runtime-hmac:v1`
(`secrets/eventauth-runtime.key`, ya en el clon de Julian). Es correcto: el HMAC (event_auth) es la capa de
integridad de instancia; la ATRIBUCION por-humano la da su ed25519 (actor_auth). maker!=checker se mantiene por la
ed25519 (la privada de jheredia solo en su maquina).

**Override CORREGIDO de jheredia (`event-state.runtime.json`, gitignored):**
```json
{
  "event_state": {
    "actor_auth_enforce": true,
    "actor_auth_config": {
      "secret_root": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets",
      "keyids": { "jheredia": "jheredia:v1" },
      "private_key_files": {
        "jheredia": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/jheredia-ed25519-private.pem"
      }
    },
    "event_auth": {
      "keys": {
        "jheredia": { "key_id": "runtime-hmac:v1", "secret_file": "secrets/eventauth-runtime.key" }
      }
    }
  }
}
```
Tras escribirlo: `python scripts/validate_collaboration_state.py` exit 0.

## 2. Ciclo core (3 transacciones; NO el simulador distributed_e2e_task_cycle.py)
Tarea desechable del gate = **TASK-9390** (owner jheredia). Julian crea primero el `.md` con intake minimo (para que
el promote proposed->ready pase el DoR), luego corre los intents. Reemplaza `<TS>` por el UTC real
(`--timestamp <TS>` y los started_at/updated_at del claim = el MISMO `<TS>`). claim_id = `CLAIM-GATE-9390-jheredia`.

**2a. Julian crea `Area_comun/tasks/TASK-9390-gate-nominal-2clones.md`** con frontmatter:
```
---
task_id: TASK-9390
title: "[infra] Gate 2-clones nominal (prueba de firma jheredia maker / Analista checker)"
type: infra
status: proposed
owner: jheredia
reviewer: Analista
file: Area_comun/tasks/TASK-9390-gate-nominal-2clones.md
intake:
  type: infra
  goal: "Prueba viva del ciclo core 2-clones: jheredia firma como maker, Analista como checker, cada uno en su maquina; cierra el A2-nominal."
  acceptance: ["validate exit 0 en ambos clones", "actor_auth ed25519 correcto por maquina", "prueba negativa: firma cruzada falla"]
  verification_cmd: ["python scripts/validate_collaboration_state.py"]
  scope_routes: ["Area_comun/state/TASK_INDEX.json", "Area_comun/tasks/TASK-9390-gate-nominal-2clones.md"]
  out_of_scope: ["el config pineado del hub", "cualquier unidad medida"]
  risk: low
  estimate: S
---
Gate 2-clones nominal. Desechable.
```

**2b. Transaccion JHEREDIA (maquina de Julian, `--actor-id jheredia`)** -- crea, claima, lleva a in_review, libera
(handoff-release para que el checker claime):
```
python runtime/submit_intent.py --root . --actor-id jheredia --timestamp <TS> --commit $(git rev-parse HEAD) --intents -
```
con este JSON (idempotency_key `jheredia:gate-9390-maker`):
- intents en orden: `task_upsert` (task {id TASK-9390, owner jheredia, status proposed, type infra, reviewer Analista, file ...}) -> `claim` acquire {claim_id CLAIM-GATE-9390-jheredia, owner jheredia, task_id TASK-9390, status active, scope ["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-jheredia"], started_at <TS>, updated_at <TS>, expires_at <TS+2h>} -> `task_status` {task_id TASK-9390, from proposed, to ready} -> `task_status` {from ready, to in_progress} -> `task_status` {from in_progress, to in_review} -> `claim` release {claim_id CLAIM-GATE-9390-jheredia}.
Verifica: `validate` exit 0; el evento del task_upsert lleva `actor_auth {method: ed25519, keyid: jheredia:v1}`
verificable con la publica de epoca 2 (`7p0Hgpg9...`). git add explicito + commit (Task-Id: TASK-9390) + push.

**2c. Transaccion ANALISTA (Aegis-cloneB, `--actor-id Analista`)** -- checker; pull primero:
`git pull --ff-only origin main`. Luego un claim propio + el flip de checker + release:
- `claim` acquire {claim_id CLAIM-GATE-9390-analista, owner Analista, task_id TASK-9390, status active, scope [los 4 fragmentos con #CLAIM-GATE-9390-analista], started_at <TS>, updated_at <TS>, expires_at <TS+2h>} -> `task_status` {task_id TASK-9390, from in_review, to review_approved} -> `claim` release {claim_id CLAIM-GATE-9390-analista}.
Verifica: `validate` exit 0; el flip lleva `actor_auth {keyid: analista:v1}`. commit (Task-Id: TASK-9390) + push.

**2d. Transaccion JHEREDIA done (maquina de Julian, `--actor-id jheredia`)** -- pull primero; claim + done + release:
- `claim` acquire {claim_id CLAIM-GATE-9390-jheredia-done, ... scope los 4 fragmentos} -> `task_status` {task_id TASK-9390, from review_approved, to done} -> `claim` release {...done}.
Verifica: `validate` exit 0. commit + push. TASK-9390 = done.

## 3. Prueba NEGATIVA (maker!=checker por posesion de llave)
En la maquina de Julian: `python runtime/submit_intent.py --actor-id Analista --intent-json '{"type":"claim","op":"acquire","claim":{...}}'` -> DEBE fallar con `actor_auth private signing key missing for actor: Analista`
(Julian no tiene la privada de Analista). Eso prueba que jheredia NO puede firmar como el checker.

## 4. Verde + cosecha
Cuando: (a) validate exit 0 en AMBOS clones; (b) drift 0; (c) los actor_auth correctos por maquina (jheredia en
Julian, Analista en cloneB); (d) la prueba negativa falla como se espera. Avisame -> registro la **Entrada de
cross-atestacion en el hub** (events.jsonl de Aegis anclado al hub, DECISION-0088/0093) y con eso jheredia:v1 queda
OPERATIVO -> habilitas las 6 unidades medidas + sello del pre-registro N=6.

## Guardrails (sin cambio)
SOLO Aegis (hub 2E35F26E/1.14.0 intacto; anchor canonico-solo, Julian nunca lo corre). Privada de jheredia SOLO en
su maquina. maker!=checker por llave.

-- Arquitecto (2026-07-12 22:10 local/UTC+2)
