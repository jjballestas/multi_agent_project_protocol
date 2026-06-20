---
decision_id: DECISION-0045
title: Boundary de una sola vez en T0 - sello criptografico de la historia pre-T0 y arranque del ledger operativo #4 fresco
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0039, DECISION-0029, DECISION-0022, DECISION-0028, DECISION-0040]
phase: P2
---

# DECISION-0045 - Boundary de una sola vez en T0; sello criptografico pre-T0

> ACCEPTED por el operador (GO ventana de piloto de #4, 2026-06-19, refinamiento Ruta B). Formaliza un
> boundary de UNA SOLA VEZ en T0 para arrancar el ledger operativo del dataset de tesis con #4 ON, sellando
> la historia pre-T0 con continuidad criptografica de provenance. Verificado VERDE en clon limpio antes de
> cualquier escritura canonica.

## Contexto (el hallazgo del piloto)

Al abrir la ventana de piloto de #4 (DECISION-0039: chain + agent_signatures + anchor + event_auth) se
descubrio que el **log de eventos vivo no puede alojar una cadena #4 valida**, porque contiene artefactos
**inmutables** de un **ensayo #4 previo SANCIONADO** (hoy 2026-06-19 ~08:26-08:39, seq 590-629):
`chain.genesis@590` con el hash de un config viejo, 20 `agent.attestation` firmadas con una clave efimera
que ya no existe, y 20 `chain.anchor`. Causa estructural (verificada en codigo):

- `validate_chain` ancla al **primer** `chain.genesis` del stream y exige `prev_hash == canonical_hash(config
  actual)`. El log vivo tiene DOS genesis (viejo@590 / nuevo) y eventos **mezclados** encadenados (590-629)
  y no-encadenados (resto), que ninguna config hace validos a la vez.
- `validate_agent_signatures` lee la historia completa (archivo + hot, AGENTS.md s.0) y las 20 attestations
  viejas dan `public_key_missing` (firmadas con clave inexistente, no re-verificables con ninguna clave
  actual).
- Archivar/compactar NO ayuda: el validador lee tambien los archivos (`events_in_log_order`).

No hay forma de re-habilitar #4 sobre ese log sin un boundary explicito. (`prune_state.py` solo archiva
STATE, no el event log.)

## Decision

1. **Boundary de UNA SOLA VEZ en T0.** El **ledger operativo** del dataset de tesis (handoffs gobernados de
   la app) **arranca en T0** desde un genesis fresco bajo el config #4 ON. La historia pre-T0 (seq 1-671)
   queda **sellada** fuera del **path de validacion operativo** del runtime (`runtime/state/events.jsonl` +
   `runtime/state/archives/`). Esto es excepcional y se ejecuta una sola vez; no es un patron de edicion
   rutinaria del ledger.

2. **Preservacion integra de la historia pre-T0.** La historia pre-T0 se preserva (a) en **git** (commit
   `94d2e58`, que contiene el log completo 1-671) y (b) en un **export frio** versionado
   `pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl` con su **sha256 registrado**. Nada se borra; se
   saca del path operativo.

3. **Continuidad criptografica de provenance.** El **sha256 del export sellado** y el **commit pre-T0**
   (`94d2e58`) se embeben en `protocol.config.json.pre_t0_provenance`. Como el genesis T0 =
   `canonical_hash(protocol.config.json)`, el **genesis T0 commitea criptograficamente** a la historia
   sellada. Se publica ademas un `chain_manifest.json` legible (espejo de la provenance). Asi hay cadena de
   provenance verificable desde el ledger T0 hacia la historia sellada, aunque esta no este en el path de
   validacion operativo.

4. **Reconciliacion con "el validador lee toda la historia" (AGENTS.md s.0).** Esa invariante se mantiene
   **dentro de la epoca operativa** (T0 en adelante: archivo + hot). La trazabilidad **pre-T0** se garantiza
   por git + el export frio + el enlace de provenance del genesis (no por el path operativo). Este boundary
   es el unico punto donde la continuidad del log operativo se reinicia, y queda explicito y registrado
   aqui.

5. **Compatibilidad con escritor-unico / runtime-authoritative (DECISION-0022/0028).** El sello + re-genesis
   es una operacion de boundary **sancionada por el operador**, ejecutada en copia limpia, verificada VERDE
   (drift 0, replay==hot, chain/firmas/anclaje/event_auth validos) ANTES del push canonico. No es una
   edicion manual rutinaria del ledger (que el hard-gate B.3 sigue rechazando). Tras T0, toda transicion
   vuelve a ir por `submit_intent`.

6. **LECCION ENFORCED (causa raiz):** **ningun piloto/ceremonia de #4 vuelve a correr contra el log vivo.**
   Siempre en copia desechable (clon fuera del mount). Correr el ensayo previo contra el log vivo fue lo que
   contamino la historia y forzo este boundary. Esta regla pasa al runbook y se propone para AGENTS.md.

## Alcance / No-alcance

- **En alcance:** el boundary de una sola vez en T0; el sello pre-T0 con preservacion (git + export frio) y
  provenance criptografica (config + manifest); arrancar el ledger operativo #4 ON desde el genesis fresco;
  la regla enforced de no-piloto-contra-vivo.
- **Fuera de alcance:** rediseñar la cadena en epocas (alternativa A, descartada por el deadline; quedaria
  como mejora futura si se quisiera validar pre-T0 en el path operativo); cambiar la politica de #4
  (DECISION-0039) o sus 4 flags; tocar la DB de Budget; DEF-PII (TASK-0118, diferida; PII de terceros nunca
  al event log, DECISION-0040).

## Consecuencias

- #4 puede encenderse sobre un ledger operativo limpio en T0, cumpliendo el deadline (#4 ON antes del primer
  handoff gobernado de la app, no retrofiteable).
- La auditoria pre-T0 no se pierde: queda en git + export frio + enlazada por provenance al genesis T0.
- Reversible hasta el push: todo el ensayo vive en clon; el vivo no se toca hasta el GO final del operador.

## Alternativas consideradas

- **A - validacion por epocas en `validate_chain`** (anclar al ultimo `chain.genesis` que case con el
  config; manifest de epocas). Mas correcta y preserva la traza completa en el path operativo, pero es
  cambio de CORE (DECISION + Codex + goldens) y **no llega al deadline**. Queda como mejora futura.
- **Registrar la clave vieja / aceptar el genesis viejo.** Inviable: las attestations viejas se firmaron con
  una privada efimera inexistente (no re-verificables) y el genesis viejo lleva un hash de config que ya no
  existe; ademas el log mezcla eventos encadenados y no-encadenados.
- **Compactar/archivar dentro de `runtime/state/archives/`.** No sirve: el validador lee los archivos.
