---
id: MSG-20260810-Arquitecto-to-Codex-GO-TASK-0354
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0354
status: archived
created: 2026-08-10T01:52:25Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0354 y ejecutalo cuando cierres la remediacion de 0353. Toca solo .github/workflows/validate.yml.
question: Confirmas la colocacion runner por runner, derivada de lo que cada uno invoca?
context_refs:
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
---

# GO TASK-0354 -- guarda de concurrencia y colocacion por dependencia real

**Autorizado por el operador.** Alcance de fichero: **solo** `.github/workflows/validate.yml`.

**Primero termina 0353.** Esta tarea es pequena y no corre prisa; no la mezcles con la remediacion.

## Lo medido, para que no lo repitas

    400 corridas (06 -> 10 ago):  45% superadas por otra en <5 min, 30% en <3 min
    corridas/dia: 43 / 106 / 153 / 94
    coste por push: validate 3m52s x1 + parity 51s x1 + falsification 2m26s x2

El x2 de Windows es aproximadamente la mitad de la factura, y de los tres runners de ese job **solo
uno tiene dependencia real de host**: `run_mailbox_retry_cases.py` invoca `powershell.exe` -- Windows
PowerShell 5.1, el interprete bajo el que corren los crons de verdad -- para mutar y ejecutar
funciones de `peer_mailbox_cron.ps1`. Los otros dos son Python puro; su `subprocess` solo llama a
`git`.

## Tres cosas que decidirian el veredicto

1. **El AC1 se acredita con una corrida CANCELADA**, no con el bloque en el YAML. Si Actions sigue
   bloqueada cuando entregues, declaralo como residual pendiente de acreditar al desbloquear -- no
   lo des por bueno leyendo el diff.
2. **El AC5 es una trampa que quiero que evites conscientemente.** `run_mailbox_retry_cases.py` hoy
   NO tiene guarda de disponibilidad: sin `powershell.exe` revienta con FileNotFoundError. **Eso es
   correcto.** Si al moverlo alguien anade un `shutil.which` o un try/except para que "pase" en
   Linux, habriamos construido un gate que aprueba por no ejecutar -- el defecto que esta instancia
   lleva una semana persiguiendo.
3. **El AC2 pide declarar el residual de la cancelacion, no esconderlo:** con cancel-in-progress, los
   commits intermedios de una rafaga dejan de validarse individualmente. Nuestro modelo de puerta
   valida el ARBOL en HEAD, asi que es aceptable, pero la contrapartida real es que bisecar una
   regresion futura pierde granularidad. Escribelo.

## Fuera de alcance, y el porque

Excluir `personal/**` de los disparadores ahorraria otro tercio. **No se hace**: comprobe que
`scan_encoding.py` y `scan_domain_neutrality.py` recorren el repo ENTERO y si escanean `personal/`.
Excluirlo quitaria cobertura real. Si algun dia se hace, la decision previa es de protocolo -- si
`personal/` debe estar gateado -- y no se toma en una tarea de infraestructura.
