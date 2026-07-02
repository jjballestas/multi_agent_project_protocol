# ANALISTA - Veredicto adversarial: pivote v2

Firma: Analista
Fecha: 2026-07-02
Ancla canonica protocolo: `d0afaa2b06df03ffcad133063cdbd8a2f1ea6ef4`
Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-relay-pivote-v2-ronda2.md`
Documento revisado: `personal/operador/pivote/DISCUSSION-pivote-v2-publicar-para-ser-citado.md`
Producto Zeus-protocol probado en clon limpio: `b2b2395da39090109db6de2dc50726dbaab1a11e` (no citado por la instruccion; incluido solo por gate general del revisor)

## Veredicto

CAMBIO-REQUERIDO antes de formalizar directiva + DECISION.

La v2 corrige sustancialmente la v1: abandona el claim amplio de unicidad, subordina el Carril B al Carril A,
declara que el dataset N=500 es validity-check bajo harness y no security proof, degrada Q3, repara el contraste
Q4 y reconoce que Nova es el motor real de evidencia. No veo NO-GO: el marco de dos carriles es viable.

No queda sellable "ya" porque el pre-registro todavia deja rutas de reinterpretacion post-hoc: excepciones de
presion por sprint, arbitraje humano, taxonomia D1-D4 incompleta para defectos de negocio, trailers `Fixes-Task:`
facilmente omitibles/ambiguos, y ausencia de politica laboral/consentimiento para medir empleados. El Carril B
tambien necesita una decision previa sobre IP/licencias/dataset/empleados y una peticion nominal a Hinds/nono antes
de gastar capital en preprint.

## Fuentes verificadas

| Fuente | Resultado |
|---|---|
| NIST CAISI AI Agent Standards Initiative, 2026-02-17, `https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure` | CONFIRMADO: canal real para interoperabilidad/seguridad de agentes; no equivale a silla disponible ni adopcion implicita. |
| NIST CAISI landing, `https://www.nist.gov/caisi` | CONFIRMADO: mandato de guias/evaluaciones/estandares voluntarios; relacionamiento, no garantia de ventana. |
| arXiv endorsement, `https://info.arxiv.org/help/endorsement.html` + update 2026-01-21 `https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/` | CONFIRMADO: endorsement es bloqueante probable para autor nuevo/categoria nueva; Semana 0 lo trata correctamente. |
| IETF draft Agent Audit Trail, `https://datatracker.ietf.org/doc/draft-sharif-agent-audit-trail/` | CONFIRMADO: ya existe formato publico con hash chaining y firmas opcionales; refuta cualquier "nadie atesta agentes". |
| Agent Receipts landscape May 2026, `https://agentreceipts.ai/blog/agent-security-tooling-landscape-may-2026/` | CONFIRMADO como fuente de mercado: signed/hash-chained receipts aparecen en varios entrantes; la categoria se mueve rapido. |
| Luke Hinds / nono / Sigstore provenance, `https://www.alwaysfurther.ai/blog/sigstore-ai-agent-provenance` y senales publicas nono | CONFIRMADO: Hinds/nono es actor dual relevante; el framing "tu cadena extendida, con datos" es mas defendible que "superset". |
| BlockA2A, `https://arxiv.org/pdf/2508.01332` | CONFIRMADO: multi-agent trust framework con auditabilidad; no cubre este ciclo operativo completo, pero debilita unicidad amplia. |
| Verifiability-First Agents, `https://openreview.net/forum?id=um3VMCCOCS` | CONFIRMADO como trabajo cercano de cryptographic action attestations; obliga related work completo. |
| PROV-AGENT, `https://arxiv.org/html/2508.02866v3` | CONFIRMADO: provenance multi-agent via W3C PROV/MCP; no reemplaza maker-checker operativo, pero elimina campo vacio. |

## Correcciones de ronda 1

| Hallazgo ronda 1 | Estado v2 | Veredicto |
|---|---|---|
| Unicidad amplia falsa | s.2/s.3/s.5 estrechan HP1' y agregan related work | PASA con vigilancia: aun falta quitar todo residuo retorico de "referencia unica" fuera del claim estrecho. |
| Dataset N=500 sobreprometido | s.1.1 declara validity-check y no security proof | PASA. |
| 90 dias fantasia | s.8 re-baselinea Semana 0 + gates + paquete minimo | PASA parcial: sigue optimista en DSSE/Rekor + paquete reproducible + externo en una sola persona. |
| Kill criteria ambiguos | s.9 separa senales/decisiones | PASA parcial: mes 6/12/18 mejoran, pero falta presupuesto operativo real y dueno de cada decision. |
| Comprador liquido sobreestimado | H-COM queda como hipotesis comercial | PASA. |
| PII/licencias/arXiv omitidos | Semana 0 agrega bloqueantes | PASA. |
| Q3 causal mala y DER invalida | Q3 descriptiva; C3' escapes post-GO como primaria | PASA. |

## HP1'-HP7

| Hipotesis | Resultado | Ataque falsable |
|---|---|---|
| HP1' activo estrecho | PASA PARCIAL | El claim correcto es "referencia operativa publicada de ciclo task->claim->delivery->review->close con checker independiente y corpus longitudinal". Si se publica como "primera atestacion de agentes", SLIP por IETF AAT/Agent Receipts/BlockA2A/PROV-AGENT. |
| HP2' ventana condicional | PASA COMO HIPOTESIS | No hay prueba de ventana. El contacto a Hinds/nono antes del preprint es correcto. Silencio 30 dias no mata el Carril B, pero mata la apuesta de estandarizacion temprana. |
| HP3 irrelevancia mayor que copia | PASA | No publicar deja cero prioridad y cero cita. El riesgo nuevo es captura sin atribucion por nono; mitigable con DOI/fecha y peticion concreta antes del contacto. |
| HP4' captura via complemento | PASA | Realista si el retorno economico principal es Nova; Carril B debe medirse como reputacion/carrera/interop, no como negocio primario. |
| HP5' 90 dias secundario | CAMBIO-REQUERIDO | Semana 0 + redaccion publica + redaccion dataset + verifier externo + DSSE/Rekor + outreach puede exceder 1 dia/semana del operador. Requiere presupuesto semanal y stop automatico si lo rebasa. |
| HP6 transferencia interna | CAMBIO-REQUERIDO | "Onboarding <= 1 dia, cero des-atascos" es medible solo si "des-atasco" se define como evento `manual.intervention` y si empleados registran friccion. Sin politica escrita, el autor puede invisibilizar ayudas por chat/llamada. |
| HP7 Nova como evidencia | PASA PARCIAL | Q1 fuerte si `cost.attributed` es automatico y bloqueante. Q2 mecanistica defendible. Q4 factible pero bajo poder. Sin pre-registro sellado + politica de excepciones + commit trailers obligatorios, degenera a anecdota. |

## Pre-registro s.7

| Vector | Resultado | Motivo falsable |
|---|---|---|
| Sellabilidad temporal | PASA PARCIAL | DECISION + hash encadenado + seq fija sella el texto si se atesta antes del primer sprint. Debe incluir hash del documento completo y dataset_start_seq equivalente; no basta "esta seccion". |
| Inviolabilidad | SLIPS | El operador sigue pudiendo suspender sprint entero, arbitrar defectos, reclasificar riesgo y omitir `Fixes-Task:` si el validador no lo exige. Cada ruta necesita evento firmado y reporte publico. |
| D1-D4 taxonomia | SLIPS | Escapan defectos de requisito mal entendido, deuda de arquitectura, performance no testeada, UX/soporte, integracion externa y defectos contables detectados por conciliacion tardia sin hotfix inmediato. Declarar subcobertura esperada. |
| Linkage por trailer | SLIPS | `Fixes-Task:` v1 es auditable solo si el validador bloquea commits de fix/revert/hotfix sin trailer y si PR/commit template impide texto libre ambiguo. |
| Q1 peones/costo | PASA | Confirmatoria defendible si los tokens del firmante se emiten automaticamente por task_id y el cierre falla si falta el evento. |
| Q2 mecanistica | PASA | "Checker atrapo N defectos concretos que gates no atraparon" es el claim mas fuerte y mas honesto. |
| Q3 calidad | PASA | Degradada a descriptiva; no vender causalidad temporal. |
| Q4 contraste | PASA PARCIAL | ITT + hash assignment + piso etico estan bien. La exclusion de alto riesgo limita generalizacion, pero es honesta. |
| Consentimiento laboral | SLIPS | Medir empleados, costo, defectos y escapes requiere politica interna: finalidad, no uso punitivo individual, retencion, acceso, redaccion y consentimiento/acuse. |

## Carril B s.8-9

| Vector | Resultado | Motivo falsable |
|---|---|---|
| Semana 0 | PASA COMO GATE | PII/secrets/licencias/arXiv/claims estrechos son bloqueantes reales. Agregar IP laboral y permisos de empleados/dataset. |
| Paquete reproducible 5-10 comandos | PASA PARCIAL | Correcto como gate, pero debe correr desde una instancia limpia sin rutas `D:/`, sin secretos privados y con verifier offline. |
| DSSE/in-toto/Rekor | CAMBIO-REQUERIDO | Es el camino correcto de interop, pero no esta estimado: puede tocar canonicalization, checkpointing, identity y genesis boundary. Hacer spike tecnico antes de prometerlo como entregable central. |
| Outreach Hinds/nono | PASA | Pregunta concreta antes del preprint reduce desperdicio. Debe decidirse si se pide PR de interop, coautoria de profile o item OpenSSF; no los tres a la vez. |
| Kill criteria | PASA PARCIAL | Senales 30/60/90 y decisiones 6/12/18 son mejores que v1. Agregar "Carril B no consume >1 dia/semana del operador; si lo hace, pausa automatica". |
| Resultado modal | PASA | Capital de carrera + empresa que mide Nova es exito parcial honesto. |

## 12 angulos de s.11 + faltantes

| Angulo | Resultado |
|---|---|
| 1 sellabilidad/inviolabilidad | SLIPS por excepciones, arbitraje, riesgo, trailers y ayudas informales. |
| 2 D1-D4/linkage | SLIPS por defectos de requisitos, arquitectura, rendimiento, UX/soporte, integracion y conciliacion tardia. |
| 3 Q4 sin alto riesgo | PASA si se declara: generaliza solo a criticidad media/baja; no prueba payroll/treasury/auth. |
| 4 excluir brazo C | PASA para v1: reduce ruido. Pero registrar como backlog exploratorio, no enterrarlo. |
| 5 HP6 medible | SLIPS sin evento `manual.intervention`, bitacora de friccion y politica de ayudas. |
| 6 DSSE/Rekor | CAMBIO-REQUERIDO: necesita spike de compatibilidad y estimacion. |
| 7 subordinacion B | SLIPS sin presupuesto semanal medido y stop automatico. |
| 8 mes 18 | PASA: no es kill disfrazado si el resultado modal aceptado es carrera/corpus y no empresa. |
| 9 0230/0232/0233/0234 | CAMBIO-REQUERIDO: requiere DECISION que supersede DECISION-0077/REQ-ZEUS-001 para fork descartado y nuevo foco employee-ready/NOVA. |
| 10 Semana 0 legal | SLIPS: falta IP/empleados/dataset/no-uso-punitivo/retencion. |
| 11 consentimiento empleados | SLIPS: debe existir politica escrita antes de medir. |
| 12 faltante | Agrego: riesgo de Goodhart por task sizing y clasificacion S/M/L; riesgo de contaminacion entre brazos; riesgo de auditoria selectiva si solo se publican tareas "limpias"; riesgo de marca/IP si Nova usa el protocolo como ventaja interna mientras el core se publica. |

## Recomendacion de cierre

CAMBIO-REQUERIDO.

El operador puede formalizar la direccion de dos carriles, pero no debe sellar todavia el pre-registro ni lanzar
Carril B publico. Cambios minimos antes de DECISION:

1. Agregar una politica interna de medicion de empleados: consentimiento/acuse, no uso punitivo individual,
   retencion, redaccion, acceso y canal de disputa.
2. Convertir ayudas/des-atascos/excepciones/suspensiones/arbitrajes en eventos firmados y publicables.
3. Hacer bloqueante el trailer `Task-Id:` y, para `type:fix|revert|hotfix`, `Fixes-Task:`.
4. Cerrar taxonomia D1-D4 con subcategorias y una seccion explicita de subconteo esperado.
5. Definir presupuesto del Carril B: maximo 1 dia/semana del operador, medido; exceso pausa el carril.
6. Registrar DECISION que supersede el fork Zeus-Aegis y re-alcance 0230/0232/0233/0234 hacia employee-ready/NOVA.
7. Ejecutar un spike DSSE/in-toto/Rekor antes de prometer interop como entregable central.
8. Sellar el pre-registro completo como documento versionado con hash, seq de inicio y reglas de exclusion antes
   de la primera tarea Nova Budget.

## Reproduccion y gates

| Gate | Exit |
|---|---:|
| `git fetch origin` | 0 |
| `git status --short` | 0, arbol con cambios ajenos/untracked previos; no tocados |
| JSON state read with `utf-8-sig` | 0 |
| `python scripts/validate_collaboration_state.py` | 0 |
| secretless clean clone validate `python scripts/validate_collaboration_state.py --root <tmp>` | 0 |
| `python scripts/scan_domain_neutrality.py` | 0 |
| `python scripts/scan_encoding.py` | 0 |
| drift check `runtime.protocol_replay.protocol_state_drift(Path("."))` | `has_drift=False`, `up_to_seq=3214` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Zeus-protocol clean clone `npm test` at `b2b2395da39090109db6de2dc50726dbaab1a11e` | 0, 87 pass, 22 skipped |
