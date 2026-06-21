---
decision_id: DECISION-0055
title: Superficie de INGESTION de archivos en el Intake (acotada, OFF-by-default, con pasada del Analista)
status: accepted
ratified_at: 2026-06-21
date: 2026-06-21
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: []
relates_to: [DECISION-0051, DECISION-0052, DECISION-0054, DECISION-0040, DECISION-0046]
phase: P2
---

# DECISION-0055 - Ingestion de archivos en el Intake (acotada, OFF-by-default)

> ACCEPTED por el operador (2026-06-21; GO-SPECS-ZEUS-PROPOSED para autorar las 9 + nota REQ-31100EAF
> "disenala OFF/gateada... pasada del Analista al cierre" + GO-PREAUTH-INGESTION-LIVE). Origen: REQ-31100EAF.
> Superficie de INGRESO NUEVA -> DECISION propia (regla 2 + frontera). maker=Codex / checker=Arquitecto +
> PASADA DEL ANALISTA (ingestion/egress) al cierre. OFF-by-default; uso vivo = pre-autorizacion condicionada
> del operador (entrega+cierre + Analista OK + activacion RUNTIME, versionado OFF).

## Contexto
REQ-31100EAF: el operador quiere adjuntar un ARCHIVO en el Intake y que su contenido alimente un requerimiento
gobernado, sin transcribir a mano. Hoy el Intake captura campos TECLEADOS. Recibir un archivo (leer su contenido,
parsearlo) es una superficie de INGRESO NUEVA: riesgos de ingestion (tipo/tamano, path traversal en el nombre,
contenido malicioso, PII en el contenido, ejecucion accidental).

## Por que DECISION propia
Una nueva via por la que ENTRAN datos al sistema (file upload) es cambio de superficie del protocolo/producto
(regla 2) y toca la frontera de seguridad (no-ejecucion, no-egress, PII). Aunque el EXECUTE final sigue siendo el
mismo task_upsert gobernado, la INGESTION previa es nueva. Merece rastro auditable.

## Decision
1. **Ingestion ACOTADA y server-side.** El archivo se procesa en el server: (a) **allowlist de tipo** (.md/.txt;
   nada ejecutable/binario activo); (b) **limite de tamano** (rechaza > N KB); (c) **nombre saneado** (sin path
   traversal: rechaza `/`,`\`,`..`,`:`, control chars; nunca se usa el nombre para escribir fuera de un area
   temporal controlada); (d) **contenido NUNCA ejecutado/evaluado** (texto inerte; no eval, no shell, no render
   activo).
2. **Mismo camino gobernado que el intake actual.** El contenido extraido alimenta el MISMO `requirement-intake`
   (task_upsert type=requirement, author=Operador, relayed_by=Arquitecto provistos por el caller, neutralidad core
   DECISION-0053): el EXECUTE gobernado es el unico que escribe; preview(dry_run) != green; idempotente (re-subir
   el mismo archivo = mismo id-hash, no duplica).
3. **PII structural guard + ASCII-only al texto EXTRAIDO** (igual que al texto tecleado; DECISION-0040).
4. **OFF BY DEFAULT, reversible por flag.** Nace deshabilitada (registro FUERA del config pinned). Uso vivo =
   activacion por RUNTIME (env), versionado `enabled:false` (patron commit-push DECISION-0054). Pre-autorizacion
   condicionada del operador: aplica SOLO tras entrega+cierre + Analista OK + activacion runtime; si el Analista
   pide CUALQUIER cambio, NO aplica hasta resolverlo.
5. **Honestidad (AC11):** exito SOLO con el requerimiento REALMENTE escrito (id+seq reales); si la ingestion o el
   execute fallan -> error real, no verde, sin requerimiento fantasma.
6. **No toca el escritor unico ni #4.** La ingestion produce el MISMO intent gobernado; no agrega un 2o escritor;
   no toca config/genesis/keys; #4 byte-identica.

## Alcance / limites
- Solo lectura/parseo de texto inerte -> alimenta el requirement-intake existente. NO ejecuta contenido, NO
  egress, NO escribe fuera del camino gobernado.
- Tipos no permitidos / sobre-tamano / nombre peligroso -> RECHAZADOS antes de tocar el intake.
- El cliente NO controla rutas de escritura ni el actor (server-side, hereda la defensa anti-impersonacion).

## Threat model (resumen)
Path traversal via nombre -> saneado/rechazado (prueba negativa permanente). Tipo/tamano abusivo (zip-bomb,
binario, ejecutable) -> allowlist + limite. Contenido malicioso (script/macro) -> texto inerte, nunca ejecutado.
PII de terceros en el archivo -> structural guard + ASCII; plano publicable redactado. Requerimiento fantasma ->
AC11 (solo execute real escribe; id+seq reales). Encendido sin querer -> off-by-default + activacion runtime.

## Consecuencias
Nueva capacidad de producto (Zeus) off-by-default. El core no cambia. Activacion viva = pre-auth condicionada del
operador (no otro GO si se cumplen las 3) + pasada del Analista (ingestion/egress) al cierre.

## Condiciones de cierre (innegociables)
(a) allowlist de tipo + limite de tamano + nombre saneado (sin traversal) + contenido nunca ejecutado, server-side;
(b) prueba negativa PERMANENTE: tipo no permitido / sobre-tamano / nombre con traversal / contenido activo ->
RECHAZADO; (c) PII structural + ASCII al texto extraido; (d) idempotente (re-subir = no duplica); (e) execute
gobernado es el unico que escribe; honestidad AC11 (id+seq reales); (f) off-by-default, reversible por flag,
registro fuera del config pinned; (g) #4 byte-identica, validate con/sin secretos exit 0, drift 0, npm test verde,
neutralidad/encoding 0; (h) PASADA DEL ANALISTA (ingestion/egress) ANTES de cerrar.
