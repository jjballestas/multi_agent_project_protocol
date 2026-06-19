---
message_id: MSG-20260619-Operador-to-Arquitecto-fix-ruta-diseno-spec0086
type: CHANGES
task_id: TASK-0124
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: T0 verificado OK (SPEC-0086 accepted, TASK-0124 ready, 44 eventos firmados, #4 intacto). PERO los insumos de diseno se movieron por decision del operador a D:\Agentes\Zeus\Zeus-protocol\design\ (el diseno de Claude Design vive en Zeus-protocol\design\interface). SPEC-0086 referencia la ruta VIEJA (Zeus\design). Corregir las refs antes de que Codex implemente TASK-0124.
requested_action: "Corregir (via update gobernado de la SPEC, esta atestada) las rutas de insumo de SPEC-0086: D:\\Agentes\\Zeus\\design\\... -> D:\\Agentes\\Zeus\\Zeus-protocol\\design\\... (front_requirements.html, front_pipeline.html, y el diseno UI en Zeus-protocol\\design\\interface\\). Asegurar que TASK-0124 / el GO a Codex apunten a la ruta nueva. Repo producto confirmado = Zeus-protocol."
question: "Confirmas corregir las refs de diseno de SPEC-0086 a D:\\Agentes\\Zeus\\Zeus-protocol\\design\\ (y TASK-0124) antes de que Codex arranque?"
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
validation_refs:
  - "Verificado canonico 064306f: SPEC-0086 accepted (refs a D:\\Agentes\\Zeus\\design\\ - VIEJA); TASK-0124 ready; 44 eventos firmados seq 672-715; #4 4 flags true; validate clon-fresco exit 0. Archivos movidos a D:\\Agentes\\Zeus\\Zeus-protocol\\design\\ (brief en design\\interface\\)."
deadline_or_blocking_level: high
---

# T0 OK; corregir ruta de diseno en SPEC-0086 (movida a Zeus-protocol\design)

Verifique T0 en canonico (064306f): **SPEC-0086 accepted, TASK-0124 ready, 44 eventos firmados (seq
672-715), #4 intacto, validate exit 0.** T0 atestado, dataset nacido. Bien.

## Correccion (decision del operador)
El repo producto es **Zeus-protocol** y **el diseno/insumos viven dentro del repo producto**:
- `D:\Agentes\Zeus\Zeus-protocol\design\front_requirements.html`
- `D:\Agentes\Zeus\Zeus-protocol\design\front_pipeline.html`
- `D:\Agentes\Zeus\Zeus-protocol\design\interface\` (aqui deposita Claude Design su salida)

SPEC-0086 referencia la ruta **vieja** (`D:\Agentes\Zeus\design\...`), que ya **movi** (esos archivos ya
no estan ahi). Antes de que Codex implemente TASK-0124 y no los encuentre:
- Corrige las refs de insumo de **SPEC-0086** a `...\Zeus-protocol\design\...` (update gobernado via
  submit_intent, ya que la SPEC esta atestada).
- Verifica que **TASK-0124 / el GO a Codex** apunten a la ruta nueva.

Nota: el directorio viejo `D:\Agentes\Zeus\design\` quedo vacio (no pude borrarlo por la ACL del mount);
inofensivo, lo limpia el operador.

#4 intacto (epoca 1.14.0). Floor: CI antes del codigo que compila/testea. Canal ASCII.
