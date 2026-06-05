---
decision_id: DECISION-0006
title: Robustez operacional — CI completo, harnesses tolerantes a runtime y migración asistida
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0003, DECISION-0004, DECISION-0005, TASK-0016, TASK-0017, TASK-0018, TASK-0019]
phase: P2
---

# DECISION-0006 — Robustez operacional

## Contexto

Auditoría externa del protocolo (operador humano, 2026-06-05) identificó tres brechas que impiden
llamarlo "profesional robusto" todavía. Las tres se verificaron en el repo:

1. **Portabilidad Python frágil en la práctica.** Los harness de validación
   (`examples/sdd_validation_cases/run_sdd_cases.ps1`,
   `examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`) invocan `& python` **y**
   `& powershell` y comparan salidas; si **cualquiera** de los dos runtimes falta (p.ej. `python`
   ausente del PATH de PowerShell en una máquina dada), el harness cae por **entorno**, no por
   lógica. Un harness de paridad que exige ambos runtimes a la vez es doblemente frágil.

2. **CI incompleto.** `.github/workflows/validate.yml` solo ejecuta `validate_collaboration_state.py`
   sobre el dogfood y sobre `minimal_instance`. **No** ejecuta: el validador PowerShell, el harness
   SDD, el harness de comunicación compacta, ni el **scan de neutralidad de dominio** que
   `AGENTS.md` §5 declara como quality gate. Hay una grieta entre el contrato (§5) y lo que CI
   realmente verifica.

3. **Adopción/migración entre proyectos manual.** El riesgo de *drift* está reconocido
   (`PROJECT_STATE.json` → risks) pero no resuelto: cada instancia adopta versiones por decisión
   (correcto por DECISION-0001) sin herramienta que reduzca el costo operativo de detectar y
   aplicar el delta entre versiones del protocolo.

## Principio

**El contrato y lo verificado deben coincidir, y la verificación no puede depender de un entorno
concreto.** Todo gate prometido en `AGENTS.md` corre en CI; ningún harness falla por un runtime
ausente; la adopción entre versiones se asiste sin romper la gobernanza por-decisión.

## Decisión

### 1. Política de runtime en harnesses — skip con aviso
Los harness de paridad (`run_sdd_cases.ps1`, `run_compact_comms_cases.ps1`, y cualquier harness
futuro) **no fallan por entorno**:

- **Detección con fallback.** Python: `python` → `py -3` → `python3`. PowerShell: `pwsh` →
  `powershell`. Se resuelve el primero disponible.
- Si **un** runtime falta, su mitad del caso se marca **`SKIPPED (WARNING)`** con mensaje visible
  (qué runtime faltó y por qué se omitió), y el harness continúa con el runtime disponible.
- La **paridad** entre `.py` y `.ps1` se verifica **solo cuando ambos** están presentes.
- El harness falla (exit ≠ 0) **solo** por: (a) lógica — el runtime presente da un exit distinto
  del esperado o las salidas difieren cuando ambos están; o (b) **ningún** runtime disponible.
- Al final, el harness **resume** qué se ejecutó y qué se saltó (sin truncado silencioso).

Endurecer esto a "exigir ambos runtimes" sería un cambio de política → requeriría nueva decisión.

### 2. CI completo (honra `AGENTS.md` §5)
`.github/workflows/validate.yml` ejecuta, además de los dos `validate.py` actuales:

- **Validador PowerShell** (`validate_collaboration_state.ps1`) vía `pwsh` en `ubuntu-latest`,
  sobre dogfood + `minimal_instance` (garantiza que el `.ps1` no diverge sin que CI lo note).
- **Harness SDD** (`run_sdd_cases.ps1`) y **harness de comunicación compacta**
  (`run_compact_comms_cases.ps1`). Con ambos runtimes presentes en CI, ejercitan la paridad real.
- **Scan de neutralidad de dominio** (§3) sobre el core y los `*.template.*`.

El job de CI tiene **ambos runtimes** instalados (`setup-python` + `pwsh` preinstalado en el
runner) precisamente para que la paridad se ejercite de verdad, no se saltee.

### 3. Scan de neutralidad de dominio (gate ejecutable)
Nuevo gate dedicado, hoy inexistente como script:

- Scripts `scripts/scan_domain_neutrality.py` y `.ps1` (paridad), que escanean el **core** y los
  archivos `*.template.*` buscando una **denylist** de términos de negocio/dominio.
- La denylist y las rutas escaneadas/exentas se configuran en `protocol.config*.json` (neutral:
  el repo provee una denylist base y cada instancia puede extenderla). El scan **no** mira
  `profiles/`, `examples/` de instancias de dominio, ni áreas privadas de agentes.
- Exit ≠ 0 si hay coincidencia en zona neutral. Se integra en CI (§2) y queda disponible local.

### 4. Migración/upgrade asistida entre versiones (anti-drift)
Herramienta `scripts/upgrade_instance.(py/ps1)` que **asiste**, no impone:

- Lee `protocol_version` de la instancia y la del master de este repo; lista los **deltas** de
  archivos núcleo y `*.template.*` entre ambas versiones (qué cambió, en qué versión).
- Emite un **reporte de adopción** con acciones recomendadas; **no aplica** cambios sin
  confirmación explícita. La adopción sigue siendo **por decisión** de la instancia (preserva
  DECISION-0001 y el risk de drift declarado): la herramienta baja el costo operativo de
  detectar y razonar el delta, sin automatizar la política.
- Diseño primero (analysis, TASK-0016) → implementación (TASK-0019).

### 5. Versionado y compatibilidad (DECISION-0001)
Todo lo anterior es **aditivo** ⇒ **MINOR, target v0.6.0**. No cambia formatos obligatorios ni
invalida estado/mensajes/handoffs históricos; los harness pasan a ser *más* tolerantes, no menos.
Endurecer gates (exigir ambos runtimes, o convertir WARNINGs en errores de build) sería **MAJOR**
y requeriría aprobación humana. Neutral de dominio en todo el core.

## Backlog
- **TASK-0016** (Claude, analysis): diseño de robustez operacional + specs (SPEC para CI, harness
  tolerante a runtime, scan de neutralidad, upgrade asistido). Desbloquea a Codex.
- **TASK-0017** (Codex, implementation): CI completo + scan de neutralidad de dominio (§2, §3).
- **TASK-0018** (Codex, implementation): harness tolerantes a runtime — skip con aviso (§1).
- **TASK-0019** (Codex, implementation): herramienta de migración/upgrade asistida (§4).

## Consecuencias
- **Positivas:** el gate de §5 deja de ser una promesa; CI verifica ambos validadores y los
  harness; ninguna máquina queda fuera por falta de un runtime; la adopción entre versiones tiene
  herramienta de soporte. Esto cierra las tres brechas de la auditoría.
- **Costo:** más superficie de CI (jobs más largos); dos scripts nuevos (scan, upgrade) a mantener
  con paridad `.py`/`.ps1`; disciplina de denylist neutral.
- **Seguimiento:** TASK-0016..0019. La capa se publica como **v0.6.0** al cerrarlos.

## Alternativas consideradas
- **Exigir ambos runtimes y documentar requisitos:** descartado ahora — máxima paridad pero menor
  portabilidad; es justo la fragilidad reportada. Reservado como posible MAJOR futuro.
- **Migración automática (aplicar el delta sin confirmación):** descartado — rompería la
  gobernanza por-decisión (DECISION-0001) y la autonomía de cada instancia.
- **Solo documentar las brechas sin ejecutarlas en CI:** insuficiente; mantiene la grieta
  contrato↔verificación.
