# DISEÑO — Robustez operacional (CI completo, harness tolerante a runtime, scan de neutralidad, upgrade asistido)

> Entregable de **TASK-0016** (Claude, `analysis`). Implementa el diseño que fija
> [DECISION-0006](../decisions/DECISION-0006-robustez-operacional.md). Es la **fuente de verdad**
> contra la que se implementan TASK-0017/0018/0019. Neutral de dominio. La capa se publica como
> **v0.6.0** (MINOR, aditivo).

## 0. Resumen

Tres brechas de la auditoría 2026-06-05 → tres contratos:
- **§1 Harness tolerante a runtime** (TASK-0018, SPEC-0018): detección con fallback + `SKIPPED
  (WARNING)`; el harness no cae por entorno.
- **§2 CI completo + §3 scan de neutralidad** (TASK-0017, SPEC-0017): todo gate de `AGENTS.md` §5
  corre en CI, incluido un scan de neutralidad **ejecutable** (hoy inexistente como script).
- **§4 Upgrade asistido** (TASK-0019, SPEC-0019): reporte de deltas entre versión de instancia y
  master, **sin aplicar sin confirmación** (preserva DECISION-0001).

## 1. Dos conjuntos de archivos (definición compartida)

Para no reinventar criterios en cada script, el diseño fija dos conjuntos por **ruta relativa a la
raíz de la instancia**:

### 1.1 Superficie neutral (la que NO puede contener términos de dominio)
Archivos genéricos del protocolo y masters publicables:
- `AGENTS.template.md`, `Area_comun/README.template.md`, `protocol.config.template.json`
- `Area_comun/state/*.template.json`
- `Area_comun/protocol/*.md` (docs de protocolo genéricos)
- `Area_comun/specs/*_TEMPLATE.md`
- `profiles/PROFILE_TEMPLATE/**` (el master de perfil, no perfiles concretos)
- `scripts/*.py`, `scripts/*.ps1` (genéricos)

### 1.2 Conjunto adoptable (lo que una instancia copia del master y puede quedar desfasado)
La superficie neutral **más** los docs de proceso publicables. En la práctica, para el upgrade
asistido, el conjunto adoptable = todos los archivos versionados del repo del protocolo **excepto**:
`Area_comun/decisions/**`, `Area_comun/tasks/**`, `Area_comun/handoffs/**`, `Area_comun/reports/**`,
`Area_comun/artifacts/**`, `Area_comun/mailbox/**`, `Area_comun/state/*.json` (vivos, no `.template`),
`AGENTS.md`, `CLAUDE.md`, `protocol.config.json`, `README*.md`, `RESUME.md`, `CHANGELOG.md`,
`examples/**`, `Claude/**`, `Codex/**`, `.git/**`.

**Exentos del scan de neutralidad** (contienen términos de stack/negocio **por diseño**): `profiles/`
(perfiles concretos como `dotnet_enterprise` traen .NET/SQL/Azure legítimamente), `examples/`
(fixtures de instancia), y todo el área viva del dogfood (decisions/tasks/handoffs/reports/artifacts/
state vivos, `AGENTS.md`, `CLAUDE.md`, `README*`, `RESUME`, `CHANGELOG`, `protocol.config.json`) que
**legítimamente** nombra al piloto `bot_spot_ai_strategy_pack`.

> Clave: la neutralidad se exige al **core genérico y a los masters**, no a la instancia dogfood ni a
> los perfiles. Por eso el scan apunta a §1.1 y exime el resto.

Ambos conjuntos se expresan como **glob allowlist + denylist** en `protocol.config*.json` (§3.2),
para que cada instancia los ajuste sin tocar los scripts.

## 2. §1 — Harness tolerante a runtime (contrato para SPEC-0018)

### 2.1 Detección con fallback
- **Python:** primer comando cuyo `--version` salga 0, en orden: `python`, `py -3`, `python3`.
- **PowerShell:** `pwsh` → `powershell`.
- Cada harness resuelve ambos al inicio y reporta qué resolvió (o `none`).

### 2.2 Semántica por caso
Por cada caso golden (que hoy compara `.py` vs `.ps1`):
- Si el runtime está disponible → ejecutar su validador y comparar su exit con el esperado.
- Si **falta** → marcar esa mitad `SKIPPED (WARNING)` con mensaje (`python no resuelto: se omite`).
- **Paridad** (igualdad de salida normalizada `.py`↔`.ps1`) se evalúa **solo si ambos** ejecutaron.

### 2.3 Cuándo falla el harness (exit 1)
- (a) un runtime **presente** da exit distinto del esperado; **o**
- (b) ambos presentes y sus salidas difieren; **o**
- (c) **ningún** runtime disponible (no se pudo verificar nada).
Si solo hubo skips por ausencia de un runtime pero el presente pasó todo → **exit 0**.

### 2.4 Resumen final (sin truncado silencioso)
Última línea: `RESUMEN: py[ok=N skip=M fail=K] ps[...] paridad[checked=P skipped=Q]`. Si hubo
skips, el harness lo dice explícitamente.

### 2.5 No-regresión
Con **ambos** runtimes presentes, los exits esperados y la comparación de paridad **no cambian**
respecto al comportamiento actual.

## 3. §2-§3 — CI completo + scan de neutralidad (contrato para SPEC-0017)

### 3.1 `.github/workflows/validate.yml`
Un job en `ubuntu-latest` con **ambos runtimes** (`actions/setup-python` + `pwsh` preinstalado),
que ejecuta, además de los dos `validate.py` actuales (dogfood + `minimal_instance`):
1. `validate_collaboration_state.ps1` (vía `pwsh`) sobre dogfood + `minimal_instance` (paridad real).
2. `examples/sdd_validation_cases/run_sdd_cases.ps1` (vía `pwsh`).
3. `examples/compact_comms_validation_cases/run_compact_comms_cases.ps1` (vía `pwsh`).
4. `scripts/scan_domain_neutrality.py --root .` (gate de `AGENTS.md` §5).
Cualquier paso en rojo ⇒ build roja. (Con ambos runtimes, los harness de §1 **no** saltan: ejercen
paridad.)

### 3.2 Scan de neutralidad — `scripts/scan_domain_neutrality.(py|ps1)`
- Lee `protocol.config.json` → bloque nuevo `domain_neutrality`:
  ```json
  {
    "domain_neutrality": {
      "enabled": true,
      "denylist": ["trading", "spot", "binance", "backtest", "estrategia de trading"],
      "scan_globs": ["AGENTS.template.md", "Area_comun/README.template.md",
                     "protocol.config.template.json", "Area_comun/state/*.template.json",
                     "Area_comun/protocol/*.md", "Area_comun/specs/*_TEMPLATE.md",
                     "profiles/PROFILE_TEMPLATE/**", "scripts/*.py", "scripts/*.ps1"],
      "exempt_globs": ["profiles/**", "examples/**", "Claude/**", "Codex/**",
                       "Area_comun/decisions/**", "Area_comun/tasks/**",
                       "Area_comun/handoffs/**", "Area_comun/reports/**",
                       "Area_comun/artifacts/**", "Area_comun/mailbox/**"]
    }
  }
  ```
- **Matching:** case-insensitive, por **límite de palabra** (`\bterm\b`) para evitar falsos
  positivos (`bot` no debe matchear `bootstrap`/`robot`). `scan_globs` define qué se mira;
  `exempt_globs` resta. Términos multi-palabra permitidos.
- **Salida:** por cada hallazgo `ruta:linea: término`. Exit `0` si limpio, `1` si hay hallazgos.
- `enabled:false` o bloque ausente ⇒ **sin scan** (exit 0). Aditivo: instancias que no lo declaren
  no se rompen.
- **Denylist base mínima y extensible:** el repo trae términos del piloto; cada instancia añade los
  suyos. Conservadora por defecto (mejor pocos falsos positivos que ruido).
- **Paridad `.py`↔`.ps1`:** misma lógica, mismos mensajes; golden cases positivo y negativo en
  `examples/neutrality_scan_cases/`.

### 3.3 Config: template y dogfood
- `protocol.config.template.json`: añadir `domain_neutrality` con `enabled:true`, denylist base
  vacía o mínima neutral y los `scan_globs/exempt_globs` de arriba (las instancias completan
  denylist).
- `protocol.config.json` (dogfood): `enabled:true` con denylist del piloto
  (`trading`, `spot`, `binance`, `backtest`, …) para que el scan **demuestre** valor sobre este repo
  sin marcar el área viva (exenta).

## 4. §4 — Upgrade asistido (contrato para SPEC-0019)

### 4.1 Invocación
`scripts/upgrade_instance.(py|ps1) --instance <ruta> [--master <ruta-repo-protocolo>] [--report <archivo>]`.
`--master` por defecto = la raíz del repo del protocolo desde donde se ejecuta.

### 4.2 Comportamiento
1. Lee `protocol_version` de `<instance>/protocol.config.json` y del master.
2. Para cada archivo del **conjunto adoptable** (§1.2) presente en el master: compara contra la
   copia de la instancia por **contenido** (hash/normalizado) → clasifica `nuevo` (no existe en
   instancia), `cambiado` (difiere), `igual`, o `eliminado` (existe en instancia, no en master).
3. Emite un **reporte de adopción** (markdown) con: versiones origen/destino, tabla de deltas y
   **acciones recomendadas** por archivo. Si hay CHANGELOG en el master, enlaza la sección de
   versiones entre ambas (best-effort; si no, omite).
4. **No escribe nada en la instancia.** Sin flag `--apply` en v0.6.0 (reservado a un futuro que
   exigiría confirmación interactiva + decisión de la instancia). El reporte es el entregable.

### 4.3 Garantías
- **Read-only sobre la instancia** (solo lee; a lo sumo escribe el `--report` donde se le indique).
- Preserva la **adopción-por-decisión** (DECISION-0001): la herramienta informa, la instancia decide.
- **Neutral:** el reporte habla de rutas/versiones/deltas, nunca de dominio.

### 4.4 Pruebas
Fixtures: una instancia "desfasada" (subconjunto de masters de una versión previa) y una "al día";
verificar que el reporte lista los deltas correctos y que **no** se modifica la instancia.

## 5. Versionado y neutralidad
Todo aditivo ⇒ **MINOR v0.6.0**. Endurecer (exigir ambos runtimes, WARNING→error de build, `--apply`
automático) sería **MAJOR**. Ningún script ni config introduce términos de dominio en §1.1.

## 6. Índice de specs del rollout (spec_id por tarea)

| Tarea | spec_id | Tipo | §DECISION-0006 |
|-------|---------|------|----------------|
| TASK-0017 | `Area_comun/specs/SPEC-0017-ci-completo-scan-neutralidad.md` | implementation | §2, §3 |
| TASK-0018 | `Area_comun/specs/SPEC-0018-harness-tolerante-runtime.md` | implementation | §1 |
| TASK-0019 | `Area_comun/specs/SPEC-0019-upgrade-asistido.md` | implementation | §4 |

Con estas specs, Codex puede completar el frontmatter SDD de cada tarea y pasarlas a `ready`/`claimed`.

## 7. Orden de implementación recomendado
1. **TASK-0018** (harness tolerante) — independiente y desbloquea CI robusto.
2. **TASK-0017** (CI + scan) — usa harness ya tolerantes; añade el scan y los pasos de CI.
3. **TASK-0019** (upgrade asistido) — independiente de 0017/0018; puede ir en paralelo.
4. Cerrar y publicar **v0.6.0** (mover Unreleased en CHANGELOG + tag), revisión cruzada del arquitecto.
