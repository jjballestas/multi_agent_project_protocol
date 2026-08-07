---
artifact: Analista-TASK-0324-post-delivery-progress-deadline-verdict-r2
task_id: TASK-0324
reviewer: Analista
role: checker (maker != checker)
verdict: OK-CLOSABLE
iteration: 2 de 2 (re-juicio)
implementation_commit: 4e07455c119641902451ca5ea789d894b84b5ba0
protocol_head: 6253c5f7b0babe3b6607be3582ea7428ec4f4b04
supersedes: Analista-TASK-0324-post-delivery-progress-deadline-verdict
created_at: 2026-08-07T11:47:00+02:00
---

# Veredicto Analista -- TASK-0324, re-juicio sobre la remediacion

Hora local del sistema: 2026-08-07 11:47 (UTC+2).

## 1. Ancla canonica

- Commit de remediacion revisado: `4e07455c119641902451ca5ea789d894b84b5ba0`.
- HEAD del protocolo al escribir: `6253c5f7b0babe3b6607be3582ea7428ec4f4b04`, identico a `origin/main`.
- Ningun commit posterior a `4e07455c` toca `scripts/harness/peer_mailbox_cron.ps1` ni
  `scripts/test_exec_lease_harness.py` (verificado con `git log --name-only 4e07455c..HEAD`), asi
  que el codigo juzgado es el que hay hoy en `main`. El handoff se corrigio despues, en `a8cc5284`.
- Alcance declarado por el Arquitecto: SOLO el hub. SIN PRODUCTO EN ALCANCE. No he ejecutado ningun
  `npm test` de Nova ni de Zeus. No he revisado 0320, 0322, 0325 ni 0326.
- Clon limpio detached bajo el scratch root de la instancia (DECISION-0104):
  `D:/Aegis_Scratch/multi_agent_project_protocol/r0324r2/cc`, `git checkout --detach 4e07455c`,
  `git status --short` = 0 lineas. TODOS los gates, mutantes y replays se ejecutaron ALLI. Tras cada
  mutante restaure con `git checkout --` y verifique `git status --short` = 0 lineas; el driver aborta
  si el clon queda sucio.

## 2. Gates recomputados por exit code, en el clon limpio

| Gate | exit |
|---|---|
| `python scripts/test_exec_lease_harness.py` (17/17, 3 corridas) | 0 / 0 / 0 |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 |
| `python scripts/validate_collaboration_state.py --root .` | 0 |
| `python scripts/scan_encoding.py --root .` | 0 |
| `python scripts/scan_domain_neutrality.py --root .` | 0 |
| `python runtime/protocol_replay.py --check-drift --root .` -> `verdict=CLEAN up_to_seq=7417` | 0 |
| `git diff --check` | 0 |
| `git status --short` | 0 lineas |

Estado canonico del arbol vivo antes de revisar: `validate_collaboration_state.py` exit 0.

El runner de este contrato SI se ejecuta en CI: `.github/workflows/validate.yml:238` corre
`python scripts/test_exec_lease_harness.py`. Verificado por lectura del workflow del commit, no por
el inventario.

## 3. Lo que pediste, punto por punto

### 3.1 Que el mutante de codigo muerto que sobrevivia ahora MATE (tu punto 1)

Lo aplique yo, con mi propio driver, sobre el fichero embarcado del clon limpio:
`if ($null -ne $postDeliveryDeadlineUtc) {` -> `if ($false -and $null -ne $postDeliveryDeadlineUtc) {`.
La sentencia de cableado queda byte a byte identica; solo su guarda pasa a ser inalcanzable.

    exit=1  MATADO
      assert live["post_delivery_timeout_fired"] is False
      AssertionError

Muere, y muere por la asercion correcta: la que dice que la fuente EMBARCADA no dispara el corte de
post-entrega. El agujero que documente en la primera vuelta esta cerrado.

Detalle util para quien lo lea despues: cuando el mutante ya esta en la fuente, el `source.replace`
interno del test cae sobre la SEGUNDA ocurrencia (la del ternario de la linea de log), asi que el
`dead_wiring` interno sigue disparando y pasa; quien mata es el probe `live`. El resultado es el
mismo -- rojo -- pero conviene saber cual de las dos aserciones lo produce.

### 3.2 Que el nuevo selector no introduzca verdad vacia (tu punto 2, y tu pregunta)

Ataque el selector por tres puertas distintas. Ninguna produce verde:

**a) El marcador desaparece del bucle.** Renombre `POST_DELIVERY_WINDOW_START` -> `POST_DELIVERY_OPENED`
en el `Write-Log` real. El probe lanza `missing live supervision loop`; PowerShell sale 1; el
`assert proc.returncode == 0` de `run_powershell` convierte eso en fallo del test.

    exit=1  MATADO
      OperationStopped: (missing live supervision loop:String) [], RuntimeException

**b) Un bucle senuelo aparece ANTES en el fichero y contiene el marcador.** Inyecte una funcion con
un `while` inalcanzable cuyo texto contiene la cadena, justo antes de
`function Get-PostDeliveryDeadlineAfterProgress`, dejando el cableado VIVO. El fichero parsea
(comprobado con `Parser::ParseFile`, 0 errores). `Select-Object -First 1` se queda con el senuelo y
el test se pone ROJO sobre una fuente sana:

    exit=1  MATADO (falsa alarma, no falso verde)
      assert live["inherited_deadline_observed"] is True

**c) Senuelo + cableado muerto.** Tambien rojo, por la misma asercion.

La razon por la que esto no puede degenerar en verdad vacia no es el `throw`: es el DIFERENCIAL. El
contrato exige del MISMO bucle seleccionado dos cosas opuestas -- que con la fuente embarcada NO
dispare `POST_DELIVERY_TIMEOUT` y que con la guarda inalcanzable SI lo dispare. Ningun bucle ajeno a
esa guarda puede satisfacer las dos. Un selector equivocado siempre falla cerrado. **Respuesta a tu
pregunta: no, el nuevo selector no introduce verdad vacia; y no por suerte, por construccion.**

### 3.3 Que el contrato ate el EFECTO y no el texto

La prueba fuerte no es (a) ni (b), es esta: deje la linea de cableado **verbatim, sin tocar un byte**,
y neutralice su efecto con una asignacion posterior dentro de la misma rama
(`$postDeliveryDeadlineUtc = [DateTime]::UtcNow.AddSeconds($PostDeliveryTimeoutSeconds)`). El
`assert wiring in source` del test se satisface; el helper es intacto; el mutante declarado no aplica.

    exit=1  MATADO
      assert live["post_delivery_timeout_fired"] is False

El contrato lo caza igual. **Ata el efecto.** Eso es exactamente lo que fallaba en la primera vuelta.

### 3.4 AC3: tope duro inextensible y muerte sin progreso (tu punto 3)

Aqui NO me apoyo en el probe del maker, y digo por que: su probe **sustituye** `Get-ExecProgressState`
por un doble que devuelve `progressing=$true` una sola vez. Es decir, no ejercita el detector real ni
la forma del incidente (consumo compartido de contadores de bytes). Corri mi propio replay del bucle
vivo extraido por AST **con la funcion `Get-ExecProgressState` REAL** leyendo crecimiento de bytes
REAL en disco, reloj comprimido: deadline principal a t0+3,5 s, ventana de post-entrega 5 s,
`ProgressExtensionSeconds` 6 s, tope duro 30 s, el falso agente escribe 98 bytes por tick.

**A -- fuente embarcada, forma del incidente (escribe en los ticks 1..4 y luego calla):**

    1,073s  POST_DELIVERY_WINDOW_START timeout_seconds=5
    4,126s  EXEC_PROGRESSING reason=run_log_growing next_deadline=09:44:38.5696220Z
            hard_deadline=09:45:01.9691172Z post_delivery_deadline=09:44:38.5696220Z
    10,147s EXEC_HUNG reason=no_progress action=terminate

    post_delivery_timeout_fired = False    muere por no_progress EN el plazo concedido

**B -- misma forma, cableado convertido en codigo muerto:**

    1,066s  POST_DELIVERY_WINDOW_START timeout_seconds=5
    4,121s  EXEC_PROGRESSING ... next_deadline=09:44:50.4197622Z
            post_delivery_deadline=09:44:46.3570335Z
    6,132s  POST_DELIVERY_TIMEOUT timeout_seconds=5 action=terminate
    6,132s  EXEC_HUNG phase=post_delivery reason=no_progress action=terminate

    post_delivery_timeout_fired = True     muere 4 s ANTES del plazo que acababa de conceder

El incidente del 2026-08-07 sigue reproduciendose en B y sigue sin reproducirse en A, ahora con el
detector de progreso real. AC1 y AC2 confirmados por segunda vez, con maquinaria distinta.

**C -- progreso perpetuo (unica via de fuga indirecta por herencia):**

    1,064s  POST_DELIVERY_WINDOW_START timeout_seconds=5
    4,130s  EXEC_PROGRESSING next_deadline=09:44:57.9 hard_deadline=09:45:21.3406857Z pd=09:44:57.9
    10,156s EXEC_PROGRESSING next_deadline=09:45:03.9 hard_deadline=09:45:21.3406857Z pd=09:45:03.9
    16,166s EXEC_PROGRESSING next_deadline=09:45:09.9 hard_deadline=09:45:21.3406857Z pd=09:45:09.9
    22,177s EXEC_PROGRESSING next_deadline=09:45:15.9 hard_deadline=09:45:21.3406857Z pd=09:45:15.9
    28,192s EXEC_PROGRESSING next_deadline=09:45:21.3406857Z (== tope) pd=09:45:21.3406857Z
    34,202s EXEC_HUNG reason=hard_cap action=terminate

Tope duro precalculado a t0+33,53 s; muerte a t0+34,20 s, es decir dentro de la granularidad de un
tick (1 s) y **sin una sola extension mas alla del tope**. La herencia no abre ninguna fuga: la
ultima extension se recorta al tope exacto. AC3 verde por comportamiento.

### 3.5 El cambio de la linea de log no rompe consumidores (tu cuarto punto)

Barri el repo (solo ficheros RASTREADOS; `git grep`, no el arbol caliente con logs de `.protocol-tmp/`):

- Unico consumidor funcional: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py:950` y `:1008`.
  Ambos son comprobaciones de subcadena por CLAVE (`"EXEC_PROGRESSING" in log`,
  `"reason=run_log_growing" in log`), no por posicion.
- `git grep` de troceo posicional (`split()[`, `-split ' '`, `Split(' ')`) sobre `*.py`, `*.ps1`,
  `*.mjs`: **cero coincidencias**. Nada parsea esa linea por indice de campo.
- El resto de apariciones son prosa: veredictos, handoffs, intakes y mi propia memoria.

El campo se inserto ANTES de `message=`, que era el ultimo. Un parser posicional se romperia; no
existe ninguno en el arbol rastreado. **No rompe consumidores.** Salvedad honesta: no puedo hablar por
consumidores fuera del repo (comandos de monitor tecleados en sesion, scripts personales no
rastreados); quien tenga uno que trocee por posicion debe revisarlo.

Y el campo aporta lo que R2 pedia: en B se ve `post_delivery_deadline=09:44:46` mientras
`next_deadline=09:44:50`. La divergencia que causo el incidente ahora es LEGIBLE en el log. Antes no
lo era. R2 cerrado de verdad, no de forma.

### 3.6 Sin regresion (tu punto 4)

Suite completa 3 corridas seguidas en el clon limpio: exit 0, 17/17 en las tres, 13-14 s cada una.
Todos los gates de la seccion 2 en exit 0. Los cuatro AC que di por verdes en la primera vuelta
siguen verdes, y AC1/AC2/AC3 los he vuelto a probar por comportamiento con maquinaria propia (3.4).

## 4. Bateria de mutantes: tabla completa

Todos aplicados por mi, al fichero EMBARCADO del clon limpio, ejecutando el contrato completo y
gateando por exit code. `MATADO` = el contrato se pone rojo.

| # | Mutante | Resultado | Asercion que lo mata |
|---|---|---|---|
| M1 | Guarda del cableado inalcanzable (`$false -and`) | MATADO | `live["post_delivery_timeout_fired"] is False` |
| M2 | El cableado pasa `-ExecDeadlineUtc $postDeliveryDeadlineUtc` (herencia nula) | MATADO | `wiring in source` (texto) |
| M3 | Marcador `POST_DELIVERY_WINDOW_START` renombrado | MATADO | `missing live supervision loop` -> exit 1 |
| N1 | Bucle senuelo antes en el fichero, cableado VIVO | MATADO (falla cerrado) | `live["inherited_deadline_observed"] is True` |
| N2 | Bucle senuelo + cableado muerto | MATADO | idem |
| N3 | **Cableado verbatim, efecto anulado por asignacion posterior** | MATADO | `live["post_delivery_timeout_fired"] is False` |
| M6 | El campo de log imprime siempre `none` | MATADO | `live["inherited_deadline_observed"] is True` |
| M8 | Recorte al tope duro borrado DENTRO del helper | MATADO | `healthy["clamped_deadline"] == "...02:59:00..."` |
| M7 | Recorte al tope duro borrado en la RAMA de post-entrega | **SOBREVIVE** (exit 0) | ninguna -- ver R-N1 |

## 5. Tabla vector por vector

| # | Vector pedido | Resultado | Evidencia |
|---|---|---|---|
| 1 | El mutante de codigo muerto MATA el contrato | **PASS** | s.3.1, M1 exit 1 |
| 2 | El selector nuevo no introduce verdad vacia | **PASS** | s.3.2, M3/N1/N2 -- tres puertas, tres rojos; diferencial estructural |
| 2b | El contrato ata el EFECTO, no el texto | **PASS** | s.3.3, N3: cableado byte-identico, efecto anulado, rojo igual |
| 3 | Tope duro inextensible y muerte sin progreso (AC3) | **PASS** | s.3.4 C: `hard_cap` a t0+34,20 s vs tope t0+33,53 s; A: `no_progress` |
| 3b | El incidente sigue reproduciendose con el detector REAL | **PASS** | s.3.4 B: `POST_DELIVERY_TIMEOUT` a 6,13 s vs plazo concedido 10,1 s |
| 4 | Sin regresion; 4 AC previos verdes; gates exit 0 | **PASS** | s.2, s.3.6, suite 3/3 verde |
| 5 | El campo nuevo del log no rompe consumidores | **PASS** | s.3.5, cero parsers posicionales rastreados |
| R1 | El numero del boundary corresponde al sistema | **PASS** | 02:44:00 + 900 s = 02:59:00, en boundary, probe y handoff |
| R2 | La observabilidad del plazo heredado esta restaurada | **PASS** | s.3.5, la divergencia de B es legible en el log |

## 6. Residuales declarados (ninguno bloqueante)

- **R-N1 (NUEVO, no es regresion de esta tarea).** Borrar el recorte al tope duro **de la rama de
  post-entrega** -- `if ($postDeliveryDeadlineUtc -gt $postDeliveryHardDeadlineUtc) { $postDeliveryDeadlineUtc = $postDeliveryHardDeadlineUtc }`
  -- deja la suite ENTERA en exit 0 (M7). Es un invariante sin negativo permanente: su gemelo dentro
  del helper si esta cubierto (M8 muere). Consecuencia acotada: la ventana de post-entrega podria
  rebasar su tope duro en como mucho un `ProgressExtensionSeconds`, porque para volver a extender hace
  falta que `UtcNow` supere el deadline ya rebasado y entonces la guarda
  `UtcNow -lt $postDeliveryHardDeadlineUtc` clasifica `hard_cap` y mata. **Origen: `e266d070`
  (`fix(harness): gate kills on bounded liveness`), anterior a TASK-0324** -- verificado con
  `git log -S`. No lo cuento contra este cierre; merece tarea propia.
- **R-N2 (NUEVO, cosmetico pero enganoso).** `inherited_deadline_observed` promete mas de lo que
  prueba: solo comprueba que el campo del log no sea `none`. **Medido**: con el cableado inalcanzable,
  el probe devuelve `inherited_deadline_observed=True` (el ternario de la linea 1128 es independiente
  de la guarda). Quien sostiene el contrato es la pareja `live=False` / `dead_wiring=True`. No es un
  agujero -- M6 demuestra que la asercion si mata la regresion del log -- pero el nombre invita a
  leerla como prueba de la herencia, que no lo es. Renombrarla a algo como
  `post_delivery_deadline_field_present` costaria una linea.
- **R-N3 (NUEVO, fragilidad, falla cerrado).** El selector usa `Select-Object -First 1` sin exigir
  unicidad. Si algun dia otro `while` anterior del fichero contiene la cadena
  `POST_DELIVERY_WINDOW_START` (p.ej. un lector de logs), el contrato se pone rojo sobre fuente sana
  (N1). Direccion segura, pero es una falsa alarma futura evitable con un `if ($matches.Count -ne 1) { throw }`.
- **R-N4 (NUEVO, acoplamiento al reloj, medido).** El probe del contrato depende de que el bucle
  termine antes del deadline heredado. Medido 6 veces en este equipo: bucle 1,663-1,689 s, deadline
  heredado a 2,245-2,271 s, **margen 0,570-0,584 s** (hace falta ~35% de ralentizacion del bucle para
  volverlo rojo); `ticks=15` en las 6 corridas y en las 8 previas. Estable aqui; en un runner de CI
  muy cargado es el candidato natural a intermitencia. Falla cerrado (rojo, nunca verde falso). Lo
  declaro medido, no especulado.
- **R-P1 (PREEXISTENTE, anomalia DECISION-0018 que senalo, no arreglo).**
  `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` sale **exit 1** en el clon limpio de
  `4e07455c`. La causa no tiene nada que ver con esta tarea: el banco lanza
  `peer_mailbox_cron.ps1` sin `-CoordinatorId`, que paso a ser obligatorio en `52d0a380`
  (TASK-0316), mientras que el banco no se toca desde `ccd80b71` (TASK-0301). Y **no esta cableado en
  ningun workflow de CI** (`grep mailbox_retry_cases .github/workflows/*.yml` = vacio), por eso nadie
  lo ha notado. Es el banco de regresion declarado del harness en el GO de TASK-0303. Mismo patron ya
  registrado como "contratos declarados que CI nunca ejecuta". Lo senalo al owner; no lo toco.
- **R3 (arrastrado, sin cambio).** La guarda comprueba `$postDeliveryDeadlineUtc` pero pasa
  `$postDeliveryHardDeadlineUtc`. Sigue siendo fallo seguro por binding tipado `[DateTime]`.
- **R4 (arrastrado, sin cambio, dentro del `out_of_scope`).** Las dos ramas siguen compartiendo
  `$progressOutputBytes`/`$progressLedgerBytes`. El fix compensa por deadline, no desacopla
  contadores. Nadie debe leer el AC2 como que la inanicion de la senal desaparecio.

## 7. Anomalia de estado de la primera vuelta: RESUELTA

En mi veredicto anterior senale (DECISION-0018) que `CLAIM-20260807-Codex-TASK-0324` seguia activo
con la tarea en `in_review`. Recomprobado hoy: los dos claims de Codex sobre TASK-0324
(`...-remediation-2` y `...-remediation-2-delivery`) estan `released`, y no hay **ningun** claim activo
en `CLAIMS.json`. Cerrada.

## 8. Veredicto

**OK-CLOSABLE.**

El AC4 -- lo unico que bloqueaba -- esta cumplido y lo he falsado por tres puertas distintas. El
negativo permanente ya no ata el helper ni una subcadena: ata el EFECTO en el camino vivo, y lo
demuestra el mutante N3, que deja la linea de cableado byte a byte identica y aun asi muere. El
selector nuevo no compra esa cobertura al precio de una verdad vacia: el diferencial
`live` / `dead_wiring` sobre el MISMO bucle hace que cualquier seleccion equivocada falle cerrado, y
las tres formas de romperlo que probe dan rojo. AC1, AC2 y AC3 los he vuelto a verificar por
comportamiento con el detector de progreso REAL, no con el doble del maker. R1 y R2 estan corregidos
de fondo, no de forma: el numero es el que produce el sistema, y la divergencia que mato al peer el
2026-08-07 ahora se lee en el log. Sin regresion, gates en exit 0 sobre clon limpio.

Los cuatro residuales nuevos son de calidad del contrato o preexistentes, ninguno toca la garantia
que esta tarea promete, y los cuatro quedan escritos aqui para que nadie los descubra dos veces.

Recomendacion de cierre: **cerrar TASK-0324**. Y abrir tarea propia para R-N1 (el tope duro de la
rama de post-entrega sin negativo permanente) y para R-P1 (el banco de regresion del harness roto y
fuera de CI desde TASK-0316).

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
