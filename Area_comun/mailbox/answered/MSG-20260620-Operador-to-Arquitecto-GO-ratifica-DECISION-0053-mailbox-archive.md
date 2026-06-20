---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-ratifica-DECISION-0053-mailbox-archive
task_id: TASK-0138
type: DECISION
from: Operador
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
one_line_summary: "RATIFICO el #3 (REQ-B65E7802 mailbox-archive) como DECISION-0053 PROPIA (no prosa en 0052), porque introduce un intent kind nuevo en el escritor-unico (regla 2 = decision auditable). Promueve DECISION-0053 -> SPEC-0086-ext5 (AC24/AC25) -> GO TASK-0138 a Codex. CONDICION DE CIERRE: hard-gate admite EXACTAMENTE {requirement-intake, mailbox-archive}; AC25 anti-impersonacion (prueba negativa permanente) verde; AC24 archive idempotente/honesto; un archive deja el canonico VERDE; #4 byte-identica; y PASADA DEL ANALISTA validando el bounding ANTES de cerrar (esta decision debe ser validada). Antes de promover: pushea los drafts (hoy estan sin commitear en tu working tree)."
requested_action: "Estoy de acuerdo: DECISION-0053 propia. Antes de promover, COMMITEA+PUSHEA tus 3 drafts (hoy en personal/Arquitecto/carril_A/ sin pushear: DRAFT-DECISION-0053-mailbox-archive-relay, DRAFT-SPEC-0086-ext5-mailbox-archive, DRAFT-TASK-0138-mailbox-archive) para que sean canonicos y verificables. Luego promueve en orden: (1) DECISION-0053 (nuevo intent kind core `mailbox_archive`, aditivo + neutral; payload estricto: mensaje existe en open/ + ruta dentro de mailbox/ sin path-traversal; idempotente; NO toca config/genesis/keys); (2) SPEC-0086-ext5 (AC24 archive gobernado idempotente y honesto + AC25 anti-impersonacion prueba negativa permanente); (3) GO TASK-0138 a Codex (maker; core en este repo + front/server en Zeus; tu checker). CONDICIONES DE CIERRE (innegociables): (a) el hard-gate 403 admite EXACTAMENTE {requirement-intake, mailbox-archive} y cualquier otra forma sigue 403 -- test permanente; (b) AC25 verde: id inexistente / fuera de open/ / path-traversal / usar mailbox-archive para emitir CUALQUIER otro intent -> RECHAZADO; (c) builder SERVER-SIDE, nunca confiar en payload.actorId/intents; (d) AC24: archive idempotente (re-archivar = no-op), atribucion honesta (relayed_by=Arquitecto/origen=Operador, nada que diga que el Operador firmo), reversible/auditable; (e) un archive REAL deja el canonico VERDE (regresion-proof, como AC22); (f) #4 byte-identica (config/manifest/keys sin cambio), validate con/sin secretos exit 0, drift 0, npm test verde, neutralidad/encoding 0; (g) **PASADA DEL ANALISTA validando el bounding + neutralidad del nuevo kind ANTES de cerrar** (yo activo al Analista con un prompt aparte). maker=Codex/checker=Arquitecto, reproduccion desde clon limpio. Reporta drafts/cierre en canonico. Tras cerrar, sigue con el #4 (auto commit+push, que va con su DECISION por transporte/credenciales)."
question: none
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0053-mailbox-archive-relay.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext5-mailbox-archive.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0138-mailbox-archive.md
  - Area_comun/tasks/req-b65e7802-requirement-seed.md
deadline_or_blocking_level: normal
---

# GO - ratifico el #3 (mailbox-archive) como DECISION-0053 propia

De acuerdo con tu recomendacion: **DECISION-0053 propia**, no prosa en 0052. Un intent kind nuevo en el
escritor-unico es cambio de superficie del protocolo (regla 2) y merece su rastro auditable.

**Antes de promover:** commitea+pushea tus 3 drafts (estan sin commitear en tu working tree; hoy no son
canonicos). Luego promueve: DECISION-0053 -> SPEC-0086-ext5 -> GO TASK-0138 a Codex.

**Condiciones de cierre (innegociables):**
- Hard-gate admite **EXACTAMENTE** {requirement-intake, mailbox-archive}; el resto sigue 403 (test permanente).
- **AC25** anti-impersonacion verde: id inexistente / fuera de open/ / path-traversal / otro-intent-via-
  mailbox-archive -> RECHAZADO. Builder server-side, nunca confiar en el cliente.
- **AC24**: archive idempotente, atribucion honesta (relayed_by=Arquitecto, nada de "Operador firmo"),
  auditable.
- Un archive real deja el canonico **VERDE** (regresion-proof); #4 byte-identica; validate con/sin secretos
  exit 0; drift 0; neutralidad limpia (el kind es maquinaria generica, sin dominio en el core).
- **PASADA DEL ANALISTA validando el bounding + neutralidad ANTES de cerrar.**

Verifico tu cierre en canonico. Canal ASCII.
