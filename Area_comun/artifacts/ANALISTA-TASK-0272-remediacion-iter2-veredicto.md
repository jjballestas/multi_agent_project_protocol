# ANALISTA - TASK-0272 remediacion iteracion 2 (ultima del tope) - re-juicio adversarial

Firma: Analista (voz adversarial independiente). Fecha local: 2026-07-20 18:20.
Instruccion canonica: `Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0272-remediacion-iter2.md`.
Alcance: SIN PRODUCTO (solo este hub), por instruccion canonica.

## Veredicto de cabecera

**OK / CERRABLE con residuales declarados.** El bloqueante de la iteracion 1
(F-0272R1-01, atribucion por autor git uniforme) esta CERRADO por comportamiento en
condiciones de despliegue reales: en sandbox con AUTOR UNIFORME (`Analista
<analista@local>`, el modelo real de este hub), un commit concurrente sin evento propio
firmado ya NO confirma (unconfirmed -> retry acotado -> RETRY_EXHAUSTED signal=watchdog,
mensaje NO quemado), y un evento propio firmado ed25519 en la ventana de seq SI confirma.
El token quedo anclado a la ULTIMA linea no vacia (los ataques A1/A2 de iter1 mueren), y
los caminos de fallo de snapshot y rollback son fail-closed (snapshot rojo -> el agente NO
arranca; HEAD movido o reset fallido -> defer, nunca restauracion a medias). Los
hardening F-02 y F-04 pedidos en iter1 estan implementados y probados.

HALLE un escape nuevo, acotado y lo declaro con repro determinista: un evento propio de
PURO claim (acquire/release) o exception.recorded en la ventana cuenta como evidencia,
asi que un exec que reclamo y aborto sin entregar nada, con token ausente y exit 0,
sigue quemando el mensaje (E04). Lo grado WARNING-real ACOTADO y NO BLOQUEANTE por las
razones dimensionadas en F-0272R2-01: es subconjunto estricto de la clase residual YA
DECIDIDA {token ausente + exit 0}, exige que el propio exec incumpla a la vez el
contrato del token y la disciplina de entrega/blocked, su frecuencia observada en campo
es cero (las 3 recurrencias reales fueron abortos PRE-claim, que esta iteracion cierra),
y a diferencia de E1 de iter1 deja SIEMPRE traza forense firmada y atribuible en el
ledger (el par de claims sin entrega entre medias). Hardening barato recomendado, no
requerido para cerrar.

## Ancla canonica y reproduccion

- Implementacion: `02cee08`; entrega `2d1f549` + memoria `bab3eba`. Clon limpio
  `D:/ccv0272r2` checkout `bab3eba`; suites y gates corridos AHI. Invariancia:
  diff `02cee08..HEAD` sobre `scripts/harness/`, `examples/mailbox_retry_cases/` y los
  tests de harness = VACIO (verificado dos veces; el HEAD vivo avanzo durante la pasada
  con coordinacion del Arquitecto: `6ebf591` aterrizo la instruccion + la cola de eventos
  5333-5342 pendiente, `299c3da` reporte al Operador; ninguno toca rutas juzgadas).
- Suites del maker en el clon (exit codes): `run_mailbox_retry_cases.py` EXIT 0;
  `test_anthropic_checker_harness.py` EXIT 0; `test_exec_lease_harness.py` EXIT 0.
- Bateria propia: (a) UNIT con `Get-OwnEvidence`, `Get-LedgerSequence` y
  `Get-ExecOutcomeClass` extraidas VERBATIM del runner del clon (regex, no copia a mano):
  17 casos de evidencia (V01-V17) + 22 de clasificador (T01-T22) + 2 one-off (V18-V19),
  41/41 conforme a lo esperado, FAILS=0; (b) E2E con el runner REAL del clon en 11
  sandboxes git efimeros (`D:/sb0272r2/*`), AUTOR UNIFORME `Analista <analista@local>` en
  TODOS (fixture y agente), agente falso por contador, `-IntervalSeconds 1
  -RetryBackoffSeconds 0 -MaxTransientRetries 3`, 23/23 asserts PASA. Los sandboxes E05,
  E06 y E07 fuerzan fallos de git con un shim de PATH (exit 7/9 selectivo por subcomando)
  para probar los caminos de fallo por comportamiento, no por lectura.

## Tabla vector por vector (los 4 frentes de la instruccion)

| # | Vector pedido | Resultado | Evidencia falsable |
|---|---------------|-----------|--------------------|
| 1a | Ventana de seq: otro actor escribe en medio | **PASA** | E03/V04: evento ajeno (actor Codex, ed25519 valido) en la ventana -> unconfirmed, retry acotado, RETRY_EXHAUSTED, NO seen. V14: ajeno intercalado no tapa al propio. |
| 1b | Seq no avanza / evento propio de ciclo anterior | **PASA** | V02/V03: seq igual o menor a la marca pre-exec NUNCA confirma. Todos los sandboxes E2E llevan un evento propio VIEJO (seq 2) sembrado y jamas confirma (E01/E03/E10). Sin evento nuevo -> unconfirmed -> retry acotado (fail-closed). |
| 1c | Actor correcto con actor_auth vacio o degradado | **PASA** | V07/V08/V15/V16: sig vacio, keyid vacio, sig whitespace, actor_auth ausente -> False. V06: `not_enforced_phase2` -> False (en instancias sin event_auth la capa queda NUNCA-CONFIRMA, la degradacion prometida). V05/V09: case-mismatch de actor o metodo -> False. |
| 1d | Colar un evento con actor correcto | **SLIPS acotado** | E04/V11/V19: evento propio de PURO claim o exception.recorded cuenta como evidencia -> burn sin trabajo util (F-0272R2-01, no bloqueante, ver abajo). V10/V18: applied:false (rechazo por fencing) y keyid AJENO tambien pasan el chequeo de presencia (F-0272R2-02, teorico: sin camino accidental en el flujo mailbox; el validador #4 lo cazaria post-hoc). |
| 2a | Entrega que termina con texto tras el token | **PASA** | T04/E09a: token en penultima linea + cola de texto -> token IGNORADO, cae a capas inferiores, NO consume (unconfirmed -> retry senalado). E09b: mismo transcript con token terminal -> definitive, consumido 1x. T08: token duplicado -> gana el ultimo. |
| 2b | Transcript vacio / truncado | **PASA con nota** | T06/T07/E10: vacio o solo whitespace -> unconfirmed -> retry acotado con senal. T11: token truncado (`OUTCOME: confir`) -> no matchea. T20: vacio + evidencia propia -> confirmed (cae en la clase F-0272R2-01). |
| 2c | Imitaciones del token | **PASA** | T09/T12/T13/T14/T21: espacio colgante, cita `> `, fence como ultima linea, minusculas, doble espacio -> todos caen a fallback. Los ataques A1/A2 de iter1 (token citado en medio del transcript) ya no matchean: solo la ULTIMA linea no vacia cuenta. |
| 3a | Snapshot falla antes del exec | **PASA** | E05/E06 (shim git exit 7): index o worktree snapshot rojo -> `RETRY_DEFER reason=*_snapshot_failed`, el agente NO arranca (contador 0), lock liberado, mensaje intacto y reintentable. Fail-closed como pedia F-04a. |
| 3b | HEAD movido entre los dos rev-parse | **PASA** | E01: commit del exec mueve HEAD -> `ROLLBACK_DEFER reason=head_changed`, commit preservado. El re-chequeo inmediatamente antes del reset (linea 481-482) cierra la ventana grande de iter1; queda TOCTOU de ms (residual declarado, abajo). |
| 3c | Reset falla a medias | **PASA** | E07 (shim exit 9 en `reset --hard`): `ROLLBACK_DEFER reason=reset_failed`, SIN restauracion parcial (el toque del exec queda integro y visible), retry sigue acotado y senalado. |
| 4 | Regresiones de lo cerrado en iter1 | **PASA** | E08: pre-sucios worktree+staged restaurados BYTE-IGUAL, porcelain identico al pre-exec, residuo staged del exec eliminado, rename revertido. E01: defer con HEAD movido. E02: entrega real con evento propio -> confirmed, seen, retry limpio, 1 exec. T15-T19: frontera token>exit>evidencia>regex intacta (T15: token gana a exit!=0; T17: evidencia gana al eco NO-GO; T18/T19: regex fallback sin cambios). |

## Hallazgos

- **F-0272R2-01 (WARNING-real ACOTADO, NO bloqueante, residual declarado): evidencia
  propia sin trabajo util.** `Get-OwnEvidence` acepta CUALQUIER evento propio firmado en
  la ventana sin mirar tipo ni payload. Repro E2E determinista (E04): exec que solo
  appendea un evento propio de claim release, narra obstaculo transitorio ("pre-gate
  rojo, claim ajeno activo"), sin token, exit 0 -> `outcome=confirmed`, seen QUEMADO,
  retry limpiado, y la evidencia PISA a la narracion transitoria (la capa 3 decide antes
  del regex). Variante V19: exception.recorded. Por que NO bloquea (dimensionado): (1)
  es subconjunto estricto del residual estructural YA DECIDIDO {token ausente + exit 0};
  (2) exige que el PROPIO exec rompa a la vez el contrato del token (inyectado en cada
  prompt) y la disciplina de entrega/blocked-con-pregunta -- las 3 recurrencias reales de
  la tanda fueron abortos PRE-claim sin evento propio, que esta iteracion deja en
  unconfirmed (E01); (3) el falso confirmed deja SIEMPRE traza firmada atribuible (par
  acquire/release sin entrega en medio), visible para la revision de >15 min del
  coordinador -- el E1 de iter1 no dejaba NADA propio; (4) la letra del AC admite "flip
  de estado" como trabajo verificable y un claim ES un flip de estado en el ledger; el
  refinamiento semantico ("trabajo util para el mensaje") no tiene proxy mecanico
  perfecto. Hardening barato recomendado (follow-up, mismo carril que TASK-0274/0275):
  contar como evidencia solo eventos `applied:true` cuyo `payload.intent_type` este en
  {task_status, task_upsert, decision} o traiga `payload.commit`; el patron real de
  entrega de los peers (transaccion con task_status + commit) seguiria confirmando y el
  par de puro claim dejaria de hacerlo.
- **F-0272R2-02 (WARNING-theoretical): el chequeo de firma es de PRESENCIA, no
  criptografico.** V10: evento `applied:false` (rechazo por stale fencing, es decir un
  intento RECHAZADO sin mutacion de estado) confirma; V18: keyid AJENO (`codex:v1` con
  actor Analista) confirma; la propia suite del maker usa `sig:"fixture-signature"`. Sin
  camino ACCIDENTAL en el flujo mailbox de este hub: los agentes van por
  `submit_intent`, que firma con la clave registrada del actor y solo emite
  `intent.applied`/`exception.recorded` con `applied:true`; el camino de fencing vive en
  `runtime/apply.py` (motor de turnos), no en el cron. Una falsificacion deliberada la
  cazaria el validador #4 en el siguiente gate, pero DESPUES del burn. Hardening barato:
  exigir `applied == true` (una linea) y, opcional, prefijo de keyid coherente con el
  actor.
- **F-0272R2-03 (WARNING-theoretical): la lista de untracked pre-exec no verifica exit
  code.** `git ls-files --others --exclude-standard -z` (linea 626) queda fuera del
  fail-closed nuevo: si fallara (lista vacia) y la enumeracion post-exec funcionara, el
  rollback trataria TODOS los untracked pre-existentes como creados por el exec y los
  BORRARIA. Sin disparador observado (fallo de solo-lectura de git, raro); asimetria
  clara con los dos parches ya gateados. Fix barato: gatear su $LASTEXITCODE igual que
  los snapshots; alimenta la cuarentena de TASK-0275.
- **F-0272R2-04 (SUGGESTION): re-apply de parches sin verificar exit.** Lineas 487-488:
  si `git apply` fallara tras un reset exitoso, el pre-sucio del peer se perderia en
  silencio (ventana estrecha: parches tomados contra el mismo HEAD al que se resetea).
  Log `APPLY_FAIL` bastaria para hacerlo visible.

## Residuales declarados (sin cambio de diseno)

- R-A: clase {token ausente + exit 0} cae a evidencia/regex viejo -- es la frontera
  DECIDIDA (T17/T18/T19 la confirman sin cambios; X1 eco NO-GO sigue quemando via regex
  cuando no hay token NI evidencia). F-0272R2-01 es el filo nuevo de esta misma clase.
- R-B: token terminal gana a exit != 0 (T15): kill tras emitir `OUTCOME: confirmed` ->
  confirmed (marginal, sin cambio desde iter1).
- R-C: stderr se concatena al transcript: una CLI que emita ruido de stderr al final
  pierde el token de stdout de forma sistematica (T04 aplica). Degradacion, no burn: las
  entregas reales confirman por evidencia; las negativas caen a retry acotado + senal.
  Vigilar en el USO VIVO con CLI real (la tasa de omision del token sigue sin medir,
  R-D de iter1).
- R-E: TOCTOU de milisegundos entre el re-chequeo de HEAD y el `reset --hard`: un commit
  de peer en ese gap quedaria huerfano del branch (recuperable por reflog); el chequeo
  post-reset no puede distinguirlo porque el reset fuerza HEAD de vuelta. Estrechado en
  ordenes de magnitud vs iter1; irreducible sin lock de repo.
- R-F: escrituras de peer DURANTE la ventana del exec siguen destruyendose en el
  rollback (untracked borrado, tracked barrido) -- residual explicito de la unidad,
  cuarentena = TASK-0275 (fuera de este juicio por instruccion).
- R-G: regenesis o poda que renumere seq DURANTE un exec deja la evidencia ciega esa
  ventana (falso negativo -> retry acotado, fail-closed; no burn).
- R-H: `Get-LedgerSequence` + `Get-OwnEvidence` parsean events.jsonl entero (~5.3k
  lineas) linea a linea en PS 5.1 dos veces por exec: latencia de segundos, sin efecto
  funcional; crecera con el ledger.
- R-I: el gate CLI real de drift sigue siendo TASK-0274 (el handoff de iter2 ya cita
  `protocol_state_drift()`, la funcion real -- corregido desde mi F-0272R1-05).

## Respuesta directa a la pregunta del REVIEW

(1) "Queda algun camino por el que un exec sin trabajo util pueda seguir marcando el
mensaje como visto?" SI, uno, acotado y con repro: evento propio firmado de puro
claim/exception en la ventana + token ausente + exit 0 (E04; variantes teoricas V10/V18
sin camino accidental). Declarado F-0272R2-01, NO bloqueante por las 4 razones
dimensionadas arriba; hardening barato recomendado. Los caminos de iter0/iter1 (commit
de peer, autor uniforme, eco de prosa con evidencia ajena) estan CERRADOS por
comportamiento (E01/E03 + V04-V09). (2) "Puede el rollback destruir estado que no creo
el propio exec?" En los caminos probados NO: pre-sucios byte-igual (E08), HEAD movido o
reset fallido -> defer sin restauracion parcial (E01/E07), snapshot rojo -> ni siquiera
arranca el exec (E05/E06). Quedan los residuales ya conocidos: escrituras de peer
DURANTE la ventana (R-F -> TASK-0275), la TOCTOU de ms (R-E) y el teorico
ls-files-sin-exit (F-0272R2-03).

## Recomendacion de cierre

**OK -> CERRABLE.** El fix-loop de 2 iteraciones queda CONSUMIDO con el bloqueante
cerrado y sin fallo nuevo bloqueante; no hay que escalar al Operador. Recomendado para
el carril de follow-ups (no condicion de cierre): (a) filtro de evidencia por
intent_type/applied (F-01/F-02, ~5 lineas + 1 negativo permanente de puro-claim); (b)
exit-gate del ls-files pre-exec (F-03, 1 linea, casa con TASK-0275); (c) log APPLY_FAIL
(F-04). TASK-0274 y TASK-0275 siguen siendo la via para el gate de drift real y la
cuarentena de untracked.

## Gates del protocolo

- `python scripts/validate_collaboration_state.py`: clon `bab3eba` (sin secretos) EXIT 0;
  vivo (con secretos) EXIT 0 tras `6ebf591`. Nota de ventana: al arrancar mi pasada el
  vivo estaba EXIT 1 por la cola de eventos 5333-5337 de la entrega de Codex sin
  commitear (snapshot atras); el Arquitecto la aterrizo en `6ebf591` y el vivo quedo
  verde -- rojo transitorio de entrega in-flight, no anomalia nueva.
- `python scripts/scan_encoding.py` EXIT 0 (clon y vivo, incluye este artefacto y el MSG).
- `python scripts/scan_domain_neutrality.py` EXIT 0 (clon y vivo).
- Drift real via `runtime.protocol_replay.protocol_state_drift()`: clon False
  `up_to_seq=5337`; vivo False `up_to_seq=5344`.
- `protocol.config.json` byte-identico vivo/clon sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; epoch 1.14.0
  intacta; fondo intocable sin tocar.
- Suites maker (clon): retry E2E EXIT 0; anthropic harness EXIT 0; exec-lease EXIT 0.
- Producto: NOT_RUN por instruccion canonica (SIN PRODUCTO EN ALCANCE).

---

task_id: TASK-0272
status: in_review
executive_summary: OK / CERRABLE con residuales declarados. El bloqueante de iter1 esta cerrado por comportamiento en sandbox de AUTOR UNIFORME (commit concurrente sin evento propio firmado -> unconfirmed -> retry acotado -> RETRY_EXHAUSTED con senal; evento propio ed25519 en la ventana -> confirmed); el token es terminal-only (cola de texto lo invalida, imitaciones caen a fallback); snapshots fail-closed (rojo -> el agente no arranca) y rollback con re-chequeo de HEAD (movido o reset fallido -> defer sin restauracion parcial; pre-sucios byte-igual). Bateria propia 41 unit + 23 asserts E2E en 11 sandboxes, todo conforme. Hallazgo nuevo acotado F-0272R2-01 (WARNING-real NO bloqueante, residual declarado): un evento propio de PURO claim o exception.recorded en la ventana + token ausente + exit 0 sigue quemando el mensaje (E04); subconjunto de la clase residual decidida, requiere doble incumplimiento del propio exec, deja traza firmada atribuible y tiene hardening barato (filtrar por intent_type/applied). Teoricos: applied:false y keyid ajeno pasan el chequeo de presencia (V10/V18); ls-files pre-exec sin exit-gate (F-03).
artifacts: Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter2-veredicto.md
gates: clon bab3eba validate/encoding/domain EXIT 0 + drift False seq 5337; vivo validate/encoding/domain EXIT 0 + drift False seq 5344; config #4 byte-identica 2E35F26E...354; suites maker retry/anthropic/lease EXIT 0; bateria propia unit 41/41 + E2E 23/23
next_recommended: Arquitecto ratifica cierre de TASK-0272 (review_approved -> done via runtime) y registra los follow-ups baratos (filtro de evidencia por intent_type/applied + exit-gate de ls-files + log APPLY_FAIL) en el carril de TASK-0274/0275; sin escalada al Operador.
risks: La clase {token ausente + exit 0} conserva los filos declarados: puro-claim/exception propio quema (E04, con traza firmada), eco NO-GO sin evidencia quema via regex (X1), CLI con stderr ruidoso pierde el token sistematicamente (degrada a retry senalado); tasa real de omision del token por CLI viva sigue sin medir; TOCTOU de ms en el reset y escrituras de peer durante la ventana (TASK-0275) persisten.
