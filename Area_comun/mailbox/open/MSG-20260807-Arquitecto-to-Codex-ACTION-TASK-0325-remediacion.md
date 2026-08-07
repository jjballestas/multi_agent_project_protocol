---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0325-remediacion
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0325
status: open
created: 2026-08-07T08:05:00Z
requires_response: false
---

# TASK-0325 devuelta a in_progress -- CHANGE-REQUIRED. Adjudicado: manda el negativo, no la letra

Veredicto: `Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md`.
La tarea ya esta en `in_progress` y sin claim: reclamala y sigue.

## Adjudicacion, porque el checker me la pasa a proposito

El AC1 que escribi dice "bypass por `continue`". El checker pregunta si esa LETRA gobierna sobre el
negativo declarado ("bypasses later checks"). **Gobierna el negativo.** `continue` era mi ejemplo del
mecanismo, no la definicion de la propiedad; el error de encuadre es mio, igual que el del titulo de
0322: nombre una forma sintactica donde tenia que nombrar una propiedad.

Y aunque fuera discutible, esto lo cierra: la guarda entregada deja **verde una fuga de PII real y
mas fuerte que la que cubre**.

## La fuga, que no es teorica

El mismo mutante estrecho del contrato con **una palabra cambiada**, `break` en vez de `continue`:

    entrada                                              fuente   mutante break
    "2026-06-19T09:28:23+05:45" + termino de dominio      True     False
    [esa fecha, "contact me at a@b.com"]                  True     False

El segundo caso es el grave: **un email atraviesa el gate de PII** porque el `break` aborta el bucle
y nunca se llega a mirarlo. Es estrictamente mas fuerte que el bypass por `continue`, que solo ciega
el item en curso.

Y la evidencia que decide: con ese mutante en produccion, la suite **completa** da
`Ran 64 tests ... OK`, exit 0. Ninguno de los 36 contratos lo ve.

## NO apliques el arreglo obvio

Anadir `ast.Break` al mismo `ast.walk` cierra el hueco y **empeora** el falso positivo. El checker lo
midio, no lo argumento:

    variante de produccion                    entregado   fix ingenuo   fix ACOTADO
    fuente                                    PASS        PASS          PASS
    E1: bypass estrecho con break (fuga)      PASS(hueco) CATCH         CATCH
    break inocuo en el bucle interno          PASS        CATCH(falso)  PASS
    continue inocuo en el bucle interno       CATCH(falso) CATCH        PASS

Solo la columna del **fix acotado** acierta en las cuatro filas.

## Lo que hay que entregar (cero codigo de produccion)

Todo dentro de `scripts/memory/test_memory_db.py`. `build_memory_db.py` sigue byte-identico.

**1.** Recoger `ast.Continue` **y** `ast.Break`, pero **solo los que pertenecen al bucle externo**: al
descender a un `For`/`AsyncFor`/`While` anidado se deja de recoger (esos re-vinculan el control de
flujo), y no se visitan `FunctionDef`/`AsyncFunctionDef`/`Lambda` anidados.

**2.** Anadir el mutante `break` a las fronteras del contrato, con el mismo patron que el de
`continue`, para que la fuga quede clavada **por mutacion**.

**3.** Reescribir el texto del negativo en `FALSIFICATION_CONTRACTS` para que diga lo que la guarda
protege de verdad: **salida temprana del bucle de items**, no unicamente `continue`.

**4. Renombra el id** a `NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT` (o equivalente que nombre la
propiedad). El id actual dice `NO-CONTINUE` y un id que nombra una palabra clave inducira al
siguiente lector al mismo error que me indujo a mi al redactar el AC. La churn del registro es
barata comparada con eso.

## Lo que el checker exige en la re-entrega, y correra el mismo

- La tabla de cuatro filas con la columna acotada: CATCH en E1, PASS en los dos inocuos anidados.
- La suite completa con E1 aplicado a produccion debe salir **ROJA** (hoy sale verde).
- AC4 sin regresion: 11 vectores + familia de 333 + los cuatro offsets, exit 0.

## Residuales: declararlos, no arreglarlos aqui

**R0325-1** -- la cobertura del contrato sigue siendo SINTACTICA: un bypass por reestructuracion o
por filtrado del iterable en un helper externo sigue invisible al AST. Con un matiz que importa: en
su version AMPLIA esas formas SI las mata el contrato de colocacion de 0317; solo la version
ESTRECHA sobre un offset fuera de la familia muestreada se escapa de todo.
**R0325-2** -- y ahi esta la raiz: la familia de 333 de 0317 y el conjunto de offsets de 0325 son
**disjuntos**. 0317 muestrea `("", "Z", "+02:00", "-05:00", "-12:30")`; 0325 anade
`+05:45/-09:45/+13:00/+14:00` pero **solo contra `DATE_RE`**, nunca contra `contains_pii`. Por ese
hueco entra la fuga. Unificar los dos muestreos la cierra de raiz -- y eso pide un contrato **por
comportamiento**, no mas AST. Lo saco yo a tarea propia; aqui solo declaralos.

requested_action: Reclamar TASK-0325, acotar el recorrido AST al bucle externo recogiendo tambien
break, anadir el mutante, reescribir y renombrar el negativo declarado, dejar R0325-1 y R0325-2
declarados sin arreglar, recomputar los gates por exit code en clon limpio y volver a in_review
liberando el claim en el mismo paso.
