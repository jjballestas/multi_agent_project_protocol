---
id: TASK-0118
title: DEF-PII - detector de PII real / exporter del plano publicable (condicion antes de captura viva #2/#3) (DECISION-0040)
type: security
status: proposed
owner: Codex
phase: P2
priority: normal
spec_id: none
linked_decisions: [DECISION-0040, DECISION-0033]
created_at: 2026-06-19
---

# TASK-0118 - DEF-PII (detector de PII / exporter del plano publicable)

## Objective

Convertir la garantia "cero PII de terceros en el event log" de **disciplinaria** a **estructural**
(DECISION-0040): un scanner/validador que detecte PII de terceros (NIT colombiano, razon social,
rutas/payloads SQL de Budget) en el plano de protocolo, y/o un exporter que emita SOLO campos
estructurados + hashes para el dataset publicable.

## DIFERIDA - condicion, no trabajo activo (regla 3.4)

`status: proposed`. **NO se construye ahora.** Condicion DURA: DEF-PII **DEBE cerrar ANTES de la captura
viva publicable** -- es decir, antes del **primer franqueo de #2/#3 contra el Core vivo o cualquier
publicacion** del dataset. NO bloquea Carril A hoy (la instrumentacion interna se sostiene por el control
disciplinario + dos planos para el sujeto-por-hash). Se activa cuando se planifique #2/#3/publicacion.

## DoD

Detector/exporter implementado + golden (PII de tercero detectada/rechazada; plano publicable solo
estructurado + hashes); cierra ANTES del franqueo de #2/#3 o publicacion; SemVer MINOR + CHANGELOG.
