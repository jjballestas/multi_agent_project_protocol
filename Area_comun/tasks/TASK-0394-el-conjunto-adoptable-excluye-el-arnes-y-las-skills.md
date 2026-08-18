---
id: TASK-0394
title: El conjunto adoptable excluye el arnes y las skills -- la via de actualizacion no transporta los ficheros donde viven los defectos reportados
status: done
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    BLOQUEANTE de la actualizacion de la instancia NOVA, descubierto al preparar su entrega.
    `scripts/upgrade_instance.py` define el conjunto adoptable con globs de UN SOLO NIVEL --
    `"scripts/*.py"` y `"scripts/*.ps1"` -- que NO alcanzan `scripts/harness/**`, y no incluye
    NINGUN glob para `skills/**`. Medido contra la instancia real
    (`/d/Agentes/NOVA-Suite/NOVA/Aegis`): el reporte declara **134 archivos adoptables** y
    `scripts/harness/peer_mailbox_cron.ps1` **no aparece**; los unicos aciertos de "harness" son
    ficheros de test que si viven en `scripts/`. Consecuencia directa: los TRES defectos que NOVA
    reporto y que el hub acepto como propios -- TASK-0337 (deadlock del guard de residuo),
    TASK-0391 (orden de la cola) y TASK-0392 (self-filter que deja el vigia mudo) -- viven en
    `scripts/harness/` y en `skills/`, asi que **aunque se arreglen perfectamente, la via
    documentada de actualizacion no se los entrega**. Clase del defecto: **el canal de entrega
    declara un conjunto que excluye lo que mas importa, y lo hace en silencio** -- el reporte se lee
    completo, con 134 ficheros y un desglose ordenado, y un lector concluye que su instancia esta
    casi al dia. Es un verde que no discrimina, en el ultimo eslabon: el que decide que llega a las
    instancias.
  acceptance:
    - "AC1 (el conjunto cubre lo que se exporta de verdad): el arnes de los peones y las skills
      entran en el conjunto adoptable. Se acredita ejecutando el reporte contra una instancia real y
      comprobando por nombre que `scripts/harness/peer_mailbox_cron.ps1` y al menos un fichero de
      `skills/` aparecen en la tabla. Hoy no aparecen."
    - "AC2 (el criterio se DERIVA, no se enumera): la definicion del conjunto deja de ser una lista
      de globs que hay que acordarse de ampliar cada vez que nace un directorio. Se declara el
      CRITERIO de pertenencia -- que hace adoptable a un fichero -- y los globs se derivan de el o se
      comprueban contra el. Si se mantiene la lista, se entrega ademas el AC3."
    - "AC3 (el hueco es detectable): existe un control que ENROJECE cuando un fichero generico del
      master queda fuera del conjunto adoptable. Se acredita por el par: crear un fichero exportable
      en un directorio no cubierto pone el control en exit 1; el conjunto correcto lo deja en 0. Sin
      esto, el siguiente directorio nuevo repite el defecto en silencio."
    - "AC4 (no ensancha hacia lo que NO debe viajar): estado vivo, mailbox, area personal, claims,
      ledger y artefactos de instancia siguen FUERA. Se acredita con la lista de exclusiones medida
      sobre el reporte, no afirmada: adoptar el estado de otra instancia seria peor que no adoptar
      nada."
    - "AC5 (el reporte dice lo que NO mira): el encabezado del reporte declara explicitamente que
      rutas del master quedan fuera del conjunto y por que. Un informe que solo enumera lo que si
      compara induce a creer que lo demas coincide."
  verification_cmd:
    - "python scripts/upgrade_instance.py --instance examples/minimal_instance"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/upgrade_instance.py
    - scripts/upgrade_instance.ps1
  out_of_scope:
    - "AMPLIACION 2026-08-15 22:22 local (Arquitecto) -- no es una exclusion, es un caso concreto que
      ENTRA en esta tarea: el residuo N-B del veredicto del Analista sobre TASK-0392 r2. En el tier
      POR DEFECTO (`coordination`) el reparto SEPARA una guia de su prueba:
      `skills/session-watchdogs.skill.md` viaja al adoptante pero
      `scripts/harness/test_session_watchdog_filter.py` no, asi que el comando del AC3 de 0392 llega
      al adoptante como exit 2 y la guia cita una ruta que en su instancia NO EXISTE. Ruta afectada:
      `scripts/new_instance.py`. Es el defecto que esta tarea ya nombra -- el canal no transporta lo
      que el adoptante necesita -- con un caso medido encima: o el arnes viaja, o la guia deja de
      citar lo que no va a estar. Se resuelve aqui, no en tarea aparte."
    - "Arreglar los defectos que hay que transportar (0337, 0391, 0392): son tareas propias. Esta
      abre el CANAL; ellas producen la carga."
    - "La discrepancia de `runtime_version` entre instancia (1.14.0) y master (0.12.0) que el mismo
      reporte muestra invertida. Se declara aqui como observacion y sale a tarea propia si se
      confirma."
    - "Automatizar la adopcion. La herramienta informa y la instancia decide por DECISION-0001; esta
      tarea no cambia ese contrato, solo lo que se informa."
  risk: high
  estimate: S
---

# TASK-0394 -- el canal que no lleva la carga

## Lo medido

    $ python scripts/upgrade_instance.py --instance /d/Agentes/NOVA-Suite/NOVA/Aegis

    Conjunto adoptable: 134 archivos (nuevo=17, cambiado=12, igual=104, eliminado=1)
    scripts/harness/peer_mailbox_cron.ps1  ->  NO APARECE
    skills/**                              ->  NO APARECE

Y la causa, en `upgrade_instance.py`:

    DEFAULT_ADOPTABLE_GLOBS = [
        ...
        "scripts/*.py",      # un solo nivel
        "scripts/*.ps1",     # un solo nivel
        ".githooks/**",      # recursivo
        "runtime/**",        # recursivo
    ]

Dos globs recursivos y dos de un nivel, sin criterio que explique la diferencia. `skills/` no figura
pese a que DECISION-0061 las declara exportables.

## Por que es bloqueante y no una mejora

Porque hay una entrega comprometida que depende de el. NOVA desarrolla hoy con una version obsoleta
y los tres defectos que reporto -- y que este hub acepto como PROPIOS -- estan en el arnes y en la
guia. Sin este arreglo, la actualizacion que se les publique **compilara, validara y no contendra lo
que fueron a buscar**.

## Por que es la misma familia de siempre

El reporte no miente: dice la verdad sobre los 134 ficheros que compara. Lo que no dice es que hay
ficheros que no compara. **Su verde no distingue "coincide" de "no lo he mirado"**, que es
exactamente el patron que el hub lleva una semana cazando en sus gates -- aqui aplicado al ultimo
eslabon, el que decide que llega a las instancias.
