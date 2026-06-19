---
decision_id: DECISION-0043
title: Resolucion fuera-del-repo del secreto HMAC de event_auth (precondicion faltante de #4) - referencias, no literales
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0029, DECISION-0039, DECISION-0010]
phase: P2
---

# DECISION-0043 - Resolucion del secreto HMAC de event_auth fuera del repo

> ACCEPTED por el operador (GO de promocion 2026-06-19) tras la pasada de factibilidad de Codex (veredicto
> FACTIBLE con 2 ajustes incorporados). Promovida al ledger por el Arquitecto (v1.12.0; SemVer MINOR +
> CHANGELOG). Esta decision NO enciende #4: habilita el provisioning del secreto HMAC fuera del repo
> (SPEC-0081 AC1, capa HMAC). Implementacion gateada via TASK-0120.

## Contexto (el hallazgo)

DECISION-0039 sec.2 + SPEC-0081 AC1 exigen, como condicion de encendido de #4, que las claves
HMAC/privadas vivan FUERA del repo, con scan de secretos limpio (DECISION-0029 sec.5). Al ir a ejecutar
el provisioning se verifico que el runtime, tal como esta construido, **no tiene donde cargar el secreto
HMAC de event_auth fuera del repo**:

- `runtime/eventlog.py:read_protocol_config` lee `protocol.config.json` directo (utf-8-sig), sin overlay,
  sin env, sin merge.
- `signing_secret` -> `agent_auth_config` resuelve el secreto HMAC SOLO inline desde
  `event_auth.keys[actor]` (o `agent_registry.agents[].auth`), ambos dentro de ese archivo commiteado.
- `append_event` firma cada evento cuando `event_auth.enabled`; si el actor no tiene secreto resoluble,
  hard-fail "event auth signing key missing for actor" -> rompe el loop de submit_intent de ese agente.

Consecuencia: encender `event_auth.enabled` en vivo hoy exigiria poner el secreto HMAC inline en el
config commiteado, lo que (a) viola AC1 + la frontera no-secretos, (b) vuelve INUTIL la atestacion (HMAC
es simetrico: secreto en archivo legible = cualquiera con acceso de lectura forja). El harness SPEC-0081
pasa porque usa secretos inline SINTETICOS (fixture), que es justo lo prohibido para la instancia viva.

Aclaracion de alcance del hueco (verificado en codigo):

- La privada **Ed25519 de firma por agente YA es wrapper-side**: `runtime/llm_turn_wrapper.py` firma
  leyendo un PEM por ruta externa (`private_key_path`) y entrega solo la firma + keyid; el runtime
  guarda/verifica contra la clave PUBLICA. La privada nunca esta en el runtime ni en el config. **No
  necesita cambio.**
- Las claves PUBLICAS (`signature_config.public_keys`) y el `agent_registry` (identidades, key_id) son
  **no-secretos** y son commiteables.
- El UNICO secreto que el runtime mismo debe sostener para #4 es el **HMAC de event_auth** (capa de
  compatibilidad, DECISION-0039 sec.1). Ese es el hueco, y el unico alcance de esta decision.

## Decision

1. **Autorizar la resolucion del secreto HMAC de event_auth por REFERENCIA, no por literal.**
   `event_auth.keys[actor]` (y/o `agent_registry.agents[].auth`) puede llevar una **referencia** a un
   secreto que vive fuera del repo, en vez del literal `secret`. La referencia es no-secreto y SI se
   commitea. Mecanismo (espejo de la convencion ya existente del PEM Ed25519): una ruta de **keyfile
   gitignored** (`secret_file`) como forma primaria; **env var** (`secret_env`) como alternativa
   vendor-neutral. El literal `secret` inline se conserva SOLO para fixtures/goldens (compatibilidad).

2. **El secreto resuelto NUNCA entra al config canonicalizado ni al evento.** La resolucion ocurre en el
   momento de firmar/verificar (`signing_secret`), por un resolutor separado que **no** modifica el dict
   devuelto por `read_protocol_config`. Por tanto genesis = SHA256(canonical_json(protocol.config.json))
   y la cadena/anclaje NO dependen del valor del secreto; solo el hash de la firma (ya hoy) entra al
   evento. Esto preserva determinismo, replay y drift 0.

3. **Fail-closed, nunca silencioso.** Si `event_auth.enabled=true` y la referencia de un actor falta, es
   ilegible o resuelve vacio, `append_event`/`sign_event` deben **fallar con error explicito** (no
   escribir un evento sin firmar ni con secreto vacio). Verificacion analoga: ref ausente -> rechazo
   con clase, no "valido por defecto".

4. **Sin secretos en el repo (frontera dura, reiterada).** El config commiteado lleva SOLO referencias.
   El scan de secretos debe quedar limpio y, ademas, **gatear** que ningun `secret` literal de un actor
   vivo este commiteado. Los keyfiles referenciados viven bajo una ruta **gitignored** (p.ej.
   `secrets/` o `.protocol-secrets/`), nunca trackeada.

5. **Aditivo, neutral, off-by-default.** No introduce dominio. El template no cambia. El mecanismo solo
   actua cuando hay una referencia presente Y event_auth esta encendido; con literal inline o sin
   event_auth, el comportamiento es identico al actual (40+ goldens no se rompen).

6. **Cambio de runtime/contrato -> esta DECISION + SPEC-0082 + aprobacion humana.** Entra por SDD
   (DECISION-0039 sec.6): SPEC-0082 con acceptance_criteria + test_plan + golden cases; TASK-0120 la
   implementa (Codex), el Arquitecto revisa (maker!=checker). Introducir las referencias en el config
   vivo cambia genesis -> re-genesis coordinado (`runtime/regenesis.py`) para volver drift a 0 (operacion
   ya conocida en modo enforce-ON).

## Pasada de factibilidad (Codex, 2026-06-19)

Codex reviso el DRAFT contra el codigo y lo declaro **FACTIBLE**, con dos ajustes incorporados a
SPEC-0082 antes de promover (maker!=checker: Arquitecto autor del diseno, Codex revisor del draft; se
invertiran para implementar/revisar TASK-0120):

1. **Thread explicito de `root`** hasta verificacion/replay: `verify_event_auth` se llama hoy sin `root`
   desde `replay_events`/`rebuild_snapshot`/`EventWriter.state()`/validadores; como `secret_file` es
   relativo, TASK-0120 debe propagar `root` explicito y no depender del `cwd`.
2. **AC4 = check DEDICADO** (no `scan_encoding`/`scan_domain_neutrality`, que no cubren secretos ni la
   estructura de `event_auth.keys`).

Confirmaciones de invariante: AC5 viable (el secreto resuelto no entra a `compute_genesis_prev_hash` ni
`event_without_chain_fields`); AC7 viable con precedencia literal->file->env (fixtures byte-identicos);
AC3 viable (`sign_event` ya es fail-closed; basta clase propia `unresolved_key` antes de
`atomic_append_jsonl`); AC6 viable con allowlist `SECRET_DIRS`. Codex NO promovio TASK-0120 ni encendio #4.

## Alcance / No-alcance

- **En alcance:** resolver el secreto HMAC de event_auth por referencia (keyfile gitignored / env);
  gate de no-literal-commiteado; fail-closed; goldens.
- **Fuera de alcance:** re-disenar firma Ed25519 (ya wrapper-side), prev_hash o anclaje (ya existen);
  encender #4 (eso es el piloto de TASK-0117 tras esta capacidad); SA.4 / Capa C / subagents;
  proveer el anchor remote (infraestructura del operador); tocar la DB de Budget.

## Consecuencias

- Cierra la unica precondicion de provisioning de #4 que no tenia home (SPEC-0081 AC1 capa HMAC), sin
  meter secretos al repo y sin debilitar la atestacion.
- Habilita la secuencia: capacidad (esta) -> provisioning real (claves publicas + agent_registry
  commiteados; HMAC por keyfile gitignored; anchor remote del operador) -> piloto AC2/AC3/AC5 -> ON.
- Reversible: sin referencias y con event_auth OFF, el runtime se comporta como hoy.

## Alternativas consideradas

- **Meter el secreto HMAC inline en protocol.config.json.** Descartada: viola AC1 + no-secretos y
  vuelve inutil el HMAC (simetrico, archivo legible).
- **Overlay completo (merge de un `protocol.config.local.json` en read_protocol_config).** Descartada
  como forma primaria: cambiaria el dict canonicalizado -> riesgo de divergencia con genesis/anclaje y
  superficie de drift. La resolucion por referencia en el punto de firma es mas acotada y deja genesis
  intacto.
- **Prescindir de event_auth (HMAC) y dejar #4 = chain + Ed25519 + anchor.** Considerada pero fuera de
  esta decision: el operador pidio los 4 flags (DECISION-0039 sec.1). Si en el futuro se decide que la
  capa HMAC es redundante con Ed25519, seria una decision aparte.
