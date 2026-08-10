---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0353
status: archived
created: 2026-08-10T03:04:43Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga TASK-0353 tras la remediacion 1, en clon limpio y con exit codes reales.
question: La lista de nueve fallos que declara la entrega sale de SU corrida, o esta transcrita de la anterior?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-filtro-derivado-dos-anclas-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353-remediation-1.md
---

# REVIEW TASK-0353 r2 -- una sola ancla, y la premisa afirmada

Escrito 05:04 local. **Ancla: `6b7b24e9f027413b985012392723220847d8bde2`**. Implementacion: `d2871436`.
**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## Lo que ya verifique yo, por comportamiento

Las dos primeras propiedades que exigiste estan atacadas en la estructura, no en el sintoma:

    def turn_schema_keys(root: Path) -> frozenset[str]:
        schema_path = root / "runtime" / "turn_schema.json"      # <- MISMA ancla que validate_turn
        schema = read_json(schema_path)
        if schema.get("additionalProperties") is not False:
            raise ValueError(f"{schema_path}: orchestrator filtering requires additionalProperties=false")

La funcion pasa a recibir `root` y resuelve el mismo artefacto que la puerta. Y la premisa que
senalaste como no afirmada **ahora se afirma y revienta ruidosamente**. Eso no te ahorra medirlo: te
ahorra descubrirlo.

## FOCO 1 -- el AC6, y creo que es donde esta el problema

La entrega declara **60 PASS / 9 FAIL / 8 UNSUPPORTED**, con los fallos en los pasos:

    declarado ahora (9) : 34, 36, 39, 40, 43, 50, 53, 58, 59
    medido por ti (7)   : 17, 36, 43, 50, 53, 58, 59      (en e853cb73)

**Los pasos 34, 39 y 40 vuelven a figurar como fallo**, y tu los mediste PASANDO -- sueltos en
`f4c6c3b9` y dentro de tu secuencia completa. Y el 17 desaparece, cosa que si cuadra: aplique la
poda vencida y ese paso salio verde.

Dos explicaciones posibles y hay que separarlas:

- **Sensibilidad al orden** dentro del replicador, que tu misma declaraste como residual R6. Si es
  esto, no es defecto de la entrega y hay que declararlo como propiedad del replicador.
- **Lista transcrita** de la entrega anterior en vez de derivada de la corrida propia. Si es esto,
  el AC6 vuelve a incumplirse por el mismo motivo exacto que la vez pasada.

El AC6 pide la lista **derivada del propio run**. Que la composicion coincida casi exactamente con
la declaracion anterior -- y contradiga tu medicion -- es lo que hay que resolver primero.

## FOCO 2 -- la tercera propiedad: el negativo muere en las DOS

Exigiste que el contrato permanente muera ante (a) anclas divergentes y (b) la relajacion de
`additionalProperties`. La entrega dice que ejercita ambas. Comprueba tambien lo que senalaste
antes: que **no derive sus claves contra un `fixture_root` que es copia del hub**, porque asi nunca
ejerce la unica configuracion en la que las dos anclas difieren. Y el `removed_key = min(...)`:
mutar la clave alfabeticamente minima ata el helper, no el efecto.

## FOCO 3 -- R4, los dos esquemas divergentes

La entrega toca `examples/full_runtime_instance/runtime/README.md`, lo que sugiere que **declara**
la divergencia 1.3.0 / 1.2.0 en vez de converger. Si es asi, juzga si la declaracion dice lo
suficiente: que el espejo es una instantanea historica, por que se conserva, y que nada del hub debe
derivar de el.

## Residuales que ya vienen declarados

- El AC3 sigue usando el monkey-patch acotado de `find_unresolved_placeholders` que tu declaraste
  como R1.
- El runner completo de instanciacion sigue rojo por los marcadores sin resolver -- territorio de
  TASK-0350, no de esta tarea.
- **Sin CI real**: la cuenta sigue bloqueada por facturacion y el operador ha decidido no
  desbloquearla hasta cerrar la cascada en local. Todo, lo tuyo incluido, es local. Declaralo.
