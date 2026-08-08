---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0342
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0342
status: open
created: 2026-08-08T16:20:00Z
requires_response: false
---

# GO TASK-0342 -- la exclusion del gemelo de encoding liga la barra de Windows

Contrato: `Area_comun/tasks/TASK-0342-la-exclusion-del-gemelo-de-encoding-liga-la-barra-de-windows.md`.
Reclamala y ejecutala. Es lo que ahora bloquea al job `validate`, **detras de tu arreglo de 0340**,
que si funciono.

## Lo medido, para que no lo re-derives

Run 31266113929, job `validate` sobre **ubuntu-latest**:

    ENCODING ERRORS:
    - mojibake: runtime/memory/index.db:1

`scripts/scan_encoding.ps1:36`:

    $File.FullName.StartsWith("$directory\", ...)     <- barra INVERTIDA literal

En Linux la ruta es `/home/.../runtime/memory/index.db` y el prefijo buscado termina en `\`. No casa
nunca, la exclusion de `runtime/memory` no se aplica, el escaner lee el SQLite y grita. El gemelo
Python no lo tiene porque compara rutas RELATIVAS con barra normal.

## Lo que reconozco de tu trabajo en 0340

Tu arreglo de la dependencia **funciono**: el validador ya no crashea. Y encontraste solo el
`fetch-depth`, que yo no habia visto, iterando contra CI real. Eso es exactamente lo que el AC6
pedia. Este fallo nuevo estaba **detras**, enmascarado desde el 2026-08-02 porque un paso anterior
caia primero.

## El AC5 no es formalidad

Cierra citando un run REAL de Actions con el paso `Scan encoding with PowerShell` en verde.
**Aqui no puedes cerrarla en local**: el defecto es invisible en Windows, que es donde trabajamos.
Certificar verde desde aqui seria certificar en el unico entorno donde el fallo no ocurre.

## Es la tercera del dia, y quiero que lo declares

Misma causa de fondo que TASK-0338 (`splitlines` frente a `Get-Content`) y que el B1 de TASK-0336
(la nocion de linea de Python frente a la de bash): **atar una forma de plataforma o de lenguaje en
vez de la propiedad**. Si al arreglarla ves que las tres piden un criterio compartido, **dilo y lo
particiono yo**. No lo absorbas.

## Lo que NO es tuyo aqui

El otro job rojo -- `falsification-runners`, con la asercion
`ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk` fallando en Windows y pasando en
local -- **no entra en esta tarea**. Lo estoy contratando aparte.

requested_action: Reclamar TASK-0342, hacer que la exclusion de directorios del escaner PowerShell
no dependa de un separador concreto, verificar por comportamiento que los dos escaneres excluyen el
mismo conjunto, anadir el negativo permanente del AC4, declarar la raiz comun con 0338 y 0336 sin
absorberlas, y cerrar citando el id de un run real de Actions con ese paso en verde.
