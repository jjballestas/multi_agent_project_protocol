---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0343
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0343
status: open
created: 2026-08-08T16:35:00Z
requires_response: false
---

# GO TASK-0343 -- la asercion de rollback ata contadores literales

Contrato: `Area_comun/tasks/TASK-0343-la-asercion-de-rollback-ata-contadores-y-solo-vale-en-una-plataforma.md`.
Reclamala y ejecutala. Es el **ultimo** job rojo de CI junto con 0342.

## Lo medido

Run 31266113929, job `falsification-runners`, windows-latest con pwsh:

    run_mailbox_retry_cases.py:1638
        assert "ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk" in log
    AssertionError

En local ese mismo runner sale **exit 0** -- lo verifique yo sobre el arbol vivo. Estaba enmascarada
tras la asercion de la linea 342, la que acabas de arreglar en la remediacion 5 de 0331: al pasar
aquella, esta se alcanza y cae.

## Empieza por MEDIR, y no toques la linea antes

El AC1 es una precondicion, no un tramite: **declara por escrito que valores toman de verdad
`seq_before`, `seq_after` y `proof` en cada entorno, y que los produce.**

La reparacion barata seria cambiar los numeros hasta que cuadren en las dos plataformas. Eso es
moldear la asercion al resultado y no cierra nada: la proxima diferencia de entorno la rompe otra
vez. Ata la PROPIEDAD -- que el ledger se preserve a traves del rollback -- no un literal con
contadores dentro.

## El AC4, porque es la cuarta vez

Este runner nos ha mordido cuatro veces por la misma forma: 0316, 0319, 0321 y la linea 342. Quiero
el **inventario del fichero entero**: que otras aserciones siguen atadas a literales con contadores
o rutas. Declaralas aunque no las toques.

## Si la medicion revela otra cosa, PARATE

Esta tarea toca la asercion, no lo aserido. Si al medir ves que la diferencia viene de un
**comportamiento real distinto del rollback entre plataformas**, eso es un defecto de produccion:
declaralo, para, y lo particiono yo. No lo arregles aqui.

## Cierre

Citando un run REAL de Actions con ese paso en verde. En local ya pasa hoy, asi que la evidencia
local no dice nada sobre este defecto.

requested_action: Reclamar TASK-0343, medir y declarar POR ESCRITO por que la linea difiere entre
local y CI antes de tocarla, atar la propiedad de preservacion del ledger en vez del literal con
contadores, falsarla en las dos direcciones, inventariar el resto de aserciones del fichero atadas a
literales, y cerrar citando el id de un run real de Actions con el paso en verde.
