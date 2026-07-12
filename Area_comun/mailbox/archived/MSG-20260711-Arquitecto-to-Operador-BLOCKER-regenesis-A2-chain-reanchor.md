---
message_id: MSG-20260711-Arquitecto-to-Operador-BLOCKER-regenesis-A2-chain-reanchor
from: Arquitecto
to: Operador
type: ACTION
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-GO-regenesis-A2-julian-y-speckit-contabilidad.md
  - Area_comun/artifacts/PREP-CONTABILIDAD-esqueleto-spec-patron.md
one_line_summary: "Orden 1 (re-genesis A2) BLOCKED: el procedimiento del runbook (agregar pubkey al config + regenesis.py) NO produce estado valido -- cambiar el config rompe el chain.genesis del eventlog y regenesis.py NO re-ancla la cadena (no hay herramienta). Reverti Aegis a limpio (validate 0, b22e49bc, config intacto), sin commitear nada roto. Opciones A1 (Julian bajo Codex via override, desbloquea YA) / B (tarea Codex: sello+regenesis-boundary para A2 nominal limpia). Recomiendo A1 ahora + encolar B. Orden 2 (kit SPEC-CONT) en curso como PREP, independiente."
requested_action: "Elige Orden 1: A1 ahora (Julian opera bajo Codex via override runtime en su maquina, sin tocar config/genesis -> desbloquea el onboarding + gate 2-clones hoy; coste: atribucion a Codex, no nominal) + encolar B (Codex construye el re-anclaje de cadena: sellar seq 672..N como el pre_t0 seal + chain.genesis nuevo atado al config con jheredia:v1) para la A2 nominal limpia antes de que la atribucion sea study-relevant; O esperar B sin A1 (Julian en hold). Orden 2 (kit SPEC-CONT PREP) la sigo en paralelo."
question: "Orden 1: A1-ahora + encolar-B (recomendado), o esperar-B-sin-A1? Orden 2 la sigo como PREP independientemente."
---

# BLOCKER - re-genesis A2 no ejecutable con el tooling actual + Orden 2 en curso

Respondo a tu ACTION (GO re-genesis A2 + kit SPEC-CONT). NO abri el build. Fondo intocable intacto.

## Orden 1 (re-genesis A2 de Aegis): BLOCKED -- hallazgo tecnico verificado
Ejecute el procedimiento A2 del runbook (s.8.4): agregue tu pubkey `jheredia:v1` a
`event_state.signature_config.public_keys` del config de AEGIS (raw 32B `7p0Hgpg9c1rBeddhj3MG8TGS6jrol5byaoYPDW4joaY=`,
extraida del PEM SPKI, prefijo ed25519 verificado) + alta en `agent_registry` (id `jheredia`, implementer) +
corri `runtime/regenesis.py` (drift 0, firma `arquitecto:v1` ed25519 + HMAC OK). PERO `validate` FALLA:
**"Runtime event log chain invalid: genesis mismatch"**.

CAUSA RAIZ (leida en el codigo, no inferida):
- El genesis de la CADENA de eventos (`chain.genesis`, seq 672) tiene
  `prev_hash = compute_genesis_prev_hash(config) = canonical_hash(protocol.config.json)` -- hash del config ENTERO
  (`runtime/eventlog.py:185/861`, check en `runtime/protocol_replay.py:171`).
- CUALQUIER cambio al config (incluida una pubkey nueva) cambia ese hash -> el `prev_hash` del `chain.genesis` ya
  no cuadra Y la cascada de `prev_hash` de TODOS los eventos (que encadena desde ese hash) se rompe.
- `runtime/regenesis.py` escribe el genesis del aggregate `protocol-state` (drift 0) pero NO toca el
  `chain.genesis` del eventlog ni re-encadena la cascada. NO existe herramienta de re-anclaje de cadena en el repo
  (busque reanchor/rechain/reseal: nada).
- Es EXACTAMENTE el "flag-en-config rompia la cadena" que el equipo documento en seq-2175 y esquivo moviendo flags
  a overrides runtime. El runbook s.8.4 describe A2 como "pubkey + regenesis.py" pero eso NO da estado valido con
  el tooling actual -> el runbook sobre-declara la herramienta (a corregir).

ACCION TOMADA: reverti TODO en Aegis (config + events + snapshot + snapshot-ref nuevo). **Aegis limpio: validate 0,
HEAD `b22e49bc`, config sin tocar.** NO commitee ni pushee nada roto. NO re-firme historia atestada a mano (seria
forjar la cadena; fuera de linea y contra el modelo de integridad).

OPCIONES (tu decides -- es fork de identidad/atribucion, study-relevant):
- **A1 (desbloquea a Julian YA):** Julian opera bajo una identidad YA registrada (Codex) via override runtime en su
  maquina -- SIN cambio de config, SIN re-genesis. Es la Opcion A1 del propio runbook s.8.4. Desbloquea onboarding +
  gate 2-clones hoy. Coste: el journal atribuye su trabajo a "Codex" (pierdes atribucion nominal por-humano).
- **B (A2 limpia, requiere tooling):** tarea Codex -- sellar el segmento operativo actual (seq 672..N) como ya se
  hizo con el `pre_t0` seal (seq 1-671, ver `pre_t0_provenance` del config) y escribir un `chain.genesis` NUEVO en
  N+1 atado al config nuevo (con `jheredia:v1`) + soporte del validador para la frontera de epoca-de-config. El
  patron de sello YA existe (pre_t0); es el re-genesis mid-chain limpio. Trabajo de runtime real, no improvisado.
- **RECOMENDACION:** A1 AHORA (desbloquea a Julian + gate 2-clones) + encolar B (Codex) para la A2 nominal limpia
  ANTES de que la atribucion nominal sea study-relevant. El BUILD sigue gated (base promovida + Sprint 1
  post-30-jul) -> hay pista para hacer B bien.

Nota: el gate e2e de 2 clones REAL (s.5) igual necesita el clon de Julian operativo (su privada + los secretos HMAC
que TU distribuyes fuera de banda); yo solo hago el lado config + un gate de paridad de replay local. Aplica a A1 y A2.

## Orden 2 (kit SPEC-CONT de Contabilidad): EN CURSO (PREP, independiente del blocker)
Arranco la instanciacion del kit `SPEC-CONT-*` (slices R1-R8, formato NOVA-SPEC-T-001, patron congelado de
Presupuesto) desde el WS1 + SDD design-source. Escribir NO construir; sin promover tareas de build; sin activar
SESSION_CONTEXT desde la API; respeto la escotilla `SESSION_CONTEXT('accounting_annual_close')` tal como quedo y
horneo el follow-up `source_module_code='accounting'` como hardening DECLARADO (no bypass). Te reporto la colocacion
gobernada (frontera hub `Area_comun/specs/nova/` vs ledger de instancia) y entrego por slice.

Fondo intocable intacto (2E35F26E, 1.14.0, N=500). A tus ordenes.
