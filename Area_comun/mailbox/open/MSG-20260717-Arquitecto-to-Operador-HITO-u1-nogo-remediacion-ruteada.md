---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-u1-nogo-remediacion-ruteada
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-HITO-u1-in-review.md
one_line_summary: "HITO U1: veredicto adversarial = CHANGE-REQUIRED con 3 BLOCKERs REALES (sink --db puede sobrescribir estado gobernado; PII de nomina escapa por validador regex de type -- la frontera dura de la instancia; hash de working-tree atribuido a HEAD, viola I8). Remediacion YA ruteada a Codex con criterios correctivos del checker + tests negativos por clave; loop acotado a 2 iteraciones, luego escalada a jball. El carril adversarial esta haciendo exactamente su trabajo."
---

# HITO - U1 NO-GO (3 BLOCKERs) -> remediacion en curso

- El Analista NO pudo romper: DDL 15 tablas, mapeo s.5.1b, I9 cero-inferencias, I6 identidad,
  clon limpio, gates felices (todo PASS con evidencia de exit-codes).
- SI rompio (probes conductuales propios, no los tests del maker):
  1. **F1 BLOCKER:** `--db` acepta cualquier ruta -> un fixture sobrescribio PROJECT_STATE.json
     con una DB SQLite. Fix: sink unico runtime/memory/index.db fail-closed + tests negativos CLI.
  2. **F2 BLOCKER (el grave):** `type` validado por regex, no enum -> salario+IBAN+nombre de
     empleado plantados en `type` llegaron a summary/search_terms/frontmatter_json. Rompe la
     frontera PII de nomina de la instancia. Fix: enum gobernado + gate PII por CADA clave
     allowlisted + tests negativos por clave.
  3. **F3 BLOCKER:** hash calculado del working tree pero atribuido a HEAD (viola I8). Fix: hash
     por blob git exacto o fallo cerrado + tests dirty-tree y golden CRLF.
- ACTION de remediacion a Codex (instancia `72f9d30`) con los criterios del checker verbatim;
  TASK-0001 sigue in_review, sin ratificar. Mismo finding-set vuelve al Analista para
  re-judgement independiente. Limite: 2 iteraciones; si la clase sobrevive, escalada a jball.
- Lectura de metodologia: los 3 escapes son clases que los tests del propio maker no cubrian
  (sink de salida, enum-vs-regex en PII, procedencia por blob) -- el checker adversarial con
  probes conductuales los cazo en el primer ciclo. Evidencia viva del valor del carril.

Sin accion tuya requerida. Proximo mail: re-entrega de Codex -> re-judgement -> GO/escalada.

-- Arquitecto. Hora local ~16:20 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
