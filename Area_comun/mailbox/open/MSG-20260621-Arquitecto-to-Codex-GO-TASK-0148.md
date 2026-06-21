---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0148
task_id: TASK-0148
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0148 (ready, maker=Codex): #9 ULTIMO - carga de requerimiento por archivo (ingestion gobernada acotada, OFF-by-default). Server-side: allowlist tipo .md/.txt + limite tamano + nombre saneado (sin path traversal) + contenido INERTE (nunca ejecutado) + PII structural/ASCII + idempotente; alimenta el MISMO requirement-intake (solo execute escribe). Anti-abuso prueba negativa permanente. #4 byte-identica. Ratificado: DECISION-0055 + ext8 SPEC-0086 (AC37/AC38). Codigo en Zeus; yo checker + PASADA DEL ANALISTA antes de cerrar. NO encender vivo (OFF; pre-auth condicionada del operador, activacion runtime)."
context_refs:
  - Area_comun/decisions/DECISION-0055-file-ingestion.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0148-codex-front-file-ingestion.md
  - Area_comun/tasks/req-31100eaf-requirement-seed.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0148 carga por archivo (RF-14, AC37/AC38; DECISION-0055) - #9 ULTIMO

Ratificado (DECISION-0055 + ext8 SPEC-0086). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA
(ingestion/egress) antes de cerrar. Codigo en Zeus (server+front). EL MAS SENSIBLE: superficie de INGRESO.
OFF BY DEFAULT.

## Alcance
1. **Server:** ingestion server-side: allowlist tipo (.md/.txt) + limite tamano (<= N KB) + nombre saneado
   (sin `/`,`\`,`..`,`:`, control) + contenido INERTE (NUNCA ejecutado/evaluado/render-activo); PII structural +
   ASCII al texto extraido; alimenta el MISMO requirement-intake (task_upsert type=requirement, author=Operador,
   relayed_by=Arquitecto provistos por el caller server-side); idempotente (mismo archivo = mismo id-hash); solo
   el execute gobernado escribe.
2. **Front:** adjuntar -> preview redactado (dry_run) -> execute+confirm -> resultado id+seq o error (no verde).
   Con OFF (default), adjuntar archivo no esta disponible / flujo no cambia.
3. **Config OFF-by-default** FUERA del config pinned. NO commitear enabled:true en el versionado (patron 0054).

## Cierre (innegociable)
- AC37 (ingestion gobernada acotada, idempotente, honesta; HEAD valida exit 0) + AC38 (anti-abuso permanente:
  tipo/tamano/traversal/contenido-activo/inyeccion -> RECHAZADO; sin egress; cliente no inyecta actor/rutas).
  Carry AC11/AC13/AC17/AC19/AC22.
- Camino feliz con ON contra clon de PRUEBA (no el vivo): archivo .md -> requirement real id+seq; HEAD valida exit 0.
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- Reproducido por el checker desde clon limpio; maker!=checker. **PASADA DEL ANALISTA antes de cerrar.**

Entrega in_review con handoff y libera tu claim. Es el ULTIMO de la cola de 9. Canal ASCII.
