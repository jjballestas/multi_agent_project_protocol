---
decision_id: DECISION-0047
title: Politica de versionado bajo #4 - protocol_version = version de EPOCA del genesis; release/capacidad en CHANGELOG/manifest fuera del config
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0045, DECISION-0046, DECISION-0044, DECISION-0001, DECISION-0029]
phase: P2
---

# DECISION-0047 - Versionado por epoca bajo #4

> ACCEPTED por el operador (cierre de FASE 1, 2026-06-19). Politica, no parche. NO bumpea version ni
> re-genesis ahora. Resuelve el hallazgo del cierre de Carril B pieza 1: con #4 (chain) ON el config quedo
> inmutable-sin-ceremonia, y el CHANGELOG [1.15.0] vs el config vivo 1.14.0 parecian contradecirse.

## Contexto (el hallazgo)

Con #4 ON, el genesis de la cadena = `canonical_hash(protocol.config.json)` y `validate_chain` ancla al
primer `chain.genesis` exigiendo `prev_hash == canonical_hash(config)`. Por tanto **cambiar
`protocol_version` en el config cambia el hash del genesis e invalida `chain.genesis`** -> el config quedo
**inmutable salvo re-genesis-boundary** (operacion gateada, su propia ventana). Al cerrar Carril B pieza 1
(capacidad connector, off-by-default, registro FUERA del config) la capacidad aterrizo sin tocar el config;
el CHANGELOG la documento como `[1.15.0]` mientras el config vivo sigue `1.14.0`. Eso NO es una
inconsistencia: son **dos ejes distintos** que esta decision nombra.

## Decision

1. **`protocol_version` (en `protocol.config.json`) = version de EPOCA del genesis.** Solo cambia en un
   **re-genesis-boundary** (coordinado, operador presente + rollback, en su propia ventana de riesgo;
   espejo del boundary T0 de DECISION-0045). **No** se bumpea por feature.

2. **La version de RELEASE/CAPACIDAD vive en CHANGELOG (+ manifest), FUERA del config genesis-hasheado.**
   Puede ir por delante de la epoca del genesis (p.ej. CHANGELOG `[1.15.0]` con epoca de config `1.14.0`)
   sin mentir: el CHANGELOG nombra la **linea de release/capacidad**; el config nombra la **epoca del
   genesis**. Ambos verdaderos a la vez.

3. **Capacidades nuevas se entregan FUERA del config genesis-hasheado** siempre que se pueda (p.ej. el
   registro de connectors en `connectors/connectors.config.json`, DECISION-0044), para no perturbar
   genesis/cadena. Solo lo que DEBE vivir en el config (flags de runtime, claves publicas, etc.) justifica
   un re-genesis-boundary.

4. **Los bumps de `protocol_version` se BATCHEAN.** Las deltas de release se acumulan en el CHANGELOG;
   cuando un re-genesis-boundary este justificado (su ventana gateada), se bumpea `protocol_version` a la
   version de release acumulada y se re-genesis en una sola operacion. **No** hay re-genesis por feature.

5. **Reconciliacion actual:** linea de release/capacidad = `1.15.0` (incluye el connector de Carril B
   pieza 1); epoca del genesis viva = `1.14.0`. Quedan asi hasta el proximo re-genesis-boundary batcheado.
   NO se bumpea ni re-genesis ahora.

## Alcance / No-alcance

- **En alcance:** nombrar los dos ejes de version (epoca-genesis vs release-capacidad) y la regla de batch
  + re-genesis-boundary; confirmar que capacidades fuera-del-config no requieren bump.
- **Fuera de alcance:** bumpear `protocol_version` o re-genesis ahora (batcheado, futuro); cambiar #4, el
  boundary T0 (DECISION-0045) o el connector (DECISION-0044); definir el formato del manifest de release
  (si se quiere, pieza futura).

## Consecuencias

- El CHANGELOG y el config dejan de "contradecirse": son ejes distintos, declarados.
- No hay churn de genesis/cadena por cada feature; el re-genesis se reserva para ventanas batcheadas
  gateadas.
- Refuerza el patron de DECISION-0044/0046: lo nuevo va fuera del config genesis-hasheado cuando se puede.

## Alternativas consideradas

- **Bumpear `protocol_version` por feature + re-genesis cada vez.** Descartada: churn de genesis,
  ventana de riesgo por cada feature, contra "una sola ventana de riesgo a la vez".
- **Congelar el CHANGELOG en `1.14.0` hasta el proximo re-genesis.** Descartada: ocultaria capacidades
  reales entregadas; el CHANGELOG debe reflejar lo entregado aunque la epoca del genesis vaya por detras.
