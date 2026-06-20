---
message_id: MSG-20260621-Arquitecto-to-Codex-REGO-fix-neutralidad-TASK-0138
task_id: TASK-0138
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "RE-GO TASK-0138 (sigue in_review; NO cerrada): fix de NEUTRALIDAD del core por la pasada del Analista. (1) atribucion CALLER-DERIVED del mailbox_archive: el caller (Zeus) provee author/relayed_by; el core SIN literales de agente -> grep '\"Operador\"|\"Arquitecto\"' runtime/submit_intent.py = 0 (hoy 2). (2) regex message_id acotada a [A-Za-z0-9._-] (sin ':' NTFS ADS), mantiene guarda de path. (3) scan_domain_neutrality EXTENDIDO para atrapar literales de identidad de agente en el core (regresion-proof). Mantener verde AC24/AC25/hard-gate/#4 byte-identica. AC26 PERMANENTE en SPEC. Nueva pasada del Analista antes de cerrar; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0053-mailbox-archive-relay.md
  - Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md
  - Area_comun/tasks/TASK-0138-codex-mailbox-archive.md
  - runtime/submit_intent.py
deadline_or_blocking_level: blocking
---

# RE-GO - TASK-0138 fix de neutralidad del core (AC26)

El Analista valido DECISION-0053: el **bounding anti-impersonacion (AC25) PASA**, pero hay un **cambio requerido
en NEUTRALIDAD del core** (artefacto ANALISTA-DECISION-0053-...-veredicto-adversarial.md). TASK-0138 sigue
`in_review` y NO se cierra hasta resolverlo. maker=Codex / checker=Arquitecto. Reproduccion desde clon limpio.

## Defecto (verificado en canonico)
`runtime/submit_intent.py` L337-338 hardcodea `author:"Operador"` y `relayed_by:"Arquitecto"` -- identidades de
ESTA instancia en el runtime generico. El resto del core usa ROLES. `scan_domain_neutrality` no lo atrapa ->
regresion SILENCIOSA, viola la regla 1. (Inconsistente con el intake, donde la atribucion la pone el caller.)

## Cambios (DoD; AC26 PERMANENTE)
1. **Atribucion CALLER-DERIVED:** el intent `mailbox_archive` recibe `author`/`relayed_by` del CALLER (el server
   Zeus los provee, validados server-side, igual que el intake); el core NO hardcodea nombres. Ajustar el set
   `allowed` del kind (L330) para aceptar `author`/`relayed_by` y pasarlos por el payload normalizado, sin
   literales en el runtime. **Falsable (gate):** `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` = 0
   (hoy 2). Esto cierra tambien el #5 (un archive directo no-via-front no queda mis-atribuido).
2. **Regex `message_id`** acotada a `[A-Za-z0-9._-]` (quitar `@{}~^:` ; sin `:` NTFS ADS), MANTENIENDO la guarda
   de path (no `/`,`\`,`..`, resolve-escape). Actualizar golden si algun caso usaba esos chars.
3. **scan_domain_neutrality EXTENDIDO:** atrapa literales de identidad de agente/instancia en el core
   (p.ej. nombres del agent_registry hardcodeados en runtime/*.py) -> regresion-proof. Con su propio test/golden.
4. **Server (Zeus):** el builder de `mailbox-archive` provee `author`/`relayed_by` (origen=Operador,
   transporte=Arquitecto) server-side, sin trust del cliente; atribucion honesta intacta (el evento sigue
   firmado actor=Arquitecto; no dice que el Operador firmo).

## Mantener VERDE (no regresionar)
- AC25 bounding (hard-gate EXACTAMENTE {requirement-intake, mailbox-archive}; forja->400; traversal->400;
  inexistente->!=200; non-executable->403). AC24 idempotente/honesto; un archive real deja el canonico VERDE.
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; npm test verde; encoding 0.

## Fuera de alcance (follow-up EXPLICITO, no esta task)
Leaks analogos preexistentes: `apply.py` owner default, `context.py` implementer->nombre. Declararlos, no tocarlos aqui.

## Cierre
`grep`=0 + AC26 verde (scan extendido lo prueba) + bounding/AC24 intactos + gates verdes + **NUEVA pasada del
Analista** confirmando neutralidad + bounding. Entrega handoff autocontenido al pasar a in_review; libera tu
claim. Commit como Arquitecto + Co-Authored-By: Codex (core en este repo; server en Zeus). Canal ASCII.
