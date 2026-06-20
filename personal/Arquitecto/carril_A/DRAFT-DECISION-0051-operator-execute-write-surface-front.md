# DECISION-0051 (DRAFT) - Superficie de escritura EXECUTE del operador desde el front

- status: proposed (DRAFT en personal/Arquitecto; NO promovido; espera ratificacion del operador)
- type: protocol-surface / governance
- proposed_by: Arquitecto
- ratifies: Operador (humano)
- relates: SPEC-0086 (extension), DECISION-0040 (gate dataset / PII), DECISION-0022/0028 (#4 enforce single-writer), TASK-0118 (DEF-PII gate)
- depends_on_intent_kind_change: NO

## Contexto

El operador pide un PULL real: conducir nova.budget desde el front montando historias/requisitos
que entren al pipeline SDD (MSG-20260620-Operador-to-Arquitecto-GO-front-intake-historias). Hoy el
front es READ-ONLY + dry_run: nunca escribio el ledger. La capacidad pedida (wizard de intake que
emite un requisito GOBERNADO via submit_intent EXECUTE) introduce, por primera vez, una **superficie
de escritura del operador al ledger desde la UI**. Por CLAUDE.md regla 2 / AGENTS.md s4, todo cambio
de superficie de escritura o de boundary exige DECISION antes de SPEC/codigo.

## Las dos preguntas de metodo (resueltas)

### 1. Nuevo intent kind? -> NO.
El intake (historia/requisito) se modela como un **`task_upsert`** de una tarea con
`type: requirement` (semilla, status `proposed`, author/owner = `Operador`), NO como un kind nuevo.
Razones:
- Reusa kind/capability/required_scopes existentes (`task_upsert` ya escribe TASK_INDEX +
  PROJECT_STATE#active_tasks + el archivo de tarea), idempotente via `idempotency_key`.
- NO toca `runtime/submit_intent.py:INTENT_TYPES` -> la superficie del runtime queda intacta ->
  **sin re-genesis-boundary, epoca #4 1.14.0 PINNED intacta** (un kind nuevo no toca el config, pero
  evitarlo mantiene minima la superficie auditada y el diff de revision adversarial).
- El requisito aterriza como artefacto gobernado y trazable en el mismo ledger atestado (dataset).

### 2. Nueva superficie de escritura del operador? -> SI. Es el nucleo de esta DECISION.
Se habilita EXECUTE del front, **acotado al intake** en esta fase, con `actorId: "Operador"`. Reglas:
- El front NO escribe estado/ledger directo: TODA escritura pasa por `runtime/submit_intent.py`
  (el server ya lo enruta; `directLedgerWrites:false` se mantiene como contrato y prueba negativa).
- EXECUTE exige confirmacion explicita y visible (`confirm:SUBMIT_INTENT`); sin confirm -> 409, no
  escribe (prueba negativa obligatoria).
- Atribucion honesta: el actor del intent es `Operador` (no `Arquitecto`); el dataset muestra la
  autoria real del operador. (El default `actorId:"Arquitecto"` del server se corrige para intake.)
- Roles intactos: operador = "que" + GO; el intake es la SEMILLA, NO la SPEC. El **Arquitecto**
  consume el requisito y autora la SPEC (AC+test_plan, neutralidad, revision adversarial) bajo SDD,
  maker=Codex/checker=Arquitecto. El handoff intake->SPEC es explicito.

## Guarda PII (innegociable)
- El texto libre de la historia (narrativa, intencion de aceptacion) puede traer PII de terceros
  (NIT, razon social, payloads SQL) en historias de nova.budget. Se REDACTA en todo plano publicable
  (preview, vista, export) y va por canal ASCII a lo que se escribe al protocolo, coherente con
  DECISION-0040. TASK-0118/DEF-PII sigue como GATE antes de captura viva de PII real; el intake
  habilitado ahora opera con redaccion best-effort + confirmacion del operador, NO levanta ese gate.

## Boundaries que esta DECISION NO mueve
- No cambia INTENT_TYPES del runtime. No habilita otros kinds desde el front (sigue solo lo que la
  SPEC acote; resto del EXECUTE permanece cerrado). No toca #4/config pinned. Neutralidad de dominio
  intacta: el codigo vive solo en Zeus-protocol; el core del protocolo no recibe terminos de negocio.

## Rollback
Deshabilitar la accion gobernada de intake en el front (flag/quitar de GOVERNED_ACTIONS) restaura el
estado read-only+dry_run; el runtime no cambia, asi que no hay nada que revertir alli.
