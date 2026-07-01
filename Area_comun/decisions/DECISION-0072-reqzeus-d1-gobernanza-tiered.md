---
decision_id: DECISION-0072
title: "REQ-ZEUS D1 - Gobernanza TIERED del producto (coordination por defecto, atestacion conmutable); NOVA permanece coordination y la demo TFM apunta al CORE"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0022]
scope: product
phase: P2
---

# DECISION-0072 (REQ-ZEUS D1) - Gobernanza tiered del producto

> ACCEPTED (operador endoso en directiva OPS-115242Z + ordeno registrar en el hub como cadena unica, 2026-06-30).
> Canonicaliza en el HUB (DECISION-0050) la D1 originalmente redactada en la instancia NOVA
> (`D:/Agentes/Zeus/NOVA/Area_comun/decisions/DECISION-0001-D1-gobernanza-tiered.md`). No toca los `*.template.*`
> (neutralidad del master enviable intacta); vive en el `Area_comun/` de la instancia viva.

## Decision
Gobernanza TIERED con tres posturas para Zeus-Aegis/NOVA:
1. **coordination (DEFECTO, NOVA/empleados):** estado JSON+git+validador+maker!=checker por disciplina; sin Ed25519,
   sin ledger firmado, sin claves. Cero friccion criptografica.
2. **attested-signers-only (upgrade conmutable, decision-gated):** `agent_signatures_enabled`+`chain_enabled` ON,
   `enforce`/`authoritative` OFF. Solo firmantes frontera tienen clave; peones nunca. Drift detectado, no hard-rejected.
3. **attested-full:** + `enforce`/`authoritative` (single-writer hard-gate); requiere re-genesis coordinado y ambos
   loops en `submit_intent` (DECISION-0022). Es la postura viva del CORE del TFM.

**NOVA permanece en coordination.** La atestacion es upgrade conmutable por instancia (re-genesis documentado).
**La demo del TFM apunta al CORE atestado, nunca a NOVA.**

## Razon
La contribucion de la tesis no es que los empleados firmen, sino que la metodologia es coordinacion ATESTADA y
verificable cuando importa. coordination-only da el 90% del valor (la disciplina) sin la friccion de claves/re-genesis;
la atestacion se difiere a donde gana su coste. "Delego pero respondo" (peon drafter no-firmante + firmante responsable)
funciona en coordination via ownership + maker!=checker.

## Consecuencias
- NOVA debe registrar el Analista (checker) para garantizar maker!=checker por roster (WS5, tarea de alta del Analista).
- F2 write-through al ledger MEDIDO sigue fuera de alcance (REQ-ZEUS): el producto opera coordination sobre la
  instancia del proyecto, no sobre el ledger del TFM.
