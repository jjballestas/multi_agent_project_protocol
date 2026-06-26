---
decision_id: DECISION-0066
title: Harness de experimento H1-H3 (aparato de medicion adversarial) - inyeccion de ataques SOLO sobre copia desechable, reproducible, salidas=datos (no ledger)
status: accepted
ratified_at: 2026-06-27
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0039, DECISION-0045, DECISION-0046, DECISION-0065, DECISION-0040]
phase: P2
---

# DECISION-0066 - Harness de experimento H1-H3

> ACCEPTED (operador GO 2026-06-27). Para MEDIR H1-H3 (pre-registro v2.0 FROZEN, sha256 e8277cc7..., atestado #4)
> hace falta un aparato **reproducible** que inyecte ataques, mida deteccion/FPR/sobrecoste y corra verificacion
> externa. El harness **forja eventos** (para probar deteccion) -> capacidad sensible -> frontera DURA. Es
> herramienta de investigacion (neutral); no cambia el core ni la gobernanza. Construirlo es seguro (opera sobre
> copias); EJECUTARLO sobre el dataset real es el paso de medicion posterior (tras el flip A2).

## Contexto

Pre-registro v2.0 fija H1 (deteccion: TPR=100% por vector A1/A2/A3 + AC2>=99% + FPR=0), H2 (sobrecoste acotado),
H3 (verificacion externa secret-indep). El mecanismo A2 (`actor_auth` Ed25519) esta construido off-by-default
(TASK-0190). Falta el aparato que convierte "instrumento" en "numeros".

## Decision

1. **Copia desechable SIEMPRE; NUNCA el #4 vivo (DECISION-0045, leccion enforced).** El harness opera sobre una
   **copia** del repo/ledger (o fixtures propios); JAMAS lee/escribe el `runtime/state/events.jsonl` vivo. Un
   **guard/test** lo prueba (no toca el root vivo). Esto evita repetir el incidente del piloto #4 contra el log vivo.
2. **Inyeccion de ataques programatica, determinista (seeded), reproducible.** Vectores:
   - **A1** (post-hoc): alterar / borrar / insertar / reordenar eventos ya escritos.
   - **A2** (atribucion cruzada): firmar como otro agente / keyid ajeno / sig invalida (reusa `actor_auth_ed25519_cases`).
   - **A3** (ancla): rollback / equivocacion del digest anclado.
   Reusa las definiciones de `examples/attestation_negative_cases` + `examples/actor_auth_ed25519_cases`; el harness
   las **escala** a una corrida con conteos (no re-implementa la cripto).
3. **Mide lo del pre-registro (§4 v1.0):** deteccion (TPR) por vector, FPR sobre dataset legitimo, salud AC2,
   Dlatencia/Dalmacenamiento(/Dtokens) **con-#4 vs sin-#4** (toggle de flags sobre la copia), acuerdo del
   verificador externo + match de hash clon-limpio (H3, DECISION-0046, solo publicas).
4. **Salidas = DATOS, no ledger.** Emite un **artefacto de resultados estructurado** (JSON/MD) que mapea a los
   umbrales pre-comprometidos; NO escribe el #4. Re-corrida determinista = mismos resultados (reproducibilidad).
5. **Neutralidad (DECISION-0040):** herramienta neutral, sin terminos de dominio ni PII; vive como tooling de
   investigacion en el repo (no en el core neutral de protocolo ni en templates).
6. **No es la corrida de medicion.** Construir+probar el harness (sobre fixtures/copias) NO requiere el flip A2 ni
   genera el dataset de tesis; eso es posterior (flip + dataset real, paso del operador).
7. **SDD:** SPEC-0104 + TASK-0191, maker=Codex / checker=Arquitecto.

## Alcance / No-alcance

- **En alcance:** el aparato (inyeccion A1/A2/A3 + medicion deteccion/FPR/sobrecoste + verificador externo +
  artefacto de resultados), su guard de copia-desechable, sus tests/golden, reproducibilidad.
- **Fuera de alcance:** EJECUTAR el harness sobre el dataset real (paso de medicion posterior); el flip A2; generar
  el dataset; tocar el core/genesis/#4; publicar el dataset (GATE-DATASET).

## Consecuencias

- Medir H1-H3 pasa a ser **ejecutar un aparato reproducible**, no improvisar. El experimento adversarial queda
  documentado y nunca toca el dataset real (credibilidad audit-first).
- Riesgo: una herramienta que forja eventos -> mitigado por la frontera dura (solo copias) + guard + tests.

## Alternativas consideradas

- **Medir a mano / scripts ad-hoc:** no reproducible, no auditable; debilita la tesis. Descartado.
- **Inyectar sobre el log vivo:** prohibido (DECISION-0045). Descartado.
