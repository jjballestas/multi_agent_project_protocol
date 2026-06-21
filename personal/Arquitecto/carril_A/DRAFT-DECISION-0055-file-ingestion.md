# DRAFT - DECISION-0055: superficie de INGESTION de archivos en el Intake (acotada, OFF-by-default)

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion. Origen: REQ-31100EAF (intake del operador).
> Superficie de INGRESO NUEVA -> DECISION propia (regla 2 + frontera). maker=Codex / checker=Arquitecto +
> PASADA DEL ANALISTA (ingestion/egress) al cierre. OFF-by-default; uso vivo = GO posterior del operador.

## status
proposed

## Contexto
REQ-31100EAF: el operador quiere adjuntar un ARCHIVO en el Intake y que su contenido alimente un requerimiento
gobernado, sin transcribir a mano. Hoy el Intake captura campos TECLEADOS. Recibir un archivo (leer su contenido,
parsearlo) es una **superficie de ingreso NUEVA**: trae riesgos de ingestion (tipo/tamano, path traversal en el
nombre, contenido potencialmente malicioso, PII en el contenido, ejecucion accidental).

## Por que DECISION propia
Una nueva via por la que ENTRAN datos al sistema (file upload) es cambio de superficie del protocolo/producto
(regla 2) y toca la frontera de seguridad (no-ejecucion, no-egress, PII). Merece rastro auditable. Aunque el
EXECUTE final sigue siendo el mismo task_upsert gobernado, la INGESTION previa es nueva.

## Decision
1. **Ingestion ACOTADA y server-side.** El archivo se procesa en el server: (a) **allowlist de tipo** (p.ej.
   .md/.txt; nada ejecutable/binario activo); (b) **limite de tamano** (rechaza > N KB); (c) **nombre saneado**
   (sin path traversal: rechaza `/`,`\`,`..`,`:`, control chars; nunca se usa el nombre para escribir en disco
   fuera de un area temporal controlada); (d) **contenido NUNCA ejecutado/evaluado** (se trata como texto inerte;
   no eval, no shell, no render activo).
2. **Mismo camino gobernado que el intake actual.** El contenido extraido alimenta el MISMO `requirement-intake`
   (task_upsert type=requirement, author=Operador, relayed_by=Arquitecto): el EXECUTE gobernado es el unico que
   escribe; preview(dry_run) != green; idempotente (re-subir el mismo archivo = mismo id-hash, no duplica).
3. **PII structural guard + ASCII-only al texto EXTRAIDO.** La guarda PII (separar plano publicable, redactar
   texto libre) y el canal ASCII se aplican al contenido del archivo igual que al texto tecleado (DECISION-0040).
4. **OFF BY DEFAULT, reversible por flag.** Nace deshabilitada (registro FUERA del config pinned, estilo
   connectors.config.json / commit-push runtime). Uso vivo = GO posterior del operador. Reversible por flag.
5. **Honestidad (AC11):** exito SOLO con el requerimiento REALMENTE escrito (id+seq reales); si la ingestion o
   el execute fallan -> error real, no verde, sin requerimiento fantasma.
6. **No toca el escritor unico ni #4.** La ingestion produce el MISMO intent gobernado; no agrega un 2o escritor;
   no toca config/genesis/keys; #4 byte-identica.

## Alcance / limites
- Solo lectura/parseo de texto inerte -> alimenta el requirement-intake existente. NO ejecuta contenido, NO
  egress, NO escribe fuera del camino gobernado.
- Tipos no permitidos / sobre-tamano / nombre peligroso -> RECHAZADOS antes de tocar el intake.
- El cliente NO controla rutas de escritura ni el actor (server-side, hereda la defensa anti-impersonacion).

## Threat model (resumen)
- Path traversal via nombre de archivo -> saneado/rechazado (prueba negativa permanente).
- Tipo/tamano abusivo (zip-bomb, binario, ejecutable) -> allowlist + limite (rechazado).
- Contenido malicioso (script, macro) -> tratado como texto inerte, NUNCA ejecutado/renderizado activo.
- PII de terceros en el archivo -> structural guard + ASCII al texto extraido; plano publicable redactado.
- Requerimiento fantasma (preview pintado verde) -> AC11 (solo execute real escribe; id+seq reales).
- Encendido sin querer -> off-by-default + GO del operador.

## Consecuencias
Nueva capacidad de producto (Zeus) off-by-default. El core no cambia. Activacion viva = GO posterior + pasada
del Analista (ingestion/egress) al cierre.

## Condiciones de cierre (innegociables)
(a) allowlist de tipo + limite de tamano + nombre saneado (sin traversal) + contenido nunca ejecutado, todo
server-side; (b) prueba negativa PERMANENTE: tipo no permitido / sobre-tamano / nombre con traversal / contenido
activo -> RECHAZADO; (c) PII structural + ASCII al texto extraido; (d) idempotente (re-subir = no duplica);
(e) execute gobernado es el unico que escribe; honestidad AC11 (id+seq reales); (f) off-by-default, reversible
por flag, registro fuera del config pinned; (g) #4 byte-identica, validate con/sin secretos exit 0, drift 0,
npm test verde, neutralidad/encoding 0; (h) PASADA DEL ANALISTA (ingestion/egress) ANTES de cerrar.
