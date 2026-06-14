---
decision_id: DECISION-0035
title: Satelite de investigacion protocol_research (read-only, acoplamiento unidireccional) - estructura y scaffolding (#1)
status: accepted
date: 2026-06-14
ratified_at: 2026-06-14
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0010, DECISION-0033, DECISION-0034]
phase: P2
---

# DECISION-0035 - Satelite de investigacion protocol_research

> Estado: ACCEPTED (ratificada por el operador 2026-06-14, tras pasada del analista, que CONCURRIO con la
> reconciliacion del mapeo de gates al brief 07). Cambio ADITIVO, documental, neutral de dominio, en el
> Core. Autoriza un repo **SEPARADO, read-only** que no escribe el Core (sostenido por diseno, no
> sandboxed en esta fase). Alcance de ESTA decision = **ESTRUCTURA + SCAFFOLDING**: el satelite NO corre
> nada y NO publica nada. NO toca #3/flag, #4/chain-auth ni SA.4.

## Contexto

El item de investigacion **#1** (estudio MAST sobre el historial propio del proyecto) quedo DIFERIDO en
DECISION-0034: FAILURE_MODES.md es MAST **aplicado a incidentes de protocolo**, explicitamente **sin**
afirmar equivalencia 1:1 con MAST-Data ni cuantificar. Convertir eso en un dataset/estudio (y, mas
adelante, alimentar exportadores de procedencia #2 y de coste #3 y un harness de ablacion/TFM) es trabajo
de **investigacion**, no de protocolo. Mezclarlo en el Core romperia dos invariantes: la **neutralidad de
dominio** del Core y su independencia de cualquier agenda de investigacion.

La pieza que falta es el **continente**: un lugar separado para la investigacion, con un **acoplamiento
explicito y unidireccional** hacia el Core y con los **hard-stops** (gates) nombrados antes de que exista
cualquier dato o ejecucion.

## Decision

Se autoriza crear **`protocol_research/`** como **repositorio git SEPARADO, read-only**, ubicado como
**hermano del Core** en `d:\Agentes\protocol_research` (el Core esta en
`d:\Agentes\multi_agent_project_protocol`). Esta decision cubre **solo estructura y scaffolding**.

### Acoplamiento UNIDIRECCIONAL (sostenido por diseno, no sandboxed en esta fase)

- El satelite **lee** el Core por ruta relativa `../multi_agent_project_protocol` (artefactos publicos:
  `Area_comun/protocol/FAILURE_MODES.md`, decisiones, y -- bajo gate -- el event log).
- El satelite **no debe escribir** el Core (ni `Area_comun/`, ni `Area_comun/state/*.json`, ni config, ni
  el event log; no emite intents, no usa `runtime/submit_intent.py`, no toca el escritor unico). **Honesto
  (lente analista):** en la fase de estructura esto se **sostiene por diseno, no se garantiza
  tecnicamente**: repo git separado (impide un *commit* al Core, no una escritura del working tree) +
  convencion read-only + inspeccion estatica. **No hay sandbox** mientras todo sea stub OFF (nada corre,
  el riesgo real es nulo), pero la garantia es convencional, no forzada.
- **Enforcement read-only requerido antes de cualquier lectura viva:** antes de que CUALQUIER codigo del
  satelite corra contra el Core **vivo** (al franquear GATE-DATASET para #2/#3, o al correr el harness
  tras GATE-INST), se exige enforcement read-only **real** (Core montado/clonado read-only, o identidad
  sin permiso de escritura al Core). Ningun franqueo de gate permite jamas que el satelite escriba el Core.
- El Core **no depende** del satelite (no lo importa, no lo referencia en gates ni en CI). La direccion
  del acoplamiento es **satelite -> Core**. Asi el Core sigue **neutral** e independiente de la agenda de
  investigacion -- independencia que se sostiene en **repo-separado + cero dependencia de codigo**, no en
  el scan de neutralidad (que solo mira terminos de trading).
- Licencia/propiedad: el satelite hereda el regimen propietario (ARR, DECISION-0010); contenido INTERNO.

### Gates como hard-stops (nombrados ahora; nombres/asignacion segun brief del operador 07 sec.2/sec.5)

- **GATE-DATASET** (legal). Gobierna (a) la **citabilidad/publicacion** del dataset #1 y (b) la
  **produccion** del exportador #2 (PROV) y el feed #3 (cost-attribution). **NO** gobierna el uso
  **INTERNO** de #1: por ser historial PROPIO del proyecto sin PII de produccion (brief 07 sec.4), el uso
  interno **no requiere** GATE-DATASET. Hasta franquearlo: #1 es **INTERNO**, **NO 'citable'/publicable**,
  **sin** claim 1:1 con MAST-Data (comparabilidad solo **reportada** como limite), sin numeros no
  validados; #2/#3 quedan **stubs OFF**. El corpus es **seudonimo y re-identificable** (RGPD Cons.26 /
  Ley 1581; DECISION-0033). Su checklist de franqueo **incluye** una **asercion verificable** de
  honestidad de #1 (cero claim 1:1; cero 'citable'; cero numeros sin corpus validado) y el **enforcement
  read-only real** para #2/#3.
- **GATE-INST** (institucional). Aprobacion **institucional** (etica/institucional) para los experimentos
  de ablacion/TFM. Hasta franquearlo: el harness es **stub OFF**.
- **PRE-REG** (pre-registro experimental). Ningun experimento de ablacion/TFM **corre** hasta
  pre-registrar hipotesis y protocolo (H1/H2/H3, #7) -- diseno congelado antes de ver resultados, para
  evitar p-hacking. El harness se gobierna por **GATE-INST + PRE-REG** (+ volumen real). Hasta entonces:
  solo el **harness como stub OFF**.

### Alcance de #1 (en este satelite)

- #1 = **dataset MAST-sobre-historial-propio**, reusando la taxonomia y el mapeo de
  `FAILURE_MODES.md` del Core (no se redefine MAST aqui). **Versionado** e **INTERNO**.
- Comparabilidad con MAST-Data: **REPORTADA como limite**, nunca afirmada; 'citable' depende de
  **GATE-DATASET**. Sin numeros de severidad/frecuencia hasta tener datos validados.

### Contenido del scaffolding (no ejecutable)

`README.md` (contrato de acoplamiento + gates + alcance), `gates/GATES.md`, `datasets/mast_over_history/`
(README + schema del registro, **sin datos**), y **stubs OFF y NO ejecutables** de: `exporters/prov/`
(#2, gate GATE-DATASET), `feeds/cost_attribution/` (#3, gate GATE-DATASET) y `harness/ablation_tfm/`
(TFM, gates GATE-INST + PRE-REG), cada uno con su gate nombrado. Los stubs son specs de interfaz +
ficheros `*.py.stub` (extension no importable como modulo): el fichero es **inerte al ejecutarse** (las
funciones nunca se auto-invocan, no hay `__main__`); `NotImplementedError` solo se lanza si se **invoca**
la funcion. Nada en el satelite se ejecuta ni se publica con esta decision.

## Alcance / No-alcance

- **En alcance:** esta DECISION en el Core (autorizacion + acoplamiento + gates + alcance #1);
  crear el repo separado read-only con estructura + scaffolding; SemVer **MINOR** + CHANGELOG (en el
  Core, por la autorizacion documental).
- **Fuera de alcance:** poblar el dataset, ejecutar exportadores/feeds/harness, publicar, o afirmar
  comparabilidad/citabilidad (cada uno tras su gate + decision propia). NO se toca #3/flag, #4/chain-auth,
  `enforce`/`authoritative`, `subagents_enabled` ni SA.4. El satelite NO muta el Core.

## Versionado y neutralidad (DECISION-0001)

Aditiva en el Core: solo anade una decision + entrada CHANGELOG que **autoriza** el satelite; no cambia
comportamiento del Core. **MINOR** (v1.8.0). Neutralidad ESTRICTA: la investigacion vive en el repo
separado; el Core no gana terminos de dominio ni dependencias. Sin secretos.

## Consecuencias

- Existe un continente separado y read-only para #1/#2/#3/TFM, con acoplamiento unidireccional explicito:
  el Core permanece neutral e independiente de la investigacion.
- Los hard-stops quedan nombrados antes de que exista dato o ejecucion: ninguna pieza puede "colarse" a
  produccion/publicacion sin franquear su gate + una decision propia.
- #1 puede madurar como dataset interno versionado sin sobre-afirmar (no 'citable' hasta GATE-DATASET),
  preservando la honestidad fijada en DECISION-0034.
