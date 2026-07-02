# PRE-DECISION - Router de ejecutores: el agente frontera decide peon vs tier

- fecha: 2026-07-02
- estado: **PRE-DECISION (CUARENTENA: el Arquitecto NO lee este documento;
  regla 3/7 del cortafuegos). Idea del Operador en discusion con el Asesor.
  Se formaliza como REQ post-Sprint 1.**
- origen: Operador 2026-07-02 ("el agente de frontera deberia poder decidir cuando
  usar un peon y cuando no... los modelos frontera tienen tiers... eso seria muy
  ganador"). Asesor: de acuerdo con matiz (abajo).
- base existente: DECISION-0074/D3 (backend hibrido, "router frontera" ya nombrado),
  DECISION-0078 (elegibilidad estatica de tareas), re-revision gentle-ai
  (model-routing por fase = adoptable), SPEC-F1-gate-intake (features de ruteo).

## 1. La idea (formulacion conjunta)

El agente frontera (implementador) decide POR TAREA quien ejecuta: peon local
(Ollama), tier barato de frontera (Haiku/Flash), tier medio (Sonnet), tier alto
(Fable/Opus). Tarea demasiado compleja para peon NO se le asigna; tarea trivial
NO consume tier alto.

## 2. El matiz que lo hace ganador (posicion del Asesor, aceptada en discusion)

"El agente elige modelo" a ojo lo hace todo el mundo (vibes-routing). El
diferenciador de ESTA metodologia es la tripleta:
1. Eleccion con RUBRICA (no vibes): features del bloque de intake.
2. Decision ATESTADA: evento firmado `routing.decision` en el ledger con rationale
   de enum cerrado (cero prosa en campos estructurales).
3. Acierto MEDIDO: el pre-registro/estudio mide la calidad del ruteo.
Nadie del landscape (BlockA2A, Agent Receipts, IETF AAT, nono) tiene ruteo de
costo con provenance firmada y medicion pre-registrada. Publicable y vendible.

## 3. Rubrica v1 (esbozo; features = bloque intake de SPEC-F1-gate-intake)

| Feature (intake) | Peon local | Tier barato | Tier medio | Tier alto |
|---|---|---|---|---|
| verification_cmd | gate objetivo fuerte (test/diff/golden) | gate parcial | gate parcial | criterio senior |
| type | mecanica/fixtures/scaffolding | doc/refactor guiado | feature acotada | arquitectura/seguridad/integracion novel |
| risk | low | low-medium | medium | high |
| estimate | S | S-M | M | M-L |
| regla 0078 | elegible estricta | n/a | n/a | NO elegible para peon |

Regla general: cuanto mas fuerte el gate de verificacion objetivo, mas barato el
ejecutor. Si la salida es funcion mecanica de la entrada: codegen/script antes que
cualquier LLM (0078).

Override: el agente PUEDE desviarse de la rubrica; el override se registra con
razon (enum: gate_debil | contexto_faltante | historial_fallos | urgencia | otro).
La TASA de overrides es metrica de salud de la rubrica.

## 4. Metricas del router (para el REQ futuro)

- tokens_firmante_total por tarea vs tier elegido (la de 0078, intacta: incluye
  rework -> la delegacion mala se paga; vacuna anti-Goodhart de sobre-delegacion).
- Tasa de escalamiento: peon/tier fallo gates -> re-ejecucion en tier superior
  (el error VISIBLE).
- Tasa de sobre-aprovisionamiento: tareas peon-elegibles ejecutadas en tier alto
  (el error INVISIBLE; nadie lo nota sin medirlo).
- Tasa y razones de override.

## 5. Limites (para no romper lo sellado)

- Q1 (pre-registro) NO se toca: mide A/B con brazos fijos. El router es FASE
  POSTERIOR o pregunta nueva (Q6 candidata); jamas retrofit al sello (seria la
  reinterpretacion post-hoc que el veredicto ronda 2 obliga a cerrar).
- El spike F6.0 (PLAN-SPIKE-PEONES-SANDBOX) puede ENSAYAR la rubrica MANUALMENTE:
  el firmante aplica la tabla s.3 a cada tarea de la tanda y anota la decision en
  la hoja de registro. Calibra la rubrica con cero infra nueva.
- Implementacion automatica (`routing.decision` + router.py): REQ para v1.19+,
  post-Sprint 1. NADA de esto entra en F1..F4 (gate 30-jul intocable).
- Peones keyless JAMAS firman (D3, invariante).

## 6. Proximo paso cuando el Operador lo decida

Convertir esto en REQ-ROUTER-EJECUTORES (area de requerimientos-futuros) con la
rubrica calibrada por el spike; entonces sale de cuarentena y se ordena al
Arquitecto via mailbox como cualquier REQ.
