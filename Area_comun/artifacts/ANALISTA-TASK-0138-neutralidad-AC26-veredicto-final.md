# ANALISTA - VOZ EXTERNA ADVERSARIAL (FINAL) - fix de neutralidad TASK-0138 (DECISION-0053 / AC26)

> Voz: Analista (escepticismo externo: intento REFUTAR que (a) el core volvio neutral y (b) el bounding
> sigue intacto). Firma: Analista. Fecha: 2026-06-20. Lente: seguridad / honestidad / neutralidad / metodologia.
> ANCLADO EN CANONICO: protocolo HEAD==origin `8317878`; codigo front en clon limpio Zeus-protocol `7619fd2`
> (arbol limpio). Verifique leyendo el CODIGO y corriendo scan/golden/suite YO MISMO; no asumi al Arquitecto.
> NO promuevo, NO autoro SPEC, NO muto estado. ANTES de cerrar TASK-0138.

## VEREDICTO: CERRABLE. No pude refutar ni (a) ni (b).
Mi CAMBIO previo (#4 neutralidad) y su corolario (#5 honestidad) estan RESUELTOS; el RIESGO previo (#2,
regex con `:`) tambien. El bounding anti-impersonacion (AC25) y la idempotencia (AC24) NO regresionaron.

## Reproduccion (gate por exit code)
- `grep '"Operador"|"Arquitecto"' runtime/submit_intent.py` -> **0**.
- Scan adversarial (inyecte el literal): scan **exit 1** y lo flagueo. Repo limpio: scan **exit 0**.
- Zeus clon @ 7619fd2: `npm test` -> **26/26 PASS**.
- Protocolo: `validate` exit 0 CON secretos y exit 0 SIN secretos (clon git, secrets/ gitignored); drift
  `has_drift=False`; neutralidad exit 0.

---

## 1) NEUTRALIDAD (mi CAMBIO previo) -> PASA
- `grep -nE '"Operador"|"Arquitecto"' runtime/submit_intent.py` = **0** (antes 2). El core no contiene
  literales de identidad de agente.
- **Caller-derived:** el normalize del kind admite ahora `{message_id, author, relayed_by, endorsement,
  idempotency_key}` y `mailbox_archive_accountability(payload)` toma `author`/`relayed_by` con
  **`require_text`** (OBLIGATORIOS del caller; sin default a "Operador"/"Arquitecto"). Los literales
  "Operador"/"Arquitecto" viven ahora en el SERVER de Zeus (`buildMailboxArchiveIntents`, commit 7619fd2)
  = el PRODUCTO/instancia, NO el core neutral. Es la separacion correcta (DECISION-0049/0050: codigo de
  producto en Zeus; core neutral en el protocolo). Mismo patron que el intake (atribucion del caller).
- **#5 CERRADO:** como el core EXIGE `author` del caller (no default), un `mailbox_archive` directo
  (no-via-front) NO queda auto-mis-atribuido a "Operador": el caller debe proveer su propia atribucion. El
  core ya no estampa un origen que no verifica; registra lo que el caller declara (como `task_upsert`).

## 2) SCAN REGRESION-PROOF -> PASA (probado empiricamente, no cosmetico)
- **Prueba adversarial directa:** copie `runtime/submit_intent.py`, le inyecte `LEAK = "Operador"`, corri
  `scan_domain_neutrality` -> **exit 1**, reportando `runtime/submit_intent.py: operador`. El scan ATRAPA
  de verdad un literal de identidad re-introducido en el core.
- Como funciona (verificado en `scripts/scan_domain_neutrality.py`): deriva los terminos de identidad del
  `config` (agent_registry) y escanea `runtime/*.py`; `submit_intent.py` **NO** esta en
  `LEGACY_IDENTITY_LITERAL_FILES` (la whitelist) -> queda vigilado. Fixtures golden:
  `examples/neutrality_scan_cases/{clean, domain_term_in_core, identity_literal_in_core,
  runtime_source_still_scanned, runtime_state_exempt}` -> cubre clean-pasa + identity-literal-falla +
  runtime-still-scanned. En limpio el scan pasa (exit 0). **Regresion-proof: re-colar el literal en el core
  ya no es silencioso.**
- **NOTA honesta (no bloqueante):** `LEGACY_IDENTITY_LITERAL_FILES` whitelista los leaks PRE-EXISTENTES
  (apply.py "Codex", context.py implementer->Codex, etc.). Eso convierte esa deuda de neutralidad en
  EXPLICITA y declarada (una whitelist nombrada y versionada), no silenciosa -- el manejo honesto. Queda
  como follow-up opcional encoger la whitelist; no afecta el cierre de TASK-0138 (submit_intent.py SI quedo
  limpio y vigilado).

## 3) BOUNDING INTACTO (no regresiono AC25/AC24) -> PASA
- `EXECUTABLE_ACTIONS = new Set(["requirement-intake","mailbox-archive"])` (sin cambio) + 403 fuera del set.
- `payload.actorId` -> 400; `payload.intents` -> 400 (rechazo crudo intacto); builder SERVER-SIDE
  (`buildMailboxArchiveIntents`), array fijo. El fix de neutralidad solo movio la FUENTE de la atribucion
  (del core al server), NO abrio la superficie.
- AC24 idempotente intacto: el test asserta `deduped:true` en re-archive (no doble-evento); side-effect
  `shutil.move` guardado por existencia (no-op si ya archivado); reversible.
- `npm test` 26/26 (incl. no-bypass, impersonacion forjada->400, traversal->400, archive write real). No
  pude forjar otro intent como Arquitecto via mailbox-archive.

## 4) GATES -> PASA
- **regex acotada:** `MAILBOX_MESSAGE_ID_RE = ^MSG-[A-Za-z0-9._-]+$` (sin `:` `@` `{` `}` `~` `^`) -> sin
  NTFS ADS; ademas `mailbox_message_id` sigue rechazando `/ \ ..` (el `.` simple es seguro, `..` bloqueado).
  Mi RIESGO previo (#2) RESUELTO.
- **#4 byte-identica:** el test asserta `protocol.config.json` / `chain_manifest.json` /
  `secrets/eventauth-arquitecto.key` byte-identicos antes/despues (no solo drift 0).
- **validate con/sin secretos exit 0** (verificado: D: con secretos y clon git sin secrets/); **drift 0**;
  **npm test verde** (26/26); neutralidad/encoding exit 0.

---

## RESUMEN
| # | Veredicto | Evidencia |
|---|-----------|-----------|
| 1 NEUTRALIDAD | PASA | grep core=0; atribucion caller-derived (require_text); literales movidos al producto Zeus; #5 cerrado |
| 2 SCAN | PASA | inyeccion adversarial -> scan exit 1 lo atrapa; submit_intent.py vigilado; fixture existe; deuda legacy declarada (whitelist) |
| 3 BOUNDING | PASA | EXECUTABLE_ACTIONS=2 + 403; actorId/intents->400; builder server-side; idempotente deduped; npm 26/26 |
| 4 GATES | PASA | regex [A-Za-z0-9._-]; #4 byte-identica; validate con/sin secretos exit 0; drift 0; npm verde |

## RECOMENDACION: **CERRABLE.**
Ambos ejes que pediste refutar resisten: (a) el core volvio neutral (grep 0 + caller-derived + scan que lo
prueba), (b) el bounding sigue intacto (AC25/AC24 sin regresion). Mi CAMBIO #4 esta resuelto y, mejor aun,
hecho regresion-proof por un scan REAL. Unica nota (no bloqueante): la whitelist legacy es deuda de
neutralidad declarada (honesta) con follow-up opcional. El cierre formal (checker) y la decision son del
Arquitecto + operador.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre la tarea. Ancle en canonico (8317878 / 7619fd2). El
  scan adversarial corrio sobre una COPIA temporal; el archive real solo en golden/clon del propio test. No
  toque el ledger vivo. Scratch limpiado.
