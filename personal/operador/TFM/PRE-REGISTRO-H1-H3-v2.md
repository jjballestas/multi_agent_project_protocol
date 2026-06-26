# Pre-registro H1–H3 — v2.0 (operativo) — Atestación de autoría multi-agente (TFM)

> Estado: **FROZEN v2.0 — 2026-06-27.** Esta v2.0 es el pre-registro **OPERATIVO** para la medición. **Hereda
> íntegra la v1.0** (`PRE-REGISTRO-H1-H3.md`, FROZEN v1.0, sha256 `1ae10e057500dfe1209e77a07f73194c021befdfa1c679432a3f5b3e965a2b47`,
> atestada en #4 seq 2124) y solo añade **una aclaración pre-medición** (legítima: se hace ANTES de generar/mirar
> cualquier dato). Tras el freeze de v2.0 no se cambian hipótesis/métricas/umbrales antes de medir.

## Único cambio respecto a v1.0: la atestación-de-registro que se mide

El operador eligió el **Camino B** (DECISION-0065, accepted): la firma de autoría por agente se produce en el
**camino de escritura real** (`submit_intent`) como el campo **`actor_auth` Ed25519** del evento de intent
(implementado off-by-default en TASK-0190, commit `d8bb869`; OFF byte-idéntico verificado en vivo; golden 5/5;
secret-independiente).

Por tanto, para toda la v1.0:
- **La "atestación de autoría" medida (A2 / H1) = `actor_auth` Ed25519 del evento de intent** (firma con la privada
  del agente, verificable con su pública de `signature_config.public_keys`), **no** el evento `agent.attestation`
  del Camino A (orquestador), que queda fuera de alcance.
- La capa **`event_auth` HMAC** sigue siendo la integridad simétrica viva (A1 + integridad); **`actor_auth`
  Ed25519** es el no-repudio asimétrico (la contribución, A2).
- Todo lo demás de v1.0 se mantiene **sin cambio**: hipótesis H1/H2/H3, modelo A1–A4, métricas (§4), **umbrales
  pre-comprometidos (§5)** [H1 detección=100%/AC2≥99%/FPR=0; H2 Δlat med≤50ms/p95≤200ms, Δstore≤4KB/ev, Δtokens≤5%;
  H3 acuerdo externo=100% + match clon-limpio], procedimiento (§6), independencia declarada (§8).

## Implicación operacional para el procedimiento (§6 de v1.0)

- El **cutover A2** (paso §6.2) = encender el flag `event_state.actor_auth_enforce` (ventana de riesgo del operador
  presente, DECISION-0039 §5; rollback = flag→false). Tras el flip, los turnos vivos llevan `actor_auth` Ed25519.
- El **experimento negativo A2** (§6.3) = inyectar atribución cruzada (firmar como otro agente / keyid ajeno / sig
  inválida) y verificar rechazo — exactamente el golden `actor_auth_ed25519_cases` (AC3), escalado por el harness.
- El **verificador externo** (§6.6) = verificar `actor_auth` con solo las públicas desde un clon limpio (AC4 /
  DECISION-0046).

## Freeze v2.0

FROZEN v2.0 el 2026-06-27 = el commit de git que introduce este archivo (fecha+hash inmutables). Su `sha256` se
registra en el mensaje del commit y se atesta en el ledger #4 (project_narrative) ANTES de generar el dataset.
v2.0 **supersede a v1.0 como pre-registro operativo**; v1.0 permanece como historia inmutable (ya atestada).
Cualquier cambio futuro = v3.0 nueva, y solo legítimo antes de mirar resultados.
