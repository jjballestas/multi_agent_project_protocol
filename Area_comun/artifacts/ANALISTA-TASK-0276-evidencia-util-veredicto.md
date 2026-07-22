---
artifact_id: ANALISTA-TASK-0276-evidencia-util-veredicto
reviewer: Analista
task_id: TASK-0276
type: review-verdict
verdict: CHANGE-REQUIRED
closable: false
created_at: 2026-07-22
local_time: "2026-07-22 16:36 (reloj del sistema, UTC+2, sin convertir)"
anchors:
  product_commit: 18ce287faa1f1df96b3a6eb6d2307565b092f6aa
  protocol_head: fd99125
  origin_main: fd99125
relates_to: [TASK-0272, TASK-0276, DECISION-0103]
executive_summary: >
  NO-GO / CHANGE-REQUIRED. El vector primario (V1: el exec de PURO claim ya NO confirma,
  E04) SLIPS por comportamiento. El fix cierra E04 solo para el sub-caso de un claim SIN
  payload.commit; pero los eventos de claim REALES llevan payload.commit (1894 de 2022
  eventos ed25519 de claim; incluidos 25+ acquire/release standalone etiquetados como
  claim/release), porque runtime/submit_intent.py estampa el --commit del llamante en el
  payload de TODO intent, tambien claim y exception. Un exec de puro claim acquire/release
  que pasa --commit (el patron real dominante de los peers) confirma via la rama
  `-or $hasCommit` y QUEMA el mensaje. Reproducido: pure_claim_acquire_label -> True,
  pure_claim_release_label -> True. V2, V3 y V4 PASAN; disciplina de mutantes de 0283 con
  dientes reales (5/5 enrojecen). Bloqueo por el vector central.
---

# Veredicto Analista - TASK-0276 (evidencia propia con trabajo util)

Voz: Analista (voz adversarial independiente). Firma al pie.
Hora local: 2026-07-22 16:36 (reloj del sistema, UTC+2, sin convertir).

## Ancla canonica

- Commit de producto bajo revision: `18ce287` (fix(TASK-0276): require useful signed own evidence).
- HEAD del protocolo / origin/main: `fd99125` (coord que me ruteo el juicio).
- Clon limpio a `/d/ccv0276`, `git checkout 18ce287`, gates corridos AHI (no en arbol caliente).

## Reproduccion (exit codes en clon limpio a 18ce287)

```
python scripts/validate_collaboration_state.py        -> OK  exit 0
python scripts/scan_encoding.py                        -> OK  exit 0
python scripts/scan_domain_neutrality.py               -> OK  exit 0
protocol_state_drift(.)                                -> has_drift=False (exit 0)
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> PASS exit 0
```

Los gates protocolares y la suite del reintento estan VERDES. El bloqueo NO es de gate:
es de COMPORTAMIENTO contra el vector primario.

## Prueba por comportamiento (mi propio probe, no los nombres de los tests)

Extraje `Get-OwnEvidence` del runner del clon limpio y lo ejercite con MIS payloads,
imitando la FORMA de los eventos reales del ledger (no solo el ejemplo del maker):

```
CASE                              CONFIRMS?
  pure_claim_no_commit             False   <- modelo del maker de E04 (cerrado)
  pure_claim_acquire_label         True    <- FUGA: claim acquire con etiqueta --commit
  pure_claim_release_label         True    <- FUGA: claim release con etiqueta --commit
  real_delivery_status             True    <- positivo correcto
  delivery_status_and_commit       True    <- positivo correcto
  applied_false_status             False   <- V3 ok (rechazo por fencing no cuenta)
  foreign_key_status               False   <- V3 ok (keyid ajeno no cuenta)
  exception_recorded               False   <- sub-criterio ok (exception sin commit)
  exception_with_commit            True    <- FUGA: misma rama commit reabre exception
  mailbox_archive / protocol_prune / project_narrative  False
```

`pure_claim_acquire_label` y `pure_claim_release_label` usan exactamente la forma de
eventos ed25519 REALES del ledger: p.ej. `analista:v1 / analista-task-0194-review-claim`
y `.../review-release`, `codex:v1 / Codex:TASK-0195:encoding-claim` y `.../encoding-release`.
Son claims puros (acquire/release) con applied:true, keyid coherente y payload.commit.
El harness los marca `confirmed` -> quema el mensaje. Eso ES E04, no cerrado.

## Causa raiz (falsable)

`runtime/submit_intent.py::event_payload_for` (lineas 645-646) estampa el `--commit`
del llamante en el payload de CUALQUIER intent, ANTES de ramificar por tipo:

```
if commit:
    payload["commit"] = commit
```

Por eso `payload.commit` NO es prueba de entrega: es la etiqueta libre que el peer pasa
en casi todo submit_intent. Conteo en el ledger del clon (18ce287):

- eventos ed25519 de claim: 2022; con payload.commit: **1894** (94%).
- de esos, 25+ son acquire/release standalone con etiqueta de claim/release (patron E04 puro).

La rama `-not ($hasUsefulIntent -or $hasCommit)` del fix trata cualquier claim con etiqueta
commit como trabajo util. Un "claim vacio que el ledger registra como un flip" -- lo que la
unidad madre dice que NO debe contar -- vuelve a contar por la rama del commit.

## Tabla vector-por-vector

| # | Vector solicitado | Resultado | Evidencia |
|---|-------------------|-----------|-----------|
| V1 | exec de PURO claim ya NO confirma (E04) -> unconfirmed/retry | **SLIPS (BLOQUEANTE)** | pure_claim_no_commit->False, pero pure_claim_acquire_label->True y pure_claim_release_label->True; 1894/2022 eventos claim reales llevan payload.commit; 25+ acquire/release standalone etiquetados. El mensaje se quema, no se reintenta. |
| V2 | entrega real (task_status [+commit]) SIGUE confirmando | PASS | real_delivery_status->True; delivery_status_and_commit->True |
| V3 | applied:true y coherencia keyid-actor (applied:false y keyid ajeno NO confirman) | PASS | applied_false_status->False; foreign_key_status->False |
| V4 | ls-files gateado por exit y APPLY_FAIL visible | PASS | fuente lineas 891-892 (untracked_snapshot_failed -> defer) y 683-684 (APPLY_FAIL log); mutantes M4/M5 enrojecen la suite |
| Sub | exception.recorded deja de confirmar | PARCIAL | exception_recorded->False (ok) PERO exception_with_commit->True (misma fuga de la rama commit) |

## Disciplina de mutantes (0283) - con dientes reales

Revertida cada correccion en el runner del clon y re-corrida la suite:

```
baseline (sin mutar)                    -> exit 0
M1 quito rama trabajo-util              -> exit 1 (enrojece)
M2 quito gate applied                   -> exit 1 (enrojece)
M3 quito gate coherencia keyid          -> exit 1 (enrojece)
M4 quito exit-gate de ls-files pre-exec -> exit 1 (enrojece)
M5 quito log APPLY_FAIL                  -> exit 1 (enrojece)
restaurado                              -> exit 0
```

5/5 negativos enrojecen al revertir su mutacion. La suite NO es un sello de goma para los
contratos que declara. El problema no es falta de dientes: es que la ESPECIFICACION del
positivo "commit" es incorrecta (afirma que claim+commit debe confirmar), y por eso el
filo E04 pasa inadvertido dentro de la propia suite.

## Residuales declarados

- La coherencia keyid usa `StartsWith(peerId.ToLower()+":", Ordinal)`. Un keyid real con
  mayuscula (`TestPeer:v1`) daria falso-negativo (retry, no burn) -- conservador, no fuga.
  Los peers reales usan minuscula (`analista:v1`, `codex:v1`, `arquitecto:v1`), asi que no
  muerde hoy; lo dejo anotado, no bloqueante.
- `$event.applied -ne $true` con un `applied` string ("true") pasaria el gate por coercion
  de PowerShell; los eventos reales traen booleano, asi que teorico, no bloqueante.

## Recomendacion de cierre: CHANGE-REQUIRED (NO-GO)

El vector primario y la pregunta de la instruccion ("el exec de PURO claim ya NO confirma,
reproduce E04 y exige unconfirmed/retry") FALLA por comportamiento en el patron real
dominante. Por la instruccion de "default a no-cerrable ante la duda" y por ser el filo
exacto que la unidad existe para cerrar, bloqueo el cierre.

## Bucle de fix esperado (max 2 iteraciones antes de escalar al humano)

1. Remediacion (elige el maker, no yo): (a) eliminar la rama independiente `-or $hasCommit`
   y exigir `$hasUsefulIntent` (applied + intent_type en {task_status,task_upsert,decision});
   la entrega real ya confirma via task_status sin commit (probado: real_delivery_status->True),
   asi que no vi regresion de positivo; o (b) gatear la rama commit para EXCLUIR intent_type
   claim y exception (contar commit solo junto a un intent de entrega).
2. Suite: cambiar la semantica del caso "commit" en run_useful_own_evidence_cases y anadir
   un PERMANENT_NEGATIVE: claim + applied + keyid coherente + etiqueta commit -> NO confirma.
3. Gates afectados: la suite del reintento (nuevo negativo + caso "commit"); validate,
   scan_encoding y scan_domain_neutrality no se ven afectados.
4. Re-juicio antes del GO de cierre: clon limpio + mi probe; exijo pure_claim_acquire_label
   y pure_claim_release_label -> False y real_delivery_status -> True. Si a la 2a iteracion
   sigue slipando, escalo al operador humano.

-- Analista
