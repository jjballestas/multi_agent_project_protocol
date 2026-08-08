---
id: TASK-0337
title: El guard de residuo veta sin mirar scope -- gemelo de TASK-0331
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    El guard pre-exec de residuo decide sobre la suciedad del arbol COMPLETO, no sobre si las rutas
    sucias intersectan lo que el mensaje diferido necesita. Es el mismo defecto de ceguera de scope
    que TASK-0331 corrige en la admision de claims, en un guard hermano del mismo fichero.
    Inventariar TODOS los vetos pre-exec, declarar para cada uno sobre que liga hoy y sobre que
    deberia ligar, y corregir los que vetan por una propiedad global cuando la decision es por-par.
  acceptance:
    - "Inventario COMPLETO de los vetos pre-exec del harness, uno por uno, con lo que liga cada uno hoy y si su alcance es correcto; el inventario se entrega aunque solo uno resulte defectuoso."
    - "Medido: un mensaje cuyo trabajo NO intersecta las rutas sucias deja de ser diferido, y un mensaje cuyo trabajo SI las intersecta sigue siendolo."
    - "Declarado explicitamente que garantiza el guard tras el cambio, incluida la frontera que deja de cubrir si la hay."
    - "Negativo permanente nuevo que MUERA ante el mutante de codigo muerto, no solo ante la ausencia del fichero."
    - "Sin regresion en lo ya probado del harness, en particular la admision atomica y el ciclo de vida de leases de TASK-0331."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El ciclo de vida de leases de TASK-0331: si el arreglo lo toca, se declara y se coordina, no se absorbe."
    - "Cualquier cambio en el umbral de poda o en el driver de peso de mailbox (RES-11)."
    - "Codigo de producto."
  risk: medium
  estimate: M
---

# TASK-0337 -- el guard de residuo veta sin mirar scope

## El hecho medido

Hoy 2026-08-08, con Codex ejecutando la remediacion 4 de TASK-0331, el cron del Analista difirio
`MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r2`:

    09:24:15 RETRY_DEFER defer=1 reason=worktree_residue_live
             paths=["Area_comun/state/*.json", "Area_comun/tasks/TASK-0331-*.md",
                    "runtime/state/events.jsonl", "runtime/state/snapshot.json",
                    "personal/Analista/drafts/DRAFT-MSG-0258-rejuicio-GO.md"]

**El mensaje diferido es de TASK-0329. Ninguna de las rutas sucias pertenece a TASK-0329.**

## El defecto

`Get-StagedResidueState` (`scripts/harness/peer_mailbox_cron.ps1:775`) toma el `git status`
porcelain del repositorio entero. El unico filtro que aplica es por area personal ajena
(`^personal/<otro>/`). Despues devuelve un veredicto GLOBAL -- `none` / `live` / `aborted` --
y el llamador (`:1274`) difiere el mensaje sea cual sea su trabajo.

No existe comparacion alguna entre las rutas sucias y las rutas que el mensaje necesita.

## Por que es el gemelo de TASK-0331

TASK-0331 se titula *claim ajeno veta sin mirar scope*. Es literalmente el mismo defecto en el
guard de al lado, en el mismo fichero: **una decision que es por-par (este mensaje contra estas
rutas) tomada sobre una propiedad global (el arbol esta sucio)**. Cerrar la admision de claims no
cerro la familia. Esto es lo que hace el hallazgo interesante y no un bug suelto.

## Lo que NO doy por sentado

No prescribo el arreglo, y hay una tension real que el inventario debe resolver antes de tocar nada:

- Un revisor que **clona limpio desde HEAD** es indiferente al arbol sucio: para el, el veto sobra
  casi siempre.
- Un agente que trabaja **en el arbol vivo** si necesita el veto.

Asi que "hacerlo scope-aware" puede ser correcto para un consumidor e incorrecto para otro. Quiero
el inventario y la propuesta razonada ANTES del parche, y quiero declarado a que consumidor sirve
cada veto.

## Direccion e impacto, sin inflarlo

**No corrompe y falla CERRADO**: bloquea de mas, nunca de menos. El presupuesto real es de 7200 s
por razon, y la razon al cambiar reinicia el reloj, asi que un exec normal de 20-40 min no lo agota.
El dano aparece cuando un peer deja trabajo sin commitear durante horas -- **paso tres veces en la
jornada del 7 al 8 de agosto**, cada una por una tarea que un peer dejo `blocked` con residuo, y las
tres las desbloquee yo a mano commiteando su trabajo. Ese es el coste que justifica la tarea, no el
diferimiento de hoy, que se resolvera solo.

## Secuenciacion -- importa

**No se rutea hasta que TASK-0331 cierre.** Comparte fichero con ella y Codex lo tiene modificado
ahora mismo. Contratarla ya es para que no se pierda; ejecutarla en paralelo es fabricar un conflicto.
