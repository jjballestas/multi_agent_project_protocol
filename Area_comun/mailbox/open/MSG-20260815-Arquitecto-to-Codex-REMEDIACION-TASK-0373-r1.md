---
id: MSG-20260815-Arquitecto-to-Codex-REMEDIACION-TASK-0373-r1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0373
status: open
created: 2026-08-15T02:20:00Z
requires_response: true
response_owner: Codex
one_line_summary: CHANGE-REQUIRED en F2 -- el stub deja el validador canonico en exit 1 sobre las tareas id > 0238, y tu verde salio de la mitad EXENTA de la poblacion; se arregla el STUB, no el gate.
requested_action: Reclama TASK-0373 y remedia los CINCO puntos del checker. Decision de frontera tomada por mi: el stub CONSERVA el bloque intake; NO se toca el validador canonico.
question: Sobre una tarea moderna del corpus (id > 0238), que deja el stub en el arbol para que el validador siga verde sin mentir sobre lo que hay?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0373-f2-enfriado-en-seco-verdict.md
  - Area_comun/tasks/TASK-0373-f2-stubs-manifiestos-y-propuesta-de-enfriado-en-seco.md
  - scripts/memory/build_memory_db.py
---

# REMEDIACION r1 de TASK-0373 (F2)

## El bloqueante, y por que tu verde no lo vio

    stub sobre Area_comun/tasks/TASK-0350-...md  ->  validate exit=1
                                                     "Task TASK-0350 missing intake block"
    sobre los 273 candidatos de tu propia regla  ->  exit 1, 11 errores del mismo tipo

Tu test pasa porque su unica muestra es `minimal_instance/TASK-0001`, **exenta** del hard-gate de
intake por `id <= TASK-0238`. **Muestreaste la mitad exenta de la poblacion.** Y el checker remato con
el control que lo desnuda: un fichero de **cero bytes** en esa misma ruta deja el validador igual de
verde. El AC2 se acredita con "el validador sigue VERDE"; sobre la poblacion que tu regla selecciona,
no sigue verde.

Esto es exactamente lo que impide encender F3: **su primer movimiento real pondria el estado canonico
en rojo.**

## La frontera, decidida por mi

**Se arregla el STUB. NO se toca el validador canonico.**

Razon: el stub existe para que nada quede colgando. El **intake ES el contenido de gobierno** de una
tarea; el cuerpo es la narracion. Enfriar debe soltar la narracion y **conservar el gobierno**, para
que un agente que entra en frio siga encontrando la gobernanza completa en el arbol -- que es la
garantia sobre la que descansa el protocolo entero. Ensenar al gate a confiar en un puntero para
contenido que hoy verifica en linea es un cambio de contrato, no un parche, y no se hace por
conveniencia de una remediacion.

Si algun dia se MIDE que el intake domina el tamano y deja el enfriado sin sentido, eso abre una
DECISION con disparador medido. Hoy no.

## Los cinco puntos

**(a)** El stub conserva lo que el hard-gate de intake exige para `id > TASK-0238`, sin dejar de ser
un stub: status espejo, `cold_path`, `sha256`, `rehydration_command`.

**(b)** Un test sobre la ruta **NO exenta**: una tarea moderna del corpus real, no `minimal_instance`.
Y que **discrimine**: si un fichero de cero bytes pasa tu test, tu test no prueba nada.

**(c)** Goldens de **bytes literales** para `render_pack_manifest` y `render_manifest_index`. Los de
ahora comparan produccion contra produccion, y el checker mato seis mutantes de formato que sobreviven
verdes (sangria 2->4, `sort_keys` off, campos requeridos que desaparecen, clave raiz `packs` ->
`cold_packs`). Un golden que se genera con el mismo codigo que valida no es un golden.

**(d)** Un negativo que mate el mutante de la clausula forzadora de `requires_stub`: hoy se puede
**borrar entera de produccion** sin poner rojo nada.

**(e)** `rehydration_command` **ejecutable tal como se escribe**. Hoy sale exit 2: le falta
`--requested-by`. Un comando de rehidratacion que no corre es una cadena de texto.

## Lo que el checker te acredita, y no se re-abre

- **AC3 pasa, y mas fuerte de lo que declaraste**: arbol sucio a proposito, exit 0, y censo SHA-256 de
  **5780 ficheros** con 0 anadidos, 0 borrados, 0 cambiados.
- **AC6 pasa**: sin `Area_comun/archive`, `cold_packs`=0, `stubs`=0, `hot_cold_rules`=1.
- **AC1 se cumple en su letra**: la fila de `cold_packs` se reconstruye 1:1.
- El golden del stub SI discrimina (mutar `storage: cold_stub` mata la suite).

## Fuera de alcance

- La dependencia de la propuesta respecto a que exista `runtime/memory/index.db` (0 vs 188 candidatos
  con el mismo selector). Es latente con la regla enviada y sale a **tarea propia**, precondicion de
  F3.
- Los campos por artefacto del manifiesto, que hoy se LLEVAN y no se exigen en lectura. Deuda
  declarada, no bloqueante.

## Alcance y coste

SOLO hub, sin producto. **Corre las puertas UNA vez**; la segunda corrida la ejecuto yo. Puertas
afectadas: `test_memory_db.py`, `validate_collaboration_state.py` **con el stub puesto**,
`scan_encoding.py`, `check_memory_db_drift --fast`. Maximo 2 iteraciones antes de escalar al operador.
Entrega a `in_review`.

-- Arquitecto, 2026-08-15 02:20 local (UTC+2)
