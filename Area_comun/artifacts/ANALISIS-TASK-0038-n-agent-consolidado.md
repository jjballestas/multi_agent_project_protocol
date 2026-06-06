# Análisis consolidado — TASK-0038 (Runtime de colaboración N-Agente)

**Tipo:** Análisis técnico unificado (documento único de record).
**Fecha:** 2026-06-06
**Autoría:** consolidación por el operador (análisis independiente) + Claude (arquitecto).
**Unifica:** `TASK-0038_IMPLEMENTACION_N_AGENT_READINESS_ANALISIS_TECNICO.md` (análisis técnico profundo) y
`ANALISIS_CRITICO_TASK-0038_N-AGENT.md` (revisión adversarial de segundo orden). Ambos se conservan como
fuentes; este documento es el análisis coherente único.
**Spec resultante:** `Area_comun/specs/SPEC-0038-n-agent-registry.md` (spec de record; decisiones
D-1..D-16 → `DECISION-0015`).
**Excluido:** evaluación legal, financiera, comercial, reputacional.

> Meta: la finalidad no es "tener más agentes", sino un **runtime de colaboración auditable** donde cada
> agente actúa bajo capacidad declarada, identidad autenticada, permiso limitado, estado verificable,
> handoff autocontenido, revisión independiente, QA reproducible y release trazable.

---

## 1. Veredicto

La dirección es **correcta y superior** a un mero "generalizar el roster". El movimiento arquitectónico
central — *los agentes no escriben estado; emiten intents append-only que un orquestador determinista de
escritor único valida y serializa sobre un snapshot derivado* — coincide con el estado del arte (event
sourcing para agentes, modelo de actividades de Temporal, checkpointing de LangGraph 1.0). Tratar
`owner`/`from`/`to`/`response_owner` como identificadores libres y localizar el único bloqueo duro en el
`enum` estático de `runtime/turn_schema.json` es correcto.

Honestamente: el diseño es **fuerte en workflow/estado/concurrencia** y, en su forma inicial, **débil en
cuatro frentes que para un sistema cuyo objetivo es la auditabilidad NO son accesorios**: (1) seguridad e
identidad agéntica; (2) idempotencia y fencing en el camino de aplicación; (3) la frontera real del
determinismo (LLM no determinista vs. orquestador determinista); (4) presupuesto de coste/latencia y
terminación. Además arrastraba **sobre-diseño** en fases tardías (observabilidad estilo OpenTelemetry,
SBOM/SLSA) para un protocolo que hoy corre 2 agentes sobre Markdown+JSON y no publica binarios.

**Resolución:** aprobar la **dirección**; **condicionar la implementación** a cerrar los P0 (identidad/
seguridad e idempotencia/fencing) y aterrizar la frontera de determinismo; reclasificar fases 5–7 como
diferidas. **Estos cierres ya están incorporados** en la SPEC-0038 consolidada (D-1..D-16, I1..I8).

---

## 2. Lo que acierta (acreditado)

- **Event sourcing + escritor único + snapshot derivado.** Decisión correcta; reduce colisiones porque los
  agentes dejan de competir por el archivo central.
- **`review ≠ author` y prohibición de self-QA elevados a invariante verificada por property tests**
  (I1, I2). Ingeniería por encima del promedio: no es norma escrita, es propiedad comprobable.
- **Leases para claims vencidos** (no borrar; marcar `expired`; permitir reclaim; rechazar reporte tardío).
- **Máquina de estados explícita para fallo de QA con corte de bucles por firma** (mismo check falla 2×
  con la misma firma → escalar a rediseño). Ataca el bucle implementador↔QA real.
- **Escalado humano como gate de decisión, no catch-all** (riesgo/política/irreversible/ambigüedad), no por
  imposibilidad operativa temporal.
- **Criterios de aceptación testeables + plan de tests con property-based y simulación de concurrencia**
  (10 implementadores / 100 tareas / leases vencidos / QA failures). Rara vez se ve especificado.
- **Matiz de SemVer sobre "enum como contrato público"**: MINOR si nadie externo valida el enum;
  potencialmente breaking si lo hace (doble compatibilidad documentada).

---

## 3. Huecos cerrados antes de implementar (P0/P1/P2)

### P0 — Seguridad e identidad agéntica
`assert report.agent in registry.enabled_agent_ids` solo comprueba el **string reclamado**; nada autentica
que el reporte lo emitió ese agente → la cadena de auditoría deja de ser atribuible. Segundo flanco:
goal/instruction hijacking por **inyección en el contenido de handoff/task** (OWASP Agentic). **Cierre
(D-1):** firmar/autenticar cada `turn_report` y evento (HMAC por agente en fase inicial, no PKI pesada);
separar instrucciones de datos en handoffs; ligar `trust_boundary` a política efectiva; rechazar y
registrar eventos no atribuibles (`security.unauthenticated_event`). Invariante I7.

### P0 — Idempotencia y fencing
Versión global de snapshot = fencing demasiado grueso → falsos conflictos entre tareas que no se tocan,
escala mal; sin `idempotency_key`, un reintento tras backoff puede **doble-aplicarse**; lease sin fencing
token queda expuesto al "proceso pausado". **Cierre (D-2, D-8):** `idempotency_key` por intent (dedupe en
el writer); concurrencia optimista **por-aggregate** (versión por-tarea, no global); **fencing token
monótono por-recurso**; rechazar escrituras con fencing menor. Invariantes I5, I8.

### P1 — Frontera de determinismo (estaba sobre-vendida)
"Replay determinista" solo aplica a las **transiciones de estado**, no a re-correr LLMs. **Cierre (D-12):**
regla explícita — *todo lo que toca el mundo exterior (LLM, herramienta, red, reloj, aleatoriedad) es un
evento registrado; el replay reconstruye estado desde eventos, no re-invoca agentes*; los tests de replay
verifican exactamente eso. Invariante I6.

### P1 — Event log como fuente de verdad (estaba subespecificado)
**Cierre (D-7, D-11):** secuencia global monótona (`seq`) + append atómico (tmp+rename / fsync, torn-write
safe); `event_schema_version`; snapshot/compactación por rango de `seq`; el snapshot es derivado y se valida
contra el log.

### P1 — Presupuesto de coste/latencia y terminación
Cortar *ciclos* no acota *coste*. **Cierre (D-14):** presupuesto de tokens + `deadline` por tarea y por
run; al agotarse, `escalated` con razón `budget_exhausted`. Límite independiente y complementario del corte
de ciclos.

### P2 — Tool policy, calibración de routing, compensación
**Cierre (D-13):** allowlist por-herramienta atada a capacidad + scope (no enum grueso). **(D-6):** pesos
de routing en config (no números mágicos) + `routing_decision.explanation` + **fairness ratio como gate de
CI**. **(D-16):** rollback de release como pasos de compensación (saga), no prosa.

---

## 4. Contraste con el estado del arte (2025/2026)

| Tema | Referencia SOTA | Estado en el diseño |
|---|---|---|
| Intents validados + orquestador determinista | Event sourcing para agentes (ESAA); Temporal; LangGraph 1.0 | Alineado (núcleo) |
| "Efecto externo = actividad/evento; lo demás determinista" | Temporal durable execution | Cerrado en D-12 |
| Leases + fencing tokens monótonos | Concurrencia distribuida (lease+fencing) | Cerrado en D-8 |
| Identidad/authN inter-agente + inyección | OWASP Top 10 Agentic (dic-2025); A2A (agentes autenticados) | Cerrado en D-1 |
| Capability discovery + task lifecycle | A2A (agent cards); MCP (agente-herramienta) | Reflejado en registry/estados |
| Observabilidad (trazas/métricas/logs) | OpenTelemetry | Fase 6 (condicionada) |
| Supply chain (provenance/SBOM) | SLSA; CycloneDX v1.7 (AI-BOM) | Fases 5–7 diferidas |

Conclusión del contraste: **alineado conceptualmente**; las brechas eran de **profundidad/rigor**, no de
dirección, y quedan cerradas en la spec consolidada.

---

## 5. Sobre-diseño y secuenciación honesta

- **Fases 0–4** (registry + validación semántica; event log + leases/fencing/idempotencia; router
  balanceado; máquina de estados Review/QA) = **el valor real y proporcionado**. Deben implementarse
  completas.
- **Fases 5–7** (observabilidad estilo OTel, SBOM/SLSA) = **condicionadas** a superficie real (acciones
  externas con efecto; publicación de binarios). Montarlas antes de tener algo que releasear es ceremonia,
  no confiabilidad.
- Todo **config-gated** con **fallback N=2 intacto** hasta demostrar N=3 y N=5 por simulación.

---

## 6. Recomendaciones (ya incorporadas a SPEC-0038 / DECISION-0015)

1. (P0) Firma/atribución de cada reporte y evento; sanitización de inputs de handoff; `trust_boundary`
   efectivo. Tests: evento no atribuible se rechaza; handoff malicioso contenido. → **D-1**.
2. (P0) `idempotency_key` por intent; fencing por-recurso; versión por-aggregate. Test: intent reintentado
   no se aplica dos veces. → **D-2, D-8**.
3. (P1) Frontera de determinismo explícita + tests de replay que la reflejen. → **D-12**.
4. (P1) Log con `seq` monótono + append atómico + esquema versionado + snapshot/compactación. → **D-7,D-11**.
5. (P1) Presupuesto de coste + deadline por tarea/run con escalado. → **D-14**.
6. (P2) Allowlist de herramientas por capacidad; fairness como gate de CI; saga para releases. → D-13,D-6,D-16.
7. (secuencia) Fases 5–7 diferidas a un release real. → §14 de la spec.

---

## 7. Próximos pasos (programa)

1. **Fase 0 — congelar diseño.** SPEC-0038 (de record) + DECISION-0015 (D-1..D-16). **Validación SOTA
   profunda independiente por Codex (TASK-0042)** como endurecimiento final, reconciliada por el
   arquitecto. Salida: aprobación humana; sin código.
2. **Fases 1–4 (núcleo)** implementadas en orden, config-gated, fallback N=2 intacto, cada fase con golden
   + property tests + replay + simulación de concurrencia; coordinación Claude (specs/review) ↔ Codex
   (implementación) por el protocolo.
3. **Fases 5–7** condicionadas a superficie real.

---

## 8. Fuentes

Event Sourcing for Autonomous Agents (ESAA, arXiv 2602.23193); Orchestration of Multi-Agent Systems
(arXiv 2601.13671); OWASP GenAI — Top 10 Agentic AI (dic-2025) y Top 10 LLM Apps 2025; Temporal/LangGraph
durable execution; fencing tokens + lease pattern; Google A2A (agent cards, task lifecycle, authN); MCP
2025-06-18; OpenTelemetry; SLSA; CycloneDX v1.7 (ML-BOM/AI-BOM); SemVer 2.0.0; JSON Schema. (URLs en
`ANALISIS_CRITICO_TASK-0038_N-AGENT.md` §9.)
