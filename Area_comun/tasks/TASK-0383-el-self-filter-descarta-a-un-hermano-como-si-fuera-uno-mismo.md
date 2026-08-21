---
id: TASK-0383
title: El self-filter descarta a una sesion hermana como si fuera uno mismo, y el lease avisa pero no controla
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0383-el-self-filter-descarta-a-un-hermano-como-si-fuera-uno-mismo.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Leccion 2 del informe de campo de la instancia NOVA, verificada por mi contra mis propias
    herramientas. Dos sesiones de Arquitecto operaron la misma instancia durante horas siendo
    INVISIBLES la una para la otra por construccion: el self-filter de los monitores descarta los
    commits propios por la firma `Co-Authored-By: Claude (Opus|Fable|Sonnet)`, que es una firma de
    MODELO -- asi que cada sesion filtraba los commits de la hermana como si fueran suyos. Lo
    comprobe en mi propia skill: el patron discrimina por modelo, no por sesion. Y el lease de
    instancia unica, que existe para impedirlo, es DECLARATIVO: la sesion hermana nunca lo leyo ni lo
    refresco, y nada se lo impidio. El coste no fue teorico -- ruteo al checker una entrega que la
    otra sesion tenia verificada como incompleta, y la evidencia no viajo en el encargo porque no lo
    escribio quien la tenia.
  acceptance:
    - "AC1 (el self-filter discrimina por SESION): el monitor de entregas identifica lo propio por
      identificador de sesion, no por firma de modelo. Se acredita con el PAR: un commit de la propia
      sesion se filtra, y un commit de una sesion hermana del MISMO modelo NO se filtra y despierta al
      monitor. Filtrar por modelo es lo que hay hoy y es el defecto."
    - "AC2 (el lease deja de ser un aviso): `submit_intent` estampa el identificador de sesion del
      actor y AVISA cuando no coincide con el lease vivo. Se acredita por conducta con dos sesiones
      simuladas: la que no tiene el lease recibe la senal. Un lease que solo se lee si alguien decide
      leerlo no es un control."
    - "AC3 (avisar, no bloquear -- y declarado): el aviso del AC2 no impide operar. Una segunda sesion
      legitima (relevo, arranque tras caida) debe poder trabajar; lo que no debe es hacerlo sin
      enterarse. Se declara explicitamente por que se elige avisar y no bloquear, y que caso quedaria
      roto si se bloqueara."
    - "AC4 (medido sobre el escenario REAL): se reproduce el escenario de campo -- dos sesiones del
      mismo modelo commiteando en el mismo arbol -- y se comprueba que cada una VE a la otra. Hoy
      ninguna ve a ninguna, y eso se descubrio inspeccionando un fichero a mano."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/submit_intent.py
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El diagnostico del error de idempotencia: es TASK-0382."
    - "Prohibir la doble sesion: no se decide aqui. Esta tarea hace que la doble sesion sea VISIBLE;
      si ademas debe prohibirse, es decision del operador y va aparte."
    - "El patron del self-filter en las skills del Arquitecto: lo actualizo yo cuando el AC1 fije la
      forma, porque la skill describe el procedimiento y el codigo lo implementa."
  risk: medium
  estimate: M
---

# TASK-0383 -- dos sesiones invisibles la una para la otra

## Lo que verifique en mi propia herramienta

El patron del monitor de entregas filtra por:

    Co-Authored-By: Claude (Opus|Fable|Sonnet)

Eso es una firma de MODELO. Una sesion hermana de Arquitecto firma exactamente igual, asi que **cada
monitor descarta los commits de la otra sesion creyendo que son propios**. El filtro que existe para
evitar el auto-ruido produce ceguera mutua.

## Por que el lease no lo mitigo

Porque es declarativo. Lleva el `session_id` de quien lo escribio y una nota de sesion unica, y la
sesion hermana simplemente **no lo leyo**. Nada se lo impidio y nada se lo senalo. Un control que
depende de que alguien decida consultarlo es un aviso, no un control -- la misma forma que ya
corregimos en DECISION-0113 para el contrato de liveness.

## El coste real, para que no se lea como higiene

La sesion hermana ruteo al checker una entrega que la otra tenia verificada como INCOMPLETA, y la
evidencia no viajo en ese encargo porque no lo escribio quien la tenia. No es ruido: es un juicio
emitido sin la informacion que existia a un metro.

## La frontera del arreglo

**Avisar, no bloquear.** Una segunda sesion legitima -- un relevo, un arranque tras caida -- tiene que
poder trabajar. Lo que no puede es trabajar sin enterarse de que no esta sola. Por eso el AC3 pide que
esa eleccion se declare y que se nombre el caso que se romperia al bloquear.
