# ANALISTA - Veredicto adversarial: pivote "publicar para ser citado"

Firma: Analista
Fecha: 2026-07-02
Ancla canonica protocolo: `756477e683a94f6eca803bb0b02f662893554f8b`
Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260702-Operador-to-Analista-REVIEW-pivote-publicar-citado.md` + relay `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-relay-pivote-publicar-citado.md`
Documento revisado: `personal/operador/pivote/DISCUSSION-pivote-publicar-para-ser-citado.md`

## Veredicto

CAMBIO-REQUERIDO antes de formalizar como directiva + DECISION.

El pivote es defendible como hipotesis de trabajo, pero el documento aun sobre-promete en tres zonas: unicidad ("nadie ocupa el hueco"), calendario de 90 dias, y fuerza probatoria del dataset N=1. No veo un angulo letal que obligue a NO-GO. Si se estrechan los claims y se mueve la primera fase a "evidencia reproducible + tesis + transferencia minima" antes de "estandarizacion", HP1, HP3 y HP4 quedan en pie; HP2 queda parcial; HP5 queda no concedida en su forma actual.

## Fuentes verificadas

| Fuente | Resultado |
|---|---|
| Hinds / NoLabs, 2026-01-21, `https://nolabs.ai/blog/sigstore-ai-agent-provenance` | CONFIRMADO: propone atestaciones para plan/generacion/aprobacion, llama a colaboracion, y plantea extender SLSA/Sigstore/in-toto al tramo agente/modelo. El mapping del protocolo es plausible, pero "superset" debe decirse como mapping funcional, no como compatibilidad de esquema. |
| NIST CAISI press release, 2026-02-17, `https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure` | CONFIRMADO: tres pilares, open protocols, industry standards, security/identity research. Tambien confirma que RFI AI Agent Security vencio 2026-03-09 y concept paper Identity/Authorization vencio 2026-04-02. |
| NIST AI Agent Standards Initiative page, `https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative` | CONFIRMADO: el canal permanente existe, pero no equivale a "proceso abierto con silla disponible"; hay que tratarlo como relacionamiento, no como ventana garantizada. |
| IETF draft, 2026-03-29, `https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/` | SLIP contra unicidad: ya hay un draft publico de formato de audit trail para agentes con hash chaining y firmas opcionales. No cubre maker!=checker ni ciclo de tareas completo, pero debilita "nadie atesta". |
| Agent Receipts landscape, 2026-05, `https://agentreceipts.ai/blog/agent-security-tooling-landscape-may-2026/` | SLIP contra "nadie ocupa": reporta signed/hash-chained receipts en varios entrantes (Asqav, nono, Pipelock, Microsoft AGT). Hay espacio, pero la categoria ya se mueve rapido. |
| Gartner, 2026-02-17, `https://www.gartner.com/en/newsroom/press-releases/2026-02-17-gartner-global-ai-regulations-fuel-billion-dollar-market-for-ai-governance-platforms` | CONFIRMADO: $492M en 2026 y >$1B en 2030 para AI governance platforms; demanda macro existe, pero no prueba demanda para este protocolo. |
| Cloud Security Alliance note, 2026-03, `https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_nist_caisi_ai_agent_standards_compliance_20260311-csa-styled.pdf` | CONFIRMADO con fuente secundaria: presion compliance e "accountability gaps" son el problema correcto, pero la nota no convierte la solucion propuesta en comprable. |
| Luke Hinds LinkedIn post sobre nono/Sigstore, 2026, `https://www.linkedin.com/posts/lukehinds_lots-of-messages-of-interest-in-our-sigstore-activity-7433577327445569536-Xg2-` | SLIP contra complacencia: nono ya integra provenance Sigstore/keyless en runtime/sandbox. No es ciclo multi-agente completo, pero el espacio "provenance agentica" no esta vacio. |

## HP1-HP5

| Hipotesis | Veredicto | Razon falsable |
|---|---|---|
| HP1 activo diferencial = metodologia + evidencia + neutralidad, no producto | PASA con estrechamiento | Es correcto abandonar el fork como eje. Lo no retro-fabricable es corpus fechado + decisiones + fallos adversariales. Pero debe decir "activo inicial", no "moat": colusion, compromiso de claves, re-genesis malicioso y N=1 siguen siendo ataques no resueltos por la evidencia actual. |
| HP2 ventana de estandarizacion abierta y sin implementacion de referencia | CAMBIO REQUERIDO | Hinds/NIST estan confirmados. Lo que no resiste es "sin implementacion de referencia": IETF AAT, nono/Sigstore, Agent Receipts/Pipelock/Microsoft AGT indican que hay candidatos parciales. Reescribir como "no hay referencia dominante de ciclo multi-agente task-claim-review-close con checker independiente". |
| HP3 riesgo dominante = irrelevancia por no publicar, no copia | PASA | No encontre un mecanismo fuerte por el cual publicar destruya valor apropiable que hoy exista. La no-publicacion deja cero cita, cero prioridad publica y cero validacion externa. La copia es manejable solo si el activo publico queda fechado y verificable. |
| HP4 captura para una persona via complemento escaso, no spec/app | PASA con frontera | La pauta de mercado es correcta: spec sola captura poco; app sola compite contra incumbentes. El complemento escaso debe definirse como "corpus reproducible + reference implementation + playbook de adopcion + marca/certificacion futura", no solo MCP/Action. |
| HP5 vehiculo 90 dias cabe para una persona con agentes | NO CONCEDIDA | S1-13 mezcla TFM, Zenodo/arXiv, extraccion de spec, limpieza de residuos, MCP, Action, outreach y conversaciones. El cuello no es escribir codigo: es calidad publica en ingles, limpieza normativa, reproducibilidad externa, TFM y respuesta a revisores. En forma actual es calendario optimista, no plan robusto. |

## Angulos adversariales

| Angulo | Resultado |
|---|---|
| 9.1 Evidencia | CAMBIO REQUERIDO. H1-H3 demuestran tamper-evidence bajo ataques inyectados, no seguridad completa. Debe declarar que no detecta colusion de firmantes, claves comprometidas, genesis malicioso aprobado por el operador, manipulacion antes de firma ni segregacion organizacional real. |
| 9.2 Anclas | CAMBIO REQUERIDO. Mapping Hinds plausible, pero "superset" es demasiado fuerte si no hay esquema compatible in-toto/Sigstore. NIST es canal, no aprobacion implicita. |
| 9.3 Transferibilidad | CAMBIO REQUERIDO. NOVA/new_instance no basta como evidencia externa si el autor opera todo. Minimo: dos terceros ejecutan desde cero con video/log reproducible, una issue de friccion cerrada y una instancia que produzca eventos verificables sin ayuda sincrona. |
| 9.4 Calendario | CAMBIO REQUERIDO. Primera semana que cae: S5-6, extraccion de core "sin residuos de instancia". Esa tarea compite con TFM y obliga a separar normativo/instancia/historia, idioma, rutas Windows, validator PS1 y ejemplos. |
| 9.5 Cancelacion gobernada | PASA con condicion. Cancelar 0230/0232 y re-alcanzar 0233/0234 no es deuda si se registra DECISION que supersede la parte fork/producto de DECISION-0077/REQ-ZEUS-001. Sin esa DECISION seria inconsistencia de direccion. |
| 9.6 Extraccion spec | CAMBIO REQUERIDO. Es trabajo mayor. La prueba no es "repo publico"; es `new_instance` desde template, validator Python normativo, ejemplos en ingles, sin rutas D:/, sin mailbox en espanol en normative core y sin referencias a este live instance como requisito. |
| 9.7 Licencia/marca | PASA parcial. Apache-2.0 para core/reference es razonable si la captura queda en marca, dataset/corpus curado, servicios/certificacion y hosted verification futura. Debe decidir desde el dia 1 que no se relicencia el core de forma hostil. |
| 9.8 TFM | BLOQUEANTE S1. Hay que verificar norma universitaria antes de Zenodo/arXiv. Si no esta permitido, invertir orden: defensa primero, publicacion inmediatamente despues. |
| 9.9 Claim de unicidad | CAMBIO REQUERIDO. La afirmacion amplia cae por AAT/nono/Agent Receipts/Pipelock. La afirmacion estrecha todavia puede sobrevivir: no vi referencia dominante que cubra ciclo multi-agente task/claim/review/close + maker!=checker + ledger reproducible. |
| 9.10 Kill criteria | CAMBIO REQUERIDO. "2 instancias externas a mes 12" es buen criterio rey, pero mes 6 "interaccion sustantiva" es ambiguo. Definir umbrales: respuesta nominal no cuenta; cuenta PR externo, issue tecnica reproducida, cita/preprint discussion, piloto de tercero o maintainer de estandar que pide cambios concretos. |

## Angulos faltantes

| Angulo agregado | Riesgo |
|---|---|
| A11 Privacidad/consentimiento del dataset | Si el dataset de eventos contiene mensajes, rutas, nombres, costos o contexto operacional, DOI inmutable puede congelar PII/secrets accidentales. Antes de Zenodo: manifest de redaccion, licencia del dataset, DPA/consentimiento si aplica y hash de exclusion de secretos. |
| A12 Idioma y audiencia | La autoridad externa exige ingles tecnico. Traducir no basta: hay que convertir "protocolo vivo dogfooded" en terminologia de assurance, provenance, change management y audit evidence. |
| A13 Canal de distribucion | "HN/X + 15-20 CTOs" no reemplaza un canal. Necesita lista nominal: OpenSSF/Sigstore, NIST/CSA, SOC2/ISO auditors, software factories reguladas, autores de AAT/nono/Agent Receipts. |
| A14 Amenaza de auto-atestacion | Neutralidad vs GitHub/Anthropic es cierta solo si el protocolo puede verificar agentes heterogeneos. Si la demo sigue en una sola maquina y un solo operador, el argumento de neutralidad queda teorico. |
| A15 Operacion del propio protocolo | El historial de jams no es solo "coste": es evidencia adversarial de que el sistema requiere operador experto. Debe publicarse como limitacion, no como anexo. |

## Afirmaciones a corregir antes de publicar

| Texto/claim | Correccion requerida |
|---|---|
| "nadie atesta el ciclo multi-agente completo" | Cambiar a "no encontre una referencia dominante que combine ciclo multi-agente de tarea/claim/review/cierre con checker independiente y verificacion reproducible; existen soluciones parciales de audit trail/receipts". |
| "nuestro protocolo ya implementa un superset de Hinds" | Cambiar a "mapea funcionalmente a Plan/Generation/Approval y agrega controles de coordinacion; falta compatibilidad formal con in-toto/Sigstore". |
| "dataset sellado ... 3 hipotesis confirmadas" | Cambiar a "hipotesis confirmadas bajo el harness definido"; no implica seguridad general ni reduccion de defectos. |
| "costo despreciable" | Solo aplica a evento/bytes. Para proceso usar "costo estructural bajo; costo operativo por tarea aun no medido". |
| "comprador liquido" | Convertir en hipotesis comercial no validada. Gartner confirma presupuesto macro, no comprador especifico para este artefacto. |
| "S1-13" | Rebaselinar con gates: TFM permissions, dataset sanitization, reproducibility external, spec extraction, MCP/Action. No vender todo como cabible hasta medir. |

## Cambios concretos al plan de 90 dias

1. Semana 0 obligatoria antes de S1: verificar normas TFM, revisar dataset por PII/secrets, fijar licencia de dataset/core/marca, y escribir claims publicos estrechos.
2. S1-2: publicar solo si pasa el gate legal/TFM/PII. Si no, congelar hashes + reproducibility package privado y publicar post-defensa.
3. S3-4: preprint primero como "verifiable governance log for multi-agent software work", no como "standard". Incluir amenazas no cubiertas en tabla principal.
4. S5-8: reemplazar "spec-repo publico completo" por "minimum public reference profile": schema de evento, verifier, threat model, one clean instance. Dejar mailbox/UI/historia fuera.
5. S9-11: MCP+Action solo si el verifier y quickstart ya fueron ejecutados por un tercero. Si no, posponer MCP y priorizar reproducibilidad externa.
6. Outreach: antes de HN/X, contacto directo y tecnico a Hinds/nono/AAT/Agent Receipts/OpenSSF/CSA con mapping y pregunta concreta. Public launch despues de tener feedback o rechazo.
7. Kill criteria: mes 3 = un tercero reproduce; mes 6 = una interaccion tecnica externa sustantiva; mes 9 = una instancia externa o design partner; mes 12 = dos instancias externas o se mata la tesis de transferibilidad.

## Reproduccion y gates

| Gate | Exit |
|---|---:|
| `git fetch origin` | 0 |
| `git status --short` | 0, arbol con cambios ajenos/untracked previos; no tocados |
| `python scripts/validate_collaboration_state.py` | 0 |
| JSON state read with `utf-8-sig` | 0 |
| `python scripts/scan_domain_neutrality.py` | 0 |
| `python scripts/scan_encoding.py` | 0 |
| secretless clean clone validate: `python scripts/validate_collaboration_state.py --root <tmp>` | 0 |
| drift check `runtime.protocol_replay.protocol_state_drift` | `has_drift=false`, `up_to_seq=3153` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| product clean clone/npm test | N/A: la instruccion de pivote no cita repo ni commit de producto; ejecutar Zeus-protocol HEAD no seria canonico |

## Recomendacion

CAMBIO-REQUERIDO, no NO-GO.

Formalizar el pivote solo despues de corregir el documento y la DECISION propuesta con el claim estrecho: "publicar evidencia reproducible de un ciclo completo de gobernanza multi-agente con integridad verificable, limitaciones explicitas, y prueba de transferencia externa". No formalizarlo como "estandar abierto sin referencia competidora" ni como plan de 90 dias completo hasta pasar Semana 0 y una reproduccion externa minima.
