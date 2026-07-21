---
task_id: TASK-0282
title: "[HARNESS] Retirar la rama destructiva del rollback: ni reset --hard ni re-apply del parche de worktree; el arbol ajeno no se reescribe nunca"
type: fix
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-07-21
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0275, TASK-0280, TASK-0281, DECISION-0020, DECISION-0103]
linked_decisions: [DECISION-0103, DECISION-0020]
file: Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
intake:
  type: fix
  goal: "ENMIENDA FIRMADA POR EL OPERADOR (2026-07-21 04:55) que SUPERSEDE la mitad 'revert' del acceptance sellado de TASK-0272 ('un exec que aborta DEBE DEJAR EL ARBOL COMO LO ENCONTRO -- unstage y revert de lo que toco'). La mitad 'unstage' se conserva; la mitad 'revert' se retira. Motivo: en un arbol compartido, revertir exige decidir que cambios son del exec, y esa decision fue la fabrica de defectos de toda la cadena 0272-0280 -- cuatro iteraciones, cada una cerrando los casos enumerados y abriendo los adyacentes, con destruccion real de trabajo ajeno en al menos cuatro ocasiones (eventos de ledger ya aplicados, filas de poda, un mensaje de review completo, y documentos creados por una decision firmada). Se retiran las dos operaciones que reescriben el arbol: git reset --hard y el re-apply del parche de worktree. El exec deja de poder deshacer contenido que no sea suyo, porque deja de poder deshacer contenido en absoluto."
  acceptance:
    - "El rollback NO ejecuta git reset --hard bajo ninguna condicion, y NO re-aplica el parche de worktree pre-exec. Se elimina el codigo, no se condiciona."
    - "La mitad conservada del acceptance de TASK-0272 sigue viva: el indice se restaura al snapshot pre-exec con git apply --cached y su exit code GATEADO; si el apply falla, se declara en el log y no se sigue en silencio."
    - "El indice se restaura ANTES de cualquier otra operacion del rollback, y cada movimiento de fichero posterior va aislado en su propio manejo de error: un fallo al mover no puede abortar la restauracion del indice (hoy el trap de la funcion mata todo lo que viene despues del primer error)."
    - "Los ficheros que el exec creo se ponen en CUARENTENA, nunca se borran (TASK-0275), con allowlist de NO-cuarentena para Area_comun/mailbox/** reutilizando el predicado que ya existe y hoy esta muerto sin llamadores (Test-LedgerManagedPath): un mensaje entrante depositado durante la ventana no puede salir de la cola sin dejar rastro."
    - "La enumeracion de untracked previos (git ls-files --others) queda gateada por exit code: si falla, no se pone nada en cuarentena y se declara; hoy un fallo ahi convierte todo el arbol untracked en material de cuarentena."
    - "La cuarentena vive fuera de Area_comun/ y de runtime/ (bajo .protocol-tmp/), y eso queda escrito para que nadie la 'mejore' hacia dentro del arbol gobernado y rompa los escaneos."
    - "Negativos permanentes: exec abortado con trabajo concurrente de otro actor en el arbol (el trabajo ajeno SOBREVIVE intacto); mensaje entrante depositado durante la ventana (NO se pone en cuarentena); fallo del apply del indice (declarado, no silencioso); fallo de la enumeracion de untracked (nada se mueve)."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde con los negativos nuevos"
    - "Prueba de bucle real: exec abortado mientras otro actor tiene cambios sin commitear; los cambios ajenos siguen ahi byte a byte"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Arrancar antes de que TASK-0281 este cerrada - PROHIBIDO. Sin la deteccion de residuo sucio del punto 4 de 0281, retirar el reset --hard convierte una destruccion visible en una parada silenciosa: un exec matado a mitad de escritura deja ficheros sucios que ningun pre-gate ve, y cada mensaje siguiente quema sus reintentos contra un validador rojo sin auto-sanacion."
    - "Reabrir el acceptance de TASK-0280 o el de TASK-0281 - FUERA."
    - "Cambiar la frontera de outcome - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: high
  estimate: M
---

# TASK-0282 - El arbol ajeno no se reescribe nunca

## Enmienda firmada

El Operador firma el 2026-07-21 a las 04:55 la **supersesion parcial** del acceptance de
TASK-0272. Aquella unidad exigia que un exec abortado dejase el arbol como lo encontro,
mediante **unstage y revert**. Se conserva el unstage; **se retira el revert**.

La razon no es que el revert fuera mala idea, sino que en un arbol compartido **revertir
exige decidir que es tuyo**, y esa decision resulto ser la fabrica de defectos de toda la
cadena: cuatro iteraciones, cada una cerrando los casos que el veredicto anterior enumero y
abriendo los adyacentes -- rutas, tipo de cambio, nombre de evento -- con destruccion real
de trabajo ajeno en al menos cuatro ocasiones documentadas el 2026-07-20: eventos de ledger
ya aplicados, filas de una poda firmada, un mensaje de review completo escrito y sin
commitear, y el documento creado por una decision firmada.

La retirada elimina la pregunta en vez de responderla mejor: el exec deja de poder deshacer
contenido ajeno porque deja de poder deshacer contenido.

## Dependencia dura

**No arranca hasta que TASK-0281 este cerrada.** Lo levanto una revision adversarial
independiente y es la unica objecion que sobrevivio al escrutinio: hoy el `reset --hard`
tapa un caso que nadie mas ve. `Get-StagedResidueState` mira solo el indice, asi que un exec
matado a mitad de escritura deja ficheros modificados sin stagear que ningun pre-gate
detecta. Si se retira el reset antes de que el pre-gate mire tambien el worktree, cambiamos
una destruccion visible por una parada silenciosa, que segun el criterio del propio Operador
es peor: la basura es reparable, la parada muda no se ve.

## Lo que hereda de sus vecinas

- De **TASK-0275**: cuarentena en vez de borrado, con la allowlist de mailbox que impide que
  un mensaje entrante desaparezca de la cola sin rastro.
- De **TASK-0281**: el pre-gate que ve residuo sucio y defiere con senal.
- De **TASK-0280**: la regla conservadora ante ambiguedad y el `PRESERVED` verificado contra
  disco, que ya estan.
