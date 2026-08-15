---
id: TASK-0401
title: El rollback destruye el residuo ambiguo que dice preservar -- y solo en CI, asi que la garantia de "no te borro lo que no se leer" no se sostiene donde importa
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0401-el-rollback-destruye-el-residuo-ambiguo-que-dice-preservar.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Quinta causa de la CI roja, descubierta al reparar la primera. Lo reporto Codex al cerrar el
    arreglo de TASK-0396 y lo verifico el Arquitecto sobre el run `31901179492`, commit `a30442c2`,
    job `falsification-runners`:

        assert (sandbox / "ambiguous-residue.txt").exists(), "mid-log ambiguity was rolled back"
        AssertionError: mid-log ambiguity was rolled back

    La asercion vive en `examples/mailbox_retry_cases/run_mailbox_retry_cases.py:2122` y comprueba una
    propiedad de PRESERVACION del rollback del arnes: cuando el arnes revierte un exec, el material
    cuyo estado no sabe interpretar -- aqui una linea de ledger ambigua, `{not-json` -- debe
    SOBREVIVIR. La idea es "si no se leerlo, no lo borro". En CI no sobrevivio.

    Por que esto no es un rojo mas de la lista. El rollback del arnes es el mismo mecanismo que
    cuarentena ficheros del arbol durante un exec, y lo hace a diario: el 2026-08-15 me cuarentena a
    mi un fichero de mi propia area personal (`ROLLBACK_QUARANTINED`). Si ese mecanismo destruye
    material que declara preservar, el riesgo no es una prueba en rojo: es perdida de trabajo en
    cualquier instancia que adopte la metodologia, y NOVA es la primera.

    Y hay una segunda lectura, obligatoria antes de tocar codigo: el caso pasa en local y falla en CI.
    O el rollback destruye de verdad y el entorno local lo enmascara, o el sandbox de la prueba no se
    construye igual en los dos sitios. Es la misma disyuntiva de TASK-0398, y como alli, elegir por
    comodidad convierte un hallazgo en un estorbo. Empezar por AVERIGUAR CUAL.
  acceptance:
    - "AC1 (nombrar el hecho antes de arreglar nada): determinar si `ambiguous-residue.txt` llega a
      existir antes del rollback en el entorno de CI. Si nunca se creo, el fallo es de construccion
      del sandbox; si existia y desaparecio, el rollback lo destruyo. Reportar cual de las dos, con
      la evidencia, ANTES de proponer arreglo."
    - "AC2 (si es destruccion real): el rollback deja de borrar el material ambiguo, y se acredita
      con el par -- material ambiguo presente antes, presente despues -- ejecutado, no razonado."
    - "AC3 (si es el sandbox): la prueba construye su material ambiguo igual en Linux y en Windows, y
      da el mismo veredicto en ambos hosts sobre el mismo commit. Es la propiedad que hoy falta."
    - "AC4 (el negativo sigue cazando su defecto): tras el cambio, un rollback que SI destruya el
      material ambiguo sale en exit 1, con el control en 0. Si el arreglo consiste en relajar o
      eliminar la asercion, el AC no se da por cumplido -- esa asercion es la unica que hoy vigila
      esta garantia."
    - "AC5 (CI, en forma discriminante): sobre el commit de entrega, la firma
      `mid-log ambiguity was rolled back` desaparece del log del job `falsification-runners` Y la
      ejecucion avanza mas alla de esa linea. NO se exige el job entero en verde: ese job carga otras
      causas registradas por separado, y exigir su verde haria el AC insatisfacible."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/
    - scripts/harness/
    - scripts/
  out_of_scope: >
    NO se toca el bloque del fixture de TASK-0301 (TASK-0396) ni el estimulo de TASK-0343
    (TASK-0395, en revision) dentro del mismo fichero: esta tarea entra SOLO por la preservacion del
    material ambiguo en el rollback y su sandbox. NO se tocan las otras cuatro causas rojas
    (TASK-0396, 0397, 0398, 0399). Si el arreglo resulta estar en el rollback de
    `scripts/harness/peer_mailbox_cron.ps1`, se puede tocar ahi -- el defecto manda sobre la ruta.
  risk: high
  estimate: M
---

# TASK-0401 -- el rollback destruye el residuo ambiguo que dice preservar

## Evidencia

Run `31901179492`, commit `a30442c2`, job `falsification-runners` (runner Windows propio):

    assert (sandbox / "ambiguous-residue.txt").exists(), "mid-log ambiguity was rolled back"
    AssertionError: mid-log ambiguity was rolled back

Las aserciones vecinas -- que el archivo de mailbox firmado, el archive de poda y el documento de
decision sobreviven al rollback -- SI pasaron. Solo cayo la del material ambiguo.

## Procedencia

Descubierta al reparar TASK-0396: con la causa de la directiva de ejecucion resuelta, el runner
avanzo y encontro esta. Codex la reporto sin absorberla en su tarea, que es exactamente lo que su AC5
pedia.

## Por que la trato como riesgo y no como rojo

El rollback del arnes cuarentena ficheros del arbol de trabajo durante los exec. Si el material que
no sabe interpretar puede desaparecer, el riesgo es perdida de trabajo real en cualquier instancia
adoptante.

-- Arquitecto, 2026-08-15
