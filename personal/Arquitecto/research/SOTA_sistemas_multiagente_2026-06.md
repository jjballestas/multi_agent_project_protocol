# Estado del arte: sistemas multiagente LLM con runtime event-sourced, seguridad por capacidad y release engineering verificable

**Fecha:** 2026-06-12 · **Autor:** Claude (Arquitecto Orquestador) · **Para:** Jball
**Objetivo:** mapa riguroso de la literatura (2015–2026) en los seis pilares de la metodología, con URLs de descarga verificadas, venues y gaps de investigación para elevar el protocolo a nivel doctoral.

**Convenciones de rigor:**
- `[PR]` peer-reviewed · `[PP]` preprint arXiv · `[LG]` literatura gris / industrial / estándar / regulación
- ✅ URL verificada por fetch directo o concordancia multi-índice · ⚠️ no verificada de forma independiente (existe en resultados de búsqueda pero no se confirmó el binario/página)
- Excluido todo lo relativo a blockchain/web3. "Tokens" = tokens de inferencia LLM.

---

## Síntesis ejecutiva

Los seis pilares de tu metodología tienen literatura activa pero **fragmentada**: cada uno vive en una comunidad distinta (sistemas distribuidos, seguridad, ingeniería de software, NLP/ML, AI safety, gobernanza) y **nadie ha publicado aún una integración de las seis capas en un solo protocolo evaluado empíricamente**. Eso es precisamente la oportunidad doctoral: la intersección está casi vacía mientras cada componente individual ya tiene vocabulario, benchmarks y venues donde publicar.

Hallazgos transversales clave:

1. **El patrón event-sourced ya llegó a los agentes** (ESAA 2026, OpenHands SDK 2025) pero sin semántica formal de replay para computación no determinista, y desconectado de los estándares de provenance (W3C PROV / PROV-AGENT).
2. **La seguridad por capacidad es la dirección dominante contra prompt injection** (CaMeL de Google DeepMind es la referencia central), pero no existe delegación atenuante estándar para cadenas humano→agente→subagente.
3. **SLSA/in-toto/Sigstore atestan builds, no autoría de cambios por agentes** — el "contribuidor agente" no tiene modelo de provenance ni de amenazas propio.
4. **El coste dominante en SE agéntico está en la revisión/verificación, no en la generación** (59,4% de tokens en code review según Tokenomics 2026); no hay estándar de cost attribution por handoff.
5. **MAST (Berkeley) demuestra que la mayoría de fallos multiagente son de coordinación** (desalineación inter-agente, verificación ausente), no del modelo individual — validando el énfasis de tu protocolo en handoffs autocontenidos y verificación.
6. **Las paradas duras tienen teoría (interruptibilidad, corrigibilidad) y mandato legal (EU AI Act art. 14), pero no mecánica para N agentes**: nadie ha resuelto la parada en cascada consistente con tareas en vuelo y estado compartido.

---

## Pilar 1 — Runtime event-sourced e integridad/auditabilidad de estado

### Fundamentos

| # | Referencia | Tipo | PDF/URL |
|---|---|---|---|
| 1.1 | Fowler, *Event Sourcing*, 2005 | [LG] ✅ | https://martinfowler.com/eaaDev/EventSourcing.html |
| 1.2 | Schneider, *Implementing Fault-Tolerant Services Using the State Machine Approach*, ACM Computing Surveys 22(4), 1990 | [PR] ✅ | https://www.cs.cornell.edu/fbs/publications/SMSurvey.pdf (DOI: 10.1145/98163.98167) |
| 1.3 | Moreau & Missier (eds.), *PROV-DM: The PROV Data Model*, W3C Recommendation, 2013 | [LG] ✅ | https://www.w3.org/TR/prov-dm/ |
| 1.4 | Chen et al., *Deterministic Replay: A Survey*, ACM Computing Surveys 48(2), 2015 | [PR] ✅ | https://dl.acm.org/doi/10.1145/2790077 (sin open access) |

- **1.1** define el patrón: estado siempre reconstruible desde un log de eventos; fundamento directo de los runtimes agénticos modernos.
- **1.2** explica por qué el no-determinismo del LLM debe aislarse fuera del bucle de orquestación (principio workflow-determinista de Temporal).
- **1.4** es el marco contra el que se mide la novedad: el no-determinismo del LLM no es capturable como el de un scheduler.

### Agentes LLM (2024–2026)

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 1.5 | Santos Filho, *ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering*, 2026 | [PP] ✅ (verificado por fetch) | https://arxiv.org/pdf/2602.23193 |
| 1.6 | Santos Filho, *ESAA-Security*, 2026 | [PP] ✅ | https://arxiv.org/pdf/2603.06365 |
| 1.7 | Dong, Lu, Zhu (CSIRO), *AgentOps: Enabling Observability of LLM Agents*, 2024 | [PP] ✅ | https://arxiv.org/pdf/2411.05285 |
| 1.8 | Cemri et al. (UC Berkeley), *Why Do Multi-Agent LLM Systems Fail?* (MAST), 2025 | [PP] ✅ (verificado por fetch) | https://arxiv.org/pdf/2503.13657 |
| 1.9 | Souza et al. (ORNL), *PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions*, IEEE e-Science 2025 | [PR] ✅ | https://arxiv.org/pdf/2508.02866 |
| 1.10 | Feng et al. (SJTU), *LLM Agents with Record & Replay* (AgentRR), 2025 | [PP] ✅ | https://arxiv.org/pdf/2505.17716 |
| 1.11 | Wang et al., *The OpenHands Software Agent SDK*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2511.03690 |
| 1.12 | Zhang, *Right to History: A Sovereignty Kernel for Verifiable AI Agent Execution*, 2026 | [PP] ✅ | https://arxiv.org/pdf/2602.20214 |
| 1.13 | *From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents*, 2026 | [PP] ✅ | https://arxiv.org/pdf/2606.04990 |
| 1.14 | *ACRFence: Preventing Semantic Rollback Attacks in Agent Checkpoint-Restore*, 2026 | [PP] ⚠️ | https://arxiv.org/pdf/2603.20625 |
| 1.15 | Temporal, *durable execution para agentes*, 2024–2026 | [LG] ✅ | https://temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal |

- **1.5 (ESAA)** es el paper más alineado con tu metodología: separa la intención cognitiva del LLM (JSON estructurado) de la mutación de estado, ejecutada por un orquestador determinista sobre log append-only con proyecciones verificadas por hash.
- **1.8 (MAST)** — 14 modos de fallo en 3 categorías sobre 1.600+ trazas; demuestra que la inspección de trazas es el mecanismo central de atribución de fallos.
- **1.11 (OpenHands SDK)** — evidencia de adopción a escala del event sourcing en agentes de producción: toda interacción es evento inmutable del que se deriva el estado.
- **1.12** formaliza el "derecho a la historia": logging tamper-evident con cinco invariantes, motivado por el EU AI Act (sin blockchain).

**Venues:** arXiv cs.AI/cs.SE/cs.MA (mayoría preprint — campo sin venue consolidado), IEEE e-Science, comunidad provenance (IPAW/TaPP), SOSP/OSDI/EuroSys emergente, ACM CSUR para fundamentos.

**Gaps:**
- **G1.1 — Semántica formal de replay no determinista.** No existe teoría de *equivalencia semántica de ejecuciones*: cuándo dos trazas divergentes cuentan como "la misma" ejecución a efectos de auditoría y recuperación.
- **G1.2 — Unificar runtime event-sourced y provenance normativa.** El log operativo (recuperación) y el grafo PROV (cumplimiento) son hoy artefactos separados que pueden contradecirse.
- **G1.3 — Evaluación académica de durable execution con cargas agénticas.** El modelo Temporal/Restate domina la práctica sin trabajo arbitrado que mida sus garantías; auditabilidad inter-agente entre fronteras de confianza casi sin explorar.

---

## Pilar 2 — Seguridad por capacidad y control de privilegios

### Fundamentos clásicos

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 2.1 | Dennis & Van Horn, *Programming Semantics for Multiprogrammed Computations*, CACM 9(3), 1966 | [PR] ✅ | https://dl.acm.org/doi/pdf/10.1145/365230.365252 |
| 2.2 | Saltzer & Schroeder, *The Protection of Information in Computer Systems*, Proc. IEEE 63(9), 1975 | [PR] ✅ | http://web.mit.edu/Saltzer/www/publications/protection/ |
| 2.3 | Miller, *Robust Composition* (tesis doctoral, object-capability model, lenguaje E), Johns Hopkins, 2006 | [LG] ⚠️ (URL canónica histórica) | http://www.erights.org/talks/thesis/markm-thesis.pdf |
| 2.4 | Watson et al., *Capsicum: Practical Capabilities for UNIX*, USENIX Security 2010 | [PR] ✅ | https://www.usenix.org/legacy/event/sec10/tech/full_papers/Watson.pdf |

### Agentes LLM (2024–2026)

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 2.5 | Debenedetti et al. (Google DeepMind/ETH), *Defeating Prompt Injections by Design* (CaMeL), IEEE SaTML | [PR] ✅ (verificado por fetch) | https://arxiv.org/pdf/2503.18813 |
| 2.6 | Debenedetti et al., *AgentDojo* (benchmark), NeurIPS 2024 D&B | [PR] ✅ | https://arxiv.org/pdf/2406.13352 |
| 2.7 | Costa et al. (Microsoft), *Securing AI Agents with Information-Flow Control* (FIDES), 2025 | [PP] ✅ | https://arxiv.org/pdf/2505.23643 |
| 2.8 | Shi et al. (UC Berkeley), *Progent: Programmable Privilege Control for LLM Agents*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2504.11703 |
| 2.9 | Wu et al., *IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems*, NDSS 2025 | [PR] ✅ | https://arxiv.org/pdf/2403.04960 |
| 2.10 | Ruan et al., *ToolEmu: Identifying the Risks of LM Agents with an LM-Emulated Sandbox*, ICLR 2024 | [PR] ✅ | https://arxiv.org/pdf/2309.15817 |
| 2.11 | Bagdasarian et al. (Google), *AirGapAgent*, ACM CCS 2024 | [PR] ✅ | https://arxiv.org/pdf/2405.05175 |
| 2.12 | Beurer-Kellner et al., *Design Patterns for Securing LLM Agents against Prompt Injections*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2506.08837 |
| 2.13 | South et al. (MIT), *Authenticated Delegation and Authorized AI Agents*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2501.09674 |
| 2.14 | Kim et al. (SNU), *Prompt Flow Integrity to Prevent Privilege Escalation* (PFI), 2025 | [PP] ✅ | https://arxiv.org/pdf/2503.15547 |
| 2.15 | Zhang et al. (Purdue/IBM), *LLM Agents Should Employ Security Principles*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2505.24019 |

- **2.5 (CaMeL)** es la referencia central del pilar: LLM privilegiado + LLM en cuarentena + intérprete que adjunta **capabilities a cada valor** y aplica políticas en cada tool call. 77% de tareas de AgentDojo con seguridad demostrable (84% sin defensa). Verificado: abstract confirma el uso explícito de capabilities.
- **2.8 (Progent)** — DSL de políticas sobre tool calls con mínimo privilegio; **2.7 (FIDES)** — etiquetas de confidencialidad/integridad con propagación dinámica (IFC).
- **2.13** cubre la capa de identidad/delegación (extensión de OAuth/OIDC para agentes) que las capabilities en runtime no abordan.

**Venues:** NDSS, ACM CCS, USENIX Security, IEEE S&P, IEEE SaTML (emergente, especializado), NeurIPS/ICLR para benchmarks.

**Gaps:**
- **G2.1 — Brecha utilidad–garantía formal.** Los enfoques con garantías sobre-restringen; falta atenuación dinámica de autoridad sin degradar utilidad, y benchmarks que midan ese coste.
- **G2.2 — Delegación atenuante multi-agente.** No hay mecanismo estándar verificado para cadenas humano→agente→subagente→herramienta con atenuación demostrable (el modelo ocap de Miller sin traducción a infraestructura web).
- **G2.3 — Síntesis y verificación de políticas.** Usar el LLM para generar políticas (Progent) reintroduce el componente no confiable en el TCB.

---

## Pilar 3 — Release engineering verificable y supply chain con agentes

### Supply chain clásico

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 3.1 | Lamb & Zacchiroli, *Reproducible Builds: Increasing the Integrity of Software Supply Chains*, IEEE Software 39(2), 2022 (Best Paper) | [PR] ✅ | https://arxiv.org/pdf/2104.06020 |
| 3.2 | Torres-Arias et al., *in-toto: Providing farm-to-table guarantees for bits and bytes*, USENIX Security 2019 | [PR] ✅ | https://www.usenix.org/system/files/sec19-torres-arias.pdf |
| 3.3 | Newman, Meyers, Torres-Arias, *Sigstore: Software Signing for Everybody*, ACM CCS 2022 | [PR] ✅ | https://dl.acm.org/doi/10.1145/3548606.3560596 (open access CC-BY) |
| 3.4 | Ladisa et al., *SoK: Taxonomy of Attacks on Open-Source Software Supply Chains*, IEEE S&P 2023 | [PR] ✅ | https://arxiv.org/pdf/2204.04008 |
| 3.5 | Williams et al., *Research Directions in Software Supply Chain Security*, ACM TOSEM 2025 | [PR] ⚠️ | https://dl.acm.org/doi/10.1145/3714464 |
| 3.6 | OpenSSF, *SLSA v1.0*, 2023 | [LG] ✅ | https://slsa.dev/spec/v1.0/ |
| 3.7 | NIST SP 800-218 (SSDF v1.1), 2022 — ver también borrador 800-218A (IA generativa) | [LG] ✅ | https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-218.pdf |
| 3.8 | Tamanna et al., *Analyzing Challenges in Deployment of the SLSA Framework*, 2024 | [PP] ⚠️ | https://arxiv.org/pdf/2409.05014 |

### Código generado por IA y agentes de SE

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 3.9 | Pearce et al., *Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions*, IEEE S&P 2022 | [PR] ✅ | https://arxiv.org/pdf/2108.09293 |
| 3.10 | Perry et al., *Do Users Write More Insecure Code with AI Assistants?*, ACM CCS 2023 | [PR] ✅ | https://arxiv.org/pdf/2211.03622 |
| 3.11 | Sun et al., *Clover: Closed-Loop Verifiable Code Generation*, SAIV 2024 (Springer LNCS) | [PR] ✅ | https://arxiv.org/pdf/2310.17807 |
| 3.12 | Jimenez et al., *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*, ICLR 2024 | [PR] ✅ | https://arxiv.org/pdf/2310.06770 |
| 3.13 | Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*, NeurIPS 2024 | [PR] ✅ | https://arxiv.org/pdf/2405.15793 |
| 3.14 | Liu et al., *LLM-Based Agents for Software Engineering: A Survey*, 2024 | [PP] ✅ | https://arxiv.org/pdf/2409.02977 |
| 3.15 | OpenAI, *SWE-bench Verified*, 2024 (deprecado en 2026 por contaminación — lección metodológica) | [LG] ✅ | https://openai.com/index/introducing-swe-bench-verified/ |

- **3.9 + 3.10** establecen empíricamente que el código generado por LLM es entrada no confiable (~40% vulnerable) y que la revisión humana no basta (falsa sensación de seguridad) → argumento directo para gates mecanizados y provenance.
- **3.2 (in-toto)** es el sustrato natural para encadenar atestaciones de pasos ejecutados por agentes; **3.13 (SWE-agent)** define la interfaz agente-computadora (ACI) que es exactamente el punto de instrumentación para registrar esas atestaciones.

**Venues:** USENIX Security, ACM CCS, IEEE S&P, ICSE/FSE/ASE, ACM TOSEM, IEEE TSE; ICLR/NeurIPS para benchmarks; OpenSSF/NIST para estándares.

**Gaps:**
- **G3.1 — Provenance de cambios hechos por agentes.** SLSA/in-toto/Sigstore atestan *builds*, no *autoría*: no hay formato estándar que capture qué agente (modelo, versión, prompt, traza) produjo un patch ni cómo encadenarlo hasta el release. **La intersección pilares 3×1 está vacía.**
- **G3.2 — Verificación escalable más allá de tests.** Tests preexistentes son frágiles/contaminables; verificación formal (Clover/Dafny) no escala a lenguajes reales. Falta el punto intermedio integrable en CI/CD.
- **G3.3 — Modelo de amenazas del "contribuidor agente".** Prompt injection vía issues/dependencias, exceso de confianza del revisor en PRs de agentes, y ¿quién firma: el agente, el orquestador o el humano que aprueba?

---

## Pilar 4 — Economía de tokens LLM en sistemas multiagente

### Cascadas, routing y compresión

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 4.1 | Chen, Zaharia, Zou, *FrugalGPT*, 2023 (luego TMLR 2024) | [PP] ✅ | https://arxiv.org/pdf/2305.05176 |
| 4.2 | Jiang et al., *LLMLingua: Compressing Prompts*, EMNLP 2023 | [PR] ✅ | https://arxiv.org/pdf/2310.05736 |
| 4.3 | Pan et al., *LLMLingua-2*, Findings of ACL 2024 | [PR] ✅ | https://arxiv.org/pdf/2403.12968 |
| 4.4 | Zhou et al., *A Survey on Efficient Inference for LLMs*, 2024 | [PP] ✅ | https://arxiv.org/pdf/2404.14294 |
| 4.5 | Ong et al., *RouteLLM: Learning to Route LLMs with Preference Data*, ICLR 2025 | [PR] ✅ | https://arxiv.org/pdf/2406.18665 |
| 4.6 | Li et al., *Survey on LLM Acceleration based on KV Cache Management*, 2024–25 | [PP] ✅ | https://arxiv.org/pdf/2412.19442 |

### Comunicación multiagente y presupuestos

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 4.7 | Zhang et al., *Cut the Crap* (AgentPrune), ICLR 2025 | [PR] ✅ | https://arxiv.org/pdf/2410.02506 |
| 4.8 | Chen et al. (THUNLP), *Optima*, Findings of ACL 2025 | [PR] ✅ | https://arxiv.org/pdf/2410.08115 |
| 4.9 | Wang et al., *AgentDropout*, ACL 2025 | [PR] ✅ | https://arxiv.org/pdf/2503.18891 |
| 4.10 | Lin et al., *Stop Wasting Your Tokens* (SupervisorAgent), ICLR 2026 | [PR] ✅ | https://arxiv.org/pdf/2510.26585 |
| 4.11 | Yang et al., *CodeAgents: Token-Efficient Codified Multi-Agent Reasoning*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2507.03254 |
| 4.12 | *BudgetThinker: Budget-Aware Reasoning with Control Tokens*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2508.17196 |
| 4.13 | Salim et al. (Concordia), *Tokenomics: Quantifying Where Tokens Are Used in Agentic SE*, 2026 | [PP] ✅ (verificado por fetch) | https://arxiv.org/pdf/2601.14470 |
| 4.14 | *How Do AI Agents Spend Your Money?*, 2026 | [PP] ⚠️ | https://arxiv.org/pdf/2604.22750 |
| 4.15 | SuDIS (Zhejiang), *Token Economics for LLM Agents: A Dual-View Study*, 2026 | [PP] ⚠️ | https://arxiv.org/pdf/2605.09104 |

- **4.13 (Tokenomics)** — hallazgo verificado por fetch: en ChatDev con modelo de razonamiento GPT-5, el *code review* iterativo consume **59,4%** de los tokens y el input es **53,9%** del total. El coste dominante está en la verificación entre agentes, no en la generación.
- **4.7 (AgentPrune)** formaliza la "redundancia de comunicación" y poda el grafo de mensajes: 28–72% menos tokens.
- **4.11 (CodeAgents)** — handoffs en pseudocódigo tipado vs. prosa libre: −55–87% tokens de entrada. Argumento directo a favor de handoffs estructurados como los de tu protocolo.

**Venues:** ICLR, ACL/EMNLP, arXiv cs.MA/cs.CL/cs.SE.

**Gaps:**
- **G4.1 — Cost attribution por handoff/decisión/agente.** Existe medición agregada por fase; no hay estándar que impute tokens a cada handoff ni telemetría comparable entre frameworks.
- **G4.2 — Presupuestos dinámicos con garantías.** Falta asignación de presupuesto entre agentes con contratos de recursos y degradación elegante cuando se agota a mitad de workflow.
- **G4.3 — Trade-off compresión vs. fiabilidad/auditabilidad.** Casi nadie cuantifica el efecto de comprimir handoffs sobre fallos en cascada y trazabilidad humana.

---

## Pilar 5 — Coordinación N-agente: protocolos, orquestación, handoffs

### Clásicos MAS

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 5.1 | Smith, *The Contract Net Protocol*, IEEE Trans. Computers C-29(12), 1980 | [PR] ✅ | https://www.reidgsmith.com/The_Contract_Net_Protocol_Dec-1980.pdf |
| 5.2 | Finin et al., *KQML as an Agent Communication Language*, CIKM 1994 | [PR] ✅ | https://dl.acm.org/doi/pdf/10.1145/191246.191322 |
| 5.3 | FIPA, *ACL Message Structure Specification* (SC00061G), 2002 | [LG] ⚠️ | http://www.fipa.org/specs/fipa00061/SC00061G.pdf |
| 5.4 | Rao & Georgeff, *BDI Agents: From Theory to Practice*, ICMAS 1995 | [PR] ⚠️ | https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf |

- **5.1** es el ancestro directo del mecanismo claim/ownership de tareas de tu protocolo (anuncio → puja → adjudicación → contrato).
- **5.4 (BDI)** — el estado intencional que los handoffs LLM deben serializar explícitamente porque el LLM no lo mantiene.

### Frameworks LLM y protocolos (2023–2026)

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 5.5 | Li et al., *CAMEL: Communicative Agents*, NeurIPS 2023 | [PR] ✅ | https://arxiv.org/pdf/2303.17760 |
| 5.6 | Wu et al., *AutoGen*, COLM 2024 | [PR] ✅ | https://arxiv.org/pdf/2308.08155 |
| 5.7 | Hong et al., *MetaGPT: Meta Programming for Multi-Agent Collaboration*, ICLR 2024 (oral) | [PR] ✅ | https://arxiv.org/pdf/2308.00352 |
| 5.8 | Qian et al., *ChatDev: Communicative Agents for Software Development*, ACL 2024 | [PR] ✅ | https://aclanthology.org/2024.acl-long.810.pdf |
| 5.9 | Anthropic/comunidad, *Model Context Protocol — Specification*, 2024– | [LG] ✅ | https://modelcontextprotocol.io/specification |
| 5.10 | Google → Linux Foundation, *Agent2Agent (A2A) Protocol*, 2025 | [LG] ✅/⚠️ | https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/ · spec: https://a2a-protocol.org |
| 5.11 | Yang et al. (SJTU), *A Survey of AI Agent Protocols*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2504.16736 |
| 5.12 | Ehtesham et al., *Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2505.02279 |
| 5.13 | Hou et al., *MCP: Landscape, Security Threats, and Future Research Directions*, ACM TOSEM 2026 | [PR] ✅ | https://arxiv.org/pdf/2503.23278 |
| 5.14 | Guo et al., *LLM-based Multi-Agents: A Survey*, IJCAI 2024 Survey Track | [PR] ✅ | https://arxiv.org/pdf/2402.01680 |
| 5.15 | He, Treude, Lo, *LLM-Based Multi-Agent Systems for SE: Literature Review, Vision and the Road Ahead*, ACM TOSEM | [PR] ✅ | https://arxiv.org/pdf/2404.04834 |
| (5.16) | Cemri et al., MAST — ver 1.8 | [PP] ✅ | https://arxiv.org/pdf/2503.13657 |

- **5.7 (MetaGPT)** — el argumento empírico más fuerte a favor de handoffs por **artefactos estructurados** (documentos de diseño, interfaces tipadas) frente a chat libre: exactamente el patrón de tu `Area_comun/`.
- **5.8 (ChatDev)** — chat chain = protocolo de handoff secuencial con verificación en recepción (*communicative dehallucination*: el receptor pide detalles antes de responder).
- **5.15** es el survey más alineado con "equipo de agentes que mantiene software": señala memoria compartida, asignación de roles y colaboración humano-agente como retos abiertos.

**Venues:** AAMAS/JAAMAS (MAS histórico), NeurIPS/ICLR/ICML, ACL/EMNLP, IJCAI/AAAI, COLM (emergente), ICSE/FSE/ASE + TOSEM/TSE (vertiente SE).

**Gaps:**
- **G5.1 — Handoffs sin semántica formal.** A2A/MCP estandarizan transporte y ciclo de vida, pero —a diferencia de FIPA-ACL— no especifican semántica de actos comunicativos ni qué contexto mínimo hace a un handoff "autocontenido". MAST muestra que ahí se concentran los fallos.
- **G5.2 — Coordinación persistente y asíncrona para mantenimiento.** Casi toda la evidencia es greenfield, síncrona y de sesión corta. Equipos de agentes de larga vida con estado duradero, claim sin conflictos y agentes heterogéneos (Claude ↔ Codex) sin contexto compartido: casi sin literatura. **Este es exactamente tu escenario.**
- **G5.3 — Evaluar la coordinación en sí.** No hay métricas estándar que midan la calidad de un protocolo de coordinación (coste de comunicación, pérdida de información por handoff) separadamente del modelo subyacente.

---

## Pilar 6 — Autonomía supervisada y paradas duras

### Teoría: interruptibilidad, corrigibilidad, apagado

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 6.1 | Orseau & Armstrong, *Safely Interruptible Agents*, UAI 2016 | [PR] ✅ | https://intelligence.org/files/Interruptibility.pdf |
| 6.2 | Soares, Fallenstein, Yudkowsky, Armstrong, *Corrigibility*, AAAI 2015 Workshop | [PR] ✅ | https://intelligence.org/files/Corrigibility.pdf |
| 6.3 | Hadfield-Menell, Dragan, Abbeel, Russell, *The Off-Switch Game*, IJCAI 2017 | [PR] ✅ | https://arxiv.org/pdf/1611.08219 |
| 6.4 | Thornley, *The Shutdown Problem: Incomplete Preferences as a Solution*, GPI Working Paper, 2023–24 | [LG] ✅ | https://philpapers.org/archive/THOTSP-8.pdf |

### Control, oversight y enforcement en runtime

| # | Referencia | Tipo | PDF |
|---|---|---|---|
| 6.5 | Greenblatt, Shlegeris, Sachan, Roger (Redwood), *AI Control: Improving Safety Despite Intentional Subversion*, ICML 2024 | [PR] ✅ | https://arxiv.org/pdf/2312.06942 |
| 6.6 | Bowman et al. (Anthropic), *Measuring Progress on Scalable Oversight*, 2022 | [PP] ✅ | https://arxiv.org/pdf/2211.03540 |
| 6.7 | Rebedea et al. (NVIDIA), *NeMo Guardrails*, EMNLP 2023 Demos | [PR] ✅ | https://aclanthology.org/2023.emnlp-demo.40.pdf |
| 6.8 | Inan et al. (Meta), *Llama Guard*, 2023 | [PP] ✅ | https://arxiv.org/pdf/2312.06674 |
| 6.9 | Alshiekh et al., *Safe Reinforcement Learning via Shielding*, AAAI 2018 | [PR] ✅ | https://arxiv.org/pdf/1708.08611 |
| 6.10 | Wang, Poskitt, Sun, *AgentSpec: Customizable Runtime Enforcement for LLM Agents*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2503.18666 |
| 6.11 | Ruan et al., *ToolEmu* — ver 2.10 | [PR] ✅ | https://arxiv.org/pdf/2309.15817 |

### Niveles de autonomía y gobernanza

| # | Referencia | Tipo | PDF/URL |
|---|---|---|---|
| 6.12 | Feng, McDonald, Zhang (UW), *Levels of Autonomy for AI Agents*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2506.12469 |
| 6.13 | Mitchell, Ghosh, Luccioni, Pistilli (HF), *Fully Autonomous AI Agents Should Not be Developed*, 2025 | [PP] ✅ | https://arxiv.org/pdf/2502.02649 |
| 6.14 | Chan et al., *Visibility into AI Agents*, ACM FAccT 2024 | [PR] ✅ | https://dl.acm.org/doi/pdf/10.1145/3630106.3658948 |
| 6.15 | UE, *AI Act* (Reg. 2024/1689), Art. 14 — Human Oversight | [LG] ✅ | https://artificialintelligenceact.eu/article/14/ (oficial: https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |

- **6.1–6.4** — la teoría del "botón rojo": el agente no debe aprender a evitar ni provocar interrupciones; la incertidumbre sobre objetivos humanos hace racional deferir (6.3); teoremas de imposibilidad con preferencias completas (6.4).
- **6.5 (AI Control)** cambia el paradigma: contener al agente aunque esté desalineado, con monitores de confianza y auditoría humana limitada — plantilla directa para tu capa de supervisión.
- **6.9 + 6.10** — del shielding formal (correcto-por-construcción, lógica temporal) al enforcement declarativo sobre agentes LLM (AgentSpec: triggers → bloquear / requerir aprobación / acción alternativa).
- **6.15** — Art. 14(4)(e): capacidad de "detener el sistema mediante un botón de parada o procedimiento similar" como requisito legal para sistemas de alto riesgo.

**Venues:** UAI/IJCAI/AAAI (teoría), ICML/ICLR/NeurIPS (AI control), EMNLP (guardrails), ACM FAccT/AIES (gobernanza), EUR-Lex (regulación).

**Gaps:**
- **G6.1 — Sin puente formal teoría↔agentes LLM.** Interruptibilidad/corrigibilidad están formuladas para agentes RL con utilidades explícitas; no hay definiciones operativas ni garantías equivalentes para agentes LLM con herramientas y memoria.
- **G6.2 — Parada en cascada N-agente.** Solo estudiada en RL descentralizado (El Mhamdi et al., NeurIPS 2017). Detener consistentemente N agentes con tareas en vuelo, estado compartido y handoffs pendientes sin efectos a medias: **sin teoría ni mecanismo estándar.** Tu protocolo (estados `blocked`/`claimed`, kill-switch jerárquico) apunta justo aquí.
- **G6.3 — Operacionalizar el Art. 14.** No hay benchmarks de "supervisión efectiva" (latencia de escalada, sesgo de automatización, falsos negativos del monitor) ni mapeo normativo nivel de autonomía → mecanismo de parada exigible.

---

## De la metodología al doctorado

### Dónde encaja tu protocolo en el mapa

Tu metodología (protocolo repetible para lanzar y mantener software con agentes: pruebas, guardrails, handoffs autocontenidos, decisiones auditables, claim de tareas, área común, reportes humanos) ocupa la intersección de los seis pilares — y esa intersección es el espacio en blanco del mapa:

| Elemento de tu protocolo | Literatura más cercana | Gap que cubre |
|---|---|---|
| Decisiones auditables (`Area_comun/decisions/`) + estado JSON | ESAA (1.5), PROV-AGENT (1.9), AgentOps (1.7) | G1.2 (log operativo = grafo de provenance) |
| Handoffs autocontenidos con `blocked` + pregunta concreta | MAST (1.8), MetaGPT (5.7), ChatDev (5.8) | G5.1 (semántica formal del handoff) |
| Claim/ownership de tareas entre agentes heterogéneos | Contract Net (5.1), A2A (5.10) | G5.2 (coordinación persistente asíncrona) |
| Guardrails + aprobación humana en releases mayores | AgentSpec (6.10), AI Control (6.5), Art. 14 (6.15) | G6.2, G6.3 (parada N-agente operacionalizada) |
| Versionado SemVer/CHANGELOG + ratificación cruzada | in-toto (3.2), SLSA (3.6) | G3.1 (provenance de cambios por agentes) |
| Presupuesto/eficiencia de interacciones | Tokenomics (4.13), AgentPrune (4.7) | G4.1 (cost attribution por handoff) |

### Tres formulaciones posibles de tesis

1. **Sistemas/SE:** *"Un runtime event-sourced con seguridad por capacidad para equipos N-agente que mantienen software: semántica de handoffs, provenance unificada y paradas duras consistentes."* Núcleo: G1.1 + G1.2 + G5.1 + G6.2. Venues objetivo: ICSE/FSE + SOSP/EuroSys + NDSS.
2. **Seguridad:** *"Delegación atenuante y provenance de autoría para el contribuidor agente en la cadena de suministro de software."* Núcleo: G2.2 + G3.1 + G3.3. Venues: USENIX Security, CCS, IEEE S&P.
3. **Empírica/SE:** *"Coordinación persistente de agentes heterogéneos en mantenimiento de software: métricas de calidad de handoff, cost attribution y supervisión efectiva."* Núcleo: G5.2 + G5.3 + G4.1 + G6.3. Venues: ICSE/FSE/ASE, TOSEM, AAMAS.

La opción 1 es la que mejor capitaliza el dogfooding de este repo: el propio protocolo es el artefacto de investigación y su historial (decisiones, handoffs, fallos) es el dataset.

### Qué exigiría el nivel doctoral (lo que la literatura ya considera estándar de evidencia)

- **Formalización:** definiciones precisas (handoff autocontenido, equivalencia de trazas, parada consistente) con propiedades demostrables o al menos falsables — el estándar lo marcan CaMeL (propiedades de no-interferencia), shielding (corrección por construcción) y Thornley (teoremas de imposibilidad).
- **Evaluación empírica controlada:** benchmarks existentes (AgentDojo para seguridad, SWE-bench para mantenimiento, MAST-Data para fallos de coordinación) + ablations. La deprecación de SWE-bench Verified por contaminación obliga a diseñar evaluación propia con cuidado.
- **Comparación con baselines:** AutoGen/ChatDev/OpenHands como sistemas de control; medir con y sin cada capa del protocolo.
- **Amenazas a la validez:** deriva de modelos entre versiones (afecta replay), contaminación de benchmarks, generalización entre proveedores de LLM.

### Pasos concretos sugeridos

1. Leer primero, en este orden: MAST (1.8) → ESAA (1.5) → CaMeL (2.5) → in-toto (3.2) → Tokenomics (4.13) → AI Control (6.5). Son los seis "anclas" — uno por pilar.
2. Escribir un *position paper* (4–6 págs.) que formule el gap integrador y posicione el protocolo; venue natural: workshop de ICSE/FSE o AAMAS (ciclo de envíos oct–ene).
3. Instrumentar este repo para generar el dataset: trazas de handoffs, decisiones, fallos y consumo de tokens, en formato compatible con MAST-Data y PROV.
4. Contactar grupos activos en los gaps: Berkeley Sky Computing (MAST/Progent), ETH SRI (Debenedetti/Tramèr), SMU (Poskitt — AgentSpec), Concordia (Shihab — Tokenomics), CSIRO Data61 (AgentOps).

---

## Nota de verificación

Verificados por fetch directo de arXiv en esta sesión: 2602.23193 (ESAA), 2503.18813 (CaMeL), 2503.13657 (MAST), 2601.14470 (Tokenomics). El resto de IDs ✅ fueron confirmados por los agentes de búsqueda contra páginas oficiales de arXiv/ACL Anthology/USENIX/ACM en resultados de búsqueda o por concordancia multi-índice (dblp, ADS, OpenReview). Los marcados ⚠️ (FIPA SC00061G, BDI/AAAI, tesis de Miller, TOSEM 3714464, SLSA-challenges 2409.05014, ACRFence 2603.20625, 2604.22750, 2605.09104, spec A2A) existen en resultados de búsqueda pero no se confirmó el enlace exacto: verificar antes de citar formalmente. Las afirmaciones de venue (p. ej. "ICLR 2026" para SupervisorAgent) deben re-confirmarse en OpenReview antes de usarlas en un documento académico.
