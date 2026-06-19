---
decision_id: DECISION-0041
title: Precondicion de acoplamiento - enforcement read-only REAL del satelite antes de cualquier lectura viva del Core (#2/#3), verificada por Codex (§9)
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0035, DECISION-0040, DECISION-0022, DECISION-0018]
phase: P2
---

# DECISION-0041 - Precondicion de acoplamiento read-only REAL

> ACCEPTED por el operador (GO de promocion 2026-06-19). Cambio
> aditivo, documental, neutral de dominio en el Core. Convierte una invariante hoy convencional en una
> precondicion dura, nombrada y con dueno.
>
> **Encuadre (GO del operador 2026-06-19):** esta decision **REFERENCIA DECISION-0035** y NO la
> redecide. La politica de satelite read-only unidireccional ya esta aceptada alli; A3 solo **anade la
> precondicion** de enforcement read-only REAL (verificada por Codex, §9) antes de cualquier lectura
> viva. Mismo patron que A1 (referencia DECISION-0029, no la duplica).

## Contexto

DECISION-0035 creo el satelite `protocol_research` (repo SEPARADO, read-only) con acoplamiento
**unidireccional** satelite -> Core. Hoy esa propiedad esta **sostenida por diseno, NO sandboxed**:
repo git separado (impide un *commit* al Core, no una escritura del working tree) + convencion
read-only + inspeccion estatica. En la fase de scaffolding todo es stub OFF (nada corre, riesgo real
nulo), pero **la garantia es convencional, no forzada** (asi lo declaro honestamente el satelite).

Cuando se franquee GATE-DATASET (DECISION-0040) para la **produccion** de #2 (PROV) / #3 (cost feed) o
se corra el harness tras GATE-INST, el satelite leera el Core **vivo** (incl. `runtime/state/events.jsonl`).
A partir de ahi la garantia convencional es insuficiente: un error de implementacion podria escribir el
Core. Esta decision fija la precondicion que lo impide.

## Decision

1. **Precondicion DURA.** Antes de que CUALQUIER codigo del satelite corra contra el Core **vivo** (al
   franquear GATE-DATASET para #2/#3, o al correr el harness tras GATE-INST), debe existir
   **enforcement read-only REAL**: el Core montado/clonado **read-only**, o el satelite corriendo bajo
   una **identidad sin permiso de escritura** al Core. No basta una asercion en codigo o docs de que
   "la ruta de lectura es read-only". **Ningun franqueo de gate permite jamas que el satelite escriba
   el Core.**

2. **Dueno: Codex (§9).** Codex verifica el invariante read-only **ANTES de cualquier lectura viva**,
   como precondicion explicita y registrada en la tarea de implementacion del acoplamiento/exportadores:
   - confirmar enforcement read-only real (montaje/clon read-only o identidad sin escritura) - no una
     mera asercion;
   - confirmar que **no existe ruta de escritura** al Core en el codigo implementado (un grep estatico
     es evadible: es una revision sustantiva, no un match de patron);
   - **prueba negativa OBJETIVA y registrada (no juicio del dueno):** ejecutar un **intento de escritura
     al Core que el SO RECHACE** (el proceso del satelite corre bajo identidad/montaje sin permiso de
     escritura al path del Core), y registrar el rechazo como evidencia reproducible -- analoga a la
     prueba negativa AC3 de A1. La verificacion de Codex NO descansa solo en su lectura del codigo.
   - **registrar** la verificacion (revision sustantiva + prueba negativa) en la tarea como precondicion
     explicita.
   Si la verificacion no esta, la lectura viva NO procede (no se cae en silencio).

3. **Direccion del acoplamiento (sin cambio).** El Core NO depende del satelite (no lo importa, no lo
   referencia en gates ni CI). La independencia del Core respecto a la agenda de investigacion descansa
   en repo-separado + cero dependencia de codigo, no en el scan de neutralidad.

4. **Notificacion de anomalia.** Si en cualquier momento se detecta una ruta de escritura del satelite
   al Core o una lectura viva sin la verificacion registrada, es una anomalia DECISION-0018: se notifica
   y se detiene; no se "arregla en silencio".

## Alcance / No-alcance

- **En alcance:** elevar la invariante unidireccional a precondicion dura con dueno (Codex), aplicable
  al franqueo de GATE-DATASET (#2/#3) y al harness (GATE-INST); registrar la verificacion como
  precondicion de la tarea.
- **Fuera de alcance:** implementar #2/#3 o el harness (siguen stubs OFF tras sus gates); construir el
  sandbox tecnico concreto (montaje/identidad) - eso es trabajo de implementacion bajo esta
  precondicion; tocar el Core como escritor.

## Consecuencias

- La invariante unidireccional deja de ser solo convencional: antes de cualquier lectura viva hay un
  control real verificado por un dueno nombrado, imposible de saltar en silencio.
- Da cobertura honesta al riesgo que el propio satelite declaro (garantia convencional en scaffolding):
  el momento de mayor riesgo (lectura viva) queda gateado.

## Alternativas consideradas

- **Confiar en la convencion + grep estatico.** Descartada: el grep es evadible y la convencion no es
  enforcement; insuficiente cuando el satelite lee el Core vivo.
- **Sandbox tecnico desde el scaffolding.** Innecesario hoy (todo stub OFF, riesgo nulo); el costo se
  justifica solo al llegar a la lectura viva. Por eso es precondicion del franqueo, no de la estructura.
