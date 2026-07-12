---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-gate-nominal-CORREGIDO
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Operador-RESP-gate-nominal-intents-y-override.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-9390-gate-nominal-2clones.md
one_line_summary: "CORREGIDO tras tu 'revisa mensaje': el runbook anterior tenia a jheredia haciendo task_upsert, pero task_upsert exige capability ORCHESTRATOR (jheredia es implementer -> habria fallado). Fix: el ARQUITECTO hace el setup (task_upsert + ready), YA HECHO (Aegis f84937d8, TASK-9390 ready). jheredia + Analista solo firman el ciclo. Override de jheredia sin cambio (con HMAC de instancia runtime-hmac:v1). Bloques corregidos abajo."
requested_action: "Descarta el runbook anterior; usa ESTE. El setup ya esta hecho (TASK-9390 ready en Aegis). Pasa a Julian: (1) el override corregido de jheredia (con event_auth runtime-hmac:v1); (2) los 2 bloques de jheredia + 1 de Analista de abajo (SIN task_upsert -- ese ya lo hice yo). Avisame validate exit 0 en ambos clones + prueba negativa + drift 0 para cosechar."
question: "Confirmas el flujo corregido (Arquitecto hace el setup orchestrator; jheredia/Analista solo firman)? Avisame cuando el gate quede verde."
---

# RESP CORREGIDO - gate 2-clones nominal (tras revisar el mensaje)

## Que estaba mal (buena que pediste revisar)
El runbook anterior ponia a **jheredia** haciendo el `task_upsert` de la tarea desechable. Verificado en
`submit_intent.py:959-961`: **`task_upsert` exige capability `orchestrator`**, y jheredia es `implementer` (Codex/
Analista tampoco lo tienen; solo el Arquitecto). -> habria fallado con "lacks required capability: orchestrator".

## Fix: el Arquitecto hace el setup (YA HECHO)
Registre + promovi la tarea desechable yo (orchestrator): **TASK-9390 = ready, owner jheredia** en Aegis
(commit `f84937d8`, validate 0). Julian solo hace `git pull` y corre su ciclo de firma. El resto del reparto es
correcto (jheredia maker por posesion de su ed25519; Analista checker en cloneB).

## Override de jheredia (SIN cambio respecto al corregido -- con HMAC de instancia)
`event-state.runtime.json` de Julian (gitignored): actor_auth_config con su ed25519 + **event_auth designando
runtime-hmac:v1** (jheredia NO esta en event_auth.keys del config; sin este bloque, sign_event falla). Ver el bloque
JSON exacto en mi mensaje anterior s.1 (ese sigue vigente).

## Ciclo core corregido (Julian pega estos; el setup ya esta)
Reemplaza `<TS>` por UTC real (= `--timestamp` y los started_at/updated_at del claim). expires_at = `<TS+2h>`.

**A. jheredia (maquina de Julian, `--actor-id jheredia`)** -- pull, claima el ready, lleva a in_review, libera:
```
git pull --ff-only origin main
python runtime/submit_intent.py --root . --actor-id jheredia --timestamp <TS> --commit $(git rev-parse HEAD) --intents -
```
intents (idempotency_key `jheredia:gate-9390-maker`): `claim` acquire {claim_id CLAIM-GATE-9390-jheredia, owner
jheredia, task_id TASK-9390, status active, scope ["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/
PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/
CLAIMS.json#CLAIM-GATE-9390-jheredia"], started_at <TS>, updated_at <TS>, expires_at <TS+2h>} -> `task_status`
{task_id TASK-9390, from ready, to in_progress} -> `task_status` {from in_progress, to in_review} -> `claim` release
{claim_id CLAIM-GATE-9390-jheredia}. Verifica: `validate` exit 0; el claim/flip lleva `actor_auth {method: ed25519,
keyid: jheredia:v1}`. commit (Task-Id: TASK-9390) + push.

**B. Analista (Aegis-cloneB, `--actor-id Analista`)** -- pull, claim propio, flip de checker, release:
```
git pull --ff-only origin main
```
intents (idempotency_key `analista:gate-9390-checker`): `claim` acquire {claim_id CLAIM-GATE-9390-analista, owner
Analista, task_id TASK-9390, status active, scope [los 4 fragmentos con #CLAIM-GATE-9390-analista], started_at <TS>,
updated_at <TS>, expires_at <TS+2h>} -> `task_status` {task_id TASK-9390, from in_review, to review_approved} ->
`claim` release {claim_id CLAIM-GATE-9390-analista}. Verifica: `validate` exit 0; el flip lleva `actor_auth {keyid:
analista:v1}`. commit (Task-Id: TASK-9390) + push.

**C. jheredia done (maquina de Julian, `--actor-id jheredia`)** -- pull, claim, done, release:
```
git pull --ff-only origin main
```
intents (idempotency_key `jheredia:gate-9390-done`): `claim` acquire {claim_id CLAIM-GATE-9390-jheredia-done, owner
jheredia, task_id TASK-9390, status active, scope [los 4 fragmentos con #CLAIM-GATE-9390-jheredia-done]} ->
`task_status` {task_id TASK-9390, from review_approved, to done} -> `claim` release {claim_id
CLAIM-GATE-9390-jheredia-done}. Verifica: `validate` exit 0. commit (Task-Id: TASK-9390) + push. TASK-9390 = done.

## Prueba NEGATIVA (maker!=checker por llave)
En la maquina de Julian: `python runtime/submit_intent.py --actor-id Analista --intent-json '{"type":"claim","op":
"acquire","claim":{"claim_id":"NEG-TEST","owner":"Analista","task_id":"TASK-9390","status":"active","scope":["Area_
comun/state/CLAIMS.json#NEG-TEST"]}}'` -> DEBE fallar con `actor_auth private signing key missing for actor:
Analista` (Julian no tiene la privada de Analista).

## Verde + cosecha
validate exit 0 en AMBOS clones + drift 0 + actor_auth correcto por maquina + la prueba negativa falla. Avisame ->
registro la Entrada de cross-atestacion en el hub -> jheredia:v1 OPERATIVO -> habilitas las 6 unidades medidas +
sello del pre-registro N=6. Guardrails sin cambio (SOLO Aegis; privada de jheredia solo en su maquina; anchor
canonico-solo).

-- Arquitecto (2026-07-12 22:25 local/UTC+2)
