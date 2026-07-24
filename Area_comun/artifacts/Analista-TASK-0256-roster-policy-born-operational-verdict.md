# Analista verdict -- TASK-0256 (espejo DECISION-0099 en el export born-operational)

- Reviewer: Analista (independent adversarial checker; provider-diverse; maker != checker).
- Verdict: **CHANGE-REQUIRED (NO-GO)** -- 1 defecto real, fix minimo de 1 clausula. Todo lo demas PASA.
- Emitted: 2026-07-24 03:30 local (UTC+0200).

## Canonical anchor

- Repo under review: multi_agent_project_protocol (protocol hub). SIN producto en alcance
  (no se corrio ningun npm test de Nova-Budget/Zeus).
- origin/main HEAD: `3b72609` (contiene la entrega `9879e9a` y el impl `8168fae`).
- Impl commit: `8168fae` (Codex). `git diff --numstat 8b93841 3b72609` fuera de ledger/mailbox/tasks
  = **exactamente `AGENTS.template.md` 14/0**; ningun commit posterior toca el texto revisado.
- Method: CLON LIMPIO de origin/main en `/d/ccv0256`, `checkout 3b72609`, gates corridos ALLI por EXIT
  code. Comportamiento probado por el ENTRYPOINT REAL (`scripts/new_instance.py`) generando instancias
  temporales en los **tres** tiers, no solo el ejemplo dado. Nada corrido in-place.

## Que cambio (auditado, no confiado)

`AGENTS.template.md` +14/-0: bloque "Roster policy" con 3 reglas numeradas, insertado en la seccion
`## 3. Agent Roles`, despues de la tabla "Suggested role model" y antes de `## 4`. Texto estatico, sin
placeholders `{{...}}`. `scripts/new_instance.py` NO cambiado (mapa `CANONICAL_TEMPLATE_FILES`,
`"AGENTS.template.md": "AGENTS.md"`, ya materializaba el template). Runtime, validadores,
`protocol.config.json`, `AGENTS.md` vivo, `examples/`, `profiles/` y `scripts/`: INTACTOS (verificado
por `git diff --numstat` con esos pathspecs = vacio).

## Reproduccion (exit codes, clon limpio /d/ccv0256 @ 3b72609)

Gates de protocolo (en el clon):
- `python scripts/validate_collaboration_state.py` -> exit 0 ("OK: collaboration state is valid.")
- `python scripts/scan_domain_neutrality.py` -> exit 0
- `python scripts/scan_encoding.py` -> exit 0 ("OK: encoding scan is clean.")
- `python runtime/protocol_replay.py --check-drift --root .` -> exit 0
  ("PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=6316") -- drift 0.

Entrypoint real (instancias TEMPORALES generadas por mi, no las del maker):
- `new_instance.py --tier coordination` -> exit 0
- `new_instance.py --tier runtime` -> exit 0
- `new_instance.py --tier attested --roster <roster con un worker>` -> exit 0
- `new_instance.py --tier attested` (roster POR DEFECTO, sin `--roster`) -> exit 0

En los 4 AGENTS generados (`<inst>/AGENTS.md`; en attested `<inst>/Aegis/AGENTS.md`):
- `grep -c "Roster policy"` -> 1
- `grep "worker agent is a code executor subordinate"` -> exit 0 (regla 1)
- `grep "maker must be a strong-capability agent and governs every worker"` -> exit 0 (regla 2)
- `grep "adversarial checker must always be a strong-capability agent"` -> exit 0 (regla 3)
- `grep "maker != checker"` -> exit 0
- `grep -o "{{[A-Z0-9_]*}}"` -> vacio (cero placeholders sin sustituir)
- bytes >127 en el AGENTS generado -> 0

Gates de la instancia RECIEN NACIDA (`--root <instancia generada>`), los 3 tiers:
- validate -> exit 0 ; scan_encoding -> exit 0 ; scan_domain_neutrality -> exit 0.

Suites de instanciacion que podrian romperse por el +14 (golden files):
- `python scripts/test_attested_instancing.py` -> exit 0 ("attested instancing golden checks passed")
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> exit 0

Falsabilidad del gate de neutralidad (para que el verde no sea vacio): inyecte en el clon una linea
con termino de negocio al final de `AGENTS.template.md` -> `scan_domain_neutrality.py` exit **1**
(`AGENTS.template.md:260: trading`); restaure el archivo -> exit **0**, `git status --short` limpio.
El scan SI cubre el archivo modificado.

## Vector por vector

| # | Vector probado | Resultado |
|---|----------------|-----------|
| V1 | Las 3 reglas de 0099 estan en `AGENTS.template.md`, dentro de la seccion de roles | PASS |
| V2 | Llegan al AGENTS GENERADO por el entrypoint real: coordination / runtime / attested(roster) / attested(default) | PASS (4/4) |
| V3 | Cero placeholders sin sustituir y cero bytes no-ASCII en el AGENTS generado | PASS |
| V4 | La instancia recien nacida pasa sus PROPIOS gates (validate/encoding/neutralidad) | PASS (3/3 raices) |
| V5 | Neutralidad: sin terminos de dominio en el texto anadido, con gate FALSABLE | PASS |
| V6 | Fidelidad semantica vs DECISION-0099 (R1 subordinacion+prohibiciones, R2 gobierno+DoR/contrato/acceptance/verification_cmd/scope/out_of_scope+accountability+refinamiento previo+mas debil=mas spec, R3 checker fuerte+capacidad ademas de llave+maker!=checker) | PASS (ver RES-3) |
| V7 | Alcance del diff: solo `AGENTS.template.md` +14/-0 fuera de ledger/mailbox/task; runtime, validador, config, `AGENTS.md` vivo, `examples/`, `profiles/`, `scripts/` sin tocar | PASS |
| V8 | No hay OTRO entrypoint de instanciacion que evada el template (no existe `new_instance.ps1`; el unico camino es `new_instance.py`; `upgrade_instance.py` lleva `AGENTS.template.md` en su set adoptable) | PASS |
| V9 | Golden/instancing suites no rotas por el +14 | PASS (2/2 exit 0) |
| V10 | Gates de protocolo en el clon limpio (validate/neutralidad/encoding/drift) | PASS (4/4 exit 0) |
| V11 | **Colision de vocabulario "worker" en el artefacto EXPORTADO** | **SLIP (bloqueante, ver abajo)** |

## SLIP-1 (bloqueante, fix de 1 clausula): el export nace llamando "worker agent" al human owner

Hecho reproducible, tier **attested**, roster POR DEFECTO (sin `--roster`), instancia generada por
`new_instance.py` en clon limpio:

- `<inst>/Aegis/protocol.config.json` -> `agent_registry.agents[]` contiene
  `{"id":"owner-a","role":"human_owner","tier":"worker",...}` (tambien replicado en
  `attested_instancing.roster[]`). Esto NO es mi roster: es el que `new_instance.py` emite por defecto
  (`scripts/new_instance.py:519`). El unico vocabulario de tier del hub es `{"signer","worker"}`
  (`scripts/new_instance.py:534`), y es una distincion de POSESION DE LLAVE, no de capacidad.
- `<inst>/Aegis/AGENTS.md:60` (tabla de roles, 4 lineas ARRIBA del texto nuevo):
  `| owner-a | Human owner | Approves project policy, critical transitions and business decisions | - |`
- `<inst>/Aegis/AGENTS.md:64` (texto NUEVO, regla 1): "A worker agent is a code executor subordinate to
  the maker ... never acts as checker, orchestrator, or ratification signer."

Consecuencia falsable: tras este commit, el bloque anadido es la **unica definicion normativa de
"worker" que una instancia nace conteniendo** (grep en la instancia generada: no hay ninguna otra
definicion de tier `worker` en su documentacion), y esa definicion es FALSA para la entrada
`tier:"worker"` que el mismo generador escribe para el human owner: dice que un worker es un ejecutor
de codigo subordinado al maker que nunca ratifica, mientras la tabla inmediatamente anterior le asigna
la aprobacion de politica y transiciones criticas. Un adoptante en frio, leyendo su `AGENTS.md`
seccion 3 junto a su propio `agent_registry`, obtiene guia contradictoria sobre quien ratifica.

Por que es defecto de ESTE cambio y no preexistente: antes de `8168fae` la instancia no contenia
ninguna definicion de "worker agent"; la colision la introduce el texto exportado al elegir
exactamente el token que el registry ya usa para el human owner. DECISION-0099 habla de "peon"
(agente trabajador debil), nunca del human owner.

Por que es bloqueante para MI: el entregable ES texto normativo y su unica funcion declarada en el
intake es que "toda instancia NUEVA nazca con la politica anotada en su contrato de roster" de forma
inequivoca. En el tier attested -- el tier al que apunta el export born-operational de DECISION-0096 --
nace equivoca. No falla en falso-verde de ningun gate: falla en el contrato que el adoptante lee.

Fix MINIMO propuesto (una clausula, sin tocar runtime, sin cambiar las 3 reglas):
en la regla 1, acotar el sujeto. Por ejemplo:

```
1. A worker agent (a weak-capability participant that executes code; this does not include the
   human owner, whose approval authority is defined in the role model above, regardless of the
   `tier` value its registry entry carries) is a code executor subordinate to the maker. ...
```

o, alternativa igual de valida, una linea introductoria antes de la lista:
"This policy governs agent participants that execute code; it does not alter the human owner's
approval authority, nor does it redefine the `signer`/`worker` key-possession tiers of the registry."

Cualquiera de las dos cierra el SLIP. La eleccion de redaccion es del maker.

## Residuales declarados (NO bloqueantes)

- RES-1: `examples/generated_minimal_instance/AGENTS.md` (instancia generada versionada como muestra)
  NO contiene la politica (`grep -c "Roster policy"` -> 0). No la regenera CI (validate.yml solo valida
  `.` y `examples/minimal_instance`), asi que no rompe ningun gate; pero quien lea ese ejemplo como
  "asi nace una instancia" no ve la politica. Artefacto historico obsoleto, no regresion de esta tarea.
- RES-2: `scripts/upgrade_instance.py` lleva `AGENTS.template.md` en `DEFAULT_ADOPTABLE_GLOBS`, es
  decir propaga el TEMPLATE a instancias existentes, no re-materializa su `AGENTS.md` vivo. Las
  instancias vivas por tanto no reciben la politica en su contrato operativo de forma automatica.
  Coincide con el out_of_scope declarado ("su AGENTS se actualiza en su propio ciclo"); lo nombro para
  que el mecanismo quede trazado, no como objecion.
- RES-3: el espejo conserva las 3 reglas pero omite la RAZON de la regla 3 de 0099 (un checker incapaz
  de refutar convierte el gate en rubber-stamp). Regla normativa intacta; el "por que" no viaja al
  adoptante, que es justo lo que sostiene la regla bajo presion.
- RES-4: "strong-capability" no esta definido ni es verificable en el template (auto-declarable). El
  enforcement mecanico esta explicitamente FUERA de alcance en el intake; lo dejo trazado para el
  follow-up que la propia DECISION-0099 contempla.

## Recomendacion de cierre

**CHANGE-REQUIRED (NO-GO).** Aceptacion 1..5 del intake: las cinco se cumplen por comportamiento; el
bloqueo es SLIP-1, defecto del texto exportado, no de los gates. Fix esperado: 1 clausula en la regla 1
(o 1 linea introductoria) en `AGENTS.template.md`; sin cambios de runtime/validador/config; sin tocar
instancias vivas.

Bucle de fix declarado (maximo 2 iteraciones antes de escalar al operador humano):
1. Remediacion por el maker (Codex) sobre `AGENTS.template.md`, solo el texto.
2. Gates afectados a re-correr en clon limpio: `validate_collaboration_state.py`,
   `scan_domain_neutrality.py`, `scan_encoding.py`, `protocol_replay.py --check-drift`,
   `test_attested_instancing.py`, `run_runtime_instantiation_cases.py`, mas la regeneracion de una
   instancia attested por defecto y grep de las 3 reglas + la clausula nueva.
3. Re-juicio del Analista ANTES del commit de cierre. Yo no cierro ni promuevo (checker-only): el flip
   `in_review -> done` y la liberacion de claims son del Arquitecto.

Nada del fondo intocable fue tocado ni evaluado (config 2E35F26E, epoch 1.14.0, N=500, N=6).

-- Analista (checker adversarial independiente), 2026-07-24 03:30 (UTC+0200).
