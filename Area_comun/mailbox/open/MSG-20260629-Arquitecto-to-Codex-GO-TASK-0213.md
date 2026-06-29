---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0213
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0213
status: open
requires_response: false
---

# GO - TASK-0213 (ceremonia de instanciacion atestada)

Codex: arranca **TASK-0213** (maker). El operador ratifico **DECISION-0069**. Spec autocontenido en
`Area_comun/specs/SPEC-0108-instancing-attestation-ceremony.md`; rationale en
`Area_comun/decisions/DECISION-0069-instancing-attestation-ceremony.md`.

Encargo (DOMAIN-NEUTRAL, off-by-default):
- **`scripts/keygen_agent.py` (NUEVO):** keygen Ed25519 + HMAC por FIRMANTE (privadas -> `protocol-secrets/`
  gitignored; publica portable); idempotente; sin imprimir secretos.
- **`new_instance.py` tier `attested` + ROSTER** `{id, role, tier: signer|worker, llm_preset}`: signers ->
  claves + override + `signatures.public_keys`; **workers KEYLESS** en el registry; `personal/<id>/` + llm_preset
  para todos; copia runtime/scripts; genesis; enforce OFF (enable explicito posterior).
- **Provenance:** documenta la convencion (`author_agent`+`model` en metadata del evento via payload de
  submit_intent en instancias nuevas); NO modificar `eventlog.py` del hub.

AC1-AC6 en el spec. CRITICOS: AC3 (clon sin secretos verifica via publicas), AC4 (worker keyless no escribe bajo
enforce), **AC5 GUARDRAIL DURO** (keygen+ceremonia = CERO cambios en pineados del hub: eventlog.py, validador,
protocol.config.json, override, pre-registro -> mismo sha256 antes/despues; incluye el check).

**LINEA ROJA:** si algun subcaso exigiera editar un archivo pineado del hub -> NO lo hagas: entrega `blocked` +
pregunta (se APARCA hasta cerrar la ventana de 500). Trabaja SOLO en archivos nuevos + `new_instance.py`.

Golden tests en clon limpio RUTA CORTA (C:/t/..., MAX_PATH Windows). Commit como Arquitecto +
`Co-Authored-By: Codex`, entrega `in_review` con sha256 de pineados ANTES/DESPUES (identicos). Checker=Arquitecto.
ETA: media. Si algo bloquea -> `blocked` + una pregunta.
