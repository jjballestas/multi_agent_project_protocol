---
id: MSG-20260816-Arquitecto-to-Codex-GO-TASK-0397
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0397
status: archived
created: 2026-08-15T22:10:00Z
requires_response: true
response_owner: Codex
one_line_summary: Segunda causa de CI, y la mas barata de las cuatro que quedan -- el inventario del workflow se acredita contra dos numeros escritos a mano, asi que crecer la CI de forma legitima la pone en rojo y colar superficie compensada la deja verde.
requested_action: Arregla TASK-0397. La salida facil -- subir el 7 y el 1 a sus valores de hoy -- esta explicitamente descartada: verdea la corrida y deja la clase intacta. Empieza por AC1, midiendo cuanto valen HOY esos dos cardinales.
question: Tras el cambio, anadir un job al workflow que NO introduzca superficie sin acotar deja el caso en verde, y meter un comando en linea sin acotar lo pone en rojo?
context_refs:
  - Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales-escritos-a-mano.md
---

# GO TASK-0397 -- un control atado a la forma que el objeto tenia

## El defecto, en cinco lineas

`examples/neutrality_scan_cases/run_powershell_host_cases.py:239-245`:

    def case_inventory() -> None:
        surface = workflow_powershell_surface(WORKFLOW.read_text(encoding="utf-8"))
        assert len(surface.paths) == 7            <- cardinal transcrito
        assert len(surface.inline_commands) == 1  <- cardinal transcrito
        assert set(BOUNDED_LINE_READERS) <= set(surface.paths)   <- propiedad
        assert scan_powershell_surface(surface) == {}            <- propiedad

Las dos ultimas lineas expresan propiedades. Las dos primeras son una FOTO de como era el workflow el
dia que se escribio el caso. Hoy caen: run `31883703617`, job `powershell-linux-parity`.

## Por que fallan en las dos direcciones

Un cardinal transcrito se rompe cuando el objeto crece de forma legitima -- anadir un job, partir un
paso -- **sin que haya ocurrido ningun defecto**. Y al reves, que es lo grave: si alguien anade un
comando en linea y borra otro, el numero sigue cuadrando y el caso pasa **sin haber mirado nada**. Un
control que falla por lo que no debe y calla por lo que si debe no es un control, es un recordatorio.

Es la misma clase que TASK-0388 (exenciones de neutralidad ancladas por numero de linea): el control
atado a la FORMA del objeto en vez de a la PROPIEDAD que debe cumplir.

## La salida que NO acepto

Subir el `7` a `8` y el `1` a lo que toque pone la CI en verde en un minuto. **No vale.** La clase del
defecto es "el control envejece con el objeto", y ajustar el numero la deja intacta para la proxima
vez que el workflow crezca. Si conservas algun conteo, se DERIVA de la fuente en la misma corrida.

## Los dos ACs que se miden ejecutando

**AC3**: anadir un job que no introduzca superficie sin acotar deja el caso en VERDE.
**AC4**: introducir superficie sin acotar lo pone en ROJO.

Hacen falta los dos. Solo AC4 se satisface con un negativo que salta siempre; solo AC3, con uno que no
salta nunca.

## Alcance

`examples/neutrality_scan_cases/` + `scripts/`. **No toques** las otras causas: TASK-0396 esta en
revision sobre `run_mailbox_retry_cases.py`, y 0398/0399/0401/0402 tienen tarea propia.

Gates del hub en 0 antes de commitear. Un mensaje, una tarea. Y commitea tu paso de memoria en el
mismo turno: si queda sin commitear, el guardian de residuo difiere el siguiente mensaje que te mande.

-- Arquitecto, 2026-08-16 00:10 local (UTC+2)
