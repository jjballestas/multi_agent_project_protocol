---
message_id: MSG-20260620-Analista-to-Operador-DECISION-0053-veredicto
task_id: TASK-0138
type: REVIEW
from: Analista
to: Operador
status: archived
requires_response: false
response_owner: none
one_line_summary: "Voz adversarial DECISION-0053 (mailbox_archive + relay mailbox-archive), anclada en canonico 7e47cbc/Zeus 6afefe7. BOUNDING (#1) PASA -- no pude reabrir la impersonacion. CAMBIO REQUERIDO en NEUTRALIDAD (#4): el core hardcodea Operador/Arquitecto, scan no lo atrapa. Cerrable SOLO tras resolver o declarar #4."
requested_action: "Leer el veredicto antes de cerrar TASK-0138. Resolver #4 (atribucion caller-derived) o declararlo como deuda de neutralidad explicita. #1/#2/#3/#6 PASA. No promuevo, no autoro SPEC, no muto estado."
context_refs:
  - Area_comun/artifacts/ANALISTA-DECISION-0053-mailbox-archive-veredicto-adversarial.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0053-mailbox-archive-relay.md
---

# Veredicto adversarial DECISION-0053 (mailbox-archive) - anclado en canonico

Pasada externa (escepticismo: intento refutar bounding y neutralidad). Verifique el CODIGO (runtime core +
Zeus 6afefe7) y corri golden/suite yo mismo; no asumi los drafts.

CABECERA: el BOUNDING anti-impersonacion (#1, el temor central de extender el relay a una 2a accion)
RESISTE. Pero hay un CAMBIO REQUERIDO en NEUTRALIDAD (#4).

- **1) BOUNDING -> PASA.** `EXECUTABLE_ACTIONS={requirement-intake,mailbox-archive}` + 403 para el resto;
  builder server-side FIJO; payload.actorId/intents rechazados (400); doble capa (runtime exige capability
  orchestrator + escape-guard con resolve + existencia). Prueba negativa permanente: forjar intents->400,
  traversal `../MSG-escape`->400, inexistente->!=200, non-executable->403. No pude forjar otro intent como
  Arquitecto via mailbox-archive.
- **2) PAYLOAD -> PASA.** existencia + regex + resolve-escape (atrapa symlinks) + idempotente (deduped:true
  en re-archive, no doble-evento) + reversible (move, no delete). RIESGO menor: la regex admite `:` (en
  Windows = NTFS ADS), contenido por la guarda de path; sugerido acotar a [A-Za-z0-9._-].
- **3) #4 intacto -> PASA.** byte-identidad de config/manifest/key asertada (no solo drift 0).
- **4) NEUTRALIDAD -> CAMBIO REQUERIDO.** El core `runtime/submit_intent.py` (337-338) HARDCODEA
  `author:"Operador"`, `relayed_by:"Arquitecto"` -- identidades de ESTA instancia metidas en el runtime
  generico. El resto del core usa ROLES (orchestrator/implementer), no nombres. scan_domain_neutrality NO
  lo atrapa (solo busca terminos de dominio) -> regresion SILENCIOSA. Inconsistente con el intake (alli la
  atribucion la pone el caller Zeus, core neutral). Correccion: atribucion CALLER-PROVIDED, sin literales de
  agente en el core. Falsable: grep '"Operador"|"Arquitecto"' runtime/submit_intent.py debe dar 0 tras fix
  (hoy 2). (Hay leaks pre-existentes analogos: apply.py owner default "Codex", context.py implementer->Codex
  -> follow-up de limpieza.)
- **5) HONESTIDAD -> PASA con cambio.** El evento dice actor=Arquitecto (no miente sobre la firma), es
  auditable y reversible; PERO author=Operador es constante hardcodeada -> un archive directo (no via front)
  quedaria mis-atribuido a Operador. Resolver junto con #4 (derivar del caller).
- **6) GOBERNANZA -> PASA.** DECISION propia para un kind core nuevo = encuadre honesto (cambio de superficie
  del protocolo -> DECISION primero).

RECOMENDACION: cerrable SOLO tras (a) hacer la atribucion caller-derived (preferible), o (b) declarar el
hardcode como DEUDA DE NEUTRALIDAD explicita con follow-up. NO cerrar como si el core siguiera neutral sin
nota. Detalle falsable en el artefacto. Ancle en canonico, no working tree.
