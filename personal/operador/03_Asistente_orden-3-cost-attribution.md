# 03_Asistente - Orden de construccion: #3 cost-attribution por handoff

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El asistente NO redacta la DECISION/SPEC ni implementa: esto es el brief de requisitos.
> El arquitecto redacta DECISION-00xx + SPEC-00xx y construye, todo via submit_intent desde VS Code.
> Fecha: 2026-06-14. Es el Paso 2 del plan aprobado por el operador (02_Asistente).

## 1. Que se pide (objetivo)

Construir #3 de la hoja de ruta: imputacion de coste de tokens POR handoff / decision / agente.
Hoy la medicion es agregada / tope global (`budget.py`); falta granularidad por evento. Esta es la
instrumentacion de medicion que debe estar VIVA antes del piloto del loop (Paso 3), para capturar en
caliente y no retrofitar.

## 2. Alcance funcional (que tocar)

- Extender `runtime/budget.py` + `runtime/metrics.py`; leer de `runtime/eventlog.py` (`seq`, `canonical_hash`).
- Imputar tokens por: handoff, decision y agente (las tres dimensiones).
- Esquema de DOS PLANOS (hoja de ruta Fase 3 / doc. 03): plano de protocolo SIN texto libre; la carga util
  solo por hash. La metrica vive en el plano de protocolo; nada de contenido sensible.
- Off-by-default: flag nuevo en `protocol.config.json` (p.ej. `metrics.cost_attribution_enabled=false`).

NO incluir aqui (son otras tareas, otra ventana): #2 PROV-AGENT (export W3C PROV) ni #4 firma por agente.
No activar el loop en esta tarea.

## 3. Entrada por el metodo (lo que el arquitecto debe producir)

1. DECISION-00xx registrada ANTES de aplicar (aditiva, off-by-default; SemVer MINOR + CHANGELOG; neutral de dominio).
2. SPEC-00xx con `acceptance_criteria` + `test_plan`.
3. Golden case determinista.
4. Sin romper neutralidad del nucleo; sin secretos.

## 4. Barra de aceptacion (lo que el operador espera ver, verificable)

- Determinista: misma entrada -> misma imputacion (golden estable).
- El golden cubre: (a) un handoff simple imputado al agente correcto; (b) VARIOS handoffs en una corrida sin
  agregacion cruzada (cada uno imputado por separado); (c) caso por decision.
- Off-by-default: con el flag en false, comportamiento byte-equivalente al actual (sin regresion).
- Sin regresion en los intent_flow goldens ni en el hard-gate (enforce: `enforced=True`, `has_drift=False`).
- Export/lectura de la metrica documentada en 1-2 frases (como se lee el coste por handoff).

## 5. Verificacion EN CALIENTE (criterio de "hecho")

No basta con cablear y pasar el golden. Marcar #3 hecho SOLO cuando:
- Con el flag activo, una transaccion/handoff real (o el smoke del wrapper) produzca la imputacion en el momento
  del evento (leida del eventlog), no calculada despues.
- Drift 0 sostenido, replay==hot.
- Reflejarlo en la reconciliacion de la hoja (Paso 1): #3 pasa de no-hecho a hecho con evidencia (commit + golden verde).

## 6. Restricciones de integridad (innegociables)
- Mutaciones SOLO por submit_intent desde VS Code (escritor unico). Edicion manual = drift.
- SemVer MINOR + entrada en CHANGELOG (cambio visible del protocolo).
- No tocar enforce/authoritative; subagents_enabled false; SA.4/loop fuera de esta tarea.
- Neutralidad de dominio en nucleo y `*.template.*`. Ningun numero no medido como promesa.

## 7. Orden corta para pegar al arquitecto
"Arquitecto: construye #3 (cost-attribution por handoff/decision/agente) entrando por el metodo:
DECISION + SPEC(acceptance+test_plan) + golden determinista, off-by-default (flag en config), esquema de dos
planos (plano de protocolo sin texto libre, carga util por hash), extendiendo budget.py + metrics.py sobre
eventlog.py. Golden cubre handoff simple, varios handoffs sin agregacion cruzada, y por decision; con flag off
byte-equivalente al actual; sin regresion en intent_flow ni en el hard-gate. Verifica EN CALIENTE (la imputacion
aparece en el evento real, no retrofiteada) con drift 0 y replay==hot. SemVer MINOR + CHANGELOG. No toques
enforce/authoritative; subagents OFF; loop fuera de esta tarea. Todo por submit_intent. Reporta para ratificacion."
