> **[SUPERSEDIDA 2026-07-02 por v2]** Esta version (v1) recibio ronda 1 adversarial: CAMBIO-REQUERIDO del
> Analista (`Area_comun/artifacts/ANALISTA-pivote-publicar-citado-veredicto.md`) + 5 revisiones externas
> (ClaudeAI/Copilot/Gemini/OpenAI/ZAI), todas CAMBIO-REQUERIDO. Version vigente:
> `DISCUSSION-pivote-v2-publicar-para-ser-citado.md` (misma carpeta), que ademas incorpora la nueva vision
> del Operador (empresa + suite Nova + TFM no formal) y el pre-registro de medicion Q1-Q4. Historico.

# DISCUSSION -- Pivote estrategico "Publicar para ser citado" (hipotesis para validacion adversarial)

Autor: Asesor del Operador. Fecha: 2026-07-02. Para: revision ADVERSARIAL (Analista, via Arquitecto).
Proposito: validar o refutar la hipotesis de pivote ANTES de formalizarla como directiva del operador +
DECISION en el ledger. El revisor debe atacar las hipotesis HP1-HP5 (s.4) y los angulos de s.9, y emitir
GO / NO-GO / CAMBIO-REQUERIDO con evidencia.

---

## 1. Estado actual (hechos verificables, 2026-07-02)

### 1.1 Lo que existe y funciona
- **Hub** `multi_agent_project_protocol`: metodologia de gobierno multi-agente dogfooded en si misma.
  81 decisiones formales, 287 tareas, ledger append-only con 2,416 eventos ATESTADOS (firma ed25519 por
  agente, prev_hash encadenado, genesis content-addressed), claims anti-colision, maker!=checker forzado,
  gates adversariales operando (el Analista refuto entregas reales: 7 NO-GO en TASK-0227, NO-GO a 0237 por
  watchdog que no cubria vendor), validadores multiplataforma, core neutral + templates + wrapper
  new_instance (instancia NOVA).
- **Evidencia medida** (dataset sellado, tag TFM-dataset-N500): 500 eventos firmados, 3 hipotesis
  PRE-REGISTRADAS confirmadas: deteccion de manipulacion 100% (450/450 ataques inyectados), falsos
  positivos 0% sobre 500 legitimos, overhead mediana 1.6ms / 0.42KB por evento, verificacion reproducible
  por verificador independiente en clon limpio con SOLO claves publicas. Informe HTML autocontenido.
- **Panel web read-only propio** (Zeus-protocol front): 49 archivos, ~180 features entregadas; observa
  ledger/mailbox/tareas/atestacion. Vanilla JS monolitico (herramienta interna, no producto).
- **TFM en curso** (tesis de master del operador) con deadline: vehiculo de credibilidad disponible.

### 1.2 Lo que existia como plan de producto y su estado
- **Zeus-Aegis** = fork de hermes-agent (NousResearch, MIT; app Electron de chat con agentes).
  DESCARTADO por el operador el 2026-07-02: 1,094 archivos ajenos vs 13 propios; treadmill de merges
  upstream; 154 assets por purgar; los jams de crons de esta semana vinieron de la suite del VENDOR;
  contradice la identidad ratificada.
- **Identidad ratificada textual** (operador, 2026-07-02): "Zeus-Aegis es para desarrolladores
  profesionales -- y para profesionalizar a quien construye software con IA sin serlo." Anti-vibecoding.
- **Pipeline REQ-ZEUS-001 vigente**: 0222-0228+0235-0237 done; 0229 (WS3 branding) in_review; 0230 (WS2
  bootstrapper del fork), 0232 (WS3.5 instalador del fork), 0233 (WS7 e2e), 0234 (WS10 runbooks)
  registradas sin promover. WS2/WS3.5 pierden sentido si el fork muere.
- **REQs futuros** (personal/operador/requerimientos-futuros/): beta publica (12 REQ-PUB), memoria
  hibrida v0.3.0 (ruta unica, Engram cerrado), intake profesional v0.2.0, anti-vibecoding v0.2.0 +
  mini-DECISION, aprendizajes externos, instalacion-poderes-db.

### 1.3 Los costos reales (honestidad preventiva; el revisor DEBE pesarlos)
- Fragilidad operativa documentada: jam de 14h (0222), jam de 30min (0229), zombies que exigieron
  Restart Manager API, 4+ commits fix(drift) en ~30 commits, deadlock en higiene de mailbox, footgun de
  stop-order. Remediado en 0235/0236/0237 + DECISION-0080, pero la TASA historica de incidentes es alta.
- Overhead de PROCESO no medido: 8-15 eventos + varios execs LLM por tarea, aun trivial. Los 1.6ms de H2
  miden el costo estructural del evento, NO el costo de coordinacion del ciclo.
- N=1: una sola instancia real, operada por su autor con contexto total. Transferibilidad NO probada.
- Restricciones: UNA persona + agentes IA; sin funding conocido; espanol nativo; Windows.

---

## 2. Investigacion (panel de 9 agentes, 2026-07-02, con fuentes; anclas verificadas de primera mano)

### 2.1 Mercado: los grandes convergen en control-plane, NO en evidencia criptografica
- GitHub: Agent Control Center GA (jun-2026), session logs enlazados a commits -- NO firmados.
  Agentic Workflows sobre Actions, sandboxes en preview.
- Anthropic Claude Code: managed-settings no-overridable, hooks como politica, Compliance API,
  OpenTelemetry -- policy enforcement + telemetria, NO atestacion.
- OpenAI Codex: RBAC enterprise, agent approvals, workspace agents -- controles, NO atestacion.
- Google Antigravity: "Artifacts" (el agente PRUEBA su trabajo: planes, screenshots, diffs) -- NO
  firmados ni encadenados. Managed Agents API (may-2026).
- Cursor: audit logs enterprise; explicitamente NO loguea contenido generado por agentes.
- Startups: dos clusteres -- observabilidad/eval (Braintrust, Galileo, LangSmith, Arize, Patronus;
  traces y scores, logging convencional) y gateways MCP/politicas (MintMCP, Lasso, Arthur, Credo).
  NINGUNO ofrece atestacion criptografica del ciclo multi-agente.
- Lo MAS cercano: nono.sh (open source Apache-2.0, abr-2026): audit trail append-only por SESION con
  Merkle tree + firma DSSE + verify de terceros. Cubre UNA sesion de UN agente: sin multi-agente, sin
  maker!=checker, sin ciclo de vida tarea->claim->review->cierre, sin evidencia medida publicada.

### 2.2 Las dos anclas de estandarizacion (VERIFICADAS de primera mano el 2026-07-02)
- **Luke Hinds (creador de Sigstore, CEO NoLabs), post del 21-ene-2026** (nolabs.ai/blog/
  sigstore-ai-agent-provenance): propone extender SLSA/in-toto/Sigstore a agentes con TRES atestaciones
  (Plan Attestation / Generation Attestation / Approval Attestation) y pide colaboracion EXPLICITA
  ("I'm actively exploring these questions and would welcome collaboration... let's talk"), contacto
  directo. Cita clave: "The chain we built assumed humans write code. That assumption is now false.
  It's time to extend the chain." NUESTRO protocolo ya implementa un superset de su taxonomia:
  Plan ~= task/spec atestada; Generation ~= eventos de entrega firmados; Approval ~= veredicto
  maker!=checker firmado; MAS claims, excepciones y ciclo completo.
- **NIST CAISI, AI Agent Standards Initiative, lanzada 17-feb-2026**: primer programa del gobierno de
  EE.UU. para estandares de agentes; "accountability gaps in autonomous action chains" identificado como
  vulnerabilidad urgente; 3 pilares (estandares liderados por industria, protocolos open-source,
  investigacion de seguridad/identidad); controles SP 800-53 adaptados a agentes, incl. chain-of-custody
  logging y multi-agent trust boundaries. **MATIZ VERIFICADO: las ventanas de comentario publico YA
  CERRARON (AI Agents: 9-mar-2026; Identity/Authorization: 2-abr-2026).** La via de entrada ya no es el
  comment period sino los pilares permanentes (proceso industria + open-source) y los canales OpenSSF/CSA.
  Implicacion: las ventanas de esta categoria se cierran EN SERIE; la urgencia es real, no retorica.

### 2.3 Demanda con dinero HOY
- NO es el EU AI Act (alto-riesgo pospuesto a dic-2027 por el Digital Omnibus; no cubre dev-tools per se).
- SI es: auditores SOC 2 / ISO 42001 que YA piden atribucion de cada cambio generado por IA a sesion
  autorizada, least-privilege de agentes y change-management identico al humano (SOC 2 CC8.1); ISO 42001
  con traccion por cadena de suministro (Microsoft SSPA exige controles IA a proveedores; KPMG primera
  Big4 certificada dic-2025). Gartner: gasto en plataformas de AI governance $492M en 2026, >$1B en 2030.
- Miedo post-incidentes: agente de Replit borro DB de produccion en code-freeze y mintio (jul-2025);
  wiper inyectado en Amazon Q distribuido a ~1M devs (jul-2025); 93% de CTOs/CISOs preocupados por codigo
  vibe-coded (Retool 2026).
- Comprador liquido: el VENDOR de software que necesita pasar auditoria para vender a enterprise;
  el CISO/compliance de regulados (finanzas, salud, gobierno).

### 2.4 Precedentes (quien capturo valor en jugadas metodologia/estandar + evidencia)
- Capturo el que poseia un COMPLEMENTO ESCASO, nunca la spec en si: Scrum -> certificacion;
  Sigstore/in-toto -> Chainguard ($3.5B vendiendo el artefacto verificado); Git -> GitHub (capa de
  producto); LangChain -> LangSmith (telemetria hosted). semver/conventional-commits: valor enorme,
  captura CERO (spec sin motor de evidencia). Wardley regalo todo sin vehiculo: solo reputacion.
  C4 (Simon Brown): techo realista de una persona -- libro + workshops + tooling propio.
- in-toto/SLSA: los academicos capturaron CARRERA (catedras, autoridad); el dinero lo capturo quien
  productizo encima. Leccion de licencia: HashiCorp/BUSL retrofit quemo confianza -> decidir frontera
  abierto/cerrado el DIA 1.

---

## 3. La pregunta que surge

El operador concluyo: (a) no quiere deuda de mantenimiento perpetua con la app de otro (fork muerto);
(b) contra Claude Code / Codex / VS Code / Antigravity / OpenCode no se compite (son los grandes);
(c) su activo real es "metodologia de gobierno de agentes con evidencia medida"; (d) teme que un
prototipo-producto sea copiado/absorbido por los grandes en ~3 meses.

**Pregunta: cual es la estrategia que maximiza el valor capturable de ese activo, para UNA persona sin
funding, sin competir con los grandes, y que hace del miedo-a-la-copia algo manejable?**

---

## 4. Hipotesis del pivote (HP1-HP5; cada una FALSABLE -- el revisor debe intentar refutarlas)

**HP1. El activo diferencial es la metodologia + evidencia pre-registrada + posicion neutral; NO el
software de producto.**
A favor: hueco de mercado verificado (2.1: nadie atesta el ciclo multi-agente completo); el corpus
(2,416 eventos, dataset sellado con hipotesis pre-registradas y fechadas) no se retro-fabrica; la
neutralidad es estructural (GitHub firmando logs de Copilot es self-attestation; Anthropic no puede
certificar agentes de OpenAI). Refutacion posible: si la evidencia no resiste peer review (angulo 9.1)
o si la metodologia no es transferible (N=1, angulo 9.3), el activo se reduce a expertise personal.

**HP2. La ventana de estandarizacion esta abierta AHORA y sin implementacion de referencia.**
A favor: Hinds pide colaboracion (ene-2026, verificado); NIST CAISI lanzada feb-2026 con accountability
chains como gap y sin implementacion de referencia; nuestro protocolo es superset de la taxonomia de
Hinds. En contra (verificado): los comment periods de NIST YA cerraron -- la entrada facil paso; quedan
los pilares permanentes. Refutacion posible: si en los procesos ya hay una implementacion de referencia
candidata que la investigacion no vio, HP2 cae.

**HP3. El riesgo dominante es IRRELEVANCIA por no-publicacion, no la copia.**
A favor: lo publicado con fecha (DOI/arXiv) convierte la copia en adopcion citable ("implementaron lo
que yo defini"); lo no publicado no se puede adoptar, citar ni comprar; los grandes ya convergen SOLOS
(Antigravity Artifacts, nono) sin haber leido nuestro repo -- la convergencia ocurre con o sin nosotros.
Refutacion posible: mostrar un mecanismo por el cual publicar destruya valor apropiable que hoy exista
(el revisor deberia intentarlo y, si no lo encuentra, conceder HP3).

**HP4. Para una persona sola, la captura viene de un complemento escaso (implementacion de referencia
citada + corpus de evidencia + herramienta minima verificable), no de poseer la spec ni de una app.**
A favor: patron uniforme en 2.4. Refutacion posible: contraejemplo de creador solo que capturo valor
poseyendo la spec (no lo encontro la investigacion) o argumento de que ninguno de los complementos
propuestos es realmente escaso.

**HP5. El vehiculo minimo viable cabe en 90 dias de UNA persona con agentes: dataset con DOI + preprint
+ spec-repo Apache-2.0 + servidor MCP minimo + GitHub Action de verificacion.**
A favor: todos los artefactos derivan de material existente (el dataset esta sellado, el informe HTML
existe, el core es extraible, el ledger ya tiene API de facto); los agentes ejecutan en paralelo.
Refutacion posible: el TFM (deadline + normas de la universidad sobre publicacion previa, angulo 9.8)
o la capacidad real (angulo 9.4) pueden romper el calendario.

---

## 5. Planteamiento: la apuesta compuesta "PUBLICAR PARA SER CITADO"

Orden estricto: evidencia academica -> contribucion a los DOS procesos abiertos -> herramienta minima
como demo viva. Servicios: SOLO inbound (max 2 assessments, caso de estudio obligatorio). Absorcion:
se cosecha, no se persigue. Regla de gobierno: CADA SEMANA sale a publico algo fechado y verificable.

### 5.1 Primeros 90 dias
- S1-2: congelar alcance del TFM. Publicar dataset N=500 + verificador + metodo en Zenodo con DOI
  (prior art fechado e inmutable). Medir y documentar el overhead honesto POR TAREA (eventos, tiempo de
  pared, intervenciones manuales) -- neutralizar el ataque antes de que lo haga un critico.
- S3-4: preprint en arXiv (ingles) con reencuadre honesto (s.7). Landing de 1 pagina: los 3 numeros +
  "verificalo tu mismo en 5 comandos".
- S5-6: extraer el core a spec-repo publico Apache-2.0, en ingles, SIN residuos de instancia (validador
  Python como normativo; nada de mailbox en espanol ni rutas Windows como parte de la spec). Posicionar
  como "reference implementation + input a estandarizacion", NO como estandar rival. (Este trabajo
  absorbe la Fase 0 de memoria-hibrida: separar normativo / instancia / historia.)
- S7-8: respuesta publica y contacto directo a Hinds (su llamada sigue abierta, verificado) con datos y
  mapping explicito de nuestro superset a su taxonomia Plan/Generation/Approval. Engagement con NIST
  CAISI via pilares permanentes (industria + open-source) y canales OpenSSF/CSA (los comment periods
  cerraron). Documento de mapping a SOC 2 CC8.1 / ISO 42001 / AI Act Art. 12.
- S9-11: unico codigo nuevo: servidor MCP minimo (claim / attest / review / close sobre el ledger,
  usable desde CUALQUIER agente) publicado en npm con quickstart de 10 minutos + GitHub Action
  `verify-agent-ledger` con badge. Nuestro propio repo como demo (2,416 eventos reales).
- S12-13: anuncio (HN, X), defensa del TFM alineada, 15-20 conversaciones con CTOs de software
  factories que venden a regulados -- para aprender y detectar inbound, no para vender.

### 5.2 Meses 4-12: kill/persevere por apuesta
- Contribucion-a-estandar: persevere si a mes 6 hay interaccion sustantiva (respuesta de Hinds/CAISI,
  issue externo serio, cita). KILL a mes 9 con cero interaccion: congelar spec como artefacto academico.
- Herramienta (MCP+Action): persevere con >=3 usuarios externos reales o 1 design partner a mes 9.
  KILL: congelar como demo del paper.
- **Metrica reina: 2 instancias EXTERNAS corriendo el protocolo a mes 12, o la tesis de transferibilidad
  muere** -- y con ella la via producto; lo que queda es expertise (que se cobra como carrera, dicho sin
  eufemismos).
- Servicios: solo inbound, max 2, precio ancla. Absorcion: revisar senales a mes 12 (issues de
  ingenieros de grandes, invitacion NIST/OpenSSF, piloto de auditora).

### 5.3 Que pasa con lo existente
- Pipeline: cerrar 0229 (in_review); CANCELAR con razon 0230 (WS2 bootstrapper del fork) y 0232 (WS3.5
  instalador del fork); RE-ALCANZAR 0233 (e2e -> "instancia externa desde template") y 0234 (runbooks ->
  plan de publicacion). Requiere DECISION formal que redefina la meta de REQ-ZEUS-001 / DECISION-0077 y
  supersede la parte de D4 (fork como producto).
- REQs futuros: anti-vibecoding SE PROMUEVE (declaracion -> narrativa del paper/spec; registro de
  excepciones -> feature de la spec). Intake SE PARTE (gate determinista de obligatorios -> spec/perfil;
  UI -> diferida a kill-criterion). Memoria hibrida DIFERIDA (Fase 0 absorbida por extraccion de spec).
  Aprendizajes-externos -> materia prima del paper. Beta publica CONGELADA (REQ-PUB-003/004/012 se
  reciclan para MCP/Action). Instalacion-poderes-db MUERE con el fork.
- Freeze del core del protocolo salvo bugs; el ledger deja de crecer como fin en si mismo.

---

## 6. Por que (resumen causal)
1. El hueco existe y esta verificado (2.1); nadie lo ocupa; los que definiran el estandar lo declararon
   abierto (2.2) -- pero las ventanas cierran en serie (comment periods ya cerrados).
2. El activo no-copiable es la evidencia fechada + el corpus + la neutralidad (2.1/2.3); todo lo demas
   (conceptos, codigo del ledger) es copiable en un sprint por un equipo grande -- defenderlo
   construyendo producto es perder; defenderlo publicando primero es ganar aunque te copien.
3. Los precedentes (2.4) muestran que una persona captura via complemento escaso; la spec sola es
   filantropia; la app sola es pelear contra los grandes con 1 persona.
4. La demanda con dinero (2.3) pide exactamente lo que el ledger da (atribucion + change-management +
   tamper-evidence) -- pero la compra via certificacion/auditoria, no via plugin de un individuo:
   por eso la ruta es credibilidad/estandar primero, monetizacion despues.

---

## 7. Concesiones YA aceptadas (el pivote las incorpora; el revisor debe verificar que son suficientes)
1. maker!=checker operado por UNA persona NO es segregacion de funciones organizacional. Reencuadre
   obligatorio en toda pieza publica: "heterogeneidad de agentes con veredicto firmado" -- control
   tecnico complementario.
2. H1-H3 miden tamper-evidence y overhead estructural, NO reduccion de defectos/retrabajo. Claim
   estrecho: "ciclo multi-agente completo con integridad verificable por terceros a costo despreciable,
   con numeros publicados y pre-registrados". No prometer mas.
3. El costo de PROCESO por tarea no esta medido y es visible en nuestro propio ledger: medirlo y
   publicarlo NOSOTROS en S1-2 (honestidad preventiva como marca).
4. N=1 declarado como limitacion central en el preprint; por eso la metrica reina son instancias
   externas, no features.

---

## 8. Riesgos de la propia hipotesis (con mitigacion)
- R1 Silencio total (publicar y que nadie responda): mitigacion = anclas con destinatario concreto
  (Hinds pide contacto directo; CSA/OpenSSF activos), 15-20 conversaciones dirigidas, kill-criteria que
  convierten el silencio en decision a mes 9, no en agonia.
- R2 Peer review hostil de H1-H3 ("tautologico"): mitigacion = claim estrecho (7.2) + publicar el
  overhead de proceso antes que un critico + el valor real es el ARTEFACTO reproducible, no la novedad
  criptografica.
- R3 nono u otro agrega multi-agente antes que nosotros: mitigacion = velocidad (S1-4 en un mes) +
  nuestro diferencial no es el trail sino el CICLO (claims, maker!=checker, excepciones) + colaborar en
  vez de competir (mismo ecosistema Sigstore).
- R4 El TFM restringe publicacion previa (normas de la universidad): VERIFICAR EN S1 antes de Zenodo;
  si restringe, invertir orden (defensa primero, publicacion inmediata despues) sin romper la secuencia.
- R5 Capacidad: 13 semanas con defensa de TFM en medio: mitigacion = los agentes producen, el operador
  decide/publica; el plan tiene UNA cosa publicable por semana, no cinco.

---

## 9. ANGULOS ADVERSARIALES para el revisor (atacar, y sumar los que falten)
1. **Evidencia**: H1-H3 resiste revision externa hostil? La inyeccion programatica de ataques contra la
   propia cadena, es un test real o un test que solo puede pasar? Que ataque NO detectaria el esquema
   (colusion de firmantes, re-genesis malicioso, compromiso de claves)?
2. **Anclas**: el mapping de nuestro protocolo a Plan/Generation/Approval de Hinds es correcto o
   forzado? Hay YA una implementacion de referencia candidata en CAISI/OpenSSF que no vimos?
3. **Transferibilidad**: que evidencia MINIMA convenceria a un tercero de que el protocolo funciona sin
   su autor? El wrapper new_instance + NOVA es suficiente para que un externo instancie sin ayuda?
4. **Calendario**: S1-13 es realista con la defensa del TFM en medio? Que semana es la primera en caer?
5. **Cancelacion gobernada**: cancelar 0230/0232 y re-alcanzar 0233/0234 deja deuda en el ledger o
   rompe compromisos de DECISION-0077? Cual es el costo de la DECISION de redefinicion?
6. **Extraccion de la spec**: el core REALMENTE se separa de la instancia (validador PS1/Windows,
   espanol, rutas)? Cuanto trabajo es "sin residuos de instancia" de verdad?
7. **Licencia/marca**: Apache-2.0 para el core es la frontera correcta el dia 1? Que queda cerrado
   (corpus? marca? certificacion futura?) y esta bien elegido?
8. **TFM**: las normas de la universidad permiten preprint/dataset publico ANTES de la defensa?
   (Bloqueante de S1-4 si no.)
9. **El claim de unicidad**: "nadie atesta el ciclo multi-agente completo" -- sobrevive a una busqueda
   adversarial dedicada (academia china/europea, tools internos de Big4)?
10. **Kill-criteria**: son falsables y estan bien calibrados, o son tan generosos que garantizan 12
    meses de inversion sin senal? La metrica reina (2 instancias externas) es alcanzable o es un
    kill-criterion disfrazado de meta?

---

## 10. Pregunta de cierre para el revisor
Veredicto GO / NO-GO / CAMBIO-REQUERIDO sobre el pivote como hipotesis de trabajo: cuales de HP1-HP5
quedan en pie tras tu ataque, que angulo de s.9 resulto letal (si alguno), y que cambiarias del plan de
90 dias antes de que el operador lo formalice como directiva + DECISION.
