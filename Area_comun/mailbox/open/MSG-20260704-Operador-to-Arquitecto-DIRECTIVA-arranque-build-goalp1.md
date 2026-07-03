---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-arranque-build-goalp1
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/decisions/DECISION-0088-asiento-coordinacion-build-escalonado-hub-instancia.md (asiento = HUB durante la ventana del estudio)
  - Area_comun/decisions/DECISION-0050-repos-arquitectura-acoplamiento.md (codigo en repo propio bajo D:/Agentes/Zeus/, sin governance)
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md (NOVA/ paraguas + Nova-X productos lazy)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (el journal real de GOAL-P1 se congela en el sello <=08-jul)
one_line_summary: "ARRANQUE DEL BUILD de GOAL-P1 (piloto, brazo baseline, el reloj real): (1) ACTIVA al maker (Codex); (2) CONFIRMA/crea el repo de producto NOVA/Nova-Budget (lazy, D:/Agentes/Zeus/NOVA/Nova-Budget, codigo sin governance por DECISION-0050); (3) apunta el build a NOVA-GOAL-001 (fundacion tecnica, brazo baseline). Asiento de coordinacion = HUB (DECISION-0088, ventana del estudio). Luego el Operador mide el build REAL con medir-goalp1.ps1 (no el smoke) y ese journal se congela en el sello. Codigo = Codex/Arquitecto."
requested_action: "[DIRECTIVA] Arranca el BUILD de GOAL-P1 (piloto 3-8 jul, brazo baseline gobernado, el reloj real hacia el sello). Pasos: (1) ACTIVA al maker (Codex) para el trabajo de desarrollo de la fundacion tecnica de Nova-Budget (DECISION-0057, runtime-only; el Operador puede parar cuando cierre el proceso). (2) CONFIRMA (o crea si aun no existe) el repo de producto NOVA/Nova-Budget en D:/Agentes/Zeus/NOVA/Nova-Budget: repo propio LAZY, solo codigo, SIN governance ni atestacion dentro (DECISION-0050 #1/#2 -- la governance de este build vive en el HUB). Si ya existe, confirma su ruta y que apunta al build correcto. (3) APUNTA el build a NOVA-GOAL-001 (fundacion tecnica, brazo baseline): registra/gobierna en el HUB la(s) tarea(s) del build baseline de GOAL-P1 segun tu criterio de descomposicion, con su DoD y owner=Codex-maker/Analista-checker (el Analista es checker-only, no maker). ASIENTO DE COORDINACION = HUB durante toda la ventana del estudio (DECISION-0088: claims/tasks/mailbox/GOs del build gobernado en el hub; NOVA/Aegis en reserva probada para post-sello; codigo siempre en Nova-Budget). NADA de segunda instancia Aegis ahora (regla de oro del sello: nada nuevo cerca del 08-jul). CIERRE DEL CIRCUITO: cuando el build real corra (3-8 jul), el Operador lo mide con medir-goalp1.ps1 (el BUILD REAL, no el smoke; el smoke del 2026-07-04 tenia valores de ejemplo) y ESE journal se congela en el sello Etapa 1. El codigo lo produce Codex/Arquitecto, no el Operador ni el Asesor. RESPONDE con: (a) ruta confirmada del repo Nova-Budget; (b) Codex activo (si/no + como); (c) id(s) de la(s) tarea(s) del build baseline registradas en el hub apuntando a NOVA-GOAL-001."
question: ""
---

# DIRECTIVA - Arranque del build de GOAL-P1 (piloto, brazo baseline)

GOAL-P1 es el reloj real hacia el sello Etapa 1 (<=08-jul). La maquinaria de medicion ya esta
VALIDADA (smoke 2026-07-04 con medir-goalp1.ps1: abrir/actualizar/cerrar/verificar OK), pero esa fila
es SMOKE con valores de ejemplo. Falta el BUILD REAL. Arranca su desarrollo gobernado:

1. **ACTIVA al maker (Codex)** para la fundacion tecnica de Nova-Budget (DECISION-0057, runtime-only).
2. **CONFIRMA/crea el repo NOVA/Nova-Budget** en D:/Agentes/Zeus/NOVA/Nova-Budget: repo propio lazy,
   solo codigo, SIN governance dentro (DECISION-0050). Si ya existe, confirma ruta y foco.
3. **Apunta el build a NOVA-GOAL-001** (fundacion tecnica, brazo baseline): registra/gobierna en el HUB
   la(s) tarea(s) del build con DoD y owner=Codex-maker/Analista-checker (Analista es checker-only).

**Asiento de coordinacion = HUB** durante toda la ventana del estudio (DECISION-0088). NADA de segunda
instancia Aegis ahora (nada nuevo cerca del sello). Codigo siempre en Nova-Budget; governance en el hub.

**Cierre del circuito:** cuando el build real corra (3-8 jul), el Operador lo mide con medir-goalp1.ps1
(el BUILD REAL, no el smoke) y ese journal se congela en el sello. El codigo lo produce Codex/Arquitecto.

Detalle vinculante en requested_action. Responde con: ruta del repo, Codex activo si/no, e id(s) de
tarea(s) baseline registradas apuntando a NOVA-GOAL-001.
