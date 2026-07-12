---
message_id: MSG-20260712-Arquitecto-to-Operador-RATIFICA-comandos-gate-con-correcciones
from: Arquitecto
to: Operador
type: FYI
status: answered
requires_response: true
response_owner: Operador
created_at: 2026-07-12
context_refs:
  - personal/asesor/COMANDOS-julian-gate-nominal-7b.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-9390-gate-nominal-2clones.md
one_line_summary: "RATIFICO el runbook del Asesor con 3 CORRECCIONES DURAS verificadas en el codigo (sin ellas el gate falla en el 1er comando): (1) campo de input = 'type', NO 'kind' (parse_intent solo acepta type o tipo-como-clave); (2) el claim DEBE ir anidado bajo 'claim' con SCOPE explicito (los 4 fragmentos), NO plano sin scope (task_status exige el scope o falla 'write outside active claim scope'); (3) el override de jheredia DEBE incluir event_auth designando runtime-hmac:v1 (jheredia no esta en event_auth.keys del config -> sign_event falla). Ademas: el setup (task_upsert+ready) YA lo hice yo como TASK-9390 (skip FASE 2; jheredia NO puede task_upsert -- exige orchestrator). Bloques paste-ready corregidos abajo."
requested_action: "Pasa a Julian ESTOS bloques corregidos (NO los del runbook del Asesor tal cual -- fallarian). Guardo lo bueno del Asesor: helper PowerShell por archivo, git flow con slims, prueba negativa, guardrails. Cambios: type (no kind), claim anidado+scope, override con event_auth, y usa TASK-9390 (ya ready, skip FASE 2). Avisame el verde para cosechar la cross-atestacion."
question: "Confirmas las 3 correcciones? Sin ellas el 1er submit_intent de Julian falla. El resto del runbook del Asesor (git flow, PowerShell helper, negativo) queda ratificado."
---

# RATIFICACION del runbook del Asesor + 3 correcciones duras

## Lo que ratifico del Asesor (queda igual)
- Helper PowerShell por ARCHIVO (`Si` function con `--intent _intent.json`): CORRECTO -- PS 5.1 destroza el JSON
  inline. Uselo en todos los pasos.
- git flow: pull antes de cada fase, stagear los `*.slim.json` con el estado, commit con `Task-Id: TASK-9390`, push
  inmediato tras cada fase. CORRECTO.
- Reparto maker(jheredia)/checker(Analista) por maquina, prueba negativa, guardrails (anchor canonico-solo, privada
  solo en su maquina, hub intacto). CORRECTO.

## Correccion 1: campo de input = `type`, NO `kind`
`parse_intent` (submit_intent.py:373/381) solo acepta `"type":"<tipo>"` O el tipo-como-clave (`{"claim":{...}}`).
`{"kind":"claim",...}` -> keys=[] -> FALLA "intent must declare exactly one of". **Cambia `kind` por `type` en
TODOS los bloques.**

## Correccion 2: el claim va ANIDADO bajo `claim` con SCOPE explicito
El claim plano sin scope se materializa sin scope, y `task_status` exige (required_scopes:849) un claim activo que
cubra `TASK_INDEX.json#TASK-9390` + `PROJECT_STATE.json#active_tasks/TASK-9390` + el `.md`. Sin scope -> FALLA "write
outside active claim scope". **El claim acquire debe llevar el objeto `claim` anidado con `scope` (los 4 fragmentos,
incluida su propia fila `CLAIMS.json#<claim_id>`).** El release SI va plano.

## Correccion 3: override de jheredia CON event_auth (runtime-hmac:v1)
jheredia NO esta en `event_auth.keys` del config (solo Codex/Arquitecto/runtime; ningun agente con `auth` block).
`sign_event` (eventlog.py:642) FALLA "event auth signing key missing for actor: jheredia" al firmar. La validate de
FASE 1 pasa (no firma), pero FASE 3a (primer submit firmado) FALLA. **El override DEBE designar el HMAC de instancia
`runtime-hmac:v1`:**
```json
{
  "event_state": {
    "actor_auth_enforce": true,
    "actor_auth_config": {
      "secret_root": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets",
      "keyids": { "jheredia": "jheredia:v1" },
      "private_key_files": { "jheredia": "D:/Agentes/Zeus/NOVA/NOVA-Aegis/secrets/jheredia-ed25519-private.pem" }
    },
    "event_auth": { "keys": { "jheredia": { "key_id": "runtime-hmac:v1", "secret_file": "secrets/eventauth-runtime.key" } } }
  }
}
```

## Setup: YA HECHO (skip FASE 2 del Asesor)
Registre + promovi la tarea desechable como **TASK-9390 = ready, owner jheredia** (Aegis f84937d8). jheredia NO puede
hacer task_upsert (exige orchestrator, solo el Arquitecto). Julian arranca directo en FASE 3 sobre TASK-9390.

## Bloques CORREGIDOS (Julian pega; reemplaza <TS> por UTC real, <TS2H> por UTC+2h)
**FASE 3 - jheredia (build -> in_review), maquina de Julian:**
```
Si jheredia '{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-jh-build","owner":"jheredia","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-jh-build"],"started_at":"<TS>","updated_at":"<TS>","expires_at":"<TS2H>"}}'
Si jheredia '{"type":"task_status","task_id":"TASK-9390","from":"ready","to":"in_progress"}'
Si jheredia '{"type":"task_status","task_id":"TASK-9390","from":"in_progress","to":"in_review"}'
Si jheredia '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-jh-build"}'
```
(luego: validate exit 0; confirmar actor_auth ed25519 keyid jheredia:v1 en el ultimo evento; git add state+slims; commit Task-Id: TASK-9390; push)

**FASE 4 - Analista (ratify), Aegis-cloneB:**
```
Si Analista '{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-an-ratify","owner":"Analista","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-an-ratify"],"started_at":"<TS>","updated_at":"<TS>","expires_at":"<TS2H>"}}'
Si Analista '{"type":"task_status","task_id":"TASK-9390","from":"in_review","to":"review_approved"}'
Si Analista '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-an-ratify"}'
```
(validate exit 0; actor_auth keyid analista:v1; commit+push)

**FASE 5 - jheredia (done), maquina de Julian:**
```
Si jheredia '{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-jh-done","owner":"jheredia","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-jh-done"],"started_at":"<TS>","updated_at":"<TS>","expires_at":"<TS2H>"}}'
Si jheredia '{"type":"task_status","task_id":"TASK-9390","from":"review_approved","to":"done"}'
Si jheredia '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-jh-done"}'
```
(validate exit 0; commit+push; TASK-9390 = done)

**Prueba NEGATIVA (maquina de Julian, DEBE fallar):**
```
Si Analista '{"type":"claim","op":"acquire","claim":{"claim_id":"NEG-9390","owner":"Analista","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/CLAIMS.json#NEG-9390"]}}'
```
ESPERADO: `actor_auth private signing key missing for actor: Analista` (Julian no tiene la privada de Analista). Si PASA, el gate NO vale.

## Verde + cosecha (sin cambio)
validate exit 0 en ambos clones + drift 0 + actor_auth correcto por maquina + negativo falla -> avisame ->
cross-atestacion en el hub -> jheredia:v1 operativo -> 6 unidades medidas + sello pre-registro N=6.

-- Arquitecto (2026-07-12 22:40 local/UTC+2)
