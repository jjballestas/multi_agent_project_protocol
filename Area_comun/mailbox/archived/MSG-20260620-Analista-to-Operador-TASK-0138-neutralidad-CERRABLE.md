---
message_id: MSG-20260620-Analista-to-Operador-TASK-0138-neutralidad-CERRABLE
task_id: TASK-0138
type: REVIEW
from: Analista
to: Operador
status: archived
requires_response: false
response_owner: none
one_line_summary: "Pasada FINAL adversarial del fix de neutralidad (AC26) de TASK-0138, anclada en 8317878/Zeus 7619fd2. CERRABLE: no pude refutar (a) core neutral ni (b) bounding intacto. Mi CAMBIO #4 resuelto y hecho regresion-proof por un scan REAL (lo probe inyectando un literal)."
requested_action: "Mi veredicto FINAL: CERRABLE. Tomarlo para el cierre de TASK-0138 (checker Arquitecto). Detalle falsable en el artefacto. No promuevo, no autoro SPEC, no muto estado."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0138-neutralidad-AC26-veredicto-final.md
  - Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md
---

# Pasada FINAL - fix de neutralidad TASK-0138 (AC26) - CERRABLE

Voz adversarial final (intento refutar core-neutral y bounding-intacto). Verifique el CODIGO y corri
scan/golden/suite yo mismo; anclado en canonico 8317878 / Zeus 7619fd2.

- **1) NEUTRALIDAD -> PASA.** `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` = **0** (antes 2).
  La atribucion es CALLER-DERIVED: el core toma author/relayed_by con `require_text` (obligatorios del
  caller, sin default a Operador); los literales viven ahora en el SERVER de Zeus (commit 7619fd2) = el
  producto, no el core. #5 cerrado: un archive directo (no-via-front) NO se auto-mis-atribuye a Operador
  (el caller debe proveer su atribucion).
- **2) SCAN REGRESION-PROOF -> PASA (probado, no cosmetico).** Inyecte `"Operador"` en una copia de
  submit_intent.py y corri el scan -> **exit 1**, lo flagueo (`runtime/submit_intent.py: operador`). En
  limpio: exit 0. submit_intent.py NO esta en la whitelist legacy -> queda vigilado. Fixture
  identity_literal_in_core existe. La deuda legacy (apply.py "Codex", etc.) quedo DECLARADA en una whitelist
  nombrada (honesto), no silenciosa.
- **3) BOUNDING -> PASA (sin regresion).** EXECUTABLE_ACTIONS={requirement-intake,mailbox-archive}+403;
  payload.actorId/intents->400; builder server-side fijo; idempotente deduped; npm test 26/26 (incl
  impersonacion forjada->400, traversal->400, write real). El fix solo movio la FUENTE de la atribucion, no
  abrio superficie.
- **4) GATES -> PASA.** regex acotada `^MSG-[A-Za-z0-9._-]+$` (sin `:` ADS; `..` sigue rechazado); #4
  byte-identica (config/manifest/key); validate exit 0 CON y SIN secretos; drift 0; npm verde.

RECOMENDACION: **CERRABLE.** Ambos ejes resisten. Mi CAMBIO previo no solo se resolvio sino que quedo
regresion-proof por un scan real. Unica nota no bloqueante: la whitelist legacy es deuda de neutralidad
declarada (follow-up opcional). Cierre formal = Arquitecto (checker) + tu visto. No promovi, no mute estado,
ancle en canonico, scratch limpiado.
