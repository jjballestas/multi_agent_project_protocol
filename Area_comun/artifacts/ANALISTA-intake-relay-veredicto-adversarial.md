# ANALISTA - VOZ EXTERNA ADVERSARIAL - mecanismo RELAY del intake del operador

> Voz: Analista (escepticismo externo: el diseno puede estar mal hasta probar lo contrario).
> Firma: Analista. Fecha: 2026-06-20. Lente: honestidad / metodologia / neutralidad / SEGURIDAD.
> ANCLADO EN CANONICO (git show), NO working tree. Protocolo HEAD == origin == `fc31bfe`.
> Drafts revisados (canonico fc31bfe): DRAFT-DECISION-0052, DRAFT-SPEC-0086-ext2, DRAFT-TASK-0134.
> Codigo del front revisado (canonico Zeus-protocol HEAD `42e7931`, TASK-0133 = el intake YA mergeado).
> NO diseno, NO autoro SPEC, NO muto estado, NO promuevo. Veredicto por punto. ANTES de la ratificacion.

## VEREDICTO DE CABECERA
El RELAY (firmar como Arquitecto en nombre del Operador) es una eleccion RAZONABLE para el problema
estrecho (Operador no es firmante -> no tocar la epoca pinned). PERO la pasada destapa un **defecto de
SEGURIDAD CRITICO que el relay NO cierra y que YA EXISTE en el canonico**: el endpoint de escritura del
front es una **superficie general de impersonacion** (firmar intents ARBITRARIOS como Arquitecto). Sin
cerrarlo, ratificar el relay LEGITIMA esa superficie. 2 CAMBIOS CRITICOS (#1, #3), 3 CAMBIOS (#2, #4, #5),
2 PASA-con-nota (#6, #7).

---

## 1) ALCANCE / SEGURIDAD del relay  ->  CAMBIO REQUERIDO (CRITICO, bloqueante)

**El relay NO esta acotado al requirement-intake, y NO existe prueba negativa.** Peor: el canonico
actual del front (`Zeus-protocol/src/server.js`, HEAD 42e7931) YA es una superficie general de
impersonacion, independiente del relay:

- `buildGovernedSubmission` (server.js ~369-371): para CUALQUIER accion distinta de `requirement-intake`,
  `intents = payload.intents` (intents ARBITRARIOS provistos por el CLIENTE) si vienen; el unico chequeo
  (~372-376) es que cada intent tenga un kind en `ALLOWED_INTENT_KINDS`
  = {task_status, task_upsert, claim, decision, project_narrative, protocol_prune}. **NO** se valida que el
  contenido/forma del intent corresponda a la accion; el `intentKinds` declarado por accion es decorativo,
  no se enforce.
- `actorId: action.actorId || payload.actorId || "Arquitecto"` (server.js ~384): solo `requirement-intake`
  fija `actorId` (Operador). Para TODAS las demas acciones, el actor lo pone el **CLIENTE**
  (`payload.actorId`) o cae por defecto a **"Arquitecto"**.
- El endpoint `/api/protocol/actions/submit` escucha en `127.0.0.1` **sin auth/token**.

**Consecuencia falsable:** un POST local a `/api/protocol/actions/submit` con
`{actionId:"go-requires-response", confirm:"SUBMIT_INTENT", intents:[{claim:{acquire ... scope}}, {decision:{...}}], actorId:"Arquitecto"}`
seria construido y enviado a `submit_intent` **firmado como Arquitecto**. Como Arquitecto ES firmante
pinned y el claim necesario va en la MISMA transaccion, el gate `enforce` NO lo detiene -> se puede
**forjar una decision/cambio de estado/claim/protocol_prune atestado, atribuido al Arquitecto.** El unico
"control" hoy (`negative no-bypass contract`) es string-match (chequea que el server contiene
"direct ledger write routes are rejected" y que no hay `/api/.../(direct|raw|bypass)`); **NO** prueba que
el actor/intents no se puedan forjar. Falso-verde de seguridad.

**Correccion (falsable, condicion de ratificacion):**
1. **Nunca confiar en `payload.actorId`:** eliminar el fallback al actor del cliente. El `actorId` lo fija
   el SERVIDOR por accion.
2. **Cada accion gobernada = builder server-side o validador de forma estricto** ligado a su `intentKinds`
   declarado (como ya hace `requirement-intake` via `buildRequirementIntakeIntents`). Rechazar
   `payload.intents` de forma libre que no casen la forma declarada de la accion.
3. **El relay (firmar como Arquitecto) aplica SOLO a la forma exacta del intake** construida por el
   servidor: `claim(acquire Arquitecto, scope=el archivo del requirement) -> task_upsert(type=requirement,
   author=Operador, relayed_by=Arquitecto) -> claim(release)`. Cualquier otra cosa, rechazada.
4. **Prueba NEGATIVA de comportamiento (permanente, CI):** una submission que intente relayar como
   Arquitecto un `task_status` / `decision` / `claim` de scope arbitrario / `protocol_prune` /
   `task_upsert` que no sea el requirement-shape, **es RECHAZADA** (no firmada, no escrita). Sin este test,
   el verde de AC15 da falsa seguridad.

**Nota DECISION-0018 (anomalia en canonico):** esta superficie ya esta MERGEADA (TASK-0133, HEAD 42e7931).
No es solo un riesgo del draft: el front canonico HOY puede forjar gobernanza como Arquitecto. Reportarlo
como anomalia y cerrarlo en TASK-0134 (no solo "no introducir" el problema: REMEDIARLO).

---

## 2) HONESTIDAD de atribucion  ->  PASA con CAMBIO

- El modelo de DECISION-0052 es honesto: `author:"Operador"` + `relayed_by:"Arquitecto"`; "nada sugiere
  que el Operador firma"; AC18 exige que el evento lleve ambos campos. El payload del intake
  (server.js ~404) ya pone `author:"Operador"`. Coherente con AC11 (no verde falso).
- **CAMBIO (falsable):** AC18 prueba el PAYLOAD ("el evento lleva ambos campos") pero NO prueba el RENDER.
  La afirmacion "ningun plano afirma que el Operador firmo" queda ASEVERADA, no testeada. Anadir un test
  de COMPORTAMIENTO de la UI: la vista de atestacion/timeline renderiza el FIRMANTE = Arquitecto (no
  Operador), etiqueta `author=Operador` como "originador (NO firmante)", y NINGUN badge/sello dice
  "Operador: firma verificada". Si no, la honestidad de atribucion es promesa, no propiedad.

---

## 3) ACCOUNTABILITY (firmar contenido no autorado ni revisado)  ->  CAMBIO REQUERIDO

El Arquitecto firma criptograficamente texto del operador que NO autoro NI reviso. DECISION-0052 lo
enmarca honestamente como "relayo, no avalo" -- pero esa distincion vive en un campo de payload
(`relayed_by`), mientras que la SEMANTICA de la firma #4 dice "Arquitecto firmo el evento N". Un analisis
del dataset atestado (el corpus de tesis) puede leer "Arquitecto firmo N" como "Arquitecto produjo/avalo
N". Riesgo de **lavado de accountability**: texto del operador entra al dataset atestado bajo la firma del
Arquitecto sin revision.

**Correccion (falsable):**
1. **`relayed` como ciudadano de primera clase**, no solo un campo: el evento/requirement declara
   explicitamente `endorsed:false` / `relayed:true` (o equivalente) para que ningun rollup confunda
   firmante con autor/avalador.
2. **DECISION-0052 declara la semantica:** "un evento relayado atesta ORIGEN + TRANSPORTE, NO revision ni
   aval del firmante; la revision/aval del Arquitecto ocurre DESPUES, al autorar la SPEC." Esto separa
   intake (semilla relayada) de SPEC (autoria/aval real).
3. **Test:** un requirement relayado NO se cuenta como "autorado por el Arquitecto" en ninguna metrica/
   vista del dataset.

---

## 4) #4 INTACTO (verificable)  ->  PASA con CAMBIO

- **Correcto en el fondo:** firmar como Arquitecto usa un firmante YA pinned (clave anclada al genesis) ->
  NO edita `protocol.config.json` (cuyo hash es el `prev_hash` del `chain.genesis`) -> **no re-genesis, no
  toca event_auth.keys, epoca 1.14.0 pinned.** El Operador NO se agrega al config. Es justo lo que evita
  el relay. Drift hoy = 0 (verificado en pasadas previas).
- **CAMBIO (falsable):** "drift 0" es NECESARIO pero NO SUFICIENTE para afirmar "#4 intacto": un config-edit
  + re-genesis tambien puede dar drift 0. La AC debe asertar, ADEMAS del drift, que `protocol_version`, el
  hash de `chain.genesis` y el conjunto `event_auth.keys` son **byte-identicos antes y despues** del write
  del intake (epoca pinned, conjunto de firmantes sin cambios). Sin esa asercion, "no toca #4" no es
  falsable, es declarativo.

---

## 5) VERIFICACION (el miss original)  ->  PASA (fuerte) con CAMBIO

- AC15 REVISADO cierra el miss de TASK-0133 (que solo probo el 409): exige test de COMPORTAMIENTO del
  CAMINO FELIZ (`execute+confirm` -> escritura REAL por submit_intent: requirement en TASK_INDEX/
  PROJECT_STATE, seq, drift 0, atribucion), "NO basta dry_run ni 409", y el DoD exige reproducir el write
  real desde clon limpio. Direccion correcta y explicita.
- **CAMBIO (falsable):** el test del happy path debe ejercer el **submit_intent REAL** (o un runtime fixture
  FIEL que escriba de verdad), NO un mock que devuelva `ok`; debe ser **permanente en CI** (node --test),
  no un smoke manual de una vez; y asertar la **mutacion real de estado** + seq + `author=Operador`/
  `relayed_by=Arquitecto`, gateado por exit code. Si se mockea el escritor, se reintroduce el falso-verde.
  (Leccion previa: el checker debe probar el WRITE real, no dry_run + negativa.)

---

## 6) GUARDA PII  ->  PASA con NOTA (no sobre-afirmar)

- Verificado en `sanitizeRequirementIntake`/`redactPublicText` (server.js): el texto libre se fuerza a
  ASCII (`ascii()` NFD + strip no-imprimibles), se quitan controles, y se redactan patrones NIT /
  "razon social" / verbos SQL (select/insert/update/delete) / `dbo.`|`schema.`. Solo
  `publicNarrative`/`publicAcceptanceIntent` (redactados) entran al payload. Es ESTRUCTURAL (siempre corre)
  y NO depende del detector DEF-PII inexistente (TASK-0118 proposed). Coherente con DECISION-0040.
- **NOTA (honestidad, no bloqueante):** la redaccion es **basada en PATRONES (best-effort), NO una garantia
  de cero-PII**. PII de tercero que no case esos patrones (nombre de persona, direccion, email, telefono,
  un NIT sin el prefijo literal "NIT") **pasaria** al plano publicable. NO sobre-afirmar "el plano publicado
  es PII-free": declarar que es redaccion best-effort + advertencia al operador, y que **DEF-PII (TASK-0118)
  sigue siendo el gate** real para citabilidad/publicacion. La UI no debe mostrar un sello "PII-free
  garantizado".

---

## 7) NEUTRALIDAD  ->  PASA

- El mecanismo (firmar-en-nombre-de por un firmante pinned + author/relayed_by/origin) es GENERICO: no mete
  dominio/negocio en el nucleo. El contenido (nova.budget) entra como DATO (campo `project`), no como logica
  de dominio. `type:"requirement"` y los campos de relay son conceptos de protocolo neutrales. DECISION-0052
  mantiene `directLedgerWrites:false` y un solo writer. Sin reglas fiscales en el core. PASA.

---

## RESUMEN (para la ratificacion del operador y la SPEC del Arquitecto)
| # | Veredicto | Lo critico |
|---|-----------|-----------|
| 1 | CAMBIO CRITICO | superficie de impersonacion (actorId cliente/default Arquitecto + intents arbitrarios) YA en canonico; acotar relay + prueba negativa |
| 2 | PASA + cambio | atribucion honesta en payload; falta test de RENDER (firmante=Arquitecto, no verde "Operador firmo") |
| 3 | CAMBIO | relayed vs endorsed first-class; semantica "firma = origen+transporte, no aval"; sin lavado |
| 4 | PASA + cambio | relay no toca #4 (correcto); pero asertar genesis/keys/version byte-identicos, no solo drift 0 |
| 5 | PASA fuerte + cambio | AC15 happy-path real; exigir write REAL (no mock) + CI permanente |
| 6 | PASA + nota | redaccion estructural real; NO es cero-PII garantizado (patron best-effort); DEF-PII sigue el gate |
| 7 | PASA | mecanismo generico, neutralidad intacta |

## Que NO hice
- No diseno la UI, no autoro la SPEC, no promovi, no mute estado. Ancle en canonico (git show fc31bfe /
  Zeus-protocol 42e7931), no en working tree. No corri el write (read-only adversarial sobre drafts+codigo).
- Recomiendo NO ratificar hasta cerrar #1 y #3 (los demas cambios pueden ir en la SPEC/TASK-0134).
