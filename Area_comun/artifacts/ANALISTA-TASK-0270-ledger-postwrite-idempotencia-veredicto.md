# ANALISTA - Veredicto adversarial TASK-0270 (endurecimiento del event log)

- Firma: Analista (revisor adversarial independiente; veredicto gatea el cierre, DECISION-0056)
- Fecha/hora local: 2026-07-20 05:33 (UTC+2)
- Instruccion: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0270-ledger
- Alcance: SIN PRODUCTO (declarado por el Arquitecto en la instruccion); solo protocolo.

## Ancla canonica

- Protocolo: origin/main HEAD `b37e638` (contiene la implementacion `a989475`,
  fix(TASK-0270): verify durable intent writes; 3 archivos: runtime/submit_intent.py,
  examples/intent_tx_cases/run_intent_tx_cases.py, examples/intent_flow_cases/run_intent_flow_cases.py).
- Todo se ejecuto en CLON LIMPIO `D:/ccv/t0270` en checkout detached de `b37e638`
  (NO working tree; el arbol vivo esta 4-5 commits ahead con entregas de peers sin push).
- Preexistencia verificada contra segundo clon limpio `D:/ccv/t0270pre` en `a989475~1` (43fdce5).

## Reproduccion (exit codes reales, sin pipes)

| Comando (en clon limpio b37e638) | Exit | Resultado |
|---|---|---|
| python examples/intent_tx_cases/run_intent_tx_cases.py | 0 | 12/12 PASS (incluye los 2 casos nuevos) |
| python examples/intent_flow_cases/run_intent_flow_cases.py | 0 | 11/11 PASS |
| python examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py | 0 | PASS |
| python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py | 1 | 1 caso rojo: case_validator_gate_off_is_silent_and_gate_on_warns |
| (mismo runner de replay en a989475~1, clon pre) | 1 | MISMO caso rojo -> residual PREEXISTENTE, no introducido por 0270 |
| python scripts/validate_collaboration_state.py (CON secretos eventauth) | 0 | OK |
| python scripts/validate_collaboration_state.py (SIN secretos) | 0 | OK |
| python scripts/scan_encoding.py | 0 | OK |
| python scripts/scan_domain_neutrality.py | 1 | ROJO en HEAD; NO atribuible a 0270 (ver Anomalia) |
| protocol_state_drift(clon) | - | has_drift: False (drift 0) |
| validate_chain(clon) | - | valid: True, 4391 eventos verificados, head 6130df52 |
| sha256(protocol.config.json) | - | 2e35f26e... intacto; epoch 1.14.0; byte-identico al arbol vivo |

## Sondeo adversarial propio (11 payloads, driver D:/ccv/probe0270.py)

No confie en los tests del maker: extraje las funciones nuevas (`verify_appended_events`,
`idempotent_state_is_coherent`) y las ramas dedup/append de submit_intent/submit_intents,
y ejercite la familia completa de cada AC con payloads propios sobre fixtures limpios.
Verifique en codigo que `EventWriter.events()` re-lee DISCO en cada llamada (via
`all_events` -> lectura del JSONL), o sea el post-write NO es tautologico; P1/P2 lo
prueban por comportamiento (mi clobber edita el archivo despues del append y el guard lo caza).

| # | Vector (payload falsable) | Esperado por el AC | Observado | Veredicto |
|---|---|---|---|---|
| P1 | Intent SUELTO: clobber inyectado (evento propio borrado del log tras append, via monkeypatch del append) | exit != 0 nombrando el evento perdido | IntentApplyError "own event missing: seq=2,aggregate=TASK-9400,idempotency=probe:flip"; estado ROLLBACK completo | PASA |
| P2 | Transaccion --intents: clobber del 2do evento del lote | idem, para tx completas | IntentApplyError "own event missing: seq=3,..."; rollback completo | PASA |
| P3 | Retry byte-identico task_status con TASK_INDEX revertido a mano (evento presente, estado divergente) | re-aplica o falla; jamas skip mudo | deduped=True + idempotency_reconciled=True + estado REPARADO (done) + drift 0 | PASA |
| P4 | Retry byte-identico claim release con claim re-marcado active a mano | idem | reconciled=True + claim vuelve a released | PASA |
| P5 | Retry byte-identico mailbox_archive con mensaje re-creado en open/ y archived/ borrado | idem | reconciled=True + archivos re-archivados (open/ vacio, archived/ presente) | PASA |
| P6 | REPLAY DEL INCIDENTE 19-jul: tx aplicada, evento del flip BORRADO del log, estado revertido, retry byte-identico del lote | jamas exit 0 mudo | IntentApplyError distintivo "partial transaction idempotency state exists; refusing to continue" | PASA |
| P7 | Intent suelto: evento borrado del log, estado con el efecto aplicado, retry byte-identico | jamas exit 0 mudo | error ruidoso de validacion "stale task_status.from ... expected done, found in_progress" | PASA |
| P8 | Retry task_upsert con la tarea borrada del index (kind NO cubierto por el check de coherencia) | sin fuga silenciosa | estado REPARADO por re-materializacion + gate duro de drift; flag reconciled subreporta False (residual R1) | PASA con residual |
| P9 | Evento con payload FORJADO manteniendo el triple seq/aggregate/idempotency | (fuera del AC) | post-write lo acepta (compara identidad, no bytes); el tamper lo caza aguas abajo validate_chain (prev_hash encadena el contenido) | residual R2, contrived |
| P10 | Caso feliz por CLI: apply limpio + retry coherente | mismos exit codes y salidas | rc=0 apply sin campo nuevo; retry rc=0 deduped + reconciled=False (campo ADITIVO solo en dedup) | PASA |
| P11 | P6 por CLI real (subprocess) | exit != 0 | rc=1, stderr "ERROR: partial transaction idempotency state exists..." | PASA |

Resultado del sondeo: 11/11 sin escape nuevo. El camino exacto del incidente del 19-jul
(exit 0 mudo con evento perdido y retry skipeado) ya NO existe: cada variante que probe
termina en error distintivo con rollback o en reconciliacion real verificada por drift 0.

## Causa raiz (AC 3)

Verificado en codigo: `ledger_file_lock` (msvcrt/fcntl exclusivo) envuelve el ciclo
read-modify-write COMPLETO de ambos caminos (repair del tail, chequeo de dedup, append,
post-write, materializacion, side effects, snapshot y verificacion de drift). La ventana
del cruce queda cerrada a nivel mecanismo; el post-write queda como compensacion frente a
escritores fuera de banda. La suite de concurrencia es de DOS PROCESOS OS reales
(subprocess.Popen de la CLI cruzados), no un mock.

## Residuales declarados

- R1 (menor, reporte): `idempotent_state_is_coherent` solo cubre task_status/claim/
  mailbox_archive; task_upsert/decision devuelven True y el flag `idempotency_reconciled`
  subreporta. NO hay fuga: la re-materializacion + gate duro de drift reparan igual (P8).
- R2 (contrived): el post-write compara identidad (seq/aggregate/idempotency), no bytes;
  un swap de payload con identidad forjada pasa el guard local pero rompe la cadena de
  prev_hash en la siguiente validacion (P9). Fuera de la clase de fallo del incidente.
- R3 (declarado por el maker, honesto): kill abrupto post-append depende de la
  recuperacion por replay (caso vivo seq 5033-5034, recupero drift 0). Coherente con R1/R2.
- R4 (declarado por el maker, VERIFICADO preexistente): el caso rojo de
  runtime_protocol_replay_cases falla IDENTICO en a989475~1; no fue introducido por 0270.

## Anomalia DECISION-0018 (fuera de 0270, reportada aparte en el MSG)

`scan_domain_neutrality.py` esta ROJO en el HEAD canonico b37e638: todos los hallazgos
apuntan a `scripts/test_anthropic_checker_harness.py` (nombres de agentes de la instancia
en un script del core), archivo agregado por `6c8a0d8` (TASK-0271, ya ratificada). Evidencia
de biseccion: scan VERDE en a989475~1, ROJO desde 6c8a0d8. La remediacion pertenece al
owner de 0271; no gatea el cierre de 0270.

## RECOMENDACION DE CIERRE

OK -> CERRABLE (GO) para TASK-0270. Los cinco vectores del acceptance aguantan el sondeo
adversarial completo; el unico gate rojo del cuadro (neutralidad) es una regresion ajena,
atribuida con biseccion y notificada como anomalia.

Nota operativa: este veredicto es el primer turno end-to-end del harness migrado del
Analista (provider Anthropic); el sondeo de tamper del ledger corrio completo y sin kills
del clasificador (evidencia viva de TASK-0271).

---

task_id: TASK-0270
status: in_review
executive_summary: Veredicto adversarial GO: post-write y coherencia idempotencia-vs-estado aguantan 11/11 payloads propios en clon limpio de b37e638, incluido el replay del incidente 19-jul (error distintivo, jamas skip mudo); residuales R1-R4 declarados y acotados; neutralidad ROJA en HEAD atribuida por biseccion a TASK-0271, no a 0270.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0270-ledger-postwrite-idempotencia-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0270-veredicto-GO.md
gates: intent_tx 12/12 exit 0; intent_flow 11/11 exit 0; concurrency exit 0; replay exit 1 (caso preexistente verificado en a989475~1); validate con y sin secretos exit 0; drift 0; chain valida 4391 eventos; config sha256 2e35f26e intacto epoch 1.14.0; scan_encoding exit 0; scan_domain_neutrality exit 1 en HEAD (regresion de 6c8a0d8/TASK-0271, no de 0270)
next_recommended: Arquitecto ratifica cierre de TASK-0270 y rutea la remediacion de neutralidad de scripts/test_anthropic_checker_harness.py al owner de TASK-0271.
risks: R1 flag reconciled subreporta en task_upsert/decision (sin fuga, reparacion verificada); R2 identidad-no-bytes en post-write (cazado aguas abajo por prev_hash); R3 kill post-append depende de replay (declarado); gate de neutralidad del hub ROJO hasta remediar 0271.
