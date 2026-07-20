# ANALISTA - TASK-0272 fin del seen-burn silencioso - veredicto adversarial

Firma: Analista (voz adversarial independiente). Fecha local: 2026-07-20 13:47.
Instruccion canonica: `Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0272-seenburn.md`.

## Veredicto de cabecera

**CAMBIO-REQUERIDO / NO CERRABLE.** La unidad es una mejora neta grande (los positivos de
suite, tope+senal, defer de residuo vivo y espejo born-operational PASAN), pero la respuesta
a la pregunta del REVIEW es SI a ambas: logre que reintente una negativa principiada
(F-0272-05) Y que un aborto deje residuo staged que ademas destruye contenido ajeno no
commiteado (F-0272-04). Peor: reproduje DOS resurrecciones del seen-burn silencioso -- el
defecto que la unidad promete eliminar -- por confirmacion falsa via commit de peer
(F-0272-01) y por eco de vocabulario definitivo en el transcript (F-0272-02); y una entrega
CONFIRMADA que termina marcada como agotada/fallida por narrar su obstaculo (F-0272-03).
Causa raiz comun: el clasificador confia en regex sobre texto libre del agente por encima de
la verdad de terreno (exit code + evidencia), y la evidencia es global del repo, no
atribuible al exec. El maker ya resolvio esta clase de problema para las ordenes de stop con
token exacto (STOP_JOB, igualdad case-sensitive): el outcome necesita la misma disciplina.

## Ancla canonica y reproduccion

- Implementacion `d3b0f55` + `9ad8c89`, entrega `881feab`; instruccion en HEAD `e7ad9e6`.
- Clon limpio `D:/ccv0272` checkout `e7ad9e6a2037e14f80855f2f0afbb50f41d59c68`; todos los
  gates y suites corridos AHI. Invariancia verificada a `22a0a2a` (HEAD avanzo durante la
  pasada por TASK-0273; diff en rutas juzgadas de 0272/0258 = solo `scripts/new_instance.py`
  con el pin CI del hook y el mensaje de poda, fuera del alcance juzgado; el runner, la
  suite, los wrappers y los tests de harness quedaron diff-vacio).
- Suites del maker en el clon (exit codes): `python examples/mailbox_retry_cases/
  run_mailbox_retry_cases.py` EXIT 0; `python scripts/test_anthropic_checker_harness.py`
  EXIT 0; `python scripts/test_exec_lease_harness.py` EXIT 0.
- Bateria adversarial propia: sandboxes git efimeros con el runner REAL del clon
  (`scripts/harness/peer_mailbox_cron.ps1`) y un agente falso scripteado
  (`-IntervalSeconds 1 -RetryBackoffSeconds 0 -MaxTransientRetries 3`; el stdout del agente
  falso es exactamente el texto citado por escenario). Observables: log del runner
  (EXEC_EXIT outcome=..., RETRY_*), seen.json, retry.json, contador de execs y
  `git status --porcelain` post-run.

## Tabla vector por vector (instruccion del Arquitecto)

| # | Vector | Resultado | Evidencia falsable |
|---|--------|-----------|--------------------|
| 1 | Visto SOLO tras ejecucion confirmada | **SLIPS** | S5: abort no-op con exit 0 y stdout "Ventana no segura; me retiro sin escribir" mientras un commit de PEER mueve HEAD durante el exec -> `outcome=confirmed`, seen marcado, 1 solo exec, cero senal. Burn silencioso reproducido. S4: retirada DECISION-0020 ("claim ajeno activo") cuyo transcript ECO "NO-GO" de un veredicto previo -> `outcome=definitive`, seen marcado al primer exec. |
| 2 | Reintento acotado + backoff + tope + senal al agotar | **PASA** | S8: transitoria persistente -> 3 intentos exactos, `RETRY_EXHAUSTED ... signal=watchdog` en el log, ciclos posteriores excluyen el mensaje (execs=3 con 6 rondas), retry.json `exhausted:true` distinguible de seen. |
| 3 | Taxonomia: definitivo JAMAS reintenta | **SLIPS** | PASA con keyword: S2 "NO-GO: rechazo por alcance" -> consumido 1 vez, sin retry. SLIPS sin keyword: S3 negativa principiada real ("No asumo este encargo: soy checker, no maker... me retiro sin escribir") -> `unconfirmed`, REINTENTADA 3 veces + RETRY_EXHAUSTED. El AC dice "no se reintentan JAMAS"; el fraseo del LLM no esta bajo control del harness. |
| 4 | Rollback del propio residuo | **SLIPS** | PASA para rutas limpias-antes (suite: archivo A staged removido). SLIPS S6: ruta tracked PRE-modificada (worktree B sin stagear, como los state/*.json de este hub casi siempre) que el exec sobreescribe (C) y stagea -> tras el aborto queda `M  f.txt` STAGED con contenido C: ni unstage ni revert, y el contenido B del peer quedo DESTRUIDO. Es la bomba del incidente 11:03 para la clase de ruta mas comun. SLIPS S7: rename staged (`git mv`) sobrevive el rollback (porcelain "old -> new" parseado como una sola ruta). |
| 5 | Idempotencia contra el estado | **SLIPS** | S9: entrega CONFIRMADA (exit 0 + commit propio "delivered work" en git log) cuyo stdout narra "Obstaculo registrado: claim ajeno activo, resuelto tras espera" -> `transient` 3 veces, seen nunca marcado, el trabajo aplicado fue RE-INVOCADO 2 veces mas (solo la idempotencia del agente evito duplicar) y la unidad ENTREGADA termina en RETRY_EXHAUSTED = senal falsa de fallo. La narracion manda sobre exit+evidencia; choca de frente con obstacles[] de TASK-0258, que institucionaliza ese vocabulario en reportes EXITOSOS. |
| 6 | Suite del escenario real | **PASA** | Suite E2E en clon EXIT 0 (aborto -> no quemado -> rollback -> procesado al ciclo siguiente, 2 execs). Falta el negativo de taxonomia (definitivo-no-reintenta: mi S2) y los negativos de S4/S5/S6/S9. |
| 7 | Espejo born-operational | **PASA** | Export runtime-tier con `new_instance.py` a sandbox: runner byte-identico sha256 `21afee4c3594dbf1d11d4636bc364fb68d96906541bd2aecf22232a50f9e5fc6` + prompts implementer/reviewer shipped. Wrappers de instancia (codex/analista_mailbox_cron.ps1) delegan al generico con paridad de parametros de retry. |
| - | Discriminador residuo vivo-vs-abortado | **PASA** | S10: staged fresco de peer -> RETRY_DEFER cada ciclo, 0 execs, mensaje intacto, trabajo del peer intacto. |
| - | Deadlock gate-peer documentado | **PASA con nota** | Dos salidas documentadas en `scripts/harness/README.md` (liberar claim / un solo `--no-verify` con gates de fondo a mano); el fix estructural es TASK-0273 (correctamente cross-referenciado en ambos out_of_scope). Nota: vive en el README del harness, no junto al hook. |

## Hallazgos (todos con repro determinista propia)

- **F-0272-01 (WARNING-real, el mas filoso): confirmacion falsa por movimiento del peer.**
  `Get-ExecOutcomeClass` computa EvidenceChanged con `git rev-parse HEAD + git status` del
  REPO entero: cualquier commit de peer durante el exec (estado normal de este arbol
  compartido) convierte un abort exit-0 sin keywords en `confirmed` y QUEMA el mensaje sin
  senal. Es la resurreccion literal del defecto de la tarea. El propio acceptance descarto
  los commits como discriminador porque "no ven trabajo en vuelo"; aqui se usan como senal de
  confirmacion con la debilidad simetrica.
- **F-0272-02 (WARNING-real): burn por eco de vocabulario definitivo.** El regex definitivo
  matchea en CUALQUIER parte del stdout+stderr. Un retiro transitorio que cite "NO-GO" (los
  mensajes de este repo lo contienen rutinariamente: la propia instruccion de este REVIEW
  lleva "NO-GO" en requested_action) se clasifica `definitive` y consume el mensaje.
- **F-0272-03 (WARNING-real): la narracion manda sobre la verdad de terreno.** Precedencia
  definitive -> transient -> exit+evidencia: una entrega confirmada que narra su obstaculo
  transitorio nunca marca seen, re-invoca trabajo aplicado y acaba en senal falsa de
  agotamiento. Interaccion directa con obstacles[] (TASK-0258).
- **F-0272-04 (WARNING-real): rollback ciego a rutas pre-sucias.** `Restore-
  TransientExecResidue` solo repara rutas AUSENTES del status previo: lo que el exec stagea/
  sobreescribe sobre una ruta ya modificada persiste staged Y con el contenido del exec
  (contenido previo del peer destruido, irrecuperable al no estar commiteado). En este hub
  los state/*.json estan pre-modificados de forma casi permanente: es la clase dominante del
  incidente 11:03. Atenuante: ya no es silencioso (defer/senal posteriores), pero la bomba
  persiste y exige limpieza manual.
- **F-0272-05 (WARNING-real): negativa principiada reintentada.** Fraseos de rechazo fuera
  de la lista de 6 keywords (p.ej. el precedente real "no lo asumo: rompe maker != checker")
  caen a `unconfirmed` y se reintentan hasta el tope. El AC lo prohibe en absoluto
  ("JAMAS"). Atenuante: acotado a 3 + senal, no bucle infinito.
- **F-0272-06 (WARNING-theoretical): rename staged sobrevive el rollback.** Porcelain
  "R old -> new" no se parsea; el comando de restore falla en silencio (2>$null).

## Recomendacion de cierre y fix-loop (iteracion 1/2)

**CAMBIO-REQUERIDO.** Remediacion esperada (espejo de la disciplina STOP_JOB que el maker ya
aplico en esta misma unidad):

1. **Contrato de outcome por token exacto** en el prompt/envelope del agente (p.ej. una
   linea final `OUTCOME: confirmed|transient|definitive` con igualdad exacta), con el regex
   actual SOLO como fallback; documentarlo en README + prompts shipped. Cierra F-01/02/03/05.
2. **Atribucion de evidencia o prioridad del token sobre la evidencia global**: el commit de
   un peer no puede confirmar mi exec (F-01); exit 0 + evidencia + token confirmado si.
3. **Rollback por delta de INDICE ademas de delta de status**: capturar `git diff --cached
   --name-only` antes/despues y desestagear lo nuevo-staged aunque la ruta estuviera
   pre-modificada; snapshot (stash create u equivalente) si se quiere restaurar contenido; y
   parseo de renames (porcelain -z o prefijo R). Cierra F-04/06.
4. **Negativos permanentes en la suite**: definitivo-no-reintenta, falso-confirmed por
   commit externo, falso-definitive por eco, entrega-narrada (S9) y pre-sucia staged (S6).

Gates afectados: suite mailbox_retry + encoding + validate. Re-juicio: re-corro mi bateria
completa (los 6 slips deben voltear a verde) + suite + gates en clon limpio. Maximo 2
iteraciones antes de escalar al Operador.

## Gates del protocolo (clon limpio e7ad9e6 salvo indicado)

- `python scripts/validate_collaboration_state.py`: vivo (con secretos) EXIT 0; clon (sin
  secretos) EXIT 0.
- `python scripts/scan_encoding.py` EXIT 0; `python scripts/scan_domain_neutrality.py` EXIT 0.
- `python runtime/protocol_replay.py --check-drift` EXIT 0 (drift 0).
- `protocol.config.json` byte-identico vivo/clon sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; epoch 1.14.0 intacta.
- Producto: NOT_RUN por instruccion canonica (SIN PRODUCTO EN ALCANCE).

## Residuales declarados

- R1: el tier coordination NO shippea `scripts/harness/` (solo runtime-tier); diseno previo a
  0272, no regresion de esta unidad, pero el claim "born operational" es por-tier.
- R2: exito externo-sin-evidencia queda `unconfirmed` y reintentable -- declarado por el
  maker en el handoff; correcto como fail-closed, se registra.
- R3: mi bateria corrio con el agente falso scripteado; la exposicion REAL de F-02/03 depende
  de cuanto transcript emite cada CLI (codex exec emite narracion completa; claude -p solo el
  mensaje final) -- el mecanismo queda probado a nivel de clasificador con repro determinista.
- R4: HEAD avanzo dos veces durante la pasada (0273 + memoria de entrega del maker);
  invariancia de rutas juzgadas verificada por diff; los state files modificados del arranque
  aterrizaron en 3062214/67ac1e8/22a0a2a y el arbol quedo limpio antes de mi entrega.

---

task_id: TASK-0272
status: in_review
executive_summary: CAMBIO-REQUERIDO / NO CERRABLE. Positivos PASAN (tope+senal, defer residuo vivo, suite E2E, espejo born-operational, keyword-definitivo no reintenta), pero reproduje con repro determinista - 2 resurrecciones del seen-burn silencioso (confirmed falso por commit de peer; definitive falso por eco de NO-GO), negativa principiada reintentada 3x, rollback que deja staged y destruye contenido pre-modificado del peer (clase dominante del incidente 11:03), rename staged sobreviviente, y entrega confirmada que muere en RETRY_EXHAUSTED por narrar su obstaculo (choque directo con obstacles[] de 0258). Causa raiz comun: regex sobre texto libre manda sobre exit+evidencia y la evidencia no es atribuible al exec. Fix esperado: contrato de outcome por token exacto (disciplina STOP_JOB) + atribucion de evidencia + rollback por delta de indice + negativos permanentes.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0272-seenburn-retry-veredicto.md
gates: clon e7ad9e6 validate EXIT 0; encoding EXIT 0; domain EXIT 0; drift EXIT 0; config #4 byte-identica 2E35F26E...354; suites maker retry/anthropic/lease EXIT 0; bateria adversarial 3 PASA / 6 SLIPS
next_recommended: Rutear la remediacion a Codex con los 4 puntos del fix-loop; re-juicio Analista con la bateria completa antes del cierre; iteracion 1/2.
risks: Mientras no aterrice el fix, el harness puede quemar mensajes en silencio bajo commits concurrentes de peer (F-01) o eco de vocabulario (F-02), reintentar negativas principiadas (F-05) y dejar residuo staged destructivo sobre rutas pre-sucias (F-04); el residuo si queda senalizado (no silencioso).
