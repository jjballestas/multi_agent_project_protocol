# DISCUSSION v2 -- Pivote "Publicar para ser citado" + Nova como motor de evidencia

Autor: Asesor del Operador (autoridad delegada por escrito). Fecha: 2026-07-02.
Para: revision ADVERSARIAL ronda 2 (Analista, via Arquitecto). SUPERSEDE la v1
(`DISCUSSION-pivote-publicar-para-ser-citado.md`, misma carpeta).

Insumos de esta version: (a) veredicto ronda 1 del Analista (CAMBIO-REQUERIDO,
`Area_comun/artifacts/ANALISTA-pivote-publicar-citado-veredicto.md`); (b) CINCO revisiones adversariales
externas encargadas por el Operador (ClaudeAI, Copilot, Gemini, OpenAI, ZAI -- `D:/Jball/data/
Adversarial_*.text`), todas CAMBIO-REQUERIDO, ninguna NO-GO; (c) NUEVA VISION del Operador (s.1.2);
(d) panel de diseno experimental de 5 agentes con verificacion adversarial interna (fixes F1-F7
incorporados). Esta v2 adopta TODAS las correcciones sostenidas y documenta cuales rechaza y por que.

---

## 1. Estado actual

### 1.1 Lo que existe (verificable)
- Hub `multi_agent_project_protocol`: metodologia de gobierno multi-agente dogfooded. 81+ decisiones,
  287+ tareas, ledger append-only con >3,100 eventos atestados (ed25519 + hash encadenado + genesis
  content-addressed), claims anti-colision, maker!=checker forzado con veredictos firmados, gates por
  exit-code, core neutral + templates + `new_instance` (instancia plantilla NOVA).
- Dataset sellado N=500 con hipotesis pre-registradas confirmadas BAJO EL HARNESS DEFINIDO (correccion
  ronda 1): deteccion de manipulacion 100% sobre 450 ataques inyectados, FP 0%, overhead estructural
  mediana 1.6ms / 0.42KB por evento, verificacion reproducible en clon limpio con claves publicas.
  **Que NO prueba (concesion adoptada 6/6):** es un validity check del esquema, no un security proof
  (no cubre colusion de firmantes, compromiso de claves, re-genesis malicioso aprobado por el operador,
  manipulacion pre-firma); no mide reduccion de defectos ni valor de negocio; N=1 operado por su autor.
- Panel web read-only propio (49 archivos) sobre ledger/mailbox/tareas. Fork Zeus-Aegis: DESCARTADO
  (decision del operador 2026-07-02; 1,094 archivos ajenos vs 13 propios).
- Costos reales declarados: fragilidad operativa historica (jams, zombies, fixes de drift) remediada en
  TASK-0235/0236/0237 + DECISION-0080 pero con tasa historica alta; overhead de PROCESO por tarea sin
  medir (8-15 eventos + varios execs LLM por tarea); el operador es hoy la raiz de confianza de todo el
  sistema (todas las claves, todos los prompts).

### 1.2 NUEVA VISION del Operador (cambia el marco de la v1)
1. **El "TFM" NO es formal**: era un analisis de si el trabajo podia formularse como TFM. Consecuencias:
   se DISUELVE el bloqueante de normas universitarias (angulo 9.8 v1, que 3 de 5 externos trataron como
   letal) y desaparece el envoltorio de credencial academica: el preprint debe sostenerse solo.
2. **Existe una empresa con empleados desarrolladores.** Objetivo de negocio real: construir la suite
   **Nova** (Budget primero; luego Accounting, Payroll, Treasury -- software financiero) usando la
   metodologia. El operador necesita la metodologia LISTA Y FUNCIONAL como herramienta interna:
   agentes coordinados + arranque en frio con BD (memoria hibrida) + doctrina de ingenieria
   (anti-vibecoding, gate de intake, excepciones auditadas) + peones + usable por empleados.
3. Si la metodologia ademas puede hacerse publica y convertirse en producto: deseable, pero SECUNDARIO.
4. El operador quiere MEDIR en Nova: que los peones reducen costo, que la metodologia reduce defectos,
   que el gobierno aumenta calidad; y pregunta si es factible un contraste modulo/sprint
   "gobierno ligero" vs "gobierno completo".

### 1.3 Implicacion central
Nova resuelve los DOS huecos que la ronda 1 dejo sin respuesta: **transferibilidad** (empleados != autor
operando el protocolo = transferencia interna, evidencia intermedia honesta; la externa sigue pendiente)
y **evidencia de valor de negocio** (defectos/retrabajo/costo medidos en desarrollo real). Ademas
resuelve la contradiccion de identidad que senalo ZAI: la identidad anti-vibecoding ("para
desarrolladores profesionales -- y para profesionalizar a quien construye software con IA sin serlo")
vive en el Carril A (practitioners: la empresa); el Carril B habla a estandares/auditoria. Dos
audiencias, dos vehiculos, una misma evidencia.

---

## 2. Que cambio desde la v1 (trazabilidad de correcciones)

| # | Hallazgo | Fuente | Cambio en v2 |
|---|---|---|---|
| 1 | **Hinds = nono = nolabs: la MISMA entidad.** El ancla de colaboracion es el CEO de la empresa que construye el competidor mas cercano, con funding, marca Sigstore y distribucion | ClaudeAI (letal) | s.3.2 reescrita; outreach redisenado (s.8.4); riesgo nuevo R6 "nolabs absorbe el diseno sin atribucion"; se elimina el framing "superset" (psicologica y tecnicamente erroneo) |
| 2 | El claim de unicidad amplio es FALSO a nivel academico: BlockA2A (ago-2025), Verifiability-First Agents (dic-2025), Ojewale et al. (ene-2026), Omega, IETF draft-sharif-agent-audit-trail, Agent Receipts (Asqav/nono/Pipelock/Microsoft AGT), sigstore-a2a, agent-sign | ClaudeAI + Analista | Claim estrecho unico (s.5 HP1'); related work obligatorio en el preprint; el diferencial es implementacion operativa + corpus real + pre-registro, NO campo vacio |
| 3 | ed25519 crudo con claves autogestionadas = infraestructura PARALELA al ecosistema Sigstore | ClaudeAI | **Interop DSSE/in-toto + anclaje periodico en Rekor = entregable tecnico central del Carril B** (desplaza al MCP server a meses 4-6); resuelve re-genesis + circularidad de confianza + convierte el pitch en "tu cadena, extendida, con datos" |
| 4 | HP5 (90 dias) cae 6/6: calendario fantasia; cuello real = calidad publica en ingles + embudo de decision del operador; extraccion de spec subestimada (posible refactor multi-mes) | 6/6 | Plan re-baselineado (s.8): Semana 0 bloqueante, fases con gates, "minimum public reference profile" en vez de spec completa, publicacion solo cuando un externo verifique en 5-10 comandos |
| 5 | Kill-criteria miscalibrados en ambos extremos | Analista + ClaudeAI + ZAI | Dos niveles (s.9): SENALES a 30/60/90 dias + DECISIONES a mes 6/9/12; metrica reina rebajada: 1 instancia externa O 1 piloto de auditora a mes 12; 2 a mes 18 |
| 6 | La demanda "compradora" esta sobreestimada: los auditores SOC2 se satisfacen con logs convencionales; el valor incremental de la atestacion criptografica se VENDE, no es pull | ZAI + Analista | "Comprador liquido" degradado a hipotesis comercial no validada (s.3.3) |
| 7 | Bloqueadores operativos no listados: endorsement de arXiv (cs.SE/cs.CR exigen endorser a autores nuevos); redaccion/PII del corpus antes de DOI inmutable; licencias dia 1 | ClaudeAI + Analista (A11) | Semana 0 (s.8.1) |
| 8 | El resultado modal del Carril B para una persona sola es capital de carrera, no empresa | ClaudeAI + ZAI | Aceptado sin eufemismos (s.9.4) -- y REPONDERADO: con Nova, el retorno principal ya no depende de adopcion externa |
| 9 | Ataques al TFM (normas universitarias como letal) | Gemini, Copilot, ZAI | MOOT: el TFM no es formal (s.1.2). Sobrevive solo la parte de endorsement arXiv y PII |
| 10 | Q3 confirmatoria via "retrabajo baja en el tiempo" es before/after confundido con aprendizaje | Panel medicion (F4) | Q3 degradada a descriptiva (s.7) |
| 11 | DER como metrica del contraste es matematicamente vacia en el brazo ligero (sin checker no hay "atrapados") | Panel medicion (F2) | Metrica primaria del contraste = escapes post-GO por tarea, intention-to-treat (s.7.3) |
| 12 | El nulo del contraste no estaba pre-decidido | Panel medicion | Pre-decision textual del nulo (s.7.5) |

---

## 3. Investigacion consolidada (rondas 1-2, fuentes verificadas)

### 3.1 Mercado
Los grandes convergen en control-plane sin evidencia criptografica: GitHub Agent Control Center
(session logs enlazados a commits, sin firmar), Anthropic (politicas/hooks/Compliance API), OpenAI
(RBAC/approvals), Antigravity (Artifacts sin firmar), Cursor (no loguea contenido de agentes).
Startups en dos clusteres (observabilidad/eval y gateways MCP) sin atestacion del ciclo. PERO la
categoria "recibos firmados de agentes" YA se mueve: nono.sh (Merkle+DSSE por sesion), Asqav, Pipelock,
Microsoft AGT, IETF draft-sharif-agent-audit-trail, sigstore-a2a, agent-sign. Y la academia ya publico
atestacion de flujos multi-agente (BlockA2A, Verifiability-First Agents, Ojewale et al., Omega).

### 3.2 El actor que importa: Luke Hinds / nolabs
Hinds (creador de Sigstore) publico el 21-ene-2026 la propuesta de extender SLSA/in-toto/Sigstore a
agentes (Plan/Generation/Approval attestations) con llamada explicita a colaborar. VERIFICADO. Y es,
A LA VEZ, el CEO de la empresa que construye nono -- el competidor mas cercano. Implicaciones adoptadas:
(a) el resultado por defecto de un outreach exitoso es que las ideas se materialicen como features de
nono, no como coautoria; (b) el framing correcto NO es "implemente un superset de tu taxonomia" sino
"tu cadena, extendida, con datos" -- via interop DSSE/in-toto/Rekor; (c) hay que decidir ANTES que se
le pide exactamente (opciones: PR de interop a nono, coautoria del profile multi-agente, item de agenda
en OpenSSF) y (d) el contacto se hace ANTES de escribir el preprint, como test barato de ventana
(propuesta ZAI): sin respuesta en 30 dias = senal, con respuesta = da forma al paper.
NIST CAISI (17-feb-2026): accountability chains como gap, 3 pilares permanentes; comment periods
CERRADOS (mar/abr-2026) -- es relacionamiento, no ventana garantizada (correccion del Analista).

### 3.3 Demanda (degradada a hipotesis comercial)
Presion real: SOC 2 CC8.1 / ISO 42001 piden atribucion y change-management del codigo generado por IA;
incidentes publicos (Replit borra DB de produccion y miente, jul-2025; wiper inyectado en Amazon Q a ~1M
devs, jul-2025); 93% de CTOs preocupados por codigo vibe-coded; Gartner $492M en 2026 para AI governance.
PERO (ZAI, sostenido): la mayoria de auditorias se satisface con logs convencionales + session id +
aprobacion humana. **Hipotesis comercial H-COM (no validada): existe un segmento (vendors auditados,
regulados) dispuesto a pagar por evidencia criptograficamente verificable por encima del logging
convencional.** El Carril B la explora; el Carril A no depende de ella.

---

## 4. La pregunta

Dado (a) una empresa que necesita la metodologia funcional para construir la suite Nova con empleados,
(b) un activo metodologico con evidencia estrecha pero real y una ventana de estandarizacion incierta y
ocupada por un actor dual (Hinds/nolabs), y (c) capacidad de UNA persona + agentes:
**cual es la secuencia que maximiza el valor conjunto (empresa + activo publico) sin que ninguno de los
dos carriles mate al otro, y que evidencia debe producir Nova para que el activo publico sea defendible?**

---

## 5. Hipotesis v2 (falsables; el revisor debe intentar refutarlas)

- **HP1' (activo, estrecho).** El activo diferencial INICIAL es: la unica implementacion de referencia
  OPERATIVA publicada del ciclo completo multi-agente (task->claim->delivery->review adversarial->close)
  con checker independiente, corpus longitudinal de uso real y mediciones pre-registradas, sin
  blockchain, compatible con agentes reales (Claude Code/Codex). NO se afirma "nadie atesta agentes"
  (falso), ni "moat" (es ventaja inicial). Refutacion: encontrar una implementacion operativa publica
  equivalente con corpus real.
- **HP2' (ventana, condicional).** PUEDE existir un rol de contribuidor/implementacion-de-referencia en
  los procesos Sigstore-agentes y NIST CAISI; no se puede verificar sin contacto directo. Por eso el
  test de ventana (contacto a Hinds con pregunta concreta) va ANTES del preprint y es kill-signal a 30
  dias. Refutacion: respuesta negativa o silencio + evidencia de candidato ya elegido.
- **HP3 (irrelevancia > copia).** EN PIE 6/6, sin cambios: lo no publicado no se puede adoptar, citar ni
  comprar; la convergencia ocurre con o sin nosotros.
- **HP4' (captura via complemento, honesto).** Para una persona sola, la captura del Carril B es:
  corpus reproducible + implementacion de referencia + expertise demostrable; el resultado modal es
  capital de carrera/credibilidad (techo realista tipo C4/Simon Brown) y se acepta sin eufemismos.
  La captura ECONOMICA principal del sistema completo es el Carril A: la empresa construyendo Nova
  mas rapido y con menos defectos (si la medicion lo confirma).
- **HP5' (plan re-baselineado).** El Carril B minimo (Semana 0 + paquete reproducible + test de ventana
  + preprint estrecho) cabe en ~90 dias SOLO como carril secundario del Carril A, con gates entre fases
  y sin fecha comprometida para spec completa / MCP / Action. Refutacion: que la Semana 0 o el paquete
  reproducible revienten el presupuesto de atencion del operador.
- **HP6 (transferencia interna).** Empleados operando instancias Nova sin ayuda sincrona del autor
  (onboarding <= 1 dia, cero des-atascos manuales del autor por semana tras el mes 1) es evidencia
  INTERMEDIA de transferibilidad, declarada como tal (no sustituye instancias externas). Refutacion:
  dependencia sostenida del autor para operar.
- **HP7 (Nova como motor de evidencia).** Con el pre-registro de s.7 sellado en el ledger ANTES del
  primer sprint, Nova Budget puede producir en 6 meses: respuesta fuerte a Q1 (peones/costo), evidencia
  mecanistica a Q2 (defectos que el checker atrapa y el gate no), y un contraste Q4 operacionalmente
  factible aunque probablemente de bajo poder. Sin pre-registro, Nova no prueba nada (anecdota +
  conflicto de interes). Refutacion: que la presion de entrega rompa la asignacion o el etiquetado.

---

## 6. Planteamiento: dos carriles con prioridad explicita

**Carril A (PRINCIPAL): metodologia employee-ready + Nova Budget como piloto instrumentado.**
Secuencia: (1) cierre gobernado del pipeline actual (0229; cancelar 0230/0232 del fork con DECISION;
re-alcanzar 0233 hacia "instancia desde template operada por no-autor" y 0234 hacia runbooks de
onboarding); (2) prerequisitos employee-ready: memoria hibrida Fase 0-1 (arranque en frio con BD,
SQLite ya disponible sin instalacion), doctrina minima (gate determinista de intake por tipo de trabajo
+ registro de excepciones auditado), hardening de `new_instance`/NOVA, SLO interno de confiabilidad
(N dias sin des-atasco manual como gate de arranque con empleados); (3) instrumentacion del estudio
(~3.5 dias-agente con las simplificaciones de s.7.6); (4) sellado del pre-registro como DECISION con
hash en el ledger; (5) arranque de Nova Budget SOLO (los otros tres Nova esperan a que Budget demuestre
el flujo); Fase 1 peones (semanas 1-4+), Fase 2 contraste (meses 2-6).

**Carril B (SECUNDARIO, barato, gateado): "publicar para ser citado" re-baselineado** (s.8). Regla de
subordinacion explicita: si en una semana dada el Carril B compite por atencion con un gate del Carril
A, gana el Carril A; el Carril B avanza con lo que los agentes produzcan y el operador apruebe en <= 1
dia/semana.

---

## 7. PRE-REGISTRO DE MEDICION (Q1-Q4) -- version post-ataque interno (F1-F7 corregidos)

### 7.0 Convenciones selladas (deciden todo)
- Unidad de analisis = TAREA. Poblacion = todas las tareas de Nova Budget v1.0 (compromiso de publicar
  el periodo COMPLETO; el ledger append-only con seq monotonica prueba que no hay omisiones).
- **Defecto** (taxonomia cerrada): D1 = gate/test rojo pre-GO; D2 = hallazgo del checker en NO-GO con
  test/repro adjunto; D3 = escape post-GO (tarea `type:fix` con trailer `Fixes-Task:` obligatorio, o
  revert/hotfix que referencia el commit aceptado); D4 = reporte de usuario. Solo D3/D4 cuentan como
  "escape". Ambiguedades -> `arbitrated:true`, reportadas aparte; si una conclusion depende de
  arbitrados, se declara.
- Trailer `Task-Id:` OBLIGATORIO en todo commit (validador lo exige). Linkage de defectos v1 = SOLO
  trailer `Fixes-Task:` (bisect/blame = v2, pospuesto por el ataque interno).
- Pre-registro completo (esta seccion + semilla + taxonomia de riesgo + reglas de parada) se sella como
  DECISION firmada en el ledger ANTES de la primera asignacion: el hash encadenado es el sello temporal
  y el argumento anti-sesgo-del-experimentador mas fuerte disponible.

### 7.1 Metricas CONFIRMATORIAS (solo estas; todo lo demas es exploratorio)
- **C1 (Q1, decisiva): tokens del firmante por tarea aceptada.** Ventana claim->GO; emision AUTOMATICA
  de `cost.attributed` con task_id en el cierre de turno del wrapper (bloqueante del cierre -- fix F5);
  tokens crudos estratificados por tamano S/M/L pre-etiquetado (SIN normalizar por LOC, gameable).
  Regla: adoptar peones si mediana(B) <= 0.6 x mediana(A) Y C2 < 20% Y escapes(B) <= escapes(A).
  Refuta: mediana(B) >= 0.85 x mediana(A).
- **C2 (Q1, guardarrail): kickback de peones.** UNA definicion mecanica (fix F3): draft de peon que no
  llega a commit firmado o recibe NO-GO en primera review. Habilita adopcion < 20%; refuta >= 35%.
- **C3' (Q2/Q4, primaria del contraste): escapes post-GO por tarea, intention-to-treat** (fix F2: DER
  es indefinida en el brazo ligero). Ventana de exposicion con fecha de corte unica pre-registrada;
  tareas con < 30 dias de exposicion se marcan censuradas y se reportan aparte (fix F6: los defectos de
  software financiero afloran en cierres contables).
- **Q2 mecanistica (co-primaria): conteo contable de defectos con test/repro que el checker atrapo y el
  gate determinista NO atrapo.** Evidencia mecanistica, no estadistica: "el checker atrapo N defectos
  concretos, aqui estan". Es la salida mas defendible del estudio.

### 7.2 Degradadas a DESCRIPTIVAS (por el ataque interno)
- DER y tasa de retrabajo/NO-GOs: solo describen el brazo completo (F2).
- Q3 "el gobierno aumenta calidad" via tendencia temporal: before/after confundido con aprendizaje (F4).
  Se reporta la evolucion sin claim causal. Q3 confirmatoria solo si el contraste Q4 la soporta.
- Densidad por KLOC, costo total por feature, tiempos de ciclo, cortes por modulo/agente: exploratorias.

### 7.3 Diseno del contraste Q4 (gobierno ligero vs completo)
- **Ambos brazos conservan** (piso etico innegociable): tests+CI bloqueantes, claims, registro pasivo
  COMPLETO en el ledger (el ledger es el instrumento; el brazo ligero no puede quedar ciego).
- **Delta experimental exactamente UNO:** el checker adversarial independiente y su ceremonia. Ligero =
  self-review del maker con checklist pre-registrada + gates verdes -> done.
- **Exclusion etica pre-registrada:** riesgo ALTO (movimiento de dinero, calculo de nomina/tesoreria,
  auth, migraciones que tocan saldos) SIEMPRE gobierno completo, fuera del contraste. Elegibles solo
  riesgo medio/bajo (UI, reporting, CRUD no monetario, refactors cubiertos). El contraste generaliza
  solo a criticidad media/baja -- declarado.
- **Asignacion:** por TAREA (fix F1; modulo confunde, sprint confunde con tiempo), determinista y
  auditable: hash(task_id + semilla pre-registrada) -> brazo, estratificada por S/M/L y riesgo, en
  bloques de 4; escrita en el ledger ANTES del claim (el hash encadenado impide cherry-picking
  retroactivo). Escalada ligero->completo permitida con excepcion auditada; analisis primario
  intention-to-treat, per-protocol como sensibilidad.
- **Peones:** SECUENCIAL, no factorial (con este n, un 2x3 es ruido): Fase 1 (semanas 1-4, extensible
  hasta >= 15 tareas/brazo) = A vs B bajo gobierno completo solamente (el brazo C con critico LLM se
  ELIMINA de v1 -- simplificacion del ataque interno); Fase 2 = contraste Q4 con la politica de peones
  ganadora CONGELADA e identica en ambos brazos.
- **Parada de seguridad:** incidente Sev1 en logica financiera del brazo ligero, o escapes(ligero) > 2x
  escapes(completo) con >= 20 tareas/brazo -> todo a gobierno completo y se REPORTA (un stop de
  seguridad ES un resultado sobre el valor del checker). Interim unico a 8 semanas, solo seguridad.
- **Valvula de presion pre-registrada:** el operador puede suspender la aleatorizacion por sprint entero
  (todo a completo) registrandolo como evento; ese periodo queda excluido, nunca re-etiquetado. Evita
  que la presion de entrega corrompa el estudio en silencio.
- **El nulo esta pre-decidido (F del ataque):** si el contraste es nulo/ambiguo se reporta "no detectamos
  diferencia >= X con este n"; el default operativo permanece gobierno completo por asimetria de riesgo
  en software financiero; la salida co-primaria (conteo mecanistico) se publica igual.

### 7.4 Amenazas top-3 y su tratamiento (resto en el pre-registro completo)
1. Sesgo del arbitro-autor: etiquetado mecanico primero; `arbitrated:true` aparte; veredicto primario lo
   emite el agente checker; anulaciones humanas solo con evento firmado y motivo (conteo publicado).
   Residuo declarado: el conflicto de interes no desaparece; se publica el ledger completo como dataset.
2. Cherry-picking: confirmatorias selladas antes de empezar; prohibido promover exploratorias post-hoc.
3. Seleccion de publicacion: compromiso de publicar el periodo completo; huecos de secuencia en el
   ledger delatan omisiones.
Ademas: Hawthorne sin mitigacion real en 2-6 personas (declarado; opera en ambos brazos); contaminacion
maker-aprende-del-checker sesga HACIA el nulo (conservador: si aun asi hay diferencia, es senal fuerte).

### 7.5 Fuerza de la conclusion (textual, va en el pre-registro y en el paper)
"Este estudio es un caso de estudio industrial instrumentado en una empresa de 2-6 personas cuyo
director es el autor de la metodologia evaluada. Su fuerza probatoria maxima es: medicion automatica
pre-registrada con sello criptografico, un contraste aleatorizado interno de baja potencia y evidencia
mecanistica contable (defectos concretos atrapados o escapados, trazados en un ledger append-only
completo y publicado). Puede establecer direcciones, magnitudes grandes y hechos contables verificables
en este proyecto; no puede establecer efectos pequenos, causalidad generalizable ni afirmacion alguna
sobre otros equipos. Un resultado nulo en el contraste no demuestra equivalencia; se interpretara segun
la regla pre-registrada y el default permanece gobierno completo."

### 7.6 Instrumentacion (con las simplificaciones del ataque)
Reuso ~60% existente (cost-attribution DECISION-0033/SPEC-0079 vivo; `agent_metrics.py` TASK-0214;
eventos de ciclo ya en el ledger). Nuevo, todo aditivo `applied:false` sin tocar el chain pineado:
etiqueta arm/mode en task_upsert + validador de trailers (0.5 dia-agente); emision automatica de
`cost.attributed` por task_id en el wrapper (1); eventos `defect.reported` + `manual.intervention` (1);
`study_metrics.py` determinista con golden fixture (1). **Total ~3.5 dias-agente** (bisect/blame y
brazo C pospuestos a v2).

### 7.7 Que sera defendible en 6 meses (expectativa honesta, del ataque interno)
Q1: SI, fuerte. Q2: mecanistica si (conteo), estadistica probablemente no. Q3: descriptiva. Q4:
operacionalmente factible, resultado probablemente de intervalos solapados con n~40/brazo -- por eso el
nulo esta pre-decidido y la co-primaria es mecanistica.

---

## 8. Carril B re-baselineado ("publicar para ser citado", subordinado al A)

### 8.1 Semana 0 (bloqueante, antes de publicar NADA)
Revision PII/secrets/confidencialidad del corpus (nombres, rutas, contexto de cliente) + manifest de
redaccion; licencias dia 1 (core Apache-2.0; dataset CC-BY-4.0; marca reservada; compromiso publico de
no-relicenciamiento hostil del core); endorsement de arXiv asegurado (cs.SE/cs.CR exigen endorser a
autores nuevos); claims publicos estrechos redactados (los de s.5).

### 8.2 Paquete minimo reproducible (gate: un externo lo verifica en 5-10 comandos)
Dataset N=500 + verificador + threat model INCLUIDO lo no-cubierto (colusion, compromiso de claves,
operador-como-raiz -- publicado por nosotros antes que por un critico) + medicion de overhead por tarea
(instrumentando el PROPIO trabajo de este plan con el protocolo: el plan se mide a si mismo, idea
adoptada de ClaudeAI) + Zenodo con DOI.

### 8.3 Entregable tecnico central: interop, no paralelo
Envolver eventos en DSSE/in-toto y anclar checkpoints periodicos del ledger en Rekor. Sustituye al MCP
server como prioridad tecnica (MCP/Action pasan a meses 4-6, y SOLO si un tercero ya reprodujo el
paquete). "Minimum public reference profile" (schema de evento + verifier + threat model + una instancia
limpia) en vez de spec-repo completo.

### 8.4 Outreach redisenado
Test de ventana PRIMERO: contacto directo y tecnico a Hinds con una pregunta concreta y UNA peticion
decidida de antemano (propuesta: PR de interop DSSE/Rekor a nono + item de agenda OpenSSF sobre profile
multi-agente), ANTES de escribir el preprint. Sin respuesta en 30 dias o respuesta negativa = se
recalibra HP2' (el Carril B continua via paquete reproducible + preprint, sin apostar a la alianza).
Canal nominal (correccion A13): Hinds/nolabs, autores de IETF AAT, OpenSSF/Sigstore WG, CSA, 2-3
auditoras ISO 42001, software factories reguladas conocidas. HN/X solo DESPUES de feedback tecnico.

### 8.5 Preprint
Systems/experience paper con related work completo (s.3.1), claims estrechos (s.5 HP1'), limitaciones
como tabla principal (jams historicos incluidos -- correccion A15), y (cuando exista) la evidencia de
Nova. Sin fecha comprometida: gate = paquete reproducible verificado por un externo.

---

## 9. Kill-criteria de dos niveles

### 9.1 SENALES (informan, no ejecutan)
- Dia 30: respuesta de Hinds (si/no/nada). Dia 60: discusion externa del paquete/DOI (issues, mails
  tecnicos). Dia 90: alguien externo reprodujo la verificacion.
### 9.2 DECISIONES
- Mes 6: si cero interaccion tecnica sustantiva (definicion mecanica: PR externo aceptado, issue tecnica
  reproducida, cita, item de agenda en WG, piloto de tercero -- cortesias NO cuentan), el Carril B se
  reduce a mantenimiento pasivo (el Carril A no se afecta).
- Mes 12: 1 instancia externa en uso real O 1 piloto con auditora -> persevere; si no, Carril B =
  artefacto academico congelado. Mes 18: 2 instancias externas o la tesis de transferibilidad EXTERNA
  se declara no probada (la interna de Nova sigue valiendo para la empresa).
- Carril A (independiente): HP6 se evalua al mes 3 de empleados operando; el estudio Q1-Q4 tiene sus
  reglas de parada propias (s.7.3).

### 9.3 Resultado modal aceptado
Si el Carril B no captura economicamente, el retorno es: credibilidad publica + capital de carrera +
una empresa que construye software financiero con una metodologia medida. Eso se declara exito parcial,
no fracaso -- sin eufemismos (correccion ClaudeAI/ZAI).

---

## 10. Riesgos v2
- R1 Silencio total del Carril B: mitigado por subordinacion al A y senales 30/60/90.
- R2 Peer review hostil: claims estrechos + threat model propio + related work completo.
- R3' nolabs/nono avanza multi-agente: mitigado por interop (mismo ecosistema) y velocidad del paquete.
- R6 (NUEVO) nolabs absorbe el diseno sin atribucion: mitigacion = DOI/fechas ANTES del contacto,
  peticion decidida de antemano, y aceptar que features-en-nono-con-atribucion es un resultado BUENO.
- R7 (NUEVO) adopcion interna falla (empleados rechazan la metodologia): mitigacion = SLO de
  confiabilidad como gate de arranque, onboarding <= 1 dia, doctrina proporcional (modos), y HP6 medida.
- R8 (NUEVO) la presion de entrega de Nova corrompe el estudio: valvula de presion pre-registrada +
  compromiso de publicar el periodo completo.
- R9 Capacidad del operador: el embudo es su atencion, no la produccion de los agentes; presupuesto
  explicito <= 1 dia/semana al Carril B.

## 11. Angulos adversariales para la ronda 2 (atacar, y sumar los que falten)
1. El pre-registro de s.7: es realmente sellable e inviolable con el mecanismo propuesto (DECISION +
   hash encadenado)? Que camino queda para re-etiquetar a posteriori?
2. La definicion de defecto D1-D4 y el linkage v1 (solo trailer): que defecto real se escapa de esa
   taxonomia y cuanto subconteo produce?
3. El contraste Q4 restringido a criticidad media/baja: el resultado sirve de algo si excluye
   exactamente el codigo donde el gobierno importa mas? (Generalizacion honesta vs utilidad.)
4. La exclusion del brazo C (critico LLM): se pierde la pregunta mas barata de responder?
5. HP6 (transferencia interna): el umbral "onboarding <= 1 dia, cero des-atascos del autor" es medible
   sin ambiguedad? Quien lo mide?
6. Interop DSSE/in-toto/Rekor: esfuerzo real? Rompe el chain pineado o el replay? Es compatible con el
   genesis content-addressed actual?
7. La subordinacion del Carril B (<= 1 dia/semana): es creible dado el historial del operador de abrir
   frentes? Que mecanismo la hace cumplible?
8. Los kill-criteria de mes 18 para instancias externas: siguen siendo un kill disfrazado?
9. La cancelacion gobernada de 0230/0232 y el re-alcance de 0233/0234: que DECISION exacta lo formaliza
   y que pasa con DECISION-0077?
10. Semana 0: falta algun bloqueante legal/operativo (propiedad intelectual de la empresa sobre el
    protocolo? contratos de empleados sobre datos del estudio?)?
11. El estudio mide a los EMPLEADOS: hace falta consentimiento informado interno / politica escrita de
    no-uso-para-evaluacion-de-desempeno? (El panel la propuso; es suficiente?)
12. Que angulo falta en esta lista?

## 12. Pregunta de cierre para el revisor
Veredicto GO / NO-GO / CAMBIO-REQUERIDO sobre: (a) el marco de dos carriles con prioridad al A;
(b) el pre-registro de medicion s.7 tal como esta (es sellable ya?); (c) el Carril B re-baselineado
s.8-9. Cuales hipotesis HP1'-HP7 quedan en pie, que angulo de s.11 resulto letal, y que cambiarias
antes de que el operador formalice directiva + DECISION.
