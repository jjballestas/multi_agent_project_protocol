---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-B-done-spec-notion-lista
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-12
context_refs:
  - Area_comun/specs/SPEC-NOTION-PROJECTOR.md
  - D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-9303-chain-reanchor-config-epoch.md
  - personal/Arquitecto/A2-nominal-pubkeys.md
one_line_summary: "CIERRE: B (TASK-9303) DONE (mecanismo + 7a, gate adversarial Analista con fix-loop F-9303-01 pasado). SPEC-NOTION-PROJECTOR ESCRITA (tests del consenso + 2 workspaces via ledger + dimension de estudio). jball pubkey persistida para A2-nominal. Higiene completa (open/ 24->0 + poda). SIGUIENTE = A2-nominal (registro jheredia:v1+jball:v1 + gate 2-clones) + construir workspace Notion. ESCALO: fix durable del prompt de Codex (announces sin Task-Id, 3x hoy)."
requested_action: "Dos cosas pendientes de coordinacion tuya: (1) A2-NOMINAL de B (SEPARADO, ya sin codigo): decide cuando lo ejecutamos -- yo registro jheredia:v1 + jball:v1 en el config-epoch de Aegis (una re-genesis, pubkeys ya en mano) y Julian corre la e2e 7b + el gate 2-clones nominal en su maquina; (2) FIX DURABLE del prompt del cron de Codex: sus announces de coordinacion en el hub sobre tareas de Aegis deben emitir Task-Id: none Y Ops-Reason juntos (hoy solo Ops-Reason) -> me obligo a grandfather manual 2x hoy (f0411e7, bdfe2db). Ajustar su prompt cierra la friccion."
question: "Confirmas cuando ejecutamos el A2-nominal de B, y autorizas ajustar el prompt del cron de Codex para que emita Task-Id: none en los announces del hub? El workspace Notion lo construyes con tu agente y luego cablamos el proyector contra la SPEC."
---

# RESP - Cierre: B DONE + SPEC-NOTION-PROJECTOR lista + higiene completa

## 1. B (TASK-9303) = DONE
El mecanismo de re-anclaje de cadena esta cerrado y gateado adversarialmente:
- Codex construyo el mecanismo; el Analista lo gateo en clon limpio y **cazo un bug CRITICAL real (F-9303-01)**:
  `validate_chain` aceptaba tamper del sello de frontera (`sealed_segment.sha256`/`event_count`/`seq_range`,
  `boundary_id`, `old_config_hash`) -> el registro que declara que historia quedo sellada era modificable sin
  detectarse.
- Codex remedio (iteracion 1/2): `validate_chain` ahora falla cerrado si el evento boundary diverge de
  `config_epoch_history` y RECOMPUTA el sello contra las lineas reales 672..N. chain_cases 26/26.
- Analista re-juzgo: **OK/CERRABLE**. Ratifique in_review->review_approved; Codex hizo el done-flip. **B DONE.**
- El **A2-nominal es SEPARADO** (sin mas codigo): registro de jheredia:v1 + jball:v1 en el config-epoch (una
  re-genesis) + la e2e 7b jheredia-live + el gate 2-clones NOMINAL en la maquina de Julian. Las 2 pubkeys ya las
  tengo (persistidas en `personal/Arquitecto/A2-nominal-pubkeys.md`). Guardrail cumplido: NUNCA se provisiono la
  privada de jheredia a la maquina de build; el hub jamas se toco.

## 2. SPEC-NOTION-PROJECTOR = ESCRITA (tu GO)
`Area_comun/specs/SPEC-NOTION-PROJECTOR.md` (patron NOVA-SPEC-T-001). Notion = read-model AUDITADO del ledger,
nunca fuente. Incluye los 5 tests del consenso (a idempotente, b drift 3-familias read-only, c no-promocion-sin-
submit_intent-firmado, d cobertura F-NOVA-01 relacional, e auditoria por campo) + tus adiciones: (f) DOS workspaces
(NOVA + Metodologia) proyectados del mismo ledger, unidos por `task_id`; (g) dimension de estudio proyectada del
pre-registro (`Reservada-para-medicion` + `Ejecutor` + `Unidades-Medidas`). Vistas humanas (kanban "mis tareas" +
progreso) sobre el backbone. Decisiones = link al ADR (no en Notion). Frontera: se cablea el proyector cuando
construyas el workspace.

## 3. Higiene + candados
open/ 24 -> 0 (thread completo de B + Notion + pubkey archivado) + poda de terminales (released_ratio bajo umbral,
cold-start eficiente). validate/scan 0 en hub y Aegis. Config del hub 2E35F26E / epoch 1.14.0 byte-identico. 0
claims activos.

## 4. Escalada (fix durable)
Los announces de Codex en el hub sobre tareas de Aegis salieron 2x hoy con solo `Ops-Reason` (sin `Task-Id: none`)
-> gate rojo que bloqueaba el pre-gate del Analista; los grandfatherie (f0411e7, bdfe2db). El fix durable es su
prompt de cron (ver requested_action). Mientras no se ajuste, cada announce suyo exige grandfather manual.

-- Arquitecto (2026-07-12 20:05 local/UTC+2)
