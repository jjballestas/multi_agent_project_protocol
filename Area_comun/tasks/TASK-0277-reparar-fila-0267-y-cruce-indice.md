---
task_id: TASK-0277
title: "[TRAZABILIDAD] Reparar la fila desaparecida de TASK-0267 y cerrar la clase: cruce de ficheros de tareas contra el indice, y cobertura de los archivos de poda en el chequeo de deriva"
type: infra
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0022, TASK-0273]
linked_decisions: [DECISION-0022]
file: Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
intake:
  type: infra
  goal: "TASK-0267 (hook v2, cerrada en done el 20-jul) fue podada del indice caliente en el evento seq 5093 pero su fila NO aterrizo en TASK_INDEX_ARCHIVE.json, mientras que las podas posteriores (0270/0271 en seq 5152, 0257/0268 en seq 5214) si lo hicieron. Hoy la unidad tiene fichero en Area_comun/tasks/, claims en el archivo de claims e historia completa en el event log, pero NINGUNA fila de indice, ni caliente ni archivada. No hay perdida de informacion (el ledger es la fuente y permite reconstruirla) pero si un agujero de trazabilidad que ningun gate detecto. Detectado por el Arquitecto al preparar el reporte de estado de la tanda. Causa mas probable, el archivo de poda quedandose sin commitear y siendo revertido por una operacion posterior sobre el arbol compartido, el mismo patron que causo cuatro abortos de peers ese dia. Esta unidad repara el caso y cierra la clase, que es lo que importa."
  acceptance:
    - "La fila de TASK-0267 vuelve a existir en TASK_INDEX_ARCHIVE.json, reconstruida desde el event log (upsert de seq 4941 mas estado final done de seq 5066) y aplicada por la via gobernada, sin edicion manual del estado."
    - "El validador cruza los ficheros de Area_comun/tasks/ contra las filas de indice: todo fichero de tarea debe tener fila en el indice caliente o en el archivo, y toda fila debe tener fichero; las discrepancias son error, no aviso."
    - "El chequeo de deriva cubre tambien los archivos de poda (TASK_INDEX_ARCHIVE.json y CLAIMS_ARCHIVE.json), de modo que perder una fila archivada deje de ser invisible."
    - "La poda verifica que lo que saca del indice caliente ESTA en el archivo antes de darse por buena, y falla ruidosamente si no es asi."
    - "Barrido de comprobacion sobre todo el historico, ninguna otra fila podada falta en el archivo; el resultado se reporta con numeros."
    - "Negativos permanentes en la suite para las tres condiciones: fichero sin fila, fila sin fichero, y fila podada que no llega al archivo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py (debe seguir en verde tras la reparacion)"
    - "Runner del negativo nuevo del cruce ficheros-indice en verde"
    - "python scripts/prune_state.py --root . --check"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - runtime/
    - Area_comun/state/
  out_of_scope:
    - "Reescribir o re-firmar historia del event log - PROHIBIDO, la reparacion RECONSTRUYE la fila derivada, no toca eventos."
    - "Cambiar la politica de poda (que se poda y cuando) - FUERA, eso lo fijo TASK-0273."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: medium
  estimate: M
---

# TASK-0277 - Una unidad se evaporo del indice con todos los gates en verde

Queda en `proposed`, no en `ready`: toca `Area_comun/state/` y la reparacion de una fila
del ledger derivado, asi que espera confirmacion del Operador, a quien se le reporto el
hallazgo el 2026-07-20 a las 16:20.

Lo que vale mas que el caso concreto son los dos huecos de clase que revela. El primero,
el validador no cruza los ficheros de tareas contra las filas del indice, asi que una
unidad puede desaparecer del indice sin que nada se ponga rojo. El segundo, el chequeo de
deriva no mira los archivos de poda, asi que la perdida de una fila archivada es
literalmente invisible para el unico mecanismo que deberia verla.

Encaja en la tanda 0103 por la misma razon que TASK-0274: la clausula C3 pide que lo que
se reporta como hecho sea verificable, y una unidad sin fila no es verificable por nadie
que llegue en frio.

Remediacion iteracion 1: la validacion de selectores de scope se limita deliberadamente
a claims activas; las filas historicas released/blocked conservan fidelidad al evento
firmado aunque su scope sea anterior al contrato de selectores.

Remediacion iteracion 2: el pre-stage de espejos usa la cabeza exacta del event log para
decidir el rollback. Interrupciones antes del evento restauran; fallos despues del evento
retienen espejos y fallan con recuperacion explicita. Las filas stale se refrescan y drift
final nunca devuelve verde.
