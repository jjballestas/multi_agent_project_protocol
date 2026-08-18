---
id: TASK-0417
title: El informe de actualizacion compara la ruta de STAGING y nunca la que la instancia consume
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0417-el-informe-compara-la-ruta-de-staging-no-la-consumida.md
created: 2026-08-18
reviewer: Analista
intake:
  type: infra
  goal: >
    Confirmado POR CONDUCTA por el checker al juzgar TASK-0394. `classify()` de
    `scripts/upgrade_instance.py` compara `master/rel` contra `instance/rel` **a la misma ruta
    relativa**. Pero `new_instance.py:501-507` despliega los masters de skills desde
    `scripts/instance_assets/claude-skills/X/` a `<gov>/.claude/skills/X/`, y `.claude/**` no
    pertenece a ningun glob del conjunto adoptable. Resultado medido: el checker inyecto divergencia
    real en el fichero que la instancia CONSUME
    (`<inst>/.claude/skills/mailbox-hygiene/SKILL.md`) y `upgrade_instance.py` salio **EXIT 0** con
    **cero filas** sobre esa ruta, mientras emitia una fila "nuevo" sobre la ruta de STAGING que
    nadie lee.
    El fondo, y es mas ancho que las skills: el conjunto adoptable necesita un mapeo
    `master_rel -> instance_rel`. Hoy esa relacion es **la identidad y es la unica posible**, asi que
    **todo master que se despliegue reubicado sera invisible al informe**. Las skills son el caso que
    ya se manifiesta, no necesariamente el unico.
    Consecuencia operativa: un adoptante que lea el informe concluye que sus skills estan al dia
    cuando pueden no estarlo. Es un verde que no discrimina en el ULTIMO eslabon -- el que decide que
    llega a las instancias.
  acceptance:
    - "AC1 (la divergencia consumida se ve): con el fichero que la instancia CONSUME divergente del
      master del que deriva, el informe lo reporta como cambiado. Se acredita con la reproduccion del
      checker: inyectar divergencia en `<inst>/.claude/skills/<X>/SKILL.md` debe dejar de salir EXIT
      0 con cero filas sobre esa ruta."
    - "AC2 (el mapeo se DECLARA, no se cablea caso a caso): existe una relacion explicita
      `master_rel -> instance_rel` que el informe consulta. Anadir el caso de las skills a mano
      satisface AC1 y NO satisface este: el siguiente master reubicado repetiria el defecto en
      silencio."
    - "AC3 (el negativo, por MUTACION): declarar un master nuevo que se despliegue reubicado y NO
      registrarlo en el mapeo debe ENROJECER. Si el informe sale verde, el mapeo es documentacion y
      no un control."
    - "AC4 (no se rompe lo que hoy funciona): las rutas cuyo mapeo ES la identidad siguen
      comparandose igual. Se acredita por censo diferencial antes/despues, sin diferencias fuera de
      las rutas reubicadas."
  verification_cmd:
    - "python scripts/upgrade_instance.py --instance <instancia>"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/upgrade_instance.py
    - scripts/upgrade_instance.ps1
  out_of_scope:
    - "Por COMPORTAMIENTO: queda fuera cambiar QUE ficheros son adoptables (eso es TASK-0394) y queda
      fuera la paridad de contenido entre las skills vivas del hub y sus masters, que es un defecto
      distinto. Lo que entra aqui es unicamente que el informe compare la ruta que la instancia
      realmente lee."
  risk: high
  estimate: M
---

# TASK-0417 -- el ultimo eslabon informa sobre un fichero que nadie lee

## Origen

Punto D del encargo de review de TASK-0394, planteado por el Arquitecto y **confirmado por conducta**
por el checker, que lo dejo fuera de 0394 a proposito.

    printf '# divergent local copy...' > <inst>/.claude/skills/mailbox-hygiene/SKILL.md
    python scripts/upgrade_instance.py --instance <inst>        EXIT 0

    fila sobre la ruta de STAGING (scripts/instance_assets/...)  ->  "nuevo"
    filas sobre la ruta CONSUMIDA (.claude/skills/...)           ->  0

## Por que importa mas de lo que parece

Arreglar el conjunto adoptable (0394) hace que el arnes y las skills **viajen**. Este defecto hace
que, una vez viajan, **nadie pueda comprobar si llegaron ni si divergieron**. Son dos mitades del
mismo canal y sin la segunda la primera no se puede acreditar.

Dato de campo, medido contra la instancia real: NOVA tiene **8** skills, el master **5**, y tres de
las suyas nunca estuvieron en el master -- llegaron copiadas a mano. Su `mailbox-hygiene` es un
tercer estado: 187 lineas frente a 197 del master y 248 del vivo del hub. **El informe de
actualizacion no ve nada de eso.**
