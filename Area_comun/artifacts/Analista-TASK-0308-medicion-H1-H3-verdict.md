# VERDICT -- TASK-0308 -- Medicion pre-registrada H1-H3 sobre el corpus sellado N=500

- Reviewer (checker): **Analista** (voz adversarial independiente; maker != checker)
- Maker: Arquitecto
- Task: TASK-0308 (status in_review)
- Fecha/hora: 2026-08-02 (UTC+2, local)
- Instruccion: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0308.md
- **Recomendacion de cierre: OK-CLOSABLE**

## 0. Ancla canonica (no arbol caliente)

- Corpus (fondo intocable) = tag **TFM-dataset-N500** = commit `e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9`.
- Entregable revisado (informe + datos crudos + drivers) = HEAD `67942f218772d18af22bb3d94d0bb06bcf32c80c`.
- Verificacion en **CLON LIMPIO** bajo `D:/Aegis_Scratch/mapp/ccv0308` (checkout del tag), no in-place.
- Recomputo independiente: no confie el conteo del maker; corri mis propios payloads contra el pipeline #4.

## 1. Gates de protocolo (exit code)

| Gate | Donde | Exit |
|------|-------|------|
| validate_collaboration_state.py | clon del tag e3646ae | **0** |
| validate_collaboration_state.py | HEAD 67942f2 | **0** |
| scan_encoding.py | HEAD | **0** |
| scan_domain_neutrality.py | HEAD | **0** |
| drift (protocol_state_drift) | clon del tag | **has_drift = False** |

## 2. FASE 0 -- Sello recomputado independientemente (clon del tag)

| Item | Pre-registro / maker | Recomputo Analista | Veredicto |
|------|----------------------|--------------------|-----------|
| Elegibles (seq>=2221 AND intent.applied AND actor_auth.method==ed25519) | 500 | **500** | PASA |
| Desglose por agente | Arq 253 / Codex 195 / Analista 52 | **253 / 195 / 52** | PASA |
| Ventana de seq | 2221..2720 | **2221..2720** | PASA |
| intent.applied no firmados en ventana | 0 | **0** | PASA |
| chain.anchor en el corpus | 0 | **0** | PASA |
| config sha256 (fondo intocable) | 2e35f26e...b354 | **2e35f26e...b354** | PASA |
| epoch protocol_version | 1.14.0 | **1.14.0** | PASA |
| Pin 1 runtime/eventlog.py | 59a8ae87...dedd | byte-identico | PASA |
| Pin 2 scripts/validate_collaboration_state.py | eb04799f...c5ab | byte-identico | PASA |
| Pin 3 protocol.config.json | 2e35f26e...b354 | byte-identico | PASA |
| Pin 5 PRE-REGISTRO-H1-H3-v2.md | e8277cc7...5e6d | byte-identico | PASA |
| Pin 4 event-state.runtime.json | b9706842...11cf | gitignored (ver R1) | RESIDUAL declarado |

Fondo intocable **no modificado**: config, epoch, N=500 y ventana de seq coinciden byte a byte.

## 3. H1 -- Deteccion, FPR, salud (recomputo por comportamiento)

Inyeccion **programatica y reproducible** (harness `fase1_attacks.py`, sin juicio de agente).
Reproduje arm1 exacto (7 vectores, 25/25 c/u) y ademas ejercite la familia completa (cola, interior,
re-encadenado, alteracion en la punta).

| Vector | Clase | Interior | Cola/punta | Veredicto s.5 (=100%/vector) |
|--------|-------|----------|------------|------------------------------|
| Alteracion de payload | A1 | DETECTADO | DETECTADO (hash mismatch en la punta) | PASA (100%) |
| Insercion de evento | A1 | DETECTADO | -- | PASA (100%) |
| Reordenamiento | A1 | DETECTADO | -- | PASA (100%) |
| **Borrado de evento** | A1 | DETECTADO (gap de seq, 6/6 posiciones) | **ACEPTADO -- EVASION** (borrar ult. 1/2/5 y el ult. elegible seq 2720) | **REFUTADA (segun enunciado)** |
| Atribucion cruzada | A2 | DETECTADO (keyid_mismatch) | -- | PASA (100%) |
| Keyid no registrado | A2 | DETECTADO | -- | PASA (100%) |
| Firma Ed25519 invalida | A2 | DETECTADO | -- | PASA (100%) |
| Rollback de ancla | A3 | 0 anclas -- no ejercitable; sintetico rechazado | -- | N/A (ventana declarada) |

**Caza de escape (intento de romper la garantia mas alla de lo declarado):**
- Re-encadenado (borrar interior + renumerar seq downstream + recomputar prev_hash): **DETECTADO**
  -> `A2:seq2471:invalid_signature`. El escape esta CERRADO porque `actor_auth_signable_event`
  **conserva `seq`**: renumerar rompe la firma Ed25519 (que no se puede re-firmar sin la privada);
  no renumerar deja gap. Cualquiera de las dos ramas se detecta.
- Alteracion de payload en la punta: **DETECTADO** (`corruption at seq 2720: hash mismatch`), via el
  prev_hash propio del evento. La punta solo es vulnerable a **truncamiento puro**, no a manipulacion.
- Conclusion: la unica evasion es el truncamiento de cola; es la limitacion A3 "cabeza no anclada"
  (0 anclas, sin head-pin) declarada en el pre-registro s.8. **No hay escape nuevo no declarado.**

**FPR / AC2:** baseline (corpus intacto) ACEPTADO -> **FPR = 0/500 = 0%**; verify_actor_auth por camino
publico -> **500/500 validos = AC2 100%** (>= 99%). PASA.

## 4. H2 -- Sobrecoste acotado

| Metrica | Umbral s.5 | Observado | Veredicto |
|---------|-----------|-----------|-----------|
| Almacenamiento | <= 4 KB/ev | campos #4 ~408 B/ev crudos; delta medido +359..+387 B/ev | **CONFIRMADA** |
| Tokens | <= 5% | ~0%; `events.jsonl` NO esta en `token_cost.coldstart_globs` (verificado) | **CONFIRMADA** |
| Latencia (Delta end-to-end submit_intent, literal) | mediana <=50 ms; p95 <=200 ms | 364..722 / 663..1252 ms; crece O(n) | **REFUTADA (segun enunciado)** |
| Latencia (coste marginal cripto de #4) | <= 50 ms | 0.03..0.07 ms/ev | PASA (lectura no-literal) |

El etiquetado contra la metrica **literal** (camino submit_intent end-to-end) es REFUTADA -- direccion
**conservadora** (etiqueta FALLO contra el umbral, sin lavar a PASA). La causa raiz O(n) (re-verificacion
del log entero por submit del core sellado; fijada post-sello por DECISION-0105, no retro-aplicable por
audit-first) es estructural y consistente con el propio validate observado (>2 min sobre este corpus).
No re-corri el benchmark wall-clock: es sensible al entorno y el veredicto ya es un FALLO conservador,
no un PASA que hubiese que defender.

## 5. H3 -- Verificabilidad independiente (clon limpio, solo publicas)

- Sin secretos en el clon (no existe `secrets/` ni `event-state.runtime.json`); config solo con 3
  claves publicas, sin privadas.
- **500/500** eventos verifican por camino publico (acuerdo 100%).
- `protocol_state_drift`: **has_drift = False** (hash materializado == replay firmado).
- `scripts/validate_collaboration_state.py`: exit **0** (gate real).
- Confirmado: `runtime/protocol_replay.py` en el tag **no tiene bloque `__main__`** (0 hits) ->
  `--check-drift` es un no-op y su exit 0 es **VACUO**; NO cuenta como verificacion externa. El informe
  lo declara y cita el gate real. **CONFIRMADA.**

## 6. Respuestas a las cuatro preguntas del operador

1. Veredicto mecanico contra s.5 correcto y **sin maquillaje**: **SI**. El informe etiqueta contra el
   umbral literal, refuta H1-estricto y H2-latencia y confirma el resto; mi recomputo coincide en todo conteo.
2. Inyeccion **programatica/reproducible** (no juicio de agente): **SI**. Harness determinista reproducido.
3. Conteos de ambos brazos **cuadran**: **SI**, reconciliados. La diferencia arm1 100% vs arm2 96.67%
   en borrado-de-evento es exactamente el hallazgo del diff-entre-brazos (arm1 apunto a interiores;
   arm2 incluyo la punta); reproduje AMBOS resultados y el truncamiento de cola de forma independiente.
4. **Fondo intocable no modificado**: **SI** (config 2e35f26e byte-identico, epoch 1.14.0, N=500, ventana 2221..2720).

## 7. Residuales declarados (no bloquean el cierre)

- **R1 (Pin 4 gitignored):** `event-state.runtime.json` no esta en el clon limpio (contiene rutas de
  claves PRIVADAS del camino de firma). El camino de **verificacion** (checker/H3) solo usa publicas,
  asi que su ausencia no afecta al veredicto; solo impide reconfirmar su sha256 desde clon limpio.
- **R2 (arm1 crudo optimista):** `CONSOLIDATED_arm1.json` conserva event-deletion `tpr=1.0`,
  `all_100pct=true`, `evasions=[]` (dato PRE-reconciliacion, solo interiores). El `RECONCILE` y el
  informe lo **corrigen** a 96.67% / cola-evade y documentan el `arm1_original_miss`. Es transparente,
  no maquillaje. Sugerencia (no bloqueante): una nota de una linea en arm1.json apuntando al RECONCILE
  para que un lector que cite arm1 en aislamiento no se confunda.
- **R3 (H2 latencia wall-clock):** magnitudes absolutas sensibles al entorno; no re-ejecutadas. El
  crecimiento O(n) es estructural y confirmado por codigo/observacion.
- **R4 (A3 no ejercitable):** 0 anclas en el corpus; solo rollback sintetico rechazado (declarado).

## 8. Cierre

Todos los gates verdes por exit code; sello, conteos y fondo intocable recomputados independientemente
y coincidentes; H1/H2/H3 verificados por comportamiento; la unica evasion (truncamiento de cola) es la
limitacion A3 declarada y no encontre ningun escape nuevo; el etiquetado es conservador y honesto.

**RECOMENDACION: OK-CLOSABLE.** No hay fix loop pendiente. Ratificacion del operador a discrecion.

-- Analista
