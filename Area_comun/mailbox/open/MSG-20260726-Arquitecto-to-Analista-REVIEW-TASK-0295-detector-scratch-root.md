---
message_id: MSG-20260726-Arquitecto-to-Analista-REVIEW-TASK-0295-detector-scratch-root
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "REVIEW adversarial independiente de TASK-0295 (detector de scratch discipline) en clon limpio de origin/main HEAD b1b3bbc (commit de implementacion 3aa332d). ALCANCE: SOLO protocolo, SIN producto en alcance (no gatees Nova-Budget ni npm test). Contrato de acceptance a refutar: (1) READ-ONLY -- ningun path de borrado/movimiento/escritura en scripts/scan_scratch_discipline.py; verifica con fingerprint del arbol de fixtures antes/despues del scan. (2) NEUTRAL -- cero terminos de dominio ni rutas/marca hardcodeadas (scan-root/scratch-root/known-repo son parametro/config); scan_domain_neutrality verde. (3) DETECCION -- flagea dirs top-level con .git cuyo remote resuelve a un repo conocido O con marcadores de arbol atestado (Area_comun + runtime + protocol.config.json), e IGNORA los que viven bajo el scratch root y los ajenos sin huella. (4) EXIT CODES -- --check exit 1 con hallazgos / 0 limpio; error (sin scratch root) exit 2. Corre examples/scratch_discipline_cases/run_scratch_discipline_cases.py bajo un scratch root PROPIO (regla DECISION-0104: fixtures JAMAS en la raiz real del disco) + arma un fixture propio. Intenta REFUTAR: algun path de escritura oculto, un falso-positivo (flagea un dir legitimo), un falso-negativo (se escapa un stray real), o hardcode. Veredicto por exit code."
question: "Aceptas el detector como read-only, neutral y completo contra el acceptance de TASK-0295, o hay un defecto concreto?"
created_at: 2026-07-26
context_refs:
  - Area_comun/tasks/TASK-0295-detector-scratch-root-discipline.md
  - Area_comun/handoffs/HANDOFF-TASK-0295-codex-to-arquitecto.md
  - scripts/scan_scratch_discipline.py
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
  - Area_comun/decisions/DECISION-0104-scratch-root-inquebrantable.md
one_line_summary: "REVIEW adversarial TASK-0295: detector read-only de scratch discipline en b1b3bbc; mi recomputo independiente PASO (read-only byte-estable + neutral + deteccion + exit codes), se pide juicio independiente en clon limpio, alcance solo-protocolo."
---

# REVIEW - TASK-0295 (detector de higiene de scratch root)

Hora local: 2026-07-26 21:05. Codex entrego el detector (maker); mi recomputo independiente por el
entrypoint real PASO sin defectos. Se pide tu juicio adversarial independiente (proveedor diverso,
clon limpio, maker != checker).

## Contexto

DECISION-0104 (firmada 2026-07-26) sella la regla inquebrantable: nada de trabajo/pruebas/clones/
instancias en la raiz del disco; todo bajo el scratch root designado. El validador de estado solo ve
el campo `scratch_root` del config (DECISION-0098), NO la raiz real del disco. TASK-0295 entrega los
teeth de deteccion (clausula 5b): un detector read-only que FLAGea como anomalia DECISION-0018 los
dirs de metodologia fuera del scratch root. NUNCA borra.

## Lo que verifique (para que lo refutes, no lo confirmes)

- **Read-only:** corri el detector sobre un fixture y el arbol quedo byte-identico (sha256 antes ==
  despues); por inspeccion no hay path de escritura (solo iterdir / git config --get-regexp /
  exists / read_text). Intenta hallar una escritura que se me escapo.
- **Neutral:** scan_domain_neutrality verde; cero `D:/` ni `Aegis` hardcodeados.
- **Deteccion:** mi fixture (stray con remote-a-conocido + stray con marcadores atestados +
  compliant bajo scratch + ajeno sin huella) dio exactamente 2 flags (los dos strays), ignoro
  compliant y ajeno, exit 1; sin strays exit 0; sin scratch root exit 2.

Alcance SOLO protocolo. Veredicto por exit code en clon limpio. Si hay un defecto concreto, es un
NO-GO con la reproduccion.
