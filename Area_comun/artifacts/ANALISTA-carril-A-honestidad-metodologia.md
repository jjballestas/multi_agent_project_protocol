# ANALISTA - Carril A (A1/A2/A3) - lente HONESTIDAD Y METODOLOGIA

> Voz: Analista (independiente, checker). Firma: Analista. Fecha: 2026-06-19.
> Insumo: personal/Arquitecto/carril_A/ (5 drafts; autor Arquitecto). Modo: read-only, no muto estado.
> maker != checker: verifique por mi cuenta config viva, DECISION-0029, estados de tarea, el contenido
> real del event log y los scans disponibles. NO consolido, NO decido, NO promuevo.

## Veredicto de cabecera

- **A1 (DECISION-0039 + SPEC-0081, activacion #4):** APROBABLE con 2 cambios (1 factual duro, 1 de
  alcance del termino "seguridad"). El encuadre "activacion, no rediseno" es HONESTO y verificado.
- **A2 (DECISION-0040, GATE-DATASET):** OBJECION CONCRETA. La respuesta a "el esquema de dos planos
  garantiza CERO PII de terceros en el event log" es **NO como esta escrito**: el event log YA contiene
  texto libre (payloads de task upsert) y NO existe scan de PII. La garantia es disciplinaria, no
  estructural, y el detector que el draft invoca no detecta PII. Ademas la base legal (Cons.26) esta
  mal aplicada y omite al unico humano del dataset. Corregible; no es fatal.
- **A3 (DECISION-0041, precondicion read-only):** APROBABLE. La precondicion es verificable y honesta;
  1 cambio menor para que "verificable" sea falsable (no quede en juicio del dueno).
- **Transversal:** el corte limpio es HONESTO (no retrofit). Regla 3.4: A1/A2 las jala una necesidad
  real con fecha; A3 es precondicion de A2, no pieza autonoma. Riesgo meta-proyecto BAJO. 1 nota.

---

## A1 - Activacion #4 (DECISION-0039 + SPEC-0081)

### PASA (verificado por mi)
- **Encuadre "activacion, no rediseno" = honesto.** DECISION-0029 existe y difiere el encendido con
  texto literal: "su encendido exige SPEC cerrada + golden cases verdes + aprobacion explicita
  posterior del operador" (DECISION-0029-firmantes-cruzados.md L19-20). A1 cita esto fielmente y NO
  re-decide la politica. Correcto referenciar, no duplicar.
- **Estado OFF verificado.** protocol.config.json -> event_state: chain_enabled=false,
  agent_signatures_enabled=false, anchor_enabled=false, signature_config.public_keys={}. enforce=true,
  authoritative=true. TASK-0101/0102/0103/0113 = done en TASK_INDEX.json. El draft describe la realidad.
- **Off -> piloto -> on es honesto.** El gate (AC2 >=99% sobre runs legitimos + AC3 prueba negativa +
  AC5 rollback ensayado byte-equivalente + AC6 goldens verdes) ANTES de ON cumple "no encender antes de
  golden verdes". El piloto corre sobre el PROPIO protocolo, no sobre el modulo-app (SPEC-0081 pipeline
  paso 3) -> separa "instrumento sano" de "dato de tesis". Metodologicamente limpio.
- **Modelo de amenaza A1-A4 vs escritor unico = SI lo cubre, honestamente.** A3-restringido nombra
  explicitamente "reescritura por el RUNTIME (escritor unico) de historia ya anclada" y lo cubre con
  anclaje externo fuera de su control de escritura, declarando el riesgo residual (ventana entre ultimo
  evento y ancla) en vez de afirmarlo cubierto. A4 (operador malicioso) declarado FUERA DE ALCANCE sin
  fingir cobertura. Esto es exactamente lo que pide la lente de honestidad: cada afirmacion cita su clase
  y lo no cubierto se nombra.

### CAMBIO REQUERIDO 1 (CORREGIDO - mi afirmacion original era imprecisa)
**RETRACTACION (honestidad, maker!=checker aplicado a mi):** mi primera version dijo "event_auth.enabled
NO existe". Es FALSO. Solo mire bajo `event_state`. Verificado de nuevo: `event_auth` SI existe como
clave **TOP-LEVEL** de protocol.config.json con `enabled: false, method: hmac-sha256, issuer:
local-runtime, audience: runtime-event-log`. El draft (que lo trata como flag en false) es CORRECTO; el
equivocado era yo.
- Falsable: `python -c "import json;print(json.load(open('protocol.config.json',encoding='utf-8-sig'))['event_auth'])"` -> {'enabled': False, ...}.
- **Lo que SOBREVIVE como cambio real (provisioning, no "flag inexistente"):** encender
  `event_auth.enabled=true` sin claves HMAC provisionadas (`event_auth.keys`) hace fallar `append_event`
  por "signing key missing"; e igual `anchor_enabled=true` con `anchor_config.remote_url=""` falla al
  primer anclaje. Accion: SPEC-0081 debe exigir provisioning de claves HMAC + remoto/proof de anclaje
  ANTES del piloto, como precondicion del encendido. (Esto converge con la objecion 1-2 de Codex.)

### CAMBIO REQUERIDO 2 (alcance del termino, honestidad semantica)
**El manipulation-check >=99% es propiedad de CALIDAD DE INSTRUMENTO, no propiedad de SEGURIDAD.** Tal
como esta definido en SPEC-0081 AC2 (tasa de atestaciones bien formadas y verificables sobre runs
LEGITIMOS), mide salud del instrumento en ausencia de adversario; NO mide resistencia al adversario.
- La propiedad de SEGURIDAD real es AC3 (prueba negativa: una atestacion forjada/alterada A1/A2 DEBE ser
  rechazada). Esa es binaria, no un umbral del 99%.
- Por tanto NO es cosmetica - PERO solo si AC3 es bloqueante igual que AC2. Riesgo de honestidad: un
  lector concluye ">=99% => seguro". 99% de bien-formadas con AC3 debil seria cosmetico.
- Accion: declarar explicitamente que (a) AC2 mide salud (sin adversario) y AC3 mide seguridad (con
  adversario); (b) AC3 es condicion de encendido tan dura como AC2; (c) el 99% NO es una afirmacion de
  seguridad. Y precisar AC3: hoy dice "RECHAZA con diagnostico de clase" pero NO fija cobertura minima
  de vectores (al menos: alteracion puntual, borrado, insercion, reordenamiento, firma con llave no
  registrada, atribucion cruzada) ni que cada uno sea golden REPRODUCIBLE con exit-code. Sin eso, "prueba
  negativa pasa" es no-falsable.

### RIESGO DECLARADO
- AC2 fija N>=20 "sugerido" y deja el denominador ("atestaciones que DEBERIAN existir") a definir. Si el
  denominador lo fija el mismo codigo que produce el numerador, el 99% es auto-cumplido. El denominador
  debe derivarse de una fuente INDEPENDIENTE del firmante (p.ej. el conteo de eventos autoria-relevantes
  del event log, no lo que el firmante decidio firmar). Nombrarlo en la SPEC.

---

## A2 - GATE-DATASET (DECISION-0040)  [OBJECION CONCRETA]

### PASA
- **Corte limpio + dos planos como direccion = correcto.** No reimportar la migracion, dataset = la
  coordinacion, payload por hash: la direccion es la adecuada y consistente con DECISION-0033.
- **Honestidad sobre el seudonimo:** el draft dice que subject_hash es "seudonimo y re-identificable (no
  anonimo)". Eso es honesto y correcto (coincide con mi pasada #3 previa). Bien no llamarlo anonimo.

### CAMBIO REQUERIDO 1 (la objecion central - responde a tu pregunta)
**"CERO texto libre / CERO PII en el event log" es FALSO como propiedad estructural HOY.** Verificado
sobre runtime/state/events.jsonl (538 eventos): el payload de `task` upsert contiene campos de TEXTO
LIBRE (`deliverables`, `file`, y por esquema `title`/`description`/`notes`). Ejemplo real recogido:
`deliverables: ["runtime/state/events.jsonl (2 intent.applied de actor Codex: auto-claim + handoff-release)", ...]`.
- Es decir: el event log YA almacena descripciones escritas por humano/agente. Un NIT, una razon social
  o un dato de tercero escrito por error en un `deliverables`/`title`/`description`/handoff/mailbox
  quedaria registrado VERBATIM en events.jsonl. El sujeto va por hash; el PREDICADO/metadato no.
- Y **no existe ningun scan de PII**: scripts/ solo tiene scan_encoding (encoding/ASCII) y
  scan_domain_neutrality (terminos de dominio). Un NIT es ASCII y no es termino de trading -> NINGUN gate
  actual lo detecta. La frase de DECISION-0040 sec.4 "el scan de canal/encoding ... detecta fugas" es
  incorrecta: el encoding scan detecta encoding, no PII.
- Conclusion: la garantia "CERO PII de terceros en el event log" es **disciplinaria + regla de boundary
  (DECISION-0018), NO estructural, y NO instrumentada**. Eso no la invalida, pero el draft la presenta
  como garantia. Sobre-afirmacion.
- Accion (falsable): (a) acotar la garantia ESTRUCTURAL a lo que es estructural - el SUJETO por hash; (b)
  para los campos de texto libre del payload (deliverables/title/description) y para handoffs/mailbox,
  declarar honestamente que es control DISCIPLINARIO; (c) si se quiere garantia real, anadir un
  detector de PII/patrones (p.ej. regex de NIT colombiano / secuencias numericas de tercero) como gate, o
  declarar el riesgo residual explicitamente; (d) borrar/corregir la afirmacion de que el encoding scan
  detecta fugas de PII.

### CAMBIO REQUERIDO 2 (base legal mal aplicada)
**RGPD Cons.26 esta citado al reves.** Cons.26 dice que los datos SEUDONIMIZADOS siguen siendo datos
personales (DENTRO del ambito); solo los ANONIMOS quedan fuera. El draft admite que el hash es
seudonimo y re-identificable y aun asi lo invoca para sacar el dato "fuera del ambito" - eso es
justo lo que Cons.26 NIEGA para seudonimos.
- La base legal REAL y solida es OTRA: el dataset no contiene datos personales de PERSONAS FISICAS
  (PII de terceros excluida por dos planos; actores = ids de agente NO humano, que no son personas
  fisicas y por tanto fuera de Ley 1581/RGPD). Esa es la linea de carga; Cons.26 sobra o va por analogia.
- Accion: reformular la base legal sobre "ausencia de datos de persona fisica en el dataset", no sobre
  "Cons.26 anonimiza el seudonimo".

### CAMBIO REQUERIDO 3 (omite al unico humano del dataset)
La DPIA-lite y la regla "actores = solo agentes no humanos" **omiten al operador humano**, que SI
aparece en el dataset de coordinacion (las DECISIONs lo nombran como `deciders: [operador humano]`; da
los GO). Es la unica persona fisica en el corpus.
- Accion: tratar explicitamente al operador como (a) investigador/responsable del tratamiento que
  consiente sobre sus propios datos, y/o (b) presente solo como ETIQUETA DE ROL ("operador humano"), no
  como nombre/identificador directo. Sin esto, "cero PII / actores no humanos" es incompleto y un revisor
  institucional (GATE-INST) lo marcaria. Declararlo ahora preserva la honestidad del gate.

### RIESGO DECLARADO
- Tabla `maco009t` = 10.676 entidades con NIT: es INSUMO del brief del operador, NO verificable por mi
  (DB privada, no la abro). Lo tomo como afirmado, no confirmado.
- "instrumentacion interna licita sin consentimiento por evento" depende ENTERAMENTE de que CR1 se
  cumpla de verdad (cero PII real en el log). Si CR1 no se endurece, la premisa legal se cae. Encadenadas.

---

## A3 - Precondicion read-only (DECISION-0041)

### PASA
- **Encuadre "referencia DECISION-0035, no la redecide" = correcto** (mismo patron honesto que A1 vs
  DECISION-0029). DECISION-0035 existe; el satelite es repo SEPARADO read-only. Consistente con mi pasada
  previa sobre DECISION-0035 (read-only sostenido por diseno, no sandbox).
- **Honestidad del estado actual:** sec. Contexto admite que hoy la garantia es "sostenida por diseno,
  NO sandboxed ... convencional, no forzada". No sobre-afirma. Bien.
- **La precondicion es real y con dueno:** enforcement read-only REAL (montaje/clon read-only o identidad
  sin escritura) ANTES de lectura viva, dueno Codex (§9), no se cae en silencio. Responde a "verificable
  antes de lectura viva": SI, el control (montaje read-only / identidad sin escritura) es objetivamente
  comprobable, no una asercion.

### CAMBIO REQUERIDO (menor, para que "verificable" sea falsable)
sec.2 pide a Codex "confirmar que no existe ruta de escritura ... es revision sustantiva, no match de
patron" - correcto que el grep es evadible, pero asi queda como JUICIO del dueno, no como prueba
reproducible. Anadir al menos UN criterio objetivo y registrable:
- evidencia del montaje/identidad read-only (p.ej. el proceso del satelite corre bajo cuenta sin permiso
  de escritura al path del Core, demostrado con un intento de escritura que el SO RECHAZA -> prueba
  negativa, analoga a AC3 de A1), registrada en la tarea.
Asi "verificado por Codex" no descansa solo en su lectura del codigo.

### RIESGO DECLARADO
- A3 NO tiene necesidad-con-fecha PROPIA: solo muerde cuando se franquee GATE-DATASET para #2/#3 o el
  harness (eventos futuros, sin fecha). Es honesto que el propio draft lo diga ("precondicion del
  franqueo, no de la estructura") -> NO es meta-proyecto: es una condicion latente barata de declarar
  ahora. Pero NO debe promoverse como si habilitara trabajo inmediato; es un guard para cuando llegue.

---

## Transversal (regla 3.4 / corte limpio / meta-proyecto)

- **Corte limpio HONESTO, no retrofit.** A1 sec. Alternativas descarta explicitamente "retrofitear
  atestacion al historial previo" como imposible/deshonesto y por eso T0 = primer handoff del modulo-app.
  La restriccion de orden DURA (#4 ON antes del primer handoff, no retrofiteable) es una propiedad
  criptografica real (cadena prev_hash), no una excusa. Aprobado.
- **Regla 3.4 (cada pieza la jala una necesidad real con fecha):**
  - A1: SI - instrumentar el modulo-app (dataset = coordinacion). Necesidad con fecha.
  - A2: SI - el modulo-app toca DB con PII de terceros; el gate es condicion para capturar licitamente.
  - A3: NO directamente (precondicion latente de A2). Aceptable como guard declarado, no como trabajo
    activo. Riesgo meta-proyecto BAJO siempre que no se le asignen tareas de implementacion ahora.
- **Una sola pieza que vigilar (meta-proyecto):** el conjunto A1+A2+A3+SPEC introduce 3 decisiones + 1
  spec para una activacion de mecanismo YA construido. Proporcionado SI el resultado es encender #4 y
  capturar el dataset; desproporcionado si genera mas harness que dato. Recomiendo que SPEC-0081 fije N y
  el alcance del piloto de forma ACOTADA (no "instrumento perpetuo") - coherente con mi principio rector:
  metas de la medicion propia, no de un harness que se auto-justifica.

## Sintesis de cambios (para el Arquitecto, si el operador da GO a revisar)

| # | Draft | Tipo | Cambio falsable |
|---|-------|------|-----------------|
| 1 | A1/SPEC-0081 | provisioning (CR1 corregido) | event_auth SI existe top-level (enabled=false); el cambio real: exigir provisioning de claves HMAC + remoto de anclaje antes del piloto (encender sin ellos hace fallar append_event/anchor) |
| 2 | A1/SPEC AC2/AC3 | honestidad semantica | 99% = salud, NO seguridad; AC3 binaria, bloqueante, vectores+goldens fijados |
| 3 | A1/SPEC AC2 | metodologia | denominador del 99% derivado de fuente independiente del firmante |
| 4 | A2 sec.1+sec.4 | OBJECION central | "CERO PII estructural" falso (payload task = texto libre; no hay scan PII); acotar a sujeto-por-hash + declarar control disciplinario / anadir detector |
| 5 | A2 sec.2 | base legal | Cons.26 mal aplicado; fundar en "no hay persona fisica", no en seudonimo-fuera-de-ambito |
| 6 | A2 DPIA-lite | completitud | tratar al operador humano (unica persona fisica del corpus) |
| 7 | A3 sec.2 | falsabilidad | anadir prueba negativa objetiva (intento de escritura rechazado por el SO) registrada |

## Que NO hice (a proposito)
- No promovi nada, no encendi flags, no toque state/*.json ni protocol.config.json.
- No lei las otras voces (Codex) antes de producir la mia (maker != checker).
- No abri la DB de Budget (insumo privado): maco009t/10.676 NITs tomados como afirmados, no confirmados.
- No consolido ni decido: estos son CAMBIOS para el Arquitecto y el operador; el GO es del operador.
