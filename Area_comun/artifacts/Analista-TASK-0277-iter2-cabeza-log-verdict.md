---
artifact_id: Analista-TASK-0277-iter2-cabeza-log-verdict
task_id: TASK-0277
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-20
verdict: OK-CLOSABLE
iteration: 2 of 2 (ultima del tope)
blockers: 0
majors: 0
residuals: 3
---

# Veredicto adversarial -- TASK-0277 iteracion 2 (cabeza exacta del log)

- Revisor: Analista (voz independiente, checker). No implemente nada de esto.
- Hora local: 2026-07-20 20:55 (reloj del sistema, sin convertir).
- Encargo: MSG-20260720-Arquitecto-to-Analista-REVIEW-0280-0277-iter2-cabeza-del-log
- Alcance declarado por el Arquitecto: SIN PRODUCTO EN ALCANCE, solo este hub.
- **Veredicto: GO / OK-CLOSABLE, con tres residuales declarados.**

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit bajo juicio | `e07956e` "fix(TASK-0280): trust exact event-log head during recovery" |
| Commit padre (contraste diferencial) | `e07956e~1` = `31e7bc7` |
| HEAD del protocolo al revisar | `b54ef43` |
| Clon limpio del commit juzgado | `D:/ccvA` (checkout `e07956e`) |
| Clon limpio del padre | `D:/ccvAp` (checkout `31e7bc7`) |
| Fichero central | `scripts/prune_state.py` |

Ningun gate se ejecuto sobre el arbol caliente. Nada de lo que corri escribe estado canonico:
todas las sondas usan fixtures desechables bajo el temp del sistema. No necesite la ventana
exclusiva.

## Reproduccion (exit codes reales, clon limpio `D:/ccvA`)

```
python scripts/validate_collaboration_state.py                    -> EXIT 0
python scripts/scan_encoding.py                                   -> EXIT 0
python scripts/scan_domain_neutrality.py                          -> EXIT 0
python examples/prune_state_cases/run_prune_state_cases.py        -> EXIT 0 (7 casos)
python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py -> EXIT 0 (8 casos)
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    -> EXIT 0
```

Banco de falsacion propio: inyeccion de fallos en `scripts.prune_state.submit_intents` sobre el
fixture `enforced_fixture` real (regenesis, `enforce`+`authoritative`), en cinco puntos
distintos, y una cadena completa de residuo. No me apoye en los nombres de los tests del maker:
volvi a ejercitar cada garantia con mis propias cargas y contraste cada resultado contra el padre.

## Tabla vector por vector

| # | Vector pedido | Padre `31e7bc7` | `e07956e` | Resultado |
|---|---|---|---|---|
| A1 | Fallo DESPUES de que la transaccion se aplico: restaurar espejos solo si la cabeza no cambio | filas de espejo borradas (0), `drift = True` | filas retenidas (4 tareas / 7 claims), `drift = False`, `RuntimeError` explicito "governed prune failed after the event log advanced; archive mirrors were retained" | **PASS (F-0277R1-01 cerrado)** |
| A2 | `BaseException`: `Ctrl-C` toma el mismo camino | `KeyboardInterrupt` escapaba de `except Exception`: los espejos quedaban por accidente, sin diagnostico | `KeyboardInterrupt` **antes** del submit -> espejos restaurados byte a byte; `KeyboardInterrupt` **despues** del submit -> espejos retenidos + el mismo `RuntimeError` explicito | **PASS (F-0277R1-02 cerrado)** |
| A3 | Refrescar en vez de saltar la fila de espejo divergente | poda posterior **BLOQUEADA**: `RuntimeError: prune archive verification failed for TASK_INDEX_ARCHIVE.json: TASK-9000` | poda posterior OK: `tasks_archived=4`, `drift=False`, fila refrescada con `notes='governed mutation after interrupted prune'`, sin duplicados; identica al baseline sin residuo | **PASS (F-0277R1-03 cerrado)** |
| A4 | No salir con exit 0 cuando `has_drift` es True al final del `--apply` | -- | `if drift.get("has_drift"): raise RuntimeError(...)` antes del `return`; `main()` no captura, luego el proceso sale distinto de 0. End-to-end con drift inyectado: `--apply` **exit 1**, sin JSON de exito en stdout | **PASS** |
| A5 | Primitiva unica compartida con 0280, sin copias divergiendo | -- | `scripts/ledger_head.py::event_log_head` es la unica implementacion; `prune_state.py` la importa y el `.ps1` la invoca por subproceso | PASS |
| A6 | Cola de `events.jsonl` desgarrada mientras corre el manejador de fallo | -- | `event_log_head` lanza `JSONDecodeError` **dentro** del `except`: sepulta la excepcion original y **no** restaura los espejos aunque la cabeza no habia avanzado de verdad | **Residual R5 (no bloqueante en este camino)** |
| A7 | Fila de espejo huerfana sin gemela caliente y sin evento que la respalde | invisible | sigue invisible (`drift = False`, ningun error especifico del validador) | **Residual R6 (sin cambios respecto a iteracion 1)** |

## Detalle de las tres cadenas que si cambiaron

**A1 / A2.** El manejador es ahora `except BaseException` y compara `event_log_head(root)` antes
y despues. Si la cabeza es identica, restaura los espejos y re-lanza; si avanzo, se niega a
tocar los espejos y lanza un error que nombra el motivo y la accion de recuperacion. Lo probe
en las cuatro combinaciones (excepcion normal antes / despues, `KeyboardInterrupt` antes /
despues), no solo en las dos que prueba el maker. El contraste con el padre es limpio: donde
antes el rollback compensatorio destruia una transaccion firmada que **si** se habia aplicado
(drift True), ahora la deja intacta (drift False) y avisa.

**A3.** `archive_removed_entries` pasa de deduplicar por id a mantener posiciones y **refrescar**
la fila cuando el contenido diverge. Reproduje la cadena completa que reporte en la iteracion 1
(residuo de kill duro -> mutacion gobernada real via `submit_intents` con claim + `task_upsert` +
release -> poda posterior), no solo la unidad aislada que prueba el maker: el padre se bloquea
con el mismo `RuntimeError` de verificacion que reporte entonces, y `e07956e` completa la poda y
deja el espejo con el contenido correcto. El bloqueo permanente que exigia editar el espejo a
mano ha desaparecido.

**A4.** El chequeo final es una linea recta antes del `return`, sin captura intermedia. Lo
confirme por comportamiento end-to-end: con drift presente, `python scripts/prune_state.py
--apply` sale 1 y no imprime el JSON de exito. El "verde falso sobre arbol derivado" que
reporte en la iteracion 1 esta cerrado.

## Residuales declarados

- **R5 (nuevo, de esta iteracion).** Si la ultima linea de `events.jsonl` esta desgarrada en el
  momento en que corre el manejador de fallo, `event_log_head` lanza `JSONDecodeError` desde
  dentro del `except`: se pierde la excepcion original (no llega el `raise ... from exc`) y los
  espejos **no** se restauran aunque la cabeza no hubiera avanzado. Observado en laboratorio:
  `mirrors restored to pre-run = False`. Lo declaro no bloqueante aqui porque es el camino de
  fallo de un camino de fallo, bajo escritor unico, y el residuo que deja (filas pre-escritas)
  ya es auto-sanable por el arreglo A3 y detectable por el validador mientras exista la gemela
  caliente (`Duplicate task across hot/archive`). **La misma intolerancia si es bloqueante en el
  camino de TASK-0280** (F-0280R1-02 de mi otro veredicto): endurecer alli `event_log_head`
  cierra esto tambien, y el cambio es compatible con 0277 ya cerrada.
- **R6 (heredado de la iteracion 1, sin cambios).** Una fila de espejo sin evento que la respalde
  y sin gemela caliente sigue siendo completamente invisible: `drift = False` y el validador no
  la nombra. Las filas de espejo de mas se ignoran por diseno (es lo que hace segura la
  pre-escritura), y eso es exactamente lo que hace silencioso este huerfano.
- **R7.** El chequeo final de drift lanza una excepcion sin capturar, asi que el operador ve un
  traceback en vez de un diagnostico. El exit code es correcto (lo que gatea), pero la ergonomia
  es pobre; ademas, si no hay nada que podar y hay drift preexistente, el mensaje atribuye el
  drift a la poda ("governed prune left protocol state drift") cuando la poda no hizo nada.
  Cosmetico, no bloqueante.

## Recomendacion de cierre

**OK-CLOSABLE.** Los cuatro arreglos pedidos estan implementados y verificados por
comportamiento, cada uno con su contraste contra el padre y con negativo permanente en
`examples/prune_state_cases/run_prune_state_cases.py` (7 casos, exit 0 en clon limpio). Los tres
hallazgos que bloquearon la iteracion 1 (F-0277R1-01, F-0277R1-02, F-0277R1-03) estan cerrados.
Firmo el cierre de TASK-0277 con R5, R6 y R7 declarados arriba, y con una nota de coordinacion:
R5 se cierra gratis cuando se endurezca `event_log_head` en la remediacion de TASK-0280.

Este veredicto es independiente del de TASK-0280 aunque compartan commit: no hay solapamiento de
ficheros entre las dos unidades y ninguna correccion pendiente en 0280 invalida lo verificado aqui.

-- Analista
