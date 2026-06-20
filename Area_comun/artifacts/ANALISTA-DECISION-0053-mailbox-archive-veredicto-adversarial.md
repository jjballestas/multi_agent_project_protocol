# ANALISTA - VOZ EXTERNA ADVERSARIAL - DECISION-0053 (mailbox_archive + relay mailbox-archive)

> Voz: Analista (escepticismo externo: intento REFUTAR que bounding y neutralidad esten cerrados).
> Firma: Analista. Fecha: 2026-06-20. Lente: seguridad / honestidad / neutralidad / metodologia.
> ANCLADO EN CANONICO: protocolo HEAD==origin `7e47cbc` (DECISION-0053 + ext5 ya promovidas);
> codigo runtime en el protocolo; codigo front en clon limpio Zeus-protocol @ `6afefe7` (arbol limpio).
> Verifique leyendo el CODIGO y corriendo golden/suite; NO asumi los drafts. NO promuevo, NO autoro SPEC,
> NO muto estado. ANTES de cerrar TASK-0138 (in_progress).

## VEREDICTO DE CABECERA
El BOUNDING anti-impersonacion (#1, lo mas critico) RESISTE: no pude reabrir la forja de intents como
Arquitecto. PERO encontre un CAMBIO REQUERIDO en NEUTRALIDAD (#4): el core hardcodea las identidades de
ESTA instancia ("Operador"/"Arquitecto") en `runtime/submit_intent.py`, y el scan de neutralidad NO lo
detecta -> regresion de neutralidad SILENCIOSA. Recomiendo: cerrable SOLO tras resolver o DECLARAR
explicitamente #4. #1/#2/#3/#6 PASA. #5 PASA con el cambio de #4.

## Reproduccion (gate por exit code)
- Golden core `examples/mailbox_archive_cases` -> **exit 0** (3/3).
- Zeus clon @ 6afefe7: `npm test` -> **26/26 PASS** (4 nuevos de mailbox-archive).
- Protocolo: `validate_collaboration_state` exit 0, `scan_domain_neutrality` exit 0, drift `has_drift=false`
  up_to_seq 883.

---

## 1) BOUNDING (lo mas critico) -> PASA (no pude refutar)
- `EXECUTABLE_ACTIONS = new Set(["requirement-intake","mailbox-archive"])` (server.js); hard-gate
  `if (!EXECUTABLE_ACTIONS.has(submission.actionId)) -> 403`. EXACTAMENTE dos; toda otra forma 403.
- Builder SERVER-SIDE (`buildMailboxArchiveIntents`): array FIJO `claim acquire -> mailbox_archive ->
  claim release`, todo como Arquitecto; el unico input del cliente es `mailbox.messageId`. `payload.actorId`
  y `payload.intents` siguen rechazados (400, heredado de AC19); `assertAllowedKeys` cierra el payload
  (top-level admite solo {actionId,mode,confirm,intake,mailbox}).
- DOS CAPAS: el runtime tambien valida `mailbox_archive` (exige capability `orchestrator`; rechaza id con
  `/ \ ..`; doble guarda de escape con `.resolve()` que atrapa symlinks; exige existencia).
- Agregar la 2a accion NO erosiona AC19: el gate es un Set cerrado y cada accion ejecutable tiene builder
  fijo; `mailbox-archive` SOLO puede emitir su `mailbox_archive` (+ claim wrapper), no intents arbitrarios.
- Prueba negativa PERMANENTE en CI (staticContract): forjar intents en mailbox-archive -> 400; traversal
  `messageId:"../MSG-escape"` -> 400; `MSG-does-not-exist` -> !=200; non-executable execute -> 403.
- Intente forjar otro intent como Arquitecto via mailbox-archive: imposible (builder fijo + rechazo de
  intents crudos + 403 fuera del set). **PASA.**

## 2) VALIDACION DEL PAYLOAD del kind -> PASA (1 RIESGO menor)
- Existencia: el runtime exige que el mensaje exista en open/ (o archived/ para idempotencia). messageId
  validado en server (regex + sin `..`/slashes) Y en runtime (regex + `.resolve()` bajo mailbox_root).
  Sin path-traversal, sin absolutos, symlinks atrapados por resolve.
- Idempotencia CORRECTA: `idempotency_key = front:mailbox-archive:<hash(messageId)>` ESTABLE -> re-archivar
  = `deduped:true` (test lo asserta), no falla, no doble-evento; el side-effect `shutil.move` esta guardado
  por `if source.exists()` -> no-op si ya archivado. Reversible (move, no delete): sin perdida de info.
- **RIESGO DECLARADO (menor, portabilidad/robustez):** `MAILBOX_MESSAGE_ID_RE = ^MSG-[A-Za-z0-9_@{}~^:-]+$`
  admite `:` `@` `{` `}` `~` `^`. En Windows `:` en un nombre de archivo crea un NTFS Alternate Data Stream.
  Queda CONTENIDO (la guarda `.resolve()`+parent mantiene el path bajo mailbox/, y se exige existencia), no
  es escape, pero permitir esos chars en un id que se escribe a disco es un smell de portabilidad. Sugerido:
  acotar la regex a `[A-Za-z0-9._-]` (los ids reales solo usan guiones).

## 3) #4 INTACTO -> PASA
- El test asserta BYTE-IDENTIDAD de `protocol.config.json`, `chain_manifest.json` y
  `secrets/eventauth-arquitecto.key` antes/despues del archive real (no solo drift 0). El nuevo kind no toca
  config/genesis/keys/`protocol_version`; los eventos encadenan normal. Un archive real deja el canonico
  VERDE (validate exit 0). **PASA.**

## 4) NEUTRALIDAD (regla 1) -> CAMBIO REQUERIDO
**El core NO queda domain/instance-neutral: hardcodea identidades de ESTA instancia.**
`runtime/submit_intent.py` (normalize del kind, lineas 336-339) estampa CONSTANTES:
```
"author": "Operador",
"relayed_by": "Arquitecto",
"endorsement": "none",
```
"Operador" y "Arquitecto" son los agentes de ESTA instancia (su `agent_registry`), NO conceptos genericos
del protocolo. El runtime es maquinaria generica (se publica); el resto del core usa ROLES/capabilities
(`orchestrator`/`implementer`/`reviewer`), no nombres -> aqui se cuela la identidad de instancia en el kind.
- **Silencioso:** `scan_domain_neutrality` pasa exit 0 (solo busca terminos de dominio/trading, no nombres
  de agente) -> la regresion de neutralidad NO la atrapa ningun gate.
- **Inconsistente con el patron del intake:** para `requirement-intake` la atribucion author=Operador/
  relayed_by=Arquitecto la pone el CALLER (el server Zeus, en el task payload) y el core `task_upsert` solo
  la almacena -> core neutral. `mailbox_archive` rompe ese patron y la hardcodea en el core.
- **Correccion (falsable):** la atribucion del relay debe ser CALLER-PROVIDED (el server Zeus la pasa en el
  payload del intent, validada), NO constante en el core; el kind `mailbox_archive` core no debe contener
  literales "Operador"/"Arquitecto". Falsable: `grep -nE '"Operador"|"Arquitecto"' runtime/submit_intent.py`
  debe dar 0 tras el fix (hoy da 2). (Nota: hay leaks PRE-EXISTENTES analogos -- apply.py:440 owner default
  "Codex", context.py:16 implementer->"Codex" -- conviene un follow-up de limpieza de neutralidad del core.)

## 5) HONESTIDAD / accountability -> PASA con CAMBIO (corolario de #4)
- Lo honesto: el evento registra `actor=Arquitecto` (firmante real) y NO afirma que el Operador firmo
  criptograficamente; el archive es auditable (evento con seq) y REVERSIBLE (move open->archived, no delete,
  sin perdida de info). En esos ejes PASA.
- El CAMBIO: como `author="Operador"` es una CONSTANTE hardcodeada (no derivada de quien origino), CUALQUIER
  `mailbox_archive` -- incluso uno que un orchestrator emita directo por terminal, NO en nombre del operador
  -- quedaria atestado con `author=Operador / endorsement=none`. Eso es una MIS-ATRIBUCION DE ORIGEN
  potencial: el mecanismo no verifica el origen, lo estampa. Hoy el unico caller es el relay del front
  (clic del operador) asi que coincide por accidente; pero para un dataset de tesis cuyo valor es la
  atestacion honesta, estampar un origen constante es debil. Resolver junto con #4 (atribucion derivada del
  caller).

## 6) GOBERNANZA -> PASA
- DECISION-0053 propia (amends 0052) para un NUEVO intent kind core es el encuadre HONESTO: agregar un kind
  al escritor unico es cambio de superficie del protocolo (regla 2: cambio de protocolo -> DECISION
  primero), aunque sea aditivo/backward-compatible. Bien registrado, con rastro de gobernanza. **PASA.**

---

## RESUMEN
| # | Veredicto | Lo critico |
|---|-----------|-----------|
| 1 BOUNDING | PASA | Set cerrado {intake,archive}+403; builder fijo server-side; 2 capas; no pude forjar otro intent |
| 2 PAYLOAD | PASA | regex+resolve-escape+existencia+idempotente(deduped); RIESGO menor: regex admite `:` (ADS Windows), contenido |
| 3 #4 intacto | PASA | byte-identidad config/manifest/key asertada, no solo drift 0 |
| 4 NEUTRALIDAD | **CAMBIO REQUERIDO** | core hardcodea "Operador"/"Arquitecto" (submit_intent.py 337-338); scan no lo atrapa = regresion silenciosa; hacer caller-derived |
| 5 HONESTIDAD | PASA + cambio | atribucion presente, reversible, no miente sobre firma; pero constante hardcodeada -> mis-atribucion de origen posible; atar a #4 |
| 6 GOBERNANZA | PASA | DECISION propia para kind nuevo = encuadre honesto |

## RECOMENDACION
**CERRABLE SOLO tras resolver o DECLARAR explicitamente #4** (neutralidad). El bounding -- el riesgo de
reabrir la impersonacion, que era el temor central -- esta CERRADO. El defecto vivo es de NEUTRALIDAD/
honestidad de atribucion (instance-names en el core neutral, atribucion constante). Opciones honestas:
(a) hacer la atribucion caller-derived (preferible, consistente con el intake) -> entonces cerrable; o
(b) si el operador/Arquitecto aceptan el hardcode para el alcance dogfooding mono-instancia, registrarlo
como DEUDA DE NEUTRALIDAD declarada (no silenciosa) con follow-up. NO cerrar como si el core siguiera
neutral sin nota.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre la tarea. Ancle en canonico (7e47cbc / 6afefe7), no
  working tree. Corri el archive real solo en golden/clon temporal del propio test (no toca el ledger vivo).
