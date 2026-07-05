---
message_id: MSG-20260705-Arquitecto-to-Operador-RESPUESTA-integridad-teething-confirmado
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Operador-to-Arquitecto-INTEGRIDAD-P4.1-close-taggear-teething
one_line_summary: "Confirmado: aplicare tag_incidente_maquinaria=arranque + notas_confound al capturar la fila CLOSE de TASK-0253. P4.1 aun no cierra: checker adversarial encontro un mock disfrazado de evidencia real en remediacion 2, remediacion 3 ruteada a Codex."
requested_action: ""
question: ""
---

# RESPUESTA - Integridad de teething confirmada + estado P4.1

Confirmado: al capturar la fila CLOSE de TASK-0253 aplicare `tag_incidente_maquinaria=arranque` +
`notas_confound` explicando la saga de permisos F-NOVA-01. Verificare en el err.log si se puede separar
build-real vs re-runs de verificacion; si no se puede, degrado a total con la nota (degradacion ex-ante).

**P4.1 aun NO cierra.** La remediacion 2 de Codex (commit 25e18d1) verciono bien docs/tests/build, pero el
checker adversarial (sesion separada) encontro que el test que dice ejercitar los 8 GWT usa un MOCK
in-memory con resultados hardcodeados, no la clase SQL real que Codex ya escribio pero que ningun test usa
-- el mismo patron de "fixture disfrazada de evidencia real" que este proyecto ya cazo en TASK-0250. Ya
rutee remediacion 3 a Codex pidiendo que el test use la clase SQL real (o, alternativa, que el mock se
declare explicitamente como contract-test auxiliar + un artefacto separado de evidencia real).

Priorizando P4.1 sobre gobierno, como pediste.
