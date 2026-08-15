---
id: TASK-0407
title: El marcador de parada del peon no para -- se comprueba solo al principio del ciclo, asi que el lote entero se ejecuta y el log promete lo contrario
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0407-el-marcador-de-parada-no-para-hasta-agotar-el-lote.md
created: 2026-08-16
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-7 del reporte de NOVA, encontrado por ellos EJERCIENDO el control -- el operador
    autorizo parar al maker para que el checker drenara tres entregas sin verificar. Es el peor sitio
    donde descubrir que un mando no hace lo que dice.

    Verificado en el hub el 2026-08-16, `scripts/harness/peer_mailbox_cron.ps1:1701`:

        foreach ($message in $messages) {
            Invoke-PeerForMessage -Message $message
        }

    Ni el `foreach` ni `Invoke-PeerForMessage` vuelven a mirar el marcador de parada. Se comprueba
    SOLO al principio del `while ($true)`, asi que una vez enumerado el lote se ejecuta entero. Con
    seis mensajes de ~20 minutos, "para" significa "para dentro de dos horas".

    Medido por ellos: marcador puesto a las `21:24:23`; el log empieza a decir
    `Stop marker detected; waiting for current exec`; y a las `21:30:32` -- SEIS MINUTOS DESPUES, con
    el marcador puesto todo el rato -- el arnes registra `EXEC_START` de un exec NUEVO y vuelve a
    decir que espera.

    **Lo grave no es el retraso, es el mensaje.** `waiting for current exec` le dice al operador que
    saldra cuando ESE exec termine. Saldra cuando termine EL LOTE. Un mando de emergencia que informa
    mal de su propio alcance es peor que no tenerlo, porque se confia en el y se planifica con esa
    creencia.
  acceptance:
    - "AC1 (reproducir la mentira, no solo el retraso): con un lote de al menos dos mensajes, poner el
      marcador durante el primer exec y capturar (a) el texto que emite y (b) el `EXEC_START` del
      segundo. Las dos mitades: el retraso solo no demuestra que el mensaje engane."
    - "AC2 (el marcador corta el lote): tras el cambio, puesto el marcador durante un exec, NO arranca
      ningun exec nuevo del lote. Se acredita con el par de AC1 repetido, mostrando la ausencia del
      segundo `EXEC_START`."
    - "AC3 (el texto dice la verdad): el mensaje nombra su alcance real -- cuantos quedan del lote, o
      que va a salir tras el exec actual -- de forma que el operador pueda planificar con el. Un
      arreglo que corte el lote pero siga diciendo lo mismo no acredita: la mitad del defecto es
      informativa."
    - "AC4 (no se mata el trabajo en curso): el exec que ya esta corriendo termina de forma ordenada y
      su entrega no se pierde. Parada != matar. Se acredita comprobando que su commit y su transicion
      de ledger quedan completos."
    - "AC5 (higiene del log, de propina y medido por NOVA): la comprobacion intermedia corre dentro de
      un `WaitForExit(1000)` y escribe UNA LINEA POR SEGUNDO mientras espera -- 392 lineas en siete
      minutos sobre un log que ya iba por 180 KB. Registrarlo una vez, o cada N latidos. No es
      cosmetica: en NOVA esa inundacion ROMPIO el vigia de higiene, que decidia por `grep EXEC_RUNNING`
      sobre el log."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/
  out_of_scope: >
    NO se rediseña el modelo de lotes ni la enumeracion de mensajes. NO se toca el guardian de residuo
    (TASK-0405, TASK-0406) ni la interseccion de alcances (0337, 0387).
  risk: high
  estimate: M
---

# TASK-0407 -- un mando de emergencia que informa mal de su propio alcance

## Procedencia

Defecto **D-7** del reporte de campo de NOVA, encontrado ejerciendo el control con autorizacion del
operador. Verificado en el hub: `peer_mailbox_cron.ps1:1701`, mismo `foreach` sin comprobacion.

## El detalle que lo convierte en cascada

La inundacion del log de AC5 no es un adorno: en NOVA **rompio el vigia de higiene**, que decidia si
habia peones ejecutando por `grep EXEC_RUNNING` sobre ese mismo log. Un defecto del arnes tumbo al
vigia que vigilaba al arnes.

-- Arquitecto, 2026-08-16
