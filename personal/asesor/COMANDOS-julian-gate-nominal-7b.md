# Comandos -- Gate 2-clones nominal (TASK-9390) -- VERSION AUTORITATIVA

> Verificado en codigo por el Arquitecto (MSG RATIFICA, ce4ac46) + revalidado por el parser real por el Asesor.
> Tarea = TASK-9390 (ya registrada = ready por el Arquitecto; jheredia NO puede task_upsert). Reparto:
> Julian = maker (jheredia:v1) | Aegis-cloneB (John) = checker (Analista). Helper = `Enviar` (NO `Si`: choca con Set-Item).
>
> **NOTA NOVA (2026-07-13, correccion):** esta receta documenta el gate A2-nominal sobre la instancia VIEJA **Aegis**
> (hecho, historico). Para **NOVA** (modelo 2.A, instancia actual): el clon esta en `D:/Agentes/NOVA-Suite/NOVA` con la
> gobernanza bajo `Aegis/`; el `secret_root` es `protocol-secrets/` (NO `secrets/`); y el `event_auth` de jheredia usa
> **`key_id: codex-hmac:v1`, `secret_file: protocol-secrets/codex-eventauth.key`** (Julian opera bajo la autenticacion
> de runtime de Codex). En NOVA NO existe `runtime-hmac:v1` / `secrets/eventauth-runtime.key` (eso era de Aegis). Los
> comandos de abajo conservan rutas/valores de Aegis por fidelidad historica; para NOVA, sustituye segun esta nota.

## SETUP DE SESION (Julian, una vez)
```powershell
cd D:\Agentes\Zeus\NOVA\NOVA-Aegis
function Enviar($actor, $json) {
  $json | Out-File -FilePath _intent.json -Encoding ascii
  $ts = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  python runtime/submit_intent.py --actor-id $actor --intent _intent.json --timestamp $ts
}
```

## FASE 1 -- Override CORREGIDO (con event_auth) [Julian]
> jheredia NO esta en event_auth.keys del config -> sin este bloque, sign_event falla "event auth signing key missing".
```powershell
@'
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
'@ | Out-File -FilePath event-state.runtime.json -Encoding ascii
python scripts/validate_collaboration_state.py
```

## FASE 3 -- jheredia: build -> in_review [Julian]
> El claim acquire lleva timestamps embebidos -> se usa here-string @"..."@ (interpola $ts). Los demas van con Enviar.
```powershell
git pull --ff-only origin main

$ts   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$ts2h = (Get-Date).ToUniversalTime().AddHours(2).ToString("yyyy-MM-ddTHH:mm:ssZ")
@"
{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-jh-build","owner":"jheredia","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-jh-build"],"started_at":"$ts","updated_at":"$ts","expires_at":"$ts2h"}}
"@ | Out-File _intent.json -Encoding ascii
python runtime/submit_intent.py --actor-id jheredia --intent _intent.json --timestamp $ts

Enviar jheredia '{"type":"task_status","task_id":"TASK-9390","from":"ready","to":"in_progress"}'
Enviar jheredia '{"type":"task_status","task_id":"TASK-9390","from":"in_progress","to":"in_review"}'
Enviar jheredia '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-jh-build"}'

python scripts/validate_collaboration_state.py
Get-Content runtime/state/events.jsonl -Tail 1      # ver actor_auth: ed25519 / keyid jheredia:v1
git add Area_comun/state/ Area_comun/tasks/ runtime/state/events.jsonl runtime/state/snapshot.json
git commit -m "gate(TASK-9390): jheredia build->in_review" -m "Task-Id: TASK-9390"
git push origin main
```

## FASE 4 -- Analista: ratify (in_review -> review_approved) [John, en Aegis-cloneB]
```powershell
# (misma funcion Enviar definida en cloneB)
git pull --ff-only origin main
$ts   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$ts2h = (Get-Date).ToUniversalTime().AddHours(2).ToString("yyyy-MM-ddTHH:mm:ssZ")
@"
{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-an-ratify","owner":"Analista","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-an-ratify"],"started_at":"$ts","updated_at":"$ts","expires_at":"$ts2h"}}
"@ | Out-File _intent.json -Encoding ascii
python runtime/submit_intent.py --actor-id Analista --intent _intent.json --timestamp $ts
Enviar Analista '{"type":"task_status","task_id":"TASK-9390","from":"in_review","to":"review_approved"}'
Enviar Analista '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-an-ratify"}'
python scripts/validate_collaboration_state.py
git add Area_comun/state/ Area_comun/tasks/ runtime/state/events.jsonl runtime/state/snapshot.json
git commit -m "gate(TASK-9390): analista review_approved" -m "Task-Id: TASK-9390"
git push origin main
```

## FASE 5 -- jheredia: done [Julian]
```powershell
git pull --ff-only origin main
$ts   = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$ts2h = (Get-Date).ToUniversalTime().AddHours(2).ToString("yyyy-MM-ddTHH:mm:ssZ")
@"
{"type":"claim","op":"acquire","claim":{"claim_id":"CLAIM-GATE-9390-jh-done","owner":"jheredia","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/TASK_INDEX.json#TASK-9390","Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-9390","Area_comun/tasks/TASK-9390-gate-nominal-2clones.md","Area_comun/state/CLAIMS.json#CLAIM-GATE-9390-jh-done"],"started_at":"$ts","updated_at":"$ts","expires_at":"$ts2h"}}
"@ | Out-File _intent.json -Encoding ascii
python runtime/submit_intent.py --actor-id jheredia --intent _intent.json --timestamp $ts
Enviar jheredia '{"type":"task_status","task_id":"TASK-9390","from":"review_approved","to":"done"}'
Enviar jheredia '{"type":"claim","op":"release","claim_id":"CLAIM-GATE-9390-jh-done"}'
python scripts/validate_collaboration_state.py
git add Area_comun/state/ Area_comun/tasks/ runtime/state/events.jsonl runtime/state/snapshot.json
git commit -m "gate(TASK-9390): jheredia done-flip" -m "Task-Id: TASK-9390"
git push origin main
```

## FASE 6 -- Prueba NEGATIVA (Julian, DEBE fallar)
```powershell
Enviar Analista '{"type":"claim","op":"acquire","claim":{"claim_id":"NEG-9390","owner":"Analista","task_id":"TASK-9390","status":"active","scope":["Area_comun/state/CLAIMS.json#NEG-9390"]}}'
# ESPERADO: "actor_auth private signing key missing for actor: Analista" (Julian no tiene la privada de Analista).
# Si PASA en vez de fallar, el gate NO es valido.
```

## VERDE del gate
validate exit 0 en ambos clones + drift 0 + actor_auth correcto por maquina + negativo falla ->
avisar al Arquitecto -> cross-atestacion en el hub -> jheredia:v1 OPERATIVO -> 6 unidades medidas + sello pre-registro N=6.

## GUARDRAILS
- Julian NUNCA corre el anchor (canonico-solo). Su privada jamas sale de su maquina. Hub 2E35F26E/1.14.0 intacto.
- Push inmediato tras cada fase (un flip sin pushear es invisible para el clon par). Stagear el estado + runtime/state.
