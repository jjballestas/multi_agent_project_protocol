# MANUAL DE OPERACION: delegacion a peones locales (v1.3; serie completa: piloto + QC-barato + estructural + techo de entrega, 18-jul)

Estado: v1.0 FINAL (piloto completo: grid 17 celdas + afinado + confirmatorio lote-100). Fuente: piloto privado del grid
(TASK-0006..0012, instancia Nova-Payroll). TODO NUMERO ES INDICATIVO (1 corrida por celda,
demo NO citable, anti-HARKing); las extrapolaciones van marcadas. Proposito: manual operativo
para delegar peones en el desarrollo NOVA (directiva del operador 85dabfc). Instrumento
maker: Codex CLI; maquina: Core 7 250H / 64GB / RTX 5060 8GB / Ollama 0.32.0 (peones en VRAM).

## 1. La tabla completa del grid (tokens frontier del exec; MEDIDO)
| Tier | Celda | Frontier | Peon / QC |
|---|---|---:|---|
| T1 lote 10 patron puro | A directo | 84121 | - |
| | B0 spec fresca 7b | 169881 | 10/10, 1 llamada, 0 corr |
| | B1 extractivo 7b | 279172 | 0/10 (3 llamadas) -> REFUTADO; contaminado por blocker (declarado) |
| | B0-reuse 3b | 104108 | 10/10, 0 corr, 15.7s |
| | B0-reuse 6.7b | 141598 | semantico 10/10, 10 normalizaciones cosmeticas; incluye cierre |
| T2 variacion media | baseline | 105539 | incluye autorar gate 18 asserts |
| | 7b B0 (spec Codex ~500tk) | 123782 | 1 correccion real |
| | 3b B0-reuse | 104432 | 1 correccion real; QUEDA BAJO baseline |
| | 6.7b B0-reuse | 142456 | 1 correccion; incluye cierre |
| ESCALA lote 50 | directo | 131340 | 2627/u |
| | delegado 7b B0-reuse+bounce | 142341 | 2847/u; 5 bounces DESLIZ (1 feedback 22tk x5), 0 techo, 0 corr |
| T3 contrato+juicio | baseline | 119418 | incluye autorar gate 29 asserts |
| | 7b (spec Arq ~440tk) | 112109 | 2 bounces -> TECHO estrecho; 1 corr minima |
| | 3b (spec Arq) | 117117 | idem 7b |
| | 6.7b (spec Arq) | 133837 | PASS con 1 bounce, 0 corr (unico); incluye cierre |
| T4 logica dura | baseline | 100459 | incluye autorar gate 20 asserts |
| | 7b (spec Arq ~295tk) | 112348 | LA LOGICA PASO EL GATE EN LLAMADA 1 (Kahn lexicografico completo); fallos = solo fences Markdown; bounce oscilo -> techo FORMAL de entrega, no de logica; correccion sin tocar codigo |

## 2. Los cuatro hallazgos (MEDIDO salvo donde se marca)
1. **La spec calibrada es la condicion de rendimiento del peon** (B1 la quito y el peon
   colapso 0/10; B0/B0-reuse la dan y el peon rinde 10/10 en T1).
2. **La amortizacion es real pero NO cruza (MEDIDO con 3 puntos por brazo)**: el gap cae
   +102 (spec fresca, lote 10) -> +24 (spec sunk, lote 10) -> +8.4 (lote 50) -> +7.1 (lote
   100) y ahi CONVERGE: ambas curvas se aplanan (directo 84121/131340/129921; delegado
   104108/142341/139195) porque el envelope del exec domina y el maker frontier escribe o
   revisa 100 unidades casi al precio de 50. **La extrapolacion break-even ~99u quedo
   REFUTADA por el punto confirmatorio: no hay cruce; el premium delegado converge a
   ~+7 por ciento (~9k tokens) constante.** El caso de negocio de delegar es DESCARGA y
   paralelismo del maker (y wall-clock local barato), no ahorro neto de frontier, bajo este
   protocolo e instrumento.
3. **QC-bounce con triaje funciona**: en zona apta, bounces de ~20-40tk sustituyen
   correcciones caras (escala: 5/5 con el mismo feedback); en zona techo, el triaje detecta
   el techo cuando el bounce 2 reintroduce defectos (T3 qwen) y la correccion directa cierra.
   Cero fallos catastroficos (estructura inventada) con specs parametros-antes-del-ejemplo.
4. **El techo es por FIT modelo-familia, no por tamano**: qwen clava patron puro (T1) y toca
   techo estrecho en T3; deepseek al reves (ruido de formato en T1, PASS por bounce en T3).
   El peon mas BARATO capaz por familia es el optimo (3b gano T1 y empato T2).

## 3. EL ENVELOPE (cuando delegar sale a cuenta; receta operativa)
Delegar a peon SOLO si (rubric v0.2, los 5 filtros + estas condiciones economicas):
- Familia REPETIDA con spec escrita UNA vez (peon-ready: parametros/datos ANTES del ejemplo,
  reglas numeradas cerradas, un ejemplo minimo) -> added-spec marginal ~0 en instancias 2..N.
- Gate objetivo DURO pre-congelado (tests/asserts por exit-code) que juzga la salida.
- QC-bounce tope 2 con triaje desliz-vs-techo (feedback minimo concreto; techo -> no quemar
  bounces).
- Peon elegido por FIT de familia: patron puro/formato -> qwen (3b basta); logica compuesta
  -> deepseek 6.7b. (INDICATIVO: 1 corrida por celda.)
- Economia (MEDIDA a 3 puntos): delegar cuesta un premium frontier pequeno y ~constante
  (~+7 por ciento a escala) que NO desaparece con el lote; lo que compra es DESCARGA del
  maker + paralelismo + ejecucion local barata. Delegar por capacidad, no por ahorro de
  tokens. (Si el coste del envelope del exec bajara, el premium relativo subiria: revisar
  si cambia el instrumento.)
- Filtro 5 SIEMPRE duro: PII real / ledger / genesis / seguridad / codigo soberano NUNCA al
  peon, aunque pudiera.

## 4. EL TECHO (que se queda en frontier)
- Diseno abierto, tradeoffs, intencion no dicha (falla filtro 1).
- Correccion subjetiva sin gate mecanico (falla filtro 2; el QC no se puede enganar solo).
- Cross-file / contexto amplio (filtro 3).
- One-off novel (filtro 4: la spec no amortiza; el riesgo de calibracion domina).
- Soberano/catastrofico (filtro 5).
- T4 (logica dura multi-paso): SLOT PENDIENTE; prediccion ex-ante = techo.
- Matiz medido en T3: el techo del peon con buena spec es ESTRECHO (fallos locales), no
  catastrofico -> en zona frontera el patron bounce+correccion-minima sigue siendo viable si
  el gate es duro; lo que NO es viable es delegar sin spec calibrada (B1).

## 5. SI-ENTONCES para enrutar tareas reales de NOVA
- SI tarea = N-esima instancia de familia con spec existente Y gate duro -> PEON (el mas
  barato capaz de la familia), QC-bounce tope 2.
- SI tarea = familia nueva pero mecanica-especificable Y habra >=3 instancias -> AUTORAR spec
  peon-ready (Arquitecto, ~300-500tk) + celda piloto 1 instancia; si pasa, PEON para el resto.
- SI variacion media (T2/T3-like) con gate duro -> PEON como BORRADOR + presupuestar 1
  correccion del maker; elegir peon por fit; no esperar ahorro frontier, si descarga.
- SI diseno/tradeoffs/cross-file/one-off/subjetivo -> CODEX directo.
- SI PII/ledger/genesis/seguridad -> CODEX (o Arquitecto), SIN excepcion.
- SIEMPRE: registrar decision ex-ante + resultado en el rubric (tasa de acierto viva).

## 6. Afinado contra el prior art (directiva 91a0897; MEDIDO)
- **Bounce-cap 2 vs 3 (TASK-0013, re-run controlado sha-identico): NO RECUPERA.** El bounce 3
  reparo unas propiedades y fallo otras; el techo persistio y la correccion del maker siguio
  haciendo falta. Coste del cap3: +1 llamada, +6s, frontier 140445 vs 112109 (+25 por ciento).
  **Tope 2 VALIDADO empiricamente para este protocolo** (divergencia del prior-art justificada
  con dato propio).
- **Gate = scorer (FrugalGPT): VERIFICADO.** Patron uniforme en la evidencia cruda: integrar
  sin tocar -> gate exit -> triaje; Codex nunca re-juzga el pass/fail. MATIZ: la conformidad
  de DATOS (escala) no era gateable y la cazo lectura QC -> fix al protocolo: derivar asserts
  de conformidad del bloque de datos (devuelve esa dimension al scorer barato).
- **Sanitizador mecanico pre-gate (hallazgo T4)**: strip de fences/prosa antes del gate
  (coste ~0). Con el, el peon habria pasado T4 en llamada 1 y parte de T3; ademas evitaria
  parte de los bounces de formato que el cap3 no recupera. AL PROTOCOLO del manual.

## 7. Cierre y decisiones declaradas
- Lote-100 confirmatorio: EJECUTADO (TASK-0014; veredicto NO-CRUCE incorporado en s.2/s.3).
  Tabla lote 100: directo 129921 (1299/u) vs delegado 139195 (1392/u); QC-bounce 5/5
  deslices de naming recuperados con 1 bounce de 22tk c/u, 0 techo, 0 correcciones.
- B2 triage: SKIP DECLARADO confirmado por el operador.
- Celda opcional sanitizador: SKIP DECLARADO por el Arquitecto tras el confirmatorio: con
  NO-CRUCE establecido y los deslices de formato recuperados por bounces de ~22tk, medirla
  no cambiaria ninguna decision de enrutado; el sanitizador queda como RECOMENDACION de
  protocolo (s.6) sin celda propia.
- Todo numero: 1 corrida por celda, hardware unico, demo privada NO citable; un estudio
  sellado multi-maquina pre-registrado seria el 3er brazo (decision futura del operador).
- Piloto cerrado en canonico: TASK-0006..0014 done (9 tareas, 19 celdas + afinado,
  ~2.6M tokens frontier de medicion + ceremonia).

## 8. Variante QC-barato (post-piloto, 18-jul; MEDIDO -- v1.1)

> ESTADO: RECOMENDACION tecnica avalada por el Asesor (ACK 18-jul), NO adoptada. La
> adopcion formal en el flujo NOVA es decision SOBERANA del operador (la delegacion al
> Asesor cubria el diseno de la corrida, no la adopcion). Si el operador firma la
> adopcion, este estado pasa a ADOPTADO.

La celda "sanitizador" que la s.7 dejo como skip declarado SE MIDIO despues por DIRECTIVA
del operador (variante QC-barato, 3 condiciones + celda marginal; TASK-0015/0016/0017;
registro y sellos en la instancia Nova-Payroll). Hipotesis: el premium +7 pct era el QC
frontier; abaratando la verificacion podria cruzar a negativo. Resultado:

| condicion | frontier | vs directo 129921 |
|---|---:|---:|
| delegado sin sanitizador (referencia TASK-0014) | 139195 | +7.1 pct |
| delegado + sanitizador, steady-state (marginal, la MEDIDA) | 135171 | +4.0 pct |
| delegado + sanitizador + checker local deepseek (bruto c/setup) | 160535 | no comparable (confound declarado) |

1. **NO HAY CRUCE ni con QC abaratado.** El premium remanente +4.0 pct es el envelope
   frontier de orquestacion. Se confirma: delegar compra CAPACIDAD, no ahorro neto.
2. **SANITIZADOR MECANICO: SIEMPRE.** Determinista, 0 LLM, solo formato/entrega (fences,
   prosa, rename derivado del bloque de datos). Recorta el premium -3.1 puntos (robusto a
   una corrida con mas friccion del peon), elimina la clase entera de deslices de
   formato/naming (90-210 renames por corrida de 100u) y su setup es one-time amortizable
   (~6k chars de script AST). CAVEAT vigilado: la rama sin-fence puede truncar codigo si
   hay sentencias top-level tras las funciones (latente, no ejercido; la telemetria
   prose_stripped lo delata) -- endurecer antes de uso intensivo.
3. **CHECKER LOCAL LLM: NO** (en familias de conformidad de datos). deepseek-6.7b como
   pre-filtro: 0 true-positives; sus GO no predicen el gate (13/18 fallaron despues); sus
   NO-GO fueron espurios; el unico chequeo mecanico util (nombres) ya lo resuelve el
   sanitizador. Anadio 12 bounces de ruido y la convergencia la sostuvo la ESCALACION
   frontier (50 pct de bloques). El QC frontier va solo donde el gate falla (escalacion),
   que es el diseno que la condicion termino ejerciendo de facto.
4. **ECONOMIA DE BOUNCES (hallazgo del sello 0101):** con decode determinista, el bounce 2
   sobre prompt identico devuelve respuesta BYTE-IDENTICA: no aporta. Tope efectivo
   recomendado: 1 bounce + triaje, correccion directa al segundo fallo. (Refina el tope-2
   de s.6: el tope-2 sigue siendo el techo validado; el segundo intento solo tiene sentido
   si el bounce cambia el prompt.)
5. Disciplina que este tramo re-valido: pre-registro ex-ante + contabilidad simetrica
   pre-sello + confounds DECLARADOS (nunca particion post-hoc) + celda marginal para el
   steady-state; el sello independiente cazo ademas un lote de datos declarado "nuevo" que
   no lo era (enmienda declarativa registrada; fix de proceso: chequeo automatico de
   no-solape antes de declarar novedad de datos).

Todo NO citable (demo privada, 1 corrida por celda, hardware unico); mismas condiciones
de evidencia que el resto del manual.

## 9. El 4to brazo y el PORQUE unificador (18-jul; MEDIDO + clausura aritmetica -- v1.2)

Ultimo experimento de la serie: probar si el premium de delegar se INVIERTE cuando la
GENERACION frontier domina el coste (unidad pesada: motor de nomina sintetico, 50
funciones/250 asserts, gate objetivo duro, setup sellado limpio por el 0101 con 250/250
casos recomputados independientemente).

- Brazo DIRECTO medido: 137042 tokens frontier, gate 250/250 a la PRIMERA iteracion.
  La garantia de regimen pre-registrada (>=440k) FALLO por un orden de magnitud: la
  fraccion de generacion quedo en ~1.4-20 pct del exec (segun anclaje del envelope,
  ambos pre-declarados). Generar el motor completo le costo al frontier ~2k-27k tokens
  marginales sobre el envelope.
- Brazo delegado NO CORRIDO por decision registrada (Asesor, opcion A): el cruce quedo
  ARITMETICAMENTE DESCARTADO (el delegado tambien paga el envelope; su suelo ~135k ~ el
  directo 137k). No se reproduce lo determinado.

**VEREDICTO ESTRUCTURAL (la explicacion de toda la serie):** dentro de la CLASE DELEGABLE
(mecanicamente especificable + gate objetivo duro -- los filtros 1 y 2 del rubric), la
generacion frontier es INTRINSECAMENTE BARATA: la spec peon-ready es la parte cara, y una
vez existe, el frontier rellena patron+tabla a ~coste de lectura (escala sublinealmente:
50u costo ~lo mismo que 100 tests de juguete). El regimen dominado-por-generacion NO
EXISTE dentro de la clase delegable, y el premium de delegar no se invierte alli. Las
tareas caras de generar (logica compuesta profunda, diseno abierto) estan FUERA de la
clase delegable (techo de fit, s.4) y escalan al frontier de todos modos.

**UNIFICACION de la serie completa** (piloto NO-CRUCE +7pct -> QC-barato +4pct ->
4to brazo estructural): *los peones no reducen tokens frontier porque lo delegable es
barato de generar y lo caro no es delegable.* El valor de delegar es CAPACIDAD (descarga,
paralelismo, ejecucion local, atribucion) -- nunca ahorro neto de tokens. El envelope
frontier (spec una vez + orquestacion + sello) es el suelo de coste de CUALQUIER brazo,
y la generacion -- lo unico descargable -- nunca es la parte dominante dentro de la clase.

DIFERIDO declarado (pregunta abierta barata, no descartada): el techo de ENTREGA del
qwen-7b a escala ~50 funciones/una unidad (para dimensionar unidades de peon en NOVA).
Todo NO citable (demo privada; 1 corrida por celda, hardware unico).

## 10. Techo de ENTREGA del 7b, MEDIDO (rectificacion del operador, 18-jul -- v1.3)

El diferido de s.9 se midio por directiva (TASK-0020: pipeline delegado completo sobre la
misma spec/gate sellados; proposito redefinido a entrega, coste solo contexto).

- **La entrega estructural NO es el techo**: a bloques de 5 funciones por llamada, el 7b
  entrego 10/10 bloques completos, 50/50 funciones, 0 truncamientos (done_reason=stop en
  las 15 llamadas), 0 omisiones. El volumen del bloque no rompio nada.
- **EL TECHO REAL ES DE REPARACION (hallazgo del sello 0101, no declarado por el maker):**
  en 4 de los 5 bounces el peon devolvio codigo BYTE-IDENTICO al inicial PESE a llevar el
  feedback del gate en el prompt. El 7b no consume feedback correctivo en este envelope.
  Solo 1/5 (redondeo_bancario, desliz de formato) reparo de verdad.
- Causas raiz de las 4 familias escaladas (ninguna por volumen/contexto): disciplina de
  tipos float/round->float (3/5: "1000.0 != 1000"), off-by-one de indexacion (1),
  malinterpretacion de la forma del dato (1).
- Fraccion de calidad del modulo final: peon 30/50 funciones; maker 20/50 (reemplazo por
  bloque familiar, byte-identico a su brazo directo).
- Coste (CONTEXTO, el cruce sigue cerrado): 195603 vs directo 137042 (~+43 pct): las
  escalaciones con correccion son caras; coherente con el veredicto estructural s.9.

**REGLAS OPERATIVAS que salen de esta medicion (dimensionamiento para NOVA):**
1. Unidades de peon de hasta 5 funciones/bloque: entrega estructural fiable en el 7b
   (con sanitizador). No hay evidencia de techo de volumen en este rango.
2. **El bounce solo paga en deslices de FORMATO.** Para fallos de LOGICA/TIPOS, el 7b
   re-emite lo mismo: triaje directo a correccion del maker SIN quemar el bounce
   (refina el tope-1 de s.8: bounce solo si el triaje clasifica desliz-de-formato).
3. Deteccion mecanica de bounce-noop: comparar hash de la respuesta del bounce vs la
   inicial; si coinciden, registrar bounce-noop y escalar sin re-gate (ahorra 1 ciclo).
4. Spec para peones con aritmetica: declarar EXPLICITO "enteros, sin float, sin round()"
   con un ejemplo negativo (la clase de fallo dominante fue round()->float).
5. Gap de spec detectado por divergencia entre brazos (deduccion_tabla subdeterminada:
   floor vs round-nearest, ambos pasan el gate): los contratos de division DEBEN declarar
   el modo de redondeo; el sello por diff-entre-brazos caza estas subdeterminaciones.

Todo NO citable (demo privada, 1 corrida). Con esto la serie queda cerrada DEL TODO:
economia (s.9, estructural) + dimensionamiento (s.10, medido).
