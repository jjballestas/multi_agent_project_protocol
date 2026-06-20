# RECONCILE - Promocion DECISION-0043/SPEC-0082/TASK-0120 medio-aplicada (v1.12.0, #4 OFF)

> El primer intento dejo DRIFT: declarativo aplicado (cfg 1.12.0 + 3 canonicos untracked + CHANGELOG) pero
> LEDGER no (0 eventos, events.jsonl 538 corrupto, TASK_INDEX sin TASK-0120, sin commit). Causa: el
> restore+verify se SALTO y `submit_intent.py` no compila en la copia corrupta, asi que solo aterrizo lo
> que NO necesita submit_intent. Reconciliacion del operador (msg promo-medio-aplicada): abortar -> clean
> ==HEAD -> verify -> redo ATOMICO con el ledger -> read-back -> commit. NO forward-fix sobre lo corrupto.
> Ejecutor = MIRROR en CHECKOUT FRESCO con ACLs heredadas que NO se re-trunca. #4 OFF. HEAD sano = 426da8f
> (events 646). La tx es idempotente (idempotency keys) -> partir de HEAD limpio no duplica.

## Secuencia (un solo shell, atomica, abortable)

### Paso 0 - ABORTAR lo medio-aplicado -> limpio == HEAD
```
git restore --source=HEAD -- protocol.config.json CHANGELOG.md \
  runtime/submit_intent.py scripts/validate_collaboration_state.py \
  runtime/state/events.jsonl runtime/state/snapshot.json Area_comun/state/*.json
git clean -f -- Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md \
  Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md \
  Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md
```
(restore revierte cfg 1.12.0->1.11.0 + CHANGELOG; clean borra los 3 canonicos untracked.)

### Paso 1 - GATE DURO (PRECONDICION QUE ABORTA, no opcional)
Verificar TODO antes de escribir NADA:
- `python -m py_compile runtime/submit_intent.py scripts/validate_collaboration_state.py` -> OK
- `runtime/state/events.jsonl` == HEAD (646 lineas)
- `python scripts/validate_collaboration_state.py --root .` VERDE + drift 0
- `git status` limpio == HEAD (sin M, sin ??)
**Si CUALQUIERA falla (p.ej. submit_intent.py no compila, events != 646) -> ABORTAR sin escribir,
re-restore y reintentar. NO continuar.**

### Paso 2 - LEDGER PRIMERO (la parte que fallo; si falla, nada mas se escribio)
```
python runtime/submit_intent.py --intents personal/Arquitecto/carril_A/PROMOTE-0043-intents.json \
  --actor-id Arquitecto --timestamp 2026-06-19T09:40:00Z --commit <pending>
```
Verificar salida sin rechazos + EVENTO de ledger presente: `grep -c 'DECISION-0043\|TASK-0120'
runtime/state/events.jsonl` > 0; TASK-0120 en TASK_INDEX (status ready); project_state.version=1.12.0;
drift 0. **Si submit_intent falla -> ABORTAR (no tocar cfg/docs); diagnosticar; no dejar declarativo
suelto.**

### Paso 3 - DECLARATIVO (solo despues de que el ledger entro)
- `protocol.config.json`: editar PUNTUAL `"protocol_version": "1.11.0"` -> `"1.12.0"`.
- Crear los 3 canonicos (cp draft -> canonico; DECISION/SPEC `status: accepted`, TASK ready; ASCII).
- CHANGELOG.md: bloque `[1.12.0]` (texto en PROMOTE-0043-APPLY.md paso 3).

### Paso 4 - READ-BACK EN DISCO (los 6, incluido el LEDGER)
- cfg = 1.12.0; project_state.version = 1.12.0 (alineados)
- DECISION-0043 / SPEC-0082 / TASK-0120 canonicos presentes
- evento de ledger DECISION-0043/TASK-0120 en events.jsonl; TASK-0120 en TASK_INDEX (ready)
- `validate --root .` verde + drift 0; events.jsonl crecio sobre 646 (no 538)

### Paso 5 - COMMIT UNICO (staging EXPLICITO)
```
git add Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md \
        Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md \
        Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md \
        protocol.config.json CHANGELOG.md \
        Area_comun/state/CLAIMS.json Area_comun/state/CLAIMS.slim.json \
        Area_comun/state/PROJECT_STATE.json Area_comun/state/PROJECT_STATE.slim.json \
        Area_comun/state/TASK_INDEX.json Area_comun/state/TASK_INDEX.slim.json \
        runtime/state/events.jsonl runtime/state/snapshot.json
git commit -m "feat(protocol): v1.12.0 - cargador HMAC event_auth fuera del repo (DECISION-0043/SPEC-0082/TASK-0120 ready); #4 OFF"
```

### Aborto/re-truncacion
Si en CUALQUIER punto el arbol se re-trunca (events vuelve a 538, .py deja de compilar) -> ABORTAR,
re-restore (Paso 0), reintentar. Nunca commitear estado torn.

## Despues (solo con los 6 en disco + commit + drift 0)
GO de implementacion a Codex para TASK-0120 con las 4 condiciones del operador: #4 OFF, fixtures-only,
golden AC1-AC8 verde, maker!=checker. Higiene mailbox ya hecha por el operador. Memoria DECISION-0026.
Gate del operador (su ventana) sigue para provisioning REAL + anchor + re-genesis + piloto + flip #4.
