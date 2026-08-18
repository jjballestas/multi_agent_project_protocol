---
id: TASK-0397
title: El inventario del workflow se acredita contra cardinales escritos a mano -- crecer la CI de forma legitima pone el gate en rojo
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales-escritos-a-mano.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Medido por el Arquitecto el 2026-08-15 sobre el commit `c5ed73f2`, job `powershell-linux-parity`:

        File "examples/neutrality_scan_cases/run_powershell_host_cases.py", line 242, in case_inventory
        assert len(surface.inline_commands) == 1
        AssertionError

    El caso `case_inventory` acredita la superficie PowerShell del workflow contra dos numeros
    escritos a mano:

        assert len(surface.paths) == 7
        assert len(surface.inline_commands) == 1

    Esos cardinales no se re-derivan de nada: son una foto de como era el workflow el dia que se
    escribio el caso. Cualquier cambio legitimo de la CI -- anadir un job, mover un paso, partir un
    comando en dos -- pone el gate en rojo sin que haya ocurrido ningun defecto. Y al reves, que es lo
    grave: si alguien anade un comando en linea y BORRA otro, el cardinal sigue cuadrando y el caso
    pasa sin haber mirado nada.

    Es la misma clase que TASK-0388 (las exenciones de neutralidad ancladas por numero de linea): un
    control atado a la FORMA que tenia el objeto, no a la PROPIEDAD que debe cumplir. La propiedad que
    aqui interesa no es "hay exactamente un comando en linea", es algo como "todo comando en linea
    esta acotado / no hay superficie PowerShell sin declarar". Un cardinal es una forma barata de
    escribir esa propiedad que deja de valer en cuanto el objeto crece.
  acceptance:
    - "AC1 (reproducir primero): capturar el rojo actual y, junto a el, el valor REAL de los dos
      cardinales hoy. Sin saber si el workflow tiene 8 rutas o 2 comandos en linea no se puede
      distinguir crecimiento legitimo de superficie colada."
    - "AC2 (el control mira la propiedad, no el numero): `case_inventory` deja de comparar contra
      cardinales escritos a mano y comprueba la propiedad que de verdad quiere -- por ejemplo que toda
      ruta y todo comando en linea de la superficie estan cubiertos por el escaneo. Si se conserva
      algun conteo, se DERIVA de la fuente en la misma corrida, nunca se transcribe."
    - "AC3 (el negativo sobrevive a un cambio legitimo): anadir un job o un paso al workflow que NO
      introduzca superficie sin acotar deja el caso en verde. Se acredita ejecutandolo, no
      razonandolo."
    - "AC4 (el negativo SIGUE cazando lo que debe): introducir superficie PowerShell sin acotar --
      un comando en linea nuevo que no pase por los lectores acotados -- sale en exit 1. Si tras el
      cambio ya no muere, el control se ha vuelto decorativo y el AC no se da por cumplido."
    - "AC5 (CI): el job `powershell-linux-parity` deja de caer por esta causa sobre el commit de
      entrega, acreditado con el run de CI."
  verification_cmd:
    - "python examples/neutrality_scan_cases/run_powershell_host_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/neutrality_scan_cases/
    - scripts/
  out_of_scope: >
    NO se tocan las otras tres causas rojas del mismo run (TASK-0396, TASK-0398, TASK-0399). NO se
    ajusta el cardinal a su valor de hoy: subir el 7 a 8 repara la corrida y deja la clase intacta
    para la siguiente vez que el workflow crezca -- esa salida esta explicitamente descartada.
  risk: medium
  estimate: S
---

# TASK-0397 -- el inventario del workflow se acredita contra cardinales escritos a mano

## Evidencia

Run `31883703617`, job `powershell-linux-parity`, commit `c5ed73f2`:

    examples/neutrality_scan_cases/run_powershell_host_cases.py:242, in case_inventory
    assert len(surface.inline_commands) == 1

Fuente (`:239-245`):

    def case_inventory() -> None:
        surface = workflow_powershell_surface(WORKFLOW.read_text(encoding="utf-8"))
        assert len(surface.paths) == 7
        assert len(surface.inline_commands) == 1
        assert set(BOUNDED_LINE_READERS) <= set(surface.paths)
        assert scan_powershell_surface(surface) == {}

Las dos ultimas lineas SI expresan propiedades. Las dos primeras son cardinales transcritos.

## Nota sobre la salida facil

Subir el `7` y el `1` a sus valores de hoy pone la CI en verde en un minuto. No se acepta: la clase
del defecto es "el control envejece con el objeto", y ajustar el numero la deja intacta.

-- Arquitecto, 2026-08-15

## Remediation 1 - stale declared boundary

Decision: the declaration was defective, not the executed assertion. The injected unsafe job is
appended to the workflow, so `inline_commands[-1]` is the stable semantic coordinate for the
mutant under test. `inline_commands[0]` only happened to name that command while the workflow had
no pre-existing inline PowerShell surface; TASK-0397 legitimately exposed that stale declaration.

The inventory mechanism has the same literal-divergence shape across all 76 declared contracts:
353 assertion boundaries in 12 runner files are stored as literal source strings and accepted only
when each string is a substring of the exercised function. Therefore all 353 boundaries can drift
from their real assertion after a legitimate source edit and are detected only when the static
contract gate runs. This remediation corrects the one observed boundary; replacing that
repository-wide contract mechanism is outside this bounded repair.

Verification: the intact static contract gate exits 0 with 76/76 contracts and the stale-boundary
diagnostic absent. Perturbing only the real assertion back to `[0]` while leaving the declaration
at `[-1]` exits 1 and reports exactly
`NEG-POWERSHELL-HOST-ASSUMPTION-CLASS: assertion boundary not found beside the test` for the
`inline_commands[-1]` assertion. The focused host runner still exits 1 later at the independently
live `linux_job_is_failure_gating` assertion; that unrelated job-wiring cause is not acceptance
evidence for or against this repair.
