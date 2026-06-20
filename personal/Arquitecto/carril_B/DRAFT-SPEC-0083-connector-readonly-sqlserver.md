---
spec_id: SPEC-0083
task_id: TASK-0121
type: security
status: draft
linked_decisions:
  - DECISION-0044
  - DECISION-0015
  - DECISION-0040
  - DECISION-0041
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0083 (DRAFT) - Connector de datos read-only (deny-by-default, sin autoridad)

## Context

DECISION-0044 autoriza una capacidad GENERICA de connector de datos read-only, off-by-default, sobre el
`tool_policy` deny-by-default existente, con read-only REAL (prueba negativa), `trust_boundary` y
principio "el connector no concede autoridad". Esta SPEC fija el diseno verificable + el golden con
fixtures (sin DB viva). Primera instancia: SQL Server (Budget), configurada pero DESHABILITADA. NO
re-disena `tool_policy`; lo extiende.

## Scope

- Definir el shape de un `connector` en config (off-by-default) y su enforcement read-only en runtime.
- Golden determinista con **fixtures fake/recorded** (sin DB viva): lectura OK, escritura/DDL RECHAZADA
  con clase, `trust_boundary`/no-autoridad presentes, off-by-default byte-equivalente.
- Instancia SQL Server (Budget) registrada en config con `enabled=false`.

## Out Of Scope

- Lectura viva de la DB (GO posterior + §9 read-only por Codex).
- Config Budget viva (cadena/credenciales) y reglas fiscales -> `profiles/financiero_presupuesto/`.
- Connectors Git/CI; encender #4/SA.4/Capa C; captura de dataset / DEF-PII.

## Diseno

### Shape en config (`protocol.config.json`, off-by-default; template intacto)
```
"connectors": {
  "enabled": false,
  "registry": {
    "budget_sqlserver_ro": {
      "enabled": false,
      "backend": "sqlserver",
      "mode": "read_only",
      "trust_boundary": "external_untrusted_input",
      "grants_authority": false,
      "allowed_objects": ["schema", "views"],          // lista blanca de objetos legibles
      "connection_ref": "secret_file:.protocol-secrets/budget_sqlserver_ro.dsn",  // FUERA del repo
      "actions": ["read"]
    }
  }
}
```
- `connectors.enabled=false` global + `registry.<id>.enabled=false` por connector = doble off-by-default.
- `mode:"read_only"` + `actions:["read"]`: solo lectura. La conexion viva usa el `connection_ref`
  (referencia fuera del repo, patron DECISION-0043), NUNCA credencial literal commiteada.
- `grants_authority:false` + `trust_boundary:"external_untrusted_input"`: marca de no-autoridad.

### Enforcement (runtime, extension de tool_policy)
- Un connector es un **tool** `connector.read.<id>`; `is_tool_allowed` lo gobierna por `tool_policy`
  (deny-by-default). Solo la accion `read` puede tener allow; cualquier otra queda denegada.
- Capa de connector (`runtime/connectors.py` o equivalente): `connector_query(id, request, config)` que
  (a) exige `connectors.enabled` y `registry[id].enabled`; (b) clasifica el request: si es escritura/DDL
  (`write|insert|update|delete|create|drop|alter|truncate|merge|grant`) -> **rechaza** con
  `ConnectorReadOnlyError("write_rejected: <verbo>")` ANTES de tocar backend; (c) restringe a
  `allowed_objects`; (d) devuelve el resultado **envuelto** con `trust_boundary` + `grants_authority:false`
  (insumo no confiable). Sin backend vivo, opera contra el fixture.
- **Sin autoridad derivada:** el resultado del connector no muta `agent_registry`/`tool_policy`/capabilities
  ni produce eventos `applied:true`; si se anota en el log (futuro), va como dato con `trust_boundary`.

### Fixture backend (para el golden, sin DB viva)
- Backend `fixture` que lee un esquema/vistas/filas *recorded* desde un archivo JSON del caso (determinista,
  sin red, sin DB). Mismo contrato que `sqlserver` para que el golden ejerza el enforcement real.

## acceptance_criteria

- **AC1 - Deny-by-default.** Con `connectors.enabled=false` o `registry[id].enabled=false`, toda llamada al
  connector es rechazada (deshabilitado). Con tool_policy sin allow de `connector.read.<id>`, denegado.
- **AC2 - Read-only REAL (prueba negativa, BINARIA).** Todo request de escritura/DDL
  (write/insert/update/delete/create/drop/alter/truncate/merge/grant) es **RECHAZADO** con clase
  (`write_rejected`) ANTES de tocar el backend. Golden por vector (>=6 verbos). No es umbral: pasa/falla.
- **AC3 - Read OK + trust_boundary + sin autoridad.** Un request de lectura permitido (schema/view en
  `allowed_objects`) devuelve datos del fixture envueltos con `trust_boundary:"external_untrusted_input"` +
  `grants_authority:false`; NO muta estado ni capabilities; el resultado no concede permiso alguno.
- **AC4 - Lista blanca de objetos.** Lectura de un objeto fuera de `allowed_objects` -> rechazada
  (`object_not_allowed`). Golden negativo.
- **AC5 - Off-by-default byte-equivalente.** Con connectors deshabilitado, el estado/byte-output es
  identico al actual (sin connector). Template (`*.template.*`) NO incluye instancia Budget.
- **AC6 - Neutralidad de dominio.** El connector del core es generico (cero terminos fiscales/Budget);
  `scan_domain_neutrality` verde. La instancia Budget (id, allowed_objects, connection_ref) es config de
  la instancia viva, no del template; las reglas fiscales NO estan aqui (van al perfil).
- **AC7 - Sin secretos en repo + lectura viva gateada.** `connection_ref` es una referencia fuera del repo
  (no credencial literal); scan de secretos limpio. La **lectura viva** exige **§9 read-only verificada por
  Codex** (invariante read-only comprobado antes de cualquier lectura viva, registrado en TASK-0121) + GO
  del operador; el golden NO toca DB viva (fixtures).
- **AC8 - Gates verdes.** `validate_collaboration_state.py --root .` (drift B.3) + `scan_encoding.py` +
  `scan_domain_neutrality.py` + el nuevo golden `connector_readonly_cases` + sin regresion de
  `runtime_tool_policy_cases`.

## test_plan

- `examples/connector_readonly_cases/run_*.py` (fixture backend, sin DB viva), reporte JSON determinista
  (timestamps fijos), exit 0/1:
  - read permitido (schema + view en allowlist) -> OK + envoltura trust_boundary/grants_authority:false (AC3).
  - >=6 vectores de escritura/DDL -> rechazo `write_rejected` por verbo, ANTES del backend (AC2).
  - objeto fuera de allowlist -> `object_not_allowed` (AC4).
  - connectors.enabled=false / registry[id].enabled=false -> rechazo "disabled" (AC1).
  - off-by-default byte-equivalente (AC5).
- `runtime_tool_policy_cases` verde (sin regresion; el connector.read.<id> respeta deny-by-default).
- Scan de secretos: sin credenciales literales; `connection_ref` fuera del repo.
- Inspeccion: el resultado del connector no produce evento `applied:true` ni muta capabilities.

## closure_criteria

- AC1-AC8 cumplidos; revision maker!=checker (Codex implementa, Arquitecto reproduce) + honestidad Analista;
  connector DESHABILITADO en instancia viva (lectura viva = GO posterior + §9); SemVer MINOR + CHANGELOG;
  memoria actualizada. Esta SPEC NO habilita lectura viva ni #4.

## Risks

- **"Read-only" falso si el backend vivo tuviera permisos de escritura.** Mitigacion: rechazo en la capa
  del connector (verificable) + recomendacion de cuenta DB read-only (defensa en profundidad) + §9 antes de
  vivo.
- **Autoridad derivada del dato leido.** Mitigacion: `trust_boundary` + `grants_authority:false` + regla
  dura "el connector no concede autoridad"; el dato es insumo, no permiso.
- **Fuga de credencial al repo.** Mitigacion: `connection_ref` fuera del repo + scan de secretos.
- **Dominio fiscal filtrandose al core.** Mitigacion: connector generico; Budget/fiscal en el perfil.

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| Deny-by-default + disabled | TASK-0121 | connector_readonly_cases (disabled) | AC1 |
| Read-only real (prueba negativa) | TASK-0121 | >=6 vectores write/DDL rechazados | AC2 |
| Read OK + trust_boundary + sin autoridad | TASK-0121 | caso read + envoltura | AC3/AC4 |
| Off-by-default + neutralidad | TASK-0121 | byte-equivalente + scan_neutrality | AC5/AC6 |
| Sin secretos + lectura viva gateada (§9) | TASK-0121 | scan secretos + §9 registrado | AC7 |
