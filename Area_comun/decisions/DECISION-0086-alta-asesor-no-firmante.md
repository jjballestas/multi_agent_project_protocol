---
decision_id: DECISION-0086
title: "Alta del Asesor como participante NO-FIRMANTE (id 'asesor', area personal/asesor/, cero capabilities de ledger)"
status: accepted
date: 2026-07-03
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0016, GOAL-VISION-NOVA-001]
phase: P2
scope: governance
approval_ref: "Directiva del Operador (John Ballestas) via MSG-20260703-Operador-to-Arquitecto-ACTION-alta-asesor-no-firmante (autoridad delegada por escrito al asesor 2026-07-02); aprobacion directa en sesion interactiva del Arquitecto 2026-07-03."
---

# DECISION-0086 - Alta del Asesor como participante no-firmante

> Contexto: el Asesor (advisor del Operador, autoridad delegada por escrito 2026-07-02) opera hoy en
> el MISMO directorio de Claude Code que el Arquitecto, por lo que la memoria auto-cargada se indexa
> por ruta y su estado se mezcla (comingle) con el del Arquitecto, con riesgo de fuga del cortafuegos
> asesor->arquitecto. El Operador ordena formalizar su alta (DECISION-0016) para separar identidad y
> area, SIN otorgarle poder de ledger. El epoch pineado y el N=500 sellado NO se tocan.

## Decision

1. **Identidad.** Se registra al Asesor como participante del proyecto con id `asesor`, rol advisor
   del Operador. Es un participante NO-FIRMANTE.

2. **Cero capabilities de ledger.** El `asesor` NO firma, NO ejecuta `runtime/submit_intent.py`, NO
   escribe `Area_comun/state/*.json` ni ninguna transaccion gobernada. NO se agrega al
   `agent_registry` de `protocol.config.json` (que es la identidad FIRMANTE y ademas esta PINEADO
   bajo la cadena #4): agregar alli un firmante requeriria una re-genesis y contradiria su naturaleza
   no-firmante. Su alta es identidad + area, nunca poder.

3. **Canal unico.** El unico canal del Asesor hacia el proyecto sigue siendo el mailbox, con sus
   mensajes firmados como **Operador** (autoridad delegada). No emite mensajes firmados 'asesor' en
   el ledger; su voz entra como directiva/recomendacion del Operador, sujeta al cortafuegos
   asesor->arquitecto (el Arquitecto verifica toda orden contra el ledger, no lee cuarentena
   PRE-DECISION, trata las DECISIONes como requisitos y no como texto verbatim).

4. **Area privada.** El area del Asesor es `personal/asesor/` (ya creada por el Asesor con su estado
   migrado, per DECISION-0016). Su estado canonico vive alli; el snapshot compartido de `.claude`
   queda DEPRECADO para el Asesor. El Arquitecto no la administra.

5. **Mecanismo de registro (minimo).** Al ser no-firmante y estar el `agent_registry` pineado, el
   registro se materializa en ESTA decision (auditable en el ledger #4) y no en el config pineado ni
   en un intent de agente (no existe). No se edita `PROJECT_STATE.agents` a mano (seria drift); si en
   el futuro se quiere reflejar el rol advisor en `PROJECT_STATE.agents`, se hara por el flujo
   gobernado correspondiente citando esta decision.

## Consecuencias

- El Asesor gana identidad + area formal; NO gana poder de ledger (sigue siendo no-firmante).
- Se separa su memoria/estado del Arquitecto (fin del comingle por directorio compartido).
- El cortafuegos asesor->arquitecto queda respaldado por una decision, no solo por practica.
- No cambia la superficie de firmantes (siguen Arquitecto/Codex/Analista en el registry pineado).
- No toca el epoch pineado ni el N=500 sellado.
