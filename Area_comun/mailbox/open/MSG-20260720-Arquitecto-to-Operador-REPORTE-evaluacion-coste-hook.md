---
message_id: MSG-20260720-Arquitecto-to-Operador-REPORTE-evaluacion-coste-hook
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-RESP-escalada-0257-O1-con-correcciones.md
  - Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md
one_line_summary: "REPORTE evaluacion de coste del hook (01:24 local, pediste numero y criterio sin decidir): serie completa 11.5-12.9 -> 29.5 -> 42.9s; medicion fresca validate solo ~12.0-12.5s (x3) + prune 0.31s + guia 0.07s -> el grueso del 42.9 es la maquinaria selector/equivalencia que 0267 ELIMINA. Criterio: acotado por defecto en local + completo en CI; re-evaluar con la cifra real de 0267 (si materializacion deja el completo en ~15s, la pregunta cambia)."
---

# REPORTE - evaluacion del coste del hook (pediste numero y criterio, no decision)

Hora local: 2026-07-20 01:24. Ejecutada tu O1 (commit 8714b5a) y GO de 0267 emitido.
Aqui la evaluacion del coste.

## Los numeros

- Serie del modo completo en ruta gobernada (mediciones del checker): 11.5-12.9s
  (iter0) -> 29.5s (iter1) -> 42.9s (iter2). Cada remediacion apilo capas de
  chequeo (equivalencia index/worktree + familia de borrados) sobre el validador.
- Medicion fresca de esta madrugada (01:21, este equipo, 3 corridas):
  validate_collaboration_state solo = 12.26 / 11.94 / 12.45s; prune_check 0.31s;
  drift de guia 0.07s. Es decir: el SUELO del modo completo es ~12.5s (el validador
  mismo) y los ~30s restantes del 42.9 son la maquinaria selector/equivalencia que
  TASK-0267 precisamente ELIMINA (la materializacion la reemplaza por una copia del
  indice + un validate sobre el temp).
- Modo acotado: 0.38-0.39s (medido por maker y checker, consistente).

## La evaluacion (criterio, decision tuya)

1. El CI ya corre validate COMPLETO desde clon limpio en cada push y PR (hub e
   instancia). Un modo completo local de 43s por commit gobernado DUPLICA esa capa
   pagandola en el peor sitio: la ruta gobernada es el flujo dominante del equipo
   (cada mensaje de mailbox, cada operacion de ledger es un commit gobernado).
2. Con tu propia lectura (hook = primera linea rapida, CI = enforcement duro), el
   acotado de 0.4s cumple exactamente el rol de primera linea; su hueco (no validar
   el estado global en cada commit) lo cubren el CI y el clean-clone del checker,
   que es donde ya se cazo TODO lo real de esta tanda.
3. PERO la cifra que importa es la de 0267: la materializacion cambia el perfil.
   Si el completo v2 queda en ~15s (validate ~12.5s + overhead de materializar),
   la friccion baja 3x y podria justificarse mantener completo-local; si queda
   cerca de 40s, no.

Mi criterio si tuviera que fijarlo hoy: acotado por defecto en local + completo bajo
demanda (flag explicito, p.ej. pre-push voluntario) + completo SIEMPRE en CI. Pero la
decision es redonda solo con la cifra del hook v2, que ya esta exigida en el handoff
de 0267 (frio/caliente). Te la traigo apenas aterrice y decides con ambas en mano.

Pendiente tuyo sin respuesta aun (re-oferta unica, luego lo parqueo): los 2 candidatos
de endurecimiento del ledger del reporte anterior (verificacion post-write del evento;
coherencia idempotencia-vs-estado).
