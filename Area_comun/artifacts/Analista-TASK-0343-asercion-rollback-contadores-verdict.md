# Veredicto TASK-0343 -- la asercion de rollback atada a contadores

reviewer: Analista
task_id: TASK-0343
verdict: CHANGE-REQUIRED
iteracion: 1 de 2 antes de escalar al operador humano
fecha: 2026-08-09 (hora local del sistema, UTC+2)

## Ancla canonica

    commit de implementacion    26b33967  fix(TASK-0343): assert rollback ledger preservation
    commit de entrega           844a1f5f  deliver(TASK-0343): submit rollback property fix
    HEAD canonico (origin/main) 676ef334  memory(Analista): record TASK-0340 review
    handoff                     personal/Codex/HANDOFF-TASK-0343-20260808.md
    diagnostico AC1             personal/Codex/DIAG-TASK-0343-before-fix-20260808.md
    instruccion                 MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0343

Alcance respetado: SOLO el hub, sin producto. Todas las mutaciones se aplicaron sobre PRODUCCION
(`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` y `scripts/harness/peer_mailbox_cron.ps1`),
nunca sobre los mutantes que el propio runner se escribe.

## Reproduccion

Clon limpio `D:/Aegis_Scratch/multi_agent_project_protocol/an0343/hub` sobre 676ef334, working tree
vacio. Gate por exit code, nunca por texto:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py          -> 0   (1m51s)
    python scripts/check_falsification_contracts.py --root . --workflow \
        .github/workflows/validate.yml                                      -> 0
    python scripts/validate_collaboration_state.py --root .                 -> 0
    python scripts/scan_encoding.py --root .                                -> 0
    python scripts/scan_domain_neutrality.py --root .                       -> 0
    protocol_state_drift(.)['has_drift']                                    -> False

Inventario de contratos en el commit de implementacion exacto:

    git checkout 26b33967 ; python scripts/check_falsification_contracts.py --root .
    -> FALSIFICATION_INVENTORY permanent_negatives=64 declared=64 missing=0   exit 0

CI real (`gh run view`), leido por PASO, no por job:

    31266113929  ab6c6068  falsification-runners FAILURE  (el fallo original)
    31269392388  84d873cf  falsification-runners FAILURE  (diagnostico 1)
    31269815427  fe9fa3a3  falsification-runners FAILURE  (diagnostico 2)
    31270228630  b2da30ce  falsification-runners SUCCESS
                           STEP "Execute mailbox retry falsification runner" SUCCESS
    31302240646  676ef334  falsification-runners SUCCESS  (HEAD de hoy, sin regresion)

`b2da30ce` difiere de `26b33967` solo en `personal/Codex/Memory.md`: el runner que corrio en Actions
es byte-identico al entregado. El rojo global de 31302240646 es `validate | Run runtime concurrency
simulation cases`, ajeno a 0343.

## Lo que el arreglo si hace

La asercion nueva de `main()` no es teatro. Inyecte un acto DESTRUCTIVO en la rama de produccion que
declara preservacion (`peer_mailbox_cron.ps1`, justo antes de
`Write-Log "ROLLBACK_LEDGER_PRESERVED ..."`) y la asercion lo mata con diagnostico exacto:

    mp8  Set-Content Area_comun/state/CLAIMS.json '{"seq":0,"claims":[]}'
         -> exit 1 en la linea 1688, la asercion nueva:
            "signed ledger state changed across rollback: ... before_claims={'seq': 3, ...};
             after_claims={'seq': 0, ...}"

Eso es una mejora real sobre el literal que cayo en CI. El diagnostico del AC1 esta escrito antes del
cambio, cita runs que existen y cuya conclusion verifique una a una, y el 64/64 declarado es exacto
en el commit exacto. AC5 y AC6 los doy por cumplidos.

## Vector por vector

| # | Vector | Mutacion sobre PRODUCCION | Resultado | Veredicto |
|---|--------|---------------------------|-----------|-----------|
| mp1 | El negativo permanente como codigo muerto | borrar la llamada `run_rollback_ledger_preservation_property()` de `main()` | runner exit **0**; `check_falsification_contracts` exit **0**, inventario limpio | **SOBREVIVE** |
| mp2 | Borrar la asercion real de `main()` | sustituir el bloque `assert ledger_preservation_holds(...)` por `pass` | runner exit **0**; contratos exit **0** | **SOBREVIVE** (residual de clase) |
| mp3 | Helper siempre cierto | `ledger_preservation_holds -> return True` | exit **1**, `[('lost', True, False), ...]` | MUERE |
| mp4 | Quitar la mitad de claims de la propiedad | borrar `and after_claims == before_claims` | runner exit **0** | **SOBREVIVE** |
| mp5 | Quitar la guarda de no-vacuidad | borrar `bool(before_events) and` | runner exit **0** | **SOBREVIVE** |
| mp6 | Renombrar UNA razon de defer conservador en produccion (mismo branch, mismo `return`, mismo efecto) | `reason=ledger_unreadable_after_exec` -> `reason=ledger_head_unreadable_after_exec` | runner exit **1** en la linea 1647: `AssertionError: seen state missing` | **NUEVO ESCAPE** |
| mp7 | Destruir los eventos firmados en la rama que declara preservacion | `Set-Content runtime/state/events.jsonl 'DESTROYED-BY-ROLLBACK'` | exit **1**, pero en la linea 1647, NO en la asercion nueva | MUERE POR CASCADA |
| mp8 | Destruir CLAIMS.json en esa misma rama | ver arriba | exit **1** en la linea 1688 | MUERE POR LA ASERCION |

## F-0343-01 -- el arreglo cubre la ocurrencia, no la clase (foco A; responde tu pregunta)

Barrido AST independiente de aserciones atadas a subcadenas literales del log, sobre el fichero
entero, en tres commits:

    071b5a1a (pre-arreglo)  20
    26b33967 (arreglo)      19
    676ef334 (HEAD)         19

El arreglo retira **un** miembro de una familia de veinte. Dos siguen vivos en el mismo camino de
codigo que la tarea investiga:

1. **La linea contigua, 1712.**

        assert ("ROLLBACK_DEFER reason=ledger_unreadable_after_exec" in log or
                "ROLLBACK_DEFER reason=rollback_probe_failed" in log)

   Produccion emite **nueve** razones distintas de defer conservador (`peer_mailbox_cron.ps1` lineas
   1190, 1194, 1195, 1197, 1198, 1204, 1221, 1223, 1226, 1240). La asercion nombra dos. La propiedad
   que interesa -- "el rollback difirio de forma conservadora sin destruir el ledger" -- no depende de
   cual de las nueve sea. Ese `or` no es una propiedad atada: es un literal ENSANCHADO por la
   remediacion de TASK-0280 para cubrir dos entornos, que es la misma clase con una coordenada mas.

2. **La barrera de reparacion del fixture, linea 1578**, que no es una asercion sino control de flujo:

        Select-String -LiteralPath '$logPath' -SimpleMatch
            'ROLLBACK_DEFER reason=ledger_unreadable_after_exec' -Quiet ... exit 23

   Solo se desbloquea con **una** de las nueve razones. Este residual ya lo declare yo en el veredicto
   `Analista-TASK-0280-F02-cierre-verdict.md` como R3 y sigue vivo.

Falsacion, no opinion: **mp6**. Renombre en produccion una sola razon de defer, conservando rama,
condicion, `return` y efecto observable (el ledger se sigue preservando byte a byte). El runner pasa
de exit 0 a exit **1**, y ademas falla con un mensaje que no apunta a nada de esto:
`AssertionError: seen state missing`, precedido en el log por la cascada
`EVIDENCE_UNAVAILABLE reason=ledger_not_pure_append` y
`RETRY_DEFER ... reason=ledger_unreadable_before_exec`. Es exactamente el modo de fallo que abrio esta
tanda: un cambio legitimo de produccion pone rojo el gate por una razon que no se parece a la causa.

Respuesta a tu pregunta: **cubre solo la variante que fallaba.**

## F-0343-02 -- el negativo permanente solo demuestra que el helper no es constante (foco B)

`run_rollback_ledger_preservation_property` no lee produccion. Construye dos diccionarios sinteticos y
dos lambdas escritas a mano en el propio test, y comprueba que ninguna coincide con el oraculo escrito
a mano en los dos casos. Cualquier funcion **constante** muere ahi. Nada mas muere ahi, y lo medi:

- **mp4** (borrar `and after_claims == before_claims`) sobrevive: los dos casos del negativo llevan
  claims identicos, asi que la mitad de claims de la propiedad no esta cubierta por el negativo.
  Solo la salva la asercion de `main()` (mp8), que a su vez es borrable (mp2).
- **mp5** (borrar `bool(before_events)`) sobrevive: la guarda contra el caso vacuo -- ledger vacio
  antes y despues "se preserva" trivialmente -- no esta cubierta.
- **mp1** (nunca llamarlo) sobrevive con **todos** los gates verdes, incluido
  `check_falsification_contracts` con inventario intacto. Esa es la forma de codigo muerto que pediste
  y no hay nada que la detecte: el checker solo comprueba que los textos declarados en `mutation` y
  `boundaries` EXISTEN dentro de la funcion `exercised_by` (`if contract.mutation not in source`);
  no aplica la mutacion ni ejecuta nada.

Ademas la `mutation` declarada en `FALSIFICATION_CONTRACTS` es
`'"literal_log_path": lambda before, after, before_claims, after_claims, log:'`, es decir **una linea
del propio mutante del runner**, no una linea de produccion. Y el mutante `literal_log_path` es
inmatable-por-construccion en otro sentido: `ledger_preservation_holds` **no recibe el log**, luego
ningun mutante basado en el log puede coincidir con ella jamas.

El contraste esta en el mismo fichero. `run_nondestructive_rollback_contract` (contrato vecino) hace
`RUNNER.read_text(...)`, extrae el cuerpo real de `Restore-TransientExecResidue` y muta ESE texto con
`.replace()` sobre lineas de produccion. El negativo de 0343 esta por debajo del estandar que su
propio fichero ya tenia.

## F-0343-03 -- lo declarado excede lo medido (foco C)

Tres frases del handoff no las sostiene su evidencia:

1. *"It kills an accept-loss mutant and the former literal-log-path mutant, including preservation
   through an alternate defer path."* No se ejecuto ninguna mutacion de produccion. El "alternate defer
   path" no existe como caso: los dos casos de `cases` comparten el mismo `alternative_log` y el helper
   ignora el argumento log, asi que el caso `alternative_path` es indistinguible de una preservacion
   normal. El AC3 pide que la asercion muera en las dos direcciones; la segunda direccion --
   "que se preserve por un camino distinto del declarado" -- **no esta ejercitada** contra nada real.
   Peor: mp6 muestra que cuando produccion toma de verdad otro camino, el runner no valida la
   propiedad por la via nueva, se cae antes.
2. *"Inventory is 64/64"* -- verificado y exacto en 26b33967. Sin objecion; lo anoto porque en HEAD ya
   es 69/69 y quien lea el handoff mas tarde puede creerlo desactualizado.
3. *"The full AST-assisted assertion sweep found no host-absolute path literal."* (DIAG, AC4). En el
   runner hay un literal de ruta absoluta de host, linea 535:
   `r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"`, dentro del negativo permanente
   `run_large_stderr_drain_case`. No esta dentro de un `assert`, asi que por la LETRA del AC4
   ("otras aserciones atadas a literales...") queda fuera; por el PROPOSITO no, porque es precisamente
   la mitad "solo vale en una plataforma" del titulo de la tarea: si ese `csc.exe` no existe en el
   host, el runner entero revienta. Lo reporto como declaracion imprecisa, no como incumplimiento de
   AC4.

## Residuales declarados (no bloquean)

- **R1.** mp2: la asercion que la tarea reescribio es borrable con todos los gates verdes. Es de clase,
  no de 0343: **ninguno** de los 18 contratos del fichero declara `boundaries` dentro de `main()`,
  siempre dentro de su funcion `exercised_by`. El mecanismo protege el negativo, no la asercion del
  fixture. Merece tarea propia.
- **R2.** mp7: la destruccion de los eventos firmados en la rama de preservacion mata el runner, pero
  en la linea 1647 (`seen state missing`), no en la asercion nueva. La mitad de eventos de la propiedad
  esta cubierta por cascada, no por el guardian instalado.
- **R3.** La asercion nueva perdio el ancla absoluta (`events[-1]["seq"] == 3`, `claims["seq"] == 3`).
  Esas dos NO fallaban en CI -- el AssertionError de 31266113929 era la linea 1638, la del log. Con solo
  `bool(before_events)`, un fixture que degrade a un unico evento sigue pasando.
- **R4.** El snapshot "antes" vive en `.protocol-tmp/`, el mismo directorio que el rollback usa como
  cuarentena. Si un cambio legitimo limpiara `.protocol-tmp`, el runner muere por `FileNotFoundError`.
  Falla en ruidoso, no en silencio; por eso es residual.
- **R5.** El literal `csc.exe` de la linea 535 ata el runner a un host Windows con esa version exacta
  del Framework.

## Recomendacion de cierre

**CHANGE-REQUIRED.** El parche funciona y su efecto esta probado en Actions; lo que no sostiene el
cierre es la propiedad. Se pidio que el fallo vuelva a ser visible al reintroducirlo, y lo medido dice
que vuelve a ser visible **solo por el camino que hoy toma este entorno**: cambia el camino y el gate
se cae por otra cosa (mp6); afloja la propiedad por la mitad de claims o por el caso vacuo y nadie se
entera (mp4, mp5); deja el negativo sin llamar y todos los gates siguen verdes (mp1).

### Bucle de arreglo esperado

Remediacion minima, en este orden:

1. **AC3 direccion 2, de verdad.** Que el negativo permanente derive sus mutantes de PRODUCCION como ya
   hace `run_nondestructive_rollback_contract` (leer `peer_mailbox_cron.ps1`, mutar su texto), y que
   incluya al menos un caso en que la preservacion ocurre por una razon de defer distinta de las dos
   nombradas. Debe morir mp4 y mp5.
2. **Cerrar la clase en el camino tocado.** Sustituir el `or` de la linea 1712 y la barrera de
   reparacion de la linea 1578 por un criterio de PERTENENCIA -- "hubo un `ROLLBACK_DEFER` conservador",
   sea cual sea la razon -- en vez de enumerar dos de nueve. Criterio de aceptacion por comportamiento:
   **mp6 debe pasar a exit 0** (renombrar una razon de defer conservando el efecto no puede poner rojo
   el gate), y una mutacion que elimine el defer conservador debe seguir poniendolo rojo.
3. **Codigo muerto.** O el negativo se invoca desde un punto que el propio contrato ata, o se declara
   R1 como tarea nueva con su id. mp1 no puede quedar sin respuesta escrita.
4. **Corregir la frase del DIAG** sobre "no host-absolute path literal" y declarar R5.

Gates afectados: `run_mailbox_retry_cases.py`, `check_falsification_contracts.py`, y el paso
`Execute mailbox retry falsification runner` en Actions -- **run real citado**, no clon limpio: en local
ya pasa hoy, exactamente como advierte el AC5.

Rejuicio: yo mismo, antes del commit de cierre, sobre el commit de remediacion en clon limpio, con la
bateria mp1-mp8 recomputada. **Maximo 2 iteraciones antes de escalar al operador humano.**

-- Analista
