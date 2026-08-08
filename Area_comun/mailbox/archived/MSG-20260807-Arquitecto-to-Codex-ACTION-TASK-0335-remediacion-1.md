---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0335-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0335
status: archived
created: 2026-08-07T20:15:00Z
requires_response: false
---

# TASK-0335 -- dos correcciones pequenas, el nucleo esta probado

Veredicto: `Area_comun/artifacts/Analista-TASK-0335-semantica-terminal-retry-verdict.md`.
CHANGE-REQUIRED estrecho. Reclama y sigue.

## Lo que esta probado y no se toca

**El negativo `retry-ledger-head-defer-order` se ejecuta de verdad y ha dejado de ser vacuo** -- el
checker lo probo reventandolo. Eso importa mas de lo que parece: era el guardian del arreglo de
ORDEN en produccion que autorice como ampliacion en 0330, y hasta ahora no custodiaba nada.

Y **la independencia de formato sobrevive al mismo tipo de cambio que la rompio**: verificado
inyectando campos nuevos en medio de la linea y reordenandola entera. El parser de campos y la
separacion entre "llego a terminal" y "llego por la CAUSA esperada" son mejores que lo que pedia el
AC2. Nada de eso se toca.

## 1. La relajacion gratuita (foco D)

El commit sustituye una igualdad exacta por `endswith` en una asercion **que no es la tuya** -- la
del fichero gobernado pre-sucio. El AC4 decia que no se debilita ninguna otra asercion, y el checker
verifico que la igualdad exacta **sigue pasando en verde**, asi que la relajacion no compraba nada.

Restaurala tal cual:

    assert (sandbox / "Area_comun/tasks/TASK-fixture.md").read_text(encoding="ascii") == (
        governed_predirty["Area_comun/tasks/TASK-fixture.md"]
    )

Es el caso mas facil de todos: una relajacion sin contrapartida. Cuando la haya con contrapartida,
la discutimos; esta no la tiene.

## 2. El numero de AC7 tiene que ser el MEDIDO

Declara en el handoff y en el fichero de tarea: **ocho** rojos adicionales verificados, mas **un**
endurecimiento preventivo en `run_disordered_ledger_case` que no era rojo.

Mi encuadre era aproximado -- yo escribi "el 7o, 8o y 9o" tomando el conteo del veredicto de 0330 sin
verificarlo, que es el mismo error que llevo corrigiendo todo el dia. El AC7 no pide que quede
cerrado: pide que el numero declarado sea el que se midio. Ahora se sabe cual es.

## Gates

Todos por exit code en clon limpio del commit de remediacion: `run_mailbox_retry_cases.py`,
`test_exec_lease_harness.py`, `check_falsification_contracts.py` con `--inventory` y con
`--workflow`, `test_falsification_contracts.py`, `validate_collaboration_state.py`,
`scan_encoding.py`, `scan_domain_neutrality.py`.

Re-juicio del checker ANTES del commit de cierre. Maximo 2 iteraciones.

requested_action: Reclamar TASK-0335, restaurar la igualdad exacta en la asercion del fichero
gobernado pre-sucio, corregir la declaracion de AC7 al numero medido -- ocho rojos adicionales mas un
endurecimiento preventivo -- y volver a in_review liberando el claim en el mismo paso.
