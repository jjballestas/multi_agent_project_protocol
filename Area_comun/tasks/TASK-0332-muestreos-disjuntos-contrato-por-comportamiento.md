---
task_id: TASK-0332
file: Area_comun/tasks/TASK-0332-muestreos-disjuntos-contrato-por-comportamiento.md
title: "Los muestreos de TASK-0317 y TASK-0325 son disjuntos y por ese hueco entra una fuga de PII demostrada: cerrarla pide un contrato POR COMPORTAMIENTO, no mas AST"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0317
  - TASK-0325
  - TASK-0322
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    Residual R0325-2 del veredicto de TASK-0325, y es la RAIZ de la fuga que ese veredicto
    demostro. Los dos muestreos que protegen la exencion de fecha son **disjuntos**:
    TASK-0317 fija una familia de 333 miembros con offsets `("", "Z", "+02:00", "-05:00", "-12:30")`
    y la ejercita contra `contains_pii`; TASK-0325 anade `+05:45`, `-09:45`, `+13:00` y `+14:00`
    pero **solo contra `DATE_RE`**, nunca contra `contains_pii`.
    Un offset que este fuera de la familia de 333 y ademas fuera del conjunto de 0325 no lo prueba
    nadie contra el gate real. Por ese hueco entro SLIP-0325-1: un bypass estrecho sobre `+05:45`
    dejaba pasar un email por el gate de PII con la suite entera en verde.
    La remediacion de 0325 clava ese hueco para `break` y `continue`, que es correcto y suficiente
    para cerrar aquella tarea. Pero la cobertura sigue siendo SINTACTICA: un bypass equivalente por
    reestructuracion (`if not DATE_RE...: <todos los chequeos>`) o por filtrado del iterable en un
    helper externo sigue invisible al AST. Medido por el checker: las tres formas pasan el contrato
    entregado.
    Lo que cierra la familia entera no es mas AST: es un contrato **por comportamiento** que muestree
    offsets fuera de los 333 contra `contains_pii` y exija la respuesta correcta.
  acceptance:
    - "AC1 (falsacion previa): se demuestra que existe al menos un offset valido que NINGUN contrato actual ejercita contra contains_pii, y que un bypass estrecho sobre el pasa la suite entera en verde. Evidencia por comportamiento."
    - "AC2 (muestreos unificados): la familia de 0317 y el conjunto de offsets de 0325 dejan de ser disjuntos. El muestreo que se ejercita contra contains_pii cubre el rango de offsets que DATE_RE acepta tras el estrechamiento de 0322, incluidos los extremos (+14:00, -14:00) y los de minutos no-cero (+05:45, -09:45)."
    - "AC3 (contrato POR COMPORTAMIENTO, no sintactico): el negativo permanente no inspecciona el AST: ejercita contains_pii con entradas reales y exige la respuesta correcta. Debe morir ante un bypass por REESTRUCTURACION -- la forma que el AST no ve -- no solo ante break/continue."
    - "AC4 (las tres formas medidas por el checker): se prueban explicitamente el bypass por reestructuracion, el filtrado del iterable en helper externo, y la salida temprana; se declara cual mata cada contrato y por que. Si alguna sigue sin cubrirse, se declara como residual con su razon, no se silencia."
    - "AC5 (sin duplicar ni relajar lo existente): los contratos de 0317, 0322 y 0325 siguen verdes y sin cambios de semantica. Si el nuevo contrato hace redundante alguno, se declara y se justifica antes de tocarlo."
    - "AC6 (sin regresion): test_memory_db.py, inventario de contratos y gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca `build_memory_db.py`: la produccion es correcta y no cambia. No se rehace la
    remediacion de 0325 (esa clava break/continue y es su alcance). No se reabre `\d` sin `re.ASCII`
    (R3 de 0322, declarado en el ledger del SPEC).
  risk: low
  estimate: M
---

# TASK-0332 -- cerrar la familia por comportamiento, no por sintaxis

## De donde sale

Residual **R0325-2**, declarado por el checker en el veredicto de TASK-0325. No es una idea mia
sobre lo que podria fallar: es la raiz medida de una fuga que ya ocurrio.

    TASK-0317   offsets ("", "Z", "+02:00", "-05:00", "-12:30")   contra contains_pii
    TASK-0325   offsets +05:45, -09:45, +13:00, +14:00            contra DATE_RE unicamente

La interseccion de lo que se prueba contra el GATE REAL con lo que se prueba en los offsets nuevos
es **vacia**. SLIP-0325-1 entro exactamente por ahi.

## Por que mas AST no lo cierra

El checker midio tres formas de bypass equivalente y las tres pasan el contrato entregado:
reestructuracion (`if not DATE_RE...:` envolviendo todos los chequeos), filtrado del iterable en un
helper externo, y salida temprana. La remediacion de 0325 clava la tercera. Las dos primeras no las
ve ningun AST razonable, porque no hay nada sintacticamente anomalo que buscar: es codigo normal que
hace otra cosa.

Lo que TODAS comparten es que cambian el **comportamiento observable** de `contains_pii` sobre
entradas concretas. Un contrato que ejercite ese comportamiento las caza a las tres sin tener que
adivinar como estan escritas.

## La leccion que esta tarea materializa

Un contrato sintactico ata la FORMA en que hoy esta escrito el defecto. Un contrato por
comportamiento ata el EFECTO, que es lo que de verdad importa y lo unico que sobrevive a un
refactor. Es la misma conclusion a la que llegaron por separado el veredicto de 0324 (el contrato
ataba el helper, no el efecto) y el de 0325 (el detector miraba el conjunto de nodos equivocado).
Tres tareas distintas convergiendo en el mismo principio es senal de que el principio, y no cada
caso, es lo que hay que dejar clavado.

## Riesgo declarado (low)

Un contrato por comportamiento sobre un espacio de offsets puede volverse lento si se muestrea a
lo bruto; acotar el muestreo a los representantes de cada clase (extremos, minutos no-cero,
signo) y declarar el criterio. Riesgo mayor: creer que este contrato cubre TODA forma de bypass.
No lo hara -- cubre las que cambian el COMPORTAMIENTO observable de contains_pii, que es
justamente la familia que importa; lo que quede fuera se declara.

## Remediation 1 contract

The behavioral sweep keeps all 1,684 ASCII offsets for the extended-time baseline and adds a
prefix-by-offset matrix over a different year, basic time, one- and six-digit fractional seconds,
plus a date-only case. Representative offsets cover no offset, `Z`, both signs, non-zero minutes,
hour 13, and both `14:00` endpoints. Every case checks a scalar timestamp, a timestamp followed by
email PII, and a one-item list whose only PII is the exempt timestamp through an instance term.

The permanent negative reconstructs the three original bypass forms plus the two independent
checker slips: a falsy return on a changed year and external iterable filtering on basic time.
Production remains unchanged; adding a special-case production key is outside this remediation.

**R0332-3 (declared, non-blocking):** the 1,684-member offset sweep is exhaustive only over ASCII
digits. `DATE_RE` uses Unicode-aware `\d`, so non-ASCII decimal digits remain TASK-0322 residual R3
and are outside this task's code scope.

## Remediation 2 contract

The operator-authorized remediation in
`MSG-20260810-Arquitecto-to-Codex-REMEDIACION-TASK-0332` supersedes the earlier statement that
production would remain untouched. The defect is closed in production: `contains_pii` first evaluates
all non-phone PII across the complete input and only then applies the date exemption to the phone
heuristic. A date-shaped item can therefore no longer stop evaluation before a sibling email or an
instance term is checked.

The behavioral corpus is a product, not a star. It derives all 12 months, all 24 hours, all 1,684
ASCII offsets, and three accepted timestamp formats, for 1,454,976 source cases. Year, day, minute,
second, and fractional length are generated across their complete accepted marginal ranges while the
product advances. Each source case places a real email after the exempt timestamp and must remain
positive through the production entry point.

Three ephemeral mutants are derived from the production two-phase body and are judged only by
execution. They reintroduce a coordinate-keyed false return, an input-order early return, and a
basic-format early return. The permanent negative requires all three to diverge while the source
product remains fully positive; it does not inspect an AST or enumerate the checker probes.

**R0332-9 (declared, non-blocking):** the finite corpus proves the complete
month-by-hour-by-ASCII-offset-by-format product and complete marginals for the other accepted ASCII
coordinates. It does not claim the impossible full Cartesian product over every coordinate
simultaneously. The production two-phase invariant, rather than that finite sample alone, prevents a
date exemption from suppressing non-phone PII in another item.
