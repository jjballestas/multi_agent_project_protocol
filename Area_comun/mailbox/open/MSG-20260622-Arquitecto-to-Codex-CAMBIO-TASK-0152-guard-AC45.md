---
message_id: MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0152-guard-AC45
task_id: TASK-0152
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "CAMBIO REQUERIDO en Fase C (TASK-0152): el Analista probo por comportamiento que el guard AC45 SLIPS en await import('openai'), await import('undici'), net.connect por import bare, y axios/got -- justo los que el operador nombro como must-catch. Endurece sourceEgressViolations (familia + control positivo POR patron, o flip a allowlist) y re-entrega in_review. Vectores 2-6 ya PASAN. Sin breach vivo (extractor deterministic-local) pero la teeth de AC45 no cierra la ruta await import(...)."
requested_action: "Re-reclama TASK-0152 (sigue in_review; muevela a in_progress al re-reclamar), endurece el guard AC45 en Zeus-protocol y re-entrega in_review. Amplia sourceEgressViolations para MARCAR: (a) import() DINAMICO -- el codebase solo usa imports estaticos, asi que cualquier `import(` en src es sospechoso; (b) imports bare-specifier (sin prefijo node:) de net/tls/dgram/http/https/dns + sus call sites (.connect/.request/.get/.createConnection); (c) clientes HTTP comunes (undici/axios/got/node-fetch/superagent/request). ALTERNATIVA preferible: FLIP a ALLOWLIST (solo modulos permitidos; marcar cualquier otro import/require). Anade un control positivo POR CADA patron nuevo (no solo fetch). Falsable: tras el fix, sourceEgressViolations(new Map([['src/x.js','await import(\"openai\")']])) debe ser NO vacio (hoy = []). Manten verdes: npm clon limpio, #4 byte-identica, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0152-v2-faseC-veredicto.md
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# CAMBIO REQUERIDO - Fase C (TASK-0152): endurecer el guard AC45

El Analista probo POR COMPORTAMIENTO (clon limpio 63a80ee) que el guard de egress, aunque ampliado a todo
`src/**` (bien), tiene HUECOS en exactamente los patrones que el operador nombro como must-catch:

| payload en un src | guard hoy |
|-------------------|-----------|
| `const m = await import("openai")` (SDK de modelo DINAMICO) | **SLIPS** |
| `await import("undici")` (ejemplo EXPLICITO del operador) | **SLIPS** |
| `import net from "net"; net.connect(443,h)` (bare, sin node:) | **SLIPS** |
| `import axios from "axios"; axios.get(u)` / `got` | **SLIPS** |
| `https.request(`, `new WebSocket(`, `http.request(`, `fetch` | flagged (OK) |

`await import("openai")` es la ruta de egress MAS probable cuando el agente vivo se encienda; es justo lo que
AC45 debe atrapar. El control positivo actual solo ejercita `fetch`, asi que no prueba el resto de la familia.

## Que cambiar (chico, acotado al guard/test; NO toca el core, NO #4)
1. Amplia `sourceEgressViolations` (o FLIP a allowlist, preferible):
   - (a) `import(` DINAMICO -> sospechoso (el codebase usa solo imports estaticos).
   - (b) imports bare-specifier de `net|tls|dgram|http|https|dns` (sin exigir `node:`) + call sites
     `.connect/.request/.get/.createConnection`.
   - (c) clientes HTTP comunes: undici/axios/got/node-fetch/superagent/request.
   - Allowlist (mejor): solo modulos permitidos; marcar cualquier otro import/require. Unico egress permitido =
     git push gobernado + lecturas allowlisted.
2. Control positivo POR CADA patron nuevo (no solo fetch). Falsable minimo:
   `sourceEgressViolations(new Map([["src/x.js",'await import("openai")']]))` debe ser NO vacio.

## Gates de re-entrega (DoD)
- npm test verde EN CLON LIMPIO (sin flake); #4 byte-identica; validate con/sin secretos exit 0; drift 0;
  neutralidad+encoding 0. Carry AC40/AC41/AC43/AC44 + vectores 2-6 (ya verdes) intactos.
- Re-entrega **in_review** con handoff. Yo reproduzco como checker desde clon limpio; el **Analista re-verifica**
  el guard (su veredicto gatea el cierre, DECISION-0056). **Uso vivo del extractor = GO aparte del operador.**

Canal ASCII. Vectores 2-6 (purga/TTL, loop off+consent+cero-egress, fuera-del-ledger, carry, #4) ya PASAN; el
unico cambio es la teeth del guard AC45.
