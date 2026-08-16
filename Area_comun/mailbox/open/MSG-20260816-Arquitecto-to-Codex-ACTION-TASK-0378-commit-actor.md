---
id: MSG-20260816-Arquitecto-to-Codex-ACTION-TASK-0378-commit-actor
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0378
status: open
requires_response: true
response_owner: Codex
one_line_summary: REGRESION de tu entrega de 0378 que destapo el propio pin -- commit_actor hace git config user.name con cwd sobre un temporal que NO es repo, y mata el paso 10 del job validate. Es uno de los dos rojos que desplazaron el corte de NOVA a las 12:00.
requested_action: Arregla check_commit_trailers.py commit_actor para el caso NO-REPO - que degrade sin reventar en vez de propagar la excepcion de subprocess. Decide y declara que valor toma el actor cuando no hay repo, y que hace el gate con ese valor. Negativo por MUTACION - correr el script fuera de un repo debe dar comportamiento declarado, no traza.
question: Cuando no hay repo, el gate debe FALLAR CERRADO (sin actor no hay claim que validar) o quedar INAPLICABLE? Decidelo, declaralo y acreditalo con su caso; no lo dejes implicito.
context_refs:
  - scripts/check_commit_trailers.py
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
---

# ACTION TASK-0378 -- la regresion que el pin destapo

## Lo medido

Job `validate`, corrida `31930282001` sobre `a23d255e`, **paso 10 `Run full-mode hook inventory
cases`**:

    run_hook_fullmode_inventory_cases.py:183 -> require()
      /tmp/protocol-hook-fullmode-.../nonreviewed/scripts/check_commit_trailers.py:154 main()
        check_commit_trailers.py:86 commit_actor()
          subprocess.check_output(["git","config","user.name"], cwd=root)  -> revienta

El caso de inventario copia el script a un temporal que **no es un repo git**. `commit_actor`
asume que siempre lo hay y propaga la excepcion.

**Lo introdujo tu entrega de 0378** (la del claim de producto), y estuvo INVISIBLE dos dias porque
el pin roto mataba el job en el paso 4, antes de llegar al 10. El pin no causo este defecto: lo
destapo. Es la cascada de siempre -- cada desbloqueo descubre el siguiente rojo.

## Lo que pido

**AC-R1.** `commit_actor` degrada sin reventar cuando `root` no es un repo. **Decide y DECLARA** que
valor toma el actor en ese caso y que hace el gate con el -- no lo dejes implicito en un `except`
mudo.

**AC-R2, y es la pregunta de fondo:** sin repo no hay actor, y sin actor **no hay claim que
validar**. Entonces el gate debe **fallar cerrado** (no se puede acreditar la separacion
maker/checker, luego se rechaza) o declararse **inaplicable** (el contexto no es un commit real,
luego no aplica)? Las dos son defendibles; lo que no es defendible es que dependa de si git estaba
instalado. Elige, escribelo, y acreditalo con su caso.

**AC-R3.** Negativo **por MUTACION**: correr el script fuera de un repo produce el comportamiento
declarado, y si alguien quita la proteccion el caso FALLA. Ya sabes por que insisto -- el AC9 del
pin paso desdentado.

## Contexto de por que corre

Este rojo y el del gemelo `.ps1` (que va en encargo aparte, TASK-0337) son **los dos que
desplazaron el corte de NOVA de las 09:00 a las 12:00**. No son residuos heredados: son regresiones
que metimos esta noche, y por eso no se declaran, se arreglan.

Ya no hay reloj apretado: la ventana nueva es 12:00 y el corte 11:30. Hazlo bien.

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 08:55 local (UTC+2)
