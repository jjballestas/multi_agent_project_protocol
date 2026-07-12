---
message_id: MSG-20260711-Operador-to-Arquitecto-ACTION-reactivar-codex-promover-B-TASK9303
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Arquitecto-to-Operador-RESP-A1-ejecutada-B-encolada.md
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-DECISION-A1-ahora-encolar-B-regenesis.md
one_line_summary: "Reactivo Codex para B. Promueve TASK-9303 (proposed -> ready, owner Codex) + rutea el GO autocontenido a Codex (contrato SPEC-AEGIS-chain-reanchor-config-epoch) por el mailbox del hub (mecanismo s.6). Hazlo AHORA (pre-30-jul) para que B aterrice antes de que Sprint 1 tome prioridad dura sobre Codex; no compite con la reconciliacion 26-29 (esa es del Analista, read-only). Guardrail ya codificado."
requested_action: "Promueve TASK-9303 en el ledger de Aegis (proposed -> ready, owner Codex) y rutea el GO/ACTION autocontenido a Codex por Area_comun/mailbox/open/ del HUB (su cron escucha el hub, mecanismo runbook s.6), con la ruta del contrato SPEC-AEGIS-chain-reanchor-config-epoch y el bloque de operacion del ledger de Aegis. El Operador reactiva/asegura el cron de Codex. Reporta cuando B pase sus 7 acceptance (incl. la e2e nominal con jheredia:v1)."
question: "Confirmas TASK-9303 promovida + GO ruteado a Codex? Reporta el resultado de las 7 acceptance de B (en especial la e2e nominal jheredia:v1) para poder cerrar la A2 nominal limpia antes de la 1a unidad gobernada de Julian."
---

# ACTION - Reactivar Codex para B (re-anclaje de cadena, A2 nominal limpia)

El Operador AUTORIZA reactivar Codex para construir B. Ejecuta el mecanismo Codex->Aegis (runbook s.6):

## Directiva
1. **Promueve TASK-9303** en el ledger de Aegis: `proposed -> ready`, owner Codex (submit_intent, ventana segura,
   slim views, push inmediato).
2. **Rutea el GO/ACTION autocontenido a Codex** por el mailbox del HUB (su cron solo escucha el hub): ruta del
   contrato `Area_comun/specs/SPEC-AEGIS-chain-reanchor-config-epoch.md` (repo Aegis) + el bloque de operacion del
   ledger de Aegis (Codex corre submit_intent DESDE D:/Agentes/Zeus/NOVA/Aegis, firma ahi, claim + flips + release
   + push a la rama de Aegis).
3. El Operador reactiva/asegura el cron de Codex de su lado.

## Por que AHORA (timing)
- Es 11-jul: ANTES de que el Sprint 1 gobernado tome prioridad DURA sobre Codex (30-jul, runbook s.6.5). Hacer B
  ahora = aterriza antes de que Sprint 1 compita por Codex.
- NO compite con la reconciliacion baseline 26-29 (esa es del Analista, read-only) ni toca el estudio medido.

## Guardrail (ya codificado en TASK-9303; reafirmo)
- B debe COMPLETAR antes de la 1a unidad de build GOBERNADA de Julian. Su trabajo actual es onboarding no-study
  bajo Codex (A1); su 1a unidad medida nace bajo `jheredia:v1` TRAS B.
- B es SOLO Aegis: el hub (epoch 1.14.0, 2E35F26E) NO se toca; la historia se preserva (patron pre_t0, sello seq
  672..N + frontera de epoca-de-config + validador multi-epoca). Sin riesgo de estudio.

## Al aterrizar B
- Corrige el runbook s.8.4 (sobre-declara "pubkey + regenesis.py" como A2 valida) -- ya lo tienes registrado.
- Avisa para que el Operador ROTE la llave de Codex (estuvo en el server externo de Julian bajo A1 = exposicion
  transitoria que B cierra al pasar Julian a jheredia:v1).

-- Operador
