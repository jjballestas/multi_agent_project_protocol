# ANALISTA TASK-0225 remediacion-2 veredicto

Firma: Analista

## Veredicto

GO / CERRABLE.

La remediacion-2 cierra el NO-GO previo: el clasificador ya no depende de `project` para contar filas
`in_review` relevantes. En clon limpio de protocolo, el dry-run canonico reporta `ledger_write=false`,
incluye `TASK-0225` y `TASK-0227` en `ws_snapshot.in_review`, y decide `review_or_ratify`, no
`promote_one_ready_task`.

## Ancla canonica

| Item | Valor |
|---|---|
| Protocolo bajo instruccion | `349a8cac40d3fdfaa7ccf463769db1526b3d6766` |
| Implementacion bajo review | `8385868` (`fix(TASK-0225): repair ws snapshot classifier`) |
| Clon limpio protocolo | `C:/Users/johnb/AppData/Local/Temp/analista-0225-review-1089e690106144bcbb9ff5d19a2a088f/protocol` |
| Producto Zeus-protocol | sin commit de producto citado en la instruccion; control en HEAD local `b2b2395da39090109db6de2dc50726dbaab1a11e` |
| Clon limpio producto | `C:/Users/johnb/AppData/Local/Temp/analista-0225-review-1089e690106144bcbb9ff5d19a2a088f/zeus-protocol` |
| `protocol.config.json` sha256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Reproduccion por exit code

| Gate | Contexto | Exit | Resultado |
|---|---:|---:|---|
| `git clone` + checkout protocolo | limpio, HEAD `349a8ca` | 0 | status limpio |
| `git clone` + checkout producto | limpio, HEAD `b2b2395` | 0 | status limpio |
| `npm test` | producto limpio | 0 | 109 tests, 87 pass, 22 skipped |
| PowerShell parser | `personal/Arquitecto/arquitecto_cron.ps1` | 0 | parser ok |
| `-RunClassifierSelfTest` | protocolo limpio | 0 | PASS, 3/3 vectores |
| `-DryRunOnce` | protocolo limpio | 0 | `ledger_write=false`, `in_review=[TASK-0222,TASK-0225,TASK-0227]`, decision `review_or_ratify` |
| Payloads propios extraidos por AST | `Test-WsTask` + `New-WsSnapshot` | 0 | PASS, 6/6 vectores |
| `python scripts/validate_collaboration_state.py` | vivo con secretos | 0 | OK; warning no bloqueante de mailbox FYI viejo |
| `python scripts/validate_collaboration_state.py` | clon limpio sin secretos | 0 | OK; mismo warning no bloqueante |
| `python scripts/scan_domain_neutrality.py --root .` | vivo y clon limpio | 0 | limpio |
| `python scripts/scan_encoding.py --root .` | vivo y clon limpio | 0 | limpio |
| drift #4 | vivo y clon limpio | 0 | `has_drift=false`, `up_to_seq=2775` |
| #4 byte-identica | vivo vs clon limpio | 0 | sha256 igual |

## Vectores adversariales

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| `TASK-02xx` `in_review` sin `project` | PASA | self-test: `task02_in_review_without_project` -> `review_or_ratify`, `in_review_count=1` |
| Tarea WS/REQ-ZEUS `in_review` sin `project` | PASA | self-test: `req_zeus_ws_in_review_without_project` -> `review_or_ratify`, `in_review_count=1` |
| Una `ready` no se promueve si existe cualquier `in_review` relevante | PASA | self-test: `ready_not_promoted_when_relevant_in_review_exists` -> `review_or_ratify`, no promotion |
| Titulo `WS1` sin `project` ni id `TASK-02` | PASA | payload propio `ws_title_without_project_counts` -> `review_or_ratify`, `in_review_count=1` |
| `project=Zeus-protocol` sin marcador en id/titulo | PASA | payload propio `known_project_without_marker_counts` -> `review_or_ratify`, `in_review_count=1` |
| Ready no relevante sin `project` | PASA | payload propio `non_relevant_ready_does_not_promote` -> `no_action` |
| Ready relevante sin reviews | PASA | payload propio `relevant_ready_promotes_when_no_review` -> `promote_one_ready_task` |
| Dry-run canonico con estado real | PASA | `TASK-0225` y `TASK-0227` aparecen en `ws_snapshot.in_review`; `ledger_write=false` |

## Residuales declarados

- El clasificador sigue siendo heuristico y amplio: `TASK-02xx` y marcadores de titulo pueden contar falsos positivos.
  En este flujo el fallo es conservador: bloquea/promueve menos, no abre promocion con review pendiente.
- No se lanzo el loop vivo; solo se verifico parser, self-test, dry-run y comportamiento de clasificacion.

## Recomendacion

OK -> CERRABLE para TASK-0225 remediacion-2.
