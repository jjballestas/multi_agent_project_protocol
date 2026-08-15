---
id: TASK-0393
title: Un rojo TRANSITORIO del validador durante la notificacion de un peon puede consumir el mensaje como visto y perder el trabajo en silencio
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0393-rojo-transitorio-del-validador-consume-el-mensaje.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-4 del informe de campo de NOVA. `validate_collaboration_state.py` da exit 1 con
    "Handoff-release violation: task X is in_review but owner still has active claim" mientras el
    peon esta a mitad de su ciclo de notificacion: la tarea ya paso a `in_review` pero todavia
    retiene el claim de mailbox. Se despeja solo en 10-30 s. El problema no es el rojo transitorio,
    sino lo que ocurre si un mensaje cae en esa ventana: el arnes del checker PRE-GATEA, VE ROJO,
    ABORTA Y MARCA EL MENSAJE COMO VISTO -- el trabajo queda sin hacer y nadie se entera. Ocurrio 3
    veces en la ventana observada de NOVA; se esquivo esperando a verde, que es una defensa que solo
    funciona si ya conoces la trampa. AVISO DE ALCANCE: la ruta exacta pre-gate -> marcar-visto NO
    esta verificada en el hub. Lo que si esta verificado aqui es que la CLASE existe: el propio
    arnes documenta en `peer_mailbox_cron.ps1:123` un caso donde un fallo acaba "silently consuming
    the queue as seen". Por eso el AC1 es REPRODUCIR el defecto antes de arreglarlo: si no se
    reproduce, la tarea se cierra declarandolo no-presente en el hub y se avisa a NOVA, que es un
    desenlace legitimo y barato.
  acceptance:
    - "AC1 (reproducir antes de arreglar): se construye la ventana -- tarea en `in_review` con claim
      de mailbox aun activo -- y se comprueba POR CONDUCTA si un mensaje ruteado en ese instante
      queda marcado como visto sin ejecutarse. Con exit codes y con el `seen.json` antes y despues.
      Si NO se reproduce, esa medicion ES el entregable y la tarea cierra."
    - "AC2 (si se reproduce, el mensaje sobrevive): un pre-gate en rojo NO consume el mensaje. Se
      difiere y se reintenta, o se marca con una causa que lo distinga de un mensaje procesado. Se
      acredita con el par: mensaje en la ventana roja sigue pendiente; mensaje procesado consta
      visto."
    - "AC3 (el estado intermedio deja de ser rojo, o se distingue): la transicion a `in_review` y el
      release del claim de mailbox son atomicas, o el validador distingue ese intermedio de un drift
      real. Decision de diseno del Arquitecto sobre la evidencia del AC1, no antes."
    - "AC4 (prueba de que RECHAZA lo que debe): un drift REAL -- tarea `in_review` con claim de
      trabajo retenido de verdad -- sigue poniendo el validador en rojo. El arreglo no puede comprar
      el silencio a cambio de dejar de ver el caso legitimo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/validate_collaboration_state.py
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El resto de causas de pre-gate rojo. Esta tarea se ocupa del intermedio in_review mas claim de
      mailbox, no de un HEAD roto de verdad."
  risk: high
  estimate: M
---

# TASK-0393 -- el mensaje que se consume sin ejecutarse

## Por que riesgo alto pese a no estar verificado aqui

Porque el modo de fallo es el peor de todos los que hemos catalogado: **el trabajo desaparece y el
sistema queda coherente**. La tarea sigue donde estaba, el mensaje figura como visto, ningun gate
enrojece, y el coordinador cree que el checker declino. En NOVA paso tres veces en una sola ventana
de observacion.

La primera obligacion de esta tarea es por tanto **medirlo aqui**, no arreglarlo a ciegas: importar
un defecto que no existe en el hub cuesta un arreglo inutil, y darlo por inexistente sin mirar cuesta
mucho mas.
