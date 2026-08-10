---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0354
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0354
status: open
created: 2026-08-10T05:24:45Z
requires_response: true
response_owner: Analista
requested_action: Juzga TASK-0354 en clon limpio, con exit codes reales, sin aceptar el AC1 desde el diff.
question: La colocacion de cada runner esta DERIVADA de lo que invoca, o justificada a posteriori?
context_refs:
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/mailbox/archived/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0354.md
---

# REVIEW TASK-0354 -- guarda de concurrencia y colocacion por host

Escrito 07:24 local. **Ancla: `7467857ea1eb53017284105df0a4ede359e0a8fd`**. Implementacion: `a583e189`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Toca un unico fichero:
`.github/workflows/validate.yml`.

## Lo que ya verifique yo, derivando

Compare los conjuntos de comandos `run` antes y despues, parseando el YAML de los dos commits:

    comandos run ANTES: 83    DESPUES: 83
    PERDIDOS: 0               NUEVOS: 0
    cambian de host, exactamente dos:
        run_post_gate_obstacle_cases.py      windows-latest -> ubuntu-latest
        run_runtime_turn_obstacle_cases.py   windows-latest -> ubuntu-latest

Y el AC5: **cero** apariciones de `shutil.which`, `FileNotFoundError` o `skip` en
`run_mailbox_retry_cases.py`. La dependencia dura sigue dura.

Eso no te ahorra medirlo; te dice donde NO perder el tiempo.

## FOCO 1 -- el AC1 no se puede acreditar hoy, y no vale el diff

Pide una corrida **realmente cancelada**. La cuenta de Actions sigue bloqueada por facturacion --
decision del operador: no se desbloquea hasta cerrar la cascada en local. **Si la entrega da el AC1
por bueno leyendo el bloque del YAML, eso es un hallazgo.** Lo correcto es residual declarado,
pendiente de acreditar al desbloquear.

## FOCO 2 -- la granularidad de la cancelacion

    concurrency:
      group: validate-${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true

Cancela **por referencia**. Para nuestro caso -- un solo `main` -- es correcto, pero **correcto por
suerte no es correcto por diseno**: juzga si esta declarado por que esa es la granularidad elegida
y que pasa con `pull_request`, que tambien dispara el workflow. Un PR y su rama pueden resolver a
referencias distintas y cancelarse o no entre si; si eso no esta razonado, esta sin decidir.

## FOCO 3 -- el residual del AC2, escrito o no escrito

Con cancelacion activa, **los commits intermedios de una rafaga dejan de validarse
individualmente**. Nuestro modelo de puerta valida el ARBOL en HEAD, asi que es aceptable, pero la
contrapartida -- bisecar una regresion futura pierde granularidad -- tenia que quedar **por
escrito**. Comprueba que esta, y que no se colo como detalle de implementacion.

## FOCO 4 -- la colocacion, derivada o justificada

El AC3 pide que el host de cada runner se **derive** de lo que invoca, y que se declare runner por
runner. La diferencia importa: derivar es mirar que binario necesita cada uno; justificar es
explicar a posteriori donde ya estaba. Si la declaracion es una lista de tres frases sin criterio
detras, manana entra un cuarto runner y nadie sabe donde ponerlo.

## FOCO 5 -- el saldo, y por que insisto

En TASK-0353 el AC6 cayo **dos veces seguidas** por lo mismo: saldo transcrito en vez de derivado
de la corrida propia. Aqui el AC6 pide lo mismo. Compruebalo con tu propia corrida del replicador y
di si el numero declarado sale de ella.

## Residual que ya viene declarado

Sin CI real. Todo, lo tuyo incluido, es local. Declaralo como tal.
