---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-benchmark-peones-privado
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-18
context_refs:
  - Area_comun/artifacts/PROBE-COSTE-tabla-AvsB.md
  - personal/Arquitecto/DISENO-probe-coste-peon-local.md
one_line_summary: "Monta el PILOTO PRIVADO de benchmark de peones (coste + latencia + calidad) para encontrar el CRUCE donde delegar empieza a ganar. Aprende del A-vs-B de TASK-0006 (negativo a escala pequena: la ceremonia no amortiza). Diseno: escalera T1-T4 con gate DURO + eje ESCALA. Grid: T1-T3 x {qwen2.5-coder:3b, deepseek-coder:6.7b, qwen2.5-coder:7b}+Codex (lote pequeno); ESCALA T1-T2 x 7b+Codex (lote grande 50-100); T4 ceiling x 7b+Codex. Instrumento maker = Codex CLI (comparabilidad). PRIVADO / NO citable. EJECUTA tras cerrar TASK-0006."
requested_action: "[DIRECTIVA] Disena e instrumenta el piloto segun el protocolo de abajo (tu/Codex materializan las tareas por tier con su gate duro; Analista gatea). NO ejecutes hasta cerrar TASK-0006. Entrega la tabla de celdas + lectura del cruce. Es DEMO PRIVADA, no citable (anti-HARKing); el sellado publico seria un estudio aparte pre-registrado, solo si el piloto da relevancia."
question: "Confirmas el protocolo (tiers, grid, metricas) o ves un ajuste antes de instrumentar? Estimas cuantos execs frontier consume el grid para que el operador lo sepa?"
---

# DIRECTIVA - Piloto PRIVADO: benchmark de peones (coste + latencia + calidad)

## Objetivo y aprendizaje del A-vs-B
El A-vs-B de TASK-0006 salio NEGATIVO a escala pequena (delegar costo ~2x: el peon rindio
excelente pero la ceremonia spec+review no se amortizo a 10 tests). El piloto busca el **CRUCE**:
a que **escala** y **dificultad** la delegacion empieza a ganar. Es PILOTO PRIVADO (soporte a la
decision del operador), **NO citable**. El operador decide direccion con los resultados.

## Diseno (escalera de dificultad con gate DURO + eje ESCALA)
Regla dura: **toda tarea de todo tier lleva una suite determinista pass/fail** (calidad objetiva,
no opinion). Sin gate auto-verificable = fuera.

- **T1 mecanica pura:** N variaciones de un patron exacto (tipo los tests NEG PII de TASK-0006).
- **T2 mecanica con variacion:** funcion pequena desde spec precisa + 2-3 edge cases, con tests.
- **T3 juicio moderado:** implementar respetando un CONTRATO ya existente (leer una firma/interfaz
  definida y ajustarse) + una micro-decision de estructura; suite determinista.
- **T4 ceiling (logica dura AUTO-VERIFICABLE):** algoritmo no trivial de varios pasos con suite
  completa. **NO diseno abierto** (eso pierde el gate y solo confirma lo obvio). Prueba el techo
  de logica del mejor peon.

## Grid (lean, 1 corrida por celda = indicativo, no estadistico)
- **Escalera base:** T1, T2, T3 x { qwen2.5-coder:3b, deepseek-coder:6.7b, qwen2.5-coder:7b } +
  Codex-baseline por tier. Lote PEQUENO.
- **Eje ESCALA:** T1 y T2 con lote GRANDE (50-100 unidades del patron) x SOLO { qwen2.5-coder:7b }
  + Codex-baseline. (Aqui es donde el A-vs-B predice que la ceremonia SI podria amortizar.)
- **T4 ceiling:** SOLO { qwen2.5-coder:7b } + Codex-baseline, lote pequeno.
- Total ~18 celdas. No corras todo-x-todo (T4 y lote-grande solo con 7b+Codex).

## Metricas por celda
- **wall-clock** del peon (modelo WARM pre-cargado; anota estado GPU).
- **iteraciones-hasta-verde** (rondas de correccion del maker hasta suite verde) = proxy de calidad
  real / overhead spec+review.
- **delta tokens frontier** del maker (con vs sin delegacion), instrumento **Codex CLI** (mismo que
  TASK-0006, para comparabilidad).
- pass/fail + modo de fallo cualitativo.

## Baseline de maquina (medido por el Asesor 2026-07-18)
CPU Intel Core 7 250H (14c/20t); RAM 63.7 GB; GPU **RTX 5060 Laptop 8 GB VRAM** (nvidia-smi);
Ollama 0.32.0. Todos los coder-peones (1.9-4.7 GB) CABEN en VRAM -> **GPU-acelerados**. Anota esto
en cada corrida (los numeros solo valen con el hardware declarado).

## Controles y guardrails
Mismo texto de tarea por (tier, escala) para todos los ejecutores. Codex CLI como maker en todas.
Demo NO citable (anti-HARKing); PII de nomina fuera; fondo intocable (2E35F26E / 1.14.0 / N=500);
DECISION-0099 (spec del maker al peon = artefacto). EJECUTA tras cerrar TASK-0006.

-- Operador (via Asesor).
