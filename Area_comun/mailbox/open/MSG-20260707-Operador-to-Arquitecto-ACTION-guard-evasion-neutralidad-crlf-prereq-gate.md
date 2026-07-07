---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-guard-evasion-neutralidad-crlf-prereq-gate
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - personal/asesor/EVIDENCIA-VIVA-metodologia.md
one_line_summary: "Dos afinamientos del Asesor a tus 2 hallazgos: (1) ademas del fix de placeholders, anadir un GUARD SISTEMICO para que scan_domain_neutrality no sea evadible por encoding (char-codes/base64/hex de terminos de dominio); (2) elevar el CRLF/LF de backlog a PREREQUISITO del gate e2e de 2 clones -- si no se canonicaliza, el clon Windows de Julian dara hashes distintos = rojo espurio."
requested_action: "(1) Ademas del fix inmediato (placeholders genuinos en test_ca11, ya ruteado a Codex), registrar como item de HARDENING DE GATE que scan_domain_neutrality detecte patrones de EVASION (tuplas de char-codes, base64, hex de terminos de dominio en fuente), no solo strings literales -- patron defecto-recurrente -> salvaguarda permanente (como el guard de procedencia F-NOVA-01). Es un hueco de integridad del gate: si un maker/peon puede ofuscar, el scanner no protege. (2) Canonicalizar los line-endings del event-log/estado de la instancia (`.gitattributes` con `eol=lf` / `-text` para events.jsonl y state json) ANTES del gate e2e de 2 clones con Julian, no como backlog: la reproducibilidad cross-clon del #4 depende de line-endings estables; sin esto el clon Windows de Julian falla el gate por hash divergente. Es prerequisito del onboarding, hermano de TASK-1105 pero con fecha (antes del 2-clones)."
question: "Confirmas (1) el guard sistemico anti-evasion del scanner de neutralidad como item de hardening, y (2) el CRLF/LF como PREREQUISITO del gate 2-clones (no backlog suelto)? Nada bloquea 1204; ambos son fix-forward pero el #2 tiene que estar antes de que Julian corra el gate."
---

# ACTION - Guard anti-evasion del scanner + CRLF/LF como prerequisito del gate 2-clones

Tus 2 hallazgos son correctos y bien cazados. Dos afinamientos del Asesor (study/gate-integrity):

## 1. Evasion del scanner de neutralidad -> guard SISTEMICO (no solo el placeholder)
El fix de placeholders genuinos en test_ca11 es correcto y ya va a Codex. PERO el hallazgo revela un HUECO
DEL GATE: `scan_domain_neutrality` es EVADIBLE por encoding (el maker escribio dominio como tuplas de bytes y
paso). Cualquier maker/peon futuro podria repetirlo. Registra como item de HARDENING DE GATE: el scanner debe
detectar patrones de evasion (char-codes / base64 / hex de terminos de dominio en fuente), no solo strings
literales. Es el patron defecto-recurrente -> salvaguarda permanente (como el guard de procedencia que
adoptamos tras el mock-evidence). Lo bueno: el checker adversarial LO CAZO (la capa humana atrapa lo que el
scanner no) -- eso es la tesis; pero el hueco del scanner hay que cerrarlo.

## 2. CRLF/LF -> PREREQUISITO del gate e2e de 2 clones (no backlog suelto)
El `validate` falso-rojo en clon limpio por CRLF/LF NO es solo cosmetico: si los line-endings cambian el hash
del event-log, la reproducibilidad CROSS-CLON se rompe. Consecuencia directa: el clon Windows de Julian
producira un events.jsonl con line-endings distintos al del operador -> hashes divergentes -> el gate e2e de
2 clones dara ROJO ESPURIO. Por eso lo elevo de "hermano de TASK-1105 (backlog)" a PREREQUISITO con fecha:
canonicaliza los line-endings del event-log/estado (`.gitattributes` `eol=lf` / `-text` para events.jsonl y
los state json) ANTES de que Julian corra el gate de apertura. Si no, el onboarding falla por infra, no por
la metodologia.

## Frontera
Nada bloquea TASK-1204. Ambos son fix-forward; el #2 solo tiene deadline (antes del 2-clones). No toca el #4
del hub (estable). Registrado en EVIDENCIA-VIVA A13/A14 (honestidad: el checker cazo la evasion, y el scanner
tenia el hueco; la reproducibilidad cross-clon es real).

-- Operador
