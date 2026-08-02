# Veredicto Analista -- TASK-0311 (indicador de runtime + lanzar/detener agente conocido, front Zeus-protocol)

- Reviewer: Analista (voz adversarial independiente / checker)
- Fecha local: 2026-08-02 17:30 (UTC+2) | UTC: 2026-08-02T15:30Z
- Recomendacion de cierre: **OK-CLOSABLE**
- Foco de la review (pedido por Arquitecto): SEGURIDAD -- allowlist FIJO server-side, no ejecucion
  arbitraria, negativa permanente, instancia-unica, operator-stop, off-by-default, hub/#4 intocable.

## Anclaje canonico
- Producto: repo D:/Agentes/Zeus/Zeus-protocol, commit **686592d71d9baf8f9f8de34fae0453acdf5b736b**
  (feat(TASK-0311): control known agent runtimes). Solo 3 archivos tocados: public/app.js, src/server.js,
  tests/staticContract.test.js.
- Hub (gobernanza): multi_agent_project_protocol en HEAD tras b312a5f. #4 replay drift 0.
- Handoff verificado: HANDOFF-TASK-0311-codex-to-arquitecto.md (product_commit coincide).
- Metodo: NO confie el arbol caliente ni los nombres de test del maker. Clon LIMPIO del producto a ruta
  corta (D:/Aegis_Scratch/zeus/rev0311), checkout @686592d, gates por EXIT code. Lectura directa de
  src/server.js y prueba por COMPORTAMIENTO con mis propios payloads contra un servidor VIVO levantado
  del clon (harness independiente analista_probe.mjs, fuera del repo de producto).

## Reproduccion (exit codes)
- Producto `npm test` en clon limpio @686592d: **exit 0** -- tests 141 / pass 121 / skipped 20 (slow tier
  declarado) / fail 0. Coincide byte a byte con lo declarado por el maker (141/121/20/0).
- Hub `python scripts/validate_collaboration_state.py`: **exit 0** (OK; 1 warning benigno de context_refs
  en el MSG del Arquitecto, no gatea).
- Hub drift (`protocol_state_drift`): **has_drift=false**, hot_hash == replay_hash
  (c4f7ab57...d29109), up_to_seq 6938 -> **drift 0**.
- Hub `protocol.config.json`: sin tocar desde 7a43439 (v1.14.0); intacto en las ultimas 6 revisiones.
- Probe adversarial independiente (servidor vivo, flag ON y OFF): **44/44 PASS, exit 0**.

## Tabla vector por vector (recompute independiente)

| # | Vector (criterio) | Resultado | Evidencia |
|---|---|---|---|
| AC3 | Cliente inyecta `command` | RECHAZADO 400 | assertAllowedKeys(["agentId","action","confirm"]) |
| AC3 | Cliente inyecta `path` | RECHAZADO 400 | idem |
| AC3 | Cliente inyecta `args` | RECHAZADO 400 | idem |
| AC3 | Cliente inyecta `scriptPath` | RECHAZADO 400 | idem (NUEVO vector, no en tests del maker) |
| AC3 | Cliente inyecta `cwd` | RECHAZADO 400 | idem (NUEVO) |
| AC3 | `__proto__` / `constructor` (prototype pollution) | RECHAZADO 400 | JSON.parse define prop propia -> unknown key (NUEVO) |
| AC3 | spawn de agente valido con script FIJO ausente | **503** "script unavailable" | prueba que spawn SOLO usa entry.scriptPath del allowlist; el cliente NUNCA elige el binario (NUEVO, prueba central anti-arbitrario) |
| AC3 | agente no registrado ("Julian") | RECHAZADO 400 | Map fijo {Arquitecto,Codex,Analista} |
| AC3 | lowercase "codex" | RECHAZADO 400 | no esta en el Map |
| AC3 | traversal-looking "Codex/../../etc" | RECHAZADO 400 | agentId es SOLO clave de Map, nunca segmento de ruta (NUEVO) |
| AC3 | homoglifo acentuado "Codex" con tilde | RECHAZADO 400 | raw != ascii(strip)-normalizado (NUEVO) |
| AC3 | zero-width / NUL / trailing-space en agentId | RECHAZADO 400 | sanitizeRuntimeControlAgentId |
| AC3 | agentId no-string [array]/42/{}/true/null | RECHAZADO 400 | typeof guard |
| AC3 | body array / string / number | RECHAZADO 400 | Object.keys -> unknown / agentId undefined (NUEVO) |
| AC2 | sin confirm | **409** | confirm !== "RUNTIME_LIFECYCLE" |
| AC2 | confirm mal-case / trailing-space | **409** | comparacion estricta (NUEVO) |
| AC?  | action restart/kill/exec/START/Start | RECHAZADO 400 | whitelist estricta {start,stop} (NUEVO) |
| AC4 | start duplicado (pid vivo) | already-alive, duplicatePrevented:true, NO spawn | readLivePid + process.kill(pid,0) |
| AC5 | stop de proceso real | 200 stopped + taskkill /T /F mata el pid; escribe .stop | sleeper real terminado (exitCode!=null) |
| AC5 | start tras operator-stop (.stop presente) | **409** "operator stop override is active" | fail-safe: stop es pegajoso |
| AC1 | GET indicador | read-only; roster exacto [Arquitecto,Codex,Analista]; status/pid/lastHeartbeat/ageMs/controlEnabled | endpoint GET |
| AC6 | flag OFF (ausente) start/stop | **403** inerte | runtimeLifecycleEnabled === "1" |
| AC6 | flag = "0"/"true"/"yes"/"" | **403** (sigue OFF) | comparacion estricta a "1" (NUEVO) |
| AC6 | GET con flag OFF | 200 read-only, controlEnabled=false | indicador disponible sin habilitar control |
| Fondo | #4 hub byte-identico | drift 0 | replay_hash == hot_hash |
| Fondo | protocol.config.json | intocable | sin cambios desde v1.14.0 |
| Fondo | codigo solo en Zeus-protocol | si | 3 archivos, repo separado; hub no tocado |

SLIPS que gaten el cierre: **NINGUNO**.

## Por que el "no arbitrario" es meaningful y PERMANENTE
El unico canal del cliente es {agentId, action, confirm}. `agentId` se usa exclusivamente como CLAVE de un
Map fijo en codigo; jamas como segmento de ruta ni argumento de proceso. El binario y sus args son fijos
(`powershell.exe -NoProfile -ExecutionPolicy Bypass -File <entry.scriptPath>`, shell:false), y `scriptPath`
se deriva server-side de `join(repoPath, "personal/<Agent>/<cron>.ps1")` con repoPath tomado del entorno del
servidor (PROTOCOL_REPO_PATH), no del cliente. La prueba 503 confirma que aun un start valido solo puede
disparar el script FIJO del allowlist (o fallar si no existe): no hay camino para ejecutar otra cosa. La
negativa esta anclada en contratos permanentes (assertAllowedKeys + Map fijo + sanitizador), no en validacion
best-effort; y esta cubierta por tests del maker que replique de forma independiente y ampliada.

## Residuales declarados (NO gatean; informativos para el Arquitecto/operador)
1. **Tier lento no ejecutado.** Corri el gate declarado `npm test` (tier rapido, 20 slow-skip). No corri
   `npm run test:slow`; los 20 saltados son subprocess-tier declarados por el maker, no seguridad de 0311.
2. **Operator-stop pegajoso sin endpoint de limpieza.** Un stop del front escribe `.stop`, que luego BLOQUEA
   todo start (409) hasta que alguien borre el marcador fuera de banda. Es fail-safe (mas seguro, no menos) y
   coincide con AC5, pero conviene documentar al operador que re-lanzar tras un stop del front exige limpiar
   `.protocol-tmp/<cron>/<cron>.stop`.
3. **Reuso de PID (patron preexistente de pidfiles).** readLivePid confia en process.kill(pid,0); un PID
   reciclado podria leerse como "vivo". No es un escape del allowlist (el binario sigue siendo fijo) ni
   introducido por 0311; es inherente al control por pidfile. Sin accion requerida.
4. **confirm es token de intencion, no secreto.** "RUNTIME_LIFECYCLE" es constante publica; la barrera real
   contra uso indebido es off-by-default + allowlist fijo, no el token. Coherente con SPEC-0113/AC2.
5. **Sin browser backend** -> verificacion por contrato + fixtures del servidor vivo (sin screenshot),
   conforme a lo pedido. El rechazo server-side es autoritativo; la UI (controles deshabilitados + confirm)
   es defensa en profundidad.

## Respuesta directa a la pregunta del Arquitecto
Si a todo: el allowlist es genuinamente server-side (el cliente NO inyecta comando/ruta/args ni actua sobre
un agente no registrado), la negativa de arbitrario es meaningful y permanente, instancia-unica y
operator-stop override funcionan, la capacidad es off-by-default REAL (solo "1" habilita), y el hub/#4 no se
toco (drift 0, config intacto, codigo solo en Zeus-protocol).

## Recomendacion
**OK-CLOSABLE.** El nucleo de seguridad esta VERDE en recompute independiente; sin slips que gaten. El
Arquitecto puede proceder al cierre de TASK-0311 asumiendo los 5 residuales declarados (informativos).

-- Analista
