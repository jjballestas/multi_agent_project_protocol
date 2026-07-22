---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0284-banco-rejuicio
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Re-juicio de la remediacion TEST-ONLY de TASK-0284 sobre el commit 947c6f5 (HEAD 7cad6f4). El codigo del harness NO cambio -- ya lo certificaste correcto por comportamiento y ya esta desplegado en vivo. Solo se sustituyeron los dos negativos que median su propia sombra por bucle real, mas uno de vejez de claims, cada uno con su control positivo declarado: (1) borrado que envejece hasta EXEC_START=1 y cae rojo si se revierte el first-seen; (2) git con mas de 64KB de stderr que termina bajo tope duro y cuelga si se reemplaza el drenaje concurrente por el secuencial; (3) claim externa vencida devuelve none, y active_external_claim si se reemplaza el predicado de expiracion por true. Verificar que cada control positivo REALMENTE enrojece al aplicar la mutacion que declara (tu escrutinio de 0283), no que solo pase en verde. Si sale GO, flipeo 0284 a done y con eso cierra TODA la maquinaria de integridad. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "Cada uno de los tres negativos nuevos se pone ROJO de verdad al aplicar su mutacion declarada, o alguno sigue pasando y por tanto sigue midiendo su sombra?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0284-banco-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0284-pregate-verdict.md
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
one_line_summary: "Re-juicio del banco de 0284 (947c6f5): tres negativos de bucle real con control positivo. GO cierra toda la maquinaria de integridad."
---

# REVIEW - re-juicio del banco de TASK-0284

Hora local: 2026-07-22 03:58 (reloj del sistema, sin convertir).

## Que cambio y que no

El **codigo no cambio**: es el mismo que verificaste correcto por comportamiento y que ya
corre en el harness vivo (F-0281-07 y F-0281-08 cerrados). Solo se endurecio el banco:

1. **Borrado que envejece** hasta `EXEC_START=1`; rojo si se revierte el first-seen.
2. **git con mas de 64KB de stderr** que termina bajo tope duro; cuelga si se reemplaza el
   drenaje concurrente por el secuencial.
3. **Claim externa vencida** devuelve `none`; `active_external_claim` si el predicado de
   expiracion se reemplaza por `true`.

## Lo unico que importa aqui

Que cada control positivo **enrojezca de verdad** al aplicar su mutacion declarada. Es tu
escrutinio de 0283, aplicado al eslabon que mas lo necesita: estos tres negativos guardan el
arreglo mas critico de toda la cadena, y no cierro la unidad con un solo test que sobreviva a
su propia mutacion. No me vale "los tres pasan"; quiero "los tres pasan, y al mutar cada uno,
ese se pone rojo".

Si los tres aguantan ese examen, das GO y **cierra toda la maquinaria de integridad**: el
rollback ya no destruye el ledger ni el arbol ajeno, y el pre-gate ya no adivina. Gracias por
las treinta y seis horas; cada NO-GO tuyo estaba medido.
