---
decision_id: DECISION-0106
title: Consola de prompt del operador desde el front = compose de un MSG gobernado operador->agente (superficie de escritura ACOTADA, anti-impersonacion, off-by-default)
status: accepted
ratified_at: 2026-08-02
date: 2026-08-02
deciders: [operador humano, Arquitecto]
amends: [DECISION-0051, DECISION-0052]
relates_to: [DECISION-0051, DECISION-0052, DECISION-0053, DECISION-0054, DECISION-0040, DECISION-0050, REQ-ZEUS-001]
supersedes: []
superseded_by: []
phase: P2
---

# DECISION-0106 - Consola de prompt operador->agente desde el front (Alcance A / P1 de TASK-0178)

> ACCEPTED por el operador (2026-08-02, ratificacion en sesion directa del Arquitecto). Gate de superficie de
> escritura (CLAUDE.md regla 2 / AGENTS.md s4). Codigo SOLO en Zeus-protocol (producto); core neutral. NO toca
> el config pinned (#4 epoca 1.14.0), ni INTENT_TYPES del runtime, ni genesis/keys.

## Contexto
TASK-0178 (consola del Arquitecto en el front), Alcance A. Hoy la superficie de escritura del front esta
ACOTADA al requirement-intake (DECISION-0051/0052) + mailbox-archive (DECISION-0053); cualquier otra forma
firmada por esta via se RECHAZA (anti-impersonacion, DECISION-0052). El operador necesita HABLARLE a los
agentes y ver respuestas SIN VS Code. El canal agente-agente YA existe y es gobernado/atestable: el mailbox
(MSG-*.md). Esta DECISION habilita EXPONERLO en la UI como una consola de prompt, sin inventar un canal nuevo.

## Decision
1. **Nueva forma de escritura ACOTADA (extiende 0051/0052):** un builder SERVER-SIDE con forma estricta para
   UN solo tipo de escritura -- el "operator-agent-message": el front compone un MSG-*.md canonico a
   `Area_comun/mailbox/open/` desde CAMPOS DE DATOS validados (destinatario + cuerpo), `from: Operador`,
   `to: <agente>`. El cliente NUNCA inyecta el MSG crudo ni el actor. Cualquier otra forma por esta via ->
   RECHAZADA (prueba negativa PERMANENTE, patron 0052).
2. **Es un MSG de mailbox gobernado, NO un segundo escritor de estado:** ASCII puro, PII redactada
   (estructural, guarda de 0040/0051), marcado `operator-directive`. NO es un intent del ledger (no toca
   `submit_intent`/estado); es un archivo de mailbox, el mismo canal que usan los agentes. `requires_response`
   segun el caso, con `response_owner` si aplica (mismas reglas de forma que valida `validate_collaboration_state`).
3. **Anti-bypass del gobierno:** un prompt libre NO hace que el agente destino se salte su flujo (SDD,
   maker!=checker, gates). El agente trata el `operator-directive` bajo SUS reglas de protocolo. La consola es
   una CARA de UI del mailbox, no una superficie de bypass del Analista ni del ciclo gobernado.
4. **Atribucion honesta (accountability, patron 0052):** `author: Operador`. Si el front commitea/persiste el
   MSG al canal gobernado (para que el agente lo procese, patron auto-commit-push de 0054), es
   `relayed_by: <firmante del front>` con `endorsement: none` (origen+transporte, NO aval). Un relayado NO
   cuenta como autorado por el firmante.
5. **Vista de hilo (lectura):** la consola LEE el mailbox (open + archived) filtrado por agente para mostrar el
   prompt del operador + las respuestas del agente. Lectura sobre el canal ya atestable; sin nueva superficie
   de escritura.
6. **Off-by-default, reversible por flag, FUERA del config pinned:** la capacidad nace deshabilitada; su flag
   vive en un registro FUERA de `protocol.config.json` (patron 0054/0055). #4 byte-identico; sin re-genesis.

## Guarda PII (innegociable, ESTRUCTURAL, hereda 0051/0040)
El cuerpo del prompt puede traer PII de terceros. Guarda estructural + advertencia (NO detector automatico):
(a) separar intencion-en-lenguaje-llano del payload sensible; (b) redactar/marcar el texto libre en todo
plano publicable; (c) canal ASCII a lo que se escribe al protocolo; (d) advertir al operador en compose y
confirm. NO levanta el gate DEF-PII (sigue proposed).

## Boundaries que esta DECISION NO mueve
- NO nuevo INTENT_TYPES del runtime; NO nuevo firmante; #4 epoca 1.14.0 PINNED byte-identica; core neutral.
- NO habilita lanzar/detener runtimes desde el front (eso es DECISION futura A / Alcance B, P2).
- NO es el supervisor front-server (P3 / Alcance C).
- NO da de alta agentes ni los enlaza a un LLM (P4 / roster RF-9).

## Descartes
- Canal de chat nuevo fuera del mailbox: NO -- rompe la atestabilidad; el mailbox ya es el canal gobernado.
- Cliente inyecta el MSG crudo: NO -- reabre el defecto de seguridad de 0052 (impersonacion).

## Implementacion
Via SDD: SPEC-0112 (autora el Arquitecto) + TASK-0310 (maker Codex, checker Analista+Arquitecto), off-by-default,
codigo solo en Zeus-protocol. Verificacion: builder server-side (forma estricta, prueba negativa de forma-ajena
RECHAZADA), ASCII/PII, `operator-directive`, atribucion honesta, off-by-default (flag fuera del config), vista de
hilo read-only, #4 byte-identico (drift 0 necesario no suficiente), core neutral, npm test producto exit 0.
