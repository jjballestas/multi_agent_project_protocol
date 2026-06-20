---
spec_id: SPEC-0083
task_id: TASK-0121
type: security
status: draft
linked_decisions:
  - DECISION-0044
  - DECISION-0041
  - DECISION-0033
  - DECISION-0040
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0083 (DRAFT) - Conector SQL Server READ-ONLY (contrato + golden con fixtures)

## Context

DECISION-0044 autoriza una capacidad neutral de conector de datos read-only. Esta SPEC fija el contrato
verificable y el golden determinista con fixtures (sin DB viva), para el adaptador SQL Server read-only
contra la DB migrada (`D:\Agentes\Ingenas\Budget`). Off-by-default, deny-by-default, read-only real,
trust_boundary, sin autoridad desde el dato. NO autoriza lectura viva (s.9 + GO posterior).

## Scope

- Framework neutral `runtime/connectors/` (o equivalente): contrato `ReadOnlyConnector` con `read(selector)
  -> RecordSet`, SIN metodos de escritura; registro gobernado por `tool_policy` (deny-by-default + scope).
- Adaptador `sqlserver_readonly`: abre en modo read-only (login read-only + `ApplicationIntent=ReadOnly`)
  + allowlist de sentencias que RECHAZA DML/DDL/EXEC.
- Etiquetado `trust_boundary` de todo `RecordSet` (`{connector_id, trust_boundary, read_only:true}`).
- Golden con adaptador FAKE/RECORDED (fixtures), sin DB viva.

## Out Of Scope

- Lectura viva de la DB real (s.9 read-only por Codex + GO posterior del operador).
- Connectors Git/CI; perfil `financiero_presupuesto` (reglas fiscales, fuera del core).
- Encender #4 / provisioning / flip. Tocar la DB o su migracion. Captura de PII.

## Diseno

### Contrato (neutral)

```
class ReadOnlyConnector(Protocol):
    connector_id: str
    trust_boundary: str
    def read(self, selector: ReadSelector) -> RecordSet: ...   # NO write/exec/ddl methods exist
```

- `ReadSelector`: descripcion de la lectura (p.ej. tabla/vista + columnas + filtro parametrizado). NUNCA
  texto SQL libre del llamador para escritura; solo lectura parametrizada/allowlisted.
- `RecordSet`: `{rows, columns, provenance: {connector_id, trust_boundary, read_only: true, source_type}}`.
- Registro: un connector solo es invocable si (a) `connectors.<id>.enabled = true` en config Y (b)
  `tool_policy` permite al agente el scope del connector. Sin ambos -> deny (no-op/error de clase).

### Read-only REAL (adaptador SQL Server)

1. **Credencial read-only fuera del repo** (patron DECISION-0043: `secret_file`/`secret_env`), usuario de
   BD con permisos solo SELECT; `ApplicationIntent=ReadOnly`. Cero secretos commiteados.
2. **Allowlist de sentencias:** solo `SELECT`/lectura parametrizada; RECHAZA por clase `INSERT/UPDATE/
   DELETE/MERGE/CREATE/ALTER/DROP/TRUNCATE/EXEC/sp_*/GRANT/...` ANTES de tocar la fuente.
3. **By-construction:** el contrato no expone metodo de escritura; el adaptador no abre handle escribible.

### Sin autoridad desde el dato

El `RecordSet` es DATO. El runtime no tiene ruta que convierta un `RecordSet` en capability/decision/
transicion de estado. Verificable por inspeccion estatica (AST/grep): ningun consumidor deriva autoridad
del contenido del connector.

## acceptance_criteria

- **AC1 - Lectura gobernada con provenance.** Con el connector habilitado + tool_policy allow, `read` sobre
  el fixture devuelve los records esperados, cada `RecordSet` con `provenance={connector_id, trust_boundary,
  read_only:true}`. Golden determinista.
- **AC2 - Read-only REAL (prueba negativa BINARIA).** Todo intento de escritura RECHAZADO con clase, por
  >=2 mecanismos independientes: (a) el contrato no expone metodo de escritura; (b) la allowlist rechaza
  DML/DDL/EXEC. Vectores fijos minimos, golden por vector: INSERT, UPDATE, DELETE, CREATE/ALTER, DROP,
  EXEC/sp_. Cada uno RECHAZADO (pasa/falla, bloqueante).
- **AC3 - Deny-by-default.** Connector deshabilitado (config off) O sin allow en tool_policy -> `read` NO
  ejecuta (no-op/error de clase). Habilitar exige ambos. Golden de ambos sub-casos.
- **AC4 - Sin autoridad desde el dato (estructural).** Inspeccion AST/estatica: ningun consumidor del
  `RecordSet` deriva capability/decision/permiso/transicion. Golden/check que falla si aparece tal ruta.
- **AC5 - Credencial read-only fuera del repo.** La credencial se resuelve por `secret_file`/`secret_env`
  (DECISION-0043); scan de secretos limpio (cero credencial commiteada). El adaptador nunca abre handle
  escribible.
- **AC6 - Neutralidad de dominio.** `scan_domain_neutrality` limpio: cero terminos fiscales/negocio en el
  framework/adaptador/template. (Las reglas fiscales van al perfil, fuera de esta SPEC.)
- **AC7 - Off-by-default byte-equivalente.** Con el connector off, el estado/comportamiento del runtime es
  byte-identico al actual; el template ship off.
- **AC8 - Golden con fixtures, SIN DB viva.** El golden usa un adaptador fake/recorded (result sets
  grabados); NO requiere ni toca la DB real. Reporte JSON determinista (timestamps fijos), exit 0/1.
- **AC9 - Gates verdes.** `validate_collaboration_state.py --root .` (drift 0), `scan_encoding.py`,
  `scan_domain_neutrality.py` + el nuevo `sqlserver_readonly_connector_cases` en CI. Sin regresion.

## test_plan

- `examples/sqlserver_readonly_connector_cases/run_*.py` (adaptador FAKE/RECORDED):
  - read habilitado + allow -> records + provenance trust_boundary (AC1).
  - 6 vectores de escritura (INSERT/UPDATE/DELETE/CREATE-ALTER/DROP/EXEC) -> RECHAZADOS con clase (AC2).
  - deny-by-default: off en config -> no-op; sin allow en tool_policy -> no-op (AC3).
  - sin-autoridad: check AST/estatico de que ningun consumidor deriva autoridad del RecordSet (AC4).
  - credencial por secret_file/secret_env + scan secretos limpio (AC5).
  - off-by-default byte-equivalente (AC7).
  - reporte JSON determinista, exit-code.
- s.9 (DECISION-0041): documentar el gate de pre-lectura-viva (Codex verifica read-only real ANTES de
  cualquier lectura viva); NO se ejecuta lectura viva en el golden.

## closure_criteria

- AC1-AC9 cumplidos; maker!=checker (Codex implementa, Arquitecto reproduce el golden + gates); honestidad
  Analista donde aplique; SemVer MINOR + CHANGELOG; memoria. NO lectura viva (s.9 + GO posterior). #4 OFF.

## Risks

- **Falso read-only (allowlist incompleta).** Mitigacion: read-only POR CONSTRUCCION (sin metodo de
  escritura) + credencial read-only + allowlist; defensa en profundidad, no una sola capa.
- **Fuga de la credencial.** Mitigacion: secret_file/secret_env fuera del repo + scan secretos en CI.
- **Autoridad derivada del dato por un consumidor futuro.** Mitigacion: AC4 estructural en CI (falla si
  aparece la ruta).
- **Arrastre de dominio al core.** Mitigacion: AC6 neutralidad; lo fiscal al perfil.

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| Lectura gobernada + provenance trust_boundary | TASK-0121 | sqlserver_readonly_connector_cases | AC1 |
| Read-only real (negativa binaria, 6 vectores) | TASK-0121 | 6 goldens de escritura rechazada | AC2 |
| Deny-by-default (config + tool_policy) | TASK-0121 | goldens off/no-allow | AC3 |
| Sin autoridad desde el dato (estructural) | TASK-0121 | check AST/estatico | AC4 |
| Credencial read-only fuera del repo | TASK-0121 | secret_file/env + scan secretos | AC5 |
| Neutralidad de dominio | TASK-0121 | scan_domain_neutrality | AC6 |
| Golden con fixtures sin DB viva | TASK-0121 | adaptador fake/recorded | AC8 |
