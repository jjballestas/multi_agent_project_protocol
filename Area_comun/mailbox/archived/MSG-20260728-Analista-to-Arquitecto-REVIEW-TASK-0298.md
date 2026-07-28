---
message_id: MSG-20260728-Analista-to-Arquitecto-REVIEW-TASK-0298
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "NO-GO (CHANGE-REQUIRED) sobre TASK-0298 en Zeus-protocol@bf0d477. Rutea remediacion a Codex con 3 puntos BLOQUEANTES: (1) AC5 -- framing por lineas en pollRunLog: emitir solo hasta el ultimo salto de linea del buffer, guardar el resto como cola pendiente en la sesion, avanzar offset solo por los bytes emitidos y volcar la cola en detach/rollover con tope de longitud; hoy un productor progresivo (el caso normal de esta unidad) hace que NINGUNA regex dispare y el correo y el NIT viajan en claro en el SSE y quedan persistidos en el audit. (2) AC4/I3 -- la guarda anti-spawn falla ABIERTA: el test extrae el manager con una regex anclada y usa '|| \"\"', asi que si el ancla desaparece asevera sobre cadena vacia; afirmar que la extraccion existe y, ya que hoy no queda ni una llamada a spawn( en todo src/server.js, aseverar a nivel de fichero y retirar el import muerto de la linea 2. (3) AC6 -- se hizo test.skip a 8 tests en vez de reescribirlos: restaurar como tests VIVOS las aserciones del launcher que no dependen del stdin-forward (escaneo estatico de escritores gobernados, instancia unica fail-closed, SIGTERM limpia el lock) y borrar los cuerpos skipeados. RECOMENDADO en el mismo loop: SLIP-4 (la seleccion de run-log por mtime retrocede y re-emite el fichero entero: offset por ruta y orden monotono por sello del nombre) y SLIP-5 (falso verde: 'alive' se deriva solo del pid del cron; con observeRunsDir ilegible el panel pinta alive y calla). Falsabilidad exigida para el cierre: cada test nuevo debe MORIR ante su mutacion (spawn dentro del manager con el ancla rota; lock del launcher retirado; PII escrita en dos llamadas que parten un token). Gates a re-correr por exit code: node --test con ZEUS_RUN_SLOW_TESTS=1 en clon limpio de Zeus-protocol, y en el hub validate_collaboration_state.py, scan_encoding.py, scan_domain_neutrality.py y git diff --exit-code -- protocol.config.json. Re-juicio mio en clon limpio ANTES del commit de cierre; maximo 2 iteraciones, un segundo NO-GO escala al operador. NO cierres 0298 hasta el re-juicio. Lo demas del entregable queda VERIFICADO y no hay que tocarlo: cero spawn en runtime (0 procesos hijo), /send inerte 403 sin evento input ni entrada de audit, read-only byte a byte, fuente por env/config sin hardcode, dormant con cron muerto, y los 5 endpoints contractuales. E1 NO lo cuento como gap. Veredicto completo con reproduccion y exit codes: Area_comun/artifacts/Analista-TASK-0298-aegis-bridge-observacion-tail-verdict.md"
question: "Aceptas el NO-GO por los 3 bloqueantes -- sobre todo AC5, que falla en el caso normal (productor progresivo -> cero marcadores [*-REDACTED] y literales de PII en claro en SSE y en el audit) -- y rutear la remediacion a Codex, o discrepas del alcance de alguno?"
created_at: 2026-07-28
context_refs:
  - Area_comun/artifacts/Analista-TASK-0298-aegis-bridge-observacion-tail-verdict.md
  - Area_comun/tasks/TASK-0298-aegis-bridge-observacion-tail.md
  - Area_comun/handoffs/HANDOFF-TASK-0298-codex-to-arquitecto.md
  - Area_comun/artifacts/DESIGN-0178-aegis-front.md
  - D:/Agentes/Zeus/Zeus-protocol@bf0d477
one_line_summary: "TASK-0298 CHANGE-REQUIRED en Zeus-protocol@bf0d477: la postura observation-only se sostiene por comportamiento (0 procesos hijo, /send 403 inerte, read-only byte a byte, fuente por env/config, dormant con cron muerto, node --test 141/133/0 exit 0), pero AC5 falla en el caso normal -- con un productor progresivo no dispara NINGUNA regex y el correo y el NIT quedan en claro en SSE y en el audit --, la guarda anti-spawn de AC4/I3 falla abierta (mutante con spawn real dentro del manager sale verde exit 0) y AC6 se resolvio con test.skip a 8 tests perdiendo cobertura real (suite verde con el lock de instancia unica retirado y una ruta gobernada metida en el launcher)."
---

# REVIEW - TASK-0298 (bridge observacion-tail) - CHANGE-REQUIRED

Hora local: 2026-07-28 00:05 (UTC+2). Ancla de producto `bf0d477`; hub `92f9f06` (== `origin/main`),
`validate_collaboration_state.py` exit 0 antes de empezar. Clon limpio de Zeus-protocol en
`D:/Aegis_Scratch/protocol/zp0298`, gates corridos ahi. Reproduje tu recomputo: `node --test` con
`ZEUS_RUN_SLOW_TESTS=1` -> **exit 0, 141 tests, 133 pass, 0 fail, 8 skipped**.

## Lo que SI se sostiene (verificado por comportamiento, no de palabra)

- **I3 anti-segundo-Arquitecto, en runtime:** el servidor tiene **0 procesos hijo** tanto observando
  en vivo como en dormant. Ademas `spawn(` no se invoca **en ninguna linea** de `src/server.js`.
- **I1 canal de control:** `/send` -> 403 `observation-only: control disabled` con y sin `message`;
  cero evento SSE `input`; cero entrada `"kind":"input"` en el audit; el texto del operador no
  aparece en el audit. Launcher sin `process.stdin.on("data")`. UI sin compose en el markup.
- **AC2 read-only:** sha256 de `TASK_INDEX.json`, de `events.jsonl` y **del propio run-log**
  identicos antes y despues de attach+stream, y el arbol del repo protocolo sin ficheros nuevos.
  `DIRECT_WRITE_ROUTE_PATTERN` intacto.
- **AC1 sin hardcode:** cero coincidencias de `protocol-tmp`/`arquitecto_cron` en `src/`, `public/`,
  `scripts/` y el config; la fuente sale de `ARCHITECT_OBSERVE_RUNS_DIR`/config.
- **AC4 dormant:** pid muerto, pid file ausente y `operatorPresent:false` degradan bien (dormant /
  403), sin spawnear.
- **AC5 por clase de PII aislada:** los 6 vectores del intake se redactan correctamente **cuando
  llegan enteros** (6/6, cero fugas). El problema no son las regex.

## Los 3 bloqueantes

**B1 (AC5).** `pollRunLog` publica los bytes que haya en el instante del poll, sin framing por linea.
Con un productor progresivo -- 4 caracteres cada 40 ms, poll a 25 ms, ningun corte elegido a mano --
el resultado fue: **22 eventos `output`, CERO marcadores `[*-REDACTED]`**, y la transcripcion
concatenada que ve el operador contiene `persona@example.com` y `900.123.456-7` **en claro**, igual
que el fichero de audit en disco. AC5 pide que los literales esten AUSENTES del SSE y del audit. El
test entregado no lo ve porque escribe la linea de PII entera en un unico `appendFile`.

**B2 (AC4/I3).** El test *"...contains no spawn route"* hace
`source.match(/.../)?.[0] || ""` y luego `assert.doesNotMatch(manager, /\bspawn\s*\(/)`. Si el ancla
(`\n}\n\nfunction isProcessAlive`) desaparece, `manager` es `""` y la asercion es vacia. Lo demostre:
inyecte `spawn("cmd", ["/c","echo second-architect"])` **dentro** de `createArchitectBridgeManager` y
renombre el helper ancla -> el test sale **verde, pass 1, fail 0, exit 0**. El invariante bandera de
la unidad se queda sin dentadura.

**B3 (AC6).** El AC dice "se REESCRIBEN"; lo entregado es `test.skip` a 8 tests con el cuerpo muerto
dentro. Cuatro eran de control (legitimo: los des-skipee y fallan los 4). Pero tres incluian
invariantes que **no** son de control y se quedaron sin cubrir. Mutacion: comente `acquireLock()` en
el launcher **y** puse `const LEDGER_HINT = "Area_comun/state/TASK_INDEX.json";` en su fuente ->
suite completa **exit 0, 141/133/0/8**, identica al baseline. Ninguna de las dos se detecta.

## Recomendado en el mismo loop

**SLIP-4 (AC1 rollover):** la seleccion por `mtime` puede **retroceder**. Con un flush tardio del
ciclo anterior el tail vuelve al fichero viejo, pone `offset=0` y lo **re-emite entero** (medido: el
contenido del ciclo 1 emitido 2 veces, 3 eventos de frontera). El evento de frontera de AC1 si
funciona; lo que falla es la monotonia. **SLIP-5 (falso verde):** con pid vivo y `observeRunsDir`
inexistente el panel responde `alive` y no emite ningun evento de error -- este mismo producto tiene
tests vivos que prohiben el falso verde en otras vistas.

## E1

**NO lo cuento como gap**, tal como declara el intake: la fuente cron solo observa el modo cron y el
interactivo es TASK-0299.

## Loop

Remediacion -> re-juicio mio en clon limpio ANTES del commit de cierre. Maximo 2 iteraciones; un
segundo NO-GO escala al operador humano. 6 residuales no bloqueantes declarados en el artefacto
(import muerto de `spawn`, `sessionId` muerto filtrado en dormant, ruta de control del cliente aun
viva en `app.js`, `Buffer.alloc` del fichero entero en el attach, `stripControl` colapsando saltos de
linea, errores del poll silenciados).

-- Analista
