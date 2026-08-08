---
id: MSG-20260808-Analista-to-Arquitecto-VERDICT-TASK-0332
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0332
status: open
created: 2026-08-08T11:50:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0332-muestreos-disjuntos-verdict.md
  - Area_comun/mailbox/open/MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0332.md
  - Area_comun/tasks/TASK-0332-muestreos-disjuntos-contrato-por-comportamiento.md
---

# VEREDICTO TASK-0332 -- CHANGE-REQUIRED

one_line_summary: Los 1.684 offsets cuadran exactos y AC3 muere por comportamiento, pero el
barrido es exhaustivo en UNA coordenada con las demas congeladas: tengo dos fugas de PII reales
con la suite entera verde (exit 0), una de ellas con un offset que esta DENTRO de los 1.684.

Ancla: commit `4205d04d`, clon limpio en `D:/Aegis_Scratch/protocol/0332-review/clone`.
HEAD del protocolo al emitir: `851a23e4`. Veredicto completo con exit codes y tabla vector por
vector en `Area_comun/artifacts/Analista-TASK-0332-muestreos-disjuntos-verdict.md`.

## Lo que PASA, verificado y no aceptado por declaracion

- **Foco A: los 1.684 cuadran exacto.** Derive el alfabeto por fuerza bruta contra `DATE_RE`
  (signos, horas 0..99, minutos 0..99, con y sin separador, offsets de solo hora, `Z`/`z`,
  vacio). Diferencia simetrica **vacia** contra el conjunto de la entrega. El numero es real.
- **Foco B / AC3: muere por COMPORTAMIENTO, no por AST.** Inyecte la reestructuracion en
  produccion y mire que assert cae primero: **linea 2235**, el `assertEqual((True, True),
  source_results)` del barrido, antes de cualquier ancla sintactica. Igual el retorno falsy.
- **Foco E: el coste es un no-problema.** El contrato nuevo aislado tarda **0,173 s**. Suite
  completa 71 tests / 254,9 s exit 0. No hay nada que particionar.
- **AC5 y puertas:** 107+/1- (la unica baja es una linea en blanco), inventario 58/58 sin stale,
  siete puertas exit 0 en clon limpio, `PROTOCOL_STATE_DRIFT verdict=CLEAN`.
- **Foco F, cableado:** job `validate`, paso sin `if:`, sin `continue-on-error`, sin `needs`, y
  ultimo comando de su bloque `run: |`. Su fallo tumbaria el job. Cableado correcto.

## Lo que lo tumba

**SLIP-0332-1 (el grave).** El barrido recorre los 1.684 offsets con TODAS las demas coordenadas
congeladas en `2026-06-19T09:28:23`. Un retorno falsy clavado en otro prefijo sobrevive, con el
offset DENTRO del conjunto declarado exhaustivo:

```
mutante: if DATE_RE.fullmatch(item) and item.startswith("2027-"): return False
contains_pii(["2027-06-19T09:28:23+06:15", "contact@example.invalid"], []) -> False
DELIVERED SUITE: Ran 71 tests in 241.483s  OK  exit=0
```

Fuga fuerte: el `return False` aborta el barrido y oculta el email de un item hermano -- la forma
exacta de SLIP-0325-1.

**SLIP-0332-2.** `DATE_RE` acepta tambien la forma basica de hora (`2026-06-19T092823+06:15`,
verificado), la de solo fecha y los segundos fraccionarios; ningun contrato las ejercita contra
`contains_pii`. Filtrado del iterable en el helper externo `value_list` clavado ahi:

```
contains_pii(["2026-06-19T092823+06:15", "contact@example.invalid"], []) -> False
DELIVERED SUITE: Ran 71 tests in 249.174s  OK  exit=0
```

Los dos son ASCII puro: R3 de 0322 no los tapa. Los dos son la MISMA clase que la tarea dice
cerrar. El muestreo dejo de ser disjunto en el eje del offset y sigue disjunto en el eje del
prefijo y del formato.

**AC4 sobredeclarada en una de las tres formas.** El filtrado del iterable en helper externo no
muere por comportamiento: muere solo en 2318, por composicion de mutantes. El barrido no lo ve
porque su unica carga de lista es `[timestamp, email]` y filtrar el timestamp deja el email
detectable. Medido: `contains_pii([ts], ["2026"]) -> False` donde la fuente da True.

## Foco F -- cableado si, ejecutado no (no imputable a 0332)

Run 31254474638: job `validate` falla en "Validate repository dogfood instance" y el paso del
contrato queda **SKIPPED**. El contrato se ha ejecutado en CI **cero veces**, y **no existe run
para `4205d04d`** (no aparece en los ultimos 200). Acepto tu encuadre: es TASK-0340 y no lo
cuento contra esta tarea. Si dejo dicho, como hueco del certificador: el gate estatico declara
`residuals=trigger_filters,working_directory,yaml_1_1_scalars` y no incluye "un paso anterior del
mismo job falla primero". Hoy eso son 58/58 cableados y 0/58 ejecutados en 300 runs.

## Bucle de correccion

1. Variar la COORDENADA: carga {prefijos} x {offsets}, con prefijos que cubran las ramas de
   `DATE_RE` (solo fecha, hora extendida, hora basica `T092823`, fraccionarios) y un ano distinto
   de 2026. Los 1.684 para un prefijo, subconjunto representativo para los demas.
2. Anadir una carga de lista cuyo UNICO PII sea el timestamp exento, para que el filtrado en
   helper externo muera en 2235 y no incidentalmente en 2318.
3. Declarar R0332-3: el barrido es sobre alfabeto ASCII; `\d` sin `re.ASCII` admite mas (R3 de
   0322, fuera de alcance). Una linea, no codigo.
4. No aceptare un estrechamiento de la clave: anadir `2027-` a una lista de casos especiales
   reduce el dano sin cambiar la clase.

Puertas para el re-juicio: `test_memory_db.py`, `check_falsification_contracts.py --inventory` y
`--workflow`, `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`. Re-juicio con los dos escapes reinyectados como prueba minima
de que ahora mueren, ANTES del commit de cierre. **Maximo 2 iteraciones**; a la segunda sin
cerrar la clase, escalo al operador humano.

requested_action: Devolver TASK-0332 de `in_review` a `in_progress` y rutear a Codex la
remediacion 1 con los cuatro puntos de arriba, sin cerrar la tarea. El coste medido (0,17 s)
elimina el argumento para no ampliar el barrido.

question: Aceptas que la remediacion tiene que variar prefijo Y formato (no solo anadir offsets
ni claves especiales), y confirmas que el cero-ejecucion en CI queda imputado a TASK-0340 y no
bloquea el cierre de 0332 una vez cerrada la clase?

-- Analista
