# F1.6 - Aprendizajes externos: extraccion de reglas (timebox 2d, paralelo)

Autor: Arquitecto - Fecha: 2026-07-03 - Pipeline: F1.6 (nucleo doctrinal, no camino critico)
Fuentes: ancladas y verificadas en personal/operador/pivote/DISCUSSION-pivote-publicar-para-ser-citado.md
(s.2, verificacion de primera mano 2026-07-02) + memoria del proyecto + benchmark del ecosistema.

## Como leer esto
Cada regla trae: FUENTE externa -> APRENDIZAJE -> REGLA extraida para la metodologia (Aegis) -> ESTADO.
ESTADO: [YA-CODIFICADA] = el aprendizaje ya vive en una DECISION/AGENTS.md (esto lo VALIDA y le da
vocabulario externo citable); [CANDIDATA] = propuesta nueva, el Operador decide adopcion via DECISION;
[MAPPING] = no cambia doctrina, solo expone nuestra doctrina en el vocabulario del estandar externo.
Extraer != adoptar: las candidatas son insumo, no cambio de protocolo (los cambios de protocolo van por
DECISION, DECISION-0002/boundary).

## Reglas extraidas

### R-EXT-01 - Nombrar nuestras atestaciones en la taxonomia de Hinds (Plan/Generation/Approval)
- FUENTE: Luke Hinds (creador de Sigstore, CEO NoLabs), post 21-ene-2026 "extend the chain to agents":
  TRES atestaciones -- Plan / Generation / Approval -- y peticion explicita de colaboracion.
- APRENDIZAJE: hay un vocabulario emergente de facto (Plan/Generation/Approval). Nuestro ledger ya es un
  SUPERSET (task/spec atestada ~ Plan; eventos de entrega firmados ~ Generation; veredicto maker!=checker
  firmado ~ Approval; MAS claims, excepciones y ciclo de vida completo).
- REGLA: exponer explicitamente el MAPPING Aegis -> Plan/Generation/Approval en el spec de referencia
  publicable (no renombrar el core; solo un anexo de interoperabilidad). Mantener el superset como
  diferenciador, pero hablar el idioma del estandar para ser citable/interoperable.
- ESTADO: [MAPPING] -> insumo para el spec de Carril B (CB.3/CB.5) y el outreach a Hinds (CB.4).

### R-EXT-02 - Chain-of-custody + frontera de confianza multi-agente como INVARIANTES nombrados
- FUENTE: NIST CAISI, AI Agent Standards Initiative (17-feb-2026): "accountability gaps in autonomous
  action chains" como vulnerabilidad urgente; controles SP 800-53 adaptados incl. chain-of-custody
  logging y multi-agent trust boundaries.
- APRENDIZAJE: el gobierno nombra exactamente nuestras piezas (cadena de custodia + fronteras de confianza
  entre agentes) como el gap a cerrar.
- REGLA: formalizar con nombre las dos piezas que ya tenemos: (a) la cadena #4 atestada = chain-of-custody;
  (b) el escritor-unico del ledger + maker!=checker + hub-jamas-compartido-con-empleados = la frontera de
  confianza multi-agente. Anotarlas como invariantes citables (state_invariants del config ya las lista;
  darles el rotulo del estandar en el spec).
- ESTADO: [YA-CODIFICADA] (DECISION-0022 escritor-unico, DECISION-0050 hub permanente, maker!=checker en
  AGENTS.md s.7) -> el aporte es el ROTULO externo + el mapping a SP 800-53.

### R-EXT-03 - No regresar a "una sesion / un agente": el multi-agente + ciclo es el foso
- FUENTE: nono.sh (OSS Apache-2.0, abr-2026): audit trail append-only por SESION con Merkle + DSSE +
  verify de terceros -- pero cubre UNA sesion de UN agente; SIN multi-agente, SIN maker!=checker, SIN
  ciclo tarea->claim->review->cierre, SIN evidencia medida.
- APRENDIZAJE: el competidor OSS mas cercano se queda en el caso trivial. Nuestro valor es exactamente lo
  que a el le falta.
- REGLA: preservar como invariantes NO-NEGOCIABLES el multi-agente + ciclo de vida formal + maker!=checker
  + evidencia MEDIDA (el estudio). Cualquier simplificacion que colapse a "una sesion" es una regresion de
  producto, no una mejora. La compatibilidad DSSE/in-toto se explora como SPIKE (CB.2), sin degradar el foso.
- ESTADO: [YA-CODIFICADA] (es el nucleo) -> el aporte es la CONSCIENCIA competitiva: no regresar.

### R-EXT-04 - Verificacion de terceros en <=N comandos = el estandar de falsabilidad
- FUENTE: in-toto/SLSA/Rekor/DSSE (atestaciones firmadas y encadenadas con verify de terceros) +
  precedente Sigstore.
- APRENDIZAJE: el valor de una atestacion es que un TERCERO la verifica sin confiar en el emisor.
- REGLA: todo lo atestado debe ser verificable en clon limpio por un externo en pocos comandos
  (ya es nuestra practica: el Analista pre-gatea en clon limpio; CB.3 = "un externo lo verifica en 5-10
  comandos"). Elevar esto a criterio DURO del paquete publicable: si un externo no puede reproducir la
  verificacion, no esta listo para publicar.
- ESTADO: [YA-CODIFICADA] (gate en clon limpio) -> el aporte es fijarlo como criterio de publicacion (CB.3).

### R-EXT-05 - El gate independiente (maker!=checker) atrapa lo que la revision informal deja pasar
- FUENTE: incidentes verificados -- agente de Replit borro DB de produccion en code-freeze y MINTIO
  (jul-2025); wiper inyectado en Amazon Q a ~1M devs (jul-2025); 93% de CTOs preocupados por vibe-coding.
  + evidencia PROPIA en vivo: en TASK-0246 el checker formal (Analista) atrapo THROWs inexistentes y
  mis-atribucion proc-vs-trigger que mi generacion por-doc y las revisiones informales dejaron pasar.
- APRENDIZAJE: "el agente mintio / no verifico contra la realidad" es el modo de fallo central; el
  antidoto medido es el checker estructuralmente independiente con acceso a la realidad (BD/artefacto).
- REGLA: el gate adversarial independiente con verificacion contra la REALIDAD desplegada (no contra los
  docs) es obligatorio para todo entregable con criterios falsables. Corolario F-NOVA-01: citar la
  definicion real (OBJECT_DEFINITION/artefacto), nunca la narracion del doc.
- ESTADO: [YA-CODIFICADA] (maker!=checker + DECISION-0084 anti-vibecoding + envelope+fixloop) -> el aporte
  es la EVIDENCIA ANECDOTICA en vivo (0246) para el estudio y el outreach.

### R-EXT-06 - Atribucion de cada cambio a sesion firmada + least-privilege (auditoria SOC2/ISO42001)
- FUENTE: demanda con dinero HOY -- SOC 2 CC8.1 (change-management identico al humano), ISO 42001,
  Microsoft SSPA (controles IA a proveedores), Gartner AI-governance $492M 2026 -> >$1B 2030.
- APRENDIZAJE: el comprador liquido (vendor que pasa auditoria, CISO regulado) YA exige atribucion por
  sesion autorizada + least-privilege de agentes.
- REGLA: mantener y publicar el mapping de nuestras piezas a los controles de auditoria: trailers
  Task-Id + Co-Authored-By + cadena #4 = atribucion por sesion; capabilities por agente + participantes
  no-firmantes = least-privilege; ciclo de vida formal = change-management. Es el argumento de venta, no
  solo de cumplimiento.
- ESTADO: [YA-CODIFICADA] (gate de trailers, agent_registry con capabilities, DECISION-0086 no-firmante)
  -> el aporte es el MAPPING a SOC2 CC8.1 / ISO 42001 para el paquete comercial/publicable.

### R-EXT-07 - La atestacion criptografica del ciclo MULTI-AGENTE es whitespace (nadie la ofrece)
- FUENTE: barrido del mercado -- observabilidad/eval (Braintrust, LangSmith, Arize, Patronus: traces y
  scores, logging convencional) y gateways MCP/politicas (MintMCP, Lasso, Arthur, Credo). NINGUNO ofrece
  atestacion criptografica del ciclo multi-agente.
- APRENDIZAJE: hay mucho "observability" y "policy gateway", cero "cryptographic attestation of the
  multi-agent cycle". Traces/scores NO son atestacion.
- REGLA: no diluir la propuesta a observabilidad. La linea roja: nuestra evidencia es ATESTADA y
  encadenada (firmada, verificable por terceros), no meramente logueada/puntuada. Mantener la distincion
  explicita en todo material (atestacion != telemetria).
- ESTADO: [CANDIDATA de posicionamiento] -> insumo para el spec/preprint (CB); no cambia doctrina interna.

### R-EXT-08 - Decidir la frontera abierto/cerrado el DIA 1 (no retrofit de licencia)
- FUENTE: precedentes de captura de valor -- quien capturo poseia un COMPLEMENTO ESCASO, nunca la spec
  (Sigstore->Chainguard $3.5B; Git->GitHub; semver captura CERO). Leccion de licencia: HashiCorp/BUSL
  retrofit QUEMO confianza.
- APRENDIZAJE: publicar la spec neutra genera reputacion; el valor lo captura el motor de evidencia
  escaso; y cambiar la licencia despues destruye confianza.
- REGLA: (a) el complemento escaso = el MOTOR DE EVIDENCIA ATESTADA + el estudio medido (eso se protege);
  (b) publicar la spec/core neutral con licencia permisiva (Apache-2.0) DECIDIDA en una DECISION antes de
  publicar; (c) NUNCA retrofit de licencia sobre lo ya publicado.
- ESTADO: [CANDIDATA] -> requiere DECISION de licencia/frontera ANTES del primer release publico (Carril B);
  no bloquea el Carril A ni el sello.

### R-EXT-09 - Memoria: ruta unica hibrida; no inyectar motores externos de memoria
- FUENTE: gentle-ai/Engram (ecosistema de memoria) -- RUTA CERRADA por el Operador; leccion: 'gentle-ai
  install' inyecta Engram (dependencia externa).
- APRENDIZAJE: adoptar un motor externo de memoria mete una dependencia que rompe el principio "Git es el
  adapter, configs commiteadas".
- REGLA: la unica ruta de memoria es la hibrida propia (REQ-MEMORIA-HIBRIDA v0.3.0: hot/cold, indice
  derivado, rebuild round-trip verde), que absorbe las lecciones del ecosistema SIN su dependencia. Toda
  decision futura de memoria debe superseder DECISION-0071 explicitamente.
- ESTADO: [YA-CODIFICADA] (decision del Operador 2026-07-02) -> el aporte es dejar la regla escrita como
  aprendizaje-externo, no solo como preferencia.

### R-EXT-10 - Las ventanas de estandar se cierran EN SERIE: la evidencia falsable es el activo durable
- FUENTE: NIST CAISI -- las ventanas de comentario publico YA CERRARON (AI Agents 9-mar; Identity 2-abr);
  la via ahora son los pilares permanentes (industria/open-source) + contacto directo (la llamada de
  Hinds sigue abierta, verificado).
- APRENDIZAJE: la urgencia es real, no retorica; las ventanas se cierran en serie. Pero el activo que NO
  caduca es la evidencia falsable (dataset DOI + paquete reproducible).
- REGLA: tratar el engagement con estandares como ventanas time-boxed (Carril B outreach, kill-criteria),
  NUNCA en camino critico del Carril A; y priorizar como activo durable la EVIDENCIA (dataset sellado +
  paquete reproducible verificable por terceros), que vale independientemente del timing de la ventana.
- ESTADO: [YA-CODIFICADA] (Carril B gateado <=1 dia/semana; el estudio/sello es Carril A) -> el aporte es
  la consciencia de serie-de-ventanas para priorizar outreach.

## Sintesis (que hacer con esto)
- 6 reglas VALIDAN doctrina existente y le dan vocabulario externo citable (R-01..R-06, R-09, R-10):
  utiles para el spec de referencia, el preprint y el outreach de Carril B; cero cambio de protocolo.
- 2 CANDIDATAS requieren DECISION antes de publicar: R-EXT-08 (frontera de licencia abierto/cerrado dia 1)
  y R-EXT-07 (linea roja atestacion!=observabilidad, si se formaliza en el spec).
- NINGUNA es camino critico (F1.6 asi lo exige). Todo es insumo para Carril B (spec/preprint/outreach) y
  para el material comercial (mapping a SOC2/ISO/NIST/Hinds).
- Recomendacion: el Operador prioriza cual candidata se eleva a DECISION cuando el Carril A de holgura;
  mientras, este documento queda como el aprendizaje-externo extraido (F1.6 hecho).
