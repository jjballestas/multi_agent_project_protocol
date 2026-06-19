---
decision_id: DECISION-0040 (DRAFT - id final al promover)
title: GATE-DATASET - base legal y esquema de dos planos para instrumentar el desarrollo del modulo-app de Presupuesto (Ley 1581/2012 + RGPD Cons.26)
status: draft (pendiente GO operador)
date: 2026-06-19
deciders: [operador humano (pendiente), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0033, DECISION-0035, DECISION-0010, DECISION-0001]
phase: P2
---

# DECISION-0040 (DRAFT) - GATE-DATASET (despeje legal + dos planos)

> DRAFT del Arquitecto para revision (Analista honestidad/metodologia + Codex invariante) y GO del
> operador. NO toca el ledger. La aprobacion por escrito del operador queda registrada como esta
> DECISION al promover. Cambio aditivo, documental, neutral de dominio en el Core.

## Contexto

El protocolo gobernara el **desarrollo del modulo-aplicacion de Presupuesto** sobre la DB ya migrada
(Access -> SQL Server, trabajo independiente del operador en `D:\Agentes\Ingenas\Budget`). **Corte
limpio (DECISION-0001 + brief):** el protocolo NO retrofitea la migracion; gobierna el desarrollo de
aqui en adelante. El **dataset de tesis es la coordinacion de agentes** (decisiones, handoffs, fallos,
coste), **NO** los datos municipales ni la migracion.

**El hecho nuevo que obliga este gate:** el modulo-app toca una DB con **PII real de terceros** (tabla
`maco009t` = 10.676 entidades con NIT). GATE-DATASET fue NOMBRADO como hard-stop en DECISION-0035 /
`gates/GATES.md` del satelite, pero sin despejarlo. Esta decision es el despeje legal y, sobre todo,
fija el **invariante que mantiene licita la instrumentacion interna sin consentimiento por evento**: la
PII de Budget **jamas entra al event log**.

## Decision

1. **Esquema de DOS PLANOS (DECISION-0033 reafirmado y endurecido).** El event log y el dataset de
   coordinacion contienen **solo plano de protocolo**: identificadores de agente, tarea, decision,
   estado, claims, coste, `canonical_hash` de artefactos. **CERO texto libre. CERO PII de terceros.**
   El payload se referencia por hash, no por contenido. La PII de Budget (NIT, razon social, datos de
   terceros) **permanece en SQL Server y nunca cruza al ledger ni al dataset de tesis.** Un handoff o
   evento que incluyera un NIT u otro dato de tercero es una violacion de boundary (anomalia
   DECISION-0018), no un caso aceptable.

2. **Base legal y minimizacion.** El tratamiento del dataset de coordinacion se ampara en:
   **Ley 1581/2012** (regimen colombiano de proteccion de datos; Galapa = municipio) y **RGPD Cons.26**
   (los datos seudonimizados/anonimizados quedan fuera del ambito cuando no permiten reidentificar). El
   `subject_hash` del corpus de coste es **seudonimo y re-identificable** (no anonimo): por eso el
   `actor` se restringe a **ids de agente no humano**, y el mapeo de reidentificacion **no forma parte
   del dataset**. Minimizacion: solo se captura el plano de protocolo necesario para estudiar la
   coordinacion.

3. **Limitacion de finalidad.** El dataset se usa para investigacion sobre **coordinacion de agentes**.
   No se usa para perfilar terceros ni para decisiones sobre personas (no hay datos de personas en el).

4. **DPIA-lite (evaluacion de impacto ligera).**
   - *Que datos:* plano de protocolo (agentes, tareas, decisiones, coste, hashes). No PII de terceros.
   - *Por que:* medir como coordinan los agentes el desarrollo del modulo-app.
   - *Riesgo:* reidentificacion del actor-agente (seudonimo) y, en el peor caso, fuga de PII de Budget
     al log por error de un agente.
   - *Mitigacion:* dos planos (sujeto por hash, sin texto libre) hace que la PII de Budget no este; el
     scan de canal/encoding y la regla de boundary detectan fugas; el mapeo de reidentificacion del
     actor se mantiene fuera del dataset; actores = solo agentes no humanos.

5. **Verificacion de ToS del proveedor LLM.** Antes de instrumentar, verificar por escrito que enviar
   **plano de protocolo (sin PII de terceros)** al proveedor LLM esta permitido por sus terminos, y que
   **ninguna PII de terceros de Budget se envia al LLM**. Registrar el resultado de la verificacion.

6. **Checklist de franqueo (de GATES.md) - alcance de ESTE despeje.** Esta decision despeja GATE-DATASET
   para la **instrumentacion INTERNA** del desarrollo del modulo-app (capturar la coordinacion como
   historial propio, sin PII de produccion). La **citabilidad/publicacion** del dataset y la
   **produccion** de los exportadores #2 (PROV) / feed #3 contra el Core vivo siguen condicionadas a:
   - **Aserciones de honestidad verificables para #1:** cero claim 1:1 con MAST-Data; cero "citable"
     hasta franqueo pleno; cero numeros sin corpus validado.
   - **Enforcement read-only REAL** antes de que #2/#3 corran contra el Core vivo (DECISION-0041 / A3).
   - **Base legal + minimizacion + de-linking** del payload para cualquier publicacion.
   - Para salida TFM/tesis: **GATE-INST** (aprobacion institucional/etica) + **PRE-REG** (pre-registro
     de hipotesis/metricas) ademas de este gate.

## Alcance / No-alcance

- **En alcance:** base legal, minimizacion, dos planos endurecido, DPIA-lite, verificacion de ToS,
  checklist de franqueo; habilita capturar la coordinacion del modulo-app de forma interna y licita.
- **Fuera de alcance:** publicar/citar el dataset; correr #2/#3 en produccion; experimentos TFM (eso es
  GATE-INST + PRE-REG); gobernar la DB de Budget o su migracion (corte limpio); introducir reglas
  fiscales en el core (van al perfil, Carril B).

## Consecuencias

- La instrumentacion del modulo-app es licita sin consentimiento por evento porque la PII de terceros
  nunca entra al dataset (dos planos).
- Queda explicito que publicar/citar exige el checklist completo + gates institucionales: honestidad
  preservada (no se sobre-afirma).
- El invariante "sin PII en el event log" pasa de buena practica a **condicion legal verificable**.

## Alternativas consideradas

- **Capturar payloads completos (con datos de Budget) y anonimizar despues.** Descartada: introduce PII
  de terceros al log, viola dos planos y la minimizacion; reidentificacion residual; riesgo legal alto.
- **No instrumentar hasta tener aprobacion institucional plena.** Descartada para el uso INTERNO: el
  historial propio sin PII no requiere GATE-INST (solo la salida TFM lo requiere); bloquear todo seria
  desproporcionado y retrasaria T0 del dataset sin reducir riesgo real.
