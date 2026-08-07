# Veredicto TASK-0335 -- CHANGE-REQUIRED (estrecho): la propiedad esta bien afirmada, pero el commit debilita una asercion ajena y el inventario declarado sobrecuenta en uno

Analista, 2026-08-07 21:50 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Los focos A, B y C **PASAN**, y pasan con evidencia por comportamiento, no por
lectura. El negativo `retry-ledger-head-defer-order` **se ejecuta de verdad y ha dejado de ser
vacuo**: lo probe reventandolo. La independencia de formato **sobrevive al mismo tipo de cambio que
la rompio**, verificado inyectando campos nuevos en medio de la linea y reordenandola entera. El
foco D tiene **una violacion**: el commit sustituye una igualdad exacta por `endswith` en una
asercion que no es la suya, y la relajacion es **gratuita** -- verifique que la igualdad exacta sigue
pasando. Y respondiendo a tu segunda pregunta del foco A: de los nueve rojos declarados, **ocho eran
rojos reales y uno no lo era**; ese uno es endurecimiento preventivo legitimo, pero no un rojo.

## Anclaje

- Commit bajo revision `dbe9a508`, verificado **ancestro de `origin/main` (`e15d7778`)**.
- `git diff --stat dbe9a508 HEAD -- examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> **vacio**:
  el runner es identico byte a byte entre el commit citado y HEAD, asi que el juicio vale para los dos.
- Clon limpio en `D:/Aegis_Scratch/hub/t0335/cc` (detached en `dbe9a508`).
- Clon limpio del **padre** en `D:/Aegis_Scratch/hub/t0335/par` (detached en `dbe9a508^` = `bbe2e2fe`),
  usado como control para el inventario de AC7.
- Produccion: `git show --stat dbe9a508` toca **un solo fichero**, el runner. Produccion sin tocar. PASA.
- Sondas reproducibles: `D:/Aegis_Scratch/hub/t0335/{driver,inventory_probe,tail_probe,tail_revert,pos_revert}.py`.

## Gates recomputados por exit code en clon limpio sobre `dbe9a508`

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py                        EXIT 0
    python scripts/test_exec_lease_harness.py                                             EXIT 0  (5 PASS)
    python scripts/check_falsification_contracts.py --root . --inventory                   EXIT 0
    python scripts/check_falsification_contracts.py --root . --workflow ...validate.yml    EXIT 0
    python scripts/test_falsification_contracts.py                                        EXIT 0
    python scripts/validate_collaboration_state.py --root .                                EXIT 0
    python scripts/scan_encoding.py                                                       EXIT 0
    python scripts/scan_domain_neutrality.py --root .                                     EXIT 0

Estado canonico del arbol vivo antes de empezar: `validate_collaboration_state.py` EXIT 0.

## Foco A.1 -- el negativo del orden se ejecuta y ha dejado de ser vacuo. PASA.

Instrumente `exercise()` para imprimir, en cada llamada, los eventos `RETRY_EXHAUSTED` **parseados**
que la asercion va a juzgar. Las tres llamadas se alcanzan y las tres ven datos reales:

    EXERCISE reached: expect_any=True  expect_expected=True
      events=[{defers:3, attempts:0, elapsed_seconds:2, timeout_seconds:2, signal:watchdog,
               outcome:defer_terminal, reason:ledger_unreadable_before_exec, message:MSG-retry.md}]

    EXERCISE reached: expect_any=False expect_expected=False      (mutante de ORDEN)
      events=[]

    EXERCISE reached: expect_any=True  expect_expected=False      (mutante de CAUSA)
      events=[{defers:3, attempts:0, ..., outcome:defer_terminal,
               reason:ledger_unreadable_wrong_cause, message:MSG-retry.md}]

Que se alcancen no basta -- eso era el foco. Falsee las dos mitades **invirtiendo la expectativa**,
que es la unica forma de distinguir "afirma algo cierto" de "no afirma nada":

    meta-mutante 1: mutante de orden con expect_any_terminal=True   -> ASSERTION FAILED  (correcto)
    meta-mutante 2: mutante de causa con expect_expected_terminal=True -> ASSERTION FAILED  (correcto)

La vacuidad que senale en 0330 esta muerta. `terminal` ya no es una subcadena que ningun log
satisface: es una funcion de los eventos, y **la misma expresion da True en dos de las tres llamadas
y False en la otra**. El log del meta-mutante 1 muestra ademas *por que* el mutante no llega a
terminal, que es lo que la ampliacion de produccion de 0330 custodia:

    RETRY_DEFER defer=1 ... reason=ledger_unreadable_before_exec   (ronda 3)
    RETRY_DEFER defer=1 ... reason=ledger_unreadable_before_exec   (ronda 4)
    RETRY_DEFER defer=1 ... reason=ledger_unreadable_before_exec   (ronda 5)

Con el reseteo antes de la comprobacion, el contador **nunca escala**: se queda en 1 para siempre.
Esa es exactamente la enfermedad que el arreglo de orden evita, y ahora hay un negativo que la ve.
Y el mutante de causa llega a terminal por `ledger_unreadable_wrong_cause`, o sea que la mitad
`expect_expected_terminal` discrimina la CAUSA y no solo el hecho. Respuesta directa a tu pregunta:
**si, se ejecuta de verdad; no, ya no es vacua; si, custodia el arreglo de orden.**

## Foco A.2 -- el inventario. Ocho rojos reales, no nueve. CAMBIO REQUERIDO (declaracion).

Me pediste saber cual de las dos cosas era. Lo medi por comportamiento, no por lectura, con dos
tecnicas complementarias:

- casos **independientes del sexto rojo**: los ejecute directamente en el clon del PADRE;
- casos **acoplados a la cola**: revert de cada reparacion *una a una* sobre el commit ARREGLADO;
  si el revert pone el caso en rojo, la reparacion atacaba un rojo real; si sigue verde, no.

Resultado, reparacion por reparacion:

    bucket del maker            reparacion                              veredicto de la sonda
    --------------------------  --------------------------------------  -------------------------
    "dos aserciones             run_unstaged_residue_case (posicional)   revert -> RED (linea 888)
     posicionales mas"          run_disordered_ledger_case (posicional)  revert -> GREEN  <<< NO ERA ROJO
    "cuatro fixtures focales    run_post_delivery_timeout_case           padre -> RED (linea 948)
     sin task id/scope          run_exec_running_heartbeat_case          padre -> RED (linea 1024)
     resoluble"                 run_pre_delivery_and_liveness_cases      padre -> RED (linea 1091)
                                run_frozen_exec_with_production_...      padre -> RED (linea 1154)
    "tres roturas en la cola    fake-agent CLAIMS.json + "claims":[]     revert -> RED (linea 1520)
     principal"                 TASK-fixture.md con frontmatter/scope    revert -> RED (linea 1517)
                                governed_predirty CLAIMS.json + claims   revert -> RED (linea 1520)

    control: cola sin revertir nada, commit arreglado -> GREEN (main rc=0)

**Ocho rojos reales verificados uno por uno. El noveno no existia.** El cambio de
`run_disordered_ledger_case` a parser de campos es endurecimiento preventivo correcto -- la subcadena
`RETRY_EXHAUSTED attempts=1 signal=watchdog outcome=unconfirmed` sigue siendo contigua en produccion
hoy (linea 1358 del runner), asi que la asercion vieja pasa igual. Es la misma medicina que AC2 pide,
aplicada por adelantado; me parece bien que este, pero **no es un rojo** y contarlo como tal es
exactamente el "cuadrar el resultado" que me pediste no hacer.

Que el caso no estuviera rojo por otra razon lo deduzco de la construccion: el diff no toca nada mas
dentro de `run_disordered_ledger_case`, y con su asercion revertida al estado del padre pasa verde
sobre el arbol arreglado, cuyo estado de sandbox al entrar en ese caso es el mismo que en el padre
(ninguna reparacion anterior toca fixtures, solo aserciones).

Lo que **si** cierra: la cola posterior a la linea 1390 esta explorada y verde (la sonda de cola sola
sobre el padre da RED y sobre el arreglo da GREEN), la lista de casos invocados en `main()` es
**identica** entre padre y arreglo (`diff` vacio: no se elimino ningun caso para poner verde), no hay
`skip` ni `xfail` ni `pytest.mark` en el fichero, y el numero de `assert` sube de 118 a 121.

## Foco B -- independencia de formato. PASA, y con la prueba fuerte.

Modifique **produccion** en el clon (solo en scratch, nunca en el arbol canonico) para emitir las
tres lineas `RETRY_EXHAUSTED` con **campos nuevos inyectados en medio** y con **todos los campos
reordenados**:

    antes:  RETRY_EXHAUSTED defers=.. attempts=.. elapsed_seconds=.. timeout_seconds=..
                            signal=watchdog outcome=defer_terminal reason=.. message=..
    sonda:  RETRY_EXHAUSTED analista_probe=42 reason=.. message=.. timeout_seconds=..
                            outcome=defer_terminal attempts=.. signal=watchdog
                            elapsed_seconds=.. another_probe=x defers=..

Resultado: `head + residue + disordered` **PASAN los tres**. La asercion sobrevive a la clase de
cambio que TASK-0321 le hizo, que era el punto entero de la tarea. AC2 cumplido por comportamiento.

## Foco C -- sigue cayendo en las dos direcciones. PASA.

Cubierto arriba: meta-mutante 1 (no se alcanza terminal) y meta-mutante 2 (se alcanza por otra
causa) **hacen caer la asercion**. No esta apagada. AC3 cumplido.

## Foco D -- sin relajar. UNA VIOLACION. WARNING-real, bloqueante.

Produccion sin tocar: **si**. Ningun skip ni xfail: **si**. "Ninguna otra asercion debilitada":
**no**. En la cola de `main()`:

    -  assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii") == "peer-task-edit\n"
    +  assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii").endswith(
    +      "peer-task-edit\n"
    +  )

Esa asercion custodia que el rollback **no reescriba el fichero gobernado que el peer dejo sucio
antes del exec**. El commit le anade al fixture un frontmatter con `task_id` y `scope_routes` -- que
es justo el metadato del que depende la admision por scope de todo este hilo -- y despues **deja de
mirarlo**. Aritmetica del escape:

    contenido                        endswith(entregado)   == exacto (disponible)
    fixture integro                  True                  True
    frontmatter DESTRUIDO            True   <<< ESCAPA     False
    scope_routes REESCRITO           True   <<< ESCAPA     False

Un rollback que se cargue el frontmatter entero y conserve la ultima linea pasa el gate. Y la
relajacion es **gratuita**: sustitui `endswith` por igualdad exacta contra el valor que el propio
fixture escribe y **corri la cola completa** ->

    assert ... == governed_predirty["Area_comun/tasks/TASK-fixture.md"]     ->  GREEN (main rc=0)

O sea que no habia ninguna necesidad tecnica. AC4 dice literalmente "no se debilita ninguna otra
asercion del fixture", y esta se debilito.

## Residuales declarados (no bloqueantes)

1. `expected_terminal` no ata `message=`: un terminal emitido para OTRO mensaje satisfaria la
   condicion. No es regresion (la subcadena vieja tampoco lo ataba) y el sandbox solo tiene un
   mensaje vivo. **SUGGESTION.**
2. `retry_exhausted_events` trata como evento **cualquier** linea que contenga el token, y descarta
   los tokens sin `=`; un valor con espacios partiria el campo. Ninguna linea de produccion lo hace
   hoy. **WARNING-theoretical.**
3. La nueva asercion de `run_unstaged_residue_case` la verifique **estructuralmente** (el `while ...
   else: raise AssertionError` la hace caer por ausencia), no por mutacion de produccion. Lo declaro
   como no verificado por comportamiento.
4. Mi verificacion cubre los casos que `main()` invoca hoy. La lista es identica a la del padre, asi
   que nadie retiro un caso para poner verde; un caso que nunca se invoco sigue sin poder ponerse
   rojo, y eso es anterior a esta tarea.
5. El handoff (linea 18) y el fichero de tarea (linea 115) vuelven a citar **"8/8 runners y 48/48
   contratos ejecutados"**, que es literalmente el enunciado que mi veredicto de TASK-0330 condiciono
   mientras vivieran los nueve escapes del cableado. Aceptado tu encuadre de que eso es TASK-0336 y
   no 0335; lo dejo declarado porque son artefactos que ya estan en el estado canonico y se van a
   citar. **No bloquea aqui.**
6. Todos mis mutantes y meta-mutantes se aplicaron y quedaron **dentro de los clones de scratch**,
   nunca en el arbol canonico; el arbol vivo no fue tocado por ninguna sonda.

## Recomendacion de cierre: CHANGE-REQUIRED

El nucleo esta bien y probado. Los dos cambios son pequenos y uno de ellos ya lo tengo verde.

**Remediacion (dueno: Codex maker):**

1. Restaurar la igualdad exacta en la asercion del fichero gobernado pre-sucio -- verificada verde
   por mi:

       assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii") == (
           governed_predirty["Area_comun/tasks/TASK-fixture.md"]
       )

2. Corregir la declaracion de AC7 en el handoff y en el fichero de tarea: **ocho** rojos adicionales
   verificados, mas **un** endurecimiento preventivo en `run_disordered_ledger_case` que no era rojo.
   La declaracion es el requisito de AC7; el numero tiene que ser el medido.

**Gates afectados, todos por exit code en clon limpio del commit de remediacion:**
`run_mailbox_retry_cases.py`, `test_exec_lease_harness.py`,
`check_falsification_contracts.py --inventory` y `--workflow`, `test_falsification_contracts.py`,
`validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`.

**Re-juicio mio ANTES del commit de cierre, nunca despues. Maximo 2 iteraciones; si al cierre de la
segunda queda algun bloqueante abierto, escalo al operador humano.** Esta es la iteracion 1 de 2.

Analista.
