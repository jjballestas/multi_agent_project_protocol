# RUNBOOK - Activacion viva de la Consola del Arquitecto

> Autor: Arquitecto. Para: operador. Gobierna: DECISION-0062 (consola/puente) + DECISION-0063 (launcher).
> Estado del codigo: COMPLETO y verde (TASK-0185 puente, 0186 UI, 0187 auditoria, 0188 launcher; test:ci 106/106).
> La consola nace **OFF-by-default**; encenderla es ESTE procedimiento, con el operador presente. **El flag NUNCA
> se commitea** (config de runtime gitignored).

## 0. Transferencia de rol (clave)

Al revivir un Arquitecto interactivo via la consola (Zeus), **ese runtime pasa a ser EL Arquitecto** y la sesion
CLI actual (la que autoro esto) **cambia de estatus a ASISTENTE del operador** (ya no Arquitecto). Asi se honra la
**sesion unica**: no hay dos Arquitectos en paralelo, hay un relevo. No abras un segundo Arquitecto por fuera
mientras la consola este viva.

## 1. Precondicion

- Repo producto en `D:/Agentes/Zeus/Zeus-protocol`, en `main` con el launcher (`scripts/architect-runtime-launcher.mjs`).
- Node 20+. (Para uso vivo real, ademas: el CLI/binario que corre un turno del Arquitecto leyendo stdin y emitiendo
  stdout = el "inner-runtime".)

## 2. Config de activacion (gitignored, NO commitear)

Crear en el repo Zeus el archivo **`architect-bridge.runtime.json`** (esta en `.gitignore`):

```json
{
  "schemaVersion": "1.0",
  "architectBridge": {
    "enabled": true,
    "operatorPresentRequired": true,
    "command": "node",
    "args": ["D:/Agentes/Zeus/Zeus-protocol/scripts/architect-runtime-launcher.mjs"],
    "env": {
      "ARCHITECT_RUNTIME_COMMAND": "<inner-cmd>",
      "ARCHITECT_RUNTIME_ARGS": "[\"<arg-absoluto-1>\",\"<arg-2>\"]",
      "ARCHITECT_EXISTING_IDENTITY": "Arquitecto",
      "ARCHITECT_RUNTIME_LOCK_PATH": "D:/Agentes/Zeus/Zeus-protocol/.runtime/architect-runtime-launcher.lock"
    }
  }
}
```

- `enabled:true` + `operatorPresentRequired:true` = on, con confirmacion de presencia.
- El puente hace `spawn(command, args, { cwd: <repo PROTOCOLO>, env: {...process.env, ...env} })`.
- **IMPORTANTE - rutas ABSOLUTAS:** el puente spawnea con `cwd = repo PROTOCOLO` (no Zeus), y el launcher
  spawnea el inner con ese mismo cwd. Por eso **`args` (ruta del launcher) y cualquier ruta en
  `ARCHITECT_RUNTIME_ARGS` (el inner) deben ser ABSOLUTAS**, o el inner debe estar en el PATH. Rutas relativas
  fallan en vivo (en los tests funcionaban porque alli el cwd era el repo Zeus).
- El **launcher** lee del env: `ARCHITECT_RUNTIME_COMMAND`/`ARGS` (el inner), `ARCHITECT_EXISTING_IDENTITY`,
  `ARCHITECT_RUNTIME_LOCK_PATH` (lock de instancia unica; por defecto junto al launcher en Zeus/.runtime).

## 3. PRIMER SMOKE SEGURO (inner = STUB, sin Arquitecto real)

Para probar la fontaneria viva SIN costo ni Arquitecto real, usa el stub de los tests como inner:

```
"ARCHITECT_RUNTIME_COMMAND": "node",
"ARCHITECT_RUNTIME_ARGS": "[\"D:/Agentes/Zeus/Zeus-protocol/tests/fixtures/architect-runtime-stub.mjs\"]"
```
(ruta ABSOLUTA al stub; ver la nota de rutas en la seccion 2)

Arrancar el front (PowerShell, en el repo Zeus):

```powershell
$env:PROTOCOL_REPO_PATH="D:/Agentes/multi_agent_project_protocol"
$env:ZEUS_ROOT_PATH="D:/Agentes/Zeus"
$env:ARCHITECT_BRIDGE_CONFIG_PATH="D:/Agentes/Zeus/Zeus-protocol/architect-bridge.runtime.json"
npm start
```

Smoke por API (otra terminal) o por la vista **Consola Arquitecto** en `http://127.0.0.1:<puerto>`:

- `GET  /api/protocol/architect-bridge`            -> `enabled:true`, `status:"dormant"`, `singleSession:true`, `noLedgerWriter:true`
- `POST /api/protocol/architect-bridge/open`  body `{"operatorPresent":true}` -> `status:"alive"`, un `sessionId`
- `POST /api/protocol/architect-bridge/send`  body `{"message":"hola"}`        -> 200
- `GET  /api/protocol/architect-bridge/stream` (SSE)                            -> evento `output` con `stub-turn-1:Arquitecto:hola`
- `POST /api/protocol/architect-bridge/stop`                                    -> `status:"dormant"`

Esperado: la consola abre, transmite la respuesta del stub, y finaliza limpio. Eso valida puente+UI+launcher vivos.

## 4. ACTIVACION REAL (inner = Arquitecto real) -- relevo de rol

Cuando el smoke pase, cambia el inner por el CLI real del Arquitecto:

```
"ARCHITECT_RUNTIME_COMMAND": "<binario/CLI del Arquitecto>",
"ARCHITECT_RUNTIME_ARGS": "[...flags para modo interactivo: lee stdin (1 mensaje/turno), emite stdout]"
```

- El inner debe correr con la **identidad EXISTENTE** del Arquitecto (su keypair ya registrada); el launcher NO crea
  identidad. Cualquier mutacion de estado que haga el Arquitecto vivo va por `submit_intent` (no-bypass; #4 intacto).
- Al hacer `open` + `send`, **este asistente (CLI) deja de actuar como Arquitecto** (relevo de seccion 0).
- Reiniciar el front con el config actualizado y repetir open/send.

## 5. Uso, cese y desactivacion

- **Usar:** vista Consola Arquitecto -> open -> escribir/enviar -> ver streaming -> finalizar.
- **Cese:** `stop` (o cerrar stdin) termina inner+launcher limpio (sin huerfanos). La UI pasa a `dormant`.
- **Desactivar del todo:** `enabled:false` en `architect-bridge.runtime.json` (o borrar el archivo) -> el puente
  no lanza nada (off-by-default). Reiniciar el front.

## 6. Garantias / invariantes (recordatorio)

- **No-bypass:** la consola es control+observabilidad; toda mutacion via `submit_intent`. Nunca escribe el ledger.
- **Runtime-only:** el launcher solo lanza/finaliza; no toca identidad/llaves/registro/config (#4 intacto).
- **Sesion unica:** una sesion viva; `open` reusa la existente; lock/PID en el launcher.
- **Off-by-default:** sin el runtime config (enabled+command), nada corre. El flag no se commitea.
- **Auditoria redactada:** la conversacion se audita en `.runtime/architect-bridge/sessions/<id>.jsonl` (gitignored,
  fuera del #4), con PII redactada por familias y tope 200 eventos/sesion.

## 7. Troubleshooting

- `403 architect bridge is disabled by configuration` -> `enabled` no es true, o falta `operatorPresent:true` en open.
- `exit 1 ARCHITECT_RUNTIME_COMMAND is required` -> no configuraste el inner (`ARCHITECT_RUNTIME_COMMAND`).
- segundo `open` devuelve el mismo `sessionId` -> correcto (sesion unica, reusa).
- el launcher no arranca un 2o -> correcto (lock de instancia unica); si quedo un lock huerfano, borrar el
  `ARCHITECT_RUNTIME_LOCK_PATH`.
- stream sin salida -> revisa que el inner emita por stdout line-buffered.
