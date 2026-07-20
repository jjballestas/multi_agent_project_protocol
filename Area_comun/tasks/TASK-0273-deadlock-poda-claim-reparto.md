---
task_id: TASK-0273
title: "[HIGIENE] Deshacer el deadlock poda-vs-claim: el gate de poda AVISA en local (no bloquea), la poda corre COORDINADA en el checkpoint del Arquitecto, y el CI la exige antes de integrar"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0020]
linked_decisions: [DECISION-0103, DECISION-0020]
file: Area_comun/tasks/TASK-0273-deadlock-poda-claim-reparto.md
intake:
  type: infra
  goal: Resolver el deadlock estructural poda-vs-claim (DIRECTIVA del Operador 2026-07-20) aplicando el MISMO reparto que E6-A, (1) el gate de poda del hook AVISA en local y NO bloquea el commit -- una poda vencida no es estado invalido ni drift, es un umbral de higiene, y bloquear a todo el equipo por mantenimiento es desproporcionado; (2) la poda se ejecuta COORDINADA en el checkpoint de higiene del Arquitecto, momento de quietud que YA existe (arbol limpio y claims liberados por construccion), con barrera explicita a los peers solo como excepcion; (3) el CI la EXIGE antes de integrar, donde el committer no alcanza. Motivo verificado, para commitear hay que podar, podar escribe en Area_comun/state y mailbox, esas rutas estan bajo claim vivo y legitimo -> nadie commitea; y el bucle se realimenta porque el aborto deja residuo staged que aborta al exec siguiente. El deadlock aparece justo en los periodos de MAS actividad.
  acceptance:
    - El hook en LOCAL emite AVISO claro cuando la poda esta vencida (que correr, por que) y NO aborta el commit por esa causa; el resto de chequeos del hook siguen bloqueando igual (validate del snapshot, drift de guia).
    - El CI EXIGE poda al dia antes de integrar (paso explicito en .github/workflows/validate.yml, fallo rojo con mensaje accionable); asi la degradacion local queda acotada por el enforcement duro.
    - Procedimiento de poda COORDINADA documentado para el checkpoint del Arquitecto (precondiciones verificables, cero claims activos y arbol limpio; barrera a peers declarada solo como excepcion) en la doc del protocolo y en la skill correspondiente si aplica.
    - MEDICION ya disponible (aportada en el registro, ver cuerpo): prune_state --apply tarda 86.7-89.1 s incluso SIN poda vencida; --check 0.31-0.61 s. El diseno DEBE tener en cuenta que la coordinacion NO es gratis, e incluir un camino no-op barato: si no hay nada que podar, --apply debe salir en tiempo comparable a --check (hoy paga el ciclo completo de transaccion aunque no haya trabajo). Esa optimizacion del camino no-op entra en el acceptance.
    - Espejo born-operational + entrada al conjunto adoptable (leccion .githooks: si no viaja, no es del protocolo).
    - Guardas intactas, claim-como-lock, validate y drift NO se relajan; solo cambia quien bloquea por una tarea de mantenimiento.
  verification_cmd:
    - Prueba en sandbox, commit con poda vencida -> AVISO y commit PASA; commit con estado invalido -> sigue abortando
    - CI, job que falla en rojo con poda vencida (evidencia del run o simulacion local del paso)
    - Medicion post-fix de prune_state --apply en camino no-op (objetivo, comparable a --check)
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - .githooks/pre-commit
    - scripts/prune_state.py
    - .github/workflows/validate.yml
    - Area_comun/protocol/
    - scripts/new_instance.py
  out_of_scope:
    - El seen-burn y el rollback del residuo de un exec abortado - FUERA (es TASK-0272; esta unidad evita que los abortos SE PRODUZCAN por deadlock, 0272 evita que quemen el mensaje cuando ocurren).
    - Relajar claim-como-lock, validate o drift - PROHIBIDO.
    - Unidades RESERVADAS del preregistro N=6 - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: medium
  estimate: M
---

# TASK-0273 - Deadlock poda-vs-claim: reparto aviso/coordinacion/CI

Origen: DIRECTIVA del Operador (MSG-20260720-Operador-to-Arquitecto-DIRECTIVA-deadlock-
poda-reparto) tras el incidente reproducido del 20-jul, en el que el Arquitecto quedo
sin salida gobernada (hook exigia poda; poda bloqueada por claim vivo de Codex) y tuvo
que usar un bypass declarado de un commit con los gates de fondo verificados a mano.

## MEDICION PEDIDA POR EL OPERADOR (aportada antes del GO)

Medido en ventana quieta, cero claims activos, arbol gobernado limpio, dos corridas:

| comando | tiempo | notas |
|---|---|---|
| `prune_state --check` | 0.307 s / 0.612 s | barato, ya conocido |
| `prune_state --apply` (poda NO vencida) | **89.055 s** y **86.732 s** | camino no-op: aun asi paga el ciclo completo |

Hallazgo relevante para el diseno: el `--apply` cuesta ~87-89 s **aunque no haya nada
que podar** -- ejecuta la maquinaria transaccional completa (claim acquire, intent,
release, materializacion) en vez de salir barato al detectar que no procede. Es decir,
la coordinacion NO es gratis, y una parte del coste es evitable. Por eso el acceptance
incluye el camino no-op barato ademas del reparto.

Consecuencia practica: con este coste, atar la poda al checkpoint (una vez por ciclo de
coordinacion) es claramente mejor que dispararla por umbral en medio del trabajo, y el
aviso-no-bloqueo evita que ese minuto y medio caiga sobre el commit de cualquiera.
