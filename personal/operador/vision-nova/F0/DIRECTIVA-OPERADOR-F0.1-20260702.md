# DIRECTIVA OPERADOR F0.1 - Vision Nova (dos carriles)

- id: DIRECTIVA-OPERADOR-F0.1-20260702
- fecha: 2026-07-02
- emite: Operador (redaccion delegada al Asesor; autoridad escrita del 2026-07-02)
- estado: EMITIDA (el commit de este archivo en el area del operador es el acto de emision)
- relates_to: Area_comun/artifacts/ANALISTA-pivote-v2-veredicto.md,
  personal/operador/vision-nova/pipeline-vision-nova.html,
  personal/operador/vision-nova/rfc-vision-nova.html

## 1. Decision de direccion

1. El fork de Hermes (productizacion de Zeus-Aegis como producto instalable) queda
   DESCARTADO como meta activa. Lo construido se conserva: Zeus-Aegis queda como panel
   F1 read-only del hub (DECISION-0050 punto 4).
2. La meta activa pasa a ser VISION NOVA: la metodologia employee-ready como herramienta
   interna de la empresa + Nova Budget como primera instancia piloto, con estudio
   PRE-REGISTRADO (Q1-Q5) antes de la primera linea de codigo del sprint.
3. Marco de DOS CARRILES:
   - Carril A (PRINCIPAL): metodologia employee-ready (F1) + instancia nova-budget
     distribuida (F2) + estudio pre-registrado (F3) + Sprint 1 (F4). Consume la
     capacidad por defecto.
   - Carril B (SECUNDARIO, GATEADO): publicacion para ser REPRODUCIDO (dataset DOI +
     paquete reproducible + preprint + outreach institucional). Presupuesto MAXIMO
     1 dia/semana del operador, MEDIDO y registrado; si una semana lo excede, el
     carril se PAUSA automaticamente y se reporta el exceso. (Bloqueante 5, ronda 2.)
4. Lenguaje obligatorio en toda pieza publica: "publicar para ser REPRODUCIDO" (no
   "citado"). Claim estrecho unico: "primera implementacion de referencia OPERATIVA del
   ciclo task->claim->delivery->review->close con checker independiente, corpus
   longitudinal real y mediciones pre-registradas, sin blockchain". Concesiones de
   ronda 1 vigentes: no es SoD (es heterogeneidad de agentes con veredicto firmado),
   H1-H3 = tamper-evidence (no security proof), N=1 declarado.

## 2. Roadmap fechado

El tablero `pipeline-vision-nova.html` es la fuente de verdad de avance (el Arquitecto
lo marca solo con evidencia + sello de hora).

- F0 Formalizacion (sem 1, jul 3-11): esta directiva (F0.1) + DECISION-hub (F0.2).
- F1 Nucleo doctrinal v1.18.0 (sem 1-2, jul 3-18). F1.6 aprendizajes-externos =
  timebox 2 dias en paralelo, NUNCA en camino critico.
- F2 Instancia nova-budget distribuida (sem 3, jul 21-25): empleados remotos via
  clones + Git; el hub jamas se comparte con empleados.
- F3 Estudio pre-registrado (sem 3-4, jul 21-29): politica de empleados + sellado
  con ancla externa.
- F4 SPRINT 1 NOVA BUDGET = 30 DE JULIO. GATE DURO: se recorta alcance, nunca la fecha.
- F5 Memoria hibrida v1.19.0 + upgrade_instance (agosto).
- F6 Estudio en marcha (ago-dic): peones A/B, contraste condicional, interim 8 semanas.
- CB Carril B: cuando el Carril A lo permita, bajo el presupuesto del punto 1.3.

## 3. Los 8 bloqueantes de la ronda 2 = condiciones de formalizacion

Mapa al tablero: (1) politica de medicion de empleados -> F3.1; (2) eventos firmados de
ayudas/des-atascos/excepciones/arbitrajes -> F1.2; (3) trailers bloqueantes Task-Id /
Fixes-Task -> F1.3; (4) taxonomia D1-D4 ampliada + subconteo declarado -> F1.4;
(5) presupuesto Carril B medido con stop -> gate global CB; (6) DECISION supersede fork +
re-alcance 0230-0234 -> F0.2; (7) spike DSSE/in-toto/Rekor antes de prometer interop ->
CB.2; (8) sellado del pre-registro completo con hash + seq de inicio + reglas de
exclusion + ANCLA EXTERNA (OpenTimestamps/Zenodo DOI/Rekor) -> F3.4.

REGLA DURA: ninguna tarea del Sprint 1 arranca sin los bloqueantes 1, 2, 3, 4 y 8
cerrados. Los bloqueantes 5 y 7 gatean el Carril B, no el A.

## 4. Duenos de decision

- Operador: kill-decisions (mes 6/12/18), politica de empleados, nivel de publicacion
  del dataset, retencion, arranque de cada fase, aprobacion de releases mayores.
- Arquitecto: DECISION-hub y re-alcances de ledger, tablero (solo con evidencia),
  releases v1.18/v1.19, coordinacion de peers.
- Analista: gate adversarial de F1 y F3 y del sellado del pre-registro.
- Codex: implementacion de F1 (validador/runtime) bajo tareas con DoD testable.

## 5. Restricciones que NO cambian

Dataset TFM N=500 SELLADO intocable (tag TFM-dataset-N500); 5 pineados byte-identicos;
epoch v1.14.0 PINNED; core del protocolo neutral de dominio; sin secretos; F2
write-through del panel gateado; repos de producto bajo D:/Agentes/Zeus/ y gobierno
SIEMPRE en el hub (DECISION-0050); Engram cerrado (DECISION-0081): PROHIBIDO
`gentle-ai install` en maquinas Nova.

Firma: Operador (emision delegada al Asesor, 2026-07-02)
