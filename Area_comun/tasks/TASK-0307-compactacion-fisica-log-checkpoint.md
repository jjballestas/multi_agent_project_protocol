---
task_id: TASK-0307
file: Area_comun/tasks/TASK-0307-compactacion-fisica-log-checkpoint.md
title: "Palanca C (DECISION-0105): compactacion fisica del log sobre el limite del checkpoint firmado + pulido fail-closed"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: normal
depends_on:
  - TASK-0306
relates_to:
  - DECISION-0105
  - TASK-0305
created_at: 2026-07-30
intake:
  type: infra
  goal: >
    Implementar la palanca C de DECISION-0105: cablear compact_through(up_to_seq) sobre el LIMITE del checkpoint
    firmado (TASK-0306) para acotar el log FISICAMENTE. Hoy events.jsonl crece sin cota (cold-start + disco). Mover
    los eventos <= up_to_seq del checkpoint de confianza a un archivo (runtime/state/archives/events-<lo>-<hi>.jsonl)
    y dejar solo la cola caliente en events.jsonl; el camino vivo confia en el prefijo archivado (respaldado por el
    checkpoint firmado + el hash del propio archivo) y solo re-verifica la cola caliente -> O(cola). El gate OFFLINE
    lee AMBOS (archivos + cola) y sigue full-auditando TODOS los eventos. El umbral de compactacion vive en
    runtime/CHECKPOINT_POLICY.json (fuera del config pineado). FAIL-SAFE: si un archivo no casa su hash -> caer a
    verificacion completa. Ademas, PLEGAR el pulido del residual compartido de 0306 (ambas capas): un up_to_seq/
    K_max NO-numerico debe degradar GRACIOSAMENTE a trusted:False (verificacion completa) en vez de abortar el submit
    por excepcion -- misma zona de codigo del checkpoint.
  acceptance:
    - "AC1 (compactacion cableada): compact_through(up_to_seq) se invoca sobre el limite del checkpoint de confianza cuando el log caliente cruza un umbral (en runtime/CHECKPOINT_POLICY.json, fuera del config pineado); mueve los eventos <= up_to_seq a runtime/state/archives/events-<lo>-<hi>.jsonl con un hash de integridad del archivo, y deja la cola caliente en events.jsonl."
    - "AC2 (union byte-identica -- EL vector critico de perdida): tras compactar, leer (archivos + cola) via events_in_log_order re-materializa al MISMO estado (canonical_hash IDENTICO) que antes de compactar, y devuelve el MISMO conjunto ordenado completo de eventos (ninguno perdido ni duplicado). Diferencial: estado/orden antes == despues. Ningun evento se pierde."
    - "AC3 (camino vivo O(cola)): replay_events con compactacion verifica SOLO la cola caliente (confiando en el prefijo archivado via el checkpoint firmado); medir que el coste de verificacion cae a O(cola), no O(todos). Byte-identico al full."
    - "AC4 (gate offline lee archivos + FAIL-SAFE): validate_collaboration_state.py / validate_chain leen archivos + cola y full-verifican TODOS los eventos (cadena + firmas sobre la union); un evento manipulado EN UN ARCHIVO SIGUE cazado offline. Fail-safe: si el hash/integridad de un archivo NO casa -> caer a verificacion COMPLETA (no confiar un archivo malo), nunca skip."
    - "AC5 (pulido fail-closed, plegado de 0306): un up_to_seq/K_max NO-numerico en el checkpoint/policy degrada GRACIOSAMENTE a trusted:False (verificacion completa) en vez de lanzar excepcion que aborte el submit. Test: valor malformado -> trusted:False -> full -> el submit completa."
    - "AC6 (alcance/config): runtime/eventlog.py (+ umbral en CHECKPOINT_POLICY.json + test); protocol.config.json BYTE-IDENTICO; sin genesis/re-genesis; sin cambio en QUE se verifica; el gate offline lee los archivos. Fallback y otros callers intactos."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - runtime/eventlog.py
  out_of_scope: >
    Cambiar protocol.config.json o el genesis. Cambiar el modelo de confianza del checkpoint (eso fue B/TASK-0306).
    Cambiar QUE se verifica de los eventos. Podar/borrar eventos de verdad (compactar MUEVE a archivo, no borra; la
    union sigue completa y auditada). Producto Zeus.
  risk: high
  estimate: M
notes: >
  Palanca C de DECISION-0105 (operador aprobo B+C misma tanda). RIESGO ALTO: mueve eventos FISICAMENTE fuera del log
  caliente -- el peligro es PERDIDA/DUPLICADO de eventos o romper la cadena. La seguridad son AC2 (la union
  re-materializa IDENTICO, cero perdida) + AC4 (el offline lee archivos y full-audita + fail-safe si un archivo no
  casa) + el gate adversarial de 2 capas. compact_through ya existe pero sin callers ni ganancia (hoy re-lee los
  archivos); esta tarea lo cablea sobre el limite del checkpoint para que la ganancia sea real. Cierra la tanda B+C.
---

# TASK-0307 - Palanca C: compactacion fisica del log sobre el checkpoint (DECISION-0105)

## Contexto
DECISION-0105 palanca C. B (TASK-0306) dio el checkpoint firmado + verificacion incremental O(nuevos). C acota el
log FISICAMENTE: mueve el prefijo <= up_to_seq a un archivo y deja la cola caliente, para que el camino vivo re-lea
menos (O(cola)) y el cold-start/disco no crezcan sin cota. El gate offline sigue full sobre la union.

## Que hacer
1. Cablear compact_through(up_to_seq) sobre el limite del checkpoint de confianza + umbral en CHECKPOINT_POLICY.json.
2. Archivo con hash de integridad; events_in_log_order lee archivos + cola; camino vivo confia el prefijo archivado.
3. Gate offline lee archivos + cola y full-audita; fail-safe si un archivo no casa -> full.
4. Plegar el pulido de 0306: up_to_seq/K_max no-numerico -> trusted:False (graceful), no excepcion.

## Como probarlo (lo critico)
- AC2: union (archivos+cola) re-materializa IDENTICO (canonical_hash) + mismo conjunto de eventos -> CERO perdida.
- AC4: evento manipulado EN UN ARCHIVO sigue cazado offline; archivo con hash malo -> fail-safe a full.
- AC3: camino vivo O(cola), byte-identico.

## No hacer
No borrar eventos (compactar MUEVE, no borra). No tocar config/genesis. No cambiar el modelo de confianza (fue B).
Fondo intocable.
