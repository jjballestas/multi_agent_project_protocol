---
spec_id: SPEC-0082
task_id: TASK-0120
type: security
status: draft
linked_decisions:
  - DECISION-0043
  - DECISION-0039
  - DECISION-0029
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0082 (DRAFT) - Resolucion del secreto HMAC de event_auth fuera del repo

## Context

DECISION-0043 autoriza resolver el secreto HMAC de `event_auth` por REFERENCIA (keyfile gitignored /
env), no por literal commiteado, para cerrar la precondicion de SPEC-0081 AC1 (capa HMAC) sin meter
secretos al repo. Esta SPEC fija el diseno tecnico verificable. **No re-implementa** firma Ed25519
(wrapper-side), prev_hash ni anclaje.

## Scope

- Extender la resolucion del secreto HMAC en `runtime/eventlog.py` (`agent_auth_config`/`signing_secret`)
  para aceptar `secret_file` (ruta a keyfile gitignored) y `secret_env` (nombre de variable de entorno),
  ademas del `secret` literal (legacy/fixtures).
- Resolutor que NO altera el dict de `read_protocol_config` (genesis intacto).
- Fail-closed: referencia presente pero irresoluble -> error explicito (no evento sin firmar).
- Gate de no-secreto-literal-commiteado para actores vivos.

## Out Of Scope

- Ed25519 (ya wrapper-side via `private_key_path`), prev_hash, anclaje.
- Overlay/merge de config (descartado en DECISION-0043).
- Encender #4 (piloto de TASK-0117) o proveer el anchor remote.

## Diseno

### Formas de `event_auth.keys[actor]` (y `agent_registry.agents[].auth`)

```
"keys": {
  "Arquitecto": { "key_id": "arquitecto:v1", "secret_file": "secrets/eventauth-arquitecto.key" },
  "Codex":      { "key_id": "codex:v1",      "secret_env":  "EVENTAUTH_CODEX" }
}
```

- `secret_file`: ruta RELATIVA al root del repo, que DEBE caer bajo una ruta gitignored (p.ej.
  `secrets/` o `.protocol-secrets/`). Su contenido (trimmed) es el secreto. La ruta es no-secreto y se
  commitea; el archivo NO.
- `secret_env`: nombre de variable de entorno cuyo valor es el secreto.
- `secret` literal: SOLO para fixtures/goldens; prohibido para actores vivos (gate AC4).
- Precedencia de resolucion (primera no-vacia gana): `secret` literal -> `secret_file` -> `secret_env`.
  (El literal primero preserva byte-identidad de los goldens existentes.)

### Punto de resolucion

`signing_secret(config, actor)` y `verify_event_auth(...)` llaman a un nuevo
`resolve_event_auth_secret(entry, root)` que materializa el valor en memoria SOLO al firmar/verificar.
`read_protocol_config` queda intacto (devuelve el config commiteado tal cual) -> genesis,
canonical_json, prev_hash y anclaje NO dependen del valor del secreto.

### Fail-closed

Si `event_auth.enabled=true`, el actor tiene una referencia (`secret_file`/`secret_env`) y esta no
resuelve a un valor no-vacio (archivo inexistente/ilegible/vacio, env ausente/vacia), entonces
`sign_event` lanza `EventLogError` con mensaje de clase (no escribe evento). En verificacion, ref
irresoluble -> `{"valid": False, "reason": "unresolved_key"}` (no "valido por defecto").

### Seguridad de ruta

`secret_file` se valida: ruta relativa, normalizada, DEBE quedar dentro de un directorio gitignored
permitido (lista en config o constante `SECRET_DIRS = {"secrets", ".protocol-secrets"}`); rutas fuera
(absolutas, con `..` que escapen, o fuera de los dirs permitidos) -> rechazo explicito. Evita leer
archivos arbitrarios del FS via el config.

## acceptance_criteria

- **AC1 - Resolucion por keyfile.** Con `secret_file` apuntando a un keyfile gitignored valido y
  `event_auth.enabled=true`, `append_event` firma y `verify_event_auth` valida; el valor del secreto NO
  aparece en el evento ni en el config canonicalizado. Golden determinista.
- **AC2 - Resolucion por env.** Idem con `secret_env`; con la env presente firma/verifica; el valor no
  aparece en disco. Golden determinista (env inyectada por el runner).
- **AC3 - Fail-closed.** Referencia presente pero irresoluble (file ausente/vacio, env ausente) ->
  `sign_event` lanza error de clase y NO escribe evento; `verify_event_auth` -> invalido con razon. Un
  golden por sub-caso (file-missing, env-missing). NUNCA evento sin firmar.
- **AC4 - Sin secreto literal commiteado (gate).** El scan de secretos (o un check dedicado) RECHAZA un
  `secret` literal para cualquier actor de `agent_registry`/`event_auth.keys` en el config commiteado;
  permite `secret_file`/`secret_env` y permite `secret` literal solo en fixtures bajo `examples/`.
- **AC5 - Genesis intacto.** Introducir/cambiar una referencia NO cambia el valor de `canonical_json`
  consumido por la firma del evento ni la semantica de prev_hash respecto al secreto; el secreto resuelto
  no entra a `signable_event`. (El config commiteado SI cambia al agregar la referencia -> re-genesis es
  esperado; lo que AC5 fija es que el VALOR del secreto no participa del hash.) Golden: dos secretos
  distintos para el mismo evento producen firmas distintas pero `signable_event`/`prev_hash` identicos.
- **AC6 - Seguridad de ruta.** `secret_file` fuera de los dirs permitidos o con traversal -> rechazo
  explicito antes de leer. Golden negativo.
- **AC7 - Compatibilidad.** Los goldens existentes que usan `secret` literal inline siguen verdes byte a
  byte (`attestation_health_cases`, `chain_auth_combined_cases`, `agent_signature_cases`, etc.).
- **AC8 - Gates verdes.** `validate_collaboration_state.py --root .` (drift B.3), `scan_encoding.py`,
  `scan_domain_neutrality.py` + el nuevo `event_auth_secret_resolution_cases` en CI.

## test_plan

- `examples/event_auth_secret_resolution_cases/run_*.py`:
  - keyfile valido -> firma/verifica; secreto ausente del evento y del config canonicalizado (AC1).
  - env valido -> firma/verifica (AC2).
  - file-missing / env-missing -> error de clase, sin evento (AC3, fail-closed).
  - dos secretos distintos -> firmas distintas, signable_event/prev_hash identicos (AC5).
  - secret_file con traversal/absoluto -> rechazo (AC6).
  - reporte JSON determinista (timestamps fijos), exit 0/1.
- Check de gate AC4: literal de actor vivo en config commiteado -> exit 1.
- Sin regresion: suites #4 existentes verdes (AC7).

## closure_criteria

- AC1-AC8 cumplidos; revision maker!=checker (Codex implementa, Arquitecto reproduce); SemVer MINOR +
  CHANGELOG; memoria actualizada. Esta SPEC NO enciende #4; habilita su provisioning.

## Risks

- **Keyfile gitignored borrado/rotado mal -> firma cae.** Mitigacion: fail-closed explicito + runbook de
  provisioning (cada agente coloca su keyfile antes del piloto).
- **secret_env filtrada en logs.** Mitigacion: nunca loguear el valor; solo key_id.
- **Falsa sensacion de seguridad del HMAC simetrico.** Declarado: el HMAC es capa de compatibilidad; la
  no-repudiacion entre agentes (A2) la da Ed25519 wrapper-side, no el HMAC.

## Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Resolucion HMAC por keyfile/env fuera del repo | TASK-0120 | event_auth_secret_resolution_cases | AC1/AC2 |
| Fail-closed ante referencia irresoluble | TASK-0120 | goldens file-missing/env-missing | AC3 |
| Sin secreto literal commiteado (gate) | TASK-0120 | check de gate AC4 | AC4 |
| Secreto fuera del hash (genesis/prev_hash intactos) | TASK-0120 | golden signable_event identico | AC5 |
| Seguridad de ruta (anti-traversal) | TASK-0120 | golden negativo | AC6 |
| Compatibilidad con goldens existentes | TASK-0120 | suites #4 existentes | AC7 |
