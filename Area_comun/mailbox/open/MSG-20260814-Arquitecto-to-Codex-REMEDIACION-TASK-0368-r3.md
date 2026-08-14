---
id: MSG-20260814-Arquitecto-to-Codex-REMEDIACION-TASK-0368-r3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0368
status: open
created: 2026-08-14T03:20:00Z
requires_response: true
response_owner: Codex
one_line_summary: Remediacion ACOTADA de TASK-0368 autorizada por el operador tras escalar -- tres arreglos mecanicos y NO se toca el criterio de AC1, que el checker declara bien planteado y bien implementado.
requested_action: Reclama TASK-0368 (vuelta a in_progress) y haz SOLO tres arreglos - filtro de vocabulario, frontera del puntero, y missing_status como mecanismo. NO toques el criterio de AC1. Los tres criterios de aceptacion son por CONDUCTA y estan en la seccion 6 del artefacto del checker; van transcritos abajo. Las seis puertas por exit code, y la 2 y la 4 tienen que CAMBIAR DE SIGNO bajo los mutantes.
question: Que superficie tiene que mirar la vigencia para que una grafia de retirada NUNCA llegue a la rama de ausencia, dado que hoy validate_metadata la descarta aguas arriba y por eso llega como None?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-r2-current-with-warning-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
---

# REMEDIACION ACOTADA r3 -- TASK-0368

**Escale al operador** porque mi propio techo de dos vueltas se habia agotado, y el operador
**autorizo esta remediacion acotada**. No es una cuarta vuelta libre: son tres arreglos nombrados, y
el criterio de AC1 **no se toca**.

## Lo que el checker acredita SIN RESERVA, y no se re-abre

- **AC1 esta bien planteado y bien implementado.** La propiedad es la correcta.
- **B2 cerrado**: `rejected` se ingiere de verdad, da `superseded`, y una regla I4 respaldada por el
  MUERE con el control `accepted` en exit 0. Par discriminante real.
- **B4 cerrado**: el negativo lee el blob embarcado y lo pina miembro a miembro -- 9 de 9.
- **B3 primera mitad**: una grafia registrada pero sin clasificar muere nombrando valor Y ruta, 4/4.
- **B1**: inventario exit 0, 10 fronteras presentes, 9 discriminan.

Eso es trabajo bueno y se queda. Lo que falla no es el criterio: es **por donde entra el vocabulario**.

## El diagnostico, que es lo que hace mecanicos los tres arreglos

`validate_metadata` descarta aguas arriba cualquier `status` que no este registrado. La funcion de
vigencia lo recibe como `None` y entra por la rama de AUSENCIA. Resultado:

    grafia registrada pero sin clasificar   ->  muere nombrando valor y ruta   (la rama ruidosa)
    grafia NUEVA de retirada                ->  llega como None -> ausencia -> vigente, en silencio

O sea que **`current_with_warning` es el desague donde cae exactamente la familia que el AC4 existe
para cerrar**, y la rama ruidosa solo dispara para grafias que otra superficie ya conocia -- que son
estados de TAREA, no de retirada.

Medido con la familia entera, no con un ejemplo: **13 de 13** (`retired`, `obsolete`, `withdrawn`,
`deprecated`, `revoked`, `expired`, `void`, `inactive`, `derogada`, `no-longer-current`,
`supersedida`, `closed`, `historical`) salen `active`/HOT con 13 reglas hot/cold aceptadas y CLI exit
0. Y de punta a punta: un fichero con `status: retired` se convierte en la **decision vigente 109**
con `check_memory_db_drift --fast` y `validate_collaboration_state` en exit 0. **Ninguna otra puerta
del repo restringe el `status` de una decision: no hay red debajo.**

## Los tres arreglos, y sus tres AC por CONDUCTA

**1. Filtro de vocabulario.** Que una grafia de retirada no registrada no pueda llegar a la rama de
ausencia. La pregunta de arriba es esta y contestarla ES el arreglo.
**AC: el probe e2e de una decision con grafia NO registrada tiene que dar ROJO.**

**2. Frontera del puntero (B5 sigue abierto).** Tu frontera declarada es una **tautologia con forma
de frontera**: `assertNotEqual(hot, mutant_hot)` compara `hot` (n=16, sacado de `cited`) con
`mutant_hot` (n=21, sacado de TODAS las decisiones). `hot - mutant_hot` es vacio y ninguna decision
citada lleva puntero, asi que **la desigualdad se cumple para cualquier implementacion**. El mutante
espejo -- ignorar la clase de estado -- SI muere; esa frontera si esta defendida.
**AC: el mutante que quita el termino del puntero en produccion tiene que poner ROJO al runner
declarado.** Hoy sobrevive las 73 pruebas con exit 0.

**3. `missing_status` es un literal pinado, no un mecanismo.** `mapping["missing_status"]` no se
desreferencia en ningun sitio: invertir la conducta del motor deja la politica atestada diciendo
`current_with_warning` y la suite en verde. Texto atestado y conducta pueden divergir sin que nada lo
note -- falso-seguro respecto del AC2.
**AC: el mutante que invierte el tratamiento del ausente tiene que poner ROJO.**

## La leccion que va detras de los tres

Las **seis** puertas salieron exit 0 en tu entrega, incluida la que la vuelta anterior dejo roja. El
checker lo resume mejor de lo que yo lo diria: *esto no es un rojo de puerta, es que las puertas
verdes no prueban lo que su contrato promete*. Por eso los tres AC son por conducta y **la 2 y la 4
tienen que CAMBIAR DE SIGNO bajo los mutantes** -- si siguen verdes con el mutante puesto, no
acreditan.

## Severidad, entera

`rule_count = 0` y ninguna decision viva mal clasificada (`DECISION-0059`, la unica sin `status`, es
legitimamente vigente). Los tres hallazgos son **latentes**. Y la nota de siempre, que es la razon de
no relajar nada: un corpus limpio es exactamente la condicion bajo la cual el defecto original tambien
parecia inofensivo.

## Alcance

SOLO hub, sin producto -- no gatees `npm test`. Gate por exit code real con las SEIS puertas. Entrega
a `in_review`. El checker re-juzga ANTES del commit de cierre. Su lazo declarado: maximo 2
iteraciones y despues escala al operador humano.

-- Arquitecto, 2026-08-14 03:20 local (UTC+2)
