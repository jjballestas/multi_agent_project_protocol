---
message_id: MSG-20260614-Claude-to-Codex-GO-TASK-0100-rescoped
type: HANDOFF
task_id: TASK-0100
from: Claude
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Tomas TASK-0100 (ready, rescoped opcion A / DECISION-0037) y la implementas, o blocked+pregunta concreta si una guarda se dispara?"
one_line_summary: FIN DEL HOLD. Opcion A ratificada (operador + concurrencia del analista). TASK-0100 reabierta a ready con alcance RESCOPED (DECISION-0037): .gitattributes para v1.2.0+, NO tocar v1.1.0 ni su firma; documentar v1.1.0 honestamente (616/127/14 + arbol sucio + protocol_replay irreproducible); verify_release fija/excluye v1.1.0 de la promesa LF. Implementa una sola; al cerrar yo+analista revisamos y promuevo TASK-0095.
requested_action: "Implementa TASK-0100 segun la seccion RESCOPE 2026-06-14 (DECISION-0037) del task .md (AUTORITATIVA, supersede el objetivo viejo): (1) anade .gitattributes raiz LF para releases futuros -- pre-condicion ya verificada: en HEAD `git add --renormalize .` solo stagea .gitattributes (0 cambios SBOM); GUARDA DURA intacta (si alterara bytes SBOM-included del HEAD -> BLOCKED+nota); (2) escribe la nota known-limitations de v1.1.0 EXPLICITA y NO eufemistica (clasificacion 616 LF/127 CRLF/14 no-EOL del artefacto del analista; manifest sobre arbol sucio = 14 deltas vs 04436c3; protocol_replay.py irreproducible desde refs; verify.integrity.json ok:true = local del emisor; corrige la premisa falsa de SPEC-0075 'ningun blob cambia'); (3) verify_release fija/excluye v1.1.0 de la promesa LF (garantia desde v1.2.0; un verify LF que falle en v1.1.0 es esperado y documentado, NO silenciar; SIN tocar el manifest firmado); (4) regresion de reproducibilidad sobre un release FUTURO (smoke) verde; cross-platform, .ps1 paridad, validador/neutralidad/encoding verdes, drift 0. NO re-firmar ni regenerar v1.1.0 (opcion B descartada). Escritor unico: adquiere tu claim, implementa, in_review + handoff con evidencia. Bump PATCH 1.9.1 lo aplico yo al cierre."
context_refs:
  - Area_comun/tasks/TASK-0100-codex-gitattributes-eol-lf.md
  - Area_comun/decisions/DECISION-0037-gitattributes-rescope-futuros.md
  - Area_comun/artifacts/ANALISTA-TASK-0100-decision-A-eol-rescope.md
  - Area_comun/specs/SPEC-0075-gitattributes-eol-lf-release-reproducible.md
---

# FIN DEL HOLD: TASK-0100 reabierta (rescoped, opcion A / DECISION-0037)

Codex:

Opcion A ratificada por el operador y concurrida por el analista (con ajustes de documentacion, ya
incorporados). **Sal del HOLD.** TASK-0100 vuelve a `ready` con alcance **rescoped** (DECISION-0037): el
objetivo viejo (verificar v1.1.0 bajo LF) queda superado -- v1.1.0 NO es reproducible (manifest sobre arbol
sucio + un fichero irrecuperable) y NO se toca su firma.

Lee la seccion **"RESCOPE 2026-06-14 (DECISION-0037) -- AUTORITATIVO"** del task .md: es la fuente de
verdad del alcance. Resumen en `requested_action`. Lo clave honesto: la nota de v1.1.0 debe llevar la
clasificacion real (616/127/14) y el defecto de arbol sucio + protocol_replay irreproducible, sin
eufemismos; corrige la premisa falsa de SPEC-0075.

Invariantes: escritor unico (submit_intent); NO re-firmar/regenerar v1.1.0; #4/chain-auth OFF,
SA.4/subagents/team_bridge OFF, #3 ON, compaction ON; NO re-armar SA.4; neutralidad; canal ASCII.

Flujo: tu implementas -> in_review + handoff con evidencia -> yo + analista revision adversarial -> cierro
a done con PATCH 1.9.1 + CHANGELOG -> recien promuevo 2/3 (TASK-0095). Una sola tarea a la vez. Si una
guarda se dispara, blocked + pregunta y paro el trio.
