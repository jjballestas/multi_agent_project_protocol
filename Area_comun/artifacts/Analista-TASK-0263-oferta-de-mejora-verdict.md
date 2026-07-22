---
artifact_id: Analista-TASK-0263-oferta-de-mejora-verdict
reviewer: Analista
task_id: TASK-0263
verdict: OK-CLOSABLE
created_at: 2026-07-23
anchor_commit: f97e0e1
protocol_head: 3fb2c91
---

# Veredicto adversarial - TASK-0263 (C3-bis mecanismo de oferta de mejora)

Voz: Analista (checker independiente). Sin producto en alcance.

## Ancla canonica

- Impl commit revisado: `f97e0e1` (feat(protocol): add deterministic improvement offers).
- Protocol HEAD al revisar: `3fb2c91`.
- Metodo: CLON LIMPIO en `/d/ccv-0263`, `git checkout f97e0e1`, gates por EXIT code
  en el clon (no en arbol caliente). Ataque por comportamiento con payloads propios
  (bateria unicode/espacios + ciclo anti-bucle via CLI real por subprocess).

## Reproduccion (exit codes en clon limpio f97e0e1)

| Gate | Comando | Exit |
|------|---------|------|
| Suite | `python examples/improvement_offer_cases/run_improvement_offer_cases.py` | 0 (`{"ok":true,"cases":6,"auto_apply_routes":0}`) |
| Validate | `python scripts/validate_collaboration_state.py` | 0 |
| Encoding | `python scripts/scan_encoding.py` | 0 |
| Neutralidad | `python scripts/scan_domain_neutrality.py` | 0 |
| Diff-check | `git diff --check` | 0 |

Estado canonico previo a la revision: validate exit 0, drift 0.

## Tabla vector por vector

| # | Vector | Resultado | Evidencia |
|---|--------|-----------|-----------|
| 1 | CERO auto-aplicacion (invariante duro) | PASS | Imports = solo stdlib (`argparse, hashlib, json, re, unicodedata, dataclasses, pathlib, typing`). Cero `subprocess/os/exec/eval/system/socket/requests`. Cero import de `submit_intent`/`ledger`. Unico efecto de escritura = `args.registry.write_text(...)` (2 llamadas, ambas a la ruta `--registry` dada por el humano). No escribe en `skills/`, `decisions/`, ni toca harness. Barrido del repo: ningun otro modulo importa `improvement_offers` ni lee el registro para aplicar; `submit_intent.py` no referencia el mecanismo. Unica salida = oferta (texto) + registro. |
| 2 | Criterio root determinista (NFKC+casefold+trim+collapse+exacto) | PASS | `root_key = " ".join(NFKC(root).casefold().split())`, funcion pura => reproducible (mismo input -> misma clave -> mismo `proposal_id`, verificado). SUB-FUSION correcta (misma clave): case, tab/multi-space, trim, NBSP, narrow-NBSP, combinante, fullwidth, ligadura fi, newline. Sin SOBRE-FUSION (claves distintas): palabras distintas, I vs i sin punto (turco), digitos distintos, substring. |
| 3 | Anti-bucle | PASS | ACEPTADA nunca recurre (`status==accepted -> continue`). RECHAZADA/PARQUEADA: solo re-oferta si `evidencia cambio Y pid en --new-evidence` (ambas condiciones). Registro se consulta ANTES (dict `prior` desde el registro). Ciclo via CLU real: rechazar+identico=NO; +evidencia sin flag=NO; +evidencia con flag=SI; flag sin evidencia nueva=NO; parqueada=NO. |
| 4 | Ambos carriles al mismo evaluador | PASS | `read_runtime` (JSON/JSONL) y `read_mailbox` (REPORTE) producen `Obstacle` que `main()` concatena hacia un unico `evaluate`. Merge cross-carril confirmado: root compartido entre runtime (2 entregas) + mailbox (1) => UNA oferta con 3 citations que incluyen prefijos `runtime:` y `mailbox:`. |
| 5 | Los 5 casos de acceptance | PASS | high->oferta; root x2 (distintas delivery_id)->oferta; rechazada->no re-oferta; aceptada->marcada y no recurre; sin candidatos->nada. Ejercitados con payloads propios via CLI, no por nombre de test. |
| 6 | Oferta con borrador concreto + cita de obstacles | PASS | `draft_change` embebe root_cause + resolution + what reales con requisito de regresion (contiene "MUST"). `citations` en forma `source#delivery:evidence`, ordenadas. |

## Residuales declarados (informativos, NO bloqueantes)

- El criterio es exactamente "NFKC+casefold+trim+collapse+exacto". Por diseno de casefold/
  NFKC, fusiona pares semanticamente-equivalentes: `strasse`/`strasze` (eszett -> ss),
  `x2`/`x^2` (superindice compat). Es el comportamiento DECLARADO del criterio, no un slip.
- Un caracter invisible de ancho cero (ZWSP U+200B) dentro del root NO se colapsa (no es
  whitespace para `.split()` ni tiene descomposicion NFKC), asi que impediria un merge que
  visualmente parece identico. Direccion FAIL-SAFE del mecanismo: produce SUB-oferta (no
  ofrece de mas), nunca auto-aplica de mas. Residual exotico, no bloqueante.
- El destino `--registry` lo da el humano; si apunta a un archivo existente que YA es un
  registro valido, se sobrescribe con JSON de registro (nunca con texto de skill/regla).
  No es una ruta impulsada por un obstacle; requiere argumento humano explicito. No es
  auto-aplicacion.

## Recomendacion de cierre

OK-CLOSABLE. El invariante duro (cero auto-aplicacion) se sostiene por lectura de imports/
llamadas y barrido de consumidores; el criterio root es determinista, reproducible y sin
sobre/sub-fusion sobre diferencias triviales; el anti-bucle bloquea la re-oferta de una
rechazada/parqueada salvo evidencia nueva declarada + flag; ambos carriles alimentan el
mismo evaluador; los 5 casos pasan por comportamiento; todos los gates exit 0 en clon
limpio. Sin residual bloqueante. TASK-0263 es cerrable.

-- Analista
