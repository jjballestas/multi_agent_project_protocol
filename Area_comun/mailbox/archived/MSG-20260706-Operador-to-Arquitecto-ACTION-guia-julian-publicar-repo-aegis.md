---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-guia-julian-publicar-repo-aegis
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md"
one_line_summary: "Prep del onboarding de Julian (id jheredia, maker de Contabilidad): (1) colocar gobernada en el repo Aegis la GUIA DE TRABAJO clara que redacto el Asesor; (2) confirmar que el main del GitHub de Aegis esta AL DIA/pusheado para que Julian descargue la metodologia YA ACTUALIZADA al clonar; (3) seguir el mandato de terminar el desarrollo pendiente. NO se re-genesis todavia (esperamos la pubkey de Julian)."
requested_action: "(1) Colocar una version gobernada de la GUIA DE TRABAJO de Julian (fuente: personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md) en el repo Aegis, junto al runbook (p.ej. Area_comun/protocol/ o Area_comun/onboarding/), para que Julian la obtenga al clonar. Ajusta/gobierna el texto a tu criterio; es el mapa, el runbook es el manual. (2) CONFIRMAR que el main del remoto GitHub PRIVADO de Aegis esta al dia y pusheado (reconciliar main vs aegis/main si sigue pendiente del item 4) -- Julian debe descargar la metodologia YA ACTUALIZADA, no un estado viejo. (3) Continuar terminando el desarrollo pendiente (1002 t3 TASK-1203 en Codex, chains 1001/1002, Contabilidad WS1). El re-genesis A2 de la identidad de Julian NO se hace aun: esperamos su pubkey."
question: "Confirmas (1) la colocacion gobernada de la guia en Aegis, (2) que el main del GitHub de Aegis queda al dia para el clon de Julian, y (3) el avance del desarrollo? Avisa si la reconciliacion de ramas del remoto sigue pendiente."
---

# ACTION - Guia de trabajo de Julian + publicar Aegis al dia + seguir el desarrollo

El operador quiere: (a) que Julian descargue la metodologia YA ACTUALIZADA, y (b) un documento CLARO de como
va a trabajar. Prep, sin re-genesis todavia (esperamos la pubkey de Julian; ese es el unico bloqueo de su
identidad A2).

## 1. Colocar la GUIA DE TRABAJO gobernada en Aegis
El Asesor redacto una guia clara y accesible para Julian (rol de maker de Contabilidad, modelo mental,
setup, el ciclo de una tarea de punta a punta, reglas duras, donde esta el detalle): fuente en
`personal/asesor/GUIA-TRABAJO-julian-maker-contabilidad-aegis.md`. Colocala gobernada en el repo Aegis junto
al runbook para que Julian la obtenga al clonar. Es el MAPA; el runbook es el MANUAL (comandos exactos).

## 2. Confirmar el repo Aegis AL DIA en GitHub
Para que "descargar la metodologia actualizada" funcione, el main del remoto GitHub privado de Aegis debe
estar al dia. Recordatorio del item 4 (LOTE1): el remoto ya apuntaba a git@github.com:jjballestas/Zeus-Aegis
.git pero quedaba reconciliar `main` (fb8cc210, init de GitHub) vs `aegis/main` (el trabajo). Confirma que el
main publicado = el estado actual con todo el trabajo (runbook, DECISIONes 1001/1002, guia, chains). Si sigue
pendiente, cierralo.

## 3. Seguir terminando el desarrollo pendiente (mandato vigente)
Continua: 1002 t3 (TASK-1203 indexador, en Codex) -> chains 1001/1002 -> Contabilidad WS1. Sin idle. El
re-genesis A2 de la identidad de Julian se hace cuando llegue su pubkey (no antes).

-- Operador
