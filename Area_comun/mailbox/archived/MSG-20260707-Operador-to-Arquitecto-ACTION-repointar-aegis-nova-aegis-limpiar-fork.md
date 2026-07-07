---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-repointar-aegis-nova-aegis-limpiar-fork
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md"
  - personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md
one_line_summary: "CORRECCION de repo: el origin de la instancia Aegis apuntaba por error al repo del FORK de Hermes (git@github.com:jjballestas/Zeus-Aegis.git). El Operador creo el repo correcto PRIVADO git@github.com:jjballestas/NOVA-Aegis.git (con deploy key + write). Re-apuntar origin, pushear el historial completo, limpiar la rama aegis/main del fork, actualizar runbook+guia."
requested_action: "En el repo de la instancia Aegis (D:/Agentes/Zeus/NOVA/Aegis): (1) git remote set-url origin git@github.com:jjballestas/NOVA-Aegis.git (la deploy key ya esta cableada por core.sshCommand del repo -> C:/Users/johnb/.ssh/NOVA-Aegis-key). (2) Pushear el historial COMPLETO de la instancia al nuevo repo (todas las ramas de trabajo: main c6cfbc7b/TASK-1203 + aegis/main; tu decides la rama canonica del modelo multi-clon). (3) VERIFICAR que NOVA-Aegis tiene todo: runbook, DECISION-1001/1002, guia de Julian, chains 1001/1002, TASK-1203. (4) Limpiar el fork: borrar la rama aegis/main que se pusheo por error a Zeus-Aegis (git push git@github.com:jjballestas/Zeus-Aegis.git --delete aegis/main, o via UI). (5) Actualizar la URL del remoto en el runbook s.1 y colocar la guia de Julian con la URL correcta NOVA-Aegis. Reportar que nada se perdio."
question: "Confirmas el re-apuntado a NOVA-Aegis + push completo + limpieza del fork + actualizacion de runbook/guia? Reporta el head del nuevo origin/main y que la verificacion (validate) sale verde tras el re-apuntado."
---

# ACTION - Re-apuntar la instancia Aegis a NOVA-Aegis + limpiar el fork

**Contexto:** el `origin` de la instancia Aegis apuntaba por ERROR al repo del fork de Hermes
(`git@github.com:jjballestas/Zeus-Aegis.git`); el trabajo de la instancia se pusheo ahi como la rama
`aegis/main`. El Operador ya creo el repo correcto PRIVADO `git@github.com:jjballestas/NOVA-Aegis.git` (vacio,
sin README, con deploy key + write access; la deploy key ya esta cableada en `core.sshCommand` del repo
local). Nombre elegido = `NOVA-Aegis` (coincide con la carpeta NOVA/Aegis, el runbook s.1 y DECISION-0087;
`Zeus-Aegis` queda reservado para el producto-front, no la instancia).

## Pasos (repo D:/Agentes/Zeus/NOVA/Aegis)
1. `git remote set-url origin git@github.com:jjballestas/NOVA-Aegis.git`
2. Push del historial COMPLETO (main + aegis/main; fija la rama canonica del modelo multi-clon a tu criterio).
3. VERIFICAR que NOVA-Aegis tiene todo (runbook, DECISION-1001/1002, guia de Julian, chains, TASK-1203); nada perdido.
4. Limpiar el fork: borrar `aegis/main` de `Zeus-Aegis` (el fork vuelve a ser solo el fork de Hermes).
5. Actualizar la URL del remoto en el runbook s.1 + colocar la guia de Julian
   (`personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md`) gobernada en Aegis con la URL correcta.

## Integridad (tranquilidad)
Mover el remoto NO rompe nada: el ledger #4 de Aegis y la cross-atestacion del hub son content-addressed
(sha256 de events.jsonl), independientes de la URL. NO requiere re-genesis. El hub/sello intactos. El
re-genesis A2 de la identidad de Julian sigue esperando su pubkey (aparte, no lo toca esto).

## Timing
Hazlo ANTES de invitar a Julian y antes de mas pushes de Aegis (para que sea un desenredo unico). Julian se
invitara al repo NOVA-Aegis correcto, no al fork.

-- Operador
