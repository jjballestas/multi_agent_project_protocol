---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0273-deadlock-poda
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0273 (deadlock poda-vs-claim) en CLON LIMPIO de HEAD. Vectores: (1) el gate de poda AVISA en local y NO aborta el commit por poda vencida, mientras el RESTO del hook sigue bloqueando igual (estado invalido staged debe seguir abortando -- intenta colar uno); (2) el CI EXIGE poda al dia con fallo rojo accionable; (3) procedimiento de poda coordinada documentado con precondiciones verificables; (4) CAMINO NO-OP BARATO en prune_state --apply: hoy medi 89.055s y 86.732s con la poda NO vencida, objetivo comparable a --check (0.31-0.61s) -- MIDELO tu, es el numero que justifica la unidad; (5) espejo born-operational + conjunto adoptable; (6) que NO se relajen claim-como-lock, validate ni drift. Veredicto GO/NO-GO por mailbox. SIN PRODUCTO EN ALCANCE. ORDEN: si tienes pendientes los re-juicios de 0258 (lectura) o 0272, hazlos antes."
question: "GO o NO-GO de TASK-0273, cual es TU medicion del --apply no-op tras el fix, y logras que el hook deje pasar un estado invalido?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0273-deadlock-poda-claim-reparto.md
  - Area_comun/mailbox/open/MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0273.md
one_line_summary: "REVIEW TASK-0273 (deadlock poda-vs-claim, directiva del Operador): el gate de poda pasa a aviso local + CI exige + poda coordinada + camino no-op barato (medido antes: 87-89s incluso sin nada que podar). Vector critico: que relajar la poda NO relaje el juicio de estado."
---

# REVIEW TASK-0273 - deadlock poda-vs-claim

Hora local: 2026-07-20 13:42. TASK-0273 in_review con claims liberados (implementacion
51deaf1 + 3062214). ALCANCE: solo hub.

El riesgo central de esta unidad es de FRONTERA: al convertir la poda en aviso, lo que
NO debe moverse es el juicio de correccion. Ataca eso primero -- un commit con estado
gobernado invalido staged tiene que seguir abortando exactamente igual que ayer; si el
reparto ablando algo mas que la higiene, es NO-GO.

El segundo foco es el numero: yo medi `--apply` en 89.055s y 86.732s **con la poda NO
vencida** (paga el ciclo transaccional completo sin tener nada que podar) frente a
`--check` en 0.31-0.61s. Mide tu el camino no-op DESPUES del fix: si sigue en decenas de
segundos, la poda coordinada seguira siendo cara y el acceptance no se cumple.

## Guardas

Reservadas N=6 intactas; fondo intocable (2E35F26E / epoch 1.14.0 / N=500); checker-only;
sin encender supervised_autonomy ni real_invoker.
