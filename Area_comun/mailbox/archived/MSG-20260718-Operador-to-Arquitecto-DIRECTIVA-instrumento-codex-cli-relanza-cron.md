---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-instrumento-codex-cli-relanza-cron
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-smoke-peon-qwen7b-verde.md
one_line_summary: "El operador elige el CODEX CLI como instrumento del probe A-vs-B (absolutos comparables), NO el worker-revivido. Relanza el cron de Codex. ADVERTENCIA: el classifier del harness te DENEGO antes lanzar el implementer (permitio Analista, no Codex); si te vuelve a bloquear NO lo rodees, REPORTA -> el operador corre la linea manual o autoriza la regla. HOLD la mecanica A-vs-B hasta que el Codex CLI viva; la prep (TASK + lote + sorteo) si puede avanzar."
requested_action: "[DIRECTIVA] Instrumento del probe = Codex CLI (no worker-revivido). Intenta relanzar el cron de Codex (peer_mailbox_cron -PeerId Codex). Si el classifier lo DENIEGA (como antes), NO lo rodees: reporta de inmediato y el operador corre la linea manual (opcion a) o autoriza la regla (opcion b). Puedes dejar registrada la TASK del probe + el lote de 20 claves + el sorteo de mitades; pero HOLD la medicion A-vs-B hasta que el Codex CLI este vivo."
question: "Confirmas: intentas el relanzamiento del cron Codex y reportas si el classifier bloquea (para que el operador actue)?"
---

# DIRECTIVA - Instrumento del probe = Codex CLI; relanza su cron (y reporta si el classifier bloquea)

El operador elige el **Codex CLI** como maker-instrumento del A-vs-B (quiere absolutos comparables),
no el worker-revivido. Relanza el cron de Codex de Nova-Payroll.

## Advertencia (el bloqueo conocido)
Relanzar el cron IMPLEMENTER (Codex) es justo lo que el classifier del harness te DENEGO antes
(permitio el Analista/reviewer, bloqueo el Codex/implementer -> el operador tuvo que correr la
linea manual). Eso NO ha cambiado: DECISION-0101 movio el CHECKER de proveedor, no la regla de
permiso del implementer-launch. Asi que es probable que te vuelva a bloquear.

- Si el classifier DENIEGA: **NO lo rodees.** Reporta de inmediato -> el operador corre la linea
  manual (opcion a) o autoriza la regla de permiso (opcion b). Es su linea, no la tuya.
- Si por lo que sea SI te deja lanzarlo: adelante, y sigue con la mecanica.

## Mientras tanto
Puedes dejar lista la PREP: registrar la TASK gobernada del probe en Nova-Payroll + el lote de 20
claves + el sorteo documentado de las 2 mitades. Pero **HOLD la medicion A-vs-B** hasta que el
Codex CLI este vivo (el operador quiere ESE instrumento, no el revivido).

## Guardrails
Demo NO citable (anti-HARKing); PII de nomina fuera del probe; fondo intocable (2E35F26E / 1.14.0 /
N=500); DECISION-0099 (spec del maker al peon como artefacto); checker fuerte.

-- Operador (via Asesor).
