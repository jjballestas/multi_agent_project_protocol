---
task_id: TASK-0194
title: "Revision ADVERSARIAL (Analista) del pipeline Zeus-Aegis (DECISION-0064) + razonamiento de alcance pre-registro + measurement baseline"
type: review
status: ready
owner: Analista
phase: P2
priority: high
created_at: 2026-06-27
reviewer: Analista
author_under_review: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
linked_decisions: [DECISION-0064, DECISION-0066, DECISION-0050, DECISION-0040, DECISION-0046]
file: Area_comun/tasks/TASK-0194-analista-adversarial-review-zeus-aegis-pipeline.md
---

# TASK-0194 - Revision adversarial del pipeline Zeus-Aegis + alcance pre-registro + baseline

> reviewer=Analista / author_under_review=Arquitecto. **NO es un sello: busca el fallo.** El operador pidio una
> mirada adversarial independiente ANTES de continuar. Yo (Arquitecto) soy autor del pipeline, sujeto que firma el
> dataset Y quien atesto el baseline -> conflicto de independencia que TU debes presionar. Entrega un VEREDICTO con
> hallazgos accionables, no una validacion.

## Objeto bajo revision

1. **DECISION-0064** (UI operador = fork Hermes "Zeus-Aegis", cliente del single-writer; contrato
   `/api/governance/*`; fases F0->F4; gate F2 post-TFM; engram rechazado; gentle-ai/Dots solo inspiracion).
2. **Mi razonamiento de ALCANCE del pre-registro** (commit 5be3c85): que construir Zeus-Aegis cae DENTRO del
   pre-registro v2.0 FROZEN porque el corpus (seccion 6.2) es agnostico de dominio y H1/H2/H3 miden el MECANISMO #4.
3. **El MEASUREMENT BASELINE CANONICO UNICO** (supersede 8943756/seq 2191-2193 Y 9d96a95/seq 2213): core e1dc631,
   A2 + 3 firmantes, pins finales, N=500, dataset_start_seq=2221, stop-rule. (Reemitido tras tu review V2/V4.)

## Vectores adversariales (presiona cada uno; default = sospecha)

- **V1 Contaminacion de alcance.** Es REALMENTE limpio "construir Zeus-Aegis = generar dataset"? Alguna fase (incl
  F0) cambia el sistema medido o el modelo de amenaza A2? Es el gate de F2 la frontera correcta Y suficiente, o
  F0/F1 ya filtran (p.ej. Codex tocando el core del protocolo por error, o eventos de import/Electron que
  distorsionan)?
- **V2 Cambio de core post-freeze.** `runtime/eventlog.py` cambio +74 lineas DESPUES del freeze (TASK-0192/
  DECISION-0067). Mi defensa "plumbing del cutover, sin violacion sustantiva" -- se sostiene o es racionalizacion?
  CRITICO: el baseline se atesto **DESPUES de existir ya 16 eventos Ed25519**, no en cero. Es eso un olor post-hoc?
  Debio re-congelarse (v3.0) en el commit post-cutover ANTES del primer evento firmado? Cuantifica el dano (si lo hay).
- **V3 Independencia / conflicto de interes.** Arquitecto = sujeto (firma) + autor del pipeline + atestador del
  baseline. La seccion 8 del pre-registro ya declara "sujeto=medidor"; el baseline lo mitiga o lo agrava? Que harias
  distinto para que un tercero lo crea?
- **V4 N=500 y regla de parada.** 500 esta justificado/potenciado? La regla es ">=500" con un MONITOR que vigila el
  conteo -> riesgo de optional-stopping/peeking? Define el problema si existe.
- **V5 Representatividad del corpus.** Eventos mecanicos de F0 (imports, commits de docs, claims solo de Codex) son
  representativos de "coordinacion multi-agente gobernada", o sesgan el corpus frente a handoffs cruzados reales?
- **V6 Riesgos de arquitectura/licencia infravalorados.** Fork de Hermes (Electron + juego 3D + churn de API joven)
  afecta H3 (reproducibilidad desde clon limpio)? La estrategia MIT/atribucion/backend-separado tiene huecos?
- **V7 Veredictos Gentleman.** Rechazar engram y degradar gentle-ai/Dots a inspiracion -- correcto, o se descarto
  algo con valor real para la metodologia?

## DoD

- Veredicto por vector V1-V7: SOSTIENE / DEBIL / REFUTADO, con evidencia y el cambio concreto exigido si aplica.
- Conclusion: el pipeline y el baseline pueden CONTINUAR como estan, o hay un BLOQUEANTE (que y como remediarlo)
  antes de seguir generando/midiendo.
- Artefacto de veredicto en `Area_comun/artifacts/ANALISTA-TASK-0194-veredicto.md` + handoff a Arquitecto.
- Minimal narration. Si algo es ambiguo -> una pregunta concreta, no suposiciones.
