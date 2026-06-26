# Mini-plan — Cutover A2 (atestación de autoría Ed25519 sobre turnos vivos)

> Autor: Arquitecto · 2026-06-27 · Para: operador. Camino crítico del TFM (mov. **a**), DESPUÉS del freeze del
> pre-registro (`c64f2b8`, ya atestado en #4 seq 2124) y ANTES de generar el dataset. Gobernado por DECISION-0039.

## 0. Corrección de premisa (importante): NO es un flag-flip

Verificado en código y en el ledger vivo:
- `event_state`: `chain_enabled / agent_signatures_enabled / anchor_enabled / event_auth` = **true** (#4 ON).
- `real_invoker.enabled` = **false**, `supervised_autonomy.enabled` = **false**.
- 1448+ eventos vivos: `actor_auth: "not_enforced_phase2"`, `event_auth: hmac-sha256`. **Cero Ed25519 por agente.**

El Ed25519 de autoría lo produce **`runtime/llm_turn_wrapper.py`** (algoritmo `ed25519`) y se materializa como un
evento **`agent.attestation`** vía `EventWriter.append_agent_attestation` (gateado por `agent_signatures_enabled`),
invocado por el **`orchestrator`** cuando `real_invoker`/`supervised_autonomy` están ON. **PERO** los agentes hoy
escriben el ledger por **`cron → CLI → submit_intent.py`**, y `submit_intent.append_event(...)` **no pasa
`actor_auth`** → default `not_enforced_phase2`. Es decir: el mecanismo Ed25519 existe y está probado en golden,
pero **no está cableado al camino de escritura real de los agentes**. Encenderlo exige una **pieza**, no un flag.

## 1. Dos caminos (decisión de diseño)

- **Camino A — orquestador/real_invoker (el "diseñado", rico):** enrutar los turnos de los agentes por el
  `orchestrator` (no por el cron directo) con `real_invoker` + `supervised_autonomy` ON, para que cada turno pase
  por `llm_turn_wrapper` y emita un `agent.attestation` Ed25519. *Coste:* cambia el modelo de operación
  (cron→orquestador) **y** abre la ventana de mayor riesgo (real_invoker/SA), que **DECISION-0039 §5 mantiene
  SEPARADA de #4** (un multiplicador por ventana).
- **Camino B — `submit_intent` firma `actor_auth` Ed25519 (mínimo, alineado con el modelo actual):** cada agente
  firma su intent con su privada Ed25519 (cargada de `D:/Agentes/protocol-secrets`, fuera del repo); el evento
  lleva `actor_auth: {method: ed25519, keyid, sig}` en vez de `not_enforced_phase2`. *Coste:* una pieza SDD
  pequeña en `submit_intent`; **no** requiere real_invoker/SA ni cambiar el modelo cron.

**Recomendación: Camino B** para el dataset de tesis — menor riesgo, menor cambio de modelo, y produce
exactamente lo que H1/A2 necesita (no-repudio por agente en los turnos reales). El Camino A queda como modo
"rico" futuro. *(Salvedad: hoy la "atestación de autoría" del diseño es el evento `agent.attestation`; en B
vivirá en `actor_auth`. Hay que declarar en el pre-registro cuál es la atestación-de-registro que se mide y ser
consistente — ver §5.)*

## 2. Precondición (ya cumplida)

- `signature_config.public_keys` provisionado (Ed25519 de Arquitecto/Codex/Analista). Privadas en
  `D:/Agentes/protocol-secrets/` (fuera del repo). HMAC `event_auth.keys` provisionado. Ancla configurada.

## 3. Pasos del cutover (Camino B)

1. **Pieza SDD (maker=Codex / checker=Arquitecto), off-by-default:** `submit_intent` carga la privada Ed25519 del
   `--actor-id` (de `protocol-secrets`, path-safe, fail-closed) y firma `actor_auth = {method:"ed25519", keyid,
   sig}` sobre el digest canónico del evento. Golden: (a) evento vivo lleva `actor_auth.ed25519` verificable con la
   pública; (b) **prueba negativa A2** — un evento atribuido a otro agente sin su privada es **rechazado** por el
   validador (atribución cruzada); (c) **secret-independiente** (DECISION-0046): clon limpio con solo públicas
   verifica; sin privadas no se puede firmar (fail-closed). NO toca `protocol.config.json`/genesis. Flag propio
   (p.ej. `actor_auth_enforce`) **off** por defecto.
2. **Provisioning de runtime:** cada cron/wrapper de agente puede leer SU privada (ya están en protocol-secrets);
   verificar permisos (solo el agente lee la suya).
3. **VENTANA DE RIESGO ÚNICA (operador presente):** encender el flag `actor_auth_enforce`. Es **su propia ventana**
   (DECISION-0039 §5): NO combinar con real_invoker/SA ni con cambios de `authoritative`. Rollback armado.
4. **Verificación post-cutover (en clon limpio + vivo):** nuevos eventos llevan `actor_auth.method=ed25519`
   verificable con la pública; `validate_collaboration_state` exit 0 (con/sin secretos); drift 0; prueba negativa
   de atribución cruzada pasa; #4 (chain+anchor+HMAC) intacto.

## 4. Rollback armado

- **Reverso:** `actor_auth_enforce` → **false**. Los eventos vuelven a `not_enforced_phase2` (la integridad HMAC +
  cadena + ancla **siguen vivas**; solo se apaga la firma asimétrica por turno). Reversible, **sin perder historia**
  (los eventos ya firmados con Ed25519 quedan; los nuevos vuelven a HMAC-only). Ensayar el reverso antes de confiar.
- **Criterio de aborto:** si tras encender, `append_event` falla (privada ausente/mal provisionada) o el validador
  se pone rojo → flag a false, diagnosticar en frío, reintentar.

## 5. Orden respecto al pre-registro y al dataset

1. Freeze pre-registro ✅ (hecho, atestado #4 seq 2124).
2. **(este cutover)** A2 vivo.
3. Generar dataset (N≥500 turnos, ≥2 agentes).
4. Inyectar A1/A2/A3 + medir coste + verificador externo → comparar con umbrales → redactar.

**Nota de consistencia (pre-registro):** si se elige Camino B, conviene una nota v2.0 del pre-registro que fije
"la atestación de autoría medida = `actor_auth` Ed25519 del evento de intent" (en vez del evento `agent.attestation`
del Camino A) — **antes de generar el dataset** (sigue siendo pre-medición, legítimo).

## 6. Qué decide el operador

- (i) **Camino A vs B** (recomiendo B).
- (ii) GO a la **pieza SDD** (paso 3.1) — es código, entra por SDD con maker=Codex/checker=Arquitecto.
- (iii) Agendar la **ventana de riesgo** (operador presente) para el flip + ensayo de rollback.
