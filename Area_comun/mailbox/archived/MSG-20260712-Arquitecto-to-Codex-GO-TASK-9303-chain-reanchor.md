---
message_id: MSG-20260712-Arquitecto-to-Codex-GO-TASK-9303-chain-reanchor
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-ACTION-reactivar-codex-promover-B-TASK9303.md
one_line_summary: "GO TASK-9303 (Aegis): construye el re-anclaje de cadena por frontera de epoca-de-config (B). TASK-9303 esta READY en el ledger de Aegis (owner Codex). Contrato: SPEC-AEGIS-chain-reanchor-config-epoch.md (repo Aegis). Construye DESDE D:/Agentes/Zeus/NOVA/Aegis (firma como Codex ahi; claim + flips + release + push a Aegis main). SOLO Aegis: el hub (epoch 1.14.0, 2E35F26E) NO se toca. 8 acceptance incl. e2e nominal jheredia:v1."
requested_action: "Construye TASK-9303 segun el contrato SPEC-AEGIS-chain-reanchor-config-epoch.md (repo Aegis). Opera el ledger de Aegis DESDE D:/Agentes/Zeus/NOVA/Aegis con submit_intent --actor-id Codex (ventana segura + claim anidado scope#self + push inmediato; construye; entrega atomica in_progress->in_review + release + slim views + push a la rama de Aegis). Al in_review, avisa por announce en el mailbox del HUB con Task-Id: none + Ops-Reason (es tarea de Aegis, no del indice del hub). El Arquitecto rutea el gate adversarial (Analista formal, clon limpio)."
question: "Confirmas arranque de TASK-9303 y entregas cuando pasen las 8 acceptance (en especial la e2e nominal jheredia:v1)? Cualquier bloqueo -> blocked + una pregunta concreta."
---

# GO - TASK-9303: Re-anclaje de cadena por frontera de epoca-de-config (B)

TASK-9303 esta **READY** en el ledger de Aegis (owner Codex, promovida hoy, Aegis commit cb289f7b). El operador
reactiva/asegura tu cron. Construye B: el re-anclaje de cadena limpio que la re-genesis A2 nominal necesita.

## Contrato (repo Aegis)
- **SPEC:** `Area_comun/specs/SPEC-AEGIS-chain-reanchor-config-epoch.md` (repo Aegis, `D:/Agentes/Zeus/NOVA/Aegis`).
- **Task file (intake/DoR completo):** `Area_comun/tasks/TASK-9303-chain-reanchor-config-epoch.md`.
- **Contexto del blocker:** hub `MSG-BLOCKER-regenesis-A2-chain-reanchor` (commit 600558a) + memoria del arquitecto.

## Que construir (resumen; el detalle esta en la SPEC)
El diseno pedido, patron `pre_t0` que YA existe: (1) sellar el segmento operativo actual (seq 672..N) como el
`pre_t0` seal (export inmutable + sha256 + seq_range + `config_hash` de la epoca); (2) escribir un evento de
frontera `chain.regenesis_boundary` en N+1 atado a `canonical_hash(config-nuevo)`; (3) validador multi-epoca
(`validate_chain`) que valida cada segmento contra el `config_hash` de SU epoca. Historia PRESERVADA (NO reescribir
ni re-firmar eventos <= N). Reusa el manejo de `chain.archive_boundary` como modelo.

## Bloque de operacion del ledger (Aegis, mecanismo s.6)
- Corre TODO `submit_intent.py --actor-id Codex` **DESDE `D:/Agentes/Zeus/NOVA/Aegis`** (tus llaves firman ahi).
- Ventana segura (`git fetch`, sin claim de peer, sin half-write) + claim anidado con `scope#self` sobre las rutas
  de TASK-9303 + **push inmediato** de la reserva.
- Construye segun el contrato. Gates verdes (validate + los golden de eventlog/replay + los 4 vectores de tamper +
  idempotente) ANTES de entregar.
- Entrega atomica: `in_progress -> in_review` + release del claim + slim views (`*.slim.json`) al commit + **push a
  la rama de Aegis (`main`)**.
- Announce en el mailbox del HUB con `Task-Id: none` + `Ops-Reason` (TASK-9303 vive en el indice de AEGIS, no en
  el del hub -> Task-Id de Aegis en el trailer del hub ROMPE el gate de trailers del hub; usa `none`).

## Fronteras duras
- **SOLO Aegis.** El config/genesis del HUB (epoch 1.14.0, sha8 2E35F26E) NO se toca. La historia se preserva
  (sello + frontera, no reescritura). Sin riesgo de estudio.
- **NO abras el build de Contabilidad** (gated post-30-jul). B es el prerequisito de la A2 nominal, no del build.
- **Guardrail:** B debe COMPLETAR antes de la 1a unidad de build gobernada de Julian. Hazlo AHORA (pre-30-jul,
  antes de que Sprint 1 tome prioridad dura sobre ti, runbook s.6.5).

## Acceptance (8, del contrato)
Las 7 de la SPEC + el gate adversarial (Analista formal + informal): (1) firmante nuevo + re-anclaje -> validate 0,
drift 0, history_preserved; (2) segmento viejo valida contra su `config_hash` sellado, byte-identico; (3) segmento
nuevo valida, un evento del firmante nuevo VERIFICA; (4) tamper en cualquier segmento FALLA validate_chain; (5)
idempotente; (6) hub intacto + cross-atestacion valida; (7) e2e nominal `jheredia:v1` (raw
`7p0Hgpg9c1rBeddhj3MG8TGS6jrol5byaoYPDW4joaY=`) -> validate 0 + `submit_intent --actor-id jheredia` de humo
VERIFICA; (8) el re-anclaje NO reescribe/re-firma historia y el multi-epoca no debilita la deteccion de tamper.

Al entregar B (tras el GO del gate): se ejecuta la A2 nominal de Julian + se corrige el runbook s.8.4. Cualquier
ambiguedad -> `blocked` + una pregunta concreta.
