---
id: TASK-0391
title: El orden de la cola lo fija el NOMBRE DEL FICHERO y no esta documentado -- la prioridad declarada en el mensaje no tiene ningun efecto
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0391-el-orden-de-la-cola-lo-fija-el-nombre-del-fichero.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-3 del informe de campo de la instancia NOVA (2026-08-15), primer uso real de la
    metodologia de principio a fin. El cron consume `Area_comun/mailbox/open/` en **orden alfabetico
    del nombre del fichero** -- `Get-ChildItem -Filter "MSG-*.md"` sin `Sort-Object` explicito
    (`peer_mailbox_cron.ps1:1348`) -- y la prioridad declarada DENTRO del mensaje no tiene ningun
    efecto. Verificado en el hub por lectura del codigo. Caso medido en NOVA: se ruteo un encargo de
    seguridad de prioridad alta como `...-GO-09-...` diciendo explicitamente en el cuerpo "Posicion:
    la PRIMERA, por delante de GO-04, GO-05 y GO-06", y el cron arranco **GO-04** dos minutos
    despues. Los `ACTION-*` se consumen antes que los `GO-*` por el mismo motivo -- la A va antes que
    la G --, no por semantica. Clase del defecto: **un contrato IMPLICITO que se descubre por
    accidente**. Hoy la unica palanca de prioridad es como nombras el fichero, y eso no esta escrito
    en ningun sitio; un coordinador que declare prioridad en el cuerpo cree estar priorizando y no lo
    hace.
  acceptance:
    - "AC1 (el orden es explicito y declarado): el criterio de ordenacion de la cola queda escrito en
      la documentacion del arnes y en el propio codigo con un `Sort-Object` explicito, de modo que
      leerlo no dependa del comportamiento por defecto de `Get-ChildItem`. Se acredita con el texto y
      con el codigo, no con uno de los dos."
    - "AC2 (si hay prioridad, es un campo): la prioridad se declara en el frontmatter y el cron ordena
      por ella. Se acredita por conducta: dos mensajes cuyo orden alfabetico es el CONTRARIO al de su
      prioridad declarada, y el cron consume primero el prioritario. El caso de NOVA -- GO-09 antes
      que GO-04 -- reproducido y en verde."
    - "AC3 (empate resuelto y estable): con prioridades iguales el orden sigue siendo determinista y
      documentado (por ejemplo antiguedad), no un artefacto del sistema de ficheros. Se acredita con
      dos corridas sobre la misma cola dando el mismo orden."
    - "AC4 (compatibilidad): los mensajes SIN campo de prioridad siguen procesandose como hoy, sin que
      su orden relativo cambie. Medido, no afirmado -- media metodologia esta ruteada con el
      contrato viejo."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/harness/README.md
  out_of_scope:
    - "Cambiar la profundidad de cola o el reloj del defer (7200 s). Es otra propiedad y va con
      TASK-0337."
    - "Renombrar los mensajes ya ruteados para forzar un orden: es el rodeo que esta tarea existe para
      eliminar."
  risk: medium
  estimate: S
---

# TASK-0391 -- la prioridad que no prioriza

## Lo medido

En el hub, por lectura del codigo:

    peer_mailbox_cron.ps1:1348
    Get-ChildItem -LiteralPath $openDir -File -Filter "MSG-*.md" | Where-Object { ... }

Sin `Sort-Object`. El orden es el que devuelve el proveedor, que en la practica es alfabetico por
nombre.

En NOVA, por conducta: un GO de seguridad marcado como primero en el cuerpo del mensaje quedo el
cuarto, y el cron arranco `GO-04` dos minutos despues de recibir `GO-09`.

## Por que importa mas de lo que parece

Porque el coordinador CREE que esta priorizando. Escribe "esta va primero" en un mensaje, el sistema
lo acepta sin protestar, y hace otra cosa. No hay error, no hay aviso: hay un contrato implicito que
solo se aprende chocando con el. En una cola donde un mensaje muere a las dos horas, el orden no es
cosmetico.
