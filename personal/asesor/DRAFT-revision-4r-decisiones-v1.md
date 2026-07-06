# DRAFT (DEBATE) - Adopcion de patrones 4R (gentle-ai) en la metodologia Sistema-Agentes

> ESTADO: DRAFT de debate en area del Asesor. NO ruteado, NO sellado, NO gobernado. Sin commitear al
> ledger. Para revision del operador + asesor. Sale de "debate" solo con orden explicita del operador.
> Fuente del material: personal/operador/Revision/ (6 archivos gentle-ai/gentle-pi, Alan Buscaglia; MIT +
> judgment-day Apache-2.0). Descargo de correlacion al pie (regla 5, obligatorio).
> Marco receptor: leer junto a [[gentle-ai-ecosystem-benchmark]] (estamos por delante en claims/atestacion/
> gates; judgment-day y envelope SDD siguen vigentes) y [[pivote-publicar-para-ser-citado]].

## Marco de honestidad (mi carril me obliga)
La metodologia receptora YA implementa versiones ATESTADAS y con GATE DURO de varios de estos patrones
(checker formal atestado, maker!=checker, evidencia obligatoria via F-NOVA-01, pre-registro, ledger #4 con
submit_intent). El ejercicio NO es "adoptar por primera vez" la mayoria de estos patrones, sino: (a) ver
donde el 4R aporta ESTRUCTURA que aun no tenemos formalizada, (b) donde CONVERGE con lo nuestro (validacion
de diseno por terceros), y (c) que es publicable como contribucion diferencial. Evito vender como adopcion
lo que ya hacemos igual o mejor.

---

# FASE A - Extraccion independiente (patron / mecanismo / instancia no transferible / analogo / riesgo)

### A1. review-risk.md (R1 Risk)
1. **Patron:** lente read-only de seguridad que solo REPORTA (no arregla), con reglas tipadas Flag/Block/
   Require-evidence y carve-outs "Do not flag".
2. **Mecanismo:** separacion tajante detectar!=arreglar (`tools: Read, Grep, Glob, Bash`, "do not fix them",
   review-risk.md:9); reglas con VERBO DE ACCION explicito (Flag/Block/Require-evidence, :15-22); exigencia de
   evidencia concreta ("cite scan failure or vulnerable package, not just 'looks risky'", :22).
3. **No transferible tal cual:** el catalogo web (secrets hardcoded, authz solo-frontend, DOM sinks, cookies
   httpOnly/sameSite, React escaping; :15-21) y las fuentes-slide OWASP (:11).
4. **Analogo por dominio:** Auditoria_Seguridad = DIRECTO (es literalmente su lente). Desarrollo_DotNet =
   nuestro F-NOVA-01 guard de procedencia SQL + THROW ya ES una lente de riesgo (mas fuerte: corre contra el
   proc desplegado). Agents_Framework = escaneo ASCII/secrets/neutralidad-de-dominio.
5. **Riesgo si se adopta mal:** duplicar como "lente nueva" lo que F-NOVA-01 ya hace atestado -> perder la
   atestacion por copiar una version advisory mas debil.

### A2. review-readability.md (R2 Readability)
1. **Patron:** lente read-only de mantenibilidad/intencion con carve-out anti-falso-positivo.
2. **Mecanismo:** exige evidencia para reclamos subjetivos ("cite exact function, branch, or repeated
   pattern", :21); carve-out explicito ("Do not flag a small helper... clear, local, self-explanatory", :22).
3. **No transferible:** code-smells web/React/hooks (:15-20), fuentes-slide (:11).
4. **Analogo:** los tres dominios (claridad de artefactos/handoffs); en nuestra metodologia mapea a la regla
   de "handoffs autocontenidos" y "narracion minima" (DECISION-0038) mas que a codigo.
5. **Riesgo:** legibilidad es el eje mas subjetivo -> sin la disciplina "cita evidencia exacta" degenera en
   opinion; adoptar la regla SIN su carve-out genera ruido.

### A3. review-reliability.md (R3 Reliability)
1. **Patron:** lente read-only de tests orientados a COMPORTAMIENTO + determinismo + contratos.
2. **Mecanismo:** Block sobre cambio-de-comportamiento sin test de contrato visible (:15); exigir determinismo
   "same input -> same output; external dependencies mocked or controlled" (:20); Block si CI pasa con
   `test.only` (:18).
3. **No transferible:** husky/forbidOnly, Playwright, selectores UI (:18,:21), fuentes-slide.
4. **Analogo:** Desarrollo_DotNet = DIRECTO (nuestros gates dotnet/arch-tests/F-NOVA-01 GWT). El determinismo
   ES nuestra tesis (study_metrics.py determinista con golden). Auditoria_Seguridad = repetibilidad de PoC.
5. **Riesgo:** el hallazgo #12 (TASK-0255, sin test HTTP con gateway falso) muestra que nuestra cobertura de
   contrato NO es uniforme -> adoptar la REGLA sin el checklist por-endpoint no cierra el hueco.

### A4. review-resilience.md (R4 Resilience)
1. **Patron:** lente read-only operacional (fallbacks/retry/observabilidad/rollback/SLO) con umbrales-ancla.
2. **Mecanismo:** UMBRALES NUMERICOS como ancla de decision ("test success <95%, prod error >1% investigate,
   >2% emergency, >5% all hands", :16); exigir camino de recuperacion concreto (:18).
3. **No transferible:** Sentry, budgets de performance percibida, los umbrales web especificos (:11,:16).
4. **Analogo:** Desarrollo_DotNet = OpenTelemetry/SLOs (ya en el roadmap P6.3). Agents_Framework = watchdogs,
   lease, rollback de submit_intent, SLA del gate (48h/gracia 72h del sello). Auditoria_Seguridad = menor.
5. **Riesgo:** copiar los umbrales web (95%/1%/2%) sin recalibrarlos a nuestra realidad medida = numeros
   sin sentido (nosotros MEDIMOS tokens/latencia real, podemos anclar umbrales verdaderos, no de slide).

### A5. trigger-rules.md (politica de activacion)
1. **Patron:** politica DECLARATIVA de activacion (evento x glob x tamano-diff -> conjunto de agentes x
   fuerza) con MODELO DE COSTE en 3 tiers, renderizada como texto e inyectada; el orquestador decide.
2. **Mecanismo:** tiers de coste explicitos (Tier1 ~1x advisory; Tier2 ~4x en hot-paths/diff>400; Tier3
   ~4+3xfindings para judgment-day post-SDD; :50-63); estatus "organic recommendations, NOT hard gates...
   gentle-ai never fires, blocks, or executes" (:11,:19); vocabulario de eventos (pre-commit/pre-pr/post-sdd-
   phase/on-ci/on-schedule) con bindings dejados abiertos para override (:65).
3. **No transferible:** la tabla de rutas de inyeccion por-herramienta (:31-44), los globs web (auth/payments).
4. **Analogo:** Agents_Framework = DIRECTO como formalizacion de CUANDO corre cada checker. Los tres dominios
   podrian compartir el mismo vocabulario de eventos + tiers de coste.
5. **Riesgo (CENTRAL):** su filosofia "recomendacion organica, NO gate duro" es OPUESTA a nuestro enforce
   atestado (B.3 hard-gate, single-writer). Adoptar el FRAMING advisory debilitaria la garantia que nos
   diferencia. Se adopta el MODELO DE COSTE-POR-TIER; se RECHAZA el "no-gate".

### A6. judgment-day-SKILL.md (revision adversarial dual y ciega)
1. **Patron:** dos jueces CIEGOS en paralelo + sintesis por cubos de acuerdo + re-juicio tras fixes +
   escalada terminal a humano.
2. **Mecanismo:** "two blind judges in parallel... never review the code yourself" (:18); esperar AMBOS antes
   de sintetizar (:19); taxonomia de acuerdo confirmado/sospechoso/contradiccion/INFO (:31-33, :41); triaje
   real-vs-teorico de warnings ("WARNING (real) only if normal intended use can trigger them", :19); re-lanzar
   ambos jueces tras CADA fix (:21); estados terminales solo APPROVED|ESCALATED (:22); tope de 2 iteraciones
   -> preguntar al humano (:23); diversificacion de modelo por juez (referenciada, H4).
3. **No transferible:** poco; es casi todo patron. Detalle de instancia = triggers en espanol "juzgar" (:3).
4. **Analogo:** los tres dominios. Ataca DIRECTO nuestro problema abierto (revisores LLM correlacionados).
   Nuestro maker!=checker ya separa roles; judgment-day anade dual-JUEZ + ciego + re-juicio + diversificacion.
5. **Riesgo:** dos jueces del MISMO proveedor siguen correlacionados (limite declarado en H4) -> NO sustituye
   al experto humano pendiente; venderlo como "resuelto" seria sobreventa.

---

# FASE B - Hipotesis contrastadas (veredicto / evidencia / esfuerzo / dominio piloto / riesgo)

- **H1 (descomposicion en lentes) -> MODIFICAR.** Evidencia: review-*.md:9 (4 lentes read-only ortogonales),
  contrato Flag/Block/Require-evidence. Nuestro Agente_Verificacion PUEDE descomponerse en lentes por dominio,
  PERO no como copia: la lente de riesgo ya existe atestada (F-NOVA-01), y anadir lentes debe respetar el
  coste medido. Esfuerzo M. Piloto: Auditoria_Seguridad (fit natural de R1/R4). Riesgo: proliferacion de
  lentes sin tier de coste -> inflacion de tokens en un estudio que MIDE tokens.
- **H2 (contrato de salida uniforme) -> CONFIRMAR (con mapeo).** Evidencia: "severity: BLOCKER|CRITICAL|
  WARNING|SUGGESTION", evidencia obligatoria, cadena EXACTA `No findings.` (review-risk.md:26). Adoptable
  como contrato de mensajes file-based (mejora parseo maquina + senal-limpia deterministica). Esfuerzo S.
  Riesgo: no reemplazar a ciegas nuestra taxonomia; MAPEAR (nuestro blocker/critico) y fijar la cadena-limpia
  canonica. Converge con nuestra evidencia-obligatoria ya vigente.
- **H3 (trigger-rules como politica publicable) -> MODIFICAR.** Evidencia: 3 tiers de coste (trigger-rules.md
  :50-63) + "organic recommendation, not hard gate" (:11). El MODELO DE COSTE-POR-TIER es formalizable y
  publicable; el FRAMING advisory se RECHAZA (choca con enforce atestado). Nuestra ventaja: podemos poner
  costes REALES (medimos tokens), no estimados de slide. Esfuerzo M. Piloto: Agents_Framework. Riesgo: si se
  adopta el "no-gate", se pierde el diferenciador de atestacion.
- **H4 (taxonomia de acuerdo de judgment-day) -> CONFIRMAR (con limite declarado).** Evidencia: cubos
  confirmado/sospechoso/contradiccion/INFO (judgment-day:31-33,41), triaje real/teorico (:19), re-juicio
  (:21), escalada terminal (:22). Responde al problema de revisores correlacionados SIN sustituir al humano.
  Esfuerzo M. Piloto: cualquier checker de dominio (empezar Desarrollo_DotNet, donde ya tenemos el adversarial
  informal). Riesgo/LIMITE: 2 jueces mismo proveedor = correlacion residual; obligatorio declararlo y mantener
  el experto humano pendiente. Es la adopcion de MAS valor (ataca nuestro gap abierto).
- **H5 (resolucion centralizada de skills) -> CONFIRMAR (per-dominio, no unificado).** Evidencia: "Resolve
  project skills before launching agents... inject the same block into both judge prompts" (judgment-day:16);
  degradacion reportada explicitamente. Adoptable como regla POR DOMINIO (cada coordinador de dominio resuelve
  e inyecta), compatible con la ausencia de orquestador unificado. Esfuerzo S-M. Riesgo: si se enmarca como
  UN orquestador global -> va a DIFERIR (regla 6); enmarcado per-dominio, se adopta.
- **H6 (4R con proveniencia criptografica) -> CONFIRMAR como CONTRIBUCION DIFERENCIAL (requiere juicio
  humano).** Evidencia: donde las 4R citan slides de curso como fuente de criterio (review-*.md:11), nosotros
  podemos citar estandares verificables y EMITIR cada hallazgo como atestacion DSSE/in-toto anclada (Rekor y/o
  nuestro #4). Ya tenemos ledger #4 + submit_intent + sha256 -> el MVP es corto: emitir UN hallazgo de review
  como atestacion firmada y verificable. Esfuerzo L (infra Sigstore/Rekor real). Es el nucleo del rail
  "publish to be cited". DECISION HUMANA (estrategica/reputacional, regla 4).

### Emergentes (no cubiertos por H1-H6)
- **H7 (emergente) -> CONFIRMAR.** Carve-outs "Do not flag when..." explicitos por lente (review-risk.md:21,
  readability:22, reliability:22, resilience:21). Patron reusable: cada gate DECLARA su supresion de falsos-
  positivos -> el alcance/punto-ciego del gate queda AUDITABLE. Conecta con mi EVIDENCIA-VIVA A2 (un gate
  estrecho tiene punto ciego; declararlo lo vuelve auditable). Publicable como "gate scope auditable".
  Esfuerzo S.
- **H8 (emergente) -> CONFIRMAR como CONVERGENCIA (no adopcion).** "Require-evidence" como categoria de regla
  de primera clase (review-risk.md:22, readability:21, reliability:20/23, resilience:18/22). YA lo hacemos
  (F-NOVA-01 procedencia). Vale como evidencia de que nuestro diseno evidencia-obligatoria es un patron
  reconocido de forma independiente -> se CITA como convergencia, no se adopta de nuevo.

---

# FASE C - Matriz de decision (PROPUESTA, pendiente de ratificacion operador+asesor)

| Patron | Evidencia (archivo:linea) | Decision propuesta | Justificacion (C1-C6) | Piloto | Esf. | Riesgo | Juicio humano? |
|---|---|---|---|---|---|---|---|
| H1 Lentes ortogonales read-only | review-*.md:9 | **Adaptar** | C1 ok (file-based); C2 ok; C3 exige tier de coste; C6 medio (3 dominios) | Auditoria_Seguridad | M | proliferacion/coste | No (diseno) |
| H2 Contrato de salida (severidad+evidencia+`No findings.`) | review-risk.md:26 | **Adoptar** (con mapeo) | C1 ok; C4 mejora trazabilidad/parseo; C5 menor | transversal | S | reemplazo ciego de taxonomia | No |
| H3 Trigger-rules: modelo de coste-por-tier | trigger-rules.md:50-63 | **Adaptar** (coste si, advisory no) | C2 CLAVE: rechazar "no-gate"; C3 fuerte (costes reales medidos); C5 alto (publicable) | Agents_Framework | M | perder atestacion si se vuelve advisory | Si (framing) |
| H4 Judgment-day: dual-juez ciego + cubos + re-juicio | judgment-day:18-23,31-41 | **Adaptar** | C1 ok; ataca gap de correlacion; C4 ok; C5 alto | DotNet | M | correlacion residual mismo-proveedor | Si (limite) |
| H5 Resolucion de skills per-dominio | judgment-day:16 | **Adaptar** (per-dominio) | C1 ok; C2 ok si NO unificado | transversal | S-M | deriva a orquestador global | No |
| H6 Proveniencia criptografica de hallazgos | review-*.md:11 vs nuestro #4 | **Adoptar** (contribucion diferencial) | C4 nucleo; C5 nucleo del rail | Auditoria_Seguridad | L | sobre-alcance/infra | SI |
| H7 Carve-outs "Do not flag" auditables | review-risk.md:21 (+3) | **Adoptar** | C4 gate-scope auditable; C5 medio | transversal | S | ninguno mayor | No |
| H8 Require-evidence (convergencia) | review-risk.md:22 (+3) | **Rechazar-como-adopcion / Citar** | ya vigente (F-NOVA-01) | n/a | - | doble-implementar | No |
| Instancia web (OWASP/React/husky/Sentry/globs) | review-*.md:11-21 | **Rechazar** | fuera de dominio (regla 3) | n/a | - | - | No |
| Framing "no hard gate" para dominios enforce | trigger-rules.md:11 | **Rechazar** | choca con enforce atestado (C2) | n/a | - | debilita garantia | Si |

## Backlog priorizado (max 3, primer paso <=1 dia)
1. **H2 contrato de salida** - primer paso: escribir un `REVIEW-CONTRACT.md` (draft en mi area) que fije
   severidad canonica (mapeo a la nuestra) + evidencia obligatoria + cadena limpia exacta. 1 dia. Barato,
   habilita H1/H4.
2. **H4 judgment-day (piloto de 1 juez-dual)** - primer paso: correr el adversarial informal EXISTENTE como
   DOS jueces ciegos en paralelo sobre un target ya cerrado (p.ej. re-juzgar TASK-0255) y comparar contra el
   GO informal de 1 pasada. Mide si el dual-ciego caza algo que el single no. 1 dia. Genera evidencia para
   EVIDENCIA-VIVA y para el rail de publicacion.
3. **H6 MVP de proveniencia** - primer paso: emitir UN hallazgo (p.ej. #10/50212) como atestacion DSSE
   minima anclada en nuestro #4 (ya existe submit_intent+sha256), documentando el mapeo hallazgo->atestacion.
   1 dia de spike. Es el nucleo diferencial; el resto (Rekor/Sigstore) es fase posterior.

## Anti-alcance explicito (tan vinculante como lo adoptado)
- NO se adopta el catalogo web/frontend (OWASP/React/husky/Sentry/globs auth-payments). Instancia, no patron.
- NO se adopta el framing "recomendacion organica, no gate" para los dominios en modo enforce atestado.
- NO se introduce un orquestador unificado por adoptar H5 (regla 6): la resolucion de skills es per-dominio.
- NO se copian los umbrales numericos web (95%/1%/2%) sin recalibrar a costes/latencias REALMENTE medidos.
- NO se trata judgment-day como sustituto del experto humano pendiente (correlacion residual declarada).

## Preguntas abiertas para el experto humano de dominio (no resolver aqui)
1. Diversificar modelo entre los dos jueces, reduce la correlacion de forma material, o el termino dominante
   es la correlacion de MISMA FAMILIA (mismo corpus de entrenamiento)? (define el valor real de H4).
2. Emitir hallazgos de review como atestaciones DSSE/in-toto/Rekor, es contribucion novedosa citable o
   incremento marginal sobre in-toto existente? (riesgo academico, regla 4).
3. Adoptar la ESTRUCTURA 4R (lentes con nombre), fortalece o DILUYE nuestra narrativa de "checker formal
   atestado unico" de cara a publicacion? (posicionamiento).

## Impacto en el rail "publish to be cited"
- **Se cita como trabajo relacionado:** el framework 4R / gentle-pi de Buscaglia (MIT), la skill judgment-day
  (Apache-2.0, derivacion con atribucion permitida), y el gate-por-fase SDD.
- **Contribucion propia diferencial:** proveniencia ATESTADA del criterio Y de los hallazgos (DSSE/in-toto/
  Rekor + ledger #4), gate PRE-REGISTRADO, coste REALMENTE MEDIDO (tokens, no estimado de slide) y la guarda
  de FALSABILIDAD (F-NOVA-01). Donde 4R es advisory + fuente-slide, lo nuestro es enforce + fuente-estandar +
  medido + falsable. H6 + H3(coste) + H7(gate auditable) son el paquete diferencial.

---

---

# RESOLUCIONES DEL DEBATE (operador, ronda 2) + H4 refinado

## R1 - Independencia DISJUNTA-DEL-MAKER (resuelve la pregunta abierta 1)
El operador confirma: diversificar modelo reduce la correlacion MATERIALMENTE. Insight clave del operador:
como el MAKER es Codex (familia OpenAI), un juez OpenAI estaria PARCIALIZADO CON EL MAKER -- comparte
corpus/familia, luego comparte los puntos ciegos del maker, luego tenderia a rubber-stampear los errores de
CLASE-MAKER. Esto es una amenaza DISTINTA y peor que la correlacion juez-juez: es correlacion JUEZ-MAKER,
que ataca la independencia del checker respecto de LO REVISADO (no solo la redundancia entre revisores).

**Principio de diseno (candidato a sellar):** familia(juez) != familia(maker) [disjuncion-del-maker], y
ademas jueces diversos entre si. Jerarquia de configuraciones:
- **Config actual:** maker=Codex(OpenAI), checker=Claude(Anthropic) -> YA cross-family; con 1 juez ya cumple
  disjuncion-del-maker. Ya supera el default de gentle-ai (que no restringe la familia del juez).
- **Dual 2xClaude:** maker-disjunto (ambos no-OpenAI) pero juez-juez correlacionado. Barato, SIN infra nueva.
  Suficiente para el piloto dual-blind (backlog #2).
- **Dual Claude+Gemini:** maker-disjunto AND juez-diverso. MAXIMA independencia, citable. Requiere 2o modelo
  frontera.
- **Claude+OpenAI: PROHIBIDO mientras Codex sea maker** (el juez OpenAI = maker-correlacionado). Descarta la
  opcion naive de "meter un juez OpenAI".

**"Necesitamos 2 modelos frontera?" (recomendacion):**
- Rutina / tier-bajo: 1 checker cross-family (Claude) BASTA.
- Piloto dual-blind: 2 Claude (maker-disjunto, sin infra nueva) -> mide si el dual-ciego caza algo que el
  single no, antes de invertir en un 2o proveedor.
- **Grado-publicacion (claim de independencia): SI, 2 familias no-maker (Claude+Gemini)** -> responde de
  frente a "sus revisores estaban correlacionados". Es la config que blinda el paper.
- Tiered por coste (ata con H3): solo los gates de alto riesgo pagan el panel completo; medimos los tokens.

**Contribucion diferencial vs judgment-day:** gentle-ai dice "diversify model" (referenciado en H4) pero SIN
la restriccion de disjuncion-del-maker. Nosotros la FORMALIZAMOS: independencia operacionalizada como
familia-juez disjunta de familia-maker. Extension citable, no copia.

**RESOLUCION operador (ronda 3): la INFRA de multi-proveedor NO se aplica ahora.** No se introduce un 2o
modelo frontera a mitad del experimento (cambiar el setup contamina lo medido; misma linea roja que ultracode-
prohibido en la ventana). En consecuencia:
- El principio de disjuncion-del-maker (familia-juez != familia-maker) se REGISTRA como diseno sellable, NO
  se opera ahora. Condicion de desbloqueo: post-ventana-medida (post-30-jul) o un experimento aparte.
- El claim de independencia grado-publicacion (Claude+Gemini) va a DIFERIR con esa condicion.
- La pata de independencia que SI tenemos hoy (maker=Codex vs checker=Claude, cross-family) se mantiene, mas
  el experto humano pendiente como la pata NO-LLM. Eso ya supera el default de gentle-ai sin tocar el setup.

## R2 - DSSE/in-toto/Rekor = contribucion novedosa (confirma pregunta 2)
Eje de novedad a declarar: in-toto/DSSE hoy atestan pasos de BUILD/cadena-de-suministro (quien construyo
que). Aplicarlos a la CAPA DE REVISION -- atestar "este juicio de calidad lo emitio ESTE revisor atestado
contra ESTE criterio atestado" -- es una aplicacion novedosa. Combinado con nuestro #4 pre-registrado =
"gobernanza atestada de la revision misma", no solo del artefacto. Ese es el nucleo citable de H6.

## R3 - Adoptar PARTE de la estructura 4R fortalece (confirma pregunta 3)
La palabra clave es PARTE. Delimitacion:
- **Se adopta como PRESENTACION / on-ramp (fortalece legibilidad):** el vocabulario de lentes ortogonales con
  nombre (H1) + el contrato de salida (H2) + los carve-outs auditables (H7). Da a nuestro "checker formal" una
  ESTRUCTURA reconocible que un revisor externo mapea rapido.
- **Se mantiene como TITULAR / diferencial (no se subordina a Buscaglia):** gate DURO atestado + proveniencia
  criptografica (H6) + independencia disjunta-del-maker (R1). 
- **Narrativa resultante:** "lentes estilo-4R, pero atestadas + con proveniencia + disjuntas-del-maker --
  donde 4R es advisory + fuente-slide + agnostico-de-proveedor, lo nuestro es enforce + fuente-estandar +
  medido + falsable + independiente-del-maker." El 4R es la rampa de acceso; la atestacion es la tesis.

## R4 - Las 4R COMO TECNICA ya las aplicamos (resolucion operador: separar tecnica de infra)
El operador separa dos cosas que yo habia mezclado: la INFRA (paneles multi-juez, 2o modelo frontera) NO se
toca ahora; pero la TECNICA de las 4 lentes (evaluar risk / readability / reliability / resilience como ejes
ortogonales de revision) YA la aplicamos, distribuida por nuestros gates. Adoptar "la tecnica" = hacer
EXPLICITO y con NOMBRE lo que ya hacemos implicito, sin infra nueva y sin tocar el modelo.

**Mapa de lo que YA hacemos por lente (con traza):**
| Lente 4R | Ya lo hacemos (traza) | Lo que falta = formalizar (no cambiar comportamiento) |
|---|---|---|
| R1 Risk | F-NOVA-01 guard de procedencia SQL + sets de THROW reales (b8f3855); scan ASCII/secrets; scan de neutralidad-de-dominio; los hallazgos #10 (50212) y #11 (default silencioso) son catches de lente-riesgo | ponerle nombre "R1" + contrato de salida |
| R2 Readability | handoffs autocontenidos; narracion minima (DECISION-0038); disciplina ASCII; menos formalizado en codigo de producto | carve-outs "do not flag" explicitos |
| R3 Reliability | gates dotnet/arch-tests; F-NOVA-01 GWT (8 casos versionados); determinismo (study_metrics.py con golden); el hallazgo #12 (sin test HTTP) es un gap de lente-fiabilidad ya detectado | checklist de contrato por-endpoint |
| R4 Resilience | watchdogs, lease, rollback de submit_intent, SLA del gate (48h + gracia 72h del sello), OpenTelemetry (P6.3), revival de sesion sin perdida (EVIDENCIA A7) | anclar umbrales a costes/latencias REALMENTE medidos |

**Frontera fina (mi carril me obliga a marcarla):** DESCRIBIR/NOMBRAR nuestras lentes existentes = pura
documentacion, segura en cualquier momento y fortalece el paper. CAMBIAR el COMPORTAMIENTO del gate (p.ej.
partir la ejecucion en 4 sub-agentes-lente que emitan veredictos distintos) = eso SI es un cambio del brazo
gobernado (el tratamiento) -> respeta la ventana sellada (aplicar post-30-jul). Regla: la tecnica-como-
presentacion se adopta ya; la tecnica-como-cambio-de-ejecucion se difiere a Sprint 1.

## Delta a la matriz tras el debate
- H4: Adaptar -> Adaptar CON regla de disjuncion-del-maker (familia-juez != familia-maker); "juez OpenAI"
  prohibido mientras Codex sea maker. Juicio humano pendiente pasa de "vale la diversificacion?" a "grado-
  publicacion necesita 2a familia no-maker (Gemini), o basta 2xClaude para el piloto?" (coste vs claim).
- H6: Adoptar -> Adoptar como CONTRIBUCION PRINCIPAL del rail; eje de novedad = atestar la capa de revision.
- H1/H2/H7: refuerzan la narrativa de publicacion (on-ramp), no la diluyen (confirmado).

---

# CONTRATO DE SALIDA R1-R4 (draft) - sobre lo que YA emiten nuestros checkers

Principio: NO cambiar lo que el checker evalua; solo ETIQUETAR con lente + fijar un contrato uniforme +
preservar nuestros campos atestados (que el 4R no tiene). Es presentacion, no cambio de comportamiento.

## Cabecera del veredicto (por revision)
```
## REVIEW -- {target} -- round {n}
reviewer_role: maker | adversarial_informal | checker_formal | judge
provider_family: anthropic            # traza para disjuncion-del-maker
maker_family: openai                  # familia de lo revisado (Codex)
lenses_run: [R1, R3]                  # COBERTURA explicita (que lentes corrieron; el resto = no evaluado)
verdict: GO | NOGO | ESCALATE
```

## Por hallazgo
```
- id: "#N"                            # numeracion del backlog QA/seguridad del hub (ya la usamos: #1..#13)
  lens: R1 | R2 | R3 | R4             # eje 4R (etiqueta nueva sobre el hallazgo existente)
  severity: BLOCKER | CRITICAL | WARNING | SUGGESTION
  blocking: true | false             # nuestro eje bloqueante-vs-quality-data (mapea a severity)
  files: ["path:line", ...]          # evidencia exacta OBLIGATORIA (ya lo exigimos)
  evidence: "que se observo y CONTRA QUE FUENTE (proc desplegado / OBJECT_DEFINITION / clon limpio)"
  why: "por que importa"
  corrective_criterion: "fix-forward horneable en SPEC"   # CAMPO NUESTRO (4R no lo tiene)
  attestation: "sha256 | #4 seq | NA"                     # CAMPO NUESTRO: proveniencia
```

## Cadena limpia canonica (nuestra version de `No findings.`)
- Por lente: `R{n}: No findings.`
- Global: `REVIEW CLEAN -- no findings across [R1,R2,R3,R4].`
(Cadena EXACTA y deterministica -> parseable por el runtime file-based, como la de gentle-ai.)

## Mapa de severidad (nuestro eje <-> taxonomia 4R)
| 4R severity | Nuestro significado | blocking | Ejemplo real |
|---|---|---|---|
| BLOCKER | rompe el gate, NOGO | true | guard SQL bypasseable (TASK-0252 NOGO del Analista) |
| CRITICAL | correctness con impacto, condicionado | true/false | (ninguno abierto ahora) |
| WARNING | no-bloqueante, quality-data del baseline | false | #11/#12/#13 |
| SUGGESTION | mejora opcional | false | refactors menores |

## Carve-outs por lente (H7, "do not flag") -- hacen AUDITABLE el punto ciego
- **R1:** no flag terminos de dominio dentro de `profiles/` (solo el core debe ser neutral); no flag secretos
  en `*.template.*` de ejemplo declarados.
- **R3:** no flag `tokens=NA` sellado como degradacion (err.log volatil, ya declarado); no flag ausencia de
  test donde el contrato es spec_prepagado.
- **R4:** no flag latencia de tareas pesadas conocidas (e2e/harness 35+min legitimo; leccion watchdog falso-jam).
- **R2:** no flag un helper local claro y autoexplicativo.

## Ejemplo REAL: los hallazgos vigentes re-emitidos en el contrato
```
## REVIEW -- TASK-0255 (PAR-2 baseline) -- round 2 (pasada transversal)
reviewer_role: adversarial_informal ; provider_family: anthropic ; maker_family: openai
lenses_run: [R1, R3] ; verdict: GO (con quality-data no-bloqueante)

- id: "#10" ; lens: R3 ; severity: WARNING ; blocking: false
  files: ["src/NOVA.Api/Program.cs:500", "src/NOVA.Api/Program.cs:513"]
  evidence: "switch compartido mapea 50212 a RN-A01; apropiacion (RN-01) ya no lo lista -> etiqueta cruzada"
  why: "businessRule/titulo mal atribuidos entre superficies; HTTP 409 y sqlErrorNumber crudos OK"
  corrective_criterion: "separar 50212 en rama neutral o duplicar el caso; horneado a decidir"
  attestation: "registrado hallazgo #10 (a2657d5), veredicto Analista pendiente"

- id: "#11" ; lens: R3 ; severity: WARNING ; blocking: false
  files: ["SqlAvailabilityCertificateAnnulmentGateway.cs:54-64", "AnnulAvailabilityCertificateEvidenceTests.cs:380,390"]
  evidence: "lectura con fallback de columnas + default silencioso 'A'; el arnes lee otra columna directa + JOIN a catalogo -> produccion no verificada contra el proc desplegado"
  why: "el API puede reportar state='A'/reversalId=null en silencio si el result-set difiere"
  corrective_criterion: "restriccion 6i en SPEC-NOVA-P4-006: leer columna confirmada vs OBJECT_DEFINITION, sin default silencioso"
  attestation: "horneado en SPEC-NOVA-P4-006 (df6b4c9); veredicto Analista pendiente"

- id: "#13" ; lens: R1 ; severity: WARNING ; blocking: false
  files: ["tests/NOVA.ArchitectureTests/LayeringTests.cs:73-75", "apps/nova-web/src/App.tsx:180,370"]
  evidence: "la lista de aislamiento del frontend omite Annul_Availability_Certificate; App.tsx contiene el literal"
  why: "rompe el patron de aislamiento de las 2 tareas previas; leak nulo pero guard debilitado"
  corrective_criterion: "restriccion 6k: incluir el proc en la lista o documentar la excepcion + etiqueta neutral"
  attestation: "horneado en SPEC-NOVA-P4-006 (df6b4c9)"

# R2 y R4 no corrieron sobre esta unidad -> lenses_run declara la cobertura, no se finge.
R2: not run. R4: not run.
```

**Lectura del ejemplo:** los hallazgos reales caen en R1/R3 -> el contrato HACE VISIBLE que R2/R4 no se
ejercieron en esta unidad (honestidad de cobertura). Los campos `corrective_criterion` y `attestation` son
justo el diferencial que el contrato 4R original no lleva: convierten un "finding" en un hallazgo GOBERNADO
CON PROVENIENCIA y fix-forward. Ese es el puente natural hacia H6 (cada linea `attestation` puede pasar de
un ref #4 a una atestacion DSSE/in-toto).

---

# DISPARO NATURAL DE LENTES PARA TODOS LOS AGENTES (R2/R4 dejan de ser decorativas)

## El problema
Hoy los hallazgos caen en R1/R3 porque esas lentes tienen disparador natural (SQL/seguridad -> R1;
tests/contrato -> R3). R2/R4 no se disparan solas -> el #10 (acople del switch compartido, senal R2) se cazo
por una pasada transversal AFORTUNADA, no por un trigger. Si el disparador vive en el PROMPT de cada agente,
se cae bajo carga y cada agente lo aplica distinto. Falla de raiz.

## El mecanismo: la lente requerida vive en el ARTEFACTO, no en el agente
`lenses_required` es un CAMPO de la tarea/handoff, COMPUTADO deterministicamente de las senales del diff, y
lo honra CUALQUIER agente que toque la tarea (maker Codex, checker adversarial, checker_formal Analista,
juez). El artefacto viaja; el requisito de cobertura viaja con el. Ningun agente decide "si mira R4": si la
tarea toca runtime, `lenses_required` incluye R4 y el gate lo exige.

Cierre del lazo con el contrato de salida: la tarea declara `lenses_required`; el revisor emite `lenses_run`.
**Gate de cobertura: `lenses_run` DEBE cubrir `lenses_required`; si no, el gate falla por cobertura
incompleta** (no por hallazgo). Eso es lo que impide saltarse R2/R4 en silencio -> deja de ser decorativa.

## Tabla de disparo (senal observable -> lente). NEUTRAL = vocabulario; INSTANCIA = globs
| Senal natural (observable en el diff/evento) | Dispara | Capa |
|---|---|---|
| toca proc mutador / SQL / auth / secretos / neutralidad-del-core | R1 Risk | glob = instancia; regla = neutral |
| toca un COMPONENTE COMPARTIDO por >=2 verticales (switch, DTO, mapper, clase base) | **R2** (acople/duplicacion) + R1 (aislamiento) | neutral (es acople, no dominio) |
| CAMBIA comportamiento observable / anade endpoint / cambia contrato | R3 Reliability | neutral |
| toca runtime / error-mapping / retry / rollback / observabilidad / un mutador NUEVO que corre en prod | **R4** Resilience | neutral |
| evento pre-handoff (GO/REVIEW al peer) | R1+R3 minimo | neutral |
| evento post-SDD design/apply | judgment-day (dual-juez) | neutral (H3 tier-3) |

## Los disparadores naturales de R2/R4 que hoy faltan (el foco de tu pedido)
- **R2 se dispara cuando el diff toca un COMPONENTE COMPARTIDO por >=2 verticales.** Es una senal de acople,
  puramente estructural (grep de "este archivo/simbolo lo referencian >=2 modulos"), NO de dominio -> vive en
  el core neutral. Habria cazado el #10/50212 por diseno, no por suerte.
- **R4 se dispara cuando el diff anade/cambia una superficie que CORRERA EN PRODUCCION** (endpoint nuevo,
  mutador nuevo, cambio en error-mapping/retry/rollback/observabilidad). Pregunta obligada de R4: fallback?
  rollback? visibilidad? Es lo que un review de solo-correctness (R1/R3) no pregunta.

## Reparto por rol -- "para todos los agentes que intervengan"
- **Maker (Codex):** AUTO-declara `lenses_run` en su handoff sobre las `lenses_required` de su tarea (auto-
  chequeo, no auto-verificacion: no da veredicto, solo declara cobertura).
- **Checker (adversarial / Analista):** CORRE las `lenses_required` y emite el contrato de salida; su gate
  falla si `lenses_run` no cubre.
- **Juez (judgment-day):** hereda el mismo bloque de lentes inyectado (H5, resolucion de skills per-dominio).
- **Coordinador de dominio (no orquestador unificado):** computa `lenses_required` de las senales del diff y
  lo estampa en la tarea. Per-dominio, compatible con la regla de no-orquestador-unificado.

## Caveats (mi carril me obliga)
1. **Cambio de COMPORTAMIENTO del gate** (anadir computo de `lenses_required` + check de cobertura) = cambio
   del brazo gobernado -> se DISENA ahora (debate), se APLICA post-30-jul (respeta la ventana sellada). Lo que
   SI es seguro ya: nombrar/declarar lentes en los reportes (presentacion).
2. **Neutralidad de dominio:** el vocabulario de lentes/eventos y la regla "componente-compartido -> R2" son
   NEUTRALES (van al core); los globs de instancia (proc mutador, DbsFinanciero) van al PROFILE de la
   instancia (DECISION-0002 core/profiles). No contaminar el core con terminos Nova.
3. Coste: cada lente extra son tokens; el disparo debe ser TIERED (H3) -> R4 no corre en un diff de solo-docs.

---

## DESCARGO DE CORRELACION (regla 5, literal)
Esta sesion es en si misma una revision LLM: mis conclusiones cuentan como opinion CORRELACIONADA, no como
validacion independiente. No sustituye la revision del experto humano de dominio pendiente.
