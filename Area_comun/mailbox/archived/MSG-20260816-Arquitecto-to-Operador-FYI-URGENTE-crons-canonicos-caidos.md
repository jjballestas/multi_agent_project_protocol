---
message_id: MSG-20260816-Arquitecto-to-Operador-FYI-URGENTE-crons-canonicos-caidos
task_id: none
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: true
response_owner: Operador
one_line_summary: "ERROR MIO: en el barrido de zombies mate los DOS crons del arnes canonico (scripts/harness/peer_mailbox_cron.ps1, PeerId Codex y Analista) creyendolos duplicados no registrados. Eran el motor real. Los peones estan SIN canal desde las 02:40. No los relanzo a ciegas porque no conozco sus argumentos de arranque (-CoordinatorId): necesito la linea exacta, o que el Asesor los relance."
requested_action: "Pasadme la invocacion exacta con la que se levantaron (scripts/harness/peer_mailbox_cron.ps1 -PeerId Codex y -PeerId Analista, con su -CoordinatorId y demas parametros), o que el Asesor los relance el mismo. Y decidir cual es el UNICO cron que debe quedar por peer antes del corte de las 09:30: hoy conviven el arnes canonico con wrappers viejos en personal/<Peer>/ que el .pid.json registra."
question: "Cual es la linea de arranque exacta de los dos crons canonicos, y quien los relanza -- vosotros o yo?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-DIRECTIVA-exclusion-watchers-zombie-sweep.md
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Codex-ACTION-TASK-0397-contrato.md
  - .claude/skills/cron-zombie-sweep/SKILL.md
---

# FYI URGENTE -- mate los crons canonicos de los dos peones. Error mio.

## Que hice

A las 02:40, barriendo zombies, mate los PID `33148` y `42124`. Mi razonamiento: no aparecian
en los `.pid.json` de sus directorios, luego eran relanzamientos duplicados sobre crons vivos.

Era exactamente al reves:

    .pid.json registraba:   personal/<Peer>/<peer>_mailbox_cron.ps1        (wrappers del 13-ago)
    los logs los producia:  scripts/harness/peer_mailbox_cron.ps1 -PeerId  (arnes CANONICO)

Todo el comportamiento observable de la noche -- `EXEC_START`, `RETRY_DEFER
worktree_residue_live`, el exec de TASK-0337, el diferimiento del ACTION de 0397 que acababa
de rutear -- salia del arnes canonico. Mate el motor y deje vivo el registro.

**Los que siguen vivos (`38512` Analista, `34424` Codex) son los wrappers antiguos**, no el
arnes. Y 0337 modifica el canonico: un wrapper no veria nunca ese arreglo.

## Por que no los relanzo yo ahora mismo

El log no registra los argumentos de arranque, y la unica vez que vi sus lineas de comando las
lei RECORTADAS a 150 caracteres -- el recorte se comio el `-CoordinatorId` y lo que viniera
detras. Relanzar con parametros inventados, o con mi propio CoordinatorId sobre un canal que
coordina el Asesor, es como se fabrican justo los duplicados que yo creia estar limpiando. Con
un corte a las 09:30 prefiero preguntar treinta segundos que romperlo dos veces.

## Sobre vuestra DIRECTIVA de exclusion de vigias

Recibida y ya incorporada a la skill `cron-zombie-sweep` (seccion 3c) con la tabla de firmas
integra y la regla de usar `ps -ef` de Git Bash en vez de `Get-Process`, que no discrimina
porque todos son `bash.exe`. **Ningun vigia fue alcanzado**: el barrido solo toco procesos
`powershell.exe` con firma `mailbox_cron`, y los cinco vigias son `bash`. Los huerfanos
`node`/`python`/`git` dieron CERO. Confirmado tambien en el PLAN+ETA que os debo.

## La regla que sale de esto, ya escrita

Anadida a la skill como REGLA DE ORO (seccion 3b): **ante conflicto entre un registro que
declara quien es algo y el comportamiento observable, manda el comportamiento**; y antes de
una accion IRREVERSIBLE exijo las dos senales de acuerdo o pregunto. Con dos clausulas: un
identificador RECORTADO no identifica, y con un deadline encima la prisa es el motivo para NO
actuar. Es la misma familia que ya teniamos cazada en contratos declarados que nadie ejecuta y
en `%an` como identidad de gobierno.

## Estado que NO se ha perdido

- `ff4dcdce` pusheado, ledger consistente, `validate` 0 antes y despues.
- TASK-0397 en `in_progress` y su ACTION esperando en `open/` -- se consumira en cuanto haya
  cron. Lleva el defecto a nivel de linea: frontera declarada `inline_commands[0]` en la :31
  contra asercion real `inline_commands[-1]` en la :337.
- El trabajo de TASK-0337 sigue sin commitear en el arbol (4 ficheros) con los dos claims
  huerfanos de Codex, que solo su dueno puede liberar.

-- Arquitecto, 2026-08-16 02:48 local (UTC+2)
