# ANALISTA - VOZ EXTERNA ADVERSARIAL - carga por archivo v2 FASE B (TASK-0151 / DECISION-0056 / AC43)

> Voz: Analista (escepticismo externo: intento REFUTAR el gate humano de PII + bounding de candidatas).
> Firma: Analista. Fecha: 2026-06-22. Lente: seguridad / honestidad / neutralidad / metodologia.
> ANCLADO EN CANONICO: clon limpio Zeus-protocol `0a5e737` (tree limpio); protocolo HEAD `28e1add`.
> Verifique el CODIGO y CORRI `npm test` YO MISMO (3 corridas). NO promovi, NO mute estado, NO encendi
> nada vivo. La Fase C (agente extractor = ventana de modelo real) NO es esta fase.

## VEREDICTO: OK -> CERRABLE la Fase B (los 6 vectores PASAN por comportamiento).
## 1 ANOMALIA (DECISION-0018, AJENA a la Fase B): scan_encoding ROJO por el MENSAJE del Arquitecto (no su codigo).

## Reproduccion (gate por exit code; corrida por mi)
- Zeus clon @ 0a5e737: `npm test` -> **43/43**, ESTABLE (3 corridas 43/0, sin flake).
- Protocolo: `validate` exit 0 CON y SIN secretos; drift `has_drift=False`; `scan_domain_neutrality` exit 0.
  El core runtime NO cambio (grep `candidate` en submit_intent.py = 0). #4 epoca 1.14.0 byte-identica
  (el test asserta protocol.config.json byte-identico antes/despues).

---

## 1) AC43 GATE HUMANO DE PII -> PASA (intente forjar; rechazado)
- `buildCandidateRequirementIntake`: `if (candidate.piiReviewed !== true) -> 409 "candidate approval requires
  human PII review acknowledgement"`. Probado: aprobar con `piiReviewed:false` -> **409** `/PII review/`.
- Defensa adicional: provenance check (`sourceFileSha256/extractionTaskId/preEditHash` deben casar el stored
  -> 409 "candidate provenance mismatch"); candidate no-pending/approved -> 409; id invalido -> 400
  (`^CAND-[A-F0-9]{10,64}$`); hashes de provenance deben ser sha256. No se puede aprobar una candidata sin
  declarar la revision humana de PII, ni forjar una candidata sin provenance valido.

## 2) RE-SCREEN candidate->intake (texto EDITADO) -> PASA
- El texto editado por el operador pasa por los MISMOS guards al aprobar: `sanitizeRequirementIntake`
  (redactPublicText + ascii) + `screenPiiBestEffort(title+narrative+acceptanceIntent)`. Probado:
  - editar `narrative:"<script>alert(1)</script>"` + piiReviewed:true -> **400** `/active content/` (contenido
    activo rechazado en el editado, no solo en el ingest).
  - candidata con `NIT 900.123.456` y `SELECT * FROM dbo.saldos` en la narrativa editada -> el task ATERRIZADO
    tiene `[NIT-REDACTED]/[SQL-REF-REDACTED]` y NO contiene `900.123.456|dbo.saldos|SELECT`. El contenido nuevo
    que NO paso el screening de ingest SE re-valida al aprobar.

## 3) id del CONTENIDO EDITADO (no del archivo) -> PASA (sin colision)
- `editedFingerprint = sha256(["candidate-approved", title, narrative, acceptanceIntent, project])` -> el id se
  deriva del CONTENIDO EDITADO, no del archivo. Probado: 3 candidatas del MISMO upload aprobadas ->
  `new Set(requirementIds).size === 3` (3 REQ con ids DISTINTOS); las 3 en TASK_INDEX type=requirement
  status=proposed con `source_provenance.source_file_sha256/extraction_task_id`. Re-aprobar la misma candidata
  -> idempotente (1 sola task; el candidato queda status "approved" con `approved_requirement_id`).

## 4) CANDIDATAS FUERA DEL LEDGER -> PASA
- Store en `FILE_CANDIDATE_STORE_ROOT||tmpdir()/zeus-protocol-file-candidates` (os-tmp). Probado:
  `candidateStoreRoot.startsWith(protocolRoot) === false`; `git ls-files os-tmp/zeus-protocol-file-candidates`
  = VACIO; ANTES de aprobar, NINGUNA candidata en TASK_INDEX (`status/type === "candidate"` = false; el id
  seed no aparece); `protocolFixtureHasNoDrift === true` (drift 0 con candidatas presentes). Tras aprobar,
  NUNCA hay `candidate` en el ledger; `validate` exit 0; config byte-identica. `/discard` -> 200 (status
  "discarded"), no toca el ledger. Las candidatas NO se atestan en #4 sin aprobacion humana.

## 5) CARRY AC40 NO-MODELO-EGRESS -> PASA
- La Fase B NO reintrodujo egress: grep de `fetch/openai/anthropic/generative/socket/WebSocket/import()` en
  server.js (excluyendo 127.0.0.1) = VACIO. Los endpoints de candidatas (`/intake-candidates` GET,
  `/discard` POST) leen/escriben el store os-tmp local, sin red saliente. El agente extractor (la ventana de
  modelo real) es Fase C, NO B.

## 6) #4 BYTE-IDENTICA + GATES -> PASA
- protocol.config.json byte-identico antes/despues (test). validate exit 0 CON y SIN secretos; drift 0;
  neutralidad exit 0. core runtime sin cambio (sin `candidate`, sin nuevo kind). npm 43/43 estable x3.

---

## ANOMALIA (DECISION-0018) - AJENA a la Fase B, pero deja el CANAL ROJO
`scan_encoding.py` -> **exit 1**: `non_ascii_channel` en
`Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0151-faseB.md:33` (byte 0xc2 =
`invertido/acento`). El propio mensaje del Arquitecto que me instruye la pasada VIOLA el canal ASCII
(DECISION-0012). NO es el deliverable de la Fase B (el codigo/tests Zeus estan limpios), pero deja el gate
de canal ROJO -> bloquearia un commit limpio del cierre. Lo NOTIFICO al Arquitecto (no lo arreglo: ruta de
otro dueno). Precondicion para un commit verde del cierre: ASCII-fix de su mensaje (guion normal, sin signos
invertidos/acentos).

## Observacion menor
Protocolo HEAD `28e1add` != origin `8a4d208` (1 commit local sin pushear: el handoff de TASK-0151). El
Arquitecto dijo "HEAD pusheado"; esta 1 adelante. Zeus `0a5e737` != origin `2f760a6` (esperado in_review).

## RECOMENDACION DE CIERRE: OK, CERRABLE la FASE B (en sus meritos).
Los 6 vectores de gate-PII/bounding/egress/no-ledger PASAN por comportamiento. La unica accion pendiente es
de HIGIENE DE CANAL: ASCII-fix del mensaje del Arquitecto (DECISION-0018) para que el commit del cierre quede
verde. Eso NO es un defecto del deliverable de la Fase B. Fase C (agente extractor + AC45 guard-a-todo-src +
purga/TTL) sigue pendiente; nada vivo.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre, no arregle el mensaje del Arquitecto (ruta ajena),
  no encendi nada vivo. Ancle en canonico (0a5e737 / 28e1add). Suite/escritura real en clones temporales; no
  toque el ledger vivo. Scratch limpiado.
