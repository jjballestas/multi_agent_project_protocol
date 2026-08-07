---
artifact: Analista-TASK-0324-post-delivery-progress-deadline-verdict
task_id: TASK-0324
reviewer: Analista
role: checker (maker != checker)
verdict: CHANGE-REQUIRED
implementation_commit: c121fa9cddc93ce84b4611fba41845423faa2fb7
protocol_head: 2d293eaccf41726fff53858f626b434d8d44292b
created_at: 2026-08-07T08:52:00+02:00
---

# Veredicto Analista -- TASK-0324 (ventana de post-entrega y extensiones por progreso)

Hora local del sistema: 2026-08-07 08:52 (UTC+2).

## 1. Ancla canonica

- Commit de implementacion revisado: `c121fa9cddc93ce84b4611fba41845423faa2fb7`.
- HEAD del protocolo: `2d293eaccf41726fff53858f626b434d8d44292b`, identico a `origin/main`.
- Alcance declarado por el Arquitecto: SOLO el hub. SIN PRODUCTO EN ALCANCE. No he ejecutado
  ningun `npm test` de Nova ni de Zeus. No he revisado 0320, 0322, 0325 ni 0326.
- Clon limpio detached bajo el scratch root de la instancia (DECISION-0104):
  `D:/Aegis_Scratch/multi_agent_project_protocol/rev0324/cc`, `git checkout --detach c121fa9c`,
  `git status --short` vacio (0 lineas). Todos los gates y todas las sondas se ejecutaron ALLI,
  nunca en el arbol caliente.

## 2. Gates recomputados por exit code

Ejecutados en el clon limpio, cada uno con su exit code capturado directamente (sin tuberia que
enmascare el codigo):

| Gate | exit |
|---|---|
| `python scripts/test_exec_lease_harness.py` (16/16) | 0 |
| `python scripts/check_falsification_contracts.py --root . --inventory` (33 declarados) | 0 |
| `python scripts/validate_collaboration_state.py --root .` | 0 |
| `python scripts/scan_encoding.py --root .` | 0 |
| `python scripts/scan_domain_neutrality.py --root .` | 0 |
| `python runtime/protocol_replay.py --check-drift --root .` -> `verdict=CLEAN up_to_seq=7358` | 0 |
| `git diff --check` | 0 |
| `git status --short` | 0 lineas |

Estado canonico del arbol vivo antes de revisar: `validate_collaboration_state.py` exit 0, sin
modificaciones en rutas gobernadas (solo ficheros sin rastrear en areas personales ajenas, que no
he tocado).

## 3. Que hace realmente el cambio

Anade `Get-PostDeliveryDeadlineAfterProgress` (12 lineas) y CABLEA tres lineas dentro de la rama de
progreso del deadline PRINCIPAL, en el bucle de supervision real: cuando la rama principal extiende
`$deadlineUtc`, empuja tambien `$postDeliveryDeadlineUtc` al maximo entre el vigente y el nuevo
deadline principal, recortado al `$postDeliveryHardDeadlineUtc` ya calculado. Nada mas cambia en el
`.ps1`.

La causa raiz del incidente es el CONSUMO COMPARTIDO de la senal de progreso: ambas ramas leen y
escriben `$progressOutputBytes`/`$progressLedgerBytes`. Si la rama principal corre primero en un
tick y consume el delta de bytes, la rama de post-entrega evalua despues sobre contadores ya
consumidos, no ve crecimiento y mata. El fix NO desacopla los contadores: compensa heredando el
deadline, de modo que la rama de post-entrega ya no llega a evaluar dentro de la ventana que la
principal acaba de conceder. Es coherente con el AC2 (aplicar la politica que la otra mitad del
archivo ya cumple) y con el `out_of_scope`, pero conviene no leer el AC2 como "la inanicion de la
senal desaparecio". Queda declarado en R4.

## 4. Reproduccion: prueba de CAMINO VIVO (foco A del Arquitecto)

No me basta con que la sonda determinista del maker pase: esa sonda invoca la funcion pura
aislada, y la unica prueba de que el arreglo esta vivo que trae el contrato es
`assert wiring in source`, una comprobacion de subcadena.

Extraje del fichero real, por AST de PowerShell, el `WhileStatementAst` que contiene
`POST_DELIVERY_WINDOW_START` -- es decir, EL BUCLE DE SUPERVISION LITERAL, texto sin reescribir --
y tambien la funcion real `Get-ExecProgressState`. Solo estan simulados `Write-Log`,
`Update-ExecLeaseHeartbeat`, `Get-OwnDeliveryEvidence`, `Stop-LeaseProcessTree` y el objeto
proceso. La deteccion de progreso es la logica embarcada leyendo tamanos de fichero REALES: el
falso proceso escribe 98 bytes al log de salida en los ticks 1..4 y luego se calla, que es
exactamente la forma del incidente (la principal consume el delta, la de post-entrega evalua
despues sobre silencio).

Reloj comprimido: deadline principal en t0+3,5 s; ventana de post-entrega de 5 s abierta en el
tick 1; `ProgressExtensionSeconds` 6 s; tope duro 30 s.

**A. Fuente tal cual se entrega en `c121fa9c`:**

    06:42:27 POST_DELIVERY_WINDOW_START pid=4242 timeout_seconds=5
    06:42:30 EXEC_PROGRESSING pid=4242 reason=run_log_growing next_deadline=06:42:36.2143207Z
    06:42:36 EXEC_HUNG pid=4242 reason=no_progress action=terminate

    post_delivery_timeout_fired = False    sobrevive 10,1 s

**B. Misma fuente con el cableado convertido en CODIGO MUERTO** (la sentencia queda byte a byte
identica; solo su rama guarda pasa a ser inalcanzable, `if ($false -and $null -ne ...)`):

    06:42:38 POST_DELIVERY_WINDOW_START pid=4242 timeout_seconds=5
    06:42:41 EXEC_PROGRESSING pid=4242 reason=run_log_growing next_deadline=06:42:47.1457990Z
    06:42:43 POST_DELIVERY_TIMEOUT pid=4242 timeout_seconds=5 action=terminate
    06:42:43 EXEC_HUNG pid=4242 phase=post_delivery reason=no_progress action=terminate

    post_delivery_timeout_fired = True     muere a los 6,1 s

La variante B es el incidente del 2026-08-07: el harness concede hasta las 06:42:47 y termina a las
06:42:43, cuatro segundos ANTES del plazo que el mismo acaba de escribir en su log. La variante A
no lo hace. **El arreglo esta en el camino vivo y el camino vivo importa: probado por
comportamiento, no por lectura.**

## 5. El SLIP: el contrato permanente NO mata esa regresion

Aplique ese mismo mutante de codigo muerto al fichero del clon limpio y corri los gates que el AC4
declara como su proteccion:

    python scripts/test_exec_lease_harness.py
      -> PASS test_post_delivery_window_honors_main_progress_extensions
      -> suite exit 0
    python scripts/check_falsification_contracts.py --root . --inventory
      -> exit 0

El mutante sobrevive intacto. La razon es estructural: la sonda del contrato llama a la funcion
pura, que el mutante no toca, y la unica atadura al camino vivo es
`assert wiring in source`, que el mutante satisface byte a byte porque no borra la sentencia, solo
la deja inalcanzable.

El AC4 pide "negativo permanente que mute el harness para que ignore las extensiones y exija que el
test caiga". He construido un mutante del harness que ignora la extension heredada -- en el unico
lugar donde ignorarla tiene consecuencias operativas -- y he probado por comportamiento que
reproduce el defecto original. El test no cae. El contrato protege el helper; no protege el efecto.
El helper por si solo no arregla nada: todo el valor de esta tarea esta en las tres lineas de
cableado, y son precisamente las que el negativo no cubre.

Es la misma forma que costo TASK-0319, en su version espejo: alli habia una rama que parecia
cobertura y era codigo muerto; aqui la cobertura es real pero el contrato no distingue el codigo
vivo del codigo muerto. Que hoy el codigo este vivo lo he verificado yo; el contrato permanente
existe para que eso siga siendo cierto sin que nadie lo verifique a mano, y hoy no lo garantiza.

Restaure el fichero (`git checkout --`, `git status --short` = 0 lineas) antes de seguir.

## 6. Tabla vector por vector

| # | Vector | Origen | Resultado | Evidencia |
|---|---|---|---|---|
| M1 | La segunda extension principal mueve el deadline de post-entrega mas alla del corte original | maker | PASS | s.4: A sin `POST_DELIVERY_TIMEOUT`; B lo dispara dentro del plazo concedido |
| M2 | Terminacion sin progreso y tope absoluto intactos | maker | PASS | s.4 A muere por `no_progress` en el plazo concedido; s.8 muere por `hard_cap` |
| M3 | El mutante declarado muere | maker | PASS | `test_post_delivery_window_honors_main_progress_extensions` exit 0 con la asercion `mutant["alive_at_original_timeout"] is False` |
| M4 | La rama principal cambio solo en sincronizar la de post-entrega | maker | PASS | diff: 3 lineas anadidas dentro de la rama, sin tocar `$deadlineUtc`, contadores ni `$execHardDeadlineUtc`; A conserva cadencia y semantica |
| A | El fix esta en el CAMINO VIVO, no solo en la sonda | Arquitecto | PASS | s.4, replay del bucle real extraido por AST |
| A1 | El contrato permanente protege ese camino vivo | derivado de A | **SLIP** | s.5: mutante de codigo muerto sobrevive a la suite y al inventario, ambos exit 0 |
| B | Clamp en las DOS direcciones | Arquitecto | PASS | s.7: 8 casos dirigidos + 120 aleatorios, 0 acortamientos, 0 desviaciones de `min(max(cur,exec),hard)` |
| C | El tope duro sigue siendo inextensible | Arquitecto | PASS | s.8: con progreso continuo muere por `hard_cap` en el instante precalculado |
| D | El inventario declara, no ejecuta | Arquitecto | PASS | verificado por EJECUCION: `.github/workflows/validate.yml:238` corre `test_exec_lease_harness.py`; el runner de ESTE contrato si se ejecuta en CI. No cuento el inventario como prueba |

## 7. Foco B -- el clamp, falsado por los dos lados

Sondas propias contra la funcion real extraida por AST, con payloads mios, no los del maker:

| caso | current | hard | exec | obtenido | esperado |
|---|---|---|---|---|---|
| V1 exec muy anterior, no debe acortar | 02:44:00 | 02:59:00 | 02:20:00 | 02:44:00 | 02:44:00 |
| V2 exec igual al vigente | 02:44:00 | 02:59:00 | 02:44:00 | 02:44:00 | 02:44:00 |
| V3 exec un tick despues | 02:44:00 | 02:59:00 | 02:44:01 | 02:44:01 | 02:44:01 |
| V4 exec igual al tope | 02:44:00 | 02:59:00 | 02:59:00 | 02:59:00 | 02:59:00 |
| V5 exec por encima del tope, recorta | 02:44:00 | 02:59:00 | 03:30:00 | 02:59:00 | 02:59:00 |
| V6 vigente ya en el tope | 02:59:00 | 02:59:00 | 03:30:00 | 02:59:00 | 02:59:00 |
| V7 incidente real con el tope de post-entrega verdadero (900 s) | 02:44:00 | 02:59:00 | 02:44:41 | 02:44:41 | 02:44:41 |
| V8 vigente por encima del tope (patologico, no alcanzable) | 03:10:00 | 02:59:00 | 02:20:00 | 02:59:00 | acorta al tope |
| V9 exec = DateTime.MinValue | 02:44:00 | 02:59:00 | MinValue | 02:44:00 | 02:44:00 |
| V10 tope duro `$null` | 02:44:00 | `$null` | 02:44:41 | `REJECTED_AT_BINDING` | falla ruidoso |

Barrido aleatorio de 120 ternas con la invariante que el bucle mantiene (`current <= hard`):
**0 desviaciones** respecto a `min(max(current, exec), hard)` y **0 casos de acortamiento**.
Monotonia bajo aplicacion repetida con una secuencia de extensiones descendente: nunca retrocede.
La direccion incompleta que el Arquitecto pedia falsar esta cerrada: la funcion es exactamente el
maximo recortado, sin ningun camino que acorte el deadline vigente.

V8 solo acorta en un estado que el bucle no puede producir (`$postDeliveryDeadlineUtc` se recorta al
tope en las dos rutas que lo escriben, asi que nunca lo supera). Lo dejo anotado, no es un defecto.

## 8. Foco C -- el tope duro, bajo progreso continuo

Mismo replay del bucle vivo, pero con el proceso escribiendo en TODOS los ticks (progreso perpetuo,
la unica forma de intentar la fuga indirecta por herencia):

    06:43:51 POST_DELIVERY_WINDOW_START timeout_seconds=5
    06:43:54 EXEC_PROGRESSING next_deadline=06:44:00.44 hard_deadline=06:44:23.8407321Z
    06:44:00 EXEC_PROGRESSING next_deadline=06:44:06.47 hard_deadline=06:44:23.8407321Z
    06:44:06 EXEC_PROGRESSING next_deadline=06:44:12.49 hard_deadline=06:44:23.8407321Z
    06:44:12 EXEC_PROGRESSING next_deadline=06:44:18.52 hard_deadline=06:44:23.8407321Z
    06:44:18 EXEC_PROGRESSING next_deadline=06:44:23.8407321Z hard_deadline=06:44:23.8407321Z
    06:44:24 EXEC_HUNG reason=hard_cap action=terminate

Muere por `hard_cap` en el instante precalculado, 34,3 s tras el arranque = deadline principal
(3,5 s) + tope (30 s), y ni una extension mas. La herencia no abre ninguna via de escape: por
construccion `postDeliveryDeadline <= postDeliveryHardDeadline` siempre, de modo que en cuanto
`UtcNow` supera el tope la rama de post-entrega entra y clasifica `hard_cap`; y el tope principal,
que es anterior o igual en la practica, ya habia matado. El unico impedimento a que un exec colgado
viva para siempre sigue intacto.

## 9. Residuales declarados (ninguno bloqueante por si mismo)

- **R1 -- un numero del contrato no corresponde al sistema real.** El boundary declarado
  `clamped_deadline == "2026-08-07T02:55:40..."` y la evidencia del AC3 en el handoff presentan
  02:55:40 como el tope duro de la ventana de POST-ENTREGA. Con los valores embarcados
  (`ProgressHardCapSeconds = 900`, base de post-entrega 02:44:00) el tope real de esa ventana en el
  incidente habria sido **02:59:00**; 02:55:40 es el tope del deadline PRINCIPAL, que es lo que
  imprimian las lineas `EXEC_PROGRESSING` del log. La funcion es generica y el recorte se ejercita
  igual, asi que no cambia ningun veredicto de codigo -- pero deja en el registro permanente un
  numero que el sistema vivo no produce en ese escenario.
- **R2 -- el fix ciega su propia observabilidad.** En las tres corridas del bucle vivo,
  `pd_progress_extensions = 0`: con la herencia activa la rama propia de post-entrega ya casi nunca
  se ejecuta, asi que la linea `EXEC_PROGRESSING ... phase=post_delivery` deja de aparecer, y la
  linea de la rama principal imprime SOLO `next_deadline`/`hard_deadline` del deadline PRINCIPAL.
  El plazo efectivo de la ventana de post-entrega pasa a ser invisible en el log. El defecto
  original se diagnostico precisamente contrastando esos plazos impresos con la hora de la muerte;
  tras el fix ese contraste ya no se puede hacer desde el log.
- **R3 -- acoplamiento fragil entre las dos variables.** La guarda comprueba
  `$null -ne $postDeliveryDeadlineUtc` pero pasa `$postDeliveryHardDeadlineUtc`. Hoy la invariante
  se sostiene porque ambas se asignan en el mismo bloque. Si se rompiera, el binding tipado
  `[DateTime]` rechaza `$null` (verificado, V10: `REJECTED_AT_BINDING`), asi que fallaria ruidoso y
  no recortaria en silencio a `DateTime.MinValue`. Fallo seguro, anotado.
- **R4 -- la causa raiz sigue viva.** Las dos ramas siguen compartiendo
  `$progressOutputBytes`/`$progressLedgerBytes`; la principal sigue consumiendo la senal que la de
  post-entrega habria usado. El fix compensa por deadline, no desacopla contadores. Dentro del
  `out_of_scope` declarado; lo registro para que nadie lea el AC2 como que la inanicion de la senal
  quedo eliminada.

## 10. Anomalia de estado (DECISION-0018), fuera del codigo

`TASK-0324` esta `in_review` y `CLAIM-20260807-Codex-TASK-0324` sigue **activo** a nombre de Codex
sobre `Area_comun/tasks/TASK-0324-*.md`, `scripts/harness/peer_mailbox_cron.ps1`,
`scripts/test_exec_lease_harness.py` y las rutas de estado. AGENTS.md s.7: "A task owner that moves
a task to `in_review` or `done` must release its active claim in the same coordination step. A
reviewed task must not retain an active claim from its owner." No he tocado esas rutas. El mismo
patron se observa en TASK-0322 y TASK-0325, que tambien estan `in_review`; no los he revisado.

## 11. Veredicto

**CHANGE-REQUIRED.**

Cuatro de los cinco AC estan verdes y probados por comportamiento sobre el commit exacto en clon
limpio: AC1 (reproduccion), AC2 (coherencia con la politica de la otra rama, verificada en el bucle
real), AC3 (sin progreso muere; el tope duro es absoluto) y AC5 (sin regresion, gates exit 0). El
arreglo es correcto y esta vivo.

Lo que falla es el **AC4**: el negativo permanente no cae ante un mutante del harness que ignora la
extension heredada en el camino vivo, y ese mutante reproduce el defecto original medido por
comportamiento. El contrato ata el helper y una subcadena; no ata el efecto. Con el helper solo, la
tarea no arregla nada -- el valor esta en las tres lineas de cableado, y son las que quedan sin
proteger.

No cierro sobre un contrato que un retroceso real sobrevive.

### Bucle de arreglo esperado

1. **Remediacion (Codex, maker):** que `NEG-HARNESS-POST-DELIVERY-PROGRESS-DEADLINE` ejercite el
   CAMINO VIVO y declare un boundary que muera cuando el cableado se vuelve inalcanzable. La
   maquinaria ya esta en el repo y es barata: el mismo idioma de extraccion por AST que usan las
   sondas actuales sirve para tomar el `WhileStatementAst` que contiene `POST_DELIVERY_WINDOW_START`
   y ejecutarlo con reloj comprimido; mi replay completo tarda ~11 s por corrida. Alternativa minima
   aceptable si se prefiere no ejecutar el bucle: un segundo mutante que neutralice la RAMA del
   cableado (no su texto) y exija que el test caiga. La primera es la honesta; la segunda cierra el
   agujero concreto que he demostrado.
   Sugiero ademas corregir el numero de R1 en el boundary y en el handoff (02:59:00, no 02:55:40),
   y considerar imprimir el plazo heredado de post-entrega en la linea de log de la rama principal
   (R2) -- esto ultimo, si se juzga fuera de alcance, que quede como tarea propia.
2. **Gates afectados a recomputar en clon limpio y por exit code:**
   `test_exec_lease_harness.py`, `check_falsification_contracts.py --root . --inventory`,
   `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
   `protocol_replay.py --check-drift`, `git diff --check` y `git status --short` vacio.
3. **Re-juicio mio ANTES del commit de cierre**, sobre el commit de remediacion exacto. Verificare
   en particular que el nuevo boundary MUERE con mi mutante de codigo muerto (`$false -and ...`),
   no solo con el mutante del helper.
4. **Maximo 2 iteraciones.** Si tras la segunda el negativo sigue sin cubrir el camino vivo, escalo
   al operador humano en lugar de seguir iterando.

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
