---
id: TASK-0367
title: El nucleo neutral trae la identidad de esta instancia cableada como valor por defecto, y una instancia recien parida la hereda
status: in_review
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
created: 2026-08-12
intake:
  type: fix
  goal: >
    El paso 50 del job `validate` (`examples/runtime_instantiation_cases`) tiene DOS causas, no una.
    La primera -- el aborto por marcadores sin resolver -- la mata TASK-0350. Con esa muerta, el
    runner llega mas lejos y descubre la segunda: la instancia GENERADA no pasa el escaner de
    neutralidad porque el nucleo trae el nombre del arquitecto de ESTA instancia cableado como valor
    por defecto en cuatro sitios (`runtime/context.py:15` en DEFAULT_AGENT_ROLES, `runtime/router.py:438`
    como retorno de ultimo recurso, `scripts/prune_state.py:252` en el texto del centinela y `:442`
    como defecto al leer el config; el arnes de peones del tier runtime anade el suyo). No es un
    fallo introducido: TASK-0350 solo toco `scripts/new_instance.py` y el runner de casos, asi que
    los cuatro son anteriores y llevaban ocultos detras del primer aborto. Es la frontera dura de
    AGENTS.md s.4 medida por conducta: un equipo que instancia el protocolo hereda por defecto la
    identidad del equipo que lo escribio.
  acceptance:
    - "AC1 (la poblacion se deriva, no se enumera): el conjunto de sitios corregidos sale de correr
      el escaner de neutralidad sobre una instancia GENERADA, no de la lista de cuatro que este
      enunciado cita. Si el escaner encuentra mas, entran; si uno de los cuatro no aparece al medir,
      se declara por que. La lista de arriba es el sintoma observado, no el criterio."
    - "AC2 (defecto que no es identidad): cada sitio se resuelve dando al nucleo un valor por defecto
      que no nombra a ningun participante concreto, o haciendo que el valor venga del config de la
      instancia. Se declara para cada uno cual de las dos vias se eligio y por que. Sustituir un
      nombre propio por otro nombre propio no acredita."
    - "AC3 (el negativo discrimina): tras el cambio, inyectar la identidad de un participante concreto
      en el nucleo vuelve a poner rojo el escaner sobre la instancia generada. Se acredita
      inyectandola y mirando el exit code. Un cambio que ponga verde el caso y ademas deje pasar la
      identidad inyectada no acredita nada."
    - "AC4 (la instancia sigue naciendo operativa): la instancia generada conserva sus roles reales
      -- los que su propio `protocol.config.json` declara -- y sus flujos siguen funcionando. Se
      acredita con el runner de casos, no afirmando que no se rompio nada."
    - "AC5 (paso 50 verde, citado): `case_coordination_default_and_flag` y
      `case_runtime_tier_scaffolds_motor_gates_ci_off` pasan en checkout limpio, con la salida del
      runner antes y despues por exit code. Este es el AC que cierra el paso 50 de verdad: TASK-0350
      mato la primera causa, esta mata la segunda."
  verification_cmd:
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - runtime/context.py
    - runtime/router.py
    - scripts/prune_state.py
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El aborto por marcadores sin resolver: es TASK-0350, la primera causa del mismo paso."
    - "Los quince rojos de causa `obstacles`: son TASK-0347, que declara el paso 50 fuera de su
      alcance precisamente por esto."
    - "Renombrar actores en la instancia VIVA de este repo: aqui el arquitecto se llama Claude por su
      propio config y eso es correcto. Lo que se corrige es el DEFECTO del nucleo, no la instancia."
  risk: medium
  estimate: S
---

# TASK-0367 -- la segunda causa del paso 50

## Como aparecio

TASK-0350 mato el aborto por marcadores. Al correr el runner con esa causa muerta, el paso 50 llega
mas lejos y falla en otro sitio:

    case_coordination_default_and_flag
      runtime/context.py:15: Claude
      runtime/router.py:438: Claude
      scripts/prune_state.py:252: Claude
      scripts/prune_state.py:442: Claude

    case_runtime_tier_scaffolds_motor_gates_ci_off
      (los cuatro anteriores) + scripts/harness/peer_mailbox_cron.ps1:553: Claude

Es el patron de la cascada: **una puerta que aborta pronto oculta lo que hay detras**. Mientras el
paso 50 moria en el chequeo de marcadores, estos cuatro no podian verse. No son nuevos y no los
introdujo TASK-0350 -- su diff toco `scripts/new_instance.py` y el runner de casos, nada mas.

## Por que no es de TASK-0347 ni de TASK-0350

TASK-0347 particiona los diecisiete rojos del job y **declara el paso 50 fuera de su alcance**,
asignandolo por nombre a TASK-0350. TASK-0350, a su vez, tiene una causa distinta y acotada. El
residuo no encajaba en ninguna de las dos: sin esta tarea se quedaba sin dueno, con las dos partes
senalandose la una a la otra. Ese es el modo exacto en que un rojo sobrevive meses.

## Lo que esta realmente en juego

No es un escaner quisquilloso. `DEFAULT_AGENT_ROLES` en el nucleo dice que el arquitecto por defecto
se llama Claude, y `router.py` lo devuelve como ultimo recurso cuando no encuentra a nadie. Un equipo
que instancie el protocolo hereda esa identidad sin pedirla. La frontera de AGENTS.md s.4 no la mide
el texto del contrato: la mide lo que sale de `new_instance.py`.

## Implementation evidence

The pre-change generated-instance scan derived four findings for the coordination tier and five for
the runtime tier: `runtime/context.py`, `runtime/router.py`, two sites in `scripts/prune_state.py`, and
the additional runtime-tier site in `scripts/harness/peer_mailbox_cron.ps1`. No cited site disappeared
from the measured population and no additional site was reported.

Each correction uses one of the two accepted neutral paths:

- `runtime/context.py` uses generic role identifiers for the no-config fallback. A generated instance
  still reads its concrete architect, implementer, and human owner from `protocol.config.json`.
- `runtime/router.py` uses the generic `architect` role identifier only when the registry contains no
  orchestrator or architect. Configured registries still return their declared concrete agent id.
- `scripts/prune_state.py` describes project memory without naming a participant, and derives the actor
  from `agent_roles.architect` with the generic role identifier only as the absent-config fallback.
- `scripts/harness/peer_mailbox_cron.ps1` derives executable discovery from the configured `PeerId`.

The permanent behavioral negative generates an instance, injects its configured architect identity
into `runtime/context.py`, executes that generated instance's neutrality scanner, and requires a
nonzero exit naming both the identity and path. The operational probe imports the generated runtime,
loads the three declared core roles into its registry, and proves escalation selects a declared role.

Before the change, `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`
exited 1 and named the two requested cases with the derived findings above. After the change it exits
0 with `OK: runtime instantiation cases passed (10 + ps1 parity when available).` The expected
placeholder-negative diagnostic remains part of the passing runner and is not a case failure.

Exact implementation commit `503303c9` passed the runtime-instantiation runner, encoding scan,
domain-neutrality scan, collaboration validator, Python compilation, diff check, and empty tracked
status in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/task0367-clean-503303c9`. Codex did not review or
ratify the implementation.

## Remediation evidence

The distinguishing criterion is behavioral: a participant identity attributes a protocol action or
selects a registered actor, while a tool name selects an executable contract installed on the host.
`PeerId` belongs to the first category; `AgentProvider` selects the second. The four runtime/context,
router, and pruning changes concern actor attribution or generic absent-config language and therefore
remain correct. `Get-AgentExecutable` concerns the host command contract, so it now chooses the
provider-specific command supplied through runtime environment configuration.

The mailbox retry suite now executes `Get-AgentExecutable` for both asymmetric peer/provider pairs.
It requires Codex/Codex to resolve a fixture `codex.exe`, requires Analista/Anthropic to resolve a
fixture `claude.ps1`, and kills a participant-name mutant by showing that it no longer preserves the
Analista resolution. The test prints both resolved binaries, making the evidence about behavior
rather than merely the spelling of the production literal.

## Remediation r2 evidence

The documented zero-configuration startup contract is restored: absent explicit environment
overrides, `Auto`/`Codex` resolves `codex` and `Anthropic` resolves `claude` from `PATH`; explicit
provider-command environment variables still override those defaults. The behavioral probe clears
both variables before resolving fixture commands, so it exercises the same no-`-AgentExe` path as
the README instead of inheriting fixture configuration. It runs only through the explicit
`--task0367-provider-only` entry point, uses the designated external scratch root, and removes its
private fixtures. The full retry suite therefore never receives TASK-0367 residue or timing effects.

The full retry suite currently exits 1 at the TASK-0343 baseline (`baseline=0/3`). The same command
at untouched pre-remediation commit `fbeb215e` produces the identical `baseline=0/3` result in a
detached worktree, while the focused TASK-0367 provider probe exits 0. This is measured attribution,
not a claim that the red is pre-existing without a control point.

The AC3 negative is intentionally narrow: it proves that the generated instance scanner rejects a
concrete identity declared by that instance when injected into core. It does not prove detection of
undeclared adopter identities; that broader population and enforcement gap belongs to TASK-0372.
