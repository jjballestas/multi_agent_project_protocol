> **UNIFICADO** en `Area_comun/artifacts/ANALISIS-TASK-0038-n-agent-consolidado.md` (analisis de record, 2026-06-06). Este documento se conserva como fuente autoral.

# Análisis crítico independiente — TASK-0038 (N-Agent Readiness)

**Autor del análisis:** Claude (revisión adversarial independiente)
**Fecha:** 2026-06-06
**Documento evaluado:** `TASK-0038_IMPLEMENTACION_N_AGENT_READINESS_ANALISIS_TECNICO.md` (repo `multi_agent_project_protocol`)
**Alcance:** calidad técnica de la especificación, asumiendo ya decidido el paso a N agentes. Excluye la decisión estratégica de fondo, lo legal, financiero y comercial.
**Postura:** honesta y no complaciente. Acreditar lo correcto con precisión; señalar huecos reales aunque el documento sea bueno.

> Nota de meta-nivel: TASK-0038 es **en sí mismo** un análisis crítico (evalúa una "propuesta original" y propone enmiendas). Este documento es por tanto una revisión de segundo orden: ¿está bien encaminado el propio TASK-0038 frente al estado del arte 2025/2026?

---

## 1. Veredicto

TASK-0038 está **bien encaminado y es netamente superior a la propuesta original que critica.** Identifica correctamente los cuatro modos de fallo que romperían el sistema en producción —escritor único como cuello de botella, sesgo de routing lexicográfico, ausencia de máquina de estados para fallo de QA, y embudo humano— y su movimiento arquitectónico central es el correcto: *los agentes no escriben estado; emiten intents append-only que un orquestador determinista de escritor único valida y serializa sobre un snapshot derivado.* Ese patrón es exactamente hacia donde converge la literatura actual (event sourcing para agentes autónomos, el modelo de actividades de Temporal, el checkpointing de LangGraph 1.0). **Dirección: correcta.**

Sin complacencia: el documento es **fuerte en el "happy path" de workflow, estado y concurrencia, y débil en cuatro frentes que, para un sistema cuyo objetivo declarado es la auditabilidad, no son accesorios:**

1. modelo de **seguridad e identidad agéntica** (autenticación de eventos, inyección vía handoffs);
2. **rigor de idempotencia y fencing** en el camino de aplicación;
3. la **frontera real del determinismo** (LLM no determinista vs. orquestador determinista), que está sobre-vendida;
4. **presupuesto de coste/latencia y garantía de terminación** global.

Además arrastra **sobre-diseño** en sus fases tardías (observabilidad estilo OpenTelemetry, SBOM/SLSA) para un protocolo que hoy corre 2 agentes sobre Markdown + JSON y no publica binarios.

**Recomendación:** aprobar la **dirección**; **condicionar la implementación** a cerrar los dos P0 (identidad/seguridad e idempotencia/fencing) y a aterrizar explícitamente la frontera de determinismo, antes de congelar `SPEC-0038` y `DECISION-0015`. Reclasificar las fases 5–7 como diferidas hasta que exista un pipeline de release real.

---

## 2. Metodología: contra qué se evaluó

El contraste se hizo con estándares y prácticas vigentes a 2025/2026:

- **Event sourcing para agentes** — patrón en el que el agente emite intenciones/diffs validados y aplicados por un orquestador determinista; concurrencia serializada a nivel de evento preservando orden total del log. Coincide con la dirección del documento.
- **Durable execution** — Temporal (checkpointing a nivel de actividad; el código de workflow es determinista y se reproduce contra el event history, saltando actividades ya completadas) y LangGraph 1.0 (oct-2025, checkpointing a nivel de nodo, "production-grade"). Regla clave: *todo lo que toca el mundo exterior es una actividad/evento registrado; el resto es lógica determinista.*
- **Concurrencia distribuida** — leases time-bound + **fencing tokens** (número monótono creciente que el recurso usa para rechazar operaciones tardías). Práctica establecida: "default to leases, always include a fencing token; un lease sin fencing token es inseguro bajo pausas de proceso".
- **OWASP Top 10 for Agentic Applications** (OWASP GenAI Security Project, dic-2025) — goal/instruction hijacking, identity abuse, tool misuse; mitigaciones: autenticar y cifrar la comunicación inter-agente, guardrails que bloquean acciones inseguras.
- **Interoperabilidad de agentes** — A2A (Google, abr-2025; agent cards, capability discovery, task lifecycle: `submitted → working → input-required → completed → canceled → failed`, agentes autenticados) y MCP (acceso agente-herramienta).
- **Supply chain** — SLSA (provenance/integridad de build), CycloneDX **v1.7** (ECMA-424 2.ª edición, oct-2025; soporte ML-BOM/AI-BOM desde v1.5).

En todo esto el documento está **alineado conceptualmente**. Las brechas que siguen son de **profundidad y rigor**, no de dirección.

---

## 3. Lo que acierta (acreditado con precisión)

- **Núcleo event-sourcing + escritor único + snapshot derivado** (§3.3, §4.3). Es la decisión correcta y coincide con el patrón de referencia: el agente emite intents, el orquestador serializa. Reduce colisiones porque los agentes dejan de competir por el archivo central.
- **`review ≠ author` y prohibición de self-QA elevadas a invariante verificada por property tests** (§5, §12.4). Esto es ingeniería genuinamente buena y por encima del promedio de proyectos de este tamaño: no es una norma escrita, es una propiedad comprobable.
- **Leases para claims vencidos** (§4.4). Patrón correcto (no borrar el claim, marcar `expired`, permitir reclaim, rechazar reporte tardío por versión obsoleta).
- **Máquina de estados explícita para fallo de QA con corte de bucles por firma del fallo** (§5.3, §5.4). Ataca una clase de bug real (bucle implementador↔QA) con un mecanismo concreto: misma firma 2 veces → escalar a rediseño arquitectónico.
- **Criterios de aceptación concretos y testeables** (§13) y **plan de tests con property-based + simulación de concurrencia** (§12). La simulación de 10 implementadores / 100 tareas / leases vencidos / QA failures repetidos es exactamente lo que el dominio exige y rara vez se ve especificado.
- **Matiz de SemVer sobre "enum como contrato público"** (§4.2, §16.3). Bien razonado y honestamente hedge-ado: minor si nadie externo valida el enum; potencialmente breaking si lo hace.
- **Escalado humano como gate de decisión, no como catch-all** (§3.5). Distinción correcta entre decisión real (riesgo, política, irreversible, ambigüedad) y mera imposibilidad operativa temporal.

---

## 4. Huecos técnicos reales (priorizados)

### P0 — Modelo de seguridad e identidad agéntica subdesarrollado

Es la brecha más grave **precisamente porque el objetivo declarado es auditabilidad**.

La validación semántica propuesta (§4.2) es:

```text
assert report.agent in registry.enabled_agent_ids
```

Esto solo comprueba el **string de identidad reclamado**. Nada autentica que el `turn_report` lo haya emitido realmente ese agente. Un agente comprometido, con bug, o un proceso confundido puede firmar como otro, y entonces *toda la cadena de auditoría deja de ser atribuible*. El documento luego quiere "commit firmado o trazable" (§10.3) pero no firma el evento que origina el commit: la atribución se rompe aguas arriba.

Segundo flanco: **goal/instruction hijacking vía inyección en el contenido del handoff/task.** Los handoffs son "texto autocontenido" (§8) — es decir, superficie de ataque directa. En el Top 10 agéntico de OWASP, la manipulación de objetivos vía instrucciones en lenguaje natural es un riesgo de cabecera. El campo `trust_boundary` existe en el registry (§4.1) pero **no está conectado a ningún mecanismo de autenticación ni a sanitización/validación de inputs** de handoff.

**Qué falta:** (a) firma/atribución autenticada de cada `turn_report` y cada evento del log; (b) validación/sanitización de los inputs de handoff y task contra inyección, con `trust_boundary` ligado a una política efectiva; (c) autenticación de la comunicación inter-agente (lo que A2A ya formaliza con agentes autenticados).

### P0 — Idempotencia y fencing insuficientes

El `state_version` (§4.3, §4.4) funciona como **fencing token global a nivel de snapshot completo**. Bien como idea, pero con dos problemas:

1. **Grano demasiado grueso.** Como toda la máquina comparte una única versión, a medida que N crece *todos* los intents compiten por la misma versión → alta tasa de `apply_conflict` y **falsos conflictos** entre tareas que no se tocan entre sí. Escala mal. Lo correcto es **versión por-tarea/aggregate**, no por snapshot.
2. **Sin idempotency key en los intents.** La política de colisión hace "reintentar con exponential backoff + jitter" (§4.3). Sin una `idempotency_key` por intent, un reintento tras backoff puede **doble-aplicarse** — exactamente el hazard "el retry crea un duplicado" que documenta la práctica de durable execution (si una actividad crea un registro en cada ejecución, el retry duplica).

Tercero: el lease (§4.4) está conceptualmente bien, pero **sin fencing token por-recurso** sigue expuesto al problema del *proceso pausado* (GC, preempción del SO, page fault): el agente cree que aún tiene el lease, el orquestador sabe que venció, y nada en el recurso rechaza la escritura tardía salvo el check de versión global —que, por el punto 1, es frágil bajo carga—.

**Qué falta:** `idempotency_key` por intent; fencing token monótono por-recurso; versión por-tarea en lugar de por-snapshot.

### P1 — La afirmación de determinismo está sobre-vendida

El documento afirma "replay determinista" y "replay reconstruye snapshot" (§4.3, §12.4, §11 Fase 2). Pero **los agentes son LLMs no deterministas.** Lo que puede ser determinista es la **lógica de orquestación**, al estilo Temporal: los efectos no deterministas (incluida la salida del agente) se **registran como eventos** y en replay se reproducen desde el historial en lugar de re-ejecutarse. El documento **no traza explícitamente esa frontera** entre "orquestador determinista" y "actividad de agente no determinista cuya salida se graba".

Consecuencia: "replay" solo es cierto para las *transiciones de estado*, no para *re-correr agentes*. Sin enunciar el límite, se transmite una **falsa sensación de reproducibilidad** que puede llevar a tests de replay que parecen verificar más de lo que verifican.

**Qué falta:** un enunciado explícito —"todo lo que toca el mundo exterior (LLM, herramienta, red) es un evento registrado; el replay reconstruye estado a partir de eventos grabados, no re-invocando agentes"— y que los tests de replay (§12.4) lo reflejen.

### P1 — Event log subespecificado para ser fuente de verdad

JSONL append-only (§16.2) es pragmático y correcto como punto de partida, pero para que el log sea **fuente de verdad** faltan tres garantías que el event sourcing exige:

1. **Secuencia global monótona + append atómico.** Con varios directorios/archivos append-only (`turn_reports`/`events`, §11 Fase 2), ¿quién garantiza el **orden total**? `state_version` ayuda pero no es lo mismo que un número de secuencia de evento; la relación entre ambos no está fijada.
2. **Versionado de esquema de eventos.** Los eventos viven para siempre y su forma cambiará; sin versión de esquema, el replay futuro se rompe.
3. **Snapshot/compactación.** "Snapshot regenerable" (§16.2) no define cada cuánto, ni cómo se trunca/compacta el log, ni cómo se valida que el snapshot derivado concuerda con el log.

También: manejo de **escritura parcial/torn write** del propio log (línea JSONL a medio escribir).

### P1 — Sin presupuesto de coste/latencia ni garantía de terminación global

Review + QA + reintentos + backoff pueden disparar **coste de tokens y wall-clock**. El documento corta *ciclos* (`max_review_cycles`, `max_qa_cycles`, §5.3) — bien — pero **no define presupuesto por tarea ni por run, ni deadline global**. Los sistemas de durable execution tienen timeouts; los agénticos necesitan además **techo de coste**. Una tarea patológica puede consumir presupuesto sin violar ningún contador de ciclos si rebota entre estados válidos.

**Qué falta:** presupuesto de coste y deadline por tarea y por run, con escalado/cancelación al agotarse.

### P2 — Compensación/saga para efectos irreversibles

Los guardrails ponen las acciones sensibles tras aprobación humana (§7.1) — bien — pero **no hay compensación/rollback modelada como estado** para un release que falla a medias. "rollback_plan por release" (§10.6) se menciona como artefacto, no como semántica de workflow. Un release multi-paso necesita pasos de compensación (patrón saga), no solo un plan en prosa.

### P2 — Granularidad de herramientas y calibración del routing

- **`tool_policy` es un enum grueso** ("restricted_write"/"sandboxed_write", §4.1). OWASP recomienda **allowlist por-herramienta** atada a capacidad + scope de tarea. El documento gesticula hacia allowlist en §7.2 pero no la liga al modelo del registry.
- **El score de routing tiene números mágicos** (pesos 10/6/6/4, §3.4/§6.2) asertados sin calibración ni feedback. Para 2–5 agentes es pragmáticamente aceptable, pero se presenta con **falsa precisión**. Bien que pida `routing_decision.explanation` (§16.4); faltaría una **métrica de fairness (ratio max/min de asignaciones) como gate de CI**, no solo como métrica observada en §9.3.

---

## 5. Sobre-diseño y secuenciación honesta

El documento **reconoce el riesgo de sobre-diseño** (§16.1) y lo mitiga con config-gating + fallback N=2 intacto — correcto. Pero seamos francos sobre el peso relativo de las fases:

- **Fases 0–4** (registry + validación semántica, event log + leases, router balanceado, máquina de estados Review/QA) = **el valor real y proporcionado** al problema.
- **Fases 5–7** (observabilidad estilo OpenTelemetry, SBOM, SLSA/provenance) = **prematuras** para un protocolo que hoy corre 2 agentes sobre Markdown + JSON y que **aún no publica binarios**. Montar SLSA/CycloneDX antes de tener algo que releasear es ceremonia, no confiabilidad.

**Recomendación de secuencia:** ejecutar 0–4 como núcleo; declarar 5–7 **condicionadas** a la existencia de un pipeline de release real (cuando una instancia piloto efectivamente publique software). Esto evita pagar complejidad de cumplimiento sin un release que la justifique.

---

## 6. Recomendaciones accionables (qué añadir antes de aprobar implementación)

En orden de prioridad, para incorporar a `SPEC-0038` / `DECISION-0015`:

1. **(P0 seguridad)** Firma/atribución autenticada de cada `turn_report` y evento; sanitización/validación de inputs de handoff y task contra inyección; ligar `trust_boundary` a una política efectiva. Añadir tests de "evento no atribuible se rechaza" y "handoff con payload malicioso se contiene".
2. **(P0 concurrencia)** `idempotency_key` por intent; fencing token monótono por-recurso; **versión por-tarea/aggregate** en lugar de por snapshot global. Añadir test "intent reintentado no se aplica dos veces".
3. **(P1 determinismo)** Párrafo explícito separando orquestador determinista de actividad de agente no determinista grabada; regla "todo efecto externo es evento registrado"; ajustar los tests de replay para reflejarlo.
4. **(P1 log)** Secuencia global monótona + append atómico; versionado de esquema de eventos; política de snapshot/compactación; manejo de torn writes.
5. **(P1 coste)** Presupuesto de coste y deadline por tarea y por run, con escalado/cancelación al agotarse.
6. **(P2)** Allowlist de herramientas por-capacidad atada al registry; métrica de fairness de routing como **gate de CI**; semántica de compensación (saga) para releases multi-paso.
7. **(secuencia)** Reclasificar Fases 5–7 como diferidas/condicionadas a un release real.

---

## 7. Tabla resumen

| Dimensión | Estado en TASK-0038 | Veredicto |
|---|---|---|
| Event sourcing + escritor único + snapshot derivado | Correcto, alineado con el estado del arte | ✅ Acierto |
| `review ≠ author` / no self-QA como invariante property-tested | Bien modelado y verificable | ✅ Acierto destacado |
| Leases para claims vencidos | Patrón correcto | ✅ con reserva (falta fencing por-recurso) |
| Máquina de estados QA-fail + corte por firma | Bien modelada | ✅ Acierto |
| Plan de tests (property-based + simulación concurrencia) | Concreto y adecuado | ✅ Acierto |
| Identidad/authN de eventos + inyección en handoffs | Ausente | ❌ P0 |
| Idempotencia + fencing + versión por-aggregate | Solo versión global, sin idempotency key | ❌ P0 |
| Frontera de determinismo (LLM vs orquestador) | Implícita y sobre-vendida | ⚠️ P1 |
| Event log como fuente de verdad (secuencia/esquema/compactación) | Subespecificado | ⚠️ P1 |
| Presupuesto de coste / terminación global | Ausente | ⚠️ P1 |
| Compensación/saga para efectos irreversibles | Solo "rollback_plan" como artefacto | ⚠️ P2 |
| Granularidad de tool_policy / calibración de routing | Grueso / números mágicos | ⚠️ P2 |
| Supply chain (SBOM/SLSA) Fases 5–7 | Correcto pero prematuro | ⚠️ Sobre-diseño |

---

## 8. Conclusión

Dirección correcta, enmiendas correctas, ejecución técnica por encima del promedio. El documento ya hace bien lo más difícil de acertar (event sourcing, escritor único con intents, no-self-review como invariante, máquina de estados de QA con corte de bucles). **Pero no está listo como spec final hasta cerrar los dos P0 —identidad/seguridad de eventos e idempotencia/fencing— y aterrizar explícitamente la frontera de determinismo.** La auditabilidad que el documento persigue es precisamente lo que esos huecos comprometen: un log inmutable solo vale si cada evento es atribuible, idempotente y reproducible bajo una definición honesta de "replay".

Aprobar la dirección; condicionar la implementación.

---

## 9. Fuentes consultadas

- ESAA: Event Sourcing for Autonomous Agents in LLM-Based Software Engineering — https://arxiv.org/html/2602.23193v1
- Agent Orchestration Patterns (supervisor / pipeline / mesh) — https://www.augmentcode.com/guides/multi-agent-orchestration-architecture-guide
- The Orchestration of Multi-Agent Systems: Architectures, Protocols, Enterprise Adoption — https://arxiv.org/html/2601.13671v1
- OWASP GenAI Security Project — Top 10 Risks & Mitigations for Agentic AI (dic-2025) — https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/
- OWASP Top 10 Agentic AI (resumen) — https://graylog.org/post/what-is-the-owasp-top-10-agentic-ai/
- Durable Agent Execution in Production: Temporal, LangGraph, Event-Sourced State — https://agentmarketcap.ai/blog/2026/04/10/durable-agent-execution-production-temporal-modal-event-sourced
- Durable Execution in LangGraph — https://vadim.blog/durable-execution-agents-that-survive-failure-and-resume-where-they-left-off
- Beyond the Lock: Why Fencing Tokens Are Essential — https://levelup.gitconnected.com/beyond-the-lock-why-fencing-tokens-are-essential-5be0857d5a6a
- Lease Pattern in Distributed Systems — https://singhajit.com/distributed-systems/lease/
- Google A2A Protocol (agent cards, task lifecycle) — https://atlan.com/know/google-a2a-protocol/
- MCP vs A2A 2025 — https://futureagi.com/blogs/mcp-vs-a2a-2025
- Fair / least-loaded routing (MARL, variance-based fairness) — https://arxiv.org/pdf/2206.01451
- Software Supply Chain Security: SBOM, SLSA — https://www.trantorinc.com/blog/software-supply-chain-security-sbom-slsa-engineering-teams
- CycloneDX ML-BOM / AI-BOM (v1.7, ECMA-424) — https://agentmodeai.com/ai-bill-of-materials-supply-chain-disclosure/
