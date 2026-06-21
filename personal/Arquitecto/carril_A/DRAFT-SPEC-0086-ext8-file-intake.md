# DRAFT - Extension 8 de SPEC-0086: carga de requerimiento por archivo (ingestion gobernada) [AC37/AC38]

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-31100EAF. Superficie de INGESTION -> bajo
> DECISION-0055. maker=Codex / checker=Arquitecto + pasada del Analista. Codigo en Zeus. OFF BY DEFAULT.

## Origen (REQ-31100EAF, author=Operador)
Adjuntar un archivo en el Intake y que su contenido alimente un requerimiento gobernado que aterriza en
canonico con id+seq reales (mismo camino que el intake actual), sin transcribir a mano. Acotada, OFF/gateada
si abre superficie nueva.

## AC37 - Carga de requerimiento por archivo, gobernada y acotada [comportamiento PERMANENTE; DECISION-0055]
Desde el Intake, el operador adjunta un archivo; el server (a) valida **tipo** (allowlist .md/.txt), **tamano**
(<= N KB) y **nombre saneado** (sin path traversal); (b) extrae el texto como contenido INERTE (nunca ejecutado/
evaluado); (c) aplica **PII structural guard + ASCII** al texto extraido; (d) alimenta el MISMO
`requirement-intake` (task_upsert type=requirement, author=Operador, relayed_by=Arquitecto). Solo el EXECUTE
gobernado escribe; preview(dry_run) != green. **Idempotente:** re-subir el mismo archivo (mismo id-hash) no
duplica. **Honestidad (AC11):** exito SOLO con el requerimiento REALMENTE escrito (id+seq reales); si la
ingestion o el execute fallan -> error real, no verde. **OFF BY DEFAULT** (flag fuera del config pinned; uso
vivo = GO posterior del operador). El HEAD resultante valida exit 0 (regresion-proof, estilo AC22).

## AC38 - Anti-abuso de ingestion (prueba negativa PERMANENTE) [CRITICO; DECISION-0055]
Tests permanentes (no reabrir): tipo NO permitido (binario/ejecutable) -> RECHAZADO; archivo sobre-tamano ->
RECHAZADO; nombre con **path traversal** (`/`,`\`,`..`,`:`, control) -> RECHAZADO/saneado; contenido "activo"
(script/macro) -> tratado como TEXTO INERTE, nunca ejecutado/renderizado; el cliente NO inyecta actor ni rutas
de escritura (server-side, hereda anti-impersonacion AC19); sin egress; #4 byte-identica (config/genesis/keys
sin cambio). PII: patrones tipo NIT/razon social/SQL en el archivo -> el plano publicable no expone el literal.

## test_plan (anadido)
- **Server (Zeus):** camino feliz con capacidad ON contra clon de prueba: archivo .md valido -> requirement
  real con id+seq; HEAD valida exit 0. Negativos (AC38): tipo/tamano/traversal/contenido-activo/inyeccion ->
  rechazados antes de tocar el intake. Idempotencia: mismo archivo -> mismo id, no duplica.
- **Front:** adjuntar archivo muestra preview redactado (dry_run); execute -> resultado con id+seq o error (no
  verde) si falla; con capacidad OFF (default), el adjuntar archivo no esta disponible / el flujo no cambia.
- **Gates:** validate con/sin secretos exit 0; drift 0; #4 byte-identica; neutralidad/encoding 0; npm test.

## Carry permanentes
AC11 / AC13 / AC17 (no 2o escritor) / AC19 (anti-impersonacion server-side) / AC22 (intake deja canonico verde).
OFF by default; uso vivo = GO operador; pasada del Analista (ingestion/egress) antes de cerrar.
