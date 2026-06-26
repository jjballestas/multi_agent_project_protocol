---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0189
task_id: TASK-0189
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0189 (remediacion consola del Arquitecto, ready, priority high). Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = Zeus-protocol. Corrige 2 defectos hallados en el smoke vivo: (1) AUDIT timestamp corrupto -- el redactor PII se aplica a campos estructurales y se come la fecha (`timestamp` queda `[PHONE-REDACTED]T..Z`); fix: redactar SOLO texto libre (text/contenido), NUNCA timestamp/sessionId/kind/stream. (2) CLEANUP no robusto del launcher -- tras el cese de la sesion o muerte del parent, el lock persiste y quedan procesos huerfanos (el cleanup solo corre en cierre por stdin); fix: el launcher remueve lock + termina el inner ante SIGTERM y stdin-close, y el cese del puente termina al launcher disparando su cleanup (SIGTERM/graceful, kill duro solo tras timeout), sin inner huerfano ni lock stale, de modo que un open POSTERIOR vuelva a arrancar. DoD = SPEC-0102 AC1-AC5. Correr test:ci en ventana quieta. NO tocar protocol.config.json/genesis/#4. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0189: remediacion consola Arquitecto (audit redacta solo texto libre + cleanup robusto del launcher: lock+inner en SIGTERM/cese)."
context_refs:
  - Area_comun/specs/SPEC-0102-consola-arquitecto-remediacion-audit-cleanup.md
  - Area_comun/tasks/TASK-0189-codex-consola-arquitecto-remediacion.md
  - Area_comun/decisions/DECISION-0062-consola-arquitecto-puente-interactivo.md
---

# GO -- TASK-0189 (remediacion: audit timestamp + cleanup del launcher)

Hallazgos del smoke vivo de la consola. Repo = **Zeus-protocol**. Anclaje: SPEC-0102 AC1-AC5. priority high.

Corregir:
- **(1) Audit timestamp corrupto:** el redactor PII se aplica a campos estructurales y muerde la fecha
  (`"timestamp":"[PHONE-REDACTED]T20:37:..Z"`). Fix: redactar **solo texto libre** (text/contenido del mensaje y la
  salida); **NUNCA** `timestamp`/`sessionId`/`kind`/`stream`. AC1: el timestamp queda ISO valido y el texto sigue
  redactado por familias.
- **(2) Cleanup no robusto del launcher:** tras el cese de la sesion o muerte del parent, el **lock persiste** +
  procesos **huerfanos** (cleanup solo en cierre por stdin). Fix: el launcher remueve lock + termina el inner ante
  **SIGTERM** y stdin-close; el cese del puente termina al launcher disparando su cleanup (SIGTERM/graceful, kill
  duro solo tras timeout), sin inner huerfano ni lock stale, de modo que **un open POSTERIOR vuelva a arrancar**.

Sin regresion de invariantes (no-bypass, identidad existente, off-by-default, instancia unica, redaccion del
contenido). Gates: gate rapido verde + test:ci en **VENTANA QUIETA** 100% pass; protocolo validate exit 0 (con/sin
secretos), drift 0, encoding/neutralidad exit 0; config pinned/genesis intactos; Co-Authored-By. Entrega a
in_review; yo re-checo clon limpio (`git -c core.longpaths=true`) repitiendo el smoke. rr=false.
