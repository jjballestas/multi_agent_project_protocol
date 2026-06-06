---
decision_id: DECISION-0012
title: Normalizacion ASCII del canal de comunicacion entre agentes
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0006, DECISION-0009]
phase: P2
---

# DECISION-0012 - Normalizacion ASCII del canal entre agentes

## Contexto
La coordinacion entre agentes (mailbox + ledgers de estado) es el nucleo del protocolo. En esta sesion
Codex corrompio un mensaje de mailbox al moverlo entre carpetas: el fichero, escrito en UTF-8 con
acentos y simbolos (signo de interrogacion invertido, vocales acentuadas, guion largo, flechas), paso
por el codec por defecto de Windows (cp1252) y quedo con doble codificacion (mojibake). "Validador
verde" no lo detecto. El operador senalo que, siendo la coordinacion lo basico, si el metodo falla hay
que adaptarlo, y propuso normalizar a ASCII la conversacion entre IAs para eliminar la causa raiz.

## Decision
El **canal de coordinacion entre agentes** se escribe **ASCII-only**:

- **Alcance duro (ASCII-only):** `Area_comun/mailbox/**` y `Area_comun/state/*.json`. Estos artefactos
  los editan ambos agentes en cada turno y son el punto de corrupcion. Reglas de escritura: usar `->`
  en vez de flecha, `=>` en vez de doble flecha, `?` en vez de signo invertido, vocales sin tilde, `-`
  en vez de guion largo. Sin emojis ni simbolos no-ASCII.
- **Alcance blando (UTF-8 valido, sin mojibake):** prosa de cara al humano (`Area_comun/reports/**`,
  cuerpos de `decisions/**`, `tasks/**`, docs, READMEs, AGENTS.md). Puede llevar acentos correctos, pero
  no mojibake ni bytes invalidos.
- **I/O explicita:** al leer/escribir/mover ficheros compartidos, usar `encoding="utf-8"` (los JSON de
  estado siguen su convencion `utf-8-sig`); nunca depender del codec por defecto de la plataforma.

## Aprobacion humana
Propuesta y aprobada por el operador humano (2026-06-06). Aditiva y back-compatible: ASCII es un
subconjunto de UTF-8; solo restringe escrituras nuevas en el canal entre agentes. No rompe historicos.

## Versionado y neutralidad (DECISION-0001)
Convencion de proceso + gate de tooling, aditiva => MINOR. El gate vive en `scripts/` (neutral); no
introduce dominio. Se publica al madurar el gate.

## Enforcement (deriva a SPEC + TASK)
- **TASK-0033 (bajo DECISION-0006, robustez operacional):** `scan_encoding` (.py/.ps1 con paridad) que
  (a) falla ante cualquier byte no-ASCII en el alcance duro, (b) falla ante firmas de mojibake en
  cualquier artefacto, (c) corre en CI. Golden: fixture limpio pasa, fixture corrupto falla. Incluye
  limpiar los 3 ficheros legacy ya corruptos (TASK-0017/0018/0021) para dejar el gate verde.
- Secuencia: despues de TASK-0032 (no interrumpir el hito de observabilidad en curso).

## Consecuencias
- **Positivas:** elimina por construccion la corrupcion de encoding en el canal critico; el gate la
  vuelve imposible de mergear; coordinacion auditable y estable cross-plataforma.
- **Costo:** los mensajes entre agentes pierden acentos (legibilidad menor para el humano que los lea
  crudos; aceptado por el operador). La prosa de cara al humano conserva acentos.

## Alternativas consideradas
- **Solo detectar mojibake (sin ASCII-only):** descartada como unica medida; detecta el sintoma pero el
  canal seguiria aceptando acentos que vuelven a corromperse en el siguiente round-trip cp1252.
- **Forzar UTF-8 en todo el toolchain:** complementaria pero fragil cross-plataforma; ASCII-only en el
  canal es la garantia robusta. Se mantiene la I/O explicita en utf-8 como refuerzo.
