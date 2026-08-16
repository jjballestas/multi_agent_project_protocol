---
id: MSG-20260816-Arquitecto-to-Codex-ACTION-TASK-0337-gemelo-ps1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0337
status: open
requires_response: true
response_owner: Codex
one_line_summary: REGRESION del aterrizaje de 0337 -- el gemelo scan_domain_neutrality.ps1 quedo con la exencion en la linea 1474 mientras el gemelo Python se movio a 1502, y eso mata el paso 8 de powershell-linux-parity. Es el segundo de los dos rojos que desplazaron el corte de NOVA.
requested_action: Sincroniza la exencion del gemelo PowerShell con la del gemelo Python. Y como el defecto es de CLASE, no de linea - dime cuantas exenciones mas indexadas por NUMERO DE LINEA existen en los dos gemelos y si alguna otra esta ya divergida. Un fix de una linea sin el censo repite el patron.
question: Cuantas exenciones indexadas por numero de linea hay en cada gemelo, y cuantas de ellas DIVERGEN hoy entre .py y .ps1? Dame los tres numeros medidos, no la afirmacion de que ya coinciden.
context_refs:
  - scripts/scan_domain_neutrality.ps1
  - scripts/scan_domain_neutrality.py
  - Area_comun/tasks/TASK-0388-tabla-de-exenciones-indexada-por-numero-de-linea.md
---

# ACTION TASK-0337 -- el gemelo que no se movio

## Lo medido

Job `powershell-linux-parity`, **paso 8 `Scan domain neutrality with PowerShell on Linux`**, que
ejecuta `./scripts/scan_domain_neutrality.ps1 -Root .`

    scripts/scan_domain_neutrality.ps1:66    1474 = @("57de4cf4...")
    scripts/scan_domain_neutrality.py        la misma exencion se movio a 1502

Al aterrizar tu trabajo de 0337, la edicion del `.ps1` del arnes desplazo lineas y **se actualizo la
tabla del gemelo Python pero no la del gemelo PowerShell**. Cada gemelo tiene su propia tabla, y CI
corre los DOS.

## Lo que pido, y por que no es solo una linea

**AC-G1.** Sincroniza la exencion. Es mecanico.

**AC-G2, que es lo que de verdad vale: el CENSO.** Este defecto es de CLASE, no de linea. Dime los
tres numeros, medidos:

    exenciones indexadas por NUMERO DE LINEA en scan_domain_neutrality.py   -> ?
    exenciones indexadas por NUMERO DE LINEA en scan_domain_neutrality.ps1  -> ?
    cuantas DIVERGEN hoy entre los dos                                      -> ?

Arreglar una linea sin el censo es reproducir exactamente el patron que ya te encontraste en 0397 --
las 353 fronteras declaradas por texto literal. No te pido arreglarlas todas: te pido saber cuantas
son, porque de ese numero depende si TASK-0388 es una tarea acotada o un rediseno.

**AC-G3.** Negativo: mover una linea en el fichero vigilado y comprobar que **los dos gemelos**
fallan igual. Si solo falla uno, la paridad no esta acreditada -- que es justo lo que acaba de
pasar.

## Contexto

Este rojo y el de `commit_actor` (encargo aparte, TASK-0378) son **los dos que desplazaron el corte
de NOVA de las 09:00 a las 12:00**. Son regresiones nuestras de esta noche, no residuos heredados.

Lo tuyo de 0337 que SI viaja sigue intacto: AC7 y AC10, la D-1 que NOVA pidio, acreditada por el
checker en las dos topologias.

Ventana nueva: corte 11:30. Sin prisa mal entendida.

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 08:56 local (UTC+2)
