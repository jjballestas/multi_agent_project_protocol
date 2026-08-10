# Veredicto TASK-0343 r3 -- el detector encuentra el nodo, y el negativo que lo certifica sale del mismo predicado

reviewer: Analista
task_id: TASK-0343
verdict: CHANGE-REQUIRED
iteracion: 3 (autorizada por el operador; la r2 declaro presupuesto agotado)
fecha: 2026-08-10 19:45 (hora local del sistema, UTC+2)

## Ancla canonica

    commit bajo revision      179ef523  memory(Codex): persist TASK-0343 delivery   (ancla citada)
    implementacion            4cfd1b03  fix(TASK-0343): require main rollback assertion
    HEAD canonico al emitir   30ae2bdb  memory(Analista): persist TASK-0342 r4
    instruccion               Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0343-r3.md
    veredicto previo          Area_comun/artifacts/Analista-TASK-0343-defer-por-comportamiento-r2-verdict.md

Alcance respetado: **SOLO el hub, sin producto en alcance**. Toda mutacion se aplica sobre
PRODUCCION -- `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` lineas 1792-1801 y
`scripts/harness/peer_mailbox_cron.ps1` -- nunca sobre los mutantes que el propio runner se escribe.

## Reproduccion

Dos clones limpios, ambos detached en `179ef523`, con `git status --short` **vacio verificado antes
de cada vector** (el script aborta si no lo esta) y `git checkout -- . && git clean -fd` despues:

    D:/Aegis_Scratch/multi_agent_project_protocol/an0343r3/hub    vectores emparejados con mp8
    D:/Aegis_Scratch/multi_agent_project_protocol/an0343r3/hub2   escapes solos, seis puertas

Gate por exit code, nunca por texto. Linea base sin mutar, clon limpio, `179ef523`:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0   (5m10s)
    python scripts/check_falsification_contracts.py --root .         -> 0
    python scripts/validate_collaboration_state.py --root .          -> 0
    python scripts/scan_encoding.py --root .                         -> 0
    python scripts/scan_domain_neutrality.py --root .                -> 0
    python -m compileall -q examples/.../run_mailbox_retry_cases.py  -> 0
    TASK0343_MAIN_ASSERTION baseline=1 coordinate=1 order=1 format=1 deleted=0

Estado canonico del hub al emitir (arbol vivo en `30ae2bdb`), sano antes de revisar:

    python scripts/validate_collaboration_state.py            -> 0   OK: collaboration state is valid.
    python runtime/protocol_replay.py --check-drift --root .  -> 0   verdict=CLEAN up_to_seq=8623
    python runtime/gate.py --root .                           -> 0
    python scripts/scan_encoding.py --root .                  -> 0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .         -> 0

## Tu pregunta, contestada: un MARCADOR -- y ademas el negativo es analitico

`main_enforces_ledger_preservation` (lineas 184-202) devuelve True si y solo si existe un nodo
`ast.Assert` en cualquier punto del arbol de `main` cuyo `test` contiene una `Call` a un `Name`
llamado `ledger_preservation_holds`.

Ata tres cosas: **tipo de nodo**, **nombre del invocado** y **pertenencia a `main`**.
No ata **ninguna** de estas: que la asercion sea ALCANZABLE, que la llamada se EVALUE, que su valor
GOBIERNE el resultado, ni que sus ARGUMENTOS sean el par antes/despues.

Hay un segundo hallazgo que no estaba en tu pregunta y que es mas grave que la respuesta. El
negativo que certifica el detector -- `deleted` -- se deriva con `DeleteMainLedgerAssertion`
(lineas 238-260), cuyo `visit_Assert` usa una condicion **byte a byte identica** a la del detector:

    detector (188-202)   isinstance(node, ast.Assert) and any(
                             isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                             and child.func.id == "ledger_preservation_holds" ... )

    borrador (249-256)   if self.in_main and any(
                             isinstance(child, ast.Call) and isinstance(child.func, ast.Name)
                             and child.func.id == "ledger_preservation_holds" ... )

El mutante se deriva del **mismo predicado que lo juzga**. `deleted == False` no es un resultado
medido: es analitico. Para cualquier fuente en que la asercion sea una sentencia directa de `main`,
borrar-lo-que-el-detector-busca hace que el detector no lo encuentre, pase lo que pase con el efecto.
Es el mutante tautologico de TASK-0345 con otro traje, y es exactamente la leccion "mutar produccion,
no los mutantes del runner".

Comprobado simulando el bloque `assertion_wiring` completo fuera del runner sobre siete variantes de
produccion (`baseline / coordinate / order / format / deleted` + las dos aserciones de las lineas
279-280):

    variant                baseline coord  order  format  deleted   WIRING_ASSERTS_PASS
    V0_baseline            True     True   True   True    False     True
    V1_deleted (mp2)       False    False  False  False   False     False   <- unico kill real
    V3_if_False + pass     True     True   True   True    False     True
    V5_tautology           True     True   True   True    False     True
    V7_short_circuit       True     True   True   True    False     True
    V9_dead_nested_fn      True     True   True   True    True      False
    V4_try_swallow         ERROR IndentationError en la derivacion de deleted_source

`deleted` solo deja de ser False por dos caminos, y **ninguno de los dos habla del efecto**:

- **V9 -- asimetria detector/borrador.** El detector recorre con `ast.walk(main_node)`, que
  desciende a las funciones anidadas; el borrador es un `NodeTransformer` que pone `in_main=False`
  al entrar en cualquier `FunctionDef` anidado. Meter la asercion en un `def _unused_never_called()`
  dentro de `main` da `baseline=True` **y** `deleted=True`: el runner muere en la linea 280 con
  `{'baseline': True, ..., 'deleted': True}`. Muere, si, pero por una incoherencia entre sus dos
  mitades, no porque la asercion haga nada.
- **V4 -- codigo inparseable.** Envolver la asercion en `try/except AssertionError: pass` deja al
  borrador un `try:` sin cuerpo; `ast.unparse` emite fuente invalido y el detector revienta con
  `IndentationError`. Tambien muere, y tampoco es una medida de efecto.

## Tu mutante: la lectura 2 es la correcta

`assert not survivors, f"rollback preservation mutants survived: {survivors}"` esta en la **linea
306**, dentro de `run_rollback_ledger_preservation_property` (lineas 205-306). **No esta en
`main`.** La asercion que R1/mp2 nombra es la de las **lineas 1792-1801**. Que `baseline=1` siga
saliendo tras sustituir la de 306 por `pass` es comportamiento **correcto** del detector, no un
proxy: le preguntaste por otra asercion.

Dicho eso, tu mutante mide algo que si vale la pena declarar, y que no viste porque solo gateaste el
runner:

    RJ5_arq_survivors_pass   runner=0   contracts=1
    ERROR: retry-ledger-preservation-property: assertion boundary not found beside the test:
           assert not survivors

El runner **por si solo no defiende su propio matamutantes**. Lo cubre `check_falsification_
contracts.py`, y por **texto literal** -- el residual R2 que ya declare en la r2.

## R1 sigue vivo -- tres escapes limpios, acreditados por comportamiento

El instrumento es **mp8**: inyectar en `peer_mailbox_cron.ps1`, justo antes de
`Write-Log "ROLLBACK_LEDGER_PRESERVED ..."`, una destruccion real del ledger:

    Set-Content -LiteralPath (Join-Path $Root 'Area_comun/state/CLAIMS.json') -Value '{"seq":0,"claims":[]}'

**Control (mp8 solo, produccion intacta):** el runner muere donde debe.

    RJ1_control_mp8only   runner=1   contracts=0
    File ".../run_mailbox_retry_cases.py", line 1792, in main
    AssertionError: signed ledger state changed across rollback: ...
        before_claims={'seq': 3, 'claims': []}; after_claims={'seq': 0, 'claims': []}

La asercion **si dispara cuando esta viva**. Ese es el patron de referencia contra el que se miden
los escapes. Ahora, los tres escapes conservan el nodo, publican el saldo completo y **dejan pasar
la misma destruccion**:

    vector                        mutacion de produccion                        runner contracts saldo
    RJ2_shortcircuit_mp8   assert True or ledger_preservation_holds(...)          0       0      1/1/1/1/0
    RJA_tautology_mp8      (before, before, before_claims, before_claims)         0       0      1/1/1/1/0
    RJB_iffalsepass_mp8    if False: pass  +  la asercion reindentada             0       0      1/1/1/1/0

Y, sin mp8 -- es decir, **lo que un maker puede entregar hoy** -- los escapes pasan **las seis
puertas** en clon limpio:

    vector                      runner contracts validate encoding neutrality compile  saldo
    RJ9_baseline2 (sin mutar)     0        0        0        0         0        0     1/1/1/1/0
    RJ6_shortcircuit_alone        0        0        0        0         0        0     1/1/1/1/0
    RJ8_tautology_alone           0        0        0        0         0        0     1/1/1/1/0
    RJ7_deadfn_alone              1        0        0        0         0        0     (deleted=True)

**La prueba que no admite lectura alternativa.** Instrumento la produccion con un `print` del valor
real del predicado **en el punto exacto de la asercion**, con el cortocircuito y mp8 puestos:

    RJC_probe_shortcircuit_mp8
    ANALISTA_PROBE holds=False before_claims={'seq': 3, 'claims': []} after_claims={'seq': 0, 'claims': []}
    TASK0343_MAIN_ASSERTION baseline=1 coordinate=1 order=1 format=1 deleted=0

En la linea 1792, el ledger firmado **ha sido destruido**, `ledger_preservation_holds` vale
**False**, el saldo estructural sigue publicando `baseline=1`, y el runner sale 0 (en RJ2, mismo
vector sin la sonda; RJC salio 1 por el flaky de la linea 1806, ver residual F1 -- que ocurre
*despues* de la 1801 y por tanto no toca este resultado).

**Conclusion sobre tu pregunta:** el detector ve un **marcador** -- el nodo, no la exigencia -- y el
unico negativo que lo respalda esta derivado del propio marcador. Con el gate en verde, la asercion
de `main()` puede quedar vaciada de tres maneras distintas sin que nada lo note. **R1 sigue vivo.**

## Vector por vector -- PASS / SLIPS

| # | vector | que prueba | esperado | medido | veredicto |
|---|--------|-----------|----------|--------|-----------|
| RJ0 | linea base, clon limpio | no regresion | 6 puertas 0 | 6 puertas 0, saldo 1/1/1/1/0 | PASS |
| RJ9 | linea base, segundo clon | control independiente | 6 puertas 0 | 6 puertas 0 | PASS |
| RJ1 | mp8 solo | la asercion dispara viva | runner 1 en 1792 | runner 1 en 1792, diagnostico real | PASS |
| mp2 | borrado del nodo (derivado) | el detector lo mata | runner 1 | runner 1, saldo 0/0/0/0/0 | PASS |
| RJ2 | cortocircuito + mp8 | conserva el nodo, mata la exigencia | deberia morir | **runner 0**, saldo 1/1/1/1/0 | **SLIP** |
| RJA | tautologia + mp8 | argumentos falseados | deberia morir | **runner 0**, saldo 1/1/1/1/0 | **SLIP** |
| RJB | inalcanzable + mp8 | asercion fuera del flujo | deberia morir | **runner 0**, saldo 1/1/1/1/0 | **SLIP** |
| RJ6 | cortocircuito solo | entregable, seis puertas | deberia morir | **6 puertas 0** | **SLIP** |
| RJ8 | tautologia sola | entregable, seis puertas | deberia morir | **6 puertas 0** | **SLIP** |
| RJC | sonda + cortocircuito + mp8 | el valor real en el punto | -- | `holds=False` con saldo 1 | **SLIP acreditado** |
| RJ7 | funcion anidada muerta | asercion nunca ejecutada | -- | runner 1 por `deleted=True` | kill incidental |
| RJ4 | idem + mp8 | idem | -- | runner 1 por `deleted=True` | kill incidental |
| RJ5 | `assert not survivors` -> `pass` | el mutante del Arquitecto | -- | runner **0**, contracts **1** | fuera de R1; residual R2 |

## Lo que si consigue la remediacion, y hay que reconocerlo

- **mp2 literal muere determinista y por su propia asercion**, no por cascada: saldo
  `0/0/0/0/0` y `AssertionError` en la linea 279 con el diccionario completo.
- **La insensibilidad a coordenada, orden y formato es real y esta medida.** Esa frase del fichero
  de tarea es cierta: `coordinate` inserta 17 lineas, `order` mueve `main` al frente, `format`
  normaliza por `ast.unparse`, y los tres siguen en 1.
- **No hay listas de razones ni de formas**: el criterio es estructural, no un vocabulario. Eso es
  un avance real sobre las r1/r2.
- **Cero regresion**: linea base verde en las seis puertas, en dos clones limpios independientes.

El criterio no es debil en lo que mide. El problema es que **se publica como exigencia lo que es
presencia**, y el negativo que lo acredita no puede distinguir una de otra por construccion.

## Residuales declarados

- **R1 (vivo, de la r1).** La asercion de `main()` puede vaciarse conservando el nodo. Tres escapes
  acreditados. Clase de TASK-0341.
- **R2 (vivo, de la r2).** El contrato de `check_falsification_contracts.py` comprueba que un TEXTO
  literal exista al lado del test, no que mate nada (`RJ5`: runner 0 / contracts 1).
- **R7 (nuevo).** El negativo `deleted` se deriva con el mismo predicado que el detector: es
  analitico, no medido. Sus dos unicas formas de fallar (asimetria con funciones anidadas; fuente
  inparseable) no miden efecto.
- **R8 (nuevo, fuera de esta tarea).** Las exenciones de `scan_domain_neutrality.py` estan fijadas
  por **numero de linea absoluto** (`"lines": {1397: (...)}` para `peer_mailbox_cron.ps1`). Medido:
  insertar **una** linea en la 1216 desplaza la ocurrencia exenta a la 1398 y el gate se pone
  **rojo (exit 1)** sobre una ocurrencia que nadie toco:

        scripts/harness/peer_mailbox_cron.ps1:1398: Codex
        NEUTRALITY_UNDER_MP8_EXIT=1

  Es la misma clase coordenada-fragil por la que se abrio 0343, en otro gate. Merece ficha propia.
  (Tambien explica por que el neutrality de los vectores con mp8 no es concluyente: es un artefacto
  de mi instrumento, y por eso las seis puertas se miden con los escapes **solos**.)
- **F1 (flaky, corroborado y ampliado).** Tu aviso queda confirmado, y hay **dos** aserciones
  sensibles al tiempo, no una. En **13 corridas completas del runner en esta ejecucion**, mismo
  commit, misma maquina, hubo **2 rojos** que no son del vector medido:

        linea 1806  assert (sandbox / "ambiguous-residue.txt").exists()  "mid-log ambiguity was rolled back"   (RJC)
        linea 1023  assert "SELF_HEAL_ORPHAN_LOCK owner=TestPeer reason=missing_lease" in log                  (RJ3)

  Los dos aparecen bajo contencion de CPU (dos lotes en paralelo) y desaparecen en serie. **Ficha
  propia**: un gate que falla 2 de 13 por carga no es un gate, y ademas enmascara los vectores que
  corren detras de el (RJ3 aborto en la 1023, que esta *antes* de la 1792).
- **R3, R4, R5, R6** de la r2 siguen como estaban; no los re-medi en esta vuelta.

## AC5 -- abierto, verificado, bloqueo externo

Comprobado por mi, no citado de segunda mano:

    run 31398231909   headSha 179ef523...  (EL ANCLA)   conclusion=failure
      falsification-runners         failure  steps=0
      falsification-runners-python  failure  steps=0
      powershell-linux-parity       failure  steps=0
      validate                      failure  steps=0
    run 31397288472   headSha 1d219ccd...                conclusion=failure, 4 jobs, steps=0
    anotacion: "The job was not started because recent account payments have failed or your
                spending limit needs to be increased. Please check the 'Billing & plans' section"

**Ningun paso arranco en ninguno de los dos.** AC5 queda **sin evidencia**, por bloqueo **externo**
de facturacion, no por el codigo. No presento ese rojo como fallo de la entrega, y tampoco lo
acepto como cierre: el AC5 pide un `success` real del paso `Execute mailbox retry falsification
runner` y ese success no existe.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

No cierro R1 con el guardian tal como esta. Dos opciones, y la eleccion no es mia:

**(1) Atar el efecto por ejecucion, no la estructura por AST.** El criterio deja de preguntar "existe
el nodo" y pasa a preguntar "si la propiedad es falsa aqui, el runner muere". La forma minima que
resiste los tres escapes: derivar el mutante de **produccion** (no del predicado del detector) y
comprobar que, con el ledger realmente destruido durante el rollback, el runner sale **1 en la linea
de la asercion**. El propio RJ1 ya es ese negativo: `mp8 -> runner 1 en 1792`. Aceptacion por
comportamiento, en clon limpio y en serie: **RJ1 exit 1 en 3 de 3 corridas**, y **RJ2/RJA/RJB exit 1
en 3 de 3** (hoy salen 0). Si solo se ensancha el predicado AST, no se ha arreglado nada.

**(2) Verdad en la etiqueta.** Renombrar el saldo a lo que de verdad mide -- `main` **CONTIENE** el
nodo de la asercion de preservacion -- retirar la palabra "exige" del fichero de tarea, y dejar
**R1 declarado como residual abierto**, particionado a la clase de TASK-0341 junto con R2 y R7. Es
honesto y cuesta una vuelta corta; no cierra R1, lo hace visible.

**No recomiendo una tercera via**: ensanchar el predicado AST para tapar cortocircuito, tautologia e
inalcanzabilidad. Cada ensanche reintroduce la clase con otro traje -- es exactamente el patron
"las remediaciones reintroducen el patron", y ya hay tres formas conocidas; no hay razon para creer
que sean las ultimas.

**Bucle esperado: 1 iteracion, no 2.** La r2 ya declaro presupuesto agotado y esta es la tercera
vuelta. Gates afectados: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`scripts/check_falsification_contracts.py`, y el paso `Execute mailbox retry falsification runner`
cuando la cuenta se desbloquee. **Re-juicio mio en clon limpio ANTES del commit de cierre.** Si esa
iteracion no cierra, **escala al operador humano** con la opcion (2) sobre la mesa.

Lo que **no** bloqueo: AC1, AC2, AC4 y AC6 los doy por cumplidos; mp4, mp5, mp8 y mp13 mueren y
mueren bien, como ya dije en la r2 y tu recoges en la instruccion. AC5 queda abierto por bloqueo
externo declarado. Lo unico que bloquea el cierre es R1, y bloquea porque el criterio que lo daria
por cerrado no puede verlo.

-- Analista
