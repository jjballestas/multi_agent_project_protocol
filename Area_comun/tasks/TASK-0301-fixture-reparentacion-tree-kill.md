---
task_id: TASK-0301
file: Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md
title: "Endurecer run_complete_tree_kill_case con fixture de re-parentacion de nietos"
status: proposed
type: test
owner: unassigned
priority: normal
depends_on:
  - TASK-0300
created_at: 2026-07-28
goal: >
  Cerrar el residual R1 de TASK-0300. El caso de regresion run_complete_tree_kill_case (examples/mailbox_retry_cases/
  run_mailbox_retry_cases.py) verifica que Stop-LeaseProcessTree snapshotea el set completo de descendientes ANTES de
  matar la raiz, PERO opera sobre un arbol de procesos INTACTO -- no ejercita el escenario REAL del incidente: un
  nieto RE-PARENTADO (cuyo padre intermedio ya murio) que `taskkill /T` pierde. El mecanismo del fix es correcto y
  AC2 se cumple literal, pero el test no falla si alguien revierte la parte de re-parentacion del barrido
  compensatorio. Anadir un fixture que simule la re-parentacion (nieto sobreviviente a la muerte del padre
  intermedio) y asevere no-survivors, para que el caso sea FALSABLE contra esa regresion especifica.
acceptance: >
  AC1: run_complete_tree_kill_case (o un caso hermano nuevo) construye un arbol donde un nieto queda re-parentado
  (padre intermedio muerto antes del kill de la raiz) y asevera 0 survivors tras Stop-LeaseProcessTree.
  AC2 (falsabilidad): mutar el runner para que el barrido compensatorio NO recoja los procesos re-parentados hace
  FALLAR el caso (survivor real detectado) -- no vacuo.
  AC3: `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` sale 0; sin regresion en los casos previos.
  AC4 alcance: solo examples/mailbox_retry_cases/ (+ si hace falta un helper de fixture); protocol.config.json
  byte-identico; scripts/harness/peer_mailbox_cron.ps1 sin cambios (el fix ya esta; esto es SOLO cobertura de test).
verification_cmd: "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
scope_routes:
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
out_of_scope: >
  El harness peer_mailbox_cron.ps1 (el fix de tree-kill ya esta en TASK-0300); hangs de proveedor del LLM; el
  review-task-hang headless de la Analista; cualquier producto Zeus/Nova.
risk: low
estimate: S
notes: >
  Origen: residual R1 del review adversarial de fallback de TASK-0300 (2026-07-28). NO bloquea el cierre de 0300
  (ratificada review_approved). Prioridad normal -- encolar cuando el operador priorice el backlog de endurecimiento.
---

# TASK-0301 - Fixture de re-parentacion para run_complete_tree_kill_case

## Contexto
TASK-0300 endurecio el harness con `Stop-LeaseProcessTree`, que snapshotea el set COMPLETO de descendientes ANTES de
matar la raiz + un barrido compensatorio, para no perder nietos re-parentados como los que `taskkill /T` deja
huerfanos (el patron zombie que colgaba los execs subsiguientes). El caso de regresion `run_complete_tree_kill_case`
prueba el snapshot-antes-de-matar sobre un arbol INTACTO, pero no simula la RE-PARENTACION real (nieto cuyo padre
intermedio ya murio). El mecanismo es correcto; falta la cobertura falsable de ese vector especifico.

## Que hacer
Anadir un fixture (proceso raiz -> hijo -> nieto; matar el hijo intermedio ANTES de invocar el tree-kill de la raiz,
de modo que el nieto quede re-parentado bajo el proceso init/otro) y asevera 0 survivors tras `Stop-LeaseProcessTree`.
Verifica falsabilidad mutando el barrido compensatorio (que ignore procesos cuyo padre-intermedio ya murio) -> el
caso debe FALLAR con un survivor real.

## No hacer
No tocar el harness (el fix ya esta). Solo cobertura de test en el banco de regresion. Fondo intocable byte-identico.
