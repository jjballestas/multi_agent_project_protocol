# ANALISTA - TASK-0258 obstacles[] en turn_schema - veredicto adversarial

- Firma: Analista (voz adversarial independiente, checker-only)
- Fecha/hora local: 2026-07-20 08:12 (UTC+2)
- Instruccion canonica: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0258-obstacles-schema.md
  (recibida en working tree al inicio de la pasada; commiteada en canonico durante la pasada,
  en 6950a48).
- Alcance declarado: SOLO hub, SIN PRODUCTO EN ALCANCE (no se ejecuta ningun repo de producto).

## VEREDICTO DE CABECERA

**CAMBIO-REQUERIDO / NO CERRABLE AUN, con remediacion docs-only barata.** El contenido
tecnico de TASK-0258 es solido: los 5 puntos del acceptance PASAN por comportamiento (36/36
probes propias + 3 probes end-to-end, cero escapes). Bloquea el cierre UN hallazgo:

- **F-0258-01 (WARNING-real, docs-only):** `Area_comun/protocol/SCHEMA_VERSIONING.md` -- el
  doc-contrato de TASK-0053 que el acceptance punto 2 invoca -- quedo desactualizado: linea 9
  dice `Current version: 1.2.0` mientras el schema canonico declara `1.3.0`, y falta la
  seccion de justificacion del bump que el propio doc mantiene para cada MINOR previo
  (Capa A -> 1.1.0; Fase 5.2 -> 1.2.0). Uso normal del doc (consultar la version vigente del
  contrato) devuelve informacion falsa. Precedente aplicado: TASK-0268 H1 (contradiccion
  doc-realidad = bloqueante docs-only).

Anomalia observada y RESUELTA durante la pasada (registro DECISION-0018, ya no bloquea):

- **A-0258-02:** al ancla inicial de esta revision (origin/main = 9ce238b) el canonico estaba
  ROJO en clon limpio: drift B.3 en CLAIMS.slim.json, PROJECT_STATE.slim.json y
  TASK_INDEX.slim.json, causado por una divergencia de push ajena a 0258 (el commit local
  aa98267 llevaba la rematerializacion de slims; el 9ce238b publicado no). El Arquitecto
  reconcilio durante mi pasada (a6e540f) y el nuevo origin/main (feb43c0) valida VERDE en
  clon limpio (verificado abajo). Queda registrado porque cualquier cierre intentado en esa
  ventana habria nacido sobre HEAD rojo.

## ANCLA CANONICA

- Ancla funcional de la revision: origin/main `9ce238b409dad2d4ef691fef660f34c57412456c`.
- HEAD avanzo durante la pasada a `feb43c003a7c0d3a1b61aeab60a9c644d3312049` (reconciliacion
  de slims + coordinacion). INVARIANCIA verificada: `git diff 9ce238b feb43c0` sobre
  `runtime/turn_schema.json`, `examples/runtime_turn_cases/`,
  `Area_comun/protocol/SCHEMA_VERSIONING.md` y el .md de la task = DIFF VACIO. Todo lo
  funcional revisado vale identico para feb43c0; los gates de canonico se re-corrieron en
  feb43c0.
- Implementacion: `9be450d` (feat: schema + 3 fixtures + runner) ; entrega: `34d5dff`.
- Clon limpio: `/d/ccv0258` (9ce238b, luego re-gateado en feb43c0); clon de contraste
  pre-0258: `/d/ccv0258p` (dab0fa6 / 34d5dff / 060d676).
- Task: `Area_comun/tasks/TASK-0258-d0103-c3-turn-schema-obstacles.md` (in_review, claim
  liberado).
- Producto: NOT_RUN por instruccion canonica (SIN PRODUCTO EN ALCANCE).

## REPRODUCCION (todo en clon limpio, gateado por exit code)

```
python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py    -> EXIT 0 (8/8)
python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py  -> EXIT 0 (5/5)
probe propia probe_0258.py (36 payloads, familia completa)             -> EXIT 0 (36 PASS, 0 SLIP)
probe e2e turn_validate.validate_turn (3 casos con obstacles)          -> EXIT 0 (3/3)
22 suites adicionales que consumen turn_schema                         -> EXIT 0 todas
4 suites rojas preexistentes (ver residual R3)                         -> EXIT 1 invariante pre/post
validate clon limpio 9ce238b (ancla inicial, sin secretos)             -> EXIT 1 (drift B.3 slims; transitorio A-0258-02)
validate clon limpio feb43c0 (HEAD actual, sin secretos)               -> EXIT 0
python scripts/validate_collaboration_state.py (vivo, con secretos)    -> EXIT 0
python scripts/scan_domain_neutrality.py (clon feb43c0)                -> EXIT 0
python scripts/scan_encoding.py (clon feb43c0 y vivo)                  -> EXIT 0
sha256 protocol.config.json (vivo, clon 9ce238b y clon feb43c0)        -> 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 (byte-identica)
```

## TABLA VECTOR-POR-VECTOR (acceptance de 5 puntos)

| # | Vector del acceptance | Resultado | Evidencia falsable |
|---|----------------------|-----------|--------------------|
| 1 | Campo opcional `obstacles`, array de objetos, required `[what, root_cause, resolution, recurrence_risk]`, `recurrence_risk` enum `[low, medium, high]`, `additionalProperties false` en el item | **PASA** | 36/36 probes propias via el MISMO consumidor real (`jsonschema.Draft7Validator`, identico a `runtime/turn_validate.py:277`): 4 casos missing-required (I1-I4), item vacio (I5), propiedad extra rechazada (I6), familia enum completa incl. case-sensitivity, espacios, null, int (I7-I14), no-objeto como item (I21-I24), `obstacles` no-array (I25-I28), item mixto valido+malformado (I29). `obstacles` omitido sigue valido (V3): campo opcional real. Root `additionalProperties:false` intacto (I30). Sin escapes. |
| 2 | Version bumpeada segun contrato SemVer TASK-0053; aditivo = minor | **PASA el bump / CAMBIO-REQUERIDO el doc-contrato** | Bump `1.2.0 -> 1.3.0` correcto: campo opcional nuevo = MINOR segun `SCHEMA_VERSIONING.md` seccion Version Policy. PERO el doc-contrato quedo contradictorio (F-0258-01): `grep -n "Current version" Area_comun/protocol/SCHEMA_VERSIONING.md` -> linea 9 `1.2.0`; `runtime/turn_schema.json` -> `1.3.0`. Falta ademas la seccion de justificacion que el doc mantiene por cada bump (patron 1.1.0 y 1.2.0). Verificado invariante en feb43c0. |
| 3 | Suites del runtime que consumen el schema actualizadas y verdes | **PASA** | `run_runtime_turn_schema_cases.py` EXIT 0 (8 casos, 3 nuevos en EXPECTED); semantic EXIT 0 (5). Barrido propio de TODAS las suites cuyo runner referencia turn_schema: 22 adicionales EXIT 0. Las 4 rojas (instantiation, loop, protocol_materialize, supervised_autonomy) fallan IDENTICO en dab0fa6 (pre-0258): preexistentes, no regresion (residual R3). |
| 4 | Casos: poblado valido / lista vacia valida / item malformado invalido | **PASA** | Fixtures `valid_obstacles_populated.json`, `valid_obstacles_empty.json`, `invalid_obstacle_malformed.json` presentes y en EXPECTED. No confie en el nombre: probe e2e propia por `turn_validate.validate_turn` (camino completo schema+semantica): poblado valido -> 0 errores; malformado -> rechazado (`'resolution' is a required property`); vacio -> 0 errores. |
| 5 | El MISMO bloque (4 campos + enum) es la forma canonica que 0261/0262 replicaran; no se inventa variante | **PASA** | El bloque del schema coincide campo a campo y en orden con DECISION-0103 clausula 3 (`what / root_cause / resolution / recurrence_risk`, enum `low|medium|high`). TASK-0261 (ready) se ancla textualmente a "mismos 4 campos + enum que el turn_schema de TASK-0258". Sin variante. Ver residuales R1/R2 (minLength y espejo del example instance) para que la unicidad no se erosione en 0261/0262. |

## HALLAZGOS

- **F-0258-01 (WARNING-real, docs-only, bloqueante por precedente 0268-H1):**
  `SCHEMA_VERSIONING.md` linea 9 declara `Current version: 1.2.0` con el schema en `1.3.0` y
  sin seccion de justificacion del nuevo MINOR. Falsable: los dos grep/lecturas de la tabla,
  vector 2. Remediacion: 1 linea + seccion corta "DECISION-0103 C3 Justification" (patron del
  propio doc). No cambia schema ni suites.
- **A-0258-02 (anomalia DECISION-0018, ajena a la unidad, RESUELTA durante la pasada):**
  canonico ROJO en clon limpio de 9ce238b por drift B.3 de los 3 slims (evidencia:
  `git diff aa98267 9ce238b --stat` = exactamente esos 3 archivos; validate EXIT 1 en clon,
  EXIT 0 en vivo). Reconciliada por el Arquitecto en a6e540f; feb43c0 valida VERDE en clon
  limpio. Se registra para trazabilidad de la ventana.

## RESIDUALES DECLARADOS (no bloquean)

- **R1 (SUGGESTION):** el schema es MAS estricto que el acceptance literal: `minLength: 1` en
  `what/root_cause/resolution` (string vacio rechazado, probes I15-I17). Correcto en espiritu
  anti-teatro, pero 0261/0262 deben replicar TAMBIEN el minLength o los dos carriles divergen
  (mailbox aceptando strings vacios que el runtime rechaza).
- **R2 (WARNING-theoretical):** `examples/full_runtime_instance/runtime/turn_schema.json`
  sigue en `1.2.0` SIN obstacles; un reporte con obstacles es RECHAZADO alli por el
  `additionalProperties:false` de raiz. No muerde el camino normal (`new_instance.py` copia
  `runtime/` canonico, verificado en `copy_runtime_dir`), pero la referencia distribuida ya
  no refleja el contrato canonico. Recomendacion: propagar el bloque al example en la ventana
  0261/0262 o declararlo explicitamente pineado.
- **R3:** 4 suites rojas preexistentes en clon limpio Windows (runtime_instantiation,
  runtime_loop, runtime_protocol_materialize, supervised_autonomy), invariantes entre dab0fa6
  y 9ce238b; coincide con lo ya declarado en revisiones previas (0267). No son de 0258.
- **R4:** la instruccion REVIEW llego sin commitear y el arbol compartido estuvo en
  entrega-a-medias del peer durante la pasada (claim CLAIM-arq-hyg-0757-20260720 solo en
  arbol al inicio; commiteado luego en 6950a48). Se reviso igual porque los commits citados
  (9be450d/34d5dff) si eran canonicos desde el inicio.
- **R5:** el mismatch `TASK-0257 index=review_approved vs file=in_review` visible en
  34d5dff/9be450d era transitorio del cierre en cadena y ya no existe en HEAD.

## RECOMENDACION DE CIERRE

**CAMBIO-REQUERIDO.** Fix-loop esperado (iteracion 1/2, maximo 2 antes de escalar al
Operador):

1. Maker (Codex): actualizar `SCHEMA_VERSIONING.md` (Current version 1.3.0 + justificacion
   del MINOR por DECISION-0103 C3). Docs-only; schema, fixtures y suites NO cambian.
2. Re-juicio Analista (barato): lectura del doc remediado + `validate_collaboration_state.py`
   EXIT 0 en clon limpio del HEAD del fix + `scan_encoding` EXIT 0. Sin re-probes
   funcionales: los 5 vectores ya quedaron probados por comportamiento y no se tocan.

task_id: TASK-0258
status: in_review (veredicto Analista: CAMBIO-REQUERIDO, no cerrable aun)
executive_summary: Los 5 puntos del acceptance PASAN por comportamiento (36/36 probes + e2e, cero escapes; bump 1.2.0->1.3.0 MINOR correcto; forma canonica identica a DECISION-0103 c.3 y anclada por TASK-0261). Bloquea el cierre solo F-0258-01: SCHEMA_VERSIONING.md (doc-contrato de TASK-0053) contradice la version vigente (1.2.0 vs 1.3.0) y omite la justificacion del MINOR; remediacion docs-only. A-0258-02 (canonico rojo por drift de slims en 9ce238b) quedo RESUELTA durante la pasada (feb43c0 verde en clon limpio).
artifacts: Area_comun/artifacts/ANALISTA-TASK-0258-obstacles-schema-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0258-obstacles-CAMBIO-REQUERIDO.md
gates: turn schema cases EXIT 0 (8/8); semantic EXIT 0 (5/5); probes propias 36/36 + e2e 3/3; 22 suites consumidoras EXIT 0; 4 suites rojas preexistentes invariantes pre/post-0258; validate vivo con secretos EXIT 0; validate clon limpio feb43c0 sin secretos EXIT 0 (9ce238b fue EXIT 1 por drift transitorio A-0258-02); domain EXIT 0; encoding EXIT 0; config #4 byte-identica 2E35F26E...354 en vivo y ambos clones
next_recommended: Codex remedia SCHEMA_VERSIONING.md (docs-only: Current version 1.3.0 + seccion de justificacion DECISION-0103 C3) y el Arquitecto me pide re-juicio barato (lectura del doc + validate clon limpio verde + encoding); iteracion 1/2.
risks: cerrar sin remediar F-0258-01 consolida un doc-contrato que miente sobre la version vigente; example full_runtime_instance divergente del contrato (R2) puede inducir una instancia manual sin obstacles; minLength no replicado en carril sesion divergiria los carriles (R1).
