---
decision_id: DECISION-0051
title: Superficie de escritura EXECUTE del operador desde el front (intake gobernado de requisitos) - intake = task_upsert requirement, sin nuevo intent kind, #4 epoca 1.14.0 pinned
status: accepted
ratified_at: 2026-06-20
date: 2026-06-20
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0049, DECISION-0050, DECISION-0040, DECISION-0022]
phase: P2
---

# DECISION-0051 - Superficie de escritura EXECUTE del operador desde el front

> ACCEPTED por el operador (2026-06-20, GO de ratificacion MSG-20260620-Operador-to-Arquitecto-GO-ratifica-libera-TASK-0133).
> Gate de superficie de escritura (CLAUDE.md regla 2 / AGENTS.md s4). NO toca el config pinned
> (#4 epoca 1.14.0; INTENT_TYPES del runtime intacto). Codigo solo en Zeus-protocol; core neutral.

## Contexto

El operador pide un PULL real: conducir nova.budget desde el front montando historias/requisitos
que entren al pipeline SDD. Hoy el front es READ-ONLY + dry_run: nunca escribio el ledger. La
capacidad pedida (wizard de intake que emite un requisito GOBERNADO via submit_intent EXECUTE)
introduce, por primera vez, una **superficie de escritura del operador al ledger desde la UI**.

## Las dos preguntas de metodo (resueltas)

### 1. Nuevo intent kind? -> NO.
El intake se modela como **`task_upsert`** de una tarea con `type: requirement` (semilla, status
`proposed`, author/owner = `Operador`), NO como un kind nuevo. Reusa kind/capability/required_scopes
existentes; idempotente via `idempotency_key`. NO toca `runtime/submit_intent.py:INTENT_TYPES` ->
superficie del runtime intacta -> **sin re-genesis-boundary, epoca #4 1.14.0 PINNED intacta**.

### 2. Nueva superficie de escritura del operador? -> SI. Es el nucleo de esta DECISION.
Se habilita EXECUTE del front, **acotado al intake** en esta fase, con `actorId: "Operador"`. Reglas:
- El front NO escribe estado/ledger directo: TODA escritura pasa por `runtime/submit_intent.py`
  (`directLedgerWrites:false` se mantiene como contrato y prueba negativa).
- EXECUTE exige confirmacion explicita y visible (`confirm:SUBMIT_INTENT`); sin confirm -> 409, no
  escribe (prueba negativa obligatoria).
- Atribucion honesta: el actor del intent es `Operador`; el dataset muestra la autoria real.
- Roles intactos: operador = "que" + GO; el intake es la SEMILLA, NO la SPEC. El **Arquitecto**
  consume el requisito y autora la SPEC (AC+test_plan, neutralidad, revision adversarial) bajo SDD,
  maker=Codex/checker=Arquitecto. El handoff intake->SPEC es explicito.
- Patron: el intake cuelga del patron existente `governed-action` (un solo writer; dry_run preview +
  execute confirmado), NO introduce un segundo escritor ni superficie de bypass (pasada del Analista).

## Guarda PII (innegociable, ESTRUCTURAL)

El texto libre de la historia puede traer PII de terceros (NIT, razon social, payloads SQL). La
guarda es **estructural + advertencia**, NO un detector automatico (TASK-0118/DEF-PII = `proposed`,
NO existe aun): (a) separar la intencion-en-lenguaje-llano (plano publicable) del payload sensible;
(b) redactar/marcar el texto libre en todo plano publicable/exportable; (c) canal ASCII a lo que se
escribe al protocolo; (d) advertir al operador en compose y en confirm. Coherente con DECISION-0040
(dos planos). El intake opera con redaccion best-effort + confirmacion y **NO levanta el gate
TASK-0118/DEF-PII** antes de captura viva de PII real.

## Boundaries que esta DECISION NO mueve

No cambia INTENT_TYPES del runtime. No habilita otros kinds desde el front (sigue solo lo que la SPEC
acote; resto del EXECUTE permanece cerrado). No toca #4/config pinned. Neutralidad de dominio intacta
(codigo solo en Zeus-protocol; el core no recibe terminos de negocio; "proyecto destino" es dato,
no logica de dominio).

## Rollback

Deshabilitar la accion gobernada de intake en el front (quitar de GOVERNED_ACTIONS) restaura el
estado read-only+dry_run; el runtime no cambia, no hay nada que revertir alli.
