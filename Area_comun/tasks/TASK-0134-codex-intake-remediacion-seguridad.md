---
task_id: TASK-0134
title: "Proyecto-front - REMEDIACION DE SEGURIDAD del intake (RF-14): anti-impersonacion (builders server-side, sin trust de payload.actorId/intents) + relay acotado + camino feliz write-real + accountability"
type: product
status: in_progress
owner: Codex
phase: P2
priority: critical
spec_id: SPEC-0086
linked_decisions: [DECISION-0052, DECISION-0051, DECISION-0018, DECISION-0040]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0134-codex-intake-remediacion-seguridad.md
---

# TASK-0134 - Remediacion de seguridad del intake (RF-14)

> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol. Ratificado: DECISION-0052 + ext2 SPEC-0086
> (AC15 revisado, AC18, AC19, AC20, AC4-byte). **Remediacion de un defecto de seguridad CRITICO ya mergeado
> (Zeus 42e7931, anomalia DECISION-0018), no solo "agregar el relay".**

## Contexto del defecto (anomalia DECISION-0018, en canonico Zeus 42e7931)
`src/server.js`: `actorId = action.actorId || payload.actorId || "Arquitecto"` (linea 384) + para acciones
no-intake los `intents` vienen crudos del cliente (linea 371; solo se valida el kind). Endpoint 127.0.0.1 sin
auth -> un POST local puede forjar decision/claim/task_status atestado firmado como Arquitecto.

## Alcance (remediacion)
1. **#1 ANTI-IMPERSONACION (CRITICO, AC19):** eliminar el trust de `payload.actorId` y de `payload.intents`
   crudos. Cada accion = builder SERVER-SIDE con forma estricta (construye el intent desde campos validados).
   `actorId` server-side. Relay-como-Arquitecto SOLO para la forma exacta `requirement-intake`. Prueba
   negativa PERMANENTE en CI: forjar actorId/intents/forma != intake como Arquitecto -> RECHAZADO.
2. **#3 ACCOUNTABILITY (AC20):** evento con `endorsement:none`; firma=origen+transporte, no aval; test de que
   un relayado NO cuenta como autorado/avalado por el Arquitecto.
3. **CAMINO FELIZ (AC15, write REAL no mock):** test de comportamiento permanente: execute+confirm ->
   escritura real (requirement en estado, seq, drift 0, author=Operador/relayed_by=Arquitecto).
4. **RENDER honesto (AC18):** UI muestra firmante=Arquitecto + author=Operador; ningun verde "Operador firmo".
5. **#4 byte-identico (AC4-byte):** asertar config/genesis/keys/version byte-identicos (no solo drift 0).
6. **PII (AC16):** redaccion estructural best-effort por patrones; NO sobre-afirmar PII-free; DEF-PII gate.
7. **UX (Claude Design):** project-first + tipografia del selector destacada (rework de components/intake/).
8. **(opcional/follow-on):** endurecer endpoint local (token/same-origin/loopback-auth) contra drive-by.

## DoD / CONDICION DE CIERRE (innegociable)
- **(a) AC19 anti-impersonacion VERDE** + **(b) AC15 camino feliz con write REAL VERDE.** NO cierra sin ambas.
- AC18/AC20 + #4 byte-identico + AC16 + carry AC11/AC12/AC13/AC14/AC17 verdes.
- node --test/CI verde (AC19 y AC15 permanentes); npm start ejecutable; vista Intake navega y ESCRIBE.
- validate exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 byte-identica;
  neutralidad limpia.
- **NUEVA pasada del Analista sobre el fix de #1 ANTES de cerrar** (que el remedio cierre la impersonacion,
  no solo la declare).
- Reproducido por el checker (Arquitecto) desde clon limpio, incluyendo el write real Y la prueba de
  impersonacion; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Operador como firmante propio (re-genesis RF-9 roster, DIFERIDO). DEF-PII vivo (TASK-0118 gate).
