---
task_id: TASK-0191
title: "Harness de experimento H1-H3: inyeccion A1/A2/A3 (solo copia desechable) + medicion deteccion/FPR/sobrecoste + verificador externo + reporte mapeado al pre-registro (SPEC-0104)"
type: protocol
status: in_review
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0104
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
origin: DECISION-0066 (aparato de medicion del TFM; pre-registro v2.0 FROZEN)
reuses: [TASK-0190]
linked_decisions: [DECISION-0066, DECISION-0039, DECISION-0045, DECISION-0046, DECISION-0065]
file: Area_comun/tasks/TASK-0191-codex-harness-experimento-h1h3.md
---

# TASK-0191 - Harness de experimento H1-H3

> maker=Codex / checker=Arquitecto. Repo = PROTOCOLO, tooling de investigacion en `research/experiment_h1h3/`
> (neutral). Construye+prueba sobre fixtures/copias; **NO** requiere el flip A2 ni el dataset real. **FRONTERA DURA:
> solo copia desechable, NUNCA el #4 vivo** (DECISION-0045). NO toca core/genesis/#4.

## Alcance (SPEC-0104 AC1-AC7)
- Runner + inyeccion (A1 alterar/borrar/insertar/reordenar; A2 atribucion-cruzada; A3 rollback/equivocacion ancla),
  determinista (seed) + parametrizada (K); reusa `examples/attestation_negative_cases` + `actor_auth_ed25519_cases`.
- Medicion: deteccion(TPR)/FPR/salud AC2 (validate/replay sobre copia atacada y limpia); sobrecoste
  Dlatencia/Dstore(/Dtokens) con-#4 vs sin-#4 (toggle en la copia); verificador externo solo-publicas (H3/0046).
- Reporte `research/experiment_h1h3/results/<run>.json` (+MD) mapeado a los umbrales del pre-registro v2.0.

## DoD (= SPEC-0104 AC1-AC7)
- AC1 CRITICO: opera solo en copia/tmp; root vivo byte-identico tras una corrida (guard + prueba negativa).
- AC2 inyeccion reproducible por vector (misma seed -> mismos ataques); reusa vectores golden.
- AC3 deteccion por vector (100%) + FPR (0) + salud AC2; salida con conteos.
- AC4 sobrecoste Dlatencia(med/p95)/Dstore con-#4 vs sin-#4; salida con numeros.
- AC5 verificador externo solo-publicas (clon limpio): acuerdo + match de hash (0046).
- AC6 reporte mapeado a umbrales v2.0 + reproducible (misma seed = mismos resultados) + doc de uso.
- AC7 gates: tests/golden del harness en CI (fixtures, sin secretos); validate exit 0; encoding/neutralidad exit 0
  (incluye research/experiment_h1h3/); Co-Author.

## Fuera de alcance
- Ejecutar sobre el dataset real / generar dataset / flip A2 (pasos posteriores con operador); publicar resultados;
  tocar core/genesis/#4.

## Notas
- Aparato, no la corrida de medicion. Windows: tmp en RUTA CORTA / tolerar MAX_PATH (leccion TASK-0190). Checker
  corre en clon limpio ruta corta. Reusar cripto/vectores existentes; cero secretos al repo.
