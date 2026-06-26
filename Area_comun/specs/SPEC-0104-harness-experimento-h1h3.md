---
spec_id: SPEC-0104
task_id: TASK-0191
type: feature
status: accepted
linked_decisions:
  - DECISION-0066
  - DECISION-0039
  - DECISION-0045
  - DECISION-0046
  - DECISION-0065
created_at: 2026-06-27
updated_at: 2026-06-27
author: Arquitecto
---

# SPEC-0104 - Harness de experimento H1-H3 (medicion adversarial reproducible)

## Context

DECISION-0066: aparato reproducible que mide H1-H3 del pre-registro v2.0 (FROZEN, sha256 e8277cc7...). Forja
eventos -> SOLO sobre copia desechable, NUNCA el #4 vivo (DECISION-0045). maker=Codex / checker=Arquitecto. Repo =
PROTOCOLO, como tooling de investigacion en `research/experiment_h1h3/`. Construye+prueba sobre fixtures/copias;
NO requiere el flip A2 ni el dataset real.

## Scope

- `research/experiment_h1h3/` (neutral): runner + modulos de inyeccion + medicion + verificacion + reporte.
- **Inyeccion** (determinista, seeded, parametrizada por K): A1 (alterar/borrar/insertar/reordenar), A2
  (atribucion cruzada: keyid ajeno / sig invalida / firmar-como-otro), A3 (rollback/equivocacion de ancla). Reusa
  las definiciones de `examples/attestation_negative_cases` + `examples/actor_auth_ed25519_cases` (no re-implementa
  cripto).
- **Medicion:** corre validate/replay sobre la copia atacada -> deteccion (TPR) por vector + sobre la copia limpia
  -> FPR + salud AC2; sobrecoste Dlatencia/Dalmacenamiento(/Dtokens) **con-#4 vs sin-#4** (toggle de flags en la
  copia); verificador externo (solo publicas, clon limpio) -> acuerdo + match de hash (H3/0046).
- **Reporte:** artefacto estructurado (JSON + MD legible) que mapea cada metrica a su umbral pre-comprometido del
  pre-registro v2.0; re-corrida determinista = mismos resultados.

## Acceptance Criteria

- **AC1 (copia-desechable; NUNCA el vivo) [CRITICO]:** el harness opera sobre una copia/tmp que el crea; **no
  lee/escribe** `runtime/state/events.jsonl` ni `Area_comun/state/*` del root vivo. Prueba negativa: un guard/test
  demuestra que el root vivo queda byte-identico tras una corrida completa.
- **AC2 (inyeccion reproducible por vector):** A1/A2/A3 inyectados de forma determinista (seed fija) y
  parametrizada (K); misma seed -> mismos ataques. Reusa los vectores golden existentes.
- **AC3 (deteccion + FPR, H1):** sobre la copia atacada, valida y registra **deteccion por vector** (esperado
  100%); sobre la copia limpia registra **FPR** (esperado 0) y **salud AC2**. Salida con conteos.
- **AC4 (sobrecoste, H2):** mide Dlatencia (mediana/p95) y Dalmacenamiento por evento **con-#4 vs sin-#4** sobre la
  copia; (Dtokens si aplica). Salida con numeros.
- **AC5 (verificador externo, H3):** verifica `actor_auth`/cadena con **solo publicas** desde un clon limpio (sin
  secretos) -> acuerdo de veredicto + match de hash canonico (DECISION-0046). Salida booleana + detalle.
- **AC6 (reporte mapeado + reproducible):** emite `research/experiment_h1h3/results/<run>.json` (+ MD) con cada
  metrica vs su umbral del pre-registro v2.0 y veredicto provisional por hipotesis; re-corrida (misma seed/copia)
  = resultados identicos. Documenta como correrlo.
- **AC7 (gates):** tests/golden del harness en CI (sobre fixtures, sin secretos); `validate_collaboration_state.py`
  exit 0; `scan_encoding`/`scan_domain_neutrality` exit 0 (incluye `research/experiment_h1h3/`); Co-Authored-By Codex.

## Out of scope

- EJECUTAR el harness sobre el dataset real / generar el dataset / el flip A2 (pasos de medicion posteriores, con
  el operador). Publicar resultados (GATE-DATASET). Tocar el core/genesis/#4.

## Notes

- El harness es el aparato; la corrida de medicion real es posterior. Construir/probar = sobre fixtures+copias
  (sin secretos en CI; las firmas Ed25519 de prueba se generan en fixtures como en `actor_auth_ed25519_cases`).
  Windows: el harness debe usar rutas de tmp CORTAS / tolerar MAX_PATH (leccion TASK-0190: temp anidados revientan
  en clones de ruta larga). Checker corre en clon limpio ruta corta.
