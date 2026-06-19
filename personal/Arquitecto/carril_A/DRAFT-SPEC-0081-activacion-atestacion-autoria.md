---
spec_id: SPEC-0081 (DRAFT - id final al promover)
task_id: TASK-XXXX (a asignar al promover)
type: security
status: draft (pendiente GO operador)
linked_decisions:
  - DECISION-0039
  - DECISION-0029
  - DECISION-0033
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0081 (DRAFT) - Activacion grado-tesis de la atestacion de autoria (#4)

## Context

DECISION-0029 dejo construido el mecanismo #4 (prev_hash + firma por agente + anclaje externo),
off-by-default (TASK-0101/0102/0103; fix chain+auth TASK-0113). DECISION-0039 autoriza su ACTIVACION
gateada (off -> piloto -> on) para instrumentar el modulo-app de Presupuesto, con la restriccion dura
de que #4 debe estar ON antes del primer handoff real (no retrofiteable). Esta SPEC fija los
criterios verificables de esa activacion. **No re-implementa** el mecanismo; cubre provisioning,
manipulation-check, piloto, prueba negativa y rollback.

## Scope

- Provisioning de identidad por agente: poblar `event_state.signature_config.public_keys`.
- Harness de manipulation-check (instrumento sano >=99%) sobre runs legitimos.
- Prueba negativa: una atestacion forjada/alterada (A1/A2) debe ser rechazada.
- Procedimiento de piloto supervisado (caps, checkpoint, rollback ensayado).
- Encendido en la instancia viva (no en el template) + SemVer MINOR + CHANGELOG.

## Out Of Scope

- Re-disenar prev_hash / firma / anclaje (ya existen).
- Encender SA.4, Capa C o subagents.
- Publicar/citar el dataset (GATE-DATASET + GATE-INST + PRE-REG).
- Tocar la DB de Budget o su migracion.

## execution_pipeline

1. **Provisioning (CONDICION DURA antes del piloto).** (a) Generar par de llaves por agente del
   `agent_registry` (privada FUERA del repo, en el wrapper de cada agente); registrar la publica en
   `signature_config.public_keys` por edicion PUNTUAL de `protocol.config.json`. (b) Proveer las claves
   HMAC en `event_auth.keys` ANTES de `event_auth.enabled=true` (si no, `append_event` falla por "signing
   key missing"). (c) Proveer `anchor_config.remote_url` (remoto git independiente) o un proof backend
   real ANTES de `anchor_enabled=true` (si no, el primer anclaje falla). Verificar ausencia de secretos
   en repo (`scan` de secretos).
2. **Harness manipulation-check.** Implementar `examples/attestation_health_cases/` (o equivalente):
   ejecuta N runs legitimos del protocolo, cuenta atestaciones bien formadas / esperadas, emite reporte
   JSON determinista (timestamps fijos), exit 0 si tasa >=99%.
3. **Prueba negativa.** Caso golden que forja/altera una atestacion (cambia payload, firma con llave
   no registrada, reordena/borra un evento) y verifica que el validador la RECHAZA con diagnostico.
4. **Piloto supervisado.** Encender chain+firmas+anclaje en ventana acotada (operador presente);
   correr 2 + 3; checkpoint humano; ensayar rollback (4 flags a false -> estado dormido
   byte-equivalente, replay==hot, drift 0).
5. **ON.** Tras GO del operador sobre el piloto, dejar #4 ON en la instancia viva; bump MINOR +
   CHANGELOG; actualizar memoria post-commit (DECISION-0026).

## acceptance_criteria

- **AC1 - Provisioning sin secretos (condicion de encendido).** (a) Cada agente del registry tiene clave
  publica en `signature_config.public_keys`; ninguna clave privada esta en el repo (scan de secretos
  limpio); una atestacion firmada por un agente verifica contra SU publica y falla contra otra. (b)
  `event_auth.keys` esta poblado antes de `event_auth.enabled=true` (sin eso `append_event` falla por
  "signing key missing"). (c) `anchor_config.remote_url`/proof backend real esta provisto antes de
  `anchor_enabled=true` (sin eso el primer anclaje falla). Un smoke de provisioning debe demostrar que
  `append_event` y el primer anclaje NO fallan tras (a)-(c).
- **AC2 - Salud del instrumento >=99% (NO es seguridad).** En >=N runs legitimos (N definido con el
  operador; sugerido N>=20), la tasa de atestaciones bien formadas y verificables es **>=99%**. Esta
  metrica mide la salud del instrumento EN AUSENCIA de adversario; **NO es una afirmacion de seguridad**
  (la seguridad la mide AC3). El reporte debe declarar explicitamente esta distincion.
  - **Definicion de "atestacion bien formada y verificable":** el evento autoria-relevante (turno o
    handoff) lleva (a) `prev_hash` que encadena correctamente contra el evento anterior; (b) firma del
    agente productor verificable contra su clave publica registrada; (c) sujeto = `canonical_hash` del
    artefacto, predicado completo (agente, modelo-version, tarea, decision, trust_boundary); (d) el
    digest de cabeza queda incluido en el siguiente anclaje (monotonia del ancla).
  - **Denominador (fuente INDEPENDIENTE del firmante):** el conteo de eventos autoria-relevantes
    derivado del **event log** (no de lo que el firmante decidio firmar); si el denominador lo fijara el
    mismo codigo que produce el numerador, el 99% seria auto-cumplido. **Numerador:** las que cumplen
    (a)-(d).
- **AC3 - Seguridad: deteccion del adversario (prueba negativa) - BINARIA y BLOQUEANTE como AC2.** El
  validador RECHAZA toda atestacion forjada/alterada. No es un umbral: es pasa/falla, y bloquea el
  encendido igual que AC2. **Vectores fijos minimos, golden reproducible (exit-code) por vector:**
  (1) alteracion puntual de payload; (2) borrado de evento; (3) insercion de evento; (4) reordenamiento;
  (5) firma con llave NO registrada; (6) atribucion cruzada (atestacion atribuida a otro agente). Cada
  vector con su golden determinista que demuestra el RECHAZO con diagnostico de clase (A1/A2).
- **AC4 - Plano de la atestacion estructurado (sin texto libre en el evento de atestacion).** El evento
  de atestacion lleva el sujeto por hash (`canonical_hash`) y predicado estructurado; no incluye texto
  libre. **Verificado por inspeccion del esquema del evento**, NO por el scan de encoding (el
  `scan_encoding` solo valida ASCII/canal, NO detecta PII; ver DECISION-0040 para la garantia de PII del
  log completo, que es disciplinaria + tarea diferida de detector).
- **AC5 - Rollback ensayado.** Apagar los 4 flags restaura el estado dormido byte-equivalente; replay
  == hot; drift 0.
- **AC6 - Gates verdes.** `scripts/validate_collaboration_state.py --root .` (incluye drift B.3),
  `scan_encoding.py`, `scan_domain_neutrality.py`, y los goldens existentes (`chain_cases`,
  `agent_signature_cases`, `anchor_cases`, `chain_auth_combined_cases`) + el nuevo
  `attestation_health_cases` en CI.

## linked_decisions

- `DECISION-0039`: autoriza la activacion gateada; esta SPEC fija sus criterios.
- `DECISION-0029`: politica + mecanismo + modelo de amenaza A1-A4 que esta SPEC instrumenta.
- `DECISION-0033`: dos planos / sin PII; la firma respeta el plano de protocolo.

## test_plan

- **Smoke de provisioning (AC1):** con `event_auth.keys` y `anchor_config.remote_url` provistos,
  `append_event` y el primer anclaje NO fallan; sin ellos, fallan con el error esperado (caso negativo).
- **Salud (AC2):** `examples/attestation_health_cases/run_*.py`: tasa >=99% sobre runs legitimos; el
  **denominador se deriva del event log** (eventos autoria-relevantes), no del firmante; reporte JSON
  determinista que DECLARA "esto es salud, no seguridad"; exit code 0/1.
- **Seguridad (AC3): goldens negativos, UNO por vector (6)** -- alteracion puntual, borrado, insercion,
  reordenamiento, firma con llave no registrada, atribucion cruzada -> cada uno RECHAZADO con clase
  (A1/A2), determinista, exit-code.
- `chain_auth_combined_cases` (ya en CI) verde con chain+auth on.
- Scan de secretos: sin claves privadas en repo.
- Ensayo de rollback: hash de estado sin cambio tras off; `protocol_replay` == hot.

## closure_criteria

- AC1-AC6 cumplidos; piloto pasado con GO del operador; #4 ON en instancia viva ANTES del primer
  handoff real del modulo-app; SemVer MINOR + CHANGELOG; memoria actualizada.

## Risks

- **Llave privada filtrada al repo.** Mitigacion: privadas fuera del repo + scan de secretos en CI.
- **Tasa <99% en piloto.** Mitigacion: no encender; diagnosticar (canonicalizacion, orden de firma,
  ventana de anclaje) y reintentar; el instrumento roto no se usa.
- **Ventana de anclaje deja eventos sin anclar (A3 residual).** Mitigacion: cadencia corta +
  atestaciones huerfanas del revisor; riesgo residual declarado, no afirmado como cubierto.
- **Combinar ventanas de riesgo.** Mitigacion: un solo multiplicador por ventana (DECISION-0039 sec.5).

## Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Provisioning (public_keys + event_auth.keys + anchor remote) sin secretos | TASK-XXXX | smoke provisioning + scan secretos + verify firma | AC1 |
| Salud del instrumento >=99% (NO seguridad; denominador del log) | TASK-XXXX | attestation_health_cases | AC2 |
| Seguridad: prueba negativa binaria, 6 vectores, golden/vector | TASK-XXXX | 6 goldens negativos A1/A2 (exit-code) | AC3 |
| Evento de atestacion estructurado (esquema, no scan_encoding) | TASK-XXXX | inspeccion de esquema | AC4 |
| Rollback reversible | TASK-XXXX | ensayo off + replay==hot | AC5 |
