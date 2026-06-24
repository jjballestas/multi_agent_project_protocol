---
task_id: TASK-0171
title: "Proyecto-front: alta de worker de producto enlazado a un modelo (US-4, SPEC-0091 AC1-AC6) -- fuera del config atestado, off-by-default, sin tocar #4/genesis/firmantes"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0091
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-4A88ECFFC4]
linked_decisions: [DECISION-0050, DECISION-0047]
file: Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
---

# TASK-0171 - Front: alta de worker de producto + modelo (SPEC-0091)

> Q3 (parte NO gateada del roster: workers de producto, NO firmantes del ledger). maker=Codex / checker=Arquitecto
> + PASADA DEL ANALISTA (fronteras). #4 byte-identica; ASCII-only. Repo producto Zeus-protocol.

## Alcance (SPEC-0091 AC1-AC6 + carries AC11/AC12/AC13)

- **AC1** Alta gobernada (preview->confirm->execute) de un worker {id, role, provider, defaultModel,
  defaultEndpoint} -> una entrada acotada en el registro de workers de producto (extractors.config.json o su
  override de runtime gitignored). Construir sobre loadProductWorkers().
- **AC2** Clave de PRODUCTO del worker: privada SOLO server-side (gitignored, nunca al cliente, nunca commiteada);
  publicKeyPem en el registro. (O publica provista por el operador; jamas privada hacia el cliente.)
- **AC3** Off-by-default: registrar NO habilita uso vivo; el uso vivo exige el gate de file-ingestion existente.
- **AC4** (FRONTERA DURA, prueba negativa) NUNCA toca protocol.config.json (agent_registry/signature_config),
  genesis ni ledger; NO emite submit_intent; #4 byte-identica; ningun firmante nuevo.
- **AC5** Write acotado/validado: campos typeof string estricto (rechaza no-string/array/object -> 400 antes de
  coercion; LECCION 0166), id no duplicado, sin path-traversal/claves-extra, endpoint loopback/localhost. 400 sin
  escribir en los casos invalidos.
- **AC6** Estado claro + error amable; off-by-default; PII redactada.

## DoD

- AC1-AC6 verdes con behavior-tests deterministas (incl. la prueba negativa AC4 #4-byte-identica y la AC5
  type-confusion); AC11/AC12/AC13 verdes. node --test clon limpio exit 0; validate con/sin secretos exit 0; drift
  0; neutralidad+encoding 0; #4 byte-identica. La clave privada del worker NUNCA en el cliente ni en git.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. **PASADA DEL ANALISTA** (AC4 no-toca-
  #4/genesis/firmantes; AC2 privada-nunca-al-cliente; AC5 write acotado sin type-confusion; off-by-default).
- REPRO: registrar un worker {id, role, modelo endpoint+nombre} -> aparece en el registro de workers de producto
  (no en signature_config), apagado, con publicKeyPem; protocol.config.json y #4 intactos; alta invalida (id dup /
  no-string / endpoint no-loopback) -> error amable, no escribe.

## Notas

- Preferir override de runtime gitignored para el alta (no commitear workers ni claves), master en estado base.
- Diferencia con US-5 (firmante = ceremonia re-genesis, GATEADA): este worker NO firma el ledger -> sin re-genesis.
- Citar el commit del design-system vigente en el handoff.
