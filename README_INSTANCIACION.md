# Guia de instanciacion del protocolo multiagente

> **Propietario — All Rights Reserved.** Ver [`LICENSE`](LICENSE) y
> [`DECISION-0010`](Area_comun/decisions/DECISION-0010-licenciamiento-propietario.md). La
> instanciacion descrita aqui es para **uso autorizado del titular**; no es una invitacion a copiar
> o reutilizar el protocolo.

Esta carpeta empaqueta una metodologia generica para coordinar proyectos de software con
varios agentes. El protocolo define como se trabaja: tareas, claims, mailbox, decisiones,
handoffs y validacion de estado. El dominio de cada proyecto se declara en la instancia.

## 1. Crear un proyecto nuevo con script

Desde la raiz de `multi_agent_project_protocol`, genera una instancia nueva con:

```powershell
python scripts\new_instance.py `
  --source-template . `
  --target D:\Agentes\mi_nuevo_proyecto `
  --project-name mi_nuevo_proyecto `
  --project-goal "Objetivo operativo del proyecto." `
  --project-description "Descripcion breve del proyecto." `
  --architect Claude `
  --implementer Codex `
  --human-owner "operador humano" `
  --phase-id P0 `
  --phase-name "Bootstrap" `
  --phase-goal "Dejar una instancia inicial valida."
```

El script usa solo Python stdlib, copia los masters `*.template.*` a sus archivos canonicos,
crea la estructura necesaria de `Area_comun/` y sustituye todos los placeholders `{{...}}`.
Si queda un placeholder sin resolver, falla. Si el `--target` existe y no esta vacio, falla salvo
que se pase `--force`.

Parametros minimos obligatorios:

- `--source-template`
- `--target`
- `--project-name`
- `--project-goal`
- `--project-description`
- `--architect`
- `--implementer`
- `--human-owner`
- `--phase-id`
- `--phase-name`
- `--phase-goal`

Parametros utiles opcionales:

- `--protocol-version`: declara la version del protocolo que sigue la instancia. Si se omite, el
  script toma la version del `protocol.config.json` o `PROJECT_STATE.json` del template fuente.
- `--domain-critical-boundaries`: fronteras duras del proyecto.
- `--stack-decisions`: decisiones de stack iniciales.
- `--quality-gates`: gates de calidad iniciales.
- `--human-approval-points`: puntos de aprobacion humana.
- `--in-scope` / `--out-of-scope`: alcance inicial.
- `--phase-exit-criteria`: criterio inicial de salida de fase.
- `--force`: permite regenerar un target no vacio.

La instancia generada deja `TASK_INDEX.json` vacio pero valido. La primera tarea real se crea
despues copiando `Area_comun/protocol/TASK_TEMPLATE.md` dentro de `Area_comun/tasks/` y
registrandola en `Area_comun/state/TASK_INDEX.json`.

### Elegir tier de adopcion

El protocolo se instancia en dos tiers, definidos por `adoption_tier`:

| Tier | Para que sirve | Que copia | Estado por defecto |
|---|---|---|---|
| `coordination` | Adoptar la disciplina de trabajo sin motor automatizado. Es el default. | `AGENTS.md`, `Area_comun/`, estado, plantillas, validadores basicos. | Coordinacion manual. |
| `runtime` | Adoptar tambien el motor local de orquestacion y sus gates. | Todo lo anterior + `runtime/`, scripts de gates, workflow CI y configuracion runtime. | Motor presente pero apagado. |

Usa `coordination` cuando el proyecto solo necesita tareas, claims, mailbox, decisiones y handoffs
auditables. Usa `runtime` cuando tambien quieres replay, routing, validacion de turnos, apply/gate,
observabilidad, presupuesto y opcion futura de agentes reales bajo gate.

Ejemplos:

```powershell
python scripts\new_instance.py ... --tier coordination
python scripts\new_instance.py ... --tier runtime
```

Si omites `--tier`, el script usa `coordination`. En el tier `runtime`, `protocol.config.json`
nace con `runtime.enabled:false`, `tool_policy.enabled:false`, `event_auth.enabled:false` y
`runtime.real_invoker.enabled:false`; tener los archivos del motor no lo activa.

### Upgrade entre versiones

Para comparar una instancia con el master del protocolo:

```powershell
python scripts\upgrade_instance.py --instance D:\Agentes\mi_nuevo_proyecto --master . --report upgrade.md
```

El reporte es informativo: no muta la instancia. Si `adoption_tier` es `runtime`, el upgrade propone
deltas de `runtime/**`, workflow de CI y `runtime_version`; si el tier es `coordination` o falta, no
propone runtime y conserva el comportamiento ligero. Los artefactos de ejecucion (`runtime/state/`,
`runtime/runs/`, `__pycache__/`) quedan fuera del upgrade.

Para reglas de versionado y migracion (`protocol_version`, `runtime_version`, `schema_version`,
`profile_version`, compatibilidad por tier y paso de `coordination` a `runtime`), ver
[`Area_comun/protocol/PACKAGE_VERSIONING.md`](Area_comun/protocol/PACKAGE_VERSIONING.md).

Para producir y verificar un release endurecido con SBOM, manifiesto, provenance y firma, ver
[`Area_comun/protocol/RELEASE_ENGINEERING.md`](Area_comun/protocol/RELEASE_ENGINEERING.md).

### Firma externa de releases

La firma de autenticidad real es opt-in y no guarda comandos, claves ni identidad privada en el repo. El
emisor configura el backend por flags en el momento de publicar:

```powershell
python scripts\sign_release.py `
  --manifest dist\vX.Y.Z\manifest.json `
  --backend external-command `
  --sign-command "<comando-local-que-emite-firma-o-bundle-por-stdout>" `
  --identity "<identidad-publica-del-firmante>" `
  --issuer "<issuer-oidc-publico>" `
  --signature-field bundle `
  --output dist\vX.Y.Z\signature.json
```

El comando externo recibe `{digest}` y `{manifest}` como placeholders; si no se usan placeholders, el digest
se envia por stdin. Para verificar, el adoptante recibe la identidad publica, el issuer y el comando exacto:

```powershell
python scripts\verify_release.py `
  --root . `
  --manifest dist\vX.Y.Z\manifest.json `
  --signature dist\vX.Y.Z\signature.json `
  --backend external-command `
  --verify-command "<comando-publico-de-verificacion>"
```

`--verify-command` puede usar `{digest}`, `{manifest}`, `{signature}`, `{bundle}`, `{signature_file}`,
`{identity}`, `{issuer}` y `{key_id}`. Si no usa placeholders, recibe el JSON de firma por stdin. Un emisor que
use una herramienta concreta (por ejemplo, keyless con identidad OIDC) debe publicar en el reporte de release:
identidad, issuer, backend declarado, archivo de firma, comando exacto de verificacion y si requiere red o
bundle offline. El backend `fixture-hmac-sha256` es solo para golden/CI determinista; no afirma autenticidad
de un release real.

#### Receta de verificacion publicada para v1.1.0 (cosign keyless)

> **Fuente firmada autoritativa:** la receta de verificacion AUTORITATIVA (cubierta por la firma del
> release) vive en
> [`Area_comun/reports/REPORT-20260610-release-v1.1.0.md`](Area_comun/reports/REPORT-20260610-release-v1.1.0.md).
> Esta copia en el README es solo para descubrabilidad y **NO esta cubierta por la firma** (este archivo
> esta dentro del SBOM, por lo que se publica en un commit posterior al tag). Ante cualquier duda de
> manipulacion de este README, la fuente firmada es el REPORT.

El release `v1.1.0` esta firmado con cosign keyless (sigstore). Identidad publica del firmante
`john.ballestas@gmail.com`, issuer OIDC `https://accounts.google.com`, transparencia en Rekor
(`logIndex 1777945271`, `https://search.sigstore.dev/?logIndex=1777945271`). Un tercero verifica la
autenticidad con cualquiera de estos dos comandos (cosign requerido en el PATH; la verificacion keyless
consulta Rekor y por tanto requiere red, o un bundle offline):

```text
# cosign directo (autenticidad):
cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
  --certificate-identity john.ballestas@gmail.com \
  --certificate-oidc-issuer https://accounts.google.com \
  dist/v1.1.0/manifest.json

# cadena del protocolo (integridad + procedencia + autenticidad, ok:true global):
python scripts/verify_release.py --root . --manifest dist/v1.1.0/manifest.json \
  --signature dist/v1.1.0/signature.json --backend external-command \
  --verify-command "cosign verify-blob --bundle dist/v1.1.0/cosign.bundle.json \
    --certificate-identity john.ballestas@gmail.com \
    --certificate-oidc-issuer https://accounts.google.com {manifest}"
```

### Operar agentes reales

El wrapper de CLI real existe solo para instancias runtime y sigue apagado por defecto. Una instancia
solo puede invocar un agente real si antes registra su propia aprobacion humana, por ejemplo:

```json
{
  "runtime": {
    "enabled": true,
    "real_invoker": {
      "enabled": true,
      "activation_decision": "DECISION-XXXX",
      "approved_by": "operador humano",
      "approved_at": "YYYY-MM-DD"
    }
  }
}
```

La ejecucion real exige ademas un unico turno:

```powershell
python runtime\orchestrator.py --run --adapter llm --llm-invoker subprocess --once --allow-real-invoker --llm-command "<command>"
python runtime\orchestrator.py --run --adapter llm --llm-invoker subprocess --once --allow-real-invoker --llm-preset claude
```

`--llm-command` y `runtime.llm_cli_presets` son configuracion local, no secretos. Las credenciales
del CLI las aporta el entorno del adoptante y nunca se commitean. El runtime aplica claim, guardrails,
tool-policy, budget/deadline, validacion de turn report, gate y 1 commit por turno antes de mutar
estado. Esto no habilita autonomia multi-turno: para mas detalle operativo, ver
[`runtime/README.md`](runtime/README.md).

### Autonomia supervisada

El runtime tambien incluye un sobre de supervision opt-in para corridas multi-turno acotadas. Nace
apagado en `runtime.supervised_autonomy` y requiere un registro local de activacion, caps validos y
el flag `--allow-supervised-autonomy`. El sobre documentado cubre `max_turns`, el centinela
`runtime/state/PAUSE`, `wall_clock_ms`, checkpoint humano por K turnos o fix-cycles, y el reporte
`*.runreport.md`.

La guia operativa esta en
[`Area_comun/protocol/SUPERVISED_AUTONOMY.md`](Area_comun/protocol/SUPERVISED_AUTONOMY.md). Esto no
habilita el invoker real multi-turno: SA.4 sigue gateado por GO del operador y rollback ensayado.

### Runtime N-agente

La operacion N-agente se documenta en
[`Area_comun/protocol/N_AGENT_RUNTIME.md`](Area_comun/protocol/N_AGENT_RUNTIME.md): registry de
agentes/capacidades, routing, estados Review/QA, seguridad, handoffs, observabilidad y presupuesto.

### Runtime escritor autoritativo

El modo escritor autoritativo es una capacidad runtime-tier opt-in. Nace apagado: una instancia no
lo activa solo por tener `runtime/` presente ni por generar un genesis. Para activarlo deben estar
en `true` `event_state.enabled`, `event_state.materialize`, `event_state.enforce` y
`event_state.authoritative`, con `adoption_tier: "runtime"`, y debe existir aprobacion local del
operador.

La migracion asistida escribe un snapshot canonico en
`runtime/state/snapshots/<hash>.json` y emite un evento `protocol.genesis` que guarda solo
`snapshot_ref = {hash, commit, actor, timestamp, schema_version}`. El snapshot queda fuera del
prompt y el replay lo hidrata solo cuando necesita materializar o verificar estado; si el archivo
falta o el hash no coincide, el runtime bloquea de forma segura.

`runtime/state/` queda committable: no se gitignora de forma general porque en modo autoritativo
contiene event log y snapshots fuente de verdad de la instancia. El scan de neutralidad lo exime por
ser estado generado; la fuente bajo `runtime/**` sigue cubierta.

Con el modo autoritativo activo, las transiciones de `Area_comun/state/*.json` se hacen como
intents al runtime. Una edicion manual genera drift y el hard-gate de `event_state.enforce` la
rechaza. La reversa operativa es apagar `event_state.enforce` y `event_state.authoritative` (y, si
se desea, `materialize`); eso devuelve la instancia al flujo manual sin borrar el snapshot de corte.

## 2. Validar la instancia generada

Valida la nueva instancia desde la raiz de este repo:

```powershell
python scripts\validate_collaboration_state.py --root D:\Agentes\mi_nuevo_proyecto
```

Tambien puedes usar el validador PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root D:\Agentes\mi_nuevo_proyecto
```

Para comprobar que no quedan placeholders sin resolver:

```powershell
rg "\{\{[A-Z0-9_]+\}\}" D:\Agentes\mi_nuevo_proyecto
```

## 3. Arrancar un proyecto con SDD

SDD es opcional y esta apagado por defecto. Para iniciar una instancia con SDD activado:

1. Crea la instancia con el script o de forma manual.
2. Activa el bloque `sdd` en `protocol.config.json`:

```json
{
  "sdd": {
    "enabled": true,
    "enforcement": "new_implementable_tasks",
    "adopted_at": "2026-06-05"
  }
}
```

3. Crea una spec en `Area_comun/specs/` usando `Area_comun/specs/SPEC_TEMPLATE.md`.
4. Declara la tarea implementable con estos seis campos:
   - `spec_id`
   - `execution_pipeline`
   - `acceptance_criteria`
   - `linked_decisions`
   - `test_plan`
   - `closure_criteria`
5. Verifica que `spec_id` apunta a un archivo existente dentro de la instancia.
6. Ejecuta ambos validadores antes del handoff.

Ejemplo minimo de tarea implementable con SDD:

```yaml
---
id: TASK-0001
owner: Codex
status: ready
type: implementation
spec_id: Area_comun/specs/SPEC-0001-example.md
execution_pipeline: [Create artifact, Run validator]
acceptance_criteria: [Artifact exists, Validator passes]
linked_decisions: [DECISION-0001]
test_plan: [python validator, powershell validator]
closure_criteria: [Handoff created, Review requested]
---
```

Para tareas de `discovery`, `analysis`, `review`, `documentation` o `triage`, usa los cuatro
campos minimos: `objective`, `expected_output`, `question_to_resolve` y `closure_criterion`.

La instancia `examples/minimal_sdd_instance/` muestra el caso minimo completo: `sdd.enabled:true`,
una spec resoluble y una tarea `implementation` conforme a SDD.

## 4. Crear un proyecto nuevo manualmente

1. Copia el contenido de `protocol_template/` a la raiz del nuevo repo.
2. Copia estos archivos master para crear los archivos vivos de la instancia:
   - `AGENTS.template.md` -> `AGENTS.md`
   - `protocol.config.template.json` -> `protocol.config.json`
   - `Area_comun/README.template.md` -> `Area_comun/README.md`
   - `Area_comun/state/PROJECT_STATE.template.json` -> `Area_comun/state/PROJECT_STATE.json`
   - `Area_comun/state/TASK_INDEX.template.json` -> `Area_comun/state/TASK_INDEX.json`
   - `Area_comun/state/CLAIMS.template.json` -> `Area_comun/state/CLAIMS.json`
3. Rellena todos los placeholders `{{...}}`.
4. Declara las fronteras duras del proyecto en `{{DOMAIN_CRITICAL_BOUNDARIES}}`.
5. Declara decisiones de stack en `{{STACK_DECISIONS}}`.
6. Declara puntos de aprobacion humana en `{{HUMAN_APPROVAL_POINTS}}`.
7. Ajusta `protocol.config.json` con `project_name`, `agent_roles`, `quality_gates` y
   `state_invariants`.
8. Declara `protocol_version` (placeholder `{{PROTOCOL_VERSION}}`) con la version del protocolo
   que sigue la instancia (p.ej. `0.1.0`); ver `CHANGELOG.md` y
   `Area_comun/decisions/DECISION-0001-versionado.md`.
9. Si vas a publicar un paquete verificable, sigue
   `Area_comun/protocol/RELEASE_ENGINEERING.md`: genera manifiesto/provenance, verifica integridad y firma con
   material del emisor fuera del repo. Si usas `external-command`, publica en el reporte de release la identidad,
   issuer y comando exacto de verificacion.

## 5. Archivos a completar primero

1. `AGENTS.md`: contrato superior del proyecto.
2. `Area_comun/state/PROJECT_STATE.json`: fase inicial, objetivo, agentes, decisiones y riesgos.
3. `protocol.config.json`: parametros que usa el validador.
4. `Area_comun/state/TASK_INDEX.json`: backlog inicial.
5. `Area_comun/tasks/TASK-0001-*.md`: primera tarea ejecutable.

## 6. Generar backlog inicial

1. Crea tareas pequenas, verificables y con un solo owner.
2. Cada tarea debe tener objetivo, entradas, archivos relevantes, entregables, DoD, riesgos y
   preguntas abiertas.
3. Registra cada tarea en `Area_comun/state/TASK_INDEX.json`.
4. Si una tarea depende de una decision, enlaza `Area_comun/decisions/DECISION-XXXX-*.md`.
5. Si hay una ambiguedad bloqueante, usa status `blocked` y una pregunta concreta.

## 7. Reclamar tareas

1. Lee `AGENTS.md`, `Area_comun/README.md`, `TASK_PROTOCOL.md`, `PROJECT_STATE.json`,
   `TASK_INDEX.json`, `CLAIMS.json`, `mailbox/open/` y el archivo de tarea.
2. Verifica que la tarea esta `ready` y que no existe claim activo de otro owner sobre sus rutas.
3. Actualiza el archivo de tarea y `TASK_INDEX.json` a `claimed` o `in_progress`.
4. Crea o actualiza una entrada en `Area_comun/state/CLAIMS.json` con scope explicito.
5. Al cerrar, libera el claim con `status: released`.

## 8. Cerrar una fase

1. Todas las tareas de salida de fase deben estar `done` o tener bloqueo aceptado.
2. Debe existir handoff autocontenido para lo que otro agente deba revisar.
3. Debe existir reporte humano en `Area_comun/reports/`.
4. `PROJECT_STATE.json` debe reflejar fase, riesgos, preguntas y proximas acciones.
5. Ejecuta el validador. Variante recomendada:

```powershell
powershell -NoProfile -File scripts\validate_collaboration_state.ps1
```

Si tu entorno local requiere una anulacion temporal de politica de ejecucion, tambien puede
funcionar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1
```

## 8.1 Activar el hook de validacion local

Cada clon debe cablear una vez el hook versionado (Git no versiona la configuracion
local):

```powershell
git config core.hooksPath .githooks
```

Compruebalo con `git config core.hooksPath`; debe devolver `.githooks`. El
`pre-commit` es la primera linea rapida: para todo commit ejecuta sobre el arbol
actual los chequeos baratos `prune_state.py --check` y drift de la guia cuando
corresponde, sin materializar el snapshot staged. El validador completo y la garantia
de juicio sobre los bytes staged quedan reservados en local para un gate explicito:

```powershell
$env:HOOK_FULL = "1"; git commit
# Alternativa persistente por clon:
git config hook.full true
```

Quita la variable o usa `git config --unset hook.full` para volver al modo acotado.
El modo completo conserva la mecanica de materializacion y juicio sobre los bytes
staged. Antes de `push`, ejecuta voluntariamente un commit/gate con modo completo.
El reparto acepta el riesgo de un HEAD local transitoriamente rojo para mantener
barato el ciclo de todos los commits; el gate completo pre-push y la validacion
desde clon limpio en CI lo mitigan. CI sigue siendo el enforcement duro y conserva
la validacion completa, ademas de verificar la existencia y SHA-256 del hook.

Desarme reversible en menos de 30 segundos si el hook bloquea al equipo:

```powershell
git config --unset core.hooksPath
```

Para rearmarlo, ejecuta de nuevo `git config core.hooksPath .githooks`. El desarme
local no debilita el enforcement duro de CI.

## 9. Validar una instancia minima de ejemplo

Desde la raiz de esta plantilla:

```powershell
powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
```

Para validar el ejemplo con SDD activado:

```powershell
python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_sdd_instance
```

## 10. Convencion de archivos template

Los archivos con sufijo `.template.*` son los unicos masters para contenido que se rellena por
proyecto. Para un proyecto NUEVO, los canonicos sin sufijo (`AGENTS.md`, `protocol.config.json`,
`PROJECT_STATE.json`, etc.) se crean en la instancia, no se mantienen como copia duplicada de la
plantilla.

**Excepcion — dogfooding de este repo:** `multi_agent_project_protocol` aplica su propio
protocolo a su desarrollo, por lo que aqui SI conviven los `.template.*` (masters publicados) con
los canonicos vivos (la instancia de este repo) y `examples/minimal_instance/` (instancia de
ejemplo). No es drift: cada par tiene un proposito distinto (master publicado vs estado vivo).

## 11. Guia humana operativa

La **guia humana operativa** es el contrato minimo de documentacion para personas (y agentes nuevos):
un solo documento que explica que es la instancia, que hace, como se construye/ejecuta/prueba/despliega/
opera, como se diagnostica, donde estan las rutas del protocolo, que roles/capacidades hay y como retomar
el contexto. Tiene 21 secciones fijas (ver `Area_comun/protocol/HUMAN_GUIDE.template.md` y SPEC-0072).

- **Fuente de verdad = el `.md`.** El HTML es un **artefacto generado** y **nunca se edita a mano** (lleva
  un banner "GENERADO - NO EDITAR").
- **Donde:** la plantilla master neutral esta en `Area_comun/protocol/HUMAN_GUIDE.template.md`; la guia
  llena de tu instancia va en la **raiz** (`HUMAN_GUIDE.md` + `HUMAN_GUIDE.html`, junto a `AGENTS.md`);
  hay un ejemplo en `examples/human_guide_instance/`.
- **Cuando completarla:** al instanciar, y como parte del DoD de cada release o cambio de
  arquitectura/roles/tier (manten la seccion 21 "Historial de cambios" al dia).
- **Como generar el HTML:**

  ```text
  python scripts/generate_human_guide.py --in HUMAN_GUIDE.md --out HUMAN_GUIDE.html
  ```

- **Tier-awareness:** las secciones solo-runtime se marcan "no aplica" automaticamente en instancias
  `coordination`.
- **Validacion/drift:** `python scripts/generate_human_guide.py --in HUMAN_GUIDE.md --check` regenera en
  memoria y compara byte a byte (falla si el HTML fue tocado a mano o si falta una seccion obligatoria o
  queda un placeholder `<...>` en una guia viva). Ese `--check` corre en CI y en el git hook local.
- **Neutralidad:** los `*.template.*` son masters neutrales de dominio (sin negocio/stack/nombres de
  agente); las versiones llenas de la instancia estan exentas del escaneo de neutralidad.
