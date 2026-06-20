# APPLY - Promocion DECISION-0043 + SPEC-0082 + TASK-0120 (v1.12.0, #4 OFF)

> ENCOLADO por el Arquitecto para que el MIRROR lo aplique sobre la copia que SI persiste a disco
> (split cache-vs-disco, corrupcion recurrente del mount - RUNBOOK-windows-sandbox-temp-acl).
> GO del operador: promover (MINOR + CHANGELOG, #4 OFF). Autor del diseno: Arquitecto. NO enciende #4.

## Precondicion (gate de integridad del operador) - SECUENCIA ATOMICA EN EL MISMO SHELL
Ejecutor = MIRROR, en una copia con ACLs heredadas que **NO se re-trunca** (checkout fresco fuera del
mount, NO el mount que se re-trunca solo). HEAD sano de referencia = `426da8f`. Secuencia atomica:
1. `git restore --source=HEAD -- runtime/submit_intent.py scripts/validate_collaboration_state.py
   runtime/state/events.jsonl runtime/state/snapshot.json Area_comun/state/*.json`
2. Verificar: `py_compile` de los 2 .py OK + `validate_collaboration_state.py --root .` verde + drift 0 +
   `git status` limpio == HEAD.
3-4. (pasos 1-5 de abajo: crear canonicos + cfg + CHANGELOG + submit_intent + read-back en DISCO
   cfg=1.12.0 & 3 canonicos creados & drift 0 + commit).
5. Si entre verify y commit el arbol se re-trunca -> **ABORTAR** (no anclar/escribir estado corrupto),
   re-restore y reintentar.
(Esto NO es el re-genesis/flip de #4; es solo la promocion del cargador. NO toca event_state flags;
#4 sigue OFF; sin re-genesis.)

## ATOMICIDAD (causa raiz del medio-aplicado, 10:04Z) - TODO o NADA
El submit_intent (la tx de 5 ops del LEDGER) es el paso que DEFINE el exito. Editar cfg/docs/canonicos NO
necesita submit_intent, asi que NO se debe hacer suelto: si se editan los archivos pero la tx del ledger
no aplica, queda "declarativo-sin-ledger" = DRIFT (config 1.12.0 pero PROJECT_STATE/events en 1.11.0).
REGLA: el read-back (pasos 4-5) DEBE mostrar el EVENTO de ledger (decision DECISION-0043 + task_upsert
TASK-0120 + project_narrative 1.12.0) en events.jsonl + PROJECT_STATE.version=1.12.0 + TASK_INDEX con
TASK-0120 + drift 0. Si el read-back NO muestra el evento de ledger (o submit_intent fallo/se bloqueo o el
arbol se re-trunco): **REVERTIR TODO a HEAD** (`git restore` tracked + `rm` los 3 canonicos untracked,
SOLO esos por path) y reintentar desde el gate; **NUNCA** dejar los edits de archivo sin el ledger.
Los edits de archivo solo se CONSERVAN/commitean si el ledger avanzo en el mismo intento.

## Orden de aplicacion

1. **Crear los 3 archivos canonicos** (cp draft -> canonico, ASCII; los drafts ya estan en
   personal/Arquitecto/carril_A/):
   - `Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md`
     <- DRAFT-DECISION-0043-event-auth-secret-resolution.md (cambiar `status: draft` -> `status: accepted`,
        y quitar el blockquote "DRAFT ... NO promovida").
   - `Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md`
     <- DRAFT-SPEC-0082-event-auth-secret-resolution.md (cambiar `status: draft` -> `status: accepted`,
        quitar "(DRAFT)" del titulo H1).
   - `Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md`
     <- DRAFT-TASK-0120-event-auth-secret-resolution.md (tal cual; status ready, owner Codex).

2. **Editar `protocol.config.json`** (edicion PUNTUAL, nunca json.dump):
   `"protocol_version": "1.11.0"` -> `"protocol_version": "1.12.0"`. NO tocar event_state (flags #4 OFF).

3. **CHANGELOG.md** - anadir bloque `[1.12.0]` (debajo del encabezado, sobre [1.11.0]):
   ```
   ## [1.12.0] - 2026-06-19
   ### Added
   - DECISION-0043 + SPEC-0082 + TASK-0120: resolucion del secreto HMAC de `event_auth` por referencia
     (`secret_file` keyfile gitignored / `secret_env`), fuera del repo commiteado, como precondicion de
     activacion de #4 (SPEC-0081 AC1, capa HMAC). Aditivo, neutral, off-by-default; el secreto resuelto no
     entra a genesis/canonical_json/prev_hash; fail-closed; gate dedicado de no-literal-commiteado. La
     privada Ed25519 sigue wrapper-side. #4 permanece OFF (chain/agent_signatures/anchor/event_auth=false).
   ```

4. **submit_intent (tx atomica count=5)** con la copia que persiste:
   ```
   python runtime/submit_intent.py --intents personal/Arquitecto/carril_A/PROMOTE-0043-intents.json \
     --actor-id Arquitecto --timestamp 2026-06-19T09:40:00Z --commit <pending-or-HEAD>
   ```
   (claim acquire -> decision DECISION-0043 -> task_upsert TASK-0120 ready -> project_narrative 1.12.0 ->
   claim release). Verificar salida sin rechazos.

5. **Gates verdes (en la copia que persiste):**
   `validate_collaboration_state.py --root .` (drift 0, replay==hot) + `scan_encoding.py` +
   `scan_domain_neutrality.py`. Confirmar events.jsonl crecio +5 y persiste a disco (no re-truncado).

6. **Higiene de mailbox = YA HECHA por el operador** (msg aplicar-promo-mirror). NO re-ejecutar (la tx
   ledger es idempotente respecto a esa higiene). Solo queda que, al confirmar el commit v1.12.0, las
   respuestas pendientes (integridad-recurrente, aplicar-promo-mirror) pasen a answered.

7. **Commit** (staging EXPLICITO por path; nunca `git add -A`):
   ```
   git add Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md \
           Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md \
           Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md \
           protocol.config.json CHANGELOG.md \
           Area_comun/state/CLAIMS.json Area_comun/state/CLAIMS.slim.json \
           Area_comun/state/PROJECT_STATE.json Area_comun/state/PROJECT_STATE.slim.json \
           Area_comun/state/TASK_INDEX.json Area_comun/state/TASK_INDEX.slim.json \
           runtime/state/events.jsonl runtime/state/snapshot.json \
           Area_comun/mailbox/answered/ Area_comun/mailbox/archived/
   git commit -m "feat(protocol): v1.12.0 - cargador HMAC event_auth fuera del repo (DECISION-0043/SPEC-0082/TASK-0120 ready); #4 OFF"
   ```
   (Mensaje termina con la linea Co-Authored-By estandar.)

8. **Post-commit:** memoria (DECISION-0026) + push si verde.

## Limites
#4 OFF (chain/agent_signatures/anchor/event_auth=false). Sin SA.4/Capa C/subagents. No re-genesis aqui
(esta promocion no toca event_state). TASK-0120 queda READY para que Codex implemente (maker!=checker:
Codex implementa, Arquitecto reproduce). Canal ASCII en mailbox/state.
