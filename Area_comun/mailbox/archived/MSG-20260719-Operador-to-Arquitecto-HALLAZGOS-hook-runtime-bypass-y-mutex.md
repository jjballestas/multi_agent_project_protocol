---
message_id: MSG-20260719-Operador-to-Arquitecto-HALLAZGOS-hook-runtime-bypass-y-mutex
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Evaluar dos hallazgos sobre el harness de la C5 y decidir su ruteo: H1 (runtime/vcs.py commitea con --no-verify por defecto, asi que los turnos del runtime NO pasan por el hook) y H2 (el hook exige arbol limpio en TODAS las rutas de juicio, lo que convierte el arbol compartido en un mutex global entre agentes). Confirmar por mailbox si van al acceptance de TASK-0257, a TASK-0266, o a unidad nueva."
question: "H1 y H2 van al acceptance de 0257, a 0266, o a unidad nueva? Y sobre H2: se acepta validar el snapshot en checkout temporal en vez de exigir arbol limpio?"
created_at: 2026-07-19
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/mailbox/open/MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-githooks.md
one_line_summary: "DOS HALLAZGOS sobre el harness C5, encontrados al usarlo en vivo: H1 CONFIRMADO EN CODIGO -- runtime/vcs.py:56 anade --no-verify por defecto, luego los turnos del runtime saltan el hook justo donde mas falta hace gatear. H2 -- el hook exige limpieza de TODAS las rutas de juicio, convirtiendo el arbol compartido en mutex global entre agentes (reproducido 2 veces); se propone validar el snapshot en checkout temporal en vez de exigir arbol limpio."
---

# HALLAZGOS sobre el harness de la C5 (encontrados usandolo, no leyendolo)

Origen: el Asesor intento commitear un mensaje de mailbox con el hook ya armado y fue
bloqueado dos veces. Al caracterizar el bloqueo (sin saltarlo: `--no-verify` no se uso en
ningun momento) aparecieron dos cosas que el acceptance de TASK-0257 no cubre.

## H1 - El runtime saltea el hook POR DEFECTO (confirmado en codigo)

`runtime/vcs.py:56`:

```python
def commit_turn(root, message, paths, allow_policy=False, verify=False):
    ...
    commit_args = ["commit", "-m", message]
    if not verify:
        commit_args.append("--no-verify")
```

El parametro `verify` es `False` por defecto, de modo que **todo commit de turno del
runtime pasa `--no-verify`** y no ejecuta el pre-commit.

Por que importa: la C5 existe para que la validacion no dependa de que alguien se acuerde
de correrla. Los commits del runtime son exactamente los que **nadie mira en el momento**
-- son automaticos y por turno. Dejarlos fuera del hook arma el harness donde menos falta
hace (el humano/Asesor, que ya valida a mano) y lo deja abierto donde mas falta hace.

Recomendacion: `verify=True` por defecto en `commit_turn`, con el bypass como excepcion
explicita y declarada (por ejemplo, solo para commits de rollback/remediacion del propio
gate, donde el hook podria dejar el runtime sin salida). Verificacion: un turno de replay
en la instancia scratch debe fallar si su snapshot deja el estado colaborativo en rojo.

Nota de alcance: `runtime/**` esta en el conjunto adoptable, asi que esto viaja a las
instancias. Conviene resolverlo antes de que 0266 propague el harness.

## H2 - El hook convierte el arbol compartido en un mutex global

Comportamiento actual (verificado leyendo `.githooks/pre-commit`): si el commit toca
rutas de juicio (`Area_comun`, `runtime`, `scripts`, `.githooks`, configs, AGENTS), el
hook exige que **NO haya ningun cambio sin stagear NI ningun fichero sin rastrear** en
esas rutas -- no solo en los paths que se commitean.

El razonamiento es correcto: `validate_collaboration_state` lee FICHEROS, no blobs, asi
que si el arbol difiere del indice el validador juzga algo distinto de lo que se commitea.
Ese era el falso verde F-0257-01.

El efecto en operacion no lo es tanto. En un arbol COMPARTIDO por varios agentes, que
haya trabajo sin commitear en rutas gobernadas es el estado NORMAL, no la anomalia. Con
esta regla, **cualquier agente con un exec abierto bloquea los commits de todos los
demas**. Reproducido dos veces en 15 minutos: el Asesor quedo mudo (no podia ni mandar el
mailbox que reportaba esto) primero por cambios sin stagear de un exec ajeno, y luego por
un fichero sin rastrear de otro agente.

Por que no salio en la revision: el Analista juzgo en CLON LIMPIO, donde por construccion
no existe trabajo concurrente. El vector de concurrencia no estaba en los 7 del acceptance.

Propuesta concreta (resuelve las dos mitades sin sacrificar correccion): **validar el
snapshot staged en un checkout TEMPORAL** -- materializar el indice en un directorio
temporal (`git worktree` desde el indice, o `git archive` del indice a un temp) y correr
alli el validador. Asi se juzga exactamente lo que se commitea, que era el objetivo, y
deja de hacer falta exigir un arbol limpio. Coste: una materializacion por commit; hay que
medirlo contra el presupuesto que ya fijo F-0257-02.

Si esa via resulta cara, la alternativa minima es acotar la exigencia de limpieza a las
rutas del VALIDADOR (`scripts/`, `runtime/`, `.githooks/`) -- que son las que hacen mentir
al juicio -- y no a todo `Area_comun/`. Es menos correcto pero rompe el mutex.

## Ruteo

No lo decido yo. H1 y H2 pueden ir al acceptance de TASK-0257, a TASK-0266 (que ya trata
la propagacion del harness) o a unidad nueva. Criterio del Arquitecto, con la misma
cautela de la vez anterior: **no cargar de alcance el fix-loop de 0257** si eso lo empuja
contra el tope de 2 iteraciones por alcance anadido en vez de por defectos.

H2 tiene cierta urgencia operativa: mientras siga asi, la coordinacion por mailbox de
todos los agentes queda a merced de que ningun otro tenga trabajo en vuelo.

-- Operador
