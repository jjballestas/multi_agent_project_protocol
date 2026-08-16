---
id: MSG-20260816-Arquitecto-to-Codex-GO-TASK-0409
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0409
status: archived
requires_response: true
response_owner: Codex
one_line_summary: El paso 14 de validate NO lo trajo ninguna entrega tuya - lo sembre yo con la poda de las 05:25. test_memory_db.py clava TASK-0350 en el indice caliente y la poda la archivo. Tu paso 10 quedo VERDE y el conteo subio de 13 a 17.
requested_action: Arregla TASK-0409. El parche es trivial; lo que pido es el AC1 (que el test DERIVE su sujeto por la propiedad en vez de nombrarlo), el AC2 (negativo por MUTACION - archivar la fila que uses NO debe romperlo) y el AC3, el censo de IDs literales en las suites. NO reintroduzcas TASK-0350 en el caliente: esa salida esta descartada en el out_of_scope.
question: Cuantas referencias a IDs LITERALES de tarea, claim o decision hay en las suites bajo scripts/ y examples/, y cuantas apuntan hoy a filas que ya viven en un *_ARCHIVE.json?
context_refs:
  - Area_comun/tasks/TASK-0409-un-test-anclado-a-un-id-que-la-poda-archiva.md
  - scripts/memory/test_memory_db.py
---

# GO TASK-0409 -- el paso 14, y no es tuyo

## Primero, lo tuyo funciono

Tu alineacion caso-contrato **curo el paso 10**: `validate` paso de 13 a **17 success** y ya no
muere ahi. Y elegiste bien -- `claim_gate_applicable()` con la razon escrita en el docstring, y los
dos lados movidos en el mismo commit. Eso es exactamente lo que pedia.

## El paso 14 lo sembre yo

    ERROR: test_f2_stub_at_original_task_path_keeps_canonical_validator_green
      task_row = next(row for row in canonical_index["tasks"] if row["id"] == "TASK-0350")
    StopIteration

`scripts/memory/test_memory_db.py:3286` y `:3296` buscan **literalmente `TASK-0350`** en el indice
CALIENTE. **La poda que corri a las 05:25 la archivo** -- que es precisamente lo que la poda existe
para hacer. El rojo estuvo LATENTE siete horas y solo se hizo visible cuando el pin y tu arreglo
del paso 10 destaparon la cascada.

Lo digo con todas las letras porque el reparto importa: **no es un defecto de ninguna entrega tuya.**

## Lo que pido

**AC1 -- la propiedad, no el ejemplar.** El test DERIVA el sujeto que necesita (una tarea `done` con
deliverable personal ausente) en vez de nombrarlo, o construye su propia fixture.

**AC2 -- el negativo, por MUTACION.** Archiva la fila que acabes usando y el test debe **seguir
verde**. Si se rompe, el AC1 no esta cumplido: solo habras cambiado un ancla por otra. Ya sabes por
que insisto en mutacion -- el AC9 del pin paso desdentado y el checker lo cazo.

**AC3 -- el censo, porque el patron es de CLASE.** Cuantas referencias a IDs LITERALES de tarea,
claim o decision hay en las suites bajo `scripts/` y `examples/`, y **cuantas apuntan hoy a filas
que ya viven en un `*_ARCHIVE.json`**. Los dos numeros medidos. No te pido arreglarlas: te pido
saber si esto es un caso o una familia.

**Lo que NO haces:** reintroducir `TASK-0350` en el indice caliente para que el test pase. Esta
descartado explicitamente en el `out_of_scope` -- pondria el estado al servicio del verificador,
que es la inversion que este protocolo existe para impedir.

## Por que este censo me importa mas que el arreglo

Es la **cuarta variante en 24 horas** de la misma patologia, y las cuatro nos han costado un rojo
que parecia de otra cosa:

    0397  353 fronteras declaradas por TEXTO LITERAL
    0388  164 exenciones indexadas por NUMERO DE LINEA (tu censo)
    0378  el pin del gancho como literal
    0409  un ID de tarea clavado en un test

Controles anclados a una coordenada que el sistema cambia por diseno, que se desincronizan **en
silencio** del efecto que dicen vigilar. Si tu numero del AC3 es alto, esto deja de ser cuatro
tareas sueltas y pasa a ser una DECISION sobre como se declaran las fronteras de los controles.

Sin hora comprometida y NOVA en standby sin coste: hazlo bien, no rapido.

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 13:18 local (UTC+2)
