---
artifact_id: ANALISTA-TASK-0276-rejuicio-GO-verdict
reviewer: Analista
task_id: TASK-0276
type: review-verdict
verdict: OK-CLOSABLE
closable: true
created_at: 2026-07-22
local_time: "2026-07-22 17:28 (reloj del sistema, UTC+2, sin convertir)"
supersedes: ANALISTA-TASK-0276-evidencia-util-veredicto (CHANGE-REQUIRED, iter1)
anchors:
  review_commit: 8649524c15fd6abd307ec7f545bf5dc8dba37fa0
  fix_commit: 6eb57c987b3c18119a9d05256400cb7ebf096923
  protocol_head: b12fff4
  origin_main: b12fff4
relates_to: [TASK-0272, TASK-0276, DECISION-0103]
executive_summary: >
  GO / OK-CLOSABLE. La remediacion elimina la rama independiente `-or $hasCommit` de
  Get-OwnEvidence y ahora solo confirma un evento propio con intent_type en
  {task_status, task_upsert, decision}, applied true y keyid coherente. payload.commit
  quedo IRRELEVANTE. Verificado por comportamiento en clon limpio a 8649524 con mi
  propio probe (no los nombres de los tests): los cuatro vectores PASAN. V1 (E04) cierra
  para TODA la familia con etiqueta commit, no solo el sub-caso sin commit: claim
  acquire/release, mailbox_archive, protocol_prune, exception y project_narrative con
  commit -> ya NO confirman (los 2634 eventos claim-con-commit y 1078 mailbox_archive-con
  -commit del ledger dejan de quemar el mensaje). V2 la entrega real (task_status +-commit,
  task_upsert, decision) SIGUE confirmando, sin regresion de positivo. V3 reintroducir la
  rama commit en el fuente ps1 pone la suite en ROJO (exit 1) -- mutacion demostrada. V4 la
  firma sigue exigiendo applied true, ed25519, keyid coherente y sig no vacia. Gates
  protocolares verdes y drift 0. Cierra la cuarta de higiene.
---

# Veredicto Analista - TASK-0276 re-juicio (evidencia propia con trabajo util)

Voz: Analista (voz adversarial independiente). Firma al pie.
Hora local: 2026-07-22 17:28 (reloj del sistema, UTC+2, sin convertir).

Este veredicto SUPERSEDE mi NO-GO de la iteracion 1
(ANALISTA-TASK-0276-evidencia-util-veredicto, CHANGE-REQUIRED). El slip que bloquee
-- la rama `-or $hasCommit` que dejaba pasar el claim con etiqueta commit -- esta cerrado.

## Ancla canonica

- Commit re-juzgado: `8649524` (coord deliver commit-proxy remediation), que contiene el
  fix `6eb57c9` (reject commit-tagged pure claims) como ancestro.
- HEAD del protocolo / origin/main: `b12fff4` (coord que ruteo el re-juicio).
- Clon limpio a `D:\ccv0276b`, `git checkout 8649524`, gates y probe corridos AHI (no en
  arbol caliente). Mutacion de fuente en un segundo clon limpio `D:\ccv0276m`.

## El fix

`scripts/harness/peer_mailbox_cron.ps1::Get-OwnEvidence` -- se elimino la rama commit:

```
-        $hasCommit = -not [string]::IsNullOrWhiteSpace([string]$event.payload.commit)
-        if (-not ($hasUsefulIntent -or $hasCommit)) { continue }
+        if (-not $hasUsefulIntent) { continue }
```

`payload.commit` ya no participa. La confirmacion exige, en orden: actor == PeerId (propio),
applied -eq true, method ed25519, keyid empieza por `<peerid>:` (ordinal), sig no vacia, e
intent_type en {task_status, task_upsert, decision}.

## Reproduccion (exit codes en clon limpio a 8649524)

```
python scripts/validate_collaboration_state.py                 -> OK   exit 0
python scripts/scan_encoding.py                                -> OK   exit 0
python scripts/scan_domain_neutrality.py                       -> OK   exit 0
protocol_state_drift(.)                                        -> has_drift=False, paths=None
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> PASS exit 0
```

## Por que payload.commit no era evidencia (dato que cerro el slip)

Conteo por intent_type en el ledger del clon (events.jsonl, 5152 eventos):

```
intent_type          count   con_commit
claim                 2956      2634
mailbox_archive       1092      1078
task_status            761       652
task_upsert            248       226
decision                60        52
protocol_prune          21        21
exception                2         2
project_narrative       10         4
```

`--commit` se estampa en el payload de casi todo intent (runtime/submit_intent.py). Bajo el
codigo viejo, los 2634 claim-con-commit + 1078 mailbox_archive-con-commit + 21 prune + 2
exception confirmaban por la rama commit y quemaban el mensaje. Bajo el codigo nuevo solo
confirman task_status/task_upsert/decision (1069 eventos): la etiqueta commit ya no discrimina.

## Prueba por comportamiento (mi propio probe, no los nombres de los tests)

Extraje `Get-FilePrefixSha256` + `Get-OwnEvidence` del ps1 del clon limpio y las ejercite con
MIS payloads, imitando la FORMA de los eventos reales del ledger (17 casos, familia completa):

```
CASE                          GOT    EXPECTED
  pure_claim_acquire_commit    False   False    <- E04 CERRADO (claim acquire con commit)
  pure_claim_release_commit    False   False    <- E04 CERRADO (claim release con commit)
  pure_claim_no_commit         False   False
  mailbox_archive_commit       False   False    <- familia commit cerrada
  protocol_prune_commit        False   False
  exception_commit             False   False    <- sub-criterio, cerrado
  project_narrative_commit     False   False
  delivery_status_nocommit     True    True     <- positivo correcto
  delivery_status_commit       True    True     <- positivo correcto
  task_upsert_commit           True    True     <- positivo correcto
  decision_commit              True    True     <- positivo correcto
  applied_false_status         False   False    <- fencing (applied:false no cuenta)
  foreign_key_status           False   False    <- keyid ajeno no cuenta
  not_ed25519_status           False   False    <- metodo no ed25519 no cuenta
  empty_sig_status             False   False    <- firma vacia no cuenta
  foreign_actor_status         False   False    <- evento de otro actor no cuenta
  uppercase_keyid_status       False   False    <- residual conservador (retry, no burn)
SLIPS: NONE
```

## Vector 3 -- la mutacion demostrada (permanent_negative con dientes reales)

(a) A nivel funcion: reintroducir la rama commit en el body extraido hace que
`pure_claim_acquire_commit`, `pure_claim_release_commit`, `mailbox_archive_commit` y
`exception_commit` vuelvan a `True` (fuga reabierta), mientras la entrega real sigue en True.

(b) A nivel fuente + suite: en un segundo clon limpio (`D:\ccv0276m`, checkout 8649524)
reintroduje la rama commit en `peer_mailbox_cron.ps1` y corri la suite:

```
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  -> AssertionError: useful-own-evidence contract is incomplete   exit 1 (ROJO)
```

La suite `run_useful_own_evidence_cases` enrojece al reintroducir la rama commit: su
contrato exige `"if (-not $hasUsefulIntent) { continue }"` presente y `"$hasCommit"`
ausente, y su `commit_proxy_mutant` afirma que reintroducir la rama hace confirmar
`claim_with_commit`. El permanent_negative no es sello de goma.

## Tabla vector-por-vector

| # | Vector solicitado | Resultado | Evidencia |
|---|-------------------|-----------|-----------|
| V1 | claim puro acquire/release CON commit ya NO confirma (E04), mensaje se reintenta | **PASS** | pure_claim_acquire_commit y pure_claim_release_commit -> False; familia completa con commit (archive/prune/exception/narrative) -> False |
| V2 | entrega real (task_status +-commit) SIGUE confirmando | PASS | delivery_status_nocommit/commit, task_upsert_commit, decision_commit -> True; sin regresion |
| V3 | reintroducir la rama commit -> permanent_negative en ROJO | PASS | suite exit 1 en clon mutado; y flip funcional de las fugas a True |
| V4 | firma exige applied true y keyid coherente (fencing y keyid ajeno NO confirman) | PASS | applied_false/foreign_key/not_ed25519/empty_sig/foreign_actor -> False |

## Residuales declarados (no bloqueantes)

- Coherencia keyid via `StartsWith(peerId.ToLower()+":", Ordinal)`. Un keyid con mayuscula
  (`TestPeer:v1`) daria falso-negativo (retry, no burn) -- confirmado en probe
  (uppercase_keyid_status -> False). Conservador; los peers reales usan minuscula
  (`analista:v1`, `codex:v1`, `arquitecto:v1`), no muerde hoy.
- `$event.applied -ne $true` con `applied` string coercionaria en PowerShell; los eventos
  reales traen booleano. Teorico, no fuga.
- Los vectores de git-path (ls-files gateado por exit, APPLY_FAIL visible) del acceptance
  original ya estaban PASS en la iteracion 1 y esta remediacion no toca esa ruta del ps1;
  la suite completa (que ejercita esos mutantes) sigue en verde -> sin regresion.

## Recomendacion de cierre: OK-CLOSABLE (GO)

La pregunta de la instruccion -- "el claim puro con etiqueta commit ya no confirma, la
entrega real sigue confirmando, y reintroducir la rama commit pone el permanent_negative en
rojo?" -- responde SI en los tres. Recomiendo cerrar TASK-0276 (flip a done) y cerrar la
cuarta de higiene. No abro nuevos hallazgos.

-- Analista
