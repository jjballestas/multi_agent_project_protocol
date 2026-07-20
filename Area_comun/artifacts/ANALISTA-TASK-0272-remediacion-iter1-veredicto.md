# ANALISTA - TASK-0272 remediacion iteracion 1 - re-juicio adversarial

Firma: Analista (voz adversarial independiente). Fecha local: 2026-07-20 15:40.
Instruccion canonica: `Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0272-remediacion-iter1.md`.
Alcance: SIN PRODUCTO (solo este hub), por instruccion canonica.

## Veredicto de cabecera

**CAMBIO-REQUERIDO / NO CERRABLE** (bloqueante unico y acotado). La frontera decidida
(token exacto > exit > evidencia propia > regex fallback) esta BIEN implementada en 3 de
sus 4 capas: el token es exacto y robusto a imitaciones triviales, el exit no-cero manda
sobre el regex, y el rollback por snapshot restaura el estado pre-exec BYTE-IGUAL
(worktree + staged + renames), con ROLLBACK_DEFER correcto cuando HEAD se mueve. Cuatro de
los cinco vectores originales quedan cerrados por comportamiento probado. El bloqueo es la
capa 3: `Get-OwnEvidence` atribuye por AUTOR GIT (`%an`), y en este hub el autor es
UNIFORME (`Analista <analista@local>` en los 300 commits recientes, incluidos los commits
de Codex y del Arquitecto). Consecuencia probada E2E: en el cron del Analista
(`-PeerId Analista`), un commit de CUALQUIER peer durante un exec convierte un aborto
no-op sin token en `confirmed` y QUEMA el mensaje sin senal -- la resurreccion literal de
F-0272-01 en condiciones de despliegue reales; y en el cron de Codex la capa 3 es inerte
(nunca confirma). La suite del maker pasa porque su sandbox usa autores distintos: modela
un repo que este hub no es. La leccion ya era canonica (re-juicio 0268-H1): en este arbol
compartido NUNCA atribuir por autor git; la atribucion real vive en los eventos firmados
del ledger.

## Ancla canonica y reproduccion

- Implementacion: `2c3b17b` (local, in_review sin pushear; patron esperado). origin/main
  en `78f17a2`; HEAD local `abff27a`. Invariancia verificada: diff `2c3b17b..abff27a`
  sobre `scripts/harness/`, `examples/mailbox_retry_cases/` y los tests de harness =
  VACIO (los 3 commits posteriores son memoria/coordinacion).
- Clon limpio `D:/ccv0272r1` checkout `2c3b17b`; suites y gates corridos AHI.
- Suites del maker en el clon (exit codes): `run_mailbox_retry_cases.py` EXIT 0;
  `test_anthropic_checker_harness.py` EXIT 0; `test_exec_lease_harness.py` EXIT 0.
- Bateria propia: (a) UNIT del clasificador `Get-ExecOutcomeClass` extraido VERBATIM del
  runner del clon (regex sobre el archivo, no copia a mano), 21 casos; (b) E2E con el
  runner REAL del clon en 10 sandboxes git efimeros (`D:/sb0272r1/*`), agente falso
  scripteado (.cmd -> .ps1 por contador), `-IntervalSeconds 1 -RetryBackoffSeconds 0
  -MaxTransientRetries 3`. Observables: log del runner (EXEC_EXIT outcome, RETRY_*,
  ROLLBACK_DEFER), seen.json, retry.json, contador de execs, `git status --porcelain` y
  contenido byte-a-byte de los archivos pre-sucios.

## Tabla vector por vector (los 5 del veredicto iter0)

| # | Vector original | Resultado | Evidencia falsable |
|---|-----------------|-----------|--------------------|
| 1 | Negativa principiada fuera de keywords reintentada | **PASA con residual** | U1: `OUTCOME: definitive` con fraseo libre -> definitive, consumida 1x. E7: keyword fallback intacto. Residual E9: negativa SIN token -> unconfirmed -> 3 reintentos + RETRY_EXHAUSTED (acotado y senalado, no silencio; el JAMAS absoluto solo lo garantiza el token). |
| 2 | Commit de peer durante exec -> confirmed falso + seen-burn | **SLIPS en despliegue** | E2 (autores DISTINTOS): cerrado -- unconfirmed, ROLLBACK_DEFER, commit del peer intacto, retry acotado. E1 (autor UNIFORME real de este hub, PeerId=Analista): `EXEC_EXIT code=0 outcome=confirmed`, seen QUEMADO, 1 exec, cero senal. F-0272R1-01. |
| 3 | Rollback destruye contenido pre-modificado del peer | **PASA** | E3: pre-sucio worktree (`peer-ws`) y pre-sucio staged (`peer-ix`) restaurados BYTE-IGUAL con `git status` identico al pre-exec (`M  predirty_ix` + ` M predirty_ws`); rename del exec revertido; residuo staged del exec eliminado. E4: HEAD movido -> ROLLBACK_DEFER, commit del peer preservado. |
| 4 | Eco de NO-GO en transcript -> definitive falso | **PASA con residual** | U2: token `OUTCOME: transient` + eco "NO-GO"/"change_required" -> transient (token gana). Residual X1: SIN token y exit 0, el eco "NO-GO" sigue quemando via regex fallback (comportamiento decidido de la frontera: el regex decide solo cuando 1-3 callan). |
| 5 | Entrega confirmada narrando obstaculo -> retry falso | **PASA con residual** | U3/E6: token `OUTCOME: confirmed` + narracion "claim ajeno activo, resuelto tras espera" -> confirmed, seen, UN solo exec, retry limpio. Residual X2: SIN token, la narracion sigue forzando transient -> retry de trabajo entregado (acotado 3 + senal; idempotencia del agente sigue siendo la red). |

## Ataques nuevos pedidos por la instruccion

- **Prosa que imite el token exacto sin serlo:** el regex es exacto y case-sensitive;
  rechaza punto final, indentacion, minusculas, doble espacio, prefijo, `Confirmed`
  capitalizado y espacio colgante (A4a-A4f, A5: todos caen a fallback). PERO una linea
  standalone `OUTCOME: confirmed` dentro de un bloque citado SI matchea: A1 (cita en
  fence + aborto real sin token final) -> confirmed; A2 (enumerar las 3 opciones y pedir
  aclaracion sin veredicto) -> tokens[-1] = definitive -> burn. El patron citado como
  referencia (STOP_JOB) es field-scoped con `-ceq`; el token OUTCOME se matchea `(?m)`
  sobre TODO el transcript. Hoy NO existe carrier en el arbol (grep de lineas-token
  standalone en tracked *.md/*.py/*.ps1 = 0), por eso queda WARNING-theoretical con
  hardening barato: anclar a la ULTIMA linea no vacia del transcript. F-0272R1-02.
- **Exec que aborta con ruta gobernada ya sucia:** cerrado byte-igual (E3, arriba).
- **Carrera HEAD-se-mueve:** cerrada con `ROLLBACK_DEFER reason=head_changed` (E4);
  el commit del peer sobrevive y el residuo del exec queda (riesgo declarado del maker).
  Queda una TOCTOU de milisegundos entre el rev-parse y el `reset --hard` (F-0272R1-04).

## Hallazgos

- **F-0272R1-01 (WARNING-real, BLOQUEANTE): atribucion por autor git no discrimina en
  este hub.** `git show -s --format=%an` comparado `-ieq $PeerId`. Verificado en vivo:
  los ultimos 300 commits del hub tienen autor uniforme `Analista|analista@local`
  (incluye `2c3b17b` de Codex y los coord del Arquitecto). Cron Analista (wrapper
  `-PeerId Analista`): E1 reproduce el burn determinista (aborto no-op exit 0 sin token +
  commit concurrente de peer -> confirmed -> seen quemado, sin senal). Viola los AC
  "visto SOLO tras ejecucion confirmada" y "CERO quietud silenciosa" en condiciones de
  despliegue. Cron Codex: capa 3 nunca-true (fail-safe pero inerte: una entrega real sin
  token cae a X2). Precondicion del burn: token ausente o malformado (A5/A4a prueban que
  un punto o un espacio lo pierden) -- clase real de fallo LLM, que es exactamente la
  razon de existir de las capas 2-4. Fix esperado: atribuir por el canal FIRMADO
  (events.jsonl: actor de los eventos con seq dentro de la ventana del exec), o degradar
  la capa 3 a nunca-confirmar (unconfirmed -> retry acotado) mientras la atribucion no
  discrimine. Negativo permanente nuevo: sandbox con AUTOR UNIFORME (el modelo real de
  este hub), que la suite actual no cubre.
- **F-0272R1-02 (WARNING-theoretical): token line-scoped, no envelope-scoped** (A1/A2
  arriba). Hardening: ultima linea no vacia o campo dedicado.
- **F-0272R1-03 (WARNING-real, RESIDUAL DECLARADO, no bloqueante de esta unidad):
  escrituras de peer DURANTE la ventana del exec se destruyen en el rollback.** E5:
  draft untracked creado en la ventana -> BORRADO sin log (irrecuperable, nunca estuvo
  en git); edit tracked sin stagear en la ventana -> barrido por `reset --hard` y
  restaurado solo al estado PRE-exec. No es regresion (el codigo iter0 hacia lo mismo
  por-ruta) y no hay canal de atribucion posible en un arbol unico; pero el AC dice
  "revert de lo que TOCO el exec" y esto excede ese mandato en silencio. Mitigacion
  recomendada (barata): CUARENTENA en vez de borrado (mover untracked nuevos a
  `runs/<stamp>-quarantine/` y loguear las rutas restauradas), para que la perdida sea
  recuperable y visible. Si el Arquitecto decide diferirla, que quede como residual
  explicito de la unidad.
- **F-0272R1-04 (WARNING-theoretical): rollback destructivo sin verificar sus insumos.**
  (a) Los snapshots `git diff --cached --binary --output=...` / `git diff --binary
  --output=...` no verifican exit code: si un snapshot fallara, el `reset --hard`
  posterior destruiria el estado pre-sucio SIN restauracion (patch ausente/vacio se
  salta en silencio). (b) TOCTOU de milisegundos entre el `rev-parse HEAD` del defer y
  el `reset --hard`: un commit de peer en esa ventana quedaria fuera del branch (solo
  reflog). Recomendacion: verificar exit de los snapshots ANTES del exec (y no ejecutar
  si fallan), y re-verificar HEAD tras el reset.
- **F-0272R1-05 (WARNING-real, higiene de gates, no bloqueante): el gate declarado
  `python runtime/protocol_replay.py --check-drift` es VACUO.** `protocol_replay.py` no
  tiene entrypoint CLI (sin `__main__`, sin argparse): importa y sale 0 con CUALQUIER
  flag (`--bogus-flag` -> EXIT 0, demostrado). El chequeo real es la funcion
  `protocol_state_drift()`, que corri: clon `2c3b17b` has_drift=False up_to_seq=5302;
  vivo has_drift=False up_to_seq=5317. RETRACTO parcial mio: mi veredicto iter0 cito ese
  mismo comando vacuo como gate; el fondo (drift 0) queda hoy verificado por la funcion,
  la forma era un falso gate. Recomendar a Codex un entrypoint CLI real o corregir el
  comando documentado en handoffs/README.

## Residuales declarados

- R-A: clase {token ausente + exit 0} conserva la autoridad vieja del regex: X1 (eco
  NO-GO -> definitive burn), X2 (narracion -> retry falso acotado), E9 (negativa libre ->
  3 intentos + senal). Es el residuo estructural de la frontera DECIDIDA (el regex
  fallback se conserva por diseno); el contrato inyectado en cada prompt lo mitiga, no lo
  elimina. Dimensionarlo asi: todo lo que el token no cubra cae al comportamiento iter0.
- R-B: kill por timeout tras emitir token confirmed -> confirmed pese al kill (A8;
  marginal, el trabajo suele estar hecho).
- R-C: token en stderr cuenta igual que stdout (A7; por diseno del transcript unico).
- R-D: mi bateria usa agente falso scripteado; la tasa REAL de omision/malformacion del
  token por CLI vivo no esta medida (el mecanismo queda probado a nivel clasificador y
  E2E determinista).
- R-E: la instruccion REVIEW llego untracked (el Arquitecto la aterriza en su coord);
  los 4 commits de la remediacion estan locales sin pushear -- mi push los publica junto
  con este veredicto (flujo establecido del arbol compartido).

## Respuesta directa a la pregunta del REVIEW

SI quedan caminos, acotados: (1) un commit ajeno SI altera el outcome en el cron
Analista deployado (E1, burn silencioso) -- ese es el bloqueante; (2) la prosa de un
obstacles[] o un eco solo altera el outcome en la clase token-ausente (X1/X2, residuo
decidido de la frontera) o imitando el token exacto en linea standalone (A1/A2,
teorico); (3) el rollback ya NO destruye contenido PREVIO del peer (E3/E4 byte-igual +
defer) -- ese vector esta cerrado; lo que SI destruye son escrituras de peer hechas
DURANTE la ventana del exec (E5, pre-existente, residual declarado con mitigacion
recomendada).

## Recomendacion de cierre y fix-loop (iteracion 2 de 2, la ultima)

**CAMBIO-REQUERIDO** acotado a F-0272R1-01: sustituir la atribucion `%an` por el canal
firmado del ledger (actor de events.jsonl en la ventana del exec) o degradar capa 3 a
nunca-confirmar; anadir a la suite el negativo de AUTOR UNIFORME. Recomendado en el
mismo commit (barato): anclaje del token a ultima linea (F-02) y verificacion de exit de
snapshots + log de rutas del rollback (F-04); cuarentena de untracked (F-03) puede
diferirse como residual explicito. Gates del re-juicio: suite retry + anthropic + lease
+ validate/encoding/neutralidad + drift REAL (funcion, no el comando vacuo) + re-corrida
de mi E1/E2/E3 y la bateria unit. Un fallo nuevo tras la iteracion 2 escala al Operador
(tope declarado en el intake).

## Gates del protocolo (clon limpio 2c3b17b salvo indicado)

- `python scripts/validate_collaboration_state.py`: vivo (con secretos) EXIT 0; clon
  (sin secretos) EXIT 0.
- `python scripts/scan_encoding.py` EXIT 0 (clon y vivo, incluye este artefacto y el MSG).
- `python scripts/scan_domain_neutrality.py` EXIT 0 (clon y vivo).
- Drift REAL via `runtime.protocol_replay.protocol_state_drift()`: clon False/5302,
  vivo False/5317 (el comando historico `--check-drift` es vacuo, ver F-05).
- `protocol.config.json` byte-identico vivo/clon sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; epoch 1.14.0
  intacta; fondo intocable sin tocar.
- Producto: NOT_RUN por instruccion canonica (SIN PRODUCTO EN ALCANCE).

---

task_id: TASK-0272
status: in_review
executive_summary: CAMBIO-REQUERIDO / NO CERRABLE con bloqueante unico. La frontera token>exit>evidencia>regex funciona en 3 de 4 capas y cierra los vectores 1, 3, 4 y 5 (token exacto robusto a imitaciones triviales; rollback byte-igual de pre-sucios worktree+staged+renames; ROLLBACK_DEFER preserva el commit del peer; entrega narrando obstaculo consumida 1x). El bloqueo es la capa de evidencia: atribuye por autor git y este hub tiene autor UNIFORME (300 commits verificados), asi que en el cron Analista cualquier commit ajeno durante un exec + token ausente convierte un aborto no-op en confirmed y quema el mensaje sin senal (E1, repro E2E determinista) -- F-0272-01 resucitado en despliegue; en el cron Codex la capa es inerte. Fix acotado: atribucion por eventos firmados del ledger o capa 3 nunca-confirma + negativo de autor uniforme en la suite. Residuales: clase token-ausente conserva el regex viejo (X1/X2); escrituras de peer DURANTE el exec se destruyen (E5, pre-existente, cuarentena recomendada); token line-scoped imitable en fence (A1/A2 teorico); gate --check-drift declarado es vacuo (drift real verificado False).
artifacts: Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter1-veredicto.md
gates: clon 2c3b17b validate/encoding/domain EXIT 0; vivo validate/encoding/domain EXIT 0; drift real False (clon seq 5302, vivo seq 5317); config #4 byte-identica 2E35F26E...354; suites maker retry/anthropic/lease EXIT 0; bateria propia 21 unit + 10 E2E: vectores 1/3/4/5 PASA, vector 2 SLIPS en despliegue (E1)
next_recommended: Rutear remediacion iteracion 2 (ultima) a Codex acotada a F-0272R1-01 con el negativo de autor uniforme; hardening barato F-02/F-04 en el mismo commit; re-juicio Analista con E1/E2/E3 + unit antes del cierre; fallo nuevo tras iter2 escala al Operador.
risks: Mientras no aterrice iter2, el cron Analista puede quemar mensajes en silencio bajo commits concurrentes cuando el agente omite o malforma el token (punto o espacio bastan para perderlo); el cron Codex reintenta entregas reales sin token (acotado y senalado). El rollback puede seguir borrando drafts de peer creados durante la ventana del exec sin log.
