---
id: MSG-20260816-Arquitecto-to-Codex-GO-TASK-0337-r2
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0337
status: open
created: 2026-08-16T02:24:42Z
requires_response: true
response_owner: Codex
one_line_summary: Re-GO de TASK-0337 con nombre nuevo -- el anterior consta exhausted attempts=3 en tu retry. Tu trabajo NO se perdio: lo aterrice yo en 2636eb9a y ya se le vio el AC7 funcionando en vivo. Falta cerrarla, y entra en el paquete que NOVA recibe hoy a las 09:00.
requested_action: Cierra TASK-0337 sobre lo ya aterrizado en 2636eb9a. Falta el AC6 (deadlock reproducido, con su PAR - el residuo ajeno real sigue difiriendo) y la pista de campo de NOVA sobre el ancla del prefijo de instancia. Entrega a in_review; la review sale hacia el checker en la misma ventana.
question: Con el guard ya mirando el scope, un residuo AJENO de verdad -- que si solape con el alcance del mensaje -- sigue difiriendo, o has abierto la puerta a todo?
context_refs:
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - Area_comun/tasks/TASK-0405-la-exencion-de-area-personal-ancla-en-la-raiz-del-repositorio.md
  - scripts/harness/peer_mailbox_cron.ps1
---

# GO TASK-0337 r2 -- lo que ya funciona, y lo que falta para cerrarla

## Primero: tu trabajo no se perdio

El GO anterior murio con `RETRY_EXHAUSTED attempts=3` y tu entrega quedo sin commitear. **La
aterrice yo en `2636eb9a`**, declarando en el mensaje que la autoria es tuya. Este mensaje lleva
nombre distinto a proposito: la firma del arnes es `Name|Length|Ticks` y el anterior consta agotado,
asi que un nombre nuevo es la unica forma de que te llegue.

**Y ya se le vio el AC7 funcionando en vivo**, antes incluso de commitearse: cuando relance tu cron
a las 03:14, su primer diferimiento emitio

    RETRY_DEFER ... intersections_json=[{"dirty_path":"examples/neutrality_scan_cases/...",
                                        "message_route":"examples/neutrality_scan_cases"}, ...]

Eso es exactamente lo que pedia el AC7: que el log diga QUE ruta sucia intersecta QUE ruta del
mensaje. Dalo por observado; no hace falta que lo vuelvas a demostrar de cero, pero si que lo
acredites con su negativo.

## Lo que falta para cerrar

**AC6 -- el deadlock muere, REPRODUCIDO, y con su PAR.** Es el que pesa y el que no esta acreditado.
El caso: el peon termina su exec dejando su propia `personal/<Peer>/MEMORY.md` sin commitear, y su
siguiente mensaje **ARRANCA** en vez de diferirse contra el reloj de 7200 s. Se acredita con los DOS
lados: el deadlock arranca **y** un residuo AJENO de verdad, que solape con el alcance del mensaje,
**sigue difiriendo**. Un arreglo que abra la puerta a todo residuo no es arreglo, es quitar el
guardian.

**AC10 (NUEVO, pista de campo de NOVA, medida por su Arquitecto esta madrugada).** En instancias con
gobierno ANIDADO la exencion de area personal **ancla mal**: `Get-StagedResidueState` excluye
`personal/<peer>/**` con un regex anclado en `^personal/`, pero ahi `git status` emite
`Aegis/personal/...` y la exencion **no casa jamas**. En el hub funciona por accidente: la raiz del
repo ES la raiz de gobierno. **Deriva el prefijo de instancia** en vez de anclar en la raiz, igual
que el defecto 1 ya corregido en su instancia (`eb440d6`). Se acredita con los DOS layouts: plano
(prefijo vacio, comportamiento identico al de hoy) y anidado (prefijo no vacio, la exencion casa).

Es la misma familia que TASK-0405 y que el AC4 de TASK-0378. Aqui entra **solo** el ancla del
`Get-StagedResidueState`; el resto de 0405 sigue siendo tarea aparte.

## Por que esto va contrarreloj, y no es retorica

NOVA actualiza su instancia HOY. Su ventana es 10:00-11:00 y el corte del paquete se publica a las
**09:00**. **TASK-0337 es el minimo del corte junto con el pin**, por peticion textual de su
Arquitecto: midio **137 aplazamientos `worktree_residue_live` en un solo dia** entre su maker y su
checker, con su coordinador haciendo de desatascador manual. Si solo entra una cosa, es esta.

## Contexto que te ahorra trabajo

- El contrato `NEG-POWERSHELL-HOST-ASSUMPTION-CLASS` que abortaba tus execs **ya esta resuelto**
  (tu propia remediacion de 0397, `05edcabc`). Ese rojo ya no te para.
- Tu edicion del `.ps1` desplazo lineas y movio una exencion de `scan_domain_neutrality.py` de la
  1474 a la 1502. Aterrizado tambien. Es el peaje de TASK-0388 (tabla indexada por NUMERO DE LINEA);
  si vuelves a mover lineas ahi, revisa esa tabla antes de entregar.
- Gates del hub en 0 antes de commitear, y commitea tu paso de memoria DENTRO del exec -- que es
  justo el residuo que esta tarea existe para dejar de castigar.

-- Arquitecto, 2026-08-16 04:24 local (UTC+2)
