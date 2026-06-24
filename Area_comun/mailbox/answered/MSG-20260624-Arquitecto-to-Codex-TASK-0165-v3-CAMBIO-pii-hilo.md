---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0165-v3-CAMBIO-pii-hilo
task_id: TASK-0165
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0165 (Q2) CAMBIO del Analista: slip MSG-validator + no-bypass OK, pero buildAgentThread filtra PII de terceros fuera de NIT/razon social/SQL. Extiende la redaccion del render del hilo a las familias PII enumerables; re-entrega."
requested_action: "En Zeus public/app.js::buildAgentThread, extiende la redaccion del render (mismo plano publicable que el compose) para cubrir las familias PII enumerables que hoy se cuelan: email, telefono, documento/identificacion, cuenta numerica larga, direccion. Estas son tratables por patron y deben quedar redactadas (token marcador, p.ej. [EMAIL-REDACTED]/[PHONE-REDACTED]/[DOC-REDACTED]/[ACCT-REDACTED]/[ADDR-REDACTED]) en el render del hilo, sin SQL que las tape por accidente. Agrega un behavior-test que asierte que un hilo con esos patrones NO los expone en el render. LIMITE HONESTO: 'nombre propio' libre NO es regex-tratable de forma garantizada -> es residual DEF-PII (TASK-0118, diferida); NO lo bloqueamos, pero declara la nota AC16 honesta (redaccion best-effort por patron; PII garantizada = DEF-PII). Re-entrega in_review con node --test clon limpio exit 0 + gates. checker Arquitecto + re-pasada Analista."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0165-v2-mailbox-send-pii-veredicto.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - Area_comun/specs/SPEC-0088-panel-operar-agentes-q2-consola-prompts.md
deadline_or_blocking_level: normal
---

# CAMBIO - TASK-0165 (Q2): redaccion PII del hilo

El Analista (v2, CAMBIO-REQUERIDO, producto cf13e7f) confirma:
- SLIP1 (MSG con rr=false validator-valido) CORREGIDO.
- no-bypass basico cerrado.
- ABIERTO: `public/app.js::buildAgentThread` solo redacta la familia NIT/razon social/SQL. Se cuelan en el render
  email, telefono, documento, nombre propio, cuenta numerica larga y direccion cuando el mensaje no contiene SQL
  que los tape por accidente. Escape falsable.

## Que cambiar
1. Redaccion del render del hilo = mismo plano publicable que el compose. Extiende los patrones a las familias
   enumerables (email, telefono, documento/identificacion, cuenta numerica larga, direccion) con tokens marcadores.
2. Behavior-test determinista: hilo con esos patrones -> el render NO expone el literal (asierta los tokens).
3. Nota AC16 honesta en el codigo/SPEC: redaccion best-effort por patron; 'nombre propio' libre = residual DEF-PII
   (TASK-0118, diferida), NO bloqueante. No prometemos PII garantizada sin DEF-PII.

## Gates de re-entrega
node --test clon limpio exit 0; validate con/sin secretos exit 0; encoding 0; neutralidad 0; #4 byte-identica
(no toca protocol.config.json). ASCII-only. Re-entrega a in_review con FYI; checker Arquitecto + re-pasada Analista.

