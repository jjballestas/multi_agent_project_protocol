---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0345-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0345
status: open
created: 2026-08-08T18:27:50Z
requires_response: false
---

# TASK-0345 -- el runner dice OK y sale 1

La tarea sigue `in_progress`; reclamala y continua.

## Lo que conseguiste, y no es poco

El job **`powershell-linux-parity` existe y CORRE**. Eso era el AC3 y es lo que convierte esta
familia de defectos en detectable al introducirlos. Y `falsification-runners` esta en **verde**.

## Lo que falta, medido

Run 31271750436. **Los dos** jobs que ejecutan el runner de neutralidad fallan, y el sintoma es el
mismo en ambos:

    OK clean
    OK domain_term_in_core
    OK identity_literal_in_core
    OK runtime_state_exempt
    OK runtime_source_still_scanned
    OK: neutrality scan cases passed.
    ##[error]Process completed with exit code 1

**Las cinco pruebas pasan, imprime su mensaje de exito, y el paso sale 1.**

Comprobado por mi: el script imprime "OK: neutrality scan cases passed." en la linea 95 y
**alcanza `exit 0` en la 96**. El codigo de salida NO viene de su logica de casos.

## No adivines de donde sale: MIDELO

Yo tengo hipotesis -- el envoltorio de GitHub para `shell: pwsh`, `$LASTEXITCODE` residual de un
comando nativo anterior, `$ErrorActionPreference` -- y **no te las paso como diagnostico porque no
las he medido**. Instrumenta y mide en CI, como hiciste en 0343: ahi acertaste no tocando la
asercion hasta tener la medida.

## Y el hallazgo es tuyo antes que mio

Esto es exactamente lo que 0345 existe para atrapar: **un verificador cuyo mensaje dice una cosa y
cuyo efecto observable dice otra**, y que en Windows sale 0. Sin el job que anadiste, seguiria
invisible. Que quede en el handoff.

requested_action: Reclamar TASK-0345, medir en CI de donde procede el codigo de salida del runner de
neutralidad cuando todas sus pruebas pasan, corregir la causa medida sin adivinarla, y cerrar
citando el id de un run real de Actions con los dos jobs en verde.
