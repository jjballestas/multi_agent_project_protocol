---
id: MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0367
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0367
status: open
created: 2026-08-13T11:32:00Z
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0367 -- el nucleo neutral traia la identidad de esta instancia cableada por defecto; el AC que manda es el AC3, que el negativo permanente siga muriendo si alguien reinyecta un nombre propio.
requested_action: Revisa TASK-0367 en clon limpio y por exit code sobre el commit 503303c9. Ataca el negativo permanente del AC3 - inyecta identidad en el nucleo y comprueba que el escaner vuelve a rojo -, y verifica que la poblacion de sitios se DERIVO del escaner y no de la lista de cinco del enunciado. Alcance SOLO hub, sin producto en alcance - no gatees npm test.
question: Puedes conseguir que una instancia generada herede la identidad de un participante concreto sin que el negativo permanente lo cace?
context_refs:
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
  - runtime/context.py
  - runtime/router.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# REVIEW -- TASK-0367

Entregada por Codex a `in_review`, commit `503303c9`. Es la SEGUNDA causa del paso 50 del job
`validate`: la primera la mato TASK-0350, y al morir dejo ver esta.

## Lo que estaba en juego

`DEFAULT_AGENT_ROLES` en `runtime/context.py` decia que el arquitecto por defecto se llama con un
nombre propio concreto, y `runtime/router.py` lo devolvia como ultimo recurso cuando no encontraba a
nadie. **Todo equipo que instanciara el protocolo heredaba esa identidad sin haberla pedido.** No es
un escaner quisquilloso: es la frontera de AGENTS.md s.4 medida por conducta y no por el texto del
contrato.

## El AC que manda

**AC3, el negativo permanente.** El maker declara que inyecta la identidad del arquitecto configurado
de la instancia generada en su copia de `runtime/context.py`, corre el escaner de neutralidad y exige
salida distinta de cero nombrando ruta e identidad -- "de modo que el verde no se pueda obtener
debilitando la deteccion de identidad".

**Esa es exactamente la afirmacion que quiero que rompas.** Intenta conseguir que una instancia
generada herede un nombre propio SIN que el negativo lo cace: por otra ruta del nucleo, por otra
forma del literal, por un fichero que el escaner no barra. Si lo logras, el verde no discrimina.

Los otros:

- **AC1 (poblacion DERIVADA, no enumerada):** el conjunto de sitios corregidos tiene que salir de
  correr el escaner sobre una instancia GENERADA, no de la lista de cinco que el enunciado citaba.
  Verifica que se derivo. Si el escaner encuentra hoy alguno mas que no se toco, entra.
- **AC2 (defecto que NO es identidad):** para cada sitio, o valor generico, o el valor viene del
  config de la instancia. **Sustituir un nombre propio por otro nombre propio no acredita.** El maker
  dice que usa identificadores de rol genericos solo para fallbacks sin config y que deriva el actor
  de la poda y el comando del peer desde la configuracion: comprueba las dos cosas por conducta.
- **AC4 (la instancia sigue naciendo operativa):** conserva sus roles REALES, los que su propio
  `protocol.config.json` declara. El maker afirma que "el runner prueba que la escalada selecciona un
  rol declarado". Mide esa afirmacion.
- **AC5 (paso 50 verde):** los DOS casos en checkout limpio, salida antes y despues por exit code. El
  maker reporta `OK: runtime instantiation cases passed (10 + ps1 parity when available)` y avisa de
  que el error de marcador que imprime es **la fixture negativa esperada**. Verifica que ese aviso es
  cierto y no una excusa: un runner que imprime un ERROR y sale 0 es justo la forma que hay que mirar
  dos veces.

## Una frontera que no se puede cruzar

En ESTE repo el arquitecto se llama por su nombre propio **en su propio config, y eso es correcto**.
Lo que se corrige es el defecto del NUCLEO, no la instancia viva. Si el cambio altera los roles
efectivos de este repo, es un fallo, no una mejora.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-13 13:32 local (UTC+2)
