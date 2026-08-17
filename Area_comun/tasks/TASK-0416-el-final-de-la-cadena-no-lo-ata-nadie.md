---
id: TASK-0416
title: El final de la cadena no lo ata nadie -- quitar un ancla que es COLA deja la cadena valida y apaga el control
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0416-el-final-de-la-cadena-no-lo-ata-nadie.md
created: 2026-08-18
reviewer: Analista
intake:
  type: infra
  goal: >
    Sexta y ultima variante de la familia de TASK-0414, medida por el checker sobre la cadena REAL al
    cerrar r5. r5 hizo FATAL la ausencia del registro cuando la cadena tiene anclas, con lo que toda
    la carga del control quedo en una sola pregunta: tiene anclas la cadena? Y esa pregunta se puede
    responder que NO borrando el ancla.
    Medido sobre el prefijo genuino de la cadena real hasta seq 9764, con los `prev_hash` de
    produccion: `validate_chain(prefijo)` da `valid True`; `validate_chain(prefijo menos la cola)` da
    `valid True` con 9091 eventos y **SIN hueco**; y con el registro borrado el guardia devuelve
    `registry_absent / valid True`, es decir, el control APAGADO. Quitar la cola no rompe ningun
    `prev_hash` porque cada evento encadena hacia atras y nadie encadena hacia el que ya no esta.
    **El genesis pineado ata el PRINCIPIO de la cadena; nada ata el FINAL.** Y no hay pin externo que
    lo compense: hay CERO eventos `chain.anchor`, luego `validate_eventlog_anchors` es hoy una puerta
    vacua (`checked=0`).
    Hoy este vector solo lo caza el detector de huecos de `validate_collaboration_state.py` (EXIT 1,
    `gap at seq 9765`) y **solo porque hay 69 eventos detras del ancla**, lo cual es un accidente
    temporal: en el instante en que un ancla se escribe, el ancla ES la cola, y lo fue durante todo
    r4c. Ademas `protocol_state_drift` no llama a `validate_chain` en ningun punto: la CLI de drift
    sale EXIT 0 `verdict=CLEAN` teniendo delante un hueco de seq.
    Se abre como agujero de DISCRIMINANTE sobre lo ya medido; la reproduccion extremo a extremo es un
    AC interno, no una precondicion de apertura.
  acceptance:
    - "AC1 (la cola queda atada): quitar el ultimo evento de la cadena deja de ser invisible. Se
      acredita por el par sobre el prefijo real: con la cola intacta el veredicto es valido; con la
      cola quitada y sin dejar hueco, el veredicto pasa a NO valido nombrando la causa. Hoy los dos
      dan valido."
    - "AC2 (no depende del detector de huecos): la senal de AC1 debe seguir apareciendo cuando el
      ancla ES el ultimo evento, es decir sin ningun evento detras que produzca hueco. Es la forma
      cara y la unica que r4c ejercito de verdad; si el arreglo solo funciona con eventos detras, no
      cierra nada."
    - "AC3 (extremo a extremo, AC INTERNO): reproducir el vector completo sobre el arbol -- revertir a
      seq 9763, re-materializar el estado caliente, borrar el ancla y el registro -- y comprobar que
      alguna puerta enrojece. Es la unica pieza que el checker declaro NO medida al cerrar r5."
    - "AC4 (residuo R1 de r5, absorbido aqui): ningun caso del runner ejercita las puertas extremo a
      extremo. Se acredita anadiendo al menos un caso que invoque la PUERTA real y no solo la funcion
      de validacion."
    - "AC5 (el negativo sobrevive a la coordenada): el mutante que acredite AC1 debe seguir muriendo
      si se cambia el orden de los eventos, el numero de eventos detras del ancla o el formato del
      registro. No vale un negativo atado a seq 9764."
  verification_cmd:
    - "python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/eventlog.py
    - runtime/protocol_replay.py
    - examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py
  out_of_scope:
    - "Por COMPORTAMIENTO, no por ruta: queda fuera cualquier cambio que toque protocol.config.json o
      que exija re-genesis. El genesis esta PINEADO y la re-genesis PROHIBIDA; el arreglo tiene que
      atar la cola SIN mover el principio de la cadena. Tambien queda fuera reabrir SLIP-A: las cinco
      formas que r5 cerro deben seguir cerradas, y eso se comprueba, no se supone."
  risk: high
  estimate: L
---

# TASK-0416 -- el genesis ata el principio; el final no lo ata nadie

## Origen

Sexta variante de la saga TASK-0414, medida por el checker sobre la cadena real al emitir el
veredicto OK-CERRABLE de r5. La pregunta se la hice yo en el encargo de review y la respuesta fue
**si, es alcanzable, y la cadena no lo impide**.

Evidencia completa en `Area_comun/artifacts/Analista-TASK-0414-r5-el-registro-ausente-que-ya-muerde-verdict.md`.

## El mapa completo de la familia, que es el hallazgo transferible

    r1   atacaron QUE DICE el discriminador   (signature.keyid lo escribe el forjador)
    r2   atacaron QUE DICE el ancla           (se la acunaba el mismo)
    r3   atacaron QUIEN ESCRIBE el registro   (cualquiera con un trailer Task-Id)
    r4c  atacaron QUE EL CONTROL EXISTA       (borrar el fichero -> valid True por early return)
    r5   la ausencia es FATAL si hay anclas   <- cerrado, con control historico
    r6   atacan QUE HAYA ANCLAS               <- esta

Cada ronda ataco una capa mas profunda del mismo control. r5 no fue un error: fue el paso correcto,
y su consecuencia es que **toda la carga quedo en una sola pregunta**. r6 ataca esa pregunta.

## Por que NO bloquea v1.19.1

El agujero es **preexistente**: esta identico en v1.19.0, que la instancia NOVA ya tiene como base.
Y el corte es **monotono en la direccion segura**: antes de r5 bastaba borrar el registro para apagar
el control; despues de r5 hay que borrar ademas el ancla. v1.19.1 **exige al atacante estrictamente
mas** que v1.19.0. No es regresion de nada de lo que embarca el corte, asi que viaja como **residuo
declarado**, con dueno y tarea registrada -- el mismo patron con el que v1.19.0 salio con seis.
