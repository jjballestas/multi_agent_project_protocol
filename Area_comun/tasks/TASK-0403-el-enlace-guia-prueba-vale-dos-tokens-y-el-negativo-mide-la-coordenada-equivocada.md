---
id: TASK-0403
title: El enlace guia-prueba vale dos tokens y el negativo de falsos positivos mide la coordenada equivocada -- reescribir la guia por otra via la deja verde
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0403-el-enlace-guia-prueba-vale-dos-tokens-y-el-negativo-mide-la-coordenada-equivocada.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Residuos N-A y N-C del veredicto del Analista sobre TASK-0392 r2
    (`Area_comun/artifacts/Analista-TASK-0392-r2-enlace-guia-prueba-verdict.md`). Declarados
    explicitamente como tareas nuevas, NO como remediacion de 0392, que cierra con OK-CLOSABLE.

    **N-A, la de mas peso.** El enlace entre la guia `skills/session-watchdogs.skill.md` y su prueba
    `scripts/harness/test_session_watchdog_filter.py` vale **dos tokens**: la prueba comprueba que la
    guia contiene el literal `<SELF_COMMIT_FILTER>`. Si alguien reescribe la guia para volver a
    prescribir filtrado por identidad SIN usar ese literal, la prueba sigue en verde. El contrato
    esta atado a una CADENA, no a la propiedad.

    Y la propiedad importa: filtrar por identidad es exactamente el defecto que 0392 vino a cerrar --
    un vigia que descarta commits por quien los firma se queda ciego al agente que mas le importa
    vigilar. Un candado de dos tokens sobre esa propiedad es un candado con la llave puesta.

    **N-C.** La asercion de falsos positivos mide el asunto del commit en el **campo 0**, que es la
    posicion del hash. En la coordenada real -- primera linea del campo 2 -- los casos C2 y C3 siguen
    filtrados. Palabras del Analista: *"el comportamiento es residuo aceptable, el verde que lo
    certifica no"*. Es decir: no se pide cambiar el comportamiento, se pide que el verde deje de
    certificar algo que no ha mirado.
  acceptance:
    - "AC1 (N-A, negativo por CLASE y no por cadena): la prueba falla si la guia ordena descartar por
      CUALQUIERA de autor, committer, proveedor, modelo o co-autor, use el literal que use. Se
      acredita con un gate de mutacion sobre una REESCRITURA de la guia que prescriba lo prohibido
      con otras palabras -- no sobre el texto viejo, que ya se sabe que muere."
    - "AC2 (N-A, el control): una reescritura LEGITIMA de la guia -- que no prescriba filtrado por
      identidad -- deja la prueba en verde. Sin este control, AC1 se satisface con un negativo que
      salta siempre, y eso no es un candado, es ruido."
    - "AC3 (N-C, la coordenada correcta): la asercion de falsos positivos mide el asunto donde el
      asunto esta -- primera linea del campo 2 -- o se retira. Si se corrige y entonces C2 y C3
      resultan filtrados, ESO es el hallazgo y se reporta; no se ajusta la asercion hasta que pase."
    - "AC4 (que el verde siga significando algo): tras el cambio, los negativos que 0392 dejo vivos
      -- el nombre no parseable que se descarta en silencio, y el nombre valido que debe dar
      exactamente una alerta -- siguen muriendo cuando se rompen. Se acredita ejecutandolos."
  verification_cmd:
    - "python scripts/harness/test_session_watchdog_filter.py --scratch-root D:/Aegis_Scratch/protocol/t403"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/
    - skills/
  out_of_scope: >
    NO se reabre TASK-0392, que cierra con OK-CLOSABLE. NO se toca el reparto por tiers -- el residuo
    N-B del mismo veredicto (la guia viaja y su prueba no, en el tier `coordination`, via
    `scripts/new_instance.py`) va con la familia de TASK-0394, no aqui. NO se cambia el
    COMPORTAMIENTO de filtrado de falsos positivos: N-C pide arreglar la MEDICION, no el
    comportamiento, que el Analista declara residuo aceptable.
  risk: medium
  estimate: M
---

# TASK-0403 -- un candado de dos tokens y un negativo que mide donde no es

## Procedencia

Residuos N-A y N-C declarados por el Analista al dar OK-CLOSABLE a TASK-0392 r2. El propio veredicto
los propone como tareas nuevas y no como otra vuelta de 0392.

## Lo que une a los dos

Los dos son la misma forma de verde vacio: un control que certifica una propiedad **sin mirarla**.
N-A mira una cadena en vez de la clase de instruccion; N-C mira el campo 0 en vez de donde vive el
asunto. En ambos casos el comportamiento puede ser aceptable -- lo que no lo es es el verde.

-- Arquitecto, 2026-08-15
