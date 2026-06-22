---
task_id: TASK-0154
title: "Proyecto-front: behavior-tests regresion-proof de 3 UX reconciliados (AC48 boton gobernado / AC49 no-reset Nueva-historia / AC50 canonico fresco sin reiniciar) (SPEC-0086)"
type: product
status: done
owner: Codex
phase: P2
priority: medium
spec_id: SPEC-0086
linked_decisions: []
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0154-codex-ux-behavior-tests-regresion-proof.md
---

# TASK-0154 - behavior-tests regresion-proof de 3 UX (AC48/AC49/AC50)

> El operador ratifico el triage: REQ-40EC863F / REQ-0873A67C / REQ-6D80DB17 quedaron `done` (el comportamiento
> ya esta en el front). Esta tarea agrega los behavior-tests PERMANENTES para que NO regresen. maker=Codex /
> checker=Arquitecto + pasada del Analista.

## Alcance (solo tests; el comportamiento ya existe)
1. **AC48 - boton 'Nueva historia/requisito' gobernado:** test que asierta que el boton usa la clase
   `governed-button` del design-system + tokens (no estilo ad-hoc). Control: un boton sin la clase gobernada
   rompe el test.
2. **AC49 - 'Nueva historia' NO resetea el form tipeado:** test de comportamiento que simula texto en el form +
   accion 'Nueva historia' (compose, SIN execute) -> el contenido PERSISTE; el reset ocurre solo con
   `status.variant === "ok"` (AC21). Control: un reset en 'Nueva historia' rompe el test.
3. **AC50 - canonico fresco sin reiniciar el server:** test que cambia el HEAD canonico entre dos requests del
   server y asierta que el 2do request refleja el cambio (lectura fresca via git show/diff, sin cache de modulo).
   Control: un cache de modulo del canonico rompe el test.

## DoD
- AC48/AC49/AC50 verdes con behavior-tests deterministas (sin flake). Carry de toda la suite (npm verde).
- node --test/CI verde EN CLON LIMPIO; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4
  byte-identica (cambio acotado a tests + lo minimo de front si falta exponer un marcador).
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- NO enciende nada vivo.

## Prereq
TASK-0153 cerrada (hecho). Triage ratificado (hecho).
