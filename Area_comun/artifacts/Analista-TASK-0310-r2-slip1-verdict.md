# VEREDICTO Analista -- TASK-0310 r2 (remediacion SLIP-1, consola prompt operador->agente)

- Reviewer: Analista (voz adversarial / checker independiente)
- Fecha/hora local: 2026-08-02 16:11 (UTC+2)
- Iteracion: 2/2 (re-review tras la remediacion de SLIP-1 que yo exigi en r1)
- Maker: Codex. Gobernanza: DECISION-0106 (accepted) + SPEC-0112.
- Recomendacion de cierre: **OK-CERRABLE (OK-CLOSABLE)**

## Anclas canonicas (no arbol caliente)
- Repo de producto: D:/Agentes/Zeus/Zeus-protocol -- commit **826be23** (== origin/main HEAD; padre 767f41f verificado).
- Hub (gobernanza): HEAD **42d9bcd**; epoch protocol_version 1.14.0; config sha256 2e35f26e (PINEADO, sin tocar); drift 0.
- Clon limpio del producto: file-clone a D:/Aegis_Scratch/z310, checkout 826be23, arbol limpio.
- Metodo de UI: SIN navegador (confirmado). Verificacion por contrato + fixtures del endpoint + drive directo del validador del hub (metodo autorizado, igual que r1 y 0309).

## Reproduccion (exit codes)
| Gate | Comando | Exit | Resultado |
|------|---------|------|-----------|
| Producto npm test (clon limpio @826be23) | `node --test` | 0 | 140 total / 118 pass / 22 skip / 0 fail |
| Tests TASK-0310 (impersonacion + off-by-default) | `node --test -tnp="TASK-0310"` | 0 | 2/2 pass |
| Hub validate | `python scripts/validate_collaboration_state.py` | 0 | OK collaboration state is valid |
| Hub encoding scan | `python scripts/scan_encoding.py` | 0 | clean |
| Hub neutrality scan | `python scripts/scan_domain_neutrality.py` | 0 | clean |
| Hub drift | `protocol_state_drift(root)` | 0 | has_drift=False |
| Hub config integridad | sha256(protocol.config.json) | -- | 2e35f26e (pineado; sin cambios desde 7a43439) |

## SLIP-1: CERRADO (verificado de forma independiente)
El fix (diff 767f41f..826be23, 6 lineas de src) confina el cambio a `buildMailboxSendMarkdown`: para
requires_response:true ahora emite INCONDICIONALMENTE `response_owner:` + `requested_action:` + `question:`
(antes emitia solo uno u otro segun messageType). El resto de src/server.js no se toca.

Recompute independiente (NO confie en el nombre del test): reconstrui la salida EXACTA de
`buildMailboxSendMarkdown` para las versiones VIEJA (767f41f) y NUEVA (826be23) y pase las 4 combinaciones
{REQUEST,QUESTION} x {requires_response input true,false} por la FUNCION `validate_mailbox` del hub (HEAD 42d9bcd),
en aislamiento, en Area_comun/mailbox/open/. Nota: `sanitizeAgentPrompt` fuerza requires_response=true cuando
messageType=QUESTION, asi que 3 de las 4 combinaciones son requires_response:true internamente.

Resultado (drive directo del validador):
- **NUEVA (826be23): 0 errores** en las 4 combinaciones.
- **VIEJA (767f41f): 3 errores** -- QUESTION/true y QUESTION/false(forzado true) fallan por
  "requires response but has no requested_action"; REQUEST/true falla por "compact ... has no question";
  REQUEST/false pasa (requires_response:false, sin contrato). Coincide byte a byte con el SLIP-1 de r1.

## Test 4-combos: MEANINGFUL (falla sin el fix)
Superpuse SOLO el test nuevo (tests/staticContract.test.js de 826be23) sobre el src VIEJO (767f41f) en clon limpio
y corri el test: **FALLA** (AssertionError; el MSG QUESTION no lleva `requested_action`). Con el src nuevo: PASA.
Ademas, mi drive directo del validador (arriba) confirma que el hueco se cierra en la CAPA DEL VALIDADOR real,
no solo en el regex del test. El hueco de cobertura de r1 (slow test env-guarded, skipped) queda convertido en
teeth por un test RAPIDO sin secretos que ejerce las 4 combinaciones contra el validador -- exactamente lo que
exigi en el bucle de fix.

## Tabla vector-por-vector
| AC / Vector | Recompute independiente | Veredicto |
|-------------|--------------------------|-----------|
| AC4 (SLIP-1) el MSG requires_response:true pasa validate_mailbox | drive directo: NUEVA 0 err / VIEJA 3 err en las 4 combos | PASS |
| Test 4-combos meaningful | test nuevo sobre src viejo -> FALLA; sobre src nuevo -> PASA | PASS |
| Anti-impersonacion (nucleo) | test "rejects impersonation" PASS @826be23: cliente from/actor/relayed_by, raw fields, destino ajeno, execute-sin-confirm(409) todos rechazados (400/409) | PASS (sin regresion) |
| Destino restringido | agentId fuera de {Arquitecto,Codex,Analista} -> 400 (sanitizeAgentPrompt:1125, sin tocar) | PASS |
| Atribucion pineada server-side | from=Operador, relayed_by=Arquitecto, endorsement=none hardcode server-side (sin tocar) | PASS |
| Off-by-default | test "inert while product flag is off" PASS @826be23: dry_run -> 403; capabilities.operatorPrompt.enabled=false | PASS |
| Fondo intocable (#4) | drift 0; config byte-identico (2e35f26e); codigo SOLO en Zeus-protocol | PASS |
| Alcance del diff | src: solo buildMailboxSendMarkdown (6 lineas); + test. Sin cambios en las guardas de seguridad | PASS |

## Busqueda de escape (adversarial)
- No hay camino que emita `requires_response: true` sin AMBOS campos: `responseFields` es incondicionalmente
  [response_owner, requested_action, question] cuando `requiresResponse` es truthy; en caso contrario, vacio.
- No hay inyeccion YAML: el prompt pasa por ascii+stripControl+redactPublicText y va como `JSON.stringify(prompt)`
  (una sola linea escapada) en el frontmatter; el cuerpo va tras el fence `---`. Ningun campo se puede forjar.
- Prompt vacio: rechazado antes (400) en sanitizeAgentPrompt; response_owner=agentId (whitelist) siempre \S+.

## Residuales declarados (no bloqueantes)
- R1: `question:` == `requested_action:` (ambos = JSON.stringify(prompt)). Para un REQUEST, un campo `question:`
  es semanticamente redundante, pero es la forma que el contrato compact del validador exige para requires_response
  y el validador solo comprueba presencia. Satisface el contrato; no es defecto.
- R2 (coupling de test, no de producto): el test 4-combos depende del hub via `PROTOCOL_REPO_PATH`
  (default D:/Agentes/multi_agent_project_protocol) y hace shell-out a `python`. Es teeth valido en este entorno;
  para CI portable conviene documentar la dependencia (hub presente + python en PATH). No bloquea el cierre.
- R3 (persiste de r1): path EXECUTE completo (submit_intent real + auto-commit-push) no reproducible en clon limpio
  por secretos event_auth fuera del repo; verificado el compose (dry_run == execute byte a byte), guardas
  confirm(409)/off-by-default(403), y la validez del MSG por la funcion del validador. El SLIP-1 no depende de esos secretos.
- R4: UI sin veredicto visual (sin navegador); wiring verificado por staticContract (test PASS).

## Cierre del bucle de fix (r1 -> r2)
El fix aplicado coincide EXACTAMENTE con la remediacion que prescribi en r1 (emitir ambos campos + test rapido de
4 combos contra el validador). SLIP-1 cerrado, test meaningful, nucleo de seguridad intacto, fondo #4 intocado.
Iteracion 2/2 consumida SIN nuevo slip. Recomiendo cierre.

-- Analista
