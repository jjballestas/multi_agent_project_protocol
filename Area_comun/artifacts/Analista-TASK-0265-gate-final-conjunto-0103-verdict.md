# ANALISTA -- TASK-0265 GATE FINAL: revision adversarial del conjunto DECISION-0103

Voz: Analista (checker independiente, proveedor diverso -- DECISION-0101). Firma: Analista.
Fecha: 2026-07-23. Rol: checker-only (DECISION-0099); no implemento, no ratifico, no cierro.

## Veredicto de cabecera

**OK-CLOSABLE** para el conjunto DECISION-0103 (unidades 0257..0264 + 0266 + 0286).
Las 6 pruebas adversariales pasan POR COMPORTAMIENTO en clon limpio de HEAD, la coherencia
cross-unit esta confirmada, y los 4 gates de protocolo estan verdes. Se declara **1 hallazgo
WARNING-real (F1)** en el hook de modo-completo (territorio E6 / TASK-0268-0269, FUERA de las
unidades de este gate): **no bloquea el batch** (falla en cerrado, CI y modo-por-defecto
intactos, la intencion de seguridad de C5 se cumple/sobre-cumple), y se rutea como follow-up.

Este veredicto NO ratifica por si mismo. Ratificacion y flips de cierre siguen el flujo normal
(Arquitecto ratifica; el done-flip de 0265 y cualquier remediacion los ejecuta el flujo del
maker).

## Ancla canonica (no working tree caliente)

- Repo bajo revision: multi_agent_project_protocol (hub / dataset atestado).
- HEAD = origin/main = `cd2ca575d5116ec0d6b77afe1c6cc5403ad37b6a`.
- Metodo: clon limpio a `C:/ccv0265`, `git checkout cd2ca57`, gates y pruebas corridas ALLI,
  gateadas por EXIT CODE. Payloads adversariales propios (no confie en nombres de test).

## Gates de protocolo (clon limpio, exit code)

| gate | comando | exit |
|---|---|---|
| estado colaborativo | `python scripts/validate_collaboration_state.py` | 0 (OK) |
| encoding ASCII | `python scripts/scan_encoding.py` | 0 (OK) |
| neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | 0 (OK) |
| drift #4 | `python runtime/protocol_replay.py --check-drift` | 0 (CLEAN, up_to_seq=6137) |

## Suites del maker (baseline, re-corridas por mi; exit 0 todas)

- 0258 schema: `run_runtime_turn_schema_cases.py` -> 8 casos OK.
- 0259 semantica/friccion: `run_runtime_turn_semantic_cases.py` (5 OK) +
  `run_runtime_turn_obstacle_cases.py` (mutation-proved OK).
- 0286 post-gate: `run_post_gate_obstacle_cases.py` OK; `check_falsification_contracts.py` +
  `test_falsification_contracts.py` OK.
- 0266 instanciacion: `run_runtime_instantiation_cases.py` (8 + ps1 parity) OK.
- 0257/E6 hook: `test_precommit_hook.py` OK (bounded <2s; full-mode, concurrency, R100,
  rejection, cleanup).

## Harness adversarial propio (34 checks, 0 SLIP)

Extraje los guardas y los ejercite con payloads propios contra el clon limpio. Diferencial
(mismo reporte, obstacles poblado vs vacio) donde aplica.

### Pruebas mandatorias, vector por vector

| # | prueba adversarial | unidad | entrypoint ejercido | resultado |
|---|---|---|---|---|
| a | commit con estado gobernado ROJO rechazado en modo enforcing (HOOK_FULL=1) | 0257 (hook) | `.githooks/pre-commit` real (git staged) | **PASS** |
| b | turno runtime con friccion autoritativa + obstacles vacio -> rechazado | 0259 | `turn_validate.validate_delivery_obstacles`/`friction_sensors` | **PASS** |
| c | REPORTE con friction_count>0 + obstacles vacio -> rechazado | 0261 | `validate_collaboration_state.validate_governed_mailbox_report` | **PASS** |
| d | historico de mailbox sigue VERDE (grandfathering) | 0261 | validate clon limpio (REPORTEs 2026-07-18 presentes) | **PASS** |
| e | oferta RECHAZADA no se re-oferta | 0263 | `improvement_offers.evaluate` | **PASS** |
| f | gate_green:false + obstacles vacio POST-gate -> rechazado por el entrypoint real | 0286 | `RunLog.append` -> `validate_post_gate_obstacles` (orchestrator.py:1136) | **PASS** |

Detalle por vector (evidencia, no nombres de test):

- **(a)** Inyecte en CLAIMS.json un claim con `status: bogus_status` (un archivo que el
  trailer-checker NO lee). Working-tree validate -> exit 1 con
  `Claim CLAIM-ADV-RED has invalid status 'bogus_status'`. Con el hook:
  - modo DEFAULT (partial): `sh .githooks/pre-commit` -> **exit 0** (solo AVISA, prune due);
    confirma E6-A (HEAD-rojo transitorio local aceptado, CI es el enforcement).
  - modo ENFORCING (`HOOK_FULL=1`): -> **exit 1**,
    `collaboration state in staged snapshot is invalid; commit rejected`, con el error del
    CLAIM entre los reportados por `validate_collaboration_state` (NO un crash del
    trailer-checker; el pre-commit no invoca trailers). El rechazo del estado gobernado rojo
    en modo enforcing esta probado.
- **(b)** Para cada senal autoritativa in-schema con obstacles=[] Y con la clave ausente:
  `task_status.to in {blocked, qa_failed, changes_requested, architect_review}`,
  `review_qa.event in {reject_review, fail_qa, assign_fix}`, y `checks_failed` no vacio ->
  todos producen `semantic: objective friction (...) requires non-empty obstacles`.
  Diferencial: el MISMO reporte con obstacles poblado NO produce el error de friccion. Turno
  de entrega (`to in {in_review, done}`) sin la clave obstacles -> rechazado por la regla de
  entrega. Coherente con E7: gate_green NO es campo legal del turn_schema
  (`additionalProperties:false`), asi que a validate-time la friccion exigible es solo la
  auto-declarable autoritativa. NO se usa `outcome` (auto-relabel-able).
- **(c)** friction_count>0 + obstacles [] -> `declares friction_count > 0 but obstacles is
  empty`. friction_count=0 + [] -> pasa (no-friccion legitima). friction_count no-entero ->
  rechazado. Obstaculo malformado (campos parciales) -> `invalid obstacles`. Obstaculo bien
  formado + friccion -> pasa.
- **(d)** El validate del clon limpio esta VERDE con REPORTEs pre-adopcion (2026-07-18)
  presentes en el arbol. Mi harness confirma: ancla-fecha pre-adopcion -> saltado; ancla-fecha
  >= 2026-07-22 -> exigido. Grandfathering intacto.
- **(e)** Oferta rechazada en el registro: misma evidencia -> NO se re-oferta; evidencia
  cambiada pero NO declarada -> NO se re-oferta; evidencia cambiada Y declarada
  (`--new-evidence`) -> se re-oferta (intencionado). Oferta aceptada -> nunca se re-oferta.
  Oferta pendiente misma evidencia -> no se duplica.
- **(f)** `RunLog.append` (el entrypoint REAL que usa el orchestrator en la etapa apply,
  orchestrator.py:1136, con `gate_green=result.get("green")` -- un bool genuino) llama
  `validate_post_gate_obstacles` incondicionalmente: gate_green False + obstacles [] o ausente
  -> `ValueError: ... gate_green:false requires non-empty obstacles`. gate_green False +
  poblado -> aceptado. gate_green True sin obstacles -> aceptado (narracion-free). El unico
  escritor del run-log es `RunLog.append` (no hay bypass de escritura directa del jsonl en el
  codigo enviado). El mutante (quitar la llamada) es cazado por la suite del maker.

### Coherencia cross-unit (confirmada)

- **C3 runtime = 0259 (pre-gate) + 0286 (post-gate)**, repartido en las dos capas correctas
  (E7). 0259 cubre la friccion auto-declarable autoritativa (declaracion==efecto, no gameable)
  en `turn_validate` (pre-gate); 0286 cubre el gate-red OBJETIVO donde `gate_green` existe (el
  run-log, post-gate). gate_green no es siquiera campo legal del turn_schema
  (`additionalProperties:false`), lo que confirma que el split de capa de E7 es correcto y no
  redundante. Cada mitad enforcea en su entrypoint real.
- **Bloque obstacles compartido 0258 <-> 0261 <-> 0262**: los campos del item en
  `runtime/turn_schema.json` == `OBSTACLE_FIELDS` del validador de mailbox ==
  {what, root_cause, resolution, recurrence_risk}; enum recurrence_risk {low, medium, high}
  con paridad schema<->mailbox; la plantilla `MAILBOX_REPORT_TEMPLATES.md` usa la MISMA forma
  y lo declara explicito ("do not rename, add, or omit fields").
- **0260 gate mecanico <-> 0264 regla escrita**: 0260 provee el gate de aprobacion de turno 0
  (`plan_approval_error`, approval_hash sobre campos MATERIALES id/acceptance/risk contra un
  evento firmado `plan.approved`, cableado en orchestrator.py:824); 0264 escribe la regla de
  arranque ("nunca ejecutar sin plan aprobado") en TASK_PROTOCOL.md Y AGENTS.template.md.
  Gate y regla son consistentes.

## Residuales honestos declarados (no bloquean)

- **R-b1 (revert proxy best-effort):** `friction_sensors` solo caza "revert/reverted/rollback"
  en `actions[].summary`. Wording evasivo ("backed out", "rolled back") NO se caza. Es un
  proxy DECLARADO en el codigo (comentario turn_validate.py) y en el contrato de falsacion
  NEG-TURN-REVERT-PROXY-OBSTACLES. Honesto, no oculto. La friccion autoritativa (transiciones)
  no depende de este proxy.
- **R-b2 (sin sensor de outcome):** un turno que NO es de entrega y NO declara transicion
  autoritativa no fuerza obstacles aunque el outcome sugiera friccion. Es por diseno (E7: no se
  usa `outcome`, que es auto-declarado y relabel-able). presencia-vs-veracidad: el validador
  fuerza que el bloque EXISTA cuando hay senal objetiva; no puede saber si un agente que peleo
  en silencio lo reporto.
- **R-c1 (grandfathering por ancla):** un REPORTE que omite date, created_at Y
  report_schema_version se trata como historico (adopted=False) y salta el chequeo de
  obstacles. Es la regla de compatibilidad DECLARADA explicitamente en
  `MAILBOX_REPORT_TEMPLATES.md` (lineas 10-12: "Every new REPORTE MUST declare at least one
  adoption anchor ... Without any anchor, the compatibility rule treats the message as
  historical"). Uso normal (copiar la plantilla) siempre trae report_schema_version -> exigido.
  Evadir requiere violar la regla escrita. WARNING-theoretical, no bloquea.
- **R-f1 (identidad `is False`):** `validate_post_gate_obstacles` usa `gate_green is False`; un
  `gate_green` entero 0 lo saltaria. NO alcanzable por el entrypoint real (el orchestrator pasa
  un bool genuino desde `run_gate`). WARNING-theoretical, no bloquea.
- **Alcance NO re-ejecutado en esta pasada combinada:** 0260 (--plan-all / gate de turno 0) y
  0264 (regla escrita) los confirme ESTRUCTURALMENTE aqui (presencia + cableado) y por su GO
  individual previo; no re-corri su acceptance completa end-to-end en este barrido (cada uno
  porta su propio gate previo). Declarado.

## Hallazgo WARNING-real (F1) -- NO bloquea el batch, se rutea como follow-up

**F1: el inventario del snapshot parcial del hook de modo-completo omite deliverables de tarea
fuera de sus raices -> el modo completo local (HOOK_FULL=1) rechaza en FALSO un arbol limpio.**

- Clase (DEFECT_TAXONOMY): WARNING-real (el uso normal lo dispara: cualquiera que siga la
  recomendacion E6-A "correr el gate completo antes de push" lo pega de inmediato). Falla en
  CERRADO (sobre-rechaza; nunca sub-acepta).
- Ubicacion: `.githooks/pre-commit` (lineas 63-77, `snapshot_inventory`) vs
  `scripts/validate_collaboration_state.py:1049-1054` (chequeo de existencia de deliverables).
- Repro (clon limpio en HEAD, arbol prin-tino):
  - `python scripts/validate_collaboration_state.py` -> **exit 0**, 0 errores de deliverable.
  - stage un cambio inocuo; `HOOK_FULL=1 sh .githooks/pre-commit` -> **exit 1**:
    `Task TASK-0037 deliverable missing: HUMAN_GUIDE.md`,
    `Task TASK-0084 deliverable missing: personal/Codex/STARTUP_PROMPT.md`,
    `collaboration state in staged snapshot is invalid; commit rejected`.
  - Ambos archivos EXISTEN en el arbol (git ls-files): es un FALSO positivo.
- Causa raiz: el inventario materializa `Area_comun runtime scripts profiles examples` + una
  lista de archivos raiz, pero NO el `HUMAN_GUIDE.md` de raiz ni `personal/**`. Los deliverables
  de tarea (TASK_INDEX/archives, campo `deliverables`) pueden apuntar fuera del inventario; el
  inventario se derivo de imports/data, no del read-set de existencia-de-deliverables. Cota
  exacta: 2 deliverables fuera de inventario (TASK-0037 -> HUMAN_GUIDE.md;
  TASK-0084 -> personal/Codex/STARTUP_PROMPT.md), ambos en TASK_INDEX_ARCHIVE.json, ambos
  existentes.
- Por que NO bloquea el conjunto 0103:
  1. Cae en el codigo E6 (TASK-0268/0269), FUERA de las unidades de este gate (0257..0264 +
     0266 + 0286); no rompe el acceptance de ninguna unidad in-scope.
  2. Falla en CERRADO: sobre-rechaza. La intencion de seguridad de C5 ("nunca se commitea
     estado roto") se cumple/sobre-cumple; ningun estado rojo pasa por el modo completo.
  3. El modo por DEFECTO (partial/avisa) no corre validate -> intacto.
  4. El enforcement DURO (CI) es independiente: `.github/workflows/validate.yml:29` corre
     `validate_collaboration_state.py --root .` sobre el arbol COMPLETO (actions/checkout, no
     el snapshot del hook) y pinea el hook por SHA-256. CI ve HUMAN_GUIDE.md y personal/ ->
     verde correcto. El falso positivo solo afecta la bandera VOLUNTARIA local HOOK_FULL=1.
- Nota de coherencia con la DECISION: la resolucion E6-A afirma "Paridad partial-vs-total
  verificada intacta ... inventario cerrado contra el read-set real". Mi prueba de
  comportamiento FALSA esa afirmacion para el read-set de existencia-de-deliverables. Es una
  incoherencia del texto E6-A + una regresion de usabilidad de la bandera voluntaria, no un
  hueco de integridad.
- Remediacion sugerida (para el maker, no la aplico): anadir al inventario del snapshot las
  rutas de deliverables que viven fuera de las raices (p.ej. `HUMAN_GUIDE.md` y `personal/`),
  o acotar el chequeo de existencia-de-deliverables a las rutas dentro del inventario cuando se
  corre sobre el snapshot parcial. Gate afectado: `test_precommit_hook.py` (anadir un caso que
  pruebe que el modo completo sobre arbol limpio da exit 0). Como 0268/0269 ya estan DONE y
  fuera de este batch, sugiero abrirlo como remediacion/tarea nueva, no como fix-loop de 0265.

## Recomendacion de cierre

- **0257..0264 + 0266 + 0286: OK-CLOSABLE.** Todas las garantias in-scope aguantan bajo
  comportamiento adversarial; los 6 vectores pasan; coherencia cross-unit confirmada; gates
  verdes.
- **F1: WARNING-real, follow-up.** Rutear como remediacion separada del hook de modo-completo
  (territorio 0268/0269); NO bloquea el cierre del conjunto 0103.

-- Analista
