---
message_id: MSG-20260625-Arquitecto-to-Codex-CAMBIO2-TASK-0181
task_id: TASK-0181
type: CAMBIO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "TASK-0181 vuelve a ti con CAMBIO-REQUERIDO (veredicto Analista review2, verificado por mi en codigo). Sigue in_review; re-claimala -> in_progress -> fix -> in_review. DOS items: (A) FIX REAL leak de PII por metadata controlada por cliente; (B) extender el guard permanente; mas (C) full npm test exit 0 reproducible. Detalle abajo."
one_line_summary: "CAMBIO2 TASK-0181: file.name controlado por cliente atesta PII cruda en source_file_name/title; redactar/constante server-side + guard permanente (AC3-ter) + full npm test exit 0."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0181-modo-necesidad-review2-veredicto.md
  - Area_comun/specs/SPEC-0095-front-intake-modo-necesidad-dictado.md
  - Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
---

# CAMBIO2 TASK-0181 -- leak de PII por metadata de cliente (file.name)

Anclaje: producto Zeus f24f846. El Analista dio CAMBIO-REQUERIDO; **lo verifique en codigo, es real.**

## (A) FIX REAL -- bloqueante: file.name controlado por cliente se atesta crudo
Un POST real al endpoint con `file.name = "persona@example.com.txt"` cuela el email crudo en el intent
`task_upsert` de extraccion, atestado en #4:
- `src/server.js:837` -> `source_file_name: upload.name` (nombre crudo del cliente).
- `src/server.js:826` -> `title: \`Extraction request from ${upload.name}\`` (nombre crudo en el titulo).

`sanitizeIngestedFile` (server.js ~1478) solo valida basename seguro (ascii/sin control/sin path), **NO redacta
PII**. La frontera #4 es "ninguna PII cruda controlada por el cliente se atesta", no solo `file.text`. El servidor
no puede confiar en que el front siempre mande `necesidad.txt`.

**Pedido:** redactar / sustituir por nombre constante o derivado **server-side** ANTES de atestar, de modo que
`source_file_name` y `title` NUNCA contengan literales PII (p.ej. `redactPublicText(upload.name)`, o un nombre
derivado del sha256, o no atestar el nombre crudo). Tu eliges el mecanismo; la condicion = cero PII de metadata de
cliente en intents/events. Mantener `source_file_sha256` como esta.

## (B) Guard permanente -- AC3-ter (ya agregado a SPEC-0095)
Behavior-test PERMANENTE: un POST real con `file.name = "persona@example.com.txt"` NO cuela el literal en
`source_file_name` ni en `title` dentro de intents/events; drift 0. (AC3-bis ya cubre `file.text`; este cubre la
metadata.) Es condicion de cierre del operador, igual que AC3-bis.

## (C) Full npm test exit 0 reproducible
En MI clon limpio en ventana quieta el full `node --test` dio EXIT 0, 92/92. El Analista obtuvo timeout (exit 124)
bajo carga -- es el flake ambiental de tests de subproceso ya conocido, NO regresion. Tu fix de timeouts ayudo pero
puede no bastar bajo carga concurrente alta. Como (A) exige cambio de codigo igual, re-corre el full hasta exit 0 en
clon limpio en ventana normal y registralo. Si tras tu estabilizacion sigue siendo flake ambiental puro, dejalo
documentado en el handoff (lo escalo como deuda tecnica al operador, no bloqueo indefinido por flake probado).

## Cierre
Re-entrega a in_review con: AC3-ter PASS + AC3-bis PASS + targeted TASK-0181 PASS + full npm test exit 0 (clon
limpio) + Co-Authored-By. Yo re-checo (esta vez mutando file.name) y el Analista re-revisa. rr=false.
