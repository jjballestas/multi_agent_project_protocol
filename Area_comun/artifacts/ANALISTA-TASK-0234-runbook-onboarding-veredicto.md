# ANALISTA - Veredicto TASK-0234 runbook onboarding remoto

Firma: Analista
Fecha: 2026-07-03
Task: TASK-0234
Decision: CAMBIO-REQUERIDO
Recomendacion de cierre: NO CERRABLE

## Ancla canonica

- Protocolo revisado: e8bb127457e0e74e4d96df13d7390cb9aec84f47.
- Entrega doc citada: 64d44ad, `Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md` v1.0.
- Producto: la instruccion de review no cita commit de producto. Para cumplir el gate de clon limpio se clono `D:/Agentes/Zeus/Zeus-protocol` y se probo el HEAD disponible `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- #4 / core pineado: `protocol.config.json` byte-identico entre 64d44ad y HEAD, sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`, 7794 bytes.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` + `git status --short` | exit 0; arbol local tenia cambios ajenos/untracked preexistentes fuera de este veredicto. |
| JSON state con `utf-8-sig` | exit 0; `Area_comun/state/*.json` parsea OK. |
| `python scripts/validate_collaboration_state.py` | exit 0; warning no bloqueante sobre FYI stale. |
| `python scripts/validate_collaboration_state.py` en clon sin `secrets/` | exit 0. |
| `python scripts/scan_domain_neutrality.py` | exit 0. |
| `python scripts/scan_encoding.py` | exit 0 antes de redactar veredicto. |
| Drift #4 | exit 0; `has_drift=false`, `up_to_seq=3601` antes de mi claim. |
| Clon limpio producto + `npm test` | exit 0; 90 pass, 22 skipped, 0 fail. |

## Vector por vector

| Vector / AC | Veredicto | Evidencia adversarial |
| --- | --- | --- |
| Onboarding en frio: clonar instancia remota privada | PASA | El runbook da `git clone -c core.longpaths=true <URL-remoto-privado> <carpeta>` y explicita que no es el hub. |
| Configurar agente con config commiteada y Git como adapter | PASA | Declara `.agents/<id>/config.json`, `adapter=git`, `committedConfig=true`; no introduce adapters multi-IDE. |
| Operar 1 tarea completa via Git puro | SLIPS | Cubre el ciclo conceptual `pull -> claim -> push -> entrega -> push -> review -> done`, pero no entrega comando falsable de `submit_intent` para claim/status/handoff ni payload minimo. Un participante no-constructor puede quedar bloqueado en el primer write gobernado. |
| Uso del harness F2.3 y ciclo e2e F2.2 | SLIPS | La aceptacion promete usar harness F2.3 y ciclo e2e F2.2. El documento solo los nombra en el subtitulo/contexto; no da ruta, comando, fixture ni criterio de exito para ejecutarlos. |
| Transferibilidad fuerte para agente que no construyo la instancia | SLIPS | La transferencia depende de conocimiento tacito: donde esta el template real de `.agents/<id>/config.json`, como invocar `runtime/submit_intent.py`, que campos exige una tarea de prueba, y como reconocer el cierre gobernado. Esto contradice "sin pasos manuales ocultos". |
| Objetivo medido `<=1 dia` y medicion HP6 posterior | PASA | Declara objetivo, cronometraje posterior y que la medicion real no forma parte del doc. |
| ASCII y neutralidad en hub | PASA | Gated por `scan_encoding.py` y `scan_domain_neutrality.py`, ambos exit 0. |
| No tocar core pineado | PASA | `protocol.config.json` byte-identico entre entrega y HEAD; no hay cambio de epoch. |

## Hallazgos

F-0234-01 (bloqueante): el runbook no es ejecutable de punta a punta por un participante no-constructor porque omite comandos/payloads concretos para las transiciones gobernadas. Reproduccion falsable: siguiendo solo el doc, el paso "Claim la tarea via submit_intent" no contiene script, flags, JSON minimo ni ejemplo de salida esperada.

F-0234-02 (bloqueante): el AC exige usar harness F2.3 y ciclo e2e F2.2, pero el runbook no referencia ruta ni comando de esos artefactos. Reproduccion falsable: buscar en `RUNBOOK_ONBOARDING_REMOTO.md` una ruta/comando ejecutable del harness; no existe.

## Residuales

- El gate de producto no esta anclado a un commit citado por la instruccion; se ejecuto sobre el HEAD limpio disponible `e7c6da4`.
- La medicion real employee-run queda correctamente fuera de alcance, pero el runbook debe quedar mas operacional antes de usarlo como instrumento de esa medicion.

## Fix-loop esperado

Remediacion maximo 2 iteraciones antes de escalar al operador:
1. Agregar ejemplos ejecutables de `runtime/submit_intent.py` para claim, entrega a `in_review`, mensaje/handoff minimo y cierre esperado, con campos obligatorios y criterio de exit code.
2. Agregar rutas/comandos concretos del harness F2.3 y del ciclo e2e F2.2 que el participante debe correr, mas salida esperada.
3. Re-juicio previo al commit de cierre con gates: validate con/sin secretos, drift 0, domain, encoding, #4 byte-identica y prueba de comportamiento del flujo documentado.

task_id: TASK-0234
status: CAMBIO-REQUERIDO
executive_summary: "NO CERRABLE: el doc pasa neutralidad, ASCII, #4 y objetivo medido, pero falla transferibilidad fuerte por omitir comandos/payloads gobernados y rutas/comandos del harness F2.3/F2.2."
artifacts: "Area_comun/artifacts/ANALISTA-TASK-0234-runbook-onboarding-veredicto.md; Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-runbook-onboarding-veredicto.md"
gates: "validate=0; validate_no_secrets=0; domain=0; encoding=0; drift=0; product_npm_test_clean_clone=0; protocol_config_byte_identical=true"
next_recommended: "Remediar F-0234-01/F-0234-02 y pedir re-juicio Analista antes del commit de cierre."
risks: "Producto sin commit citado en instruccion; doc podria no sostener una employee-run externa sin asistencia tacita."
