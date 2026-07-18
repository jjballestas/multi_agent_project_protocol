# MANUAL DE OPERACION: delegacion a peones locales (draft; sintesis del piloto 18-jul)

Estado: DRAFT pre-cierre de T4 (slot 7b-T4 pendiente). Fuente: piloto privado del grid
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
2. **La amortizacion es real y tiene dos palancas**: reuso de spec (gap +102 -> +24 en lote
   10) y escala (gap +24 -> +8.4 en lote 50). Marginales: delegado ~956/u vs directo ~1180/u
   -> **break-even EXTRAPOLADO ~99 unidades/exec** (2 puntos, proxy 3b: INDICATIVO).
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
- Economia: con lote < ~100u el objetivo es DESCARGA del maker (coste neutro o leve
  sobrecoste frontier); con lote >= ~100u/exec ademas AHORRA frontier (EXTRAPOLADO ~99u,
  pendiente confirmacion lote-100 PARQUEADA por el operador).
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

## 7. Pendientes declarados
- Lote-100 confirmatorio: GO del operador (decision 2, cambia el parqueo); EN EJECUCION
  (TASK-0014, ambos brazos, protocolo identico a 10/50). El break-even con 3 puntos sustituye
  la extrapolacion de 2 en la seccion 2 al cerrar.
- B2 triage: SKIP DECLARADO confirmado por el operador (decision 1).
- Celda opcional sanitizador: decision del Arquitecto POST-brazos del lote-100 (etiquetada
  aparte, fuera de la comparabilidad del confirmatorio).
- Todo numero: 1 corrida, hardware unico, no citable; un estudio sellado multi-maquina
  pre-registrado seria el 3er brazo (decision futura del operador).
