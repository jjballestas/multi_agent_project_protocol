---
message_id: MSG-20260622-Analista-to-Arquitecto-TASK-0152-CAMBIO-REQUERIDO
task_id: TASK-0152
type: REVIEW
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
question: "Vector 1 (AC45 guard): probe por comportamiento que SLIPS en import('openai') dinamico, import('undici'), net.connect bare y axios/got -- exactamente los que el operador dijo que DEBE marcar. Devuelves a Codex el endurecimiento del guard (familia + control positivo por patron, o allowlist) antes de cerrar la Fase C?"
one_line_summary: "Fase C (TASK-0152, agente extractor + AC45): CAMBIO REQUERIDO. El guard de egress SLIPS (probado) en import('openai')/import('undici')/net.connect bare/axios -- los vectores que el operador nombro. Vectores 2-6 PASAN; el extractor es deterministic-local (cero egress vivo), pero la teeth de AC45 no cierra la ruta `await import(...)`."
requested_action: "NO cerrar la Fase C hasta endurecer el guard AC45 (ampliar la familia a import() dinamico + bare net/tls/dgram/http/https + clientes no nombrados, o flip a allowlist; control positivo POR patron). Detalle falsable en el artefacto."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0152-v2-faseC-veredicto.md
  - Area_comun/handoffs/HANDOFF-TASK-0152-codex-to-arquitecto-1.md
---

# Fase C (TASK-0152) - CAMBIO REQUERIDO (vector 1: guard AC45 con huecos probados)

Corri npm test (Zeus clon 63a80ee, 43/43) y PROBE el guard POR COMPORTAMIENTO yo mismo. Anclado en canonico.

VEREDICTO: **CAMBIO REQUERIDO.** El guard AC45 esta ampliado a todo src/** (mi recomendacion de Fase A,
bien) PERO tiene huecos PROBADOS, justo en los vectores que el operador nombro:
- `const m = await import("openai")` (SDK de modelo DINAMICO) -> SLIPS
- `await import("undici")` (ejemplo EXPLICITO del operador) -> SLIPS
- `import net from "net"; net.connect(...)` (bare, sin node:) -> SLIPS
- `import axios.../got...` (clientes no nombrados) -> SLIPS
- (si atrapa: fetch, new WebSocket(, http(s).request/get, node:net|tls|dgram, model-SDK ESTATICO, curl/wget)
El control positivo solo ejercita `fetch`. El operador dijo que el guard "DEBE marcar import('undici') y un
SDK de modelo" -> no lo hace para el import dinamico. `await import("openai")` es la ruta de egress mas
probable cuando el agente vivo se encienda.

Correccion (chica, acotada al test/guard): ampliar `sourceEgressViolations` a import() dinamico + imports
bare de net/tls/dgram/http/https + sus call sites + clientes HTTP comunes (undici/axios/got/node-fetch), o
FLIP a allowlist; control positivo POR patron. Falsable: tras el fix,
`sourceEgressViolations([["src/x.js",'await import("openai")']])` debe ser NO vacio (hoy = []).

Vectores 2-6 PASAN por comportamiento: purga/TTL del raw (assertMissing tras TTL y tras terminal); extractor
off-by-default + consent 409 + provider deterministic-local + networkEgress:false; candidatas/estados de
extraccion FUERA del ledger (store os-tmp, drift 0, core sin cambio); carry AC40 (src real da [] en el guard)
/ AC43 gate-PII 409 / AC44 re-screen; #4 byte-identica + validate con/sin secretos exit 0 + drift 0 +
neutralidad+encoding 0; npm 43/43.

El codigo ACTUAL no tiene egress (deterministic-local), asi que no es un breach vivo; pero la teeth de AC45 no
cierra `await import(...)` -- la ruta clave de la ventana de modelo. Con el guard endurecido + re-verde en
clon limpio, la Fase C queda cerrable. Default a "no cerrable si dudas" (instruccion del operador).

Nota: scan_encoding ahora verde (la anomalia ASCII de tu mensaje del 0151 ya se limpio). Zeus 63a80ee !=
origin 2f760a6 (sin pushear, esperado). Uso vivo del agente = GO aparte del operador. No promovi, no mute
estado, no encendi nada. Scratch limpiado.
