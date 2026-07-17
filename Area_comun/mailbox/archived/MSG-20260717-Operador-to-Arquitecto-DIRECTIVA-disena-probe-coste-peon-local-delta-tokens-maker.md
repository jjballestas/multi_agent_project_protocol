---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-disena-probe-coste-peon-local-delta-tokens-maker
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
one_line_summary: "DISENA un probe de COSTE: cablear un peon LOCAL (Ollama qwen/deepseek) como sub-worker que el MAKER delega, para MEDIR si reduce el consumo de tokens FRONTIER del maker. Fase A no lo toco (maker frontier hizo todo solo) -> la value-prop de coste esta sin medir. Demo primero (soporte a decision, no citable); riguroso = pre-registro (Fase B). Ejecuta TRAS cerrar U4, no disrumpas el build."
requested_action: "[DIRECTIVA] Disena el probe de reduccion de tokens del peon (diseno abajo, objetable) y devuelve el diseno para revision. NO lo ejecutes hasta cerrar U4 (Fase A). Papel/diseno ahora."
question: "Confirmas el diseno (sub-tarea mecanica de alto volumen, 2 condiciones maker-solo vs maker-delega-a-peon, metrica = delta de tokens frontier del maker contando overhead de spec+review)? Propones mejor sub-tarea o metrica?"
---

# DIRECTIVA - Disena el probe de coste: el peon local reduce los tokens del maker?

## El hueco (por que)
Fase A demostro (1) que la memoria funciona y (2) que el gate caza bugs, pero el **maker frontier
lo hizo TODO solo** -> el modelo peon nunca se cableo. La 3a value-prop de la metodologia -- COSTE
(peones locales baratos que descargan al maker frontier caro) -- esta **sin medir**. Sin cablear
un peon local no se puede saber si reduce el consumo de tokens del maker.

## [RECOMENDACION] Diseno del probe (objetable)
- **Cableado:** un peon LOCAL (Ollama, p.ej. qwen2.5-coder:7b o deepseek-coder:6.7b) como
  sub-worker que el MAKER (Codex frontier) delega, cumpliendo DECISION-0099: peon SUBORDINADO,
  el maker le da spec DETALLADA y responde por el resultado ante el checker.
- **Sub-tarea objetivo = MECANICA de ALTO VOLUMEN** (donde la delegacion plausiblemente gana): p.ej.
  generar un lote de tests negativos boilerplate / fixtures repetitivos. NO una sub-tarea compleja
  (ahi el overhead de spec+review se come el ahorro).
- **Dos condiciones, misma sub-tarea:** (A) maker-solo (baseline); (B) maker-delega-al-peon.
- **Metrica = delta de tokens FRONTIER del maker** (los del peon local ~= gratis). CLAVE: contar en
  el coste del maker el overhead de (a) escribir la spec del peon + (b) revisar/integrar su salida.
  El ahorro neto solo cuenta si (spec+review) < hacerlo-directo. El Codex CLI ya reporta tokens.
- **Salida:** delta observado + lectura cualitativa (que clase de sub-tarea ahorra, cual no).

## Firewall (clase de evidencia)
- **DEMO primero** = soporte a la decision del operador, **NO citable** (anti-HARKing). Un numero
  RIGUROSO/citable exige pre-registro (Fase B) si la demo promete. No confundir clases.

## Timing y guardrails
- **Ejecuta TRAS cerrar U4** (Fase A). Diseno/papel ahora; no disrumpas el build en curso.
- PII de nomina fuera del store; fondo intocable (2E35F26E / epoch 1.14.0 / N=500); DECISION-0099
  (peon maker-only, checker fuerte -- el peon aqui es lado-maker, el checker sigue fuerte); 0081
  intacta. Es un probe de COSTE del carril, no toca el estudio medido.

Devuelve el diseno para mi revision antes de ejecutar.

-- Operador (via Asesor).
