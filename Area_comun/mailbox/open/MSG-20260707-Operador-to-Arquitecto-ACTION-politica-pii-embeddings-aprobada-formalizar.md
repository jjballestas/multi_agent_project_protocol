---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-politica-pii-embeddings-aprobada-formalizar
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
one_line_summary: "El Operador APROBO la politica PII de embeddings de la memoria hibrida (F4). Formalizarla como enmienda de DECISION-1002 en el ledger de Aegis (llena el requisito ya nombrado 's.6: embeddings SOLO con politica PII explicita'). F4 avanza FTS-only; los embeddings quedan OPT-IN bajo esta politica."
requested_action: "Formalizar la politica PII de embeddings (6 puntos abajo, APROBADA por el Operador) como enmienda fechada de DECISION-1002 (o sub-decision) en el ledger de AEGIS -- llena el requisito s.6 'embeddings SOLO con politica PII explicita'. Confirmar que 1002 F4 procede FTS-ONLY y que los embeddings quedan OPT-IN detras de esta politica (no se activan hasta necesidad concreta). NO toca el hub ni el estudio medido."
question: "Confirmas la formalizacion de la politica como enmienda de DECISION-1002 en Aegis y que F4 sigue FTS-only con embeddings opt-in-bajo-politica?"
---

# ACTION - Politica PII de embeddings APROBADA -> formalizar en DECISION-1002 (Aegis)

El Operador aprobo la politica PII para los embeddings de la memoria hibrida (F4). Formalizala como enmienda
de DECISION-1002 en el ledger de Aegis (el requisito 's.6: embeddings SOLO con politica PII explicita' ya
existe; esto lo llena). F4 avanza FTS-only; los embeddings son OPT-IN bajo esta politica.

## Politica PII de embeddings (APROBADA, 6 puntos)
1. **Embeddings LOCAL-ONLY.** Se calculan con modelo local; el contenido NUNCA sale de la maquina.
   Prohibida cualquier API externa de embeddings.
2. **Clasificar antes de embeber.** Solo contenido clasificado no-PII/no-secreto (reusa 1002 s.4b: allowlist
   cerrada por valor; contenido libre atado por content_sha256 con redaction_state).
3. **Texto libre: DENY-BY-DEFAULT, no detect-and-scrub.** El texto libre no es embebible salvo (A) como
   resumen estructurado bajo esquema cerrado no-PII (el crudo queda en content_sha256, no embebido), o (B) con
   redaction_state=cleared por un HUMANO. Un pre-filtro regex determinista (cedula/NIT / email / telefono /
   cuenta financiera / secretos-API-keys / centinelas de dominio) BLOQUEA fail-closed cualquier match; pasar
   el regex NO auto-limpia. Ante duda, no se embebe. Se prueba con un golden test de PII plantada = 0 fugas.
   Limite declarado: la deteccion sobre texto libre es imperfecta -> por eso deny-by-default.
4. **Solo contenido de gobernanza/metodologia por ahora.** Metadata/gobernanza + resumenes neutrales SI;
   contenido de PRODUCTO con datos reales (Contabilidad/Budget/empleados) FUERA de alcance hasta una politica
   per-dominio + el hilo legal del consentimiento cerrado.
5. **Derivado, reconstruible, gitignored** (ya invariante): los embeddings viven en la DB derivada, nunca se
   commitean, se reconstruyen del origen.
6. **Chequeo falsable:** golden test con PII plantada (cedula/email/secreto/registro financiero falsos) que
   demuestra 0 fugas al embedder + test de que contenido sin clasificar/sin clear no se embebe.

## Frontera
FTS-only sigue siendo el default de F4; embeddings opt-in solo cuando haya necesidad concreta, siempre bajo
esta politica. No toca el estudio medido ni el genesis del hub. Enmienda en el ledger de Aegis.

-- Operador
