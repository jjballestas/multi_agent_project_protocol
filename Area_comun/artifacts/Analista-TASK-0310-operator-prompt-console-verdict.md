# VEREDICTO Analista -- TASK-0310 (consola de prompt operador->agente, front Zeus-protocol)

- Reviewer: Analista (voz adversarial / checker independiente)
- Fecha/hora local: 2026-08-02 15:30 (UTC+2)
- Tarea: TASK-0310 -- consola de prompt operador->agente (Alcance A de TASK-0178)
- Maker: Codex. Gobernanza: DECISION-0106 (accepted) + SPEC-0112.
- Recomendacion de cierre: **CAMBIO-REQUERIDO (CHANGE-REQUIRED)**

## Anclas canonicas (no arbol caliente)
- Repo de producto: D:/Agentes/Zeus/Zeus-protocol -- commit **767f41f** (== origin/main HEAD; ancestro verificado).
- Hub (gobernanza): HEAD **d7ce511**; epoch protocol_version 1.14.0; config sha256 2e35f26e (PINEADO); drift 0.
- Clon limpio del producto: file-clone a D:/Aegis_Scratch/zp0310, checkout 767f41f, arbol limpio.
- Metodo de UI: SIN navegador en el entorno (confirmado). Render NO verificado por screenshot; verificacion por
  contrato + fixtures del endpoint vivo + negativa de impersonacion (metodo autorizado, igual que 0309).

## Reproduccion (exit codes)
| Gate | Comando | Exit | Resultado |
|------|---------|------|-----------|
| Producto npm test (clon limpio @767f41f) | `node --test` | 0 | 140 total / 118 pass / 22 skip / 0 fail |
| Producto slow (test bajo revision) | `ZEUS_RUN_SLOW_TESTS=1 node --test -tnp="mailbox_send execute writes validator-valid operator directive"` | 0 | **SKIPPED**: "protocol fixture with event_auth secrets is unavailable" |
| node --check src/server.js / public/app.js | (implicito en suite) | 0 | ok |
| Hub validate | `python scripts/validate_collaboration_state.py` | 0 | OK collaboration state is valid (baseline sano) |
| Hub validate (clon limpio @d7ce511) | idem en D:/Aegis_Scratch/hub0310 | 0 | baseline verde (replay ~3 min) |
| Hub encoding scan | `python scripts/scan_encoding.py` | 0 | clean |
| Hub neutrality scan | `python scripts/scan_domain_neutrality.py` | 0 | clean |
| Hub drift | `protocol_replay.protocol_state_drift` | 0 | has_drift=false; hot==replay; up_to_seq 6897 |
| Hub config integridad | sha256(protocol.config.json) | -- | 2e35f26e (pineado, sin tocar por commits de review) |

Probe adversarial independiente (servidor vivo, dry_run; hub NO mutado -- md5 de git status identico antes/despues):
`node adv_probe.mjs` -> **27/27 PASS**. Cuatro instancias de servidor (enabled+ready, relay-mismatch, persistencia-off, disabled).

## Tabla vector-por-vector (foco SEGURIDAD)
| AC / Vector | Recompute independiente | Veredicto |
|-------------|--------------------------|-----------|
| AC3 builder server-side (assertAllowedKeys top-level = 5 datos; sub-agentPrompt = 5) | from/actor/relayed_by/endorsement/author/actorId/intents cliente RECHAZADOS (400) tanto top-level como dentro de agentPrompt | PASS |
| AC3 destino restringido | agentId fuera de {Arquitecto,Codex,Analista} -> 400; "Operador"/"codex"(minus)/"Extractor" -> 400 | PASS |
| AC3 forma acotada | messageType DIRECTIVE(antiguo)/GO -> 400 (solo REQUEST/QUESTION); actionId ajeno -> 400 | PASS |
| AC3 anti-YAML-injection (NUEVO vector) | prompt con "\n---\nfrom: Codex\n..." -> stripControl aplana a 1 linea dentro de requested_action; from sigue Operador; un solo from/relayed_by; sin frontmatter inyectado | PASS |
| AC3 atribucion pineada server-side | from=Operador, relayed_by=Arquitecto (hardcode action.relayedBy), endorsement=none; el cliente no puede alterarlas | PASS |
| AC3 relay-actor fail-safe (NUEVO) | config relayActor != action.relayedBy -> 500 (no emite mensaje con relay forjado) | PASS |
| AC4 redaccion PII server-side (NUEVO: ataque directo saltando el cliente) | email/NIT/SELECT/dbo enviados crudos al endpoint -> [EMAIL/NIT/SQL-REF-REDACTED]; 0 fugas | PASS |
| AC7 off-by-default | flag off -> dry_run 403 y execute 403; capabilities.operatorPrompt.enabled=false; defensa en profundidad (endpoint + buildMailboxSendIntents) | PASS |
| Gate persistencia | enabled pero autoCommitPush off + execute -> 503; dry_run sigue 200 | PASS |
| Gate confirm | execute sin confirm -> 409 | PASS |
| Fondo intocable (#4) | drift 0; config byte-identico; codigo SOLO en Zeus-protocol | PASS |
| **AC4 el MSG compuesto pasa validate_collaboration_state** | **FALLA para requires_response:true** (ver SLIP-1) | **SLIP** |

## SLIP-1 (CONFIRMED, falsable) -- el MSG compuesto RED-linea el validador cuando requires_response:true
El corazon de la funcion es escribir mensajes gobernados VALIDOS. AC4 exige "El MSG compuesto pasa
validate_collaboration_state". Recompute: extraje el MSG real que produce el endpoint (dry_run, byte a byte igual
al que execute escribe -- src/server.js:1103-1116 escribe `buildMailboxSendMarkdown(...)` sin post-proceso) y lo
pase por la FUNCION del validador `validate_mailbox` del HEAD citado (d7ce511), en aislamiento, con la ruta
Area_comun/mailbox/open/.

Resultado (3 variantes generadas por el endpoint vivo):
- **QUESTION + requires_response:true** -> FAIL: "Mailbox message requires response but has no requested_action"
  (validator linea 1188: exige el substring `requested_action` en TODO mensaje open con requires_response:true).
  El MSG solo emite `question:` (buildMailboxSendMarkdown: `messageType==="QUESTION" ? "question" : "requested_action"`).
- **REQUEST + requires_response:true** -> FAIL: "Compact mailbox message requires response but has no question"
  (validator linea 1193: todo mensaje "compact" -- y todos lo son porque siempre llevan `one_line_summary` --
  con requires_response:true exige tambien `question`). El MSG solo emite `requested_action:`.
- REQUEST + requires_response:false -> PASS (unica variante valida; sin contrato de respuesta).

Camino real desde la UI (public/app.js:1276): casilla "requires response" marcada -> QUESTION + requires_response:true
-> **FALLA**; desmarcada -> REQUEST + requires_response:false -> pasa. Es decir, la ruta "pedir respuesta al agente"
(el proposito central de la consola) produce un mensaje que deja el estado canonico ROJO al escribirse via execute,
bajo modo runtime-authoritative/enforce.

Por que la evidencia del maker no lo cazo: el unico test que corre validate sobre un MSG QUESTION real
(`mailbox_send execute writes validator-valid operator directive`) esta **SKIPPED** (env-guarded: faltan los
secretos event_auth del fixture) tanto en mi clon como en el reporte del maker (19 skips en test:slow). La
propiedad "validator-valid" de AC4 nunca fue ejercida por un test que corriera. El hueco de cobertura coincide
exactamente con el defecto.

Impacto y alcance honesto: la capacidad es off-by-default e INERTE tal como se entrega, asi que el hub NO esta
hoy en riesgo. El defecto se manifiesta cuando el operador ACTIVA la consola y envia un prompt con respuesta
requerida. El nucleo de SEGURIDAD (foco primario de la review: anti-impersonacion, off-by-default, atribucion
honesta, redaccion) esta SOLIDO; lo que falla es la validez protocolar del mensaje compuesto (AC4).

## Residuales declarados (no bloqueantes)
- R1: `pii_guard.redactions` es un flag binario (0/1), no un conteo (server: `original===publicPrompt ? 0 : 1`).
  Con multiples familias PII redactadas sigue reportando 1. Honesto ("hubo redaccion") pero subestima la cuenta.
  Cosmetico; la redaccion real si se aplica. Mismo patron que el intake existente.
- R2: El path EXECUTE completo (escritura real via submit_intent + validate + auto-commit-push) no se pudo
  reproducir en clon limpio por falta de los secretos event_auth (fuera del repo). Verifique el compose (dry_run,
  identico byte a byte al de execute), las guardas confirm(409)/persistencia(503), y la validez del MSG via la
  funcion del validador en aislamiento. El SLIP-1 no depende de esos secretos.
- R3: UI sin veredicto visual (sin navegador); wiring verificado por staticContract (buildAgentPromptPayload,
  "Preview dry_run", window.confirm, buildAgentThread) -- test PASS.

## Bucle de fix esperado (CHANGE-REQUIRED)
- Remediacion (maker=Codex): en `buildMailboxSendMarkdown`, para requires_response:true emitir AMBOS campos
  `requested_action:` Y `question:` (ambos con el prompt), de modo que se satisfagan la linea 1188 (requested_action
  incondicional) y la 1193 (question para compact). Como todo MSG lleva `one_line_summary` (siempre compact), ambos
  campos son necesarios en la ruta requires_response.
- Cobertura: convertir el hueco en teeth -- un test RAPIDO (sin secretos) que pase la salida de
  `buildMailboxSendMarkdown` por `validate_mailbox` para las 4 combinaciones {REQUEST,QUESTION} x
  {requires_response true,false} y exija 0 errores. (No basta con dejar el slow test skipped.)
- Gates afectados: scripts/validate_collaboration_state.py (validate_mailbox); staticContract del producto.
- Re-juicio (Analista): re-correr la funcion validate_mailbox sobre las 4 variantes + npm test clon limpio; exigir
  exit 0 y 0 errores del validador. Maximo 2 iteraciones antes de escalar al operador humano.

-- Analista
